# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · `upd_hypo`
> Run: `run_3fUR0i5e8NC7` — Thermodynamic Entropy Calibration for Improved Confidence Estimation in LLM Classifiers
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-18 17:56:05 UTC

````
<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: Evaluate thermodynamic entropy calibration for LLMs
hypothesis: >-
  Physics-inspired calibration methods that adjust per-sample temperature based on predictive entropy and decision margin
  can provide interpretable confidence calibration for LLM classifiers, though their empirical advantage over standard temperature
  scaling remains unproven and may be limited to specific scenarios such as heterogeneous miscalibration patterns or multi-class
  settings with class-conditional effects. The primary potential novelty lies in inference-time temperature annealing (currently
  unimplemented) rather than post-hoc calibration.
motivation: >-
  LLM classifiers often exhibit overconfidence, which undermines reliability in high-stakes applications. A physics-inspired
  calibration method that treats uncertainty as entropy could provide a principled, model-agnostic way to improve trustworthiness
  without extensive retraining.
assumptions:
- >-
  Predictive uncertainty in LLMs can be meaningfully analogized to thermodynamic entropy.
- >-
  Temperature-based annealing during inference does not severely degrade classification accuracy.
- >-
  The entropy of the output distribution correlates with true error probability in a way that can be adjusted via temperature
  scaling.
investigation_approach: >-
  Implement a temperature-annealing schedule during decoding or final-layer logit adjustment, compute entropy-based uncertainty
  metrics, and evaluate calibration error (ECE, Brier score) on standard classification benchmarks compared to baseline temperature
  scaling and other calibration methods.
success_criteria: >-
  The proposed method achieves statistically significant lower expected calibration error (ECE) and Brier score compared to
  standard temperature scaling and uncalibrated baselines, while maintaining or improving accuracy on held-out test sets.
related_works:
- >-
  Temperature scaling (Guo et al., 2017) calibrates by tuning a single temperature parameter on validation data; our approach
  differs by using an annealing schedule inspired by thermodynamic principles rather than a fixed scaling factor.
- >-
  Entropy-based uncertainty estimation (e.g., in Bayesian neural networks) uses Shannon entropy of predictive distributions;
  we extend this by explicitly linking entropy to a thermodynamic analogy and incorporating an annealing procedure during
  inference.
inspiration: >-
  Thermodynamic entropy and temperature annealing from statistical physics, where entropy measures disorder and temperature
  controls the system's exploration of states; adapted to the context of LLM predictive distributions.
terms:
- term: Expected Calibration Error (ECE)
  definition: >-
    A metric that measures the difference between a model's predicted confidence and its actual accuracy by binning predictions
    and computing weighted absolute differences.
- term: Temperature scaling
  definition: >-
    A post-hoc calibration method that divides logits by a scalar temperature parameter before applying softmax to adjust
    confidence scores.
- term: Thermodynamic entropy
  definition: >-
    A physical quantity representing the amount of disorder or randomness in a system, often used in statistical mechanics
    to describe the distribution of microstates.
- term: Annealing
  definition: >-
    A process of gradually changing a control parameter (like temperature) to allow a system to reach a more stable or optimal
    state, commonly used in optimization and physics.
summary: >-
  This hypothesis proposes a physics-inspired calibration method that treats LLM predictive uncertainty as thermodynamic entropy
  and uses temperature annealing during inference to improve confidence calibration.
_relation_rationale: >-
  Refined to acknowledge negative results; narrowed from universal claim to conditional/scenario-specific
_confidence_delta: decreased
_key_changes:
- >-
  Removed claim that method 'produces better-calibrated confidence scores' - evidence shows TS outperforms TEC
- >-
  Added caveat that empirical advantage 'remains unproven' given experimental results
- >-
  Narrowed scope to 'specific scenarios' (heterogeneous miscalibration, multi-class) not yet tested
- Clarified that inference-time annealing is unimplemented potential novelty
- Shifted from positive performance claim to evaluative/exploratory framing
relation_type: evolution
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

--- Item 1 ---
id: art_EQYpVcsEAvw1
type: research
title: LLM Calibration and Thermodynamic Entropy Methods
summary: >-
  This comprehensive literature review surveys state-of-the-art methods for LLM calibration, entropy-based uncertainty estimation,
  thermodynamic principles in machine learning, and standard evaluation metrics. Key findings include: (1) Temperature scaling
  (Guo et al., 2017) is the baseline calibration method using formula $\hat{q}_i = \max_k \sigma_{SM}(z_i/T)^{(k)}$ [1]. Extensions
  include Dirichlet calibration (Kull et al., 2019) [5], Parameterized Temperature Scaling (Tomani et al., 2021) [6], and
  Adaptive Temperature Scaling (Joy et al., 2023; Xie et al., 2024) [7, 8]. (2) Semantic entropy (Kuhn et al., 2023) clusters
  semantically equivalent answers to improve uncertainty estimation on TriviaQA and CoQA [2]. (3) The softmax function is
  mathematically identical to the Boltzmann distribution from statistical mechanics, with temperature T corresponding to thermodynamic
  temperature [3, 12]. Shannon entropy and Gibbs entropy share the same mathematical form but differ physically [13]. (4)
  Temperature annealing during inference for calibration appears novel - while Exploratory Annealed Decoding (EAD) uses annealing
  for RL exploration [4], no work combines temperature scaling with annealing for calibration. (5) Standard metrics include
  Expected Calibration Error (ECE) [1], Brier score [15], and benchmarks include TriviaQA, CoQA [16], and GLUE [17]. The review
  identifies temperature annealing during inference for calibration as a potential novelty, with high confidence (90%) that
  this approach is unexplored in the literature.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 2 ---
id: art_SSmr6ZrIe2PQ
type: dataset
title: Text classification datasets for LLM calibration
summary: >-
  Successfully collected 5 diverse text classification datasets from HuggingFace Hub for LLM calibration evaluation. Datasets
  include binary (SST-2, QNLI) and multi-class (AG News with 4 classes, MNLI with 3 classes, DBpedia with 14 classes) classification
  tasks with varying difficulty levels. All datasets were standardized to a unified JSON schema with text input, integer labels
  (0-indexed), and metadata fields. Train/validation/test splits were created with stratified sampling to preserve class distribution.
  Validation sets are sized appropriately for temperature tuning (1-5K examples). The datasets were transformed to exp_sel_data_out.json
  schema format with 150,000 total examples across 5 datasets. Full, mini (15 examples), and preview (15 examples, truncated)
  variants were generated. All files passed JSON schema validation. Total dataset size is 116MB (under 300MB limit). The datasets
  are established benchmarks from GLUE, AG News, and DBpedia, ensuring evaluation comparability. Python scripts (data.py,
  download_and_standardize.py, subsample_datasets.py) are included for reproducibility.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 3 ---
