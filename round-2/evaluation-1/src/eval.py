#!/usr/bin/env python3
"""
Statistical Evaluation of LLM Calibration Methods

Comprehensive evaluation comparing thermodynamic entropy calibration against
temperature scaling and uncalibrated baselines across multiple datasets
with bootstrap confidence intervals and significance testing.

Metrics:
- Expected Calibration Error (ECE) with 95% bootstrap CI
- Brier Score with 95% bootstrap CI
- Negative Log-Likelihood (NLL) with 95% bootstrap CI
- Accuracy with 95% bootstrap CI
- Reliability diagram data
- ECE decomposition by confidence bins
- Statistical significance tests (Wilcoxon, bootstrap, Cohen's d)
"""

from loguru import logger
from pathlib import Path
import json
import sys
import numpy as np
from scipy.stats import wilcoxon, norm
from sklearn.metrics import brier_score_loss, log_loss
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

# =============================================================================
# Utility Functions
# =============================================================================

def parse_prob_string(prob_str: str) -> np.ndarray:
    """Parse probability string to numpy array."""
    return np.array(json.loads(prob_str))

def compute_ece(probs: np.ndarray, labels: np.ndarray, n_bins: int = 10) -> float:
    """
    Compute Expected Calibration Error (ECE).

    Args:
        probs: [N, C] array of predicted probabilities
        labels: [N] array of true labels
        n_bins: Number of bins for calibration

    Returns:
        ECE value
    """
    # Get predicted class and confidence
    pred_confs = np.max(probs, axis=1)
    pred_classes = np.argmax(probs, axis=1)

    # Bin by confidence
    bins = np.linspace(0, 1, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        mask = (pred_confs >= bins[i]) & (pred_confs < bins[i + 1])
        if i == n_bins - 1:  # Include right edge for last bin
            mask = (pred_confs >= bins[i]) & (pred_confs <= bins[i + 1])

        if np.sum(mask) > 0:
            # Accuracy in this bin
            bin_acc = np.mean(pred_classes[mask] == labels[mask])
            # Average confidence in this bin
            bin_conf = np.mean(pred_confs[mask])
            # Weight by fraction of samples
            weight = np.sum(mask) / len(labels)
            ece += weight * abs(bin_acc - bin_conf)

    return ece

def compute_ece_decomposition(probs: np.ndarray, labels: np.ndarray, n_bins: int = 10) -> Dict:
    """
    Compute ECE decomposition by confidence bins.

    Returns detailed per-bin statistics for diagnostic analysis.
    """
    pred_confs = np.max(probs, axis=1)
    pred_classes = np.argmax(probs, axis=1)

    bins = np.linspace(0, 1, n_bins + 1)
    decomposition = []

    for i in range(n_bins):
        mask = (pred_confs >= bins[i]) & (pred_confs < bins[i + 1])
        if i == n_bins - 1:
            mask = (pred_confs >= bins[i]) & (pred_confs <= bins[i + 1])

        if np.sum(mask) > 0:
            bin_acc = np.mean(pred_classes[mask] == labels[mask])
            bin_conf = np.mean(pred_confs[mask])
            bin_count = np.sum(mask)
            bin_ece = abs(bin_acc - bin_conf)

            decomposition.append({
                "bin_index": i,
                "bin_range": [float(bins[i]), float(bins[i + 1])],
                "count": int(bin_count),
                "accuracy": float(bin_acc),
                "confidence": float(bin_conf),
                "ece_contribution": float(bin_ece * bin_count / len(labels))
            })
        else:
            decomposition.append({
                "bin_index": i,
                "bin_range": [float(bins[i]), float(bins[i + 1])],
                "count": 0,
                "accuracy": 0.0,
                "confidence": 0.0,
                "ece_contribution": 0.0
            })

    return {"bins": decomposition}

def compute_brier_score(probs: np.ndarray, labels: np.ndarray) -> float:
    """Compute Brier Score for multi-class."""
    n_samples, n_classes = probs.shape
    # One-hot encode labels
    y_true = np.zeros((n_samples, n_classes))
    y_true[np.arange(n_samples), labels] = 1
    # Brier score is mean squared error
    return np.mean(np.sum((probs - y_true) ** 2, axis=1))

def compute_nll(probs: np.ndarray, labels: np.ndarray) -> float:
    """Compute Negative Log-Likelihood."""
    # Get probability assigned to true class
    true_class_probs = probs[np.arange(len(labels)), labels]
    # Clip to avoid log(0)
    true_class_probs = np.clip(true_class_probs, 1e-15, 1.0)
    return -np.mean(np.log(true_class_probs))

def compute_accuracy(probs: np.ndarray, labels: np.ndarray) -> float:
    """Compute accuracy."""
    pred_classes = np.argmax(probs, axis=1)
    return np.mean(pred_classes == labels)

def bootstrap_metric(metric_func, probs: np.ndarray, labels: np.ndarray,
                     n_bootstrap: int = 1000, confidence: float = 0.95,
                     **kwargs) -> Tuple[float, float, float]:
    """
    Compute metric with bootstrap confidence interval.

    Returns:
        (point_estimate, ci_lower, ci_upper)
    """
    n_samples = len(labels)
    point_estimate = metric_func(probs, labels, **kwargs)

    # Bootstrap
    bootstrap_values = []
    for _ in range(n_bootstrap):
        indices = np.random.choice(n_samples, size=n_samples, replace=True)
        bootstrap_probs = probs[indices]
        bootstrap_labels = labels[indices]
        bootstrap_values.append(metric_func(bootstrap_probs, bootstrap_labels, **kwargs))

    bootstrap_values = np.array(bootstrap_values)

    # Compute confidence interval
    alpha = (1 - confidence) / 2
    lower = np.percentile(bootstrap_values, 100 * alpha)
    upper = np.percentile(bootstrap_values, 100 * (1 - alpha))

    return point_estimate, lower, upper

def bootstrap_paired_difference(probs1: np.ndarray, probs2: np.ndarray,
                                labels: np.ndarray, metric_func,
                                n_bootstrap: int = 1000) -> Tuple[float, float, float]:
    """
    Bootstrap hypothesis test for paired difference in metrics.

    Returns:
        (observed_difference, p_value, ci_lower, ci_upper)
    """
    n_samples = len(labels)

    # Observed difference
    obs_diff = metric_func(probs1, labels) - metric_func(probs2, labels)

    # Bootstrap differences
    bootstrap_diffs = []
    for _ in range(n_bootstrap):
        indices = np.random.choice(n_samples, size=n_samples, replace=True)
        diff = metric_func(probs1[indices], labels[indices]) - metric_func(probs2[indices], labels[indices])
        bootstrap_diffs.append(diff)

    bootstrap_diffs = np.array(bootstrap_diffs)

    # P-value (two-sided)
    p_value = np.mean(np.abs(bootstrap_diffs) >= np.abs(obs_diff))

    # Confidence interval for difference
    lower = np.percentile(bootstrap_diffs, 2.5)
    upper = np.percentile(bootstrap_diffs, 97.5)

    return obs_diff, p_value, lower, upper

def cohens_d(x1: np.ndarray, x2: np.ndarray) -> float:
    """Compute Cohen's d for paired samples."""
    diff = x1 - x2
    return np.mean(diff) / np.std(diff, ddof=1)

# =============================================================================
# Main Evaluation Function
# =============================================================================

@logger.catch(reraise=True)
def main():
    # Create output directory
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)
    (output_dir / "logs").mkdir(exist_ok=True)

    # Load experiment output
    logger.info("Loading experiment output")
    with open("experiment_out.json", "r") as f:
        exp_data = json.load(f)

    # Load metadata
    with open("metadata.json", "r") as f:
        metadata = json.load(f)

    logger.info(f"Experiment: {metadata['method_name']}")
    logger.info(f"Dataset: {metadata['dataset_info']['name']}")
    logger.info(f"Number of test samples: {metadata['dataset_info']['n_test']}")

    # Extract predictions and labels from experiment output
    dataset_name = exp_data["datasets"][0]["dataset"]
    examples = exp_data["datasets"][0]["examples"]

    logger.info(f"Processing {len(examples)} examples from {dataset_name}")

    # Parse predictions
    methods = ["uncalibrated", "temperature_scaling", "thermodynamic_entropy"]
    method_probs = {}
    method_prob_keys = {
        "uncalibrated": "metadata_uncalibrated_probs",
        "temperature_scaling": "metadata_ts_probs",
        "thermodynamic_entropy": "metadata_te_probs"
    }
    labels = []

    for method in methods:
        method_probs[method] = []

    for i, example in enumerate(examples):
        # Parse true label
        true_label_str = example["output"].split(": ")[1].strip()
        true_label = int(true_label_str)
        labels.append(true_label)

        # Parse probabilities for each method
        for method in methods:
            prob_key = method_prob_keys[method]
            if prob_key in example:
                probs = parse_prob_string(example[prob_key])
                method_probs[method].append(probs)

    labels = np.array(labels)
    for method in methods:
        method_probs[method] = np.array(method_probs[method])

    logger.info(f"Loaded predictions for {len(methods)} methods")
    logger.info(f"Labels shape: {labels.shape}")
    for method in methods:
        logger.info(f"{method} probs shape: {method_probs[method].shape}")

    # Also extract logits for tradeoff analysis
    test_logits = []
    for example in examples:
        if "metadata_test_logits" in example:
            logits = parse_prob_string(example["metadata_test_logits"])
            test_logits.append(logits)
    test_logits = np.array(test_logits)
    logger.info(f"Test logits shape: {test_logits.shape}")

    # =========================================================================
    # Step 1: Compute metrics with bootstrap confidence intervals
    # =========================================================================
    logger.info("\n" + "="*60)
    logger.info("STEP 1: Computing metrics with bootstrap CI")
    logger.info("="*60)

    n_bootstrap = 1000
    results = {}

    for method in methods:
        logger.info(f"\nEvaluating {method}...")

        probs = method_probs[method]

        # ECE
        ece, ece_lower, ece_upper = bootstrap_metric(
            compute_ece, probs, labels, n_bootstrap=n_bootstrap
        )

        # Brier Score
        brier, brier_lower, brier_upper = bootstrap_metric(
            compute_brier_score, probs, labels, n_bootstrap=n_bootstrap
        )

        # NLL
        nll, nll_lower, nll_upper = bootstrap_metric(
            compute_nll, probs, labels, n_bootstrap=n_bootstrap
        )

        # Accuracy
        acc, acc_lower, acc_upper = bootstrap_metric(
            compute_accuracy, probs, labels, n_bootstrap=n_bootstrap
        )

        results[method] = {
            "ece": {"value": ece, "ci_lower": ece_lower, "ci_upper": ece_upper},
            "brier": {"value": brier, "ci_lower": brier_lower, "ci_upper": brier_upper},
            "nll": {"value": nll, "ci_lower": nll_lower, "ci_upper": nll_upper},
            "accuracy": {"value": acc, "ci_lower": acc_lower, "ci_upper": acc_upper}
        }

        logger.info(f"  ECE: {ece:.4f} [{ece_lower:.4f}, {ece_upper:.4f}]")
        logger.info(f"  Brier: {brier:.4f} [{brier_lower:.4f}, {brier_upper:.4f}]")
        logger.info(f"  NLL: {nll:.4f} [{nll_lower:.4f}, {nll_upper:.4f}]")
        logger.info(f"  Accuracy: {acc:.4f} [{acc_lower:.4f}, {acc_upper:.4f}]")

    # =========================================================================
    # Step 2: Statistical significance tests
    # =========================================================================
    logger.info("\n" + "="*60)
    logger.info("STEP 2: Statistical significance tests")
    logger.info("="*60)

    # Paired Wilcoxon Signed-Rank Test (per-sample metrics)
    logger.info("\nPaired Wilcoxon Signed-Rank Test...")

    # Compute per-sample metrics for Wilcoxon test
    for method in methods:
        probs = method_probs[method]
        # Per-sample NLL
        true_class_probs = probs[np.arange(len(labels)), labels]
        true_class_probs = np.clip(true_class_probs, 1e-15, 1.0)
        results[method]["per_sample_nll"] = -np.log(true_class_probs)

        # Per-sample accuracy (0/1)
        pred_classes = np.argmax(probs, axis=1)
        results[method]["per_sample_acc"] = (pred_classes == labels).astype(float)

    # Compare methods using Wilcoxon test
    comparisons = [
        ("temperature_scaling", "uncalibrated"),
        ("thermodynamic_entropy", "uncalibrated"),
        ("thermodynamic_entropy", "temperature_scaling")
    ]

    statistical_tests = {}

    for method1, method2 in comparisons:
        logger.info(f"\nComparing {method1} vs {method2}...")

        # Wilcoxon test on per-sample NLL
        stat, p_value_nll = wilcoxon(
            results[method1]["per_sample_nll"],
            results[method2]["per_sample_nll"],
            alternative='two-sided'
        )

        # Bootstrap hypothesis test on ECE difference
        ece_diff, p_value_ece, ece_diff_lower, ece_diff_upper = bootstrap_paired_difference(
            method_probs[method1],
            method_probs[method2],
            labels,
            compute_ece,
            n_bootstrap=1000
        )

        # Effect size (Cohen's d) for NLL difference
        nll_diff = results[method1]["per_sample_nll"] - results[method2]["per_sample_nll"]
        nll_diff_ref = np.zeros_like(nll_diff)  # Under null hypothesis
        effect_size = cohens_d(results[method1]["per_sample_nll"], results[method2]["per_sample_nll"])

        statistical_tests[f"{method1}_vs_{method2}"] = {
            "wilcoxon_p_value_nll": float(p_value_nll),
            "bootstrap_p_value_ece": float(p_value_ece),
            "ece_difference": float(ece_diff),
            "ece_diff_ci_lower": float(ece_diff_lower),
            "ece_diff_ci_upper": float(ece_diff_upper),
            "cohens_d_nll": float(effect_size)
        }

        logger.info(f"  Wilcoxon p-value (NLL): {p_value_nll:.4f}")
        logger.info(f"  Bootstrap p-value (ECE): {p_value_ece:.4f}")
        logger.info(f"  ECE difference: {ece_diff:.4f} [{ece_diff_lower:.4f}, {ece_diff_upper:.4f}]")
        logger.info(f"  Cohen's d (NLL): {effect_size:.4f}")

    # =========================================================================
    # Step 3: Reliability diagram data
    # =========================================================================
    logger.info("\n" + "="*60)
    logger.info("STEP 3: Generating reliability diagram data")
    logger.info("="*60)

    reliability_data = {}

    for method in methods:
        probs = method_probs[method]
        pred_confs = np.max(probs, axis=1)
        pred_classes = np.argmax(probs, axis=1)

        n_bins = 10
        bins = np.linspace(0, 1, n_bins + 1)

        bin_data = []

        for i in range(n_bins):
            mask = (pred_confs >= bins[i]) & (pred_confs < bins[i + 1])
            if i == n_bins - 1:
                mask = (pred_confs >= bins[i]) & (pred_confs <= bins[i + 1])

            if np.sum(mask) > 0:
                bin_acc = np.mean(pred_classes[mask] == labels[mask])
                bin_conf = np.mean(pred_confs[mask])
                bin_count = np.sum(mask)
            else:
                bin_acc = 0.0
                bin_conf = 0.0
                bin_count = 0

            bin_data.append({
                "bin_index": i,
                "bin_range": [float(bins[i]), float(bins[i + 1])],
                "count": int(bin_count),
                "accuracy": float(bin_acc),
                "confidence": float(bin_conf)
            })

        reliability_data[method] = bin_data

        # Also save as plot
        plot_reliability_diagram(
            probs, labels,
            method.replace("_", " ").title(),
            str(output_dir / f"reliability_{method}.png")
        )

    # =========================================================================
    # Step 4: ECE Decomposition
    # =========================================================================
    logger.info("\n" + "="*60)
    logger.info("STEP 4: ECE Decomposition Analysis")
    logger.info("="*60)

    ece_decomposition = {}

    for method in methods:
        probs = method_probs[method]
        decomp = compute_ece_decomposition(probs, labels)
        ece_decomposition[method] = decomp

        # Log top contributing bins
        bins_sorted = sorted(decomp["bins"], key=lambda x: x["ece_contribution"], reverse=True)
        logger.info(f"\n{method} - Top ECE contributors:")
        for bin_info in bins_sorted[:3]:
            if bin_info["count"] > 0:
                logger.info(f"  Bin {bin_info['bin_index']} ({bin_info['bin_range'][0]:.1f}-{bin_info['bin_range'][1]:.1f}): "
                          f"count={bin_info['count']}, acc={bin_info['accuracy']:.3f}, "
                          f"conf={bin_info['confidence']:.3f}, ece_contrib={bin_info['ece_contribution']:.4f}")

    # =========================================================================
    # Step 5: Accuracy-Calibration Tradeoff Analysis
    # =========================================================================
    logger.info("\n" + "="*60)
    logger.info("STEP 5: Accuracy-Calibration Tradeoff Analysis")
    logger.info("="*60)

    # Need to use softmax function
    from scipy.special import softmax

    # For temperature scaling, vary temperature parameter
    logger.info("\nGenerating temperature scaling tradeoff curve...")

    tradeoff_data = {}

    # Temperature scaling tradeoff
    temperatures = np.linspace(0.1, 5.0, 50)
    ts_tradeoff = {"temperatures": [], "ece": [], "accuracy": []}

    for T in temperatures:
        # Apply temperature scaling
        scaled_logits = test_logits / T
        scaled_probs = softmax(scaled_logits, axis=1)

        # Compute metrics
        ece = compute_ece(scaled_probs, labels)
        acc = compute_accuracy(scaled_probs, labels)

        ts_tradeoff["temperatures"].append(float(T))
        ts_tradeoff["ece"].append(float(ece))
        ts_tradeoff["accuracy"].append(float(acc))

    tradeoff_data["temperature_scaling"] = ts_tradeoff

    # Thermodynamic entropy tradeoff (vary T_0 parameter)
    logger.info("Generating thermodynamic entropy tradeoff curve...")

    # Load original hyperparameters
    alpha_opt = metadata["hyperparameters"]["thermodynamic_entropy"]["alpha"]

    T_0_values = np.linspace(0.1, 5.0, 50)
    te_tradeoff = {"T_0_values": [], "ece": [], "accuracy": []}

    for T_0 in T_0_values:
        # Apply thermodynamic entropy calibration with varying T_0
        # Compute probabilities at T_0
        probs_T0 = softmax(test_logits / T_0, axis=1)

        # Compute entropy and per-sample temperature
        entropy = -np.sum(probs_T0 * np.log(probs_T0 + 1e-15), axis=1)
        max_entropy = np.log(probs_T0.shape[1])
        normalized_entropy = entropy / max_entropy

        # Compute per-sample temperature
        T_sample = T_0 * (1 + alpha_opt * normalized_entropy)
        T_sample = np.clip(T_sample, 0.1, 10.0)

        # Apply temperature
        te_probs_list = []
        for i in range(len(test_logits)):
            scaled = test_logits[i] / T_sample[i]
            te_probs_list.append(softmax(scaled))

        te_probs = np.array(te_probs_list)

        # Compute metrics
        ece = compute_ece(te_probs, labels)
        acc = compute_accuracy(te_probs, labels)

        te_tradeoff["T_0_values"].append(float(T_0))
        te_tradeoff["ece"].append(float(ece))
        te_tradeoff["accuracy"].append(float(acc))

    tradeoff_data["thermodynamic_entropy"] = te_tradeoff

    # Plot tradeoff curves
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Temperature scaling
    ax1.plot(ts_tradeoff["ece"], ts_tradeoff["accuracy"], 'o-', linewidth=2)
    ax1.set_xlabel('ECE (Calibration Error)', fontsize=12)
    ax1.set_ylabel('Accuracy', fontsize=12)
    ax1.set_title('Temperature Scaling: Accuracy vs Calibration', fontsize=14)
    ax1.grid(True, alpha=0.3)

    # Thermodynamic entropy
    ax2.plot(te_tradeoff["ece"], te_tradeoff["accuracy"], 'o-', linewidth=2)
    ax2.set_xlabel('ECE (Calibration Error)', fontsize=12)
    ax2.set_ylabel('Accuracy', fontsize=12)
    ax2.set_title('Thermodynamic Entropy: Accuracy vs Calibration', fontsize=14)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(str(output_dir / "accuracy_calibration_tradeoff.png"), dpi=150)
    plt.close()

    logger.info(f"Saved tradeoff plot to {output_dir / 'accuracy_calibration_tradeoff.png'}")

    # Save tradeoff data
    tradeoff_file = output_dir / "tradeoff_data.json"
    json.dump(tradeoff_data, open(tradeoff_file, "w"), indent=2)
    logger.info(f"Saved tradeoff data to {tradeoff_file}")

    # =========================================================================
    # Step 6: Save results in exp_eval_sol_out.json format
    # =========================================================================
    logger.info("\n" + "="*60)
    logger.info("STEP 6: Saving results")
    logger.info("="*60)

    # Format results to match exp_eval_sol_out.json schema
    # Create per-example evaluations
    eval_examples = []

    for i in range(len(labels)):
        example = {
            "input": exp_data["datasets"][0]["examples"][i]["input"],
            "output": exp_data["datasets"][0]["examples"][i]["output"]
        }

        # Add per-example evaluation metrics
        for method in methods:
            probs = method_probs[method][i:i+1]
            label = labels[i:i+1]

            # Per-example NLL
            true_class_prob = probs[0, label[0]]
            true_class_prob = np.clip(true_class_prob, 1e-15, 1.0)
            example[f"eval_{method}_nll"] = float(-np.log(true_class_prob))

            # Per-example accuracy (0/1)
            pred_class = np.argmax(probs[0])
            example[f"eval_{method}_accuracy"] = float(pred_class == label[0])

            # Per-example confidence
            example[f"eval_{method}_confidence"] = float(np.max(probs[0]))

        eval_examples.append(example)

    # Aggregate metrics for metrics_agg
    metrics_agg = {}

    for method in methods:
        for metric in ["ece", "brier", "nll", "accuracy"]:
            value = results[method][metric]["value"]
            metrics_agg[f"{method}_{metric}"] = float(value)

    # Build output
    output = {
        "metadata": {
            "evaluation_name": "Statistical Evaluation of LLM Calibration Methods",
            "description": "Comprehensive comparison of thermodynamic entropy calibration vs temperature scaling and uncalibrated baseline",
            "dataset": dataset_name,
            "methods": methods,
            "n_bootstrap": n_bootstrap,
            "statistical_tests": statistical_tests,
            "ece_decomposition": ece_decomposition
        },
        "metrics_agg": metrics_agg,
        "datasets": [
            {
                "dataset": dataset_name,
                "examples": eval_examples
            }
        ]
    }

    # Save main output
    output_file = output_dir / "eval_out.json"
    output_file.write_text(json.dumps(output, indent=2))
    logger.info(f"Saved evaluation results to {output_file}")

    # Save reliability data separately for plotting
    reliability_file = output_dir / "reliability_data.json"
    json.dump(reliability_data, open(reliability_file, "w"), indent=2)
    logger.info(f"Saved reliability data to {reliability_file}")

    # Save statistical test results
    stats_file = output_dir / "statistical_tests.json"
    json.dump(statistical_tests, open(stats_file, "w"), indent=2)
    logger.info(f"Saved statistical tests to {stats_file}")

    # =========================================================================
    # Step 6: Print summary
    # =========================================================================
    logger.info("\n" + "="*60)
    logger.info("EVALUATION COMPLETE")
    logger.info("="*60)

    logger.info("\nResults Summary (with 95% CI):")
    logger.info(f"{'Method':<30} {'ECE':>12} {'Brier':>12} {'NLL':>12} {'Acc':>12}")
    logger.info("-" * 78)

    for method in methods:
        ece_val = results[method]["ece"]["value"]
        ece_ci = f"[{results[method]['ece']['ci_lower']:.4f}, {results[method]['ece']['ci_upper']:.4f}]"
        brier_val = results[method]["brier"]["value"]
        nll_val = results[method]["nll"]["value"]
        acc_val = results[method]["accuracy"]["value"]

        logger.info(f"{method:<30} {ece_val:>8.4f} {brier_val:>12.4f} {nll_val:>12.4f} {acc_val:>12.4f}")

    logger.info("\nStatistical Significance (p-values):")
    for comp, tests in statistical_tests.items():
        logger.info(f"  {comp}: Wilcoxon={tests['wilcoxon_p_value_nll']:.4f}, "
                   f"Bootstrap={tests['bootstrap_p_value_ece']:.4f}")

    return output

