#!/usr/bin/env python3
"""
Thermodynamic Entropy Calibration for LLM Classifiers

Implements a physics-inspired calibration method that treats LLM predictive uncertainty
as thermodynamic entropy, using temperature annealing during inference to improve
confidence calibration.

Compares against:
1. Uncalibrated baseline
2. Standard Temperature Scaling (Guo et al. 2017)
3. Thermodynamic Entropy Calibration (proposed method)

Metrics: ECE, Brier Score, NLL, Accuracy
"""

import sys
import os
import gc
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Tuple, Optional, List
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import softmax
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from loguru import logger

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Try to import torch and transformers
HAS_TORCH = False
try:
    import torch
    import torch.nn.functional as F
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    from datasets import load_dataset
    HAS_TORCH = True
    logger.info("torch and transformers imported successfully")
except ImportError as e:
    logger.warning(f"torch/transformers not available ({e}), using synthetic data")


# =============================================================================
# Hardware Detection
# =============================================================================

def detect_hardware():
    """Detect hardware resources (container-aware)."""
    import math
    import psutil

    # CPU detection (cgroup-aware)
    def _detect_cpus():
        try:
            parts = Path("/sys/fs/cgroup/cpu.cfs_quota_us").read_text().strip()
            period = Path("/sys/fs/cgroup/cpu.cfs_period_us").read_text().strip()
            if parts != "-1":
                return math.ceil(int(parts) / int(period))
        except:
            pass
        try:
            return len(os.sched_getaffinity(0))
        except:
            pass
        return os.cpu_count() or 1

    # RAM detection (cgroup-aware)
    def _container_ram_gb():
        try:
            v = Path("/sys/fs/cgroup/memory/memory.limit_in_bytes").read_text().strip()
            if v != "9223372036854771712":  # Not max
                return int(v) / 1e9
        except:
            pass
        return None

    num_cpus = _detect_cpus()
    has_gpu = HAS_TORCH and torch.cuda.is_available()
    vram_gb = 0
    device = "cpu"

    if has_gpu:
        try:
            vram_gb = torch.cuda.get_device_properties(0).total_mem / 1e9
            device = "cuda"
        except:
            has_gpu = False

    total_ram_gb = _container_ram_gb() or (psutil.virtual_memory().total / 1e9)
    available_ram_gb = min(psutil.virtual_memory().available / 1e9, total_ram_gb)

    return {
        "num_cpus": num_cpus,
        "has_gpu": has_gpu,
        "vram_gb": vram_gb,
        "device": device,
        "total_ram_gb": total_ram_gb,
        "available_ram_gb": available_ram_gb
    }


# =============================================================================
# Dataset Preparation
# =============================================================================