id: art_Oc5BxFWZU7a3
type: experiment
title: Thermodynamic Entropy Calibration Experiment
summary: |-
  Implemented and evaluated a physics-inspired calibration method that treats LLM predictive uncertainty as thermodynamic entropy. The method adjusts per-sample temperature based on predictive entropy and margin (difference between top-2 probabilities). Compared against uncalibrated baseline and standard temperature scaling (Guo et al. 2017) on synthetic miscalibrated data mimicking SST-2 sentiment classification.

  Key results:
  - Uncalibrated: ECE=0.243, Accuracy=74.9%
  - Temperature Scaling: ECE=0.031 (87.1% reduction), Accuracy=74.9%
  - Thermodynamic Entropy: ECE=0.162 (33.4% reduction), Accuracy=74.9%

  Temperature scaling outperformed the thermodynamic method on this dataset, suggesting global temperature adjustment is more effective for uniform miscalibration. The thermodynamic method still provided meaningful calibration improvement and offers interpretability through the physics analogy.

  Experiment includes: method.py implementation, reliability diagrams, hyperparameter tuning via grid search, and full JSON output matching exp_gen_sol_out schema.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 4 ---
id: art_xdUSFFTTrRuY
type: experiment
in_dependencies:
- id: art_SSmr6ZrIe2PQ
  label: datasets
title: TEC vs TS calibration on 5 LLM datasets
summary: >-
  Completed experiment comparing Thermodynamic Entropy Calibration (TEC) vs Temperature Scaling (TS) on 5 text classification
  datasets (SST-2, QNLI, AG News, MNLI, DBpedia) using pre-trained transformers. Methods: (1) Uncalibrated baseline, (2) Temperature
  Scaling, (3) TEC with per-sample temperature based on entropy + margin. Metrics: ECE, Brier score, NLL, Accuracy with bootstrap
  CI (200 samples). Heterogeneous analysis on easy/hard splits by decision margin. Results: TEC outperformed TS on 2/5 datasets
  (QNLI, DBpedia), TS outperformed TEC on 3/5 datasets. Both methods significantly improved calibration over uncalibrated
  baseline. Output saved to method_out.json in exp_gen_sol_out schema format with per-example predictions.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 5 ---
id: art_5XrEi0TPtFOf
type: experiment
in_dependencies:
- id: art_SSmr6ZrIe2PQ
  label: datasets
- id: art_EQYpVcsEAvw1
  label: methodology
title: Temperature Annealing LLM Calibration Experiment
summary: >-
  Implemented and evaluated inference-time temperature annealing for LLM calibration on SST-2, AG News, and DBpedia datasets.
  Compared against Temperature Scaling (TS) and Thermodynamic Entropy Calibration (TEC) baselines. Used simulated logits (NumPy-based
  implementation) to test four methods: uncalibrated baseline, TS, TEC, and Annealing+Softmax. Results on 1000 samples show
  TS reduces ECE by ~56% on SST-2 (0.2985 to 0.1302). Annealing shows mixed results - helps SST-2 (ECE 0.2400 vs 0.2985 uncalibrated)
  but not AG News. All methods maintain similar accuracy while improving calibration. Output validates against exp_gen_sol_out.json
  schema.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 6 ---
id: art_PHvp8viBEPFq
type: evaluation
in_dependencies:
- id: art_Oc5BxFWZU7a3
  label: baseline-results
- id: art_SSmr6ZrIe2PQ
  label: datasets
title: Statistical Evaluation of LLM Calibration Methods
summary: |-
  This evaluation artifact provides a comprehensive statistical comparison of three calibration methods for LLM classifiers: uncalibrated baseline, standard temperature scaling (Guo et al. 2017), and thermodynamic entropy calibration (proposed method). The evaluation uses the SST-2 sentiment classification dataset with 175 test samples.

  Metrics computed with 95% bootstrap confidence intervals (1000 iterations):
  1. Expected Calibration Error (ECE): Primary metric for calibration quality
  2. Brier Score: Penalizes both miscalibration and poor accuracy
  3. Negative Log-Likelihood (NLL): Measures pure probabilistic quality
  4. Accuracy: Percentage of correct predictions

  Statistical significance tests:
  1. Paired Wilcoxon Signed-Rank Test: Compares per-sample NLL between methods
  2. Bootstrap Hypothesis Test: Tests if difference in ECE between methods is significant
  3. Cohen's d: Effect size for practical significance of differences

  Additional analyses:
  1. Reliability diagrams: Visual calibration assessment for each method
  2. ECE decomposition: Breakdown of ECE by confidence bins to identify where each method succeeds/fails
  3. Accuracy-calibration tradeoff curves: Plot accuracy vs ECE for varying temperature parameters

  Key results:
  - Temperature scaling achieves best calibration (ECE=0.0313 with 95% CI [0.0129, 0.0959])
  - Thermodynamic entropy improves over uncalibrated (ECE=0.1619 vs 0.2431)
  - All methods maintain same accuracy (74.86%), confirming calibration doesn't affect predictions
  - Statistical significance: P-values > 0.05 suggest results may not be statistically significant with n=175

  The evaluation output includes:
  - eval.py: Main evaluation script
  - results/eval_out.json: Main evaluation output (validated against exp_eval_sol_out schema)
  - results/full_eval_out.json: Full evaluation output
  - results/mini_eval_out.json: Mini version (3 examples)
  - results/preview_eval_out.json: Preview version (3 examples, truncated)
  - results/reliability_*.png: Reliability diagrams for each method
  - results/accuracy_calibration_tradeoff.png: Tradeoff analysis plots
  - results/tradeoff_data.json: Raw tradeoff curve data
  - results/statistical_tests.json: Statistical test results
  - results/reliability_data.json: Reliability diagram data for plotting
workspace_path: >-
  /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</all_artifacts>

<new_artifacts_this_iteration>
These 3 artifacts were created THIS iteration.

id: art_xdUSFFTTrRuY
type: experiment
in_dependencies:
- id: art_SSmr6ZrIe2PQ
  label: datasets
title: TEC vs TS calibration on 5 LLM datasets
summary: >-
  Completed experiment comparing Thermodynamic Entropy Calibration (TEC) vs Temperature Scaling (TS) on 5 text classification
  datasets (SST-2, QNLI, AG News, MNLI, DBpedia) using pre-trained transformers. Methods: (1) Uncalibrated baseline, (2) Temperature
  Scaling, (3) TEC with per-sample temperature based on entropy + margin. Metrics: ECE, Brier score, NLL, Accuracy with bootstrap
  CI (200 samples). Heterogeneous analysis on easy/hard splits by decision margin. Results: TEC outperformed TS on 2/5 datasets
  (QNLI, DBpedia), TS outperformed TEC on 3/5 datasets. Both methods significantly improved calibration over uncalibrated
  baseline. Output saved to method_out.json in exp_gen_sol_out schema format with per-example predictions.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_5XrEi0TPtFOf
type: experiment
in_dependencies:
- id: art_SSmr6ZrIe2PQ
  label: datasets
- id: art_EQYpVcsEAvw1
  label: methodology
title: Temperature Annealing LLM Calibration Experiment
summary: >-
  Implemented and evaluated inference-time temperature annealing for LLM calibration on SST-2, AG News, and DBpedia datasets.
  Compared against Temperature Scaling (TS) and Thermodynamic Entropy Calibration (TEC) baselines. Used simulated logits (NumPy-based
  implementation) to test four methods: uncalibrated baseline, TS, TEC, and Annealing+Softmax. Results on 1000 samples show
  TS reduces ECE by ~56% on SST-2 (0.2985 to 0.1302). Annealing shows mixed results - helps SST-2 (ECE 0.2400 vs 0.2985 uncalibrated)
  but not AG News. All methods maintain similar accuracy while improving calibration. Output validates against exp_gen_sol_out.json
  schema.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_art/gen_art_experiment_2
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

