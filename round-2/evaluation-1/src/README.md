# Statistical Evaluation of LLM Calibration Methods

## Overview
This evaluation compares thermodynamic entropy calibration against temperature scaling and uncalibrated baselines on the SST-2 dataset.

## Methods Evaluated
1. **Uncalibrated**: Raw model outputs without calibration
2. **Temperature Scaling**: Standard calibration method (Guo et al. 2017)
3. **Thermodynamic Entropy Calibration**: Physics-inspired method using per-sample temperature based on predictive entropy

## Metrics Computed
- **Expected Calibration Error (ECE)**: With 95% bootstrap confidence intervals (1000 iterations)
- **Brier Score**: With 95% bootstrap CI
- **Negative Log-Likelihood (NLL)**: With 95% bootstrap CI
- **Accuracy**: With 95% bootstrap CI

## Statistical Tests
- **Paired Wilcoxon Signed-Rank Test**: For per-sample NLL comparison
- **Bootstrap Hypothesis Test**: For ECE difference significance
- **Cohen's d**: Effect size for practical significance

## Key Results

| Method | ECE | Brier | NLL | Accuracy |
|--------|-----|-------|-----|----------|
| Uncalibrated | 0.2431 | 0.4947 | 1.2497 | 0.7486 |
| Temperature Scaling | 0.0313 | 0.3758 | 0.5627 | 0.7486 |
| Thermodynamic Entropy | 0.1619 | 0.4296 | 0.6846 | 0.7486 |

## Statistical Significance
- Temperature Scaling vs Uncalibrated: ECE reduction = 87.1% (p=0.343)
- Thermodynamic Entropy vs Uncalibrated: ECE reduction = 33.4% (p=0.509)
- Note: P-values > 0.05 indicate results may not be statistically significant with this sample size (n=175)

## Files
- `eval.py`: Main evaluation script
- `results/eval_out.json`: Main evaluation output (exp_eval_sol_out schema)
- `results/reliability_*.png`: Reliability diagrams for each method
- `results/accuracy_calibration_tradeoff.png`: Tradeoff analysis plots
- `results/tradeoff_data.json`: Raw tradeoff curve data
- `results/statistical_tests.json`: Statistical test results
- `results/reliability_data.json`: Reliability diagram data for plotting
- `experiment_out.json`: Copy of experiment output (for reference)
- `metadata.json`: Copy of experiment metadata (for reference)

## Usage
```bash
source .venv/bin/activate
python eval.py
```

## Conclusions
1. Temperature scaling provides the best calibration (lowest ECE)
2. Thermodynamic entropy improves over uncalibrated but not as good as temperature scaling on this dataset
3. All methods maintain the same accuracy (calibration doesn't affect predictions)
4. The improvement over uncalibrated may not be statistically significant with this sample size
