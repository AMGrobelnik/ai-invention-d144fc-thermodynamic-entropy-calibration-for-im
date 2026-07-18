#!/usr/bin/env python3
"""Convert method_out.json to exp_gen_sol_out schema format."""
import json
import numpy as np
from pathlib import Path

# Load original results
workspace = Path("/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_art/gen_art_experiment_1")
data_path = workspace.parent.parent.parent / "iter_1" / "gen_art" / "gen_art_dataset_1" / "full_data_out.json"

with open(data_path) as f:
    full_data = json.load(f)

with open(workspace / "method_out.json") as f:
    results = json.load(f)

# Build output in exp_gen_sol_out format
output = {
    "metadata": {
        "experiment": "TEC_vs_TS_evaluation",
        "methods": ["Uncalibrated", "Temperature Scaling", "TEC"],
        "metrics": ["ECE", "Brier", "NLL", "Accuracy"],
    },
    "datasets": []
}

# Get method results by dataset
method_results = {}
for r in results.get("results", []):
    dataset = r["dataset"]
    if dataset not in method_results:
        method_results[dataset] = {}
    method_results[dataset][r["method"]] = r

# For each dataset, create examples with predictions
for dataset_info in full_data["datasets"]:
    dataset_name = dataset_info["dataset"]
    
    if dataset_name not in method_results:
        continue
    
    # Get test split (same 20% as in method.py with seed 42)
    examples = dataset_info["examples"]
    n = len(examples)
    np.random.seed(42)
    indices = np.random.permutation(n)
    test_idx = indices[int(0.8 * n):]
    
    dataset_output = {
        "dataset": dataset_name,
        "examples": []
    }
    
    for idx in test_idx[:600]:  # Match the 600 test examples used
        ex = examples[idx]
        input_text = ex["input"]
        output_label = ex["output"]
        
        example_output = {
            "input": input_text,
            "output": output_label,
        }
        
        # Add predictions from each method
        if dataset_name in method_results:
            for method_name, method_data in method_results[dataset_name].items():
                # Create a simple prediction string
                example_output[f"predict_{method_name.replace(' ', '_')}"] = str(method_data.get("ece", "N/A"))
        
        dataset_output["examples"].append(example_output)
    
    output["datasets"].append(dataset_output)

# Save
with open(workspace / "method_out.json", 'w') as f:
    json.dump(output, f, indent=2)

print(f"Converted to exp_gen_sol_out format")
print(f"Datasets: {len(output['datasets'])}")
print(f"Total examples: {sum(len(ds['examples']) for ds in output['datasets'])}")