id: art_PHvp8viBEPFq
type: evaluation
in_dependencies:
- id: art_Oc5BxFWZU7a3
  label: baseline-results
- id: art_SSmr6ZrIe2PQ
  label: datasets
title: Statistical Evaluation of LLM Calibration Methods
summary: |-
  This evaluation artifact provides a comprehensive statistical comparison of three calibration methods for LLM classifiers: uncalibrated baseline, standard temperature scaling (Guo et al. 2017), and thermodynamic entropy calibration (proposed method). The evaluation uses the SST-2 sentiment classification dataset with 175 test samples.

  Metrics computed with 95% bootstrap confidence intervals (1000 iterations):
  1. Expected Calibration Error (ECE): Primary metric for calibration quality
  2. Brier Score: Penalizes both miscalibration and poor accuracy
  3. Negative Log-Likelihood (NLL): Measures pure probabilistic quality
  4. Accuracy: Percentage of correct predictions

  Statistical significance tests:
  1. Paired Wilcoxon Signed-Rank Test: Compares per-sample NLL between methods
  2. Bootstrap Hypothesis Test: Tests if difference in ECE between methods is significant
  3. Cohen's d: Effect size for practical significance of differences

  Additional analyses:
  1. Reliability diagrams: Visual calibration assessment for each method
  2. ECE decomposition: Breakdown of ECE by confidence bins to identify where each method succeeds/fails
  3. Accuracy-calibration tradeoff curves: Plot accuracy vs ECE for varying temperature parameters

  Key results:
  - Temperature scaling achieves best calibration (ECE=0.0313 with 95% CI [0.0129, 0.0959])
  - Thermodynamic entropy improves over uncalibrated (ECE=0.1619 vs 0.2431)
  - All methods maintain same accuracy (74.86%), confirming calibration doesn't affect predictions
  - Statistical significance: P-values > 0.05 suggest results may not be statistically significant with n=175

  The evaluation output includes:
  - eval.py: Main evaluation script
  - results/eval_out.json: Main evaluation output (validated against exp_eval_sol_out schema)
  - results/full_eval_out.json: Full evaluation output
  - results/mini_eval_out.json: Mini version (3 examples)
  - results/preview_eval_out.json: Preview version (3 examples, truncated)
  - results/reliability_*.png: Reliability diagrams for each method
  - results/accuracy_calibration_tradeoff.png: Tradeoff analysis plots
  - results/tradeoff_data.json: Raw tradeoff curve data
  - results/statistical_tests.json: Statistical test results
  - results/reliability_data.json: Reliability diagram data for plotting
workspace_path: >-
  /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_art/gen_art_evaluation_1
out_expected_files:
- eval.py
- full_eval_out.json
- mini_eval_out.json
- preview_eval_out.json
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# Introduction

Large Language Models (LLMs) have demonstrated remarkable capabilities across natural language understanding tasks, yet their deployment in high-stakes domains remains hindered by unreliable confidence estimates. A well-calibrated classifier should produce predicted probabilities that reflect true outcome frequencies: among all predictions made with 80% confidence, approximately 80% should be correct [1]. Modern neural networks, including LLMs, systematically violate this property, exhibiting overconfidence where predicted probabilities exceed actual accuracy [1].

This miscalibration is particularly problematic for applications in healthcare, law, and autonomous systems, where overconfident incorrect predictions can lead to consequential errors. While post-hoc calibration methods like temperature scaling [1] effectively reduce calibration error, they apply a global temperature adjustment that may not account for varying uncertainty across individual predictions. Recent work has explored input-dependent temperature adjustment [6, 7, 8], but these approaches learn temperature from data using neural networks rather than deriving functional forms from principled theoretical foundations.

This paper explores whether treating predictive uncertainty as thermodynamic entropy—drawing on the mathematical equivalence between the softmax function and the Boltzmann distribution—can inspire interpretable calibration approaches. The key insight is that temperature in softmax distributions plays an analogous role to thermodynamic temperature in statistical mechanics: it controls the entropy (dispersion) of the probability distribution over classes [3, 12].

## 1.1 Problem Statement

Given a classifier that produces logits $z_i$ for each class $i$, the standard approach applies a global temperature scaling:

$$p_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

where $T > 0$ is a scalar temperature parameter optimized on a validation set to minimize Expected Calibration Error (ECE) [1].

The limitation of this approach is that a single temperature $T$ must balance calibration across all predictions, regardless of each sample's intrinsic difficulty or ambiguity. Intuitively, easy examples (where the correct class is clear from the input) and ambiguous examples (where multiple interpretations are plausible) may benefit from different temperature adjustments. Prior work on adaptive temperature scaling [7, 8] addresses this limitation by predicting per-sample temperatures using learned functions, but does not provide a physically interpretable connection between temperature and uncertainty.

## 1.2 Proposed Approach

We propose Thermodynamic Entropy Calibration (TEC), which computes per-sample temperatures based on two uncertainty indicators:

1. **Predictive entropy** $H(p) = -\sum_i p_i \log p_i$: Higher entropy indicates greater uncertainty.
2. **Decision margin** $m = p_{(1)} - p_{(2)}$: The difference between the top two predicted probabilities (higher margin = more confident).

The per-sample temperature is computed as:

$$T_i = T_0 \cdot (1 + \alpha \cdot H(p_i) + \beta \cdot (1 - m_i))$$

where $T_0$, $\alpha$, and $\beta$ are hyperparameters tuned on a validation set.

This formulation has a physical interpretation: samples with high entropy (analogous to high thermodynamic entropy) or low margin (analogous to low energy difference between states) receive higher temperatures, producing flatter, more conservative probability distributions.

## 1.3 Summary of Contributions

This paper makes the following contributions:

1. We introduce Thermodynamic Entropy Calibration (TEC), a physics-inspired post-hoc calibration method that adjusts per-sample temperature based on predictive entropy and decision margin. The method is compared against standard temperature scaling and uncalibrated baselines on five diverse text classification datasets using real pre-trained transformer embeddings.

2. We provide a comprehensive evaluation showing that TEC provides **conditional** calibration benefits: it outperforms temperature scaling on datasets with heterogeneous miscalibration (QNLI, DBpedia), while temperature scaling remains superior on simpler tasks. Both methods significantly improve calibration over uncalibrated baselines.

3. We evaluate TEC on multi-class datasets with up to 14 classes (DBpedia), demonstrating that per-sample temperature adjustment can help in settings where class-conditional miscalibration patterns exist.

4. We discuss the theoretical implications and limitations of treating predictive uncertainty as thermodynamic entropy, and provide an honest assessment of when physics-inspired calibration does and does not provide empirical benefits.

# Related Work

## 2.1 Calibration Methods for Neural Networks

Temperature scaling, introduced by Guo et al. [1], is the simplest and most widely used post-hoc calibration method for modern neural networks. It optimizes a single scalar temperature parameter $T$ by minimizing Negative Log-Likelihood (NLL) on a validation set. Despite its simplicity, temperature scaling often outperforms more complex methods like vector scaling and matrix scaling [1].

Recent extensions have proposed more flexible calibration approaches:

- **Dirichlet calibration** [5] generalizes temperature scaling to natively handle multi-class settings using Dirichlet distributions, improving calibration especially when class-conditional miscalibration patterns exist.

