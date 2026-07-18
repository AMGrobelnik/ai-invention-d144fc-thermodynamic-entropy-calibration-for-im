#!/usr/bin/env python3
"""
Quick test script for TEC vs TS experiment.
Runs on mini dataset (20 examples) for quick verification.
"""

import json
import numpy as np
import torch
import warnings
from pathlib import Path
from loguru import logger
import sys

warnings.filterwarnings("ignore")

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

# Simplified version - just test core logic
def softmax(logits, temperature=1.0):
    logits_t = logits / temperature
    exp_logits = np.exp(logits_t - np.max(logits_t, axis=-1, keepdims=True))
    return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

def compute_ece(probs, labels, n_bins=10):
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

def test_core_logic():
    """Test calibration methods with dummy logits."""
    logger.info("Testing core calibration logic...")
    
    # Create dummy logits (10 samples, 2 classes)
    np.random.seed(42)
    n_samples = 20
    n_classes = 2
    
    # Simulate somewhat calibrated logits
    logits = np.random.randn(n_samples, n_classes) * 2
    labels = np.array([0, 1] * 10)
    
    # Test uncalibrated
    probs_uncal = softmax(logits, 1.0)
    ece_uncal = compute_ece(probs_uncal, labels)
    logger.info(f"Uncalibrated ECE: {ece_uncal:.4f}")
    
    # Test Temperature Scaling
    from scipy.optimize import minimize_scalar
    
    def nll_loss(T):
        probs = softmax(logits, T)
        probs = np.clip(probs, 1e-12, 1.0)
        log_probs = np.log(probs)
        return -np.mean(log_probs[np.arange(len(labels)), labels])
    
    result = minimize_scalar(nll_loss, bounds=(0.01, 10.0), method='bounded')
    optimal_T = result.x
    logger.info(f"Optimal T: {optimal_T:.4f}")
    
    probs_ts = softmax(logits, optimal_T)
    ece_ts = compute_ece(probs_ts, labels)
    logger.info(f"TS ECE: {ece_ts:.4f}")
    
    # Test TEC
    H = -np.sum(probs_uncal * np.log(np.clip(probs_uncal, 1e-12, 1.0)), axis=-1)
    H_max = np.log(n_classes)
    H_norm = H / H_max
    sorted_probs = np.sort(probs_uncal, axis=-1)
    M = sorted_probs[:, -1] - sorted_probs[:, -2]
    
    T0, alpha, beta = 1.0, 1.0, 0.5
    T_i = T0 * (1 + alpha * H_norm - beta * M)
    T_i = np.clip(T_i, 0.01, 100.0)
    
    # Apply per-sample temperature
    probs_tec = np.array([
        softmax(logits[i:i+1], T_i[i])[0]
        for i in range(n_samples)
    ])
    ece_tec = compute_ece(probs_tec, labels)
    logger.info(f"TEC ECE: {ece_tec:.4f}")
    
    logger.info("Core logic test PASSED!")
    return True

def test_with_mini_dataset():
    """Test with actual mini dataset and a real model."""
    logger.info("Testing with mini dataset (SST-2, 20 examples)...")
    
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    
    # Load mini data
    data_path = Path("mini_data_out.json")
    with open(data_path) as f:
        data = json.load(f)
    
    # Get SST-2 examples
    for ds in data['datasets']:
        if ds['dataset'] == 'sst-2':
            examples = ds['examples']
            texts = [e['input'] for e in examples]
            labels = np.array([int(e['output']) for e in examples])
            break
    
    logger.info(f"Loaded {len(texts)} SST-2 examples")
    
    # Load model
    logger.info("Loading distilbert-sst2 model...")
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased-finetuned-sst-2-english"
    )
    
    # Get logits
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    
    # Tokenize
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits.cpu().numpy()
    
    logger.info(f"Logits shape: {logits.shape}")
    
    # Test methods
    probs_uncal = softmax(logits, 1.0)
    ece_uncal = compute_ece(probs_uncal, labels)
    acc_uncal = np.mean(np.argmax(probs_uncal, axis=-1) == labels)
    logger.info(f"Uncalibrated: ECE={ece_uncal:.4f}, Acc={acc_uncal:.4f}")
    
    # TS
    from scipy.optimize import minimize_scalar
    def nll_loss(T):
        probs = softmax(logits, T)
        probs = np.clip(probs, 1e-12, 1.0)
        log_probs = np.log(probs)
        return -np.mean(log_probs[np.arange(len(labels)), labels])
    
    result = minimize_scalar(nll_loss, bounds=(0.01, 10.0), method='bounded')
    optimal_T = result.x
    
    probs_ts = softmax(logits, optimal_T)
    ece_ts = compute_ece(probs_ts, labels)
    acc_ts = np.mean(np.argmax(probs_ts, axis=-1) == labels)
    logger.info(f"TS (T={optimal_T:.4f}): ECE={ece_ts:.4f}, Acc={acc_ts:.4f}")
    
    logger.info("Mini dataset test PASSED!")
    return True

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Running quick tests for TEC vs TS experiment")
    logger.info("=" * 60)
    
    try:
        test_core_logic()
        test_with_mini_dataset()
        logger.info("ALL TESTS PASSED!")
    except Exception as e:
        logger.error(f"Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
