#!/usr/bin/env python3
import json
from pathlib import Path

def transform_dataset(input_file, dataset_name):
    with open(Path(input_file), "r") as f:
        data = json.load(f)
    examples = []
    for row in data:
        example = {
            "input": row["text"],
            "output": str(row["label"]),
            "metadata_label_text": row.get("label_text", ""),
            "metadata_original_label": row["metadata"]["original_label"],
        }
        examples.append(example)
    return {"dataset": dataset_name, "examples": examples}

def main():
    datasets = [
        ("temp/datasets/sst-2_train.json", "sst-2"),
        ("temp/datasets/ag_news_train.json", "ag_news"),
        ("temp/datasets/mnli_train.json", "mnli"),
        ("temp/datasets/qnli_train.json", "qnli"),
        ("temp/datasets/dbpedia_train.json", "dbpedia"),
    ]
    
    all_datasets = []
    for input_file, dataset_name in datasets:
        print(f"Transforming {dataset_name}...")
        dataset_group = transform_dataset(input_file, dataset_name)
        all_datasets.append(dataset_group)
        print(f"  Added {len(dataset_group['examples'])} examples")
    
    output = {
        "datasets": all_datasets,
        "metadata": {
            "description": "Text classification datasets for LLM calibration",
            "num_datasets": len(all_datasets),
            "total_examples": sum(len(d["examples"]) for d in all_datasets)
        }
    }
    
    with open("full_data_out.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved {output['metadata']['total_examples']} examples to full_data_out.json")

if __name__ == "__main__":
    main()