- **Parameterized Temperature Scaling (PTS)** [6] computes prediction-specific temperatures using a small neural network, reducing calibration error by approximately 30% over standard temperature scaling on vision tasks.

- **Adaptive Temperature Scaling (ATS)** [7] predicts temperature scaling parameters for each input using a lightweight network trained on top of frozen embeddings. ATS is closely related to our work but learns the temperature prediction function from data rather than deriving it from physical principles.

- **Calibrating Language Models with Adaptive Temperature Scaling** [8] extends ATS specifically for LLMs, showing that per-token temperature adjustment can improve calibration in language generation tasks.

**Differentiation from prior work.** TEC differs from ATS [7] and PTS [6] in its use of physics-inspired principles: rather than learning temperature adjustments from data alone, we derive the functional form of per-sample temperature from the thermodynamic analogy between predictive distributions and Boltzmann distributions. The TEC formula $T_i = T_0 \cdot (1 + \alpha \cdot H(p_i) + \beta \cdot (1 - m_i))$ is a **interpretable heuristic** motivated by statistical mechanics, not a learned black-box function. This provides transparency: practitioners can examine how entropy and margin influence each prediction's temperature. However, we acknowledge that this heuristic does not currently outperform learned approaches on all datasets (see Section 4.2).

## 2.2 Entropy-Based Uncertainty Estimation

Entropy is a fundamental measure of uncertainty in probability distributions. In Bayesian neural networks, the entropy of the predictive distribution quantifies total uncertainty (sum of aleatoric and epistemic uncertainty) [11].

For LLMs, recent work has adapted entropy-based uncertainty estimation to the generative setting:

- **Predictive entropy** [2] computes $PE(x) = H(Y|x) = -\int p(y|x) \ln p(y|x) dy$ over multiple generated samples, measuring uncertainty in generated outputs.

- **Semantic entropy** [2] addresses the observation that LLMs can generate semantically equivalent but lexically different responses. By clustering semantically equivalent samples and computing entropy over meaning clusters rather than individual tokens, semantic entropy provides better uncertainty estimates than token-level entropy.

- **Length-normalized entropy** [2] normalizes log-probabilities by sequence length to address the issue that longer generations accumulate more uncertainty.

Our approach uses **predictive entropy** (computed from the classifier's output distribution rather than generated samples) as one component of per-sample temperature adjustment, connecting entropy-based uncertainty to the thermodynamic interpretation of temperature. Importantly, TEC uses entropy from a **single forward pass** (the classifier's output distribution), making it computationally cheaper than methods requiring multiple samples [2].

## 2.3 Thermodynamic Principles in Machine Learning

The connection between information theory and statistical mechanics has been recognized since the work of Jaynes [13]. The key mathematical equivalences are:

1. **Boltzmann distribution = Softmax**: The Boltzmann distribution from statistical mechanics, $p_i = \frac{1}{Z} e^{-\beta E_i}$ where $\beta = 1/T$, is mathematically identical to the softmax function with logits $z_i = -E_i$ (negative energies) [3, 12].

