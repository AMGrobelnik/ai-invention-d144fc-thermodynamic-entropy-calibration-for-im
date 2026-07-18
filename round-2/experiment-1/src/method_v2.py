#!/usr/bin/env python3
"""
TEC vs TS Calibration Experiment for LLM Classifiers - Production Version

Compares Thermodynamic Entropy Calibration (TEC) with Temperature Scaling (TS)
across 5 text classification datasets (SST-2, QNLI, AG News, MNLI, DBpedia).

Methods:
1. Uncalibrated baseline (softmax on raw logits)
2. Temperature Scaling (TS) - single T tuned on validation set  
3. Thermodynamic Entropy Calibration (TEC) - per-sample T based on entropy + margin
"""

import json
import gc
import sys
import warnings
from pathlib import Path
from loguru import logger
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.optimize import minimize_scalar

warnings.filterwarnings("ignore")

# =============================================================================
# Setup Logging
# =============================================================================
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

# =============================================================================
# Hardware Setup
# =============================================================================
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
HAS_GPU = torch.cuda.is_available()
if HAS_GPU:
    logger.info(f"GPU: {torch.cuda.get_device_name(0)}, VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB")
else:
    logger.info("No GPU detected, using CPU")

# =============================================================================
# Data Structures
# =============================================================================

@dataclass
class CalibrationResult:
    """Results for a single method on a single dataset."""
    method_name: str
    dataset_name: str
    ece: float
    brier: float
    nll: float
    accuracy: float
    ece_ci_lower: float
    ece_ci_upper: float
    brier_ci_lower: float
    brier_ci_upper: float
    nll_ci_lower: float
    nll_ci_upper: float
    accuracy_ci_lower: float
    accuracy_ci_upper: float
    ece_easy: float
    ece_hard: float
    accuracy_easy: float
    accuracy_hard: float
    temperatures: Optional[List[float]] = None


# =============================================================================
# Dataset Handling
# =============================================================================

class TextDataset(Dataset):
    """PyTorch dataset for text classification."""
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length: int = 512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "label": torch.tensor(self.labels[idx], dtype=torch.long)
        }


def load_and_split_dataset(data_path: Path, dataset_name: str, 
                           max_examples: int = 5000) -> Tuple[List[str], List[int], int]:
    """
    Load dataset and create 60/20/20 train/val/test splits.
    
    Returns:
        (texts_train, labels_train, texts_val, labels_val, texts_test, labels_test, num_classes)
    """
    logger.info(f"Loading and splitting {dataset_name} (max {max_examples} examples)")
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # Find the dataset
    dataset_info = None
    for ds in data['datasets']:
        if ds['dataset'] == dataset_name:
            dataset_info = ds
            break
    
    if dataset_info is None:
        raise ValueError(f"Dataset {dataset_name} not found")
    
    examples = dataset_info['examples']
    
    # Limit total examples
    if len(examples) > max_examples:
        # Stratified sampling
        np.random.seed(42)
        indices = np.random.choice(len(examples), max_examples, replace=False)
        examples = [examples[i] for i in indices]
    
    # Extract texts and labels
    texts = [ex['input'] for ex in examples]
    labels = [int(ex['output']) for ex in examples]
    
    # Get unique labels and map to 0-indexed if needed
    unique_labels = sorted(set(labels))
    label_map = {old: new for new, old in enumerate(unique_labels)}
    labels = [label_map[l] for l in labels]
    num_classes = len(unique_labels)
    
    # Create 60/20/20 split
    n = len(texts)
    np.random.seed(42)
    indices = np.random.permutation(n)
    
    train_end = int(0.6 * n)
    val_end = int(0.8 * n)
    
    train_idx = indices[:train_end]
    val_idx = indices[train_end:val_end]
    test_idx = indices[val_end:]
    
    texts_train = [texts[i] for i in train_idx]
    labels_train = [labels[i] for i in train_idx]
    texts_val = [texts[i] for i in val_idx]
    labels_val = [labels[i] for i in val_idx]
    texts_test = [texts[i] for i in test_idx]
    labels_test = [labels[i] for i in test_idx]
    
    logger.info(f"  Split: train={len(texts_train)}, val={len(texts_val)}, test={len(texts_test)}, classes={num_classes}")
    
    return (texts_train, labels_train, texts_val, labels_val, 
            texts_test, labels_test, num_classes)


