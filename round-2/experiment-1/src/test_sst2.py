#!/usr/bin/env python3
"""Test script - runs only on SST-2 with 100 examples to verify code works."""
import json
import gc
import sys
import warnings
from pathlib import Path
from loguru import logger
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.optimize import minimize_scalar

warnings.filterwarnings("ignore")
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Softmax
def softmax(logits, temperature=1.0):
    logits_t = logits / temperature
    logits_t = logits_t - np.max(logits_t, axis=-1, keepdims=True)
    exp_logits = np.exp(logits_t)
    return exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

# ECE
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

# Dataset class
class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx], truncation=True, padding="max_length",
            max_length=self.max_length, return_tensors="pt"
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "label": torch.tensor(self.labels[idx], dtype=torch.long)
        }

logger.info("Loading SST-2 data...")
with open("mini_data_out.json") as f:
    data = json.load(f)

for ds in data['datasets']:
    if ds['dataset'] == 'sst-2':
        examples = ds['examples']
        texts = [e['input'] for e in examples]
        labels = [int(e['output']) for e in examples]
        break

# Use 20 examples from mini dataset
logger.info(f"Using {len(texts)} SST-2 examples")

# Load model
logger.info("Loading SST-2 model (cached)...")
tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english",
    local_files_only=True
)
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english",
    local_files_only=True
)
model.to(DEVICE)
model.eval()

# Tokenize
logger.info("Tokenizing...")
dataset = TextDataset(texts, labels, tokenizer)
loader = DataLoader(dataset, batch_size=8, shuffle=False)

# Extract logits
logger.info("Extracting logits...")
all_logits = []
all_labels = []
with torch.no_grad():
    for batch in loader:
        input_ids = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        lbls = batch["label"]
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        all_logits.append(outputs.logits.cpu().numpy())
        all_labels.append(lbls.numpy())

logits = np.vstack(all_logits)
labels_np = np.concatenate(all_labels)
logger.info(f"Logits shape: {logits.shape}")

# Test Uncalibrated
probs_uncal = softmax(logits, 1.0)
ece_uncal = compute_ece(probs_uncal, labels_np)
acc_uncal = np.mean(np.argmax(probs_uncal, axis=-1) == labels_np)
logger.info(f"Uncalibrated: ECE={ece_uncal:.4f}, Acc={acc_uncal:.4f}")

# Test TS
logger.info("Tuning Temperature Scaling...")
def nll_loss(T):
    p = softmax(logits, T)
    p = np.clip(p, 1e-12, 1.0)
    return -np.mean(np.log(p[np.arange(len(labels_np)), labels_np]))

result = minimize_scalar(nll_loss, bounds=(0.01, 10.0), method='bounded')
optimal_T = result.x
probs_ts = softmax(logits, optimal_T)
ece_ts = compute_ece(probs_ts, labels_np)
acc_ts = np.mean(np.argmax(probs_ts, axis=-1) == labels_np)
logger.info(f"TS (T={optimal_T:.4f}): ECE={ece_ts:.4f}, Acc={acc_ts:.4f}")

# Test TEC
logger.info("Running TEC...")
probs_init = softmax(logits, 1.0)
H = -np.sum(probs_init * np.log(np.clip(probs_init, 1e-12, 1.0)), axis=-1)
sorted_p = np.sort(probs_init, axis=-1)
M = sorted_p[:, -1] - sorted_p[:, -2]
H_max = np.log(2)
H_norm = H / H_max

# Simple TEC: T_i = 1.0 * (1 + 1.0 * H_norm - 0.5 * M)
T_i = 1.0 * (1 + 1.0 * H_norm - 0.5 * M)
T_i = np.clip(T_i, 0.01, 100.0)

probs_tec = np.array([softmax(logits[i:i+1], T_i[i])[0] for i in range(len(logits))])
ece_tec = compute_ece(probs_tec, labels_np)
acc_tec = np.mean(np.argmax(probs_tec, axis=-1) == labels_np)
logger.info(f"TEC: ECE={ece_tec:.4f}, Acc={acc_tec:.4f}")

logger.info("\n" + "="*60)
logger.info("TEST RESULTS SUMMARY (SST-2, 20 examples)")
logger.info("="*60)
logger.info(f"Uncalibrated: ECE={ece_uncal:.4f}, Acc={acc_uncal:.4f}")
logger.info(f"TS:            ECE={ece_ts:.4f}, Acc={acc_ts:.4f}")
logger.info(f"TEC:           ECE={ece_tec:.4f}, Acc={acc_tec:.4f}")
logger.info("\nTest completed successfully!")