2. **Gibbs entropy = Shannon entropy**: The Gibbs entropy formula $S = -k_B \sum_i p_i \ln p_i$ has the same mathematical form as Shannon entropy $H = -\sum_i p_i \log p_i$, differing only in physical units ($k_B$ is Boltzmann's constant) [13].

These equivalences suggest that techniques from statistical mechanics might inform machine learning practice. For example, simulated annealing [14] uses a temperature schedule to escape local optima in optimization problems—a concept that could be adapted to temperature scheduling during LLM inference. However, existing work using temperature schedules in LLMs focuses on reinforcement learning exploration (e.g., Exploratory Annealed Decoding [4]) rather than calibration. 

**Novelty statement.** To our knowledge, no prior work combines **per-sample temperature scaling** with the **thermodynamic entropy analogy** for improved calibration. While ATS [7] and PTS [6] use per-sample temperatures, they do not draw on statistical mechanics for the functional form. Conversely, work on thermodynamic connections [3, 12] establishes the mathematical equivalence but does not operationalize it for calibration. Our contribution is to bridge these strands by deriving an interpretable, physics-inspired calibration method and evaluating it on real LLM embeddings.

## 2.4 Calibration Metrics and Benchmarks

The standard metric for classification calibration is Expected Calibration Error (ECE) [1], which partitions predictions into $M$ bins based on confidence and computes the weighted average of calibration gaps:

$$ECE = \sum_{m=1}^M \frac{|B_m|}{n} |acc(B_m) - conf(B_m)|$$

where $B_m$ is the set of predictions in bin $m$, and $acc(B_m)$ and $conf(B_m)$ are the accuracy and average confidence in that bin.

Other metrics include:

- **Brier Score** [15]: Mean squared difference between predicted probabilities and one-hot encoded true labels, ranging from 0 (perfect) to 1 (worst).
- **Negative Log-Likelihood (NLL)**: Measures the average log-probability assigned to the true class, with lower values indicating better calibration.
- **Maximum Calibration Error (MCE)** [1]: The worst-case calibration gap across bins, focusing on the largest miscalibration.

Benchmarks for evaluating LLM calibration include TriviaQA and CoQA (used in semantic uncertainty work [2]), GLUE and SuperGLUE [17] (general language understanding), and TruthfulQA [18] (measuring truthfulness). Our work uses five datasets spanning binary and multi-class classification: SST-2 (binary sentiment), QNLI (binary natural language inference), AG News (4-class topic classification), MNLI (3-class textual entailment), and DBpedia (14-class ontology classification).

# Methods

## 3.1 Thermodynamic Entropy Calibration

Our proposed Thermodynamic Entropy Calibration (TEC) method is a post-hoc calibration approach that adjusts per-sample temperature based on uncertainty estimates. The method consists of three steps:

**Step 1: Compute uncalibrated probabilities and uncertainty metrics.**

Given logits $z_i$ for sample $i$, compute:

$$p_i = \text{softmax}(z_i) \quad \text{(uncalibrated probabilities)}$$

$$H(p_i) = -\sum_k p_{i,k} \log p_{i,k} \quad \text{(predictive entropy)}$$

Sort probabilities in descending order and compute:

$$m_i = p_{i,(1)} - p_{i,(2)} \quad \text{(decision margin)}$$

**Step 2: Compute per-sample temperature.**

$$T_i = T_0 \cdot (1 + \alpha \cdot H(p_i) + \beta \cdot (1 - m_i))$$

where:
- $T_0$ is a base temperature (analogous to the global temperature in temperature scaling)
- $\alpha \geq 0$ controls the weight of entropy
- $\beta \geq 0$ controls the weight of (inverse) margin

This formulation ensures that samples with high entropy (uncertain predictions) or low margin (close competition between top classes) receive higher temperatures, producing flatter, more conservative probability distributions. The hyperparameters $T_0$, $\alpha$, and $\beta$ are tuned on a validation set (see Section 3.3).

**Step 3: Apply temperature adjustment.**

$$\tilde{p}_i = \text{softmax}(z_i / T_i) \quad \text{(calibrated probabilities)}$$

[FIGURE:fig1]

## 3.2 Physical Interpretation

The method draws on the following physical analogies:

- **Logits as negative energies**: Setting $E_{i,k} = -z_{i,k}$ (negative logit for class $k$) makes the softmax distribution identical to the Boltzmann distribution $p_{i,k} \propto e^{-E_{i,k}/T_i}$.
- **Temperature as thermal energy**: In statistical mechanics, higher temperature flattens the Boltzmann distribution, allowing the system to explore higher-energy states. Similarly, higher $T_i$ flattens the predictive distribution, reducing confidence.
- **Entropy as disorder**: Higher predictive entropy corresponds to higher thermodynamic entropy (more disorder). The temperature adjustment $T_i \propto H(p_i)$ increases temperature for high-entropy (high-uncertainty) predictions.
- **Margin as energy gap**: A large margin $m_i$ indicates a clear preference for one class (analogous to a large energy gap between ground and excited states). Small margin $\rightarrow$ low energy gap $\rightarrow$ higher temperature.

## 3.3 Hyperparameter Tuning

The hyperparameters $T_0$, $\alpha$, and $\beta$ are tuned on a validation set to minimize Expected Calibration Error (ECE):

$$\mathcal{L}(T_0, \alpha, \beta) = \text{ECE}(\tilde{p}_i, y_i)$$

where $y_i$ is the true label for validation sample $i$. We use ECE (rather than NLL) as the tuning objective because the goal is calibration, not likelihood.

In our implementation, we use grid search over an expanded space:
- $T_0 \in \{0.5, 1.0, 2.0, 4.0, 6.0, 8.0\}$
- $\alpha \in \{0.0, 0.25, 0.5, 0.75, 1.0\}$
- $\beta \in \{0.0, 0.25, 0.5\}$

The expanded search space for $T_0$ (up to 8.0) reflects that optimal temperatures for temperature scaling can exceed 4.0, and TEC's base temperature should span a similar range.

## 3.4 Baseline Methods

We compare TEC against two baselines:

1. **Uncalibrated**: Direct softmax probabilities from logits without any temperature adjustment.
2. **Temperature Scaling** [1]: Global temperature scaling with a single parameter $T$ optimized on the validation set to minimize ECE.

# Experiments

## 4.1 Experimental Setup

**Datasets.** We evaluate on five text classification datasets spanning binary and multi-class settings [ARTIFACT:art_SSmr6ZrIe2PQ]:

| Dataset | Classes | Task | Train | Val | Test |
|---------|---------|------|-------|-----|------|
| SST-2 | 2 | Sentiment classification | 600 | 200 | 200 |
| QNLI | 2 | Natural language inference | 600 | 200 | 200 |
| AG News | 4 | Topic classification | 600 | 200 | 200 |
| MNLI | 3 | Textual entailment | 600 | 200 | 200 |
| DBpedia | 14 | Ontology classification | 600 | 200 | 200 |

All datasets are standardized to 600 train / 200 validation / 200 test examples with stratified sampling to preserve class distribution.

**Embeddings.** We use pre-trained DistilBERT (from HuggingFace Transformers) to generate embeddings for each text input, followed by a linear classification layer trained on the training set. Logits from this classifier are used as input to the calibration methods. This ensures evaluation on **real LLM embeddings** rather than synthetic data, addressing a key limitation identified in the previous version of this work.

**Evaluation Metrics.** We report:
- **Expected Calibration Error (ECE)** [1]: Lower is better (0 = perfectly calibrated).
- **Brier Score** [15]: Lower is better (0 = perfect predictions).
- **Negative Log-Likelihood (NLL)**: Lower is better.
- **Accuracy**: Percentage of correct predictions.

**Statistical significance.** For SST-2, we compute 95% bootstrap confidence intervals (1000 iterations) and perform paired Wilcoxon signed-rank tests to compare methods [ARTIFACT:art_PHvp8viBEPFq]. Results show that while calibration improves over uncalibrated baseline, the improvement may not reach statistical significance with n=200 test samples (p-value > 0.05). This highlights the need for larger-scale evaluation in future work.

## 4.2 Main Results

Table 1 presents the main results comparing uncalibrated baseline, temperature scaling, and Thermodynamic Entropy Calibration (TEC) across five datasets.

**Table 1: Calibration performance on five text classification datasets using pre-trained transformer embeddings.** Values are ECE (lower is better). Full results including Brier score, NLL, and accuracy are in Appendix A. Bold indicates best (lowest) ECE per dataset.

| Dataset | Uncalibrated | Temperature Scaling | TEC | Winner |
|---------|---------------|---------------------|-----|--------|
| SST-2 | 0.0078 | **0.0042** | 0.0071 | TS |
| QNLI | 0.1364 | 0.0076 | **0.0042** | TEC |
| AG News | 0.0625 | **0.0029** | 0.0146 | TS |
| MNLI | 0.6337 | **0.1686** | 0.2293 | TS |
| DBpedia | 0.0531 | 0.0088 | **0.0075** | TEC |

**Key findings:**

1. **Both calibration methods significantly improve over uncalibrated baseline.** Across all five datasets, temperature scaling reduces ECE by 45-95% compared to uncalibrated predictions. TEC also provides substantial improvements (27-97% ECE reduction), confirming that calibration adjustments are beneficial.

2. **TEC outperforms temperature scaling on 2/5 datasets.** On QNLI (ECE=0.0042 for TEC vs. 0.0076 for TS, a 45% relative improvement) and DBpedia (ECE=0.0075 for TEC vs. 0.0088 for TS, a 15% relative improvement), TEC achieves better calibration. These datasets represent interesting cases: QNLI requires reasoning about textual entailment (inherently ambiguous in some cases), and DBpedia has 14 classes (many more opportunities for class-conditional miscalibration).

3. **Temperature scaling outperforms TEC on 3/5 datasets.** On SST-2, AG News, and MNLI, temperature scaling achieves lower ECE. The gap is largest on MNLI (ECE=0.1686 for TS vs. 0.2293 for TEC), suggesting that TEC's per-sample adjustment may be harmful when the optimal temperature is similar across samples.

4. **All methods maintain accuracy.** Classification accuracy is identical across calibration methods within each dataset (see Appendix A), confirming that calibration adjustments do not degrade predictive performance.

[FIGURE:fig2]

## 4.3 When Does TEC Provide Benefits?

To understand the conditions under which TEC outperforms temperature scaling, we analyze the dataset characteristics and perform additional experiments.

**Heterogeneous miscalibration hypothesis.** TEC adjusts temperature per-sample based on entropy and margin. This should be beneficial when miscalibration is **heterogeneous** across samples: some examples are well-calibrated (easy examples), while others are highly overconfident (ambiguous examples). Global temperature scaling applies the same adjustment to all samples, which may over-correct easy examples while under-correcting hard ones.

To test this hypothesis, we split each test set into "easy" and "hard" subsets based on the decision margin $m_i$ (top-1 probability minus top-2 probability). Samples with margin above the median are classified as "easy" (model is confident), and samples with margin below the median are "hard" (model is uncertain).

Figure 3 shows ECE decomposition by easy/hard splits. On QNLI and DBpedia (where TEC wins), the hard subset has substantially higher ECE than the easy subset, confirming heterogeneous miscalibration. TEC's per-sample adjustment specifically benefits the hard subset by assigning higher temperatures to uncertain predictions.

**Multi-class effect.** DBpedia has 14 classes, the most of any dataset evaluated. On this dataset, TEC outperforms TS (ECE=0.0075 vs. 0.0088). Dirichlet calibration [5] similarly targets multi-class settings where class-conditional miscalibration exists. The per-sample temperature in TEC implicitly captures class-conditional effects: if the model is systematically overconfident on certain classes, those classes will have lower margins on average, triggering higher temperatures.

**When TEC does not help.** On AG News (4 classes) and MNLI (3 classes), temperature scaling outperforms TEC. This suggests that simply having multiple classes is not sufficient for TEC to provide benefits; the miscalibration must be **heterogeneous across samples**, not just across classes. On AG News, the miscalibration appears to be relatively uniform, making global temperature scaling adequate.

[FIGURE:fig3]

## 4.4 Reliability Diagrams

Reliability diagrams visually assess calibration by plotting accuracy vs. confidence in bins. A perfectly calibrated model falls on the diagonal line.

[FIGURE:fig4]

Figure 4 shows reliability diagrams for temperature scaling and TEC on QNLI (where TEC wins) and SST-2 (where TS wins). On QNLI, TEC's reliability curve is closer to the diagonal across all confidence bins, indicating better calibration. On SST-2, both methods produce well-calibrated predictions (close to diagonal), but TS is slightly better in the high-confidence bins.

## 4.5 Inference-Time Temperature Annealing

As an additional direction, we explore whether **annealing** the temperature during inference (rather than post-hoc calibration on fixed logits) can improve calibration. Drawing on simulated annealing [14], we implement an annealing schedule:

$$T(t) = T_{init} \cdot \left(\frac{T_{final}}{T_{init}}\right)^{t/T_{total}}$$

where $t$ is the token position during generation. Our initial implementation on SST-2, AG News, and DBpedia (using simulated logits) shows mixed results: annealing helps SST-2 (ECE=0.2400 vs. 0.2985 uncalibrated) but does not outperform post-hoc temperature scaling [ARTIFACT:art_5XrEi0TPtFOf]. More importantly, the current annealing implementation does not yet use real LLM generation, representing a limitation for future work.

# Discussion

## 5.1 Interpretation of Results

Our evaluation on five datasets with real pre-trained transformer embeddings reveals a **nuanced picture** of when physics-inspired per-sample calibration helps. The key insight is that TEC provides benefits in **specific scenarios** rather than universally:

1. **Heterogeneous miscalibration** (QNLI): When some examples are easy and others are hard, per-sample temperature adjustment outperforms global scaling.
2. **Multi-class settings with class-conditional effects** (DBpedia, 14 classes): With many classes, class-conditional miscalibration patterns emerge. TEC's per-sample temperatures implicitly adapt to these patterns.
3. **Simple binary classification** (SST-2): When miscalibration is relatively uniform across samples, global temperature scaling is sufficient and TEC provides no additional benefit.

These findings suggest that the choice between TEC and TS should be informed by the dataset characteristics. Practitioners can diagnose heterogeneous miscalibration by examining the ECE decomposition across easy/hard splits (as in Figure 3).

## 5.2 Comparison to Adaptive Temperature Scaling

A natural question is how TEC compares to Adaptive Temperature Scaling (ATS) [7], which also predicts per-sample temperatures. ATS uses a learned neural network, while TEC uses a physics-inspired heuristic. We acknowledge that a learned approach may outperform our heuristic on many datasets. However, TEC offers two advantages:

1. **Interpretability**: The TEC formula $T_i = T_0 \cdot (1 + \alpha H(p_i) + \beta(1-m_i))$ is directly interpretable. Practitioners can examine the per-sample temperatures and understand which factor (entropy or margin) drove the adjustment. ATS uses a black-box neural network.
2. **No additional parameters beyond calibration hyperparameters**: TEC tunes $T_0, \alpha, \beta$ on a validation set. ATS requires training a neural network for temperature prediction, which may overfit on small validation sets.

A direct comparison to ATS on the same datasets remains future work. We view TEC as complementary to learned approaches: the physics-inspired heuristic could be used as a **feature** in a learned calibration model, combining interpretability with expressive power.

## 5.3 Theoretical Implications

The mathematical equivalence between softmax distributions and Boltzmann distributions suggests deeper connections between machine learning and statistical mechanics. Our work takes a step toward operationalizing this connection for practical benefit (calibration), but several theoretical questions remain:

1. **Is Shannon entropy the correct analog for thermodynamic entropy in classification?** While the mathematical forms are identical, thermodynamic entropy satisfies the Second Law of Thermodynamics (it never decreases in a closed system), whereas Shannon entropy does not have this property [13]. The physical interpretation of "temperature" in softmax distributions should be interpreted as a mathematical analogy rather than a claim of physical identity.
2. **What is the optimal functional form for per-sample temperature?** Our formulation $T_i = T_0 \cdot (1 + \alpha H(p_i) + \beta(1-m_i))$ is motivated by physical intuition but not derived from first principles. Alternative formulations may prove more effective, and the optimal form may be dataset-dependent.
3. **Can inference-time temperature annealing improve calibration?** Our current method applies post-hoc calibration to fixed logits. An intriguing direction is to anneal temperature during sequence generation, drawing on simulated annealing concepts. This requires integrating calibration objectives into the decoding process and remains future work.

## 5.4 Limitations

**Evaluation on moderate-sized datasets.** Our experiments use 600 training examples per dataset. While this is sufficient for calibration evaluation (following Guo et al. [1]), larger-scale evaluation would strengthen the findings. Additionally, statistical significance tests show that improvements may not be significant with limited sample size [ARTIFACT:art_PHvp8viBEPFq].

**Modest improvement over baseline.** On datasets where TEC outperforms TS, the improvement is modest (e.g., QNLI: 45% relative ECE reduction; DBpedia: 15% relative ECE reduction). While meaningful, these improvements may not justify the additional complexity of per-sample temperature computation in production systems.

**Hyperparameter sensitivity.** TEC introduces two additional hyperparameters ($\alpha$ and $\beta$) beyond the base temperature $T_0$. This increases the risk of overfitting on small validation sets. Future work should explore more robust hyperparameter estimation techniques.

**Classification only.** Our evaluation focuses on classification tasks. The method should also be evaluated on **generative** LLM tasks, where entropy-based approaches like semantic entropy [2] have shown promise.

# Conclusion

This paper introduced Thermodynamic Entropy Calibration (TEC), a physics-inspired post-hoc calibration method that adjusts per-sample temperature based on predictive entropy and decision margin. By drawing on the mathematical equivalence between softmax distributions and Boltzmann distributions, TEC provides an interpretable approach to confidence calibration.

Our evaluation on five text classification datasets with real pre-trained transformer embeddings shows a **nuanced picture**: TEC outperforms standard temperature scaling on datasets with heterogeneous miscalibration (QNLI, DBpedia), while temperature scaling remains superior on simpler tasks (SST-2, AG News, MNLI). Both methods significantly improve calibration over uncalibrated baselines. These findings suggest that **per-sample temperature adjustment is most beneficial when miscalibration patterns vary across samples**—a condition that global temperature scaling cannot address.

The primary contribution of this work is not the empirical results alone, but the introduction of a **physics-inspired framework** for thinking about calibration. By connecting predictive uncertainty to thermodynamic entropy, we open new avenues for developing calibration methods grounded in statistical mechanics principles. The interpretability of TEC's formula—practitioners can examine how entropy and margin influence each prediction's temperature—is a valuable property for building trustworthy AI systems.

Future work should focus on: (1) evaluating TEC on larger datasets and generative LLM tasks, (2) developing inference-time temperature annealing schedules that adapt dynamically during generation, (3) combining TEC with semantic entropy [2] for improved uncertainty quantification, and (4) conducting a direct comparison to Adaptive Temperature Scaling [7] to better understand the trade-offs between learned and heuristic temperature adjustment.

As LLMs see increasing deployment in high-stakes applications, well-calibrated confidence estimates are essential. Physics-inspired calibration methods like TEC represent a promising direction—not as a universal replacement for temperature scaling, but as a complementary tool for scenarios where per-sample calibration adjustment provides benefits.

# Acknowledgments

We thank the anonymous reviewers for their thoughtful feedback, which significantly improved this paper.

# References

[1] Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning (ICML)*.

[2] Kuhn, L., Gal, Y., and Farquhar, S. (2023). Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation. In *Proceedings of the 11th International Conference on Learning Representations (ICLR)*.

[3] Physics Stack Exchange (2023). Softmax function - relation to statistical mechanics. https://physics.stackexchange.com/questions/669314/softmax-function-relation-to-stat-mech

[4] Yang, A., et al. (2024). Let it calm: Exploratory annealed decoding for verifiable reinforcement learning. https://yangalan123.github.io/ead_rlvr/

[5] Kull, M., Perello-Nieto, M., Kangsepp, M., Silva Filho, T., Song, H., and Flach, P. (2019). Beyond temperature scaling: Obtaining well-calibrated multi-class probabilities with Dirichlet calibration. *Advances in Neural Information Processing Systems (NeurIPS)*, 32.

[6] Tomani, C., Gruber, S., Erdem, M. E., Cremers, D., and Buettner, F. (2021). Parameterized temperature scaling for boosting the expressive power of convolutional neural network architectures. *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)*.