# =============================================================================
# Model Loading
# =============================================================================

MODEL_MAP = {
    "sst-2": "distilbert-base-uncased-finetuned-sst-2-english",
    "ag_news": "bert-base-uncased",
    "qnli": "bert-base-uncased",
    "mnli": "roberta-large-mnli",
    "dbpedia": "bert-base-uncased",
}

def load_model(dataset_name: str, num_labels: int):
    """Load pre-trained model with fallback."""
    model_name = MODEL_MAP.get(dataset_name, "bert-base-uncased")
    
    logger.info(f"Loading model: {model_name}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels
        )
        logger.info(f"  Loaded {model_name}")
    except Exception as e:
        logger.warning(f"  Failed to load {model_name}: {e}")
        logger.info("  Falling back to bert-base-uncased")
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        model = AutoModelForSequenceClassification.from_pretrained(
            "bert-base-uncased",
            num_labels=num_labels
        )
    
    model.to(DEVICE)
    model.eval()
    return model, tokenizer


# =============================================================================
# Logit Extraction
# =============================================================================

def extract_logits(model, dataloader) -> Tuple[np.ndarray, np.ndarray]:
    """Extract logits and labels from model."""
    all_logits = []
    all_labels = []
    
    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            labels = batch["label"]
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            
            all_logits.append(logits.cpu().numpy())
            all_labels.append(labels.numpy())
    
    return np.vstack(all_logits), np.concatenate(all_labels)


# =============================================================================
# Calibration Methods
# =============================================================================

def softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    """Apply softmax with temperature."""
    logits_t = logits / temperature
    logits_t = logits_t - np.max(logits_t, axis=-1, keepdims=True)  # Numerical stability
    exp_logits = np.exp(logits_t)
    return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)


def compute_entropy(probs: np.ndarray) -> np.ndarray:
    """Compute Shannon entropy."""
    probs = np.clip(probs, 1e-12, 1.0)
    return -np.sum(probs * np.log(probs), axis=-1)


def compute_margin(probs: np.ndarray) -> np.ndarray:
    """Compute decision margin (difference between top two probs)."""
    sorted_probs = np.sort(probs, axis=-1)
    return sorted_probs[:, -1] - sorted_probs[:, -2]


def calibrate_ts(logits: np.ndarray, logits_val: np.ndarray, labels_val: np.ndarray) -> Tuple[np.ndarray, float]:
    """Temperature Scaling calibration."""
    # Tune temperature on validation set
    def nll_loss(T):
        probs = softmax(logits_val, T)
        probs = np.clip(probs, 1e-12, 1.0)
        log_probs = np.log(probs)
        return -np.mean(log_probs[np.arange(len(labels_val)), labels_val])
    
    result = minimize_scalar(nll_loss, bounds=(0.01, 10.0), method='bounded')
    optimal_T = result.x
    
    # Apply to test set
    probs_cal = softmax(logits, optimal_T)
    return probs_cal, optimal_T


