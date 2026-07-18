#!/usr/bin/env python3
"""Download and standardize text classification datasets for LLM calibration evaluation."""

from datasets import load_dataset
import json
from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split

# Create output directory
output_dir = Path("temp/datasets")
output_dir.mkdir(parents=True, exist_ok=True)

def standardize_sst2():
    """Download and standardize SST-2 dataset."""
    print("\nProcessing SST-2...")
    dataset = load_dataset("stanfordnlp/sst2")
    
    result = {}
    for split in ["train", "validation", "test"]:
        if split in dataset:
            rows = []
            for row in dataset[split]:
                rows.append({
                    "text": row["sentence"],
                    "label": int(row["label"]),
                    "label_text": "negative" if row["label"] == 0 else "positive",
                    "metadata": {
                        "dataset_name": "sst2",
                        "split": split,
                        "original_label": row["label"]
                    }
                })
            result[split] = rows
    
    return result, 2  # 2 classes

def standardize_ag_news():
    """Download and standardize AG News dataset."""
    print("\nProcessing AG News...")
    dataset = load_dataset("fancyzhx/ag_news")
    
    # AG News labels are already 0-indexed: 0=World, 1=Sports, 2=Business, 3=Sci/Tech
    label_map = {0: "World", 1: "Sports", 2: "Business", 3: "Sci/Tech"}
    
    result = {}
    for split in ["train", "test"]:
        if split in dataset:
            rows = []
            for row in dataset[split]:
                rows.append({
                    "text": row["text"],
                    "label": int(row["label"]),
                    "label_text": label_map[row["label"]],
                    "metadata": {
                        "dataset_name": "ag_news",
                        "split": split,
                        "original_label": row["label"]
                    }
                })
            result[split] = rows
    
    # Create validation split from train
    if "train" in result:
        train_rows = result["train"]
        train_labels = [r["label"] for r in train_rows]
        
        # Stratified split
        train_idx, val_idx = train_test_split(
            range(len(train_rows)), 
            test_size=0.1, 
            random_state=42, 
            stratify=train_labels
        )
        
        result["train"] = [train_rows[i] for i in train_idx]
        result["validation"] = [train_rows[i] for i in val_idx]
    
    return result, 4  # 4 classes

def standardize_mnli():
    """Download and standardize MNLI dataset."""
    print("\nProcessing MNLI...")
    dataset = load_dataset("nyu-mll/glue", "mnli")
    
    # MNLI labels: 0=entailment, 1=neutral, 2=contradiction
    label_map = {0: "entailment", 1: "neutral", 2: "contradiction"}
    
    result = {}
    for split in ["train", "validation_matched", "validation_mismatched"]:
        if split in dataset:
            rows = []
            for row in dataset[split]:
                # Combine premise and hypothesis
                text = f"Premise: {row['premise']} Hypothesis: {row['hypothesis']}"
                rows.append({
                    "text": text,
                    "label": int(row["label"]),
                    "label_text": label_map[row["label"]],
                    "metadata": {
                        "dataset_name": "mnli",
                        "split": split,
                        "original_label": row["label"]
                    }
                })
            result[split] = rows
    
    # Rename validation splits
    if "validation_matched" in result:
        result["validation"] = result.pop("validation_matched")
    if "validation_mismatched" in result:
        result["test"] = result.pop("validation_mismatched")
    
    return result, 3  # 3 classes