[7] Joy, T., Pinto, F., Lim, S. N., Torr, P. H., and Dokania, P. K. (2023). Sample-dependent adaptive temperature scaling for improved calibration. In *Proceedings of the AAAI Conference on Artificial Intelligence*, 37(12).

[8] Xie, H., Qing, Y., Huang, Y., and Xiao, Y. (2024). Calibrating language models with adaptive temperature scaling. *arXiv preprint arXiv:2409.19817*.

[9] Tian, K., Mitchell, E., Zhou, A., Sharma, A., Rafailov, R., Yao, H., and Finn, C. (2023). Just ask for calibration: Strategies for eliciting calibrated confidence estimates from language models. *arXiv preprint arXiv:2305.14975*.

[10] Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379-423.

[11] Gal, Y. and Ghahramani, Z. (2016). Dropout as a Bayesian approximation: Representing model uncertainty in deep learning. In *Proceedings of the 33rd International Conference on Machine Learning (ICML)*.

[12] Towards AI (2023). The softmax function every transformer uses is the Boltzmann distribution, not inspired by it. https://pub.towardsai.net/the-softmax-function-every-transformer-uses-is-the-boltzmann-distribution-not-inspired-by-it-not-080fb2036918

[13] Jaynes, E. T. (1957). Information theory and statistical mechanics. *Physical Review*, 106(4), 620-630.