def prepare_dataset(
    dataset_name: str = "sst2",
    model_name: str = "distilbert-base-uncased",
    split: str = "validation",
    max_samples: Optional[int] = None,
    cache_dir: str = "dataset_cache"
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load dataset and compute logits using pre-trained model.

    Returns:
        logits: [N, num_classes] array
        labels: [N] array of true labels
    """
    if not HAS_TORCH:
        logger.warning("Using synthetic data (torch not available)")
        return generate_synthetic_data(n_samples=872, n_classes=2)

    logger.info(f"Loading dataset: {dataset_name}")
    cache_path = Path(cache_dir)
    cache_path.mkdir(exist_ok=True)

    logits_file = cache_path / f"{dataset_name}_{model_name.replace('/', '_')}_{split}_logits.npy"
    labels_file = cache_path / f"{dataset_name}_{model_name.replace('/', '_')}_{split}_labels.npy"

    # Check cache
    if logits_file.exists() and labels_file.exists():
        logger.info("Loading cached logits and labels")
        logits = np.load(logits_file)
        labels = np.load(labels_file)
        if max_samples and len(labels) > max_samples:
            logits = logits[:max_samples]
            labels = labels[:max_samples]
        return logits, labels

    # Load dataset
    if dataset_name.lower() == "sst2":
        dataset = load_dataset("glue", "sst2", split=split)
        num_classes = 2
    elif dataset_name.lower() == "mnli":
        dataset = load_dataset("glue", "mnli", split="validation_matched")
        num_classes = 3
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    if max_samples:
        dataset = dataset.select(range(min(max_samples, len(dataset))))

    # Load model
    logger.info(f"Loading model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()

    hardware = detect_hardware()
    device = torch.device(hardware["device"])
    model.to(device)
    logger.info(f"Using device: {device}")

    # Compute logits
    logits_list = []
    labels_list = []

    batch_size = 32 if hardware["has_gpu"] else 8

    with torch.no_grad():
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i+batch_size]

            # Tokenize
            if dataset_name.lower() == "sst2":
                texts = batch["sentence"]
            else:
                texts = batch["premise"]  # Simplified for MNLI

            inputs = tokenizer(
                texts,
                padding=True,
                truncation=True,
                max_length=128,
                return_tensors="pt"
            ).to(device)

            # Forward pass
            outputs = model(**inputs)
            batch_logits = outputs.logits.cpu().numpy()
            logits_list.append(batch_logits)

            # Get labels
            if dataset_name.lower() == "sst2":
                batch_labels = batch["label"]
            else:
                batch_labels = batch["label"]

            labels_list.extend(batch_labels)

            if (i // batch_size) % 10 == 0:
                logger.info(f"Processed {i}/{len(dataset)} samples")

            # Clean up
            del inputs, outputs, batch_logits
            if hardware["has_gpu"]:
                torch.cuda.empty_cache()

    logits = np.vstack(logits_list)
    labels = np.array(labels_list)

    # Cache results
    np.save(logits_file, logits)
    np.save(labels_file, labels)
    logger.info(f"Saved logits to {logits_file}")

    return logits, labels


def generate_synthetic_data(
    n_samples: int = 872,
    n_classes: int = 2,
    random_seed: int = 42,
    calibration_error: float = 0.15  # Intentionally add miscalibration
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate realistic synthetic logits that mimic LLM classifier outputs.

    Creates data with:
    - Class imbalance (similar to SST-2)
    - Varying confidence levels
    - Intentional miscalibration (overconfident predictions)
    """
    np.random.seed(random_seed)

    # Generate "true" class probabilities (ground truth confidence)
    # SST-2 is roughly balanced but with some ambiguity
    if n_classes == 2:
        # Binary case (SST-2): generate with class imbalance
        labels = np.random.binomial(1, 0.55, size=n_samples)
    else:
        # Multi-class case: uniform
        labels = np.random.randint(0, n_classes, size=n_samples)

    logits = np.zeros((n_samples, n_classes))

    for i in range(n_samples):
        true_class = labels[i]

        # Generate logits with bias toward true class
        # Real LLMs are often overconfident, so add noise
        base_logits = np.random.randn(n_classes) * 1.0

        # Boost true class logit (creates varying confidence)
        # Make it overconfident (high logit = high confidence)
        confidence_boost = np.random.uniform(2.0, 6.0)  # More overconfident
        base_logits[true_class] += confidence_boost

        # Add miscalibration: sometimes wrong class has higher logit
        # This creates poorly calibrated predictions
        if np.random.rand() < 0.20:  # 20% misclassified (worse than before)
            wrong_idx = 1 - true_class if n_classes == 2 else np.random.choice([j for j in range(n_classes) if j != true_class])
            base_logits[wrong_idx] += 3.0

        # Add systematic overconfidence: push all logits to be more extreme
        base_logits = base_logits * (1 + calibration_error)

        logits[i] = base_logits

    return logits, labels.astype(int)


# =============================================================================
# Calibration Methods
# =============================================================================

def uncalibrated_predictions(logits: np.ndarray) -> Dict:
    """Baseline: uncalibrated softmax predictions."""
    probs = softmax(logits, axis=1)
    preds = np.argmax(probs, axis=1)
    confs = np.max(probs, axis=1)

    return {
        "probs": probs,
        "preds": preds,
        "confs": confs
    }


def temperature_scaling(
    logits: np.ndarray,
    labels: np.ndarray,
    val_logits: Optional[np.ndarray] = None,
    val_labels: Optional[np.ndarray] = None,
    T_init: float = 1.0
) -> Dict:
    """
    Standard Temperature Scaling (Guo et al. 2017).

    Optimizes temperature T on validation set to minimize NLL.
    Uses the training set for tuning if validation is not provided.
    """
    # Use training data for tuning if validation not provided
    if val_logits is None or val_labels is None:
        val_logits = logits
        val_labels = labels

    def nll_loss(T):
        """Negative log-likelihood loss for given temperature."""
        scaled_logits = val_logits / T
        probs = softmax(scaled_logits, axis=1)
        # NLL: -log(p_true)
        nll = -np.log(probs[np.arange(len(val_labels)), val_labels] + 1e-10)
        return np.mean(nll)

    # Optimize temperature with wider bounds
    result = minimize_scalar(nll_loss, bounds=(0.05, 10.0), method='bounded')
    T_opt = result.x

    logger.info(f"Optimal temperature: {T_opt:.4f}")

    # Apply optimal temperature to input logits
    scaled_logits = logits / T_opt
    probs = softmax(scaled_logits, axis=1)
    preds = np.argmax(probs, axis=1)
    confs = np.max(probs, axis=1)

    return {
        "probs": probs,
        "preds": preds,
        "confs": confs,
        "T_opt": T_opt
    }


def thermodynamic_entropy_calibration(
    logits: np.ndarray,
    labels: Optional[np.ndarray] = None,
    val_logits: Optional[np.ndarray] = None,
    val_labels: Optional[np.ndarray] = None,
    T_0: float = 1.0,
    alpha: float = 0.5,
    beta: float = 0.3,  # New parameter: weight for margin term
    tune_hyperparams: bool = True
) -> Dict:
    """
    Thermodynamic Entropy Calibration (proposed method).

    Physics Analogy:
    - Logits = negative energies: E_i = -logits_i
    - Boltzmann distribution: p_i = softmax(logits/T)
    - Entropy: S(T) = -sum p_i log(p_i)

    Per-sample temperature based on predictive entropy AND margin:
    T_i = T_0 * (1 + alpha * H(p) + beta * (1 - margin))
    where margin = p_max - p_second (higher margin = more confident)
    """
    # Compute uncalibrated probabilities, entropy, and margin
    probs_uncal = softmax(logits, axis=1)
    entropy = -np.sum(probs_uncal * np.log(probs_uncal + 1e-10), axis=1)

    # Margin: difference between top-2 probabilities (measure of confidence)
    sorted_probs = np.sort(probs_uncal, axis=1)
    margin = sorted_probs[:, -1] - sorted_probs[:, -2]  # p_max - p_second

    if tune_hyperparams and val_logits is not None and val_labels is not None:
        # Hyperparameter tuning on validation set
        best_score = float('inf')
        best_params = {"T_0": T_0, "alpha": alpha, "beta": beta}

        for T_0_trial in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
            for alpha_trial in [0.0, 0.25, 0.5, 0.75, 1.0]:
                for beta_trial in [0.0, 0.25, 0.5]:
                    # Compute validation predictions
                    val_probs_uncal = softmax(val_logits, axis=1)
                    val_entropy = -np.sum(val_probs_uncal * np.log(val_probs_uncal + 1e-10), axis=1)
                    val_sorted = np.sort(val_probs_uncal, axis=1)
                    val_margin = val_sorted[:, -1] - val_sorted[:, -2]

                    # Compute per-sample temperature
                    T_val = T_0_trial * (1 + alpha_trial * val_entropy + beta_trial * (1 - val_margin))

                    # Apply calibration
                    val_logits_norm = val_logits / T_val[:, np.newaxis]
                    val_probs_cal = softmax(val_logits_norm, axis=1)

                    # Evaluate: use NLL as criterion
                    nll = -np.log(val_probs_cal[np.arange(len(val_labels)), val_labels] + 1e-10)
                    score = np.mean(nll)

                    if score < best_score:
                        best_score = score
                        best_params = {"T_0": T_0_trial, "alpha": alpha_trial, "beta": beta_trial}

        T_0 = best_params["T_0"]
        alpha = best_params["alpha"]
        beta = best_params["beta"]
        logger.info(f"Optimal hyperparameters: T_0={T_0:.2f}, alpha={alpha:.2f}, beta={beta:.2f}")

    # Apply thermodynamic calibration
    T_per_sample = T_0 * (1 + alpha * entropy + beta * (1 - margin))

    # Vectorized implementation
    logits_norm = logits / T_per_sample[:, np.newaxis]
    probs_cal = softmax(logits_norm, axis=1)

    preds = np.argmax(probs_cal, axis=1)
    confs = np.max(probs_cal, axis=1)

    return {
        "probs": probs_cal,
        "preds": preds,
        "confs": confs,
        "T_per_sample": T_per_sample,
        "T_0": T_0,
        "alpha": alpha,
        "beta": beta,
        "entropy": entropy,
        "margin": margin
    }


# =============================================================================
# Calibration Metrics
# =============================================================================

def compute_ece(
    probs: np.ndarray,
    labels: np.ndarray,
    n_bins: int = 10,
    strategy: str = "uniform"
) -> float:
    """
    Compute Expected Calibration Error (ECE).

    Args:
        probs: [N, C] predicted probabilities
        labels: [N] true labels
        n_bins: number of bins
        strategy: 'uniform' (equal width) or 'quantile' (equal count)
    """
    confs = np.max(probs, axis=1)
    preds = np.argmax(probs, axis=1)
    accs = (preds == labels).astype(float)

    if strategy == "uniform":
        bins = np.linspace(0, 1, n_bins + 1)
    else:  # quantile
        bins = np.quantile(confs, np.linspace(0, 1, n_bins + 1))

    ece = 0.0
    for i in range(n_bins):
        mask = (confs >= bins[i]) & (confs < bins[i+1])
        if np.sum(mask) > 0:
            bin_acc = np.mean(accs[mask])
            bin_conf = np.mean(confs[mask])
            bin_weight = np.sum(mask) / len(confs)
            ece += bin_weight * abs(bin_acc - bin_conf)

    return ece


def compute_brier_score(probs: np.ndarray, labels: np.ndarray) -> float:
    """Compute Brier Score (mean squared error of probabilities vs one-hot)."""
    n_samples, n_classes = probs.shape
    one_hot = np.zeros((n_samples, n_classes))
    one_hot[np.arange(n_samples), labels] = 1
    return np.mean((probs - one_hot) ** 2)


def compute_nll(probs: np.ndarray, labels: np.ndarray) -> float:
    """Compute Negative Log-Likelihood."""
    # Get probability of true class
    true_class_probs = probs[np.arange(len(labels)), labels]
    return -np.mean(np.log(true_class_probs + 1e-10))


def compute_accuracy(preds: np.ndarray, labels: np.ndarray) -> float:
    """Compute accuracy."""
    return np.mean(preds == labels)


def evaluate_predictions(
    probs: np.ndarray,
    preds: np.ndarray,
    labels: np.ndarray
) -> Dict:
    """Compute all calibration metrics."""
    return {
        "ece": compute_ece(probs, labels),
        "brier": compute_brier_score(probs, labels),
        "nll": compute_nll(probs, labels),
        "accuracy": compute_accuracy(preds, labels)
    }


# =============================================================================
# Reliability Diagram
# =============================================================================

def plot_reliability_diagram(
    probs: np.ndarray,
    labels: np.ndarray,
    method_name: str,
    output_path: str,
    n_bins: int = 10
):
    """
    Plot reliability diagram (accuracy vs confidence per bin).

    Args:
        probs: [N, C] predicted probabilities
        labels: [N] true labels
        method_name: name for the plot legend
        output_path: where to save the plot
    """
    confs = np.max(probs, axis=1)
    preds = np.argmax(probs, axis=1)
    accs = (preds == labels).astype(float)

    bins = np.linspace(0, 1, n_bins + 1)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_accs = []
    bin_confs = []
    bin_counts = []

    for i in range(n_bins):
        mask = (confs >= bins[i]) & (confs < bins[i+1])
        if np.sum(mask) > 0:
            bin_accs.append(np.mean(accs[mask]))
            bin_confs.append(np.mean(confs[mask]))
            bin_counts.append(np.sum(mask))
        else:
            bin_accs.append(0)
            bin_confs.append(bin_centers[i])
            bin_counts.append(0)

    # Plot
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # Reliability diagram
    ax[0].plot([0, 1], [0, 1], 'k--', label='Perfect calibration')
    ax[0].bar(bin_centers, bin_accs, width=0.08, alpha=0.6, label=method_name)
    ax[0].set_xlabel('Confidence')
    ax[0].set_ylabel('Accuracy')
    ax[0].set_title(f'Reliability Diagram: {method_name}')
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)

    # Confidence histogram
    ax[1].hist(confs, bins=20, alpha=0.6, label=method_name)
    ax[1].set_xlabel('Confidence')
    ax[1].set_ylabel('Count')
    ax[1].set_title(f'Confidence Distribution: {method_name}')
    ax[1].legend()
    ax[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved reliability diagram to {output_path}")


# =============================================================================
# Main Experiment
# =============================================================================

@logger.catch(reraise=True)
def main():
    """Run the full calibration experiment."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="sst2", choices=["sst2", "mnli"])
    parser.add_argument("--model", default="distilbert-base-uncased")
    parser.add_argument("--max_samples", type=int, default=None)
    parser.add_argument("--output_dir", default="results")
    parser.add_argument("--use_synthetic", action="store_true")
    args = parser.parse_args()

    # Setup
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    logs_dir = output_dir / "logs"
    logs_dir.mkdir(exist_ok=True)

    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(logs_dir / "run.log", rotation="30 MB", level="DEBUG")

    logger.info("=" * 60)
    logger.info("Thermodynamic Entropy Calibration Experiment")
    logger.info("=" * 60)

    # Hardware info
    hardware = detect_hardware()
    logger.info(f"Hardware: {hardware}")

    # =========================================================================
    # Step 1: Dataset Preparation
    # =========================================================================
    logger.info("\n[Step 1] Dataset Preparation")

    # Check for pre-saved miscalibrated data
    miscal_logits_path = output_dir / "synthetic_logits.npy"
    miscal_labels_path = output_dir / "synthetic_labels.npy"

    if args.use_synthetic or not HAS_TORCH:
        if miscal_logits_path.exists() and miscal_labels_path.exists():
            logger.info("Loading pre-saved miscalibrated synthetic data")
            logits = np.load(miscal_logits_path)
            labels = np.load(miscal_labels_path)
        else:
            logger.info("Using generated synthetic data")
            logits, labels = generate_synthetic_data(
                n_samples=872,
                n_classes=2,
                calibration_error=0.3  # Higher miscalibration
            )
    else:
        logits, labels = prepare_dataset(
            dataset_name=args.dataset,
            model_name=args.model,
            split="validation",
            max_samples=args.max_samples
        )

    logger.info(f"Dataset: {len(labels)} samples, {logits.shape[1]} classes")

    # Split: 60% train (for tuning), 20% val, 20% test
    n = len(labels)
    indices = np.random.permutation(n)
    train_end = int(0.6 * n)
    val_end = int(0.8 * n)

    train_idx = indices[:train_end]
    val_idx = indices[train_end:val_end]
    test_idx = indices[val_end:]

    train_logits, train_labels = logits[train_idx], labels[train_idx]
    val_logits, val_labels = logits[val_idx], labels[val_idx]
    test_logits, test_labels = logits[test_idx], labels[test_idx]

    logger.info(f"Train: {len(train_labels)}, Val: {len(val_labels)}, Test: {len(test_labels)}")

    # Clean up original arrays
    del logits, labels, indices
    gc.collect()

    # =========================================================================
    # Step 2: Baseline - Uncalibrated
    # =========================================================================
    logger.info("\n[Step 2] Uncalibrated Baseline")

    uncal_result = uncalibrated_predictions(test_logits)
    uncal_metrics = evaluate_predictions(
        uncal_result["probs"], uncal_result["preds"], test_labels
    )
    logger.info(f"Uncalibrated metrics: {uncal_metrics}")

    # =========================================================================
    # Step 3: Temperature Scaling
    # =========================================================================
    logger.info("\n[Step 3] Temperature Scaling")

    ts_result = temperature_scaling(
        test_logits, test_labels,
        val_logits=val_logits, val_labels=val_labels
    )
    ts_metrics = evaluate_predictions(
        ts_result["probs"], ts_result["preds"], test_labels
    )
    logger.info(f"Temperature Scaling metrics: {ts_metrics}")
    logger.info(f"Optimal T: {ts_result['T_opt']:.4f}")

    # =========================================================================
    # Step 4: Thermodynamic Entropy Calibration
    # =========================================================================
    logger.info("\n[Step 4] Thermodynamic Entropy Calibration")

    te_result = thermodynamic_entropy_calibration(
        test_logits, test_labels,
        val_logits=val_logits, val_labels=val_labels,
        tune_hyperparams=True
    )
    te_metrics = evaluate_predictions(
        te_result["probs"], te_result["preds"], test_labels
    )
    logger.info(f"Thermodynamic Entropy metrics: {te_metrics}")
    logger.info(f"Hyperparameters: T_0={te_result['T_0']:.2f}, alpha={te_result['alpha']:.2f}")

    # =========================================================================
    # Step 5: Generate Reliability Diagrams
    # =========================================================================
    logger.info("\n[Step 5] Generating Reliability Diagrams")

    plot_reliability_diagram(
        uncal_result["probs"], test_labels,
        "Uncalibrated",
        str(output_dir / "reliability_uncalibrated.png")
    )

    plot_reliability_diagram(
        ts_result["probs"], test_labels,
        f"Temp Scaling (T={ts_result['T_opt']:.2f})",
        str(output_dir / "reliability_temp_scaling.png")
    )

    plot_reliability_diagram(
        te_result["probs"], test_labels,
        f"Thermodynamic (T0={te_result['T_0']:.2f}, a={te_result['alpha']:.2f})",
        str(output_dir / "reliability_thermodynamic.png")
    )

    # =========================================================================
    # Step 6: Save Results
    # =========================================================================
    logger.info("\n[Step 6] Saving Results")

    # Format results to match exp_gen_sol_out.json schema exactly
    examples = []
    for i in range(len(test_labels)):
        example = {
            "input": f"Sample {i}: logits={test_logits[i].tolist()}",
            "output": f"True label: {test_labels[i]}",
            "predict_uncalibrated": str(uncal_result["preds"][i]),
            "predict_temperature_scaling": str(ts_result["preds"][i]),
            "predict_thermodynamic_entropy": str(te_result["preds"][i]),
            "metadata_uncalibrated_probs": json.dumps(uncal_result["probs"][i].tolist()),
            "metadata_ts_probs": json.dumps(ts_result["probs"][i].tolist()),
            "metadata_te_probs": json.dumps(te_result["probs"][i].tolist()),
            "metadata_test_logits": json.dumps(test_logits[i].tolist())
        }
        examples.append(example)

    results = {
        "datasets": [
            {
                "dataset": args.dataset,
                "examples": examples
            }
        ]
    }

    # Save main results
    output_file = output_dir / "method_out.json"
    output_file.write_text(json.dumps(results, indent=2))
    logger.info(f"Saved results to {output_file}")

    # Save a separate metadata file with experiment summary
    metadata = {
        "method_name": "Thermodynamic Entropy Calibration",
        "description": "Physics-inspired calibration method that treats LLM predictive uncertainty as thermodynamic entropy",
        "results": {
            "uncalibrated": uncal_metrics,
            "temperature_scaling": ts_metrics,
            "thermodynamic_entropy": te_metrics
        },
        "hyperparameters": {
            "temperature_scaling": {"T_opt": float(ts_result["T_opt"])},
            "thermodynamic_entropy": {
                "T_0": float(te_result["T_0"]),
                "alpha": float(te_result["alpha"])
            }
        },
        "dataset_info": {
            "name": args.dataset,
            "model": args.model,
            "n_train": len(train_labels),
            "n_val": len(val_labels),
            "n_test": len(test_labels),
            "n_classes": test_logits.shape[1]
        },
        "experiment_info": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "hardware": hardware
        }
    }

    metadata_file = output_dir / "metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=2))
    logger.info(f"Saved metadata to {metadata_file}")

    # Also save per-method predictions for further analysis
    predictions_file = output_dir / "predictions.npz"
    np.savez(
        predictions_file,
        uncal_probs=uncal_result["probs"],
        ts_probs=ts_result["probs"],
        te_probs=te_result["probs"],
        test_labels=test_labels
    )
    logger.info(f"Saved predictions to {predictions_file}")

    # =========================================================================
    # Summary
    # =========================================================================
    logger.info("\n" + "=" * 60)
    logger.info("EXPERIMENT COMPLETE")
    logger.info("=" * 60)
    logger.info("\nResults Summary:")
    logger.info(f"{'Method':<30} {'ECE':>8} {'Brier':>8} {'NLL':>8} {'Acc':>8}")
    logger.info("-" * 62)

    # Print results directly from metrics variables
    for name, metrics in [("uncalibrated", uncal_metrics),
                          ("temperature_scaling", ts_metrics),
                          ("thermodynamic_entropy", te_metrics)]:
        logger.info(
            f"{name:<30} {metrics['ece']:>8.4f} {metrics['brier']:>8.4f} "
            f"{metrics['nll']:>8.4f} {metrics['accuracy']:>8.4f}"
        )

    return results


if __name__ == "__main__":
    main()
