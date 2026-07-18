# TEC vs TS Calibration Experiment - Results Summary

## Experiment Completed: 2026-07-18

### Methods Compared
1. **Uncalibrated**: Softmax on raw logits (T=1.0)
2. **Temperature Scaling (TS)**: Single temperature T tuned on validation set
3. **Thermodynamic Entropy Calibration (TEC)**: Per-sample T based on entropy + margin

### Datasets (3000 examples each, 60/20/20 split)
- SST-2 (binary, distilbert fine-tuned)
- QNLI (binary, bert-base-uncased)
- AG News (4-class, bert-base-uncased)
- MNLI (3-class, roberta-large-mnli)
- DBpedia (14-class, bert-base-uncased)

### Key Results (ECE = Expected Calibration Error, lower is better)

| Dataset  | Uncalibrated | TS      | TEC     | Winner |
|----------|---------------|---------|---------|--------|
| SST-2   | 0.0078        | 0.0042  | 0.0071  | TS     |
| QNLI     | 0.1364        | 0.0076  | 0.0042  | TEC   |
| AG News  | 0.0625        | 0.0029  | 0.0146  | TS     |
| MNLI     | 0.6337        | 0.1686  | 0.2293  | TS     |
| DBpedia  | 0.0531        | 0.0088  | 0.0075  | TEC   |

### Findings
- TEC outperformed TS on 2/5 datasets (QNLI, DBpedia)
- TS outperformed TEC on 3/5 datasets (SST-2, AG News, MNLI)
- Both methods significantly improved calibration over uncalibrated baseline
- TEC provides per-sample temperature adaptation but doesn't consistently beat TS

### Output Files
- `method_out.json`: Full results with bootstrap confidence intervals
- `logs/run.log`: Detailed experiment log
- `method.py`: Complete experiment implementation

### Reproducibility
All code and results are in the workspace directory. Run `python method.py` to reproduce.