[14] Kirkpatrick, S., Gelatt, C. D., and Vecchi, M. P. (1983). Optimization by simulated annealing. *Science*, 220(4598), 671-680.

[15] Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1-3.

[16] Joshi, M., Choi, E., Weld, D. S., and Zettlemoyer, L. (2017). TriviaQA: A large scale distantly supervised challenge dataset for reading comprehension. In *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL)*.

[17] Wang, A., Singh, A., Michael, J., Hill, F., Levy, O., and Bowman, S. (2018). GLUE: A multi-task benchmark and analysis platform for natural language understanding. *arXiv preprint arXiv:1804.07461*.

[18] Lin, S., Hilton, J., and Evans, O. (2021). TruthfulQA: Measuring how models mimic human falsehoods. *arXiv preprint arXiv:2109.07914*.

# Appendix A: Full Results

**Table A1: Full calibration results on five datasets.** Accuracy is identical across methods within each dataset (calibration does not change predictions). Results from [ARTIFACT:art_xdUSFFTTrRuY].

| Dataset | Method | ECE | Brier Score | NLL | Accuracy |
|---------|--------|-----|-------------|-----|----------|
| SST-2 | Uncalibrated | 0.0078 | 0.0150 | 0.0361 | 0.9917 |
|  | Temperature Scaling | **0.0042** | **0.0150** | **0.0337** | 0.9917 |
|  | TEC | 0.0071 | 0.0152 | 0.0349 | 0.9917 |
| QNLI | Uncalibrated | 0.1364 | 0.5306 | 0.7254 | 0.5183 |
|  | Temperature Scaling | 0.0076 | 0.4986 | 0.6917 | 0.5183 |
|  | TEC | **0.0042** | **0.4985** | **0.6917** | 0.5183 |
| AG News | Uncalibrated | 0.0625 | 0.7677 | 1.4248 | 0.2600 |
|  | Temperature Scaling | **0.0029** | **0.7506** | **1.3876** | 0.2600 |
|  | TEC | 0.0146 | 0.7532 | 1.3930 | 0.2600 |
| MNLI | Uncalibrated | 0.6337 | 1.3255 | 3.7380 | 0.2650 |
|  | Temperature Scaling | **0.1686** | **0.7325** | **1.2015** | 0.2650 |
|  | TEC | 0.2293 | 0.7912 | 1.2979 | 0.2650 |
| DBpedia | Uncalibrated | 0.0531 | 0.9353 | 2.6809 | 0.0667 |
|  | Temperature Scaling | 0.0088 | 0.9286 | 2.6391 | 0.0667 |
|  | TEC | **0.0075** | **0.9286** | **2.6390** | 0.0667 |

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (novelty) The paper claims TEC is novel because it uses 'physics-inspired principles' rather than 'learning temperature adjustments from data alone' (Section 2.1, Differentation from prior work). However, per-sample temperature scaling has already been proposed in multiple prior works: (1) Joy et al. (AAAI 2023) 'Sample-Dependent Adaptive Temperature Scaling' predicts per-sample temperatures using a VAE-based module. (2) Tomani et al. (WACV 2021) 'Parameterized Temperature Scaling' uses a neural network to predict sample-specific temperatures. (3) Xie et al. (arXiv 2024) 'Calibrating Language Models with Adaptive Temperature Scaling' extends ATS to LLMs. The paper acknowledges these works but claims the difference is that TEC is 'interpretable' and 'physics-inspired' rather than a 'learned black-box function.' This is a valid but MODEST differentiation - the core idea (per-sample temperature) already exists, and TEC's formula is essentially a 2-feature linear model (using entropy and margin as features), which is less expressive than a learned neural network.
  Action: To strengthen the novelty claim: (1) Provide a direct comparison to Adaptive Temperature Scaling (Joy et al. 2023) on the same datasets. Does the physics-inspired heuristic outperform the learned approach? If not, clearly frame TEC as a computationally cheaper/interpretable alternative rather than a more effective method. (2) Ablate the contribution of the physics framing: Is TEC better than simply using entropy + margin as features in a small neural network (as in PTS)? (3) If the key novelty is the thermodynamic connection, then derive the TEC formula from first principles in statistical mechanics rather than presenting it as a heuristic motivated by physics. The current Section 3.2 explains analogies but doesn't derive the formula.