def standardize_qnli():
    """Download and standardize QNLI dataset."""
    print("\nProcessing QNLI...")
    dataset = load_dataset("nyu-mll/glue", "qnli")
    
    # QNLI labels: 0=not_entailment, 1=entailment
    # Note: test set has label=-1 (hidden)
    label_map = {0: "not_entailment", 1: "entailment"}
    
    result = {}
    for split in ["train", "validation"]:
        if split in dataset:
            rows = []
            for row in dataset[split]:
                # Combine question and sentence
                text = f"Question: {row['question']} Sentence: {row['sentence']}"
                rows.append({
                    "text": text,
                    "label": int(row["label"]),
                    "label_text": label_map[row["label"]],
                    "metadata": {
                        "dataset_name": "qnli",
                        "split": split,
                        "original_label": row["label"]
                    }
                })
            result[split] = rows
    
    # Create test split from validation (since test labels are hidden)
    if "validation" in result and len(result["validation"]) > 2000:
        val_rows = result["validation"]
        val_labels = [r["label"] for r in val_rows]
        
        # Split validation into validation and test
        val_idx, test_idx = train_test_split(
            range(len(val_rows)), 
            test_size=0.5, 
            random_state=42, 
            stratify=val_labels
        )
        
        result["validation"] = [val_rows[i] for i in val_idx]
        result["test"] = [val_rows[i] for i in test_idx]
    else:
        # If no validation split, create from train
        if "train" in result:
            train_rows = result["train"]
            train_labels = [r["label"] for r in train_rows]
            
            # Split train into train/val/test
            train_idx, temp_idx = train_test_split(
                range(len(train_rows)), 
                test_size=0.2, 
                random_state=42, 
                stratify=train_labels
            )
            
            temp_rows = [train_rows[i] for i in temp_idx]
            temp_labels = [r["label"] for r in temp_rows]
            
            val_idx, test_idx = train_test_split(
                range(len(temp_rows)), 
                test_size=0.5, 
                random_state=42, 
                stratify=temp_labels
            )
            
            result["train"] = [train_rows[i] for i in train_idx]
            result["validation"] = [temp_rows[i] for i in val_idx]
            result["test"] = [temp_rows[i] for i in test_idx]
    
    return result, 2  # 2 classes

def standardize_dbpedia():
    """Download and standardize DBpedia dataset."""
    print("\nProcessing DBpedia...")
    dataset = load_dataset("fancyzhx/dbpedia_14")
    
    # DBpedia has 14 classes (0-13)
    result = {}
    for split in ["train", "test"]:
        if split in dataset:
            rows = []
            for row in dataset[split]:
                # Combine title and content
                text = f"Title: {row['title']} Content: {row['content']}"
                rows.append({
                    "text": text,
                    "label": int(row["label"]),
                    "label_text": f"class_{row['label']}",  # DBpedia doesn't have label names in this version
                    "metadata": {
                        "dataset_name": "dbpedia",
                        "split": split,
                        "original_label": row["label"]
                    }
                })
            result[split] = rows
    
    # Create validation split from train
    if "train" in result:
        train_rows = result["train"]
        train_labels = [r["label"] for r in train_rows]
        
        # Stratified split (use 5% for validation due to large dataset)
        train_idx, val_idx = train_test_split(
            range(len(train_rows)), 
            test_size=0.05, 
            random_state=42, 
            stratify=train_labels
        )
        
        result["train"] = [train_rows[i] for i in train_idx]
        result["validation"] = [train_rows[i] for i in val_idx]
    
    return result, 14  # 14 classes

# Process all datasets
datasets_to_process = [
    ("SST-2", standardize_sst2),
    ("AG News", standardize_ag_news),
    ("MNLI", standardize_mnli),
    ("QNLI", standardize_qnli),
    ("DBpedia", standardize_dbpedia),
]

summary = {}

for name, func in datasets_to_process:
    try:
        print(f"\n{'='*60}")
        print(f"Processing {name}...")
        print(f"{'='*60}")
        
        data, num_classes = func()
        
        # Save each split
        for split, rows in data.items():
            output_file = output_dir / f"{name.lower().replace(' ', '_')}_{split}.json"
            with open(output_file, "w") as f:
                json.dump(rows, f, indent=2)
            print(f"  Saved {len(rows)} examples to {output_file}")
        
        # Add to summary
        summary[name] = {
            "num_classes": num_classes,
            "splits": {split: len(rows) for split, rows in data.items()}
        }
        
    except Exception as e:
        print(f"Error processing {name}: {e}")
        import traceback
        traceback.print_exc()

# Save summary
summary_file = output_dir / "dataset_summary.json"
with open(summary_file, "w") as f:
    json.dump(summary, f, indent=2)

print(f"\n\nDataset summary saved to: {summary_file}")
print("\nSummary:")
for name, info in summary.items():
    print(f"\n{name}:")
    print(f"  Num classes: {info['num_classes']}")
    for split, count in info["splits"].items():
        print(f"  {split}: {count} examples")