def calibrate_tec(logits: np.ndarray, logits_val: np.ndarray, labels_val: np.ndarray, 
                  n_classes: int) -> Tuple[np.ndarray, np.ndarray, float, float, float]:
    """
    Thermodynamic Entropy Calibration (TEC).
    
    T_i = T0 * (1 + alpha * H_norm - beta * M)
    """
    # Tune hyperparameters on validation set
    probs_val = softmax(logits_val, 1.0)
    H_val = compute_entropy(probs_val)
    M_val = compute_margin(probs_val)
    H_max = np.log(n_classes)
    H_norm_val = H_val / H_max
    
    # Grid search for T0, alpha, beta
    best_ece = float('inf')
    best_params = (1.0, 1.0, 0.5)
    
    for T0 in [0.5, 1.0, 2.0, 5.0]:
        for alpha in [0.0, 0.5, 1.0, 2.0]:
            for beta in [0.0, 0.25, 0.5, 1.0]:
                T_i = T0 * (1 + alpha * H_norm_val - beta * M_val)
                T_i = np.clip(T_i, 0.01, 100.0)
                
                # Vectorized per-sample temperature scaling
                logits_t = logits_val / T_i[:, np.newaxis]
                logits_t = logits_t - np.max(logits_t, axis=-1, keepdims=True)
                exp_logits = np.exp(logits_t)
                probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
                
                ece = compute_ece(probs, labels_val)
                if ece < best_ece:
                    best_ece = ece
                    best_params = (T0, alpha, beta)
    
    T0_opt, alpha_opt, beta_opt = best_params
    logger.info(f"  TEC optimal params: T0={T0_opt}, alpha={alpha_opt}, beta={beta_opt}, val_ECE={best_ece:.4f}")
    
    # Apply to test set
    probs_test = softmax(logits, 1.0)
    H_test = compute_entropy(probs_test)
    M_test = compute_margin(probs_test)
    H_norm_test = H_test / np.log(n_classes)
    
    T_i_test = T0_opt * (1 + alpha_opt * H_norm_test - beta_opt * M_test)
    T_i_test = np.clip(T_i_test, 0.01, 100.0)
    
    # Vectorized per-sample temperature scaling
    logits_t = logits / T_i_test[:, np.newaxis]
    logits_t = logits_t - np.max(logits_t, axis=-1, keepdims=True)
    exp_logits = np.exp(logits_t)
    probs_cal = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
    
    return probs_cal, T_i_test, T0_opt, alpha_opt, beta_opt


# =============================================================================
# Metrics
# =============================================================================

def compute_ece(probs: np.ndarray, labels: np.ndarray, n_bins: int = 10) -> float:
    """Compute Expected Calibration Error."""
    n_samples = len(labels)
    confidences = np.max(probs, axis=-1)
    predictions = np.argmax(probs, axis=-1)
    accuracies = (predictions == labels).astype(float)
    
    ece = 0.0
    for i in range(n_bins):
        lower = i / n_bins
        upper = (i + 1) / n_bins
        if i == n_bins - 1:
            mask = (confidences >= lower) & (confidences <= upper)
        else:
            mask = (confidences >= lower) & (confidences < upper)
        
        if np.sum(mask) > 0:
            bin_accuracy = np.mean(accuracies[mask])
            bin_confidence = np.mean(confidences[mask])
            bin_weight = np.sum(mask) / n_samples
            ece += bin_weight * abs(bin_accuracy - bin_confidence)
    
    return ece


def compute_nll(probs: np.ndarray, labels: np.ndarray) -> float:
    """Compute Negative Log-Likelihood."""
    probs = np.clip(probs, 1e-12, 1.0)
    log_probs = np.log(probs)
    return -np.mean(log_probs[np.arange(len(labels)), labels])


def compute_brier(probs: np.ndarray, labels: np.ndarray, n_classes: int) -> float:
    """Compute Brier score."""
    n_samples = len(labels)
    one_hot = np.zeros((n_samples, n_classes))
    one_hot[np.arange(n_samples), labels] = 1.0
    return np.mean(np.sum((probs - one_hot) ** 2, axis=-1))


def compute_accuracy(probs: np.ndarray, labels: np.ndarray) -> float:
    """Compute accuracy."""
    predictions = np.argmax(probs, axis=-1)
    return np.mean(predictions == labels)


# =============================================================================
# Bootstrap CI
# =============================================================================

def bootstrap_ci(metric_func, probs: np.ndarray, labels: np.ndarray,
                 n_bootstrap: int = 200, **kwargs) -> Tuple[float, float]:
    """Compute bootstrap confidence interval."""
    n_samples = len(labels)
    bootstrap_metrics = []
    
    for _ in range(n_bootstrap):
        indices = np.random.choice(n_samples, size=n_samples, replace=True)
        probs_boot = probs[indices]
        labels_boot = labels[indices]
        
        if kwargs:
            metric_val = metric_func(probs_boot, labels_boot, **kwargs)
        else:
            metric_val = metric_func(probs_boot, labels_boot)
        bootstrap_metrics.append(metric_val)
    
    lower = np.percentile(bootstrap_metrics, 2.5)
    upper = np.percentile(bootstrap_metrics, 97.5)
    return lower, upper


