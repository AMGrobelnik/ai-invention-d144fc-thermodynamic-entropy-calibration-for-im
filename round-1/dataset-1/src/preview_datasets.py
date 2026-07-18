#!/usr/bin/env python3
"""Preview HuggingFace datasets for text classification."""

from datasets import load_dataset
import json
from pathlib import Path

# Create output directory
output_dir = Path("temp/datasets")
output_dir.mkdir(parents=True, exist_ok=True)

# List of candidate datasets to preview
datasets_to_preview = [
    ("stanfordnlp/sst2", "sst2"),
    ("fancyzhx/ag_news", "ag_news"),
    ("CogComp/trec", "trec"),
    ("stanfordnlp/imdb", "imdb"),
    ("fancyzhx/dbpedia_14", "dbpedia"),
    ("community-datasets/yahoo_answers_topics", "yahoo_answers"),
    ("nyu-mll/glue", "glue_mnli"),
    ("nyu-mll/glue", "glue_qnli"),
    ("nyu-mll/glue", "glue_rte"),
]

for dataset_id, name in datasets_to_preview:
    try:
        print(f"\n{'='*60}")
        print(f"Previewing: {dataset_id} ({name})")
        print(f"{'='*60}")
        
        # Load dataset
        if "glue" in dataset_id and name.startswith("glue_"):
            config = name.split("_")[1]
            dataset = load_dataset(dataset_id, config, split="train", streaming=True)
        else:
            dataset = load_dataset(dataset_id, split="train", streaming=True)
        
        # Get first 3 rows
        rows = []
        for i, row in enumerate(dataset):
            rows.append(row)
            if i >= 2:  # Get 3 rows (0, 1, 2)
                break
        
        # Print preview
        print(f"\nColumns: {list(rows[0].keys())}")
        print(f"\nFirst 3 rows:")
        for i, row in enumerate(rows):
            print(f"\nRow {i+1}:")
            for key, value in row.items():
                if isinstance(value, str) and len(value) > 100:
                    print(f"  {key}: {value[:100]}...")
                else:
                    print(f"  {key}: {value}")
        
        # Save preview to file
        preview_file = output_dir / f"preview_{name}.json"
        with open(preview_file, "w") as f:
            json.dump(rows, f, indent=2, default=str)
        print(f"\nPreview saved to: {preview_file}")
        
    except Exception as e:
        print(f"Error previewing {dataset_id}: {e}")
        import traceback
        traceback.print_exc()