- [MAJOR] (methodology) There is a significant inconsistency between the TEC formula presented in the paper and the actual code implementation. Paper Section 3.1 states: T_i = T_0 * (1 + alpha * H(p_i) + beta * (1 - m_i)). However, the code (method.py line 222) implements: T_i = T0 * (1 + alpha * H_norm_val - beta * M_val). These give different behaviors: (1) The paper's formula uses raw entropy H(p_i), while the code uses normalized entropy H_norm = H / log(n_classes). (2) The paper's formula has '+ beta * (1 - m_i)' which simplifies to '+ beta - beta * m_i', while the code has '- beta * M_val'. The code's formulation allows temperature to go BELOW T0 (when beta > 0 and margin > 0), while the paper's formulation ensures T_i >= T_0 (when alpha, beta >= 0). (3) The hyperparameter search spaces also differ: Paper Section 3.3 says T0 in {0.5, 1.0, 2.0, 4.0, 6.0, 8.0}, but code uses [0.5, 1.0, 2.0, 5.0].
  Action: Fix the inconsistency between paper and code: (1) Either update the paper's formula to match the code: T_i = T0 * (1 + alpha * H_norm - beta * M), or update the code to match the paper: T_i = T_0 * (1 + alpha * H + beta * (1-m)). (2) Clearly specify whether entropy is normalized and how margin affects temperature. (3) Report the actual hyperparameter search space used in experiments, not the expanded space mentioned in the paper. (4) Ensure the results in the paper are reproducible from the paper description alone - currently they are not due to this inconsistency.
- [MAJOR] (methodology) The experimental comparison between TS and TEC is compromised by using different tuning objectives. The paper states (Section 3.3): 'The hyperparameters T_0, alpha, and beta are tuned on a validation set to minimize Expected Calibration Error (ECE).' And Section 3.4 describes TS as: 'Global temperature scaling with a single parameter T optimized on the validation set to minimize ECE.' However, in the code, the `calibrate_ts` function (lines 195-206) uses Negative Log-Likelihood (NLL) as the tuning objective, not ECE. This means TS is tuned with NLL but TEC is tuned with ECE - an unfair comparison. Guo et al. (2017) originally proposed tuning TS with NLL, and that is the standard approach. If the paper wants to tune TEC with ECE, it should also tune TS with ECE for a fair comparison.
  Action: Use the same tuning objective for both TS and TEC: (1) Option A: Tune both with NLL (standard approach from Guo et al. 2017). (2) Option B: Tune both with ECE (as the paper claims but the code doesn't implement for TS). Whichever option, clearly state the tuning objective in the paper and ensure the code matches. (3) Consider reporting results with both tuning objectives to show robustness. (4) Justify why ECE is used for TEC instead of NLL - the paper says 'the goal is calibration, not likelihood' but NLL is also a calibration metric (it measures probabilistic quality).
- [MAJOR] (evidence) The empirical results show TEC outperforms TS on only 2/5 datasets (QNLI, DBpedia), while TS outperforms TEC on the other 3 datasets. On MNLI, TS achieves ECE=0.1686 while TEC achieves ECE=0.2293 - a substantial gap. The paper honestly reports these mixed results, which is commendable, but it weakens the case for adopting TEC over TS. The improvements where TEC wins are also modest (45% relative ECE reduction on QNLI, 15% on DBpedia). For a new method to justify adoption, it should show consistent and substantial improvements over strong baselines.
  Action: Strengthen the empirical evaluation: (1) Evaluate on more datasets to show that TEC's benefits generalize. The current 5 datasets may not be representative. (2) Conduct a large-scale evaluation with more diverse tasks (e.g., NLI, QA, sentiment, topic classification) to identify when TEC helps. (3) Consider reframing the paper: If TEC doesn't consistently outperform TS, perhaps the contribution is the analysis of when per-sample calibration helps (heterogeneous miscalibration) and the diagnostic tools (ECE decomposition by easy/hard splits). This would be a valuable contribution even if the method itself is not always better. (4) Compare to other baselines beyond TS, such as Dirichlet calibration (Kull et al. 2019) for multi-class settings.
- [MINOR] (rigor) The evaluation uses small datasets (600 train / 200 val / 200 test per dataset). The paper acknowledges this limitation (Section 5.4: 'Our experiments use 600 training examples per dataset. While this is sufficient for calibration evaluation (following Guo et al. [1]), larger-scale evaluation would strengthen the findings.'). However, the paper also notes that statistical significance tests show improvements may not be significant with n=200 test samples (Section 4.1, referencing artifact art_PHvp8viBEPFq). This suggests the current results may not be reliable.
  Action: Increase the evaluation scale: (1) Use larger datasets or report results with 95% confidence intervals to show variance. (2) The paper mentions bootstrap CI but doesn't show them in Table 1 or Figure 2. Add confidence intervals to the main results. (3) Consider using pre-trained models that are already fine-tuned on the full training sets of GLUE datasets (e.g., use HuggingFace models fine-tuned on QNLI, MNLI) rather than training on 600 examples. This would give more realistic calibration estimates. (4) Report the variance across multiple random seeds/splits to show that results are consistent.
- [MINOR] (clarity) Section 4.5 ('Inference-Time Temperature Annealing') discusses a preliminary experiment on temperature annealing during inference. However, the implementation 'does not yet use real LLM generation' and 'represents a limitation for future work.' This section is distracting because it discusses a different setting (generation with temperature annealing) than the main paper (post-hoc calibration for classification). The results are also mixed (annealing helps SST-2 but not AG News). Including this preliminary result dilutes the main contribution.
  Action: Move the temperature annealing results to supplementary materials or a future work section. The main paper should focus on the core contribution (post-hoc TEC vs. TS comparison for classification). The temperature annealing direction is interesting but not yet mature enough for inclusion in the main paper. Alternatively, if the authors want to include it, they should: (1) Implement it with real LLM generation (not simulated logits), (2) Compare to post-hoc methods more directly, (3) Clearly frame it as a separate contribution from the main TEC method.
- [MINOR] (scope) The evaluation is limited to classification tasks. The paper mentions in Section 5.4 that 'the method should also be evaluated on generative LLM tasks, where entropy-based approaches like semantic entropy [2] have shown promise.' This is a valid limitation, but generative tasks are where LLM calibration is most critical (e.g., uncertainty in generated answers). Evaluating only on classification limits the impact.
  Action: Expand the evaluation to generative tasks: (1) Evaluate TEC on uncertainty estimation for generative LLMs using semantic entropy or other approaches. (2) Test whether per-sample temperature adjustment during decoding (rather than post-hoc) improves calibration for generation. (3) If generative evaluation is not feasible, clearly state this as a limitation and remove or downplay claims about 'high-stakes domains' (Introduction, first paragraph) which typically involve generative tasks (e.g., medical QA, legal reasoning).
</reviewer_feedback>



<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for the field's landscape, prior work, crowded lanes, and the novelty bar — consult it while revising so the updated hypothesis stays genuinely novel and well-positioned.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/upd_hypo/upd_hypo/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/upd_hypo/upd_hypo/.sdk_openhands_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-07-18 17:56:05 UTC

```
Better uncertainty calibration for LLM classifiers
```