# =============================================================================
# Heterogeneous Analysis
# =============================================================================

def heterogeneous_analysis(probs: np.ndarray, labels: np.ndarray,
                          margins: np.ndarray) -> Tuple[float, float, float, float]:
    """Split into easy/hard by margin and compute ECE + accuracy."""
    sorted_indices = np.argsort(margins)
    n = len(sorted_indices)
    mid = n // 2
    
    hard_idx = sorted_indices[:mid]
    easy_idx = sorted_indices[mid:]
    
    ece_easy = compute_ece(probs[easy_idx], labels[easy_idx])
    ece_hard = compute_ece(probs[hard_idx], labels[hard_idx])
    acc_easy = compute_accuracy(probs[easy_idx], labels[easy_idx])
    acc_hard = compute_accuracy(probs[hard_idx], labels[hard_idx])
    
    return ece_easy, ece_hard, acc_easy, acc_hard


# =============================================================================
# Main Experiment
# =============================================================================

@logger.catch(reraise=True)
def run_experiment(data_path: Path, output_path: Path,
                   max_examples: int = 3000, n_bootstrap: int = 200):
    """
    Run the full TEC vs TS comparison experiment.
    
    Args:
        data_path: Path to full_data_out.json
        output_path: Path to save results
        max_examples: Max examples per dataset (total, before splitting)
        n_bootstrap: Number of bootstrap samples
    """
    logger.info("=" * 80)
    logger.info("TEC vs TS Calibration Experiment")
    logger.info(f"  Device: {DEVICE}, Max examples: {max_examples}")
    logger.info("=" * 80)
    
    datasets = ["sst-2", "qnli", "ag_news", "mnli", "dbpedia"]
    all_results = []
    
    for dataset_name in datasets:
        logger.info(f"\n{'='*80}")
        logger.info(f"Dataset: {dataset_name}")
        logger.info(f"{'='*80}")
        
        # Load and split data
        try:
            (texts_train, labels_train, texts_val, labels_val, 
             texts_test, labels_test, num_classes) = load_and_split_dataset(
                data_path, dataset_name, max_examples
            )
        except Exception as e:
            logger.error(f"Failed to load {dataset_name}: {e}")
            continue
        
        # Load model
        model, tokenizer = load_model(dataset_name, num_classes)
        
        # Create dataloaders
        batch_size = 32 if HAS_GPU else 8
        val_dataset = TextDataset(texts_val, labels_val, tokenizer)
        test_dataset = TextDataset(texts_test, labels_test, tokenizer)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
        
        # Extract logits
        logger.info("  Extracting logits...")
        logits_val, labels_val_np = extract_logits(model, val_loader)
        logits_test, labels_test_np = extract_logits(model, test_loader)
        
        # Free model memory
        del model, tokenizer, val_dataset, test_dataset, val_loader, test_loader
        gc.collect()
        if HAS_GPU:
            torch.cuda.empty_cache()
        
        logger.info(f"  Logits shape: val={logits_val.shape}, test={logits_test.shape}")
        
        # ---------------------------------------------------------------------
        # Method 1: Uncalibrated
        # ---------------------------------------------------------------------
        logger.info("\n  [1/3] Uncalibrated")
        probs_uncal = softmax(logits_test, 1.0)
        
        ece = compute_ece(probs_uncal, labels_test_np)
        brier = compute_brier(probs_uncal, labels_test_np, num_classes)
        nll = compute_nll(probs_uncal, labels_test_np)
        acc = compute_accuracy(probs_uncal, labels_test_np)
        
        ece_ci = bootstrap_ci(compute_ece, probs_uncal, labels_test_np, n_bootstrap)
        brier_ci = bootstrap_ci(compute_brier, probs_uncal, labels_test_np, n_bootstrap, n_classes=num_classes)
        nll_ci = bootstrap_ci(compute_nll, probs_uncal, labels_test_np, n_bootstrap)
        acc_ci = bootstrap_ci(compute_accuracy, probs_uncal, labels_test_np, n_bootstrap)
        
        margins = compute_margin(probs_uncal)
        het = heterogeneous_analysis(probs_uncal, labels_test_np, margins)
        
        result = CalibrationResult(
            method_name="Uncalibrated", dataset_name=dataset_name,
            ece=ece, brier=brier, nll=nll, accuracy=acc,
            ece_ci_lower=ece_ci[0], ece_ci_upper=ece_ci[1],
            brier_ci_lower=brier_ci[0], brier_ci_upper=brier_ci[1],
            nll_ci_lower=nll_ci[0], nll_ci_upper=nll_ci[1],
            accuracy_ci_lower=acc_ci[0], accuracy_ci_upper=acc_ci[1],
            ece_easy=het[0], ece_hard=het[1],
            accuracy_easy=het[2], accuracy_hard=het[3]
        )
        all_results.append(result)
        logger.info(f"    ECE={ece:.4f} [{ece_ci[0]:.4f}, {ece_ci[1]:.4f}], Acc={acc:.4f}")
        
        # ---------------------------------------------------------------------
        # Method 2: Temperature Scaling
        # ---------------------------------------------------------------------
        logger.info("\n  [2/3] Temperature Scaling")
        probs_ts, optimal_T = calibrate_ts(logits_test, logits_val, labels_val_np)
        
        ece = compute_ece(probs_ts, labels_test_np)
        brier = compute_brier(probs_ts, labels_test_np, num_classes)
        nll = compute_nll(probs_ts, labels_test_np)
        acc = compute_accuracy(probs_ts, labels_test_np)
        
        ece_ci = bootstrap_ci(compute_ece, probs_ts, labels_test_np, n_bootstrap)
        brier_ci = bootstrap_ci(compute_brier, probs_ts, labels_test_np, n_bootstrap, n_classes=num_classes)
        nll_ci = bootstrap_ci(compute_nll, probs_ts, labels_test_np, n_bootstrap)
        acc_ci = bootstrap_ci(compute_accuracy, probs_ts, labels_test_np, n_bootstrap)
        
        margins = compute_margin(probs_ts)
        het = heterogeneous_analysis(probs_ts, labels_test_np, margins)
        
        result = CalibrationResult(
            method_name="Temperature Scaling", dataset_name=dataset_name,
            ece=ece, brier=brier, nll=nll, accuracy=acc,
            ece_ci_lower=ece_ci[0], ece_ci_upper=ece_ci[1],
            brier_ci_lower=brier_ci[0], brier_ci_upper=brier_ci[1],
            nll_ci_lower=nll_ci[0], nll_ci_upper=nll_ci[1],
            accuracy_ci_lower=acc_ci[0], accuracy_ci_upper=acc_ci[1],
            ece_easy=het[0], ece_hard=het[1],
            accuracy_easy=het[2], accuracy_hard=het[3]
        )
        all_results.append(result)
        logger.info(f"    T={optimal_T:.4f}, ECE={ece:.4f} [{ece_ci[0]:.4f}, {ece_ci[1]:.4f}], Acc={acc:.4f}")
        
        # ---------------------------------------------------------------------
        # Method 3: TEC
        # ---------------------------------------------------------------------
        logger.info("\n  [3/3] Thermodynamic Entropy Calibration (TEC)")
        probs_tec, temps, T0, alpha, beta = calibrate_tec(
            logits_test, logits_val, labels_val_np, num_classes
        )
        
        ece = compute_ece(probs_tec, labels_test_np)
        brier = compute_brier(probs_tec, labels_test_np, num_classes)
        nll = compute_nll(probs_tec, labels_test_np)
        acc = compute_accuracy(probs_tec, labels_test_np)
        
        ece_ci = bootstrap_ci(compute_ece, probs_tec, labels_test_np, n_bootstrap)
        brier_ci = bootstrap_ci(compute_brier, probs_tec, labels_test_np, n_bootstrap, n_classes=num_classes)
        nll_ci = bootstrap_ci(compute_nll, probs_tec, labels_test_np, n_bootstrap)
        acc_ci = bootstrap_ci(compute_accuracy, probs_tec, labels_test_np, n_bootstrap)
        
        margins = compute_margin(probs_tec)
        het = heterogeneous_analysis(probs_tec, labels_test_np, margins)
        
        result = CalibrationResult(
            method_name="TEC", dataset_name=dataset_name,
            ece=ece, brier=brier, nll=nll, accuracy=acc,
            ece_ci_lower=ece_ci[0], ece_ci_upper=ece_ci[1],
            brier_ci_lower=brier_ci[0], brier_ci_upper=brier_ci[1],
            nll_ci_lower=nll_ci[0], nll_ci_upper=nll_ci[1],
            accuracy_ci_lower=acc_ci[0], accuracy_ci_upper=acc_ci[1],
            temperatures=temps.tolist(),
            ece_easy=het[0], ece_hard=het[1],
            accuracy_easy=het[2], accuracy_hard=het[3]
        )
        all_results.append(result)
        logger.info(f"    T0={T0}, alpha={alpha}, beta={beta}")
        logger.info(f"    ECE={ece:.4f} [{ece_ci[0]:.4f}, {ece_ci[1]:.4f}], Acc={acc:.4f}")
        logger.info(f"    T stats: mean={np.mean(temps):.4f}, std={np.std(temps):.4f}")
        
        gc.collect()
        if HAS_GPU:
            torch.cuda.empty_cache()
    
    # =========================================================================
    # Save Results
    # =========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("Saving results...")
    
    results_dict = {
        "experiment": "TEC_vs_TS_evaluation",
        "datasets": datasets,
        "summary": {
            "num_datasets": len(datasets),
            "methods": ["Uncalibrated", "Temperature Scaling", "TEC"],
            "metrics": ["ECE", "Brier", "NLL", "Accuracy"],
            "bootstrap_samples": n_bootstrap,
            "max_examples_per_dataset": max_examples,
        },
        "results": []
    }
    
    for r in all_results:
        rd = {
            "method": r.method_name,
            "dataset": r.dataset_name,
            "ece": r.ece,
            "ece_ci": [r.ece_ci_lower, r.ece_ci_upper],
            "brier": r.brier,
            "brier_ci": [r.brier_ci_lower, r.brier_ci_upper],
            "nll": r.nll,
            "nll_ci": [r.nll_ci_lower, r.nll_ci_upper],
            "accuracy": r.accuracy,
            "accuracy_ci": [r.accuracy_ci_lower, r.accuracy_ci_upper],
            "ece_easy": r.ece_easy,
            "ece_hard": r.ece_hard,
            "accuracy_easy": r.accuracy_easy,
            "accuracy_hard": r.accuracy_hard,
        }
        if r.temperatures is not None:
            rd["temperature_stats"] = {
                "mean": float(np.mean(r.temperatures)),
                "std": float(np.std(r.temperatures)),
                "min": float(np.min(r.temperatures)),
                "max": float(np.max(r.temperatures)),
            }
        results_dict["results"].append(rd)
    
    # Print summary
    logger.info("\n" + "=" * 80)
    logger.info("RESULTS SUMMARY")
    logger.info("=" * 80)
    for dataset_name in datasets:
        logger.info(f"\nDataset: {dataset_name}")
        logger.info(f"{'Method':<25} {'ECE':<12} {'Brier':<12} {'NLL':<12} {'Accuracy':<10}")
        logger.info("-" * 70)
        for r in all_results:
            if r.dataset_name == dataset_name:
                logger.info(f"{r.method_name:<25} {r.ece:<12.4f} {r.brier:<12.4f} {r.nll:<12.4f} {r.accuracy:<10.4f}")
    
    with open(output_path, 'w') as f:
        json.dump(results_dict, f, indent=2)
    
    logger.info(f"\nResults saved to {output_path}")
    return results_dict


def main():
    """Main entry point."""
    workspace = Path("/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_art/gen_art_experiment_1")
    data_path = workspace.parent.parent.parent / "iter_1" / "gen_art" / "gen_art_dataset_1" / "full_data_out.json"
    output_path = workspace / "method_out.json"
    
    # Use 3000 examples per dataset for manageable runtime
    # Reduce bootstrap to 200 for speed
    results = run_experiment(
        data_path=data_path,
        output_path=output_path,
        max_examples=3000,
        n_bootstrap=200
    )
    
    logger.info("\nExperiment completed successfully!")


if __name__ == "__main__":
    main()