# =============================================================================
# Plotting Function
# =============================================================================

def plot_reliability_diagram(probs: np.ndarray, labels: np.ndarray,
                             method_name: str, output_path: str):
    """Generate reliability diagram."""
    pred_confs = np.max(probs, axis=1)
    pred_classes = np.argmax(probs, axis=1)

    n_bins = 10
    bins = np.linspace(0, 1, n_bins + 1)

    bin_accs = []
    bin_confs = []
    bin_counts = []

    for i in range(n_bins):
        mask = (pred_confs >= bins[i]) & (pred_confs < bins[i + 1])
        if i == n_bins - 1:
            mask = (pred_confs >= bins[i]) & (pred_confs <= bins[i + 1])

        if np.sum(mask) > 0:
            bin_accs.append(np.mean(pred_classes[mask] == labels[mask]))
            bin_confs.append(np.mean(pred_confs[mask]))
            bin_counts.append(np.sum(mask))
        else:
            bin_accs.append(0.0)
            bin_confs.append(0.0)
            bin_counts.append(0)

    # Plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Diagonal reference line
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Perfect calibration')

    # Reliability curve
    ax.plot(bin_confs, bin_accs, 'o-', linewidth=2, label=method_name)

    # Formatting
    ax.set_xlabel('Confidence', fontsize=14)
    ax.set_ylabel('Accuracy', fontsize=14)
    ax.set_title(f'Reliability Diagram: {method_name}', fontsize=16)
    ax.grid(True, alpha=0.3)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.legend(fontsize=12)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    logger.info(f"Saved reliability diagram to {output_path}")

if __name__ == "__main__":
    main()
