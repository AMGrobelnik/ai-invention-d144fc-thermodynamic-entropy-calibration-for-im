# gen_strat_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_strat`
> Run: `run_3fUR0i5e8NC7` — Thermodynamic Entropy Calibration for Improved Confidence Estimation in LLM Classifiers
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_strat_1` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-18 16:33:00 UTC

````
<hypothesis>
Your strategy should advance this hypothesis.

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
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for study design, proper baselines, and the evaluation/validity norms this field demands.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<iteration_status>
Current iteration: 2 of 2
Remaining (including this one): 1
</iteration_status>

<previous_strategies>
Strategies from the PREVIOUS iteration. You can CONTINUE these directions,
ADAPT based on what worked and what didn't in the artifacts produced, or PIVOT if results suggest a better path.

--- Strategy 1 ---
kind: strategy
id: gen_strat_1_idx1
title: Thermodynamic Entropy Calibration Foundation
objective: >-
  Establish the theoretical foundation and empirical baseline for calibrating LLM uncertainty using thermodynamic entropy
  principles, preparing datasets and initial method implementation for evaluation.
rationale: >-
  This is the first iteration with 2 total iterations. We need to (1) thoroughly understand existing calibration methods and
  thermodynamic entropy applications in ML, (2) acquire appropriate classification datasets for evaluation, and (3) implement
  the core thermodynamic entropy calibration method. These artifacts will run in parallel to maximize progress and set up
  iteration 2 for comprehensive evaluation and comparison.
artifact_directions:
- id: research_iter1_dir1
  type: research
  objective: >-
    Survey existing LLM calibration methods, temperature scaling variants, entropy-based uncertainty estimation, and applications
    of thermodynamic principles in machine learning to inform our method design.
  approach: >-
    Conduct comprehensive literature review covering: (1) Temperature scaling and variants (Guo et al. 2017 and follow-ups),
    (2) Entropy-based uncertainty estimation in neural networks and LLMs, (3) Thermodynamic entropy analogies in ML (free
    energy, Boltzmann distributions), (4) Temperature annealing schedules in optimization and inference, (5) Standard calibration
    metrics (ECE, Brier score) and benchmarks. Search for recent papers on LLM calibration, uncertainty quantification, and
    physics-inspired ML methods.
  depends_on: []
- id: dataset_iter1_dir2
  type: dataset
  objective: >-
    Collect and prepare text classification datasets suitable for evaluating LLM confidence calibration, ensuring diversity
    in domain and difficulty for robust evaluation.
  approach: >-
    Search HuggingFace Hub and academic benchmarks for: (1) Standard text classification datasets (SST-2, AG News, TREC, etc.),
    (2) Datasets with multiple classes to test calibration beyond binary, (3) Both easy and challenging classification tasks.
    Download 3-5 datasets, standardize to JSON format with fields for text, label, and metadata. Create train/validation/test
    splits suitable for calibration evaluation (validation set needed for temperature tuning). Generate full/mini/preview
    variants. Target total size under 300MB.
  depends_on: []
- id: experiment_iter1_dir3
  type: experiment
  objective: >-
    Implement the thermodynamic entropy calibration method and baseline calibration approaches, preparing for empirical evaluation
    in iteration 2.
  approach: >-
    Implement: (1) Baseline methods - uncalibrated softmax, standard temperature scaling, (2) Thermodynamic entropy calibration
    method with temperature annealing during inference - treat logit distributions as thermodynamic systems where temperature
    controls entropy, implement annealing schedule (linear, exponential, or physics-inspired cooling), (3) Compute calibration
    metrics (ECE, Brier score, negative log-likelihood), (4) Use small-scale initial tests to verify implementation correctness.
    Method should be modular to allow different annealing schedules and entropy formulations. Save implementation for reuse
    in iteration 2 with full datasets.
  depends_on: []
expected_outcome: >-
  After this iteration, we will have: (1) A comprehensive research report on calibration methods and thermodynamic entropy
  in ML, (2) 3-5 standardized classification datasets ready for experiments, and (3) Working implementations of baseline and
  thermodynamic entropy calibration methods. This foundation enables iteration 2 to focus on large-scale evaluation, hyperparameter
  tuning, statistical significance testing, and comparison against more baselines.
summary: >-
  Build foundation for thermodynamic entropy calibration by researching existing methods, collecting diverse classification
  datasets, and implementing the core calibration approach with baselines.
</previous_strategies>

<dependency_rules>
- depends_on is a list of objects {id, label} — each entry references an existing artifact and tags how it is being used
- "id" can ONLY reference IDs from <existing_artifacts> — never IDs you are proposing (all new artifacts run in parallel)
- "label" is a SHORT free-text type label (a word or two, NOT a sentence) describing what role the dep plays — e.g. "dataset", "validates", "extends", "supersedes". Required on every dep.
- Setting depends_on provides the dependency's out_dependency_files to your artifact at execution time
- If no suitable existing artifacts exist, use empty depends_on
- New artifact IDs are assigned by the system after submission — do not invent IDs for your proposed artifacts
</dependency_rules>

<available_artifact_types>
Artifact types you can plan. Use this to choose the right types for your strategy objectives.

<artifact_types>
RESEARCH
Web research to answer key questions — like a researcher making decisions.
Runtime: LLM Agent, no code execution.
Tools: the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text).
Capabilities: Find, synthesize, and compare information across sources; survey SOTA and best practices.
Deps: REQUIRED none | OPTIONAL other RESEARCH to build on prior findings

EXPERIMENT
Run code to test hypotheses, implement methods, and collect empirical results.
Runtime: Python 3.12, UV (any pip package), isolated workspace, gradual scaling (mini → full data).
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Implement and run any code-based experiment, compare method vs baselines.
Deps: REQUIRED at least one DATASET | OPTIONAL RESEARCH for methodology guidance

DATASET
Collect, prepare, and merge datasets for experiments and analysis.
Runtime: Python 3.12, UV, isolated workspace.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-hf-datasets (HuggingFace Hub — ML datasets, many UCI/OpenML/Kaggle mirrors), aii-owid-datasets (Our World in Data — global statistics), aii-json (schema validation). Also any Python source (sklearn.datasets, openml, direct URLs, APIs) — must verify within 300MB limit.
Capabilities: Search, acquire, transform, combine, and standardize data from any available source.
Deps: REQUIRED none | OPTIONAL RESEARCH for guidance on what data to collect

EVALUATION
Evaluate experiment results with metrics, statistical analysis, and validity checks.
Runtime: Python 3.12, UV (any evaluation library), isolated workspace, gradual scaling matching experiment.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-json (schema validation), aii-openrouter-llms (call any LLM — GPT, Gemini, Llama, etc.), domain-specific as needed.
Capabilities: Compute any quantitative metrics and statistical tests, analyze validity and robustness.
Deps: REQUIRED at least one EXPERIMENT | OPTIONAL DATASET if reference data needed

PROOF
Formally prove mathematical statements in Lean 4 with automated iteration.
Runtime: LLM agent with Lean 4 compiler feedback loop.
Tools: Full shell/Python/filesystem access, the aii-web-tools skill (web search, page fetch, regex grep over full page/PDF text), and other skills.
Skills: aii-lean (proof verification, Mathlib search, tactics: ring, linarith, nlinarith, omega, simp, etc.)
Capabilities: Formally verify properties and inequalities, iterative proof development, lemma decomposition.
Deps: REQUIRED none | OPTIONAL RESEARCH for mathematical background
</artifact_types>
</available_artifact_types>

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results

DATASET executor scope:
  Output: data_out.json with rows of {input, output, metadata_fold, ...} — raw data only, no derived computations
  DOES: Download/generate datasets, analyze candidates to pick the best ones, standardize to JSON schema (features, labels, folds, metadata), validate schema, split into full/mini/preview
  DOES NOT: Run experiments, train models, compute derived statistics (PID/MI/correlations/synergy matrices) as final output
  If you need to COMPUTE something from data (synergy matrices, MI scores, timing benchmarks), use an EXPERIMENT artifact instead

EVALUATION executor scope:
  Output: eval_out.json with evaluation results
  DOES: Any evaluation of experiment results — metrics, statistical tests, ablations, comparisons, visualizations, robustness checks, error analysis, etc.
  DOES NOT: Implement new methods (use EXPERIMENT), collect data (use DATASET)
  This is for analyzing experiment outputs from any angle

PROOF executor scope:
  Output: Lean 4 proof files (.lean) with verified theorems
  DOES: Write and verify Lean 4 formal proofs with Mathlib, iterative compilation
  DOES NOT: Run Python experiments, collect data, do empirical analysis
  Use only when formal mathematical guarantees are needed
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
DATASET:
- Plan for REAL third-party datasets (HuggingFace, Kaggle, direct-download URLs) — downloadable within time and size constraints
- Describe dataset criteria (domain, size, format) — executors find exact sources, but you can suggest candidates or search directions
- ALWAYS prefer real datasets over synthetic. Synthetic is a LAST RESORT only when no suitable real data exists
EVALUATION: Must depend on at least one EXPERIMENT. Focus on statistical rigor and validity checks.
PROOF: Use only when the hypothesis requires formal mathematical guarantees. Lean 4 + Mathlib.
</artifact_planning_rules>

<existing_artifacts>
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
out_dependency_files:
  file_list:
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
out_dependency_files:
  file_list:
  - data.py
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json
  data_file_paths:
  - full_data_out.json
  - mini_data_out.json
  - preview_data_out.json

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
out_dependency_files:
  file_list:
  - method.py
  - full_method_out.json
  - mini_method_out.json
  - preview_method_out.json
</existing_artifacts>

<current_paper>
The current paper draft — represents the research story so far.

Use this to understand what's working, what's not, and what gaps remain.
Gaps and weak results signal what to try differently — not what to conclude.

# Thermodynamic Entropy Calibration for Improved Confidence Estimation in LLM Classifiers

## 1 Introduction

Large Language Models (LLMs) have demonstrated remarkable capabilities across natural language understanding tasks, yet their deployment in high-stakes domains remains hindered by unreliable confidence estimates. A well-calibrated classifier should produce predicted probabilities that reflect true outcome frequencies: among all predictions made with 80% confidence, approximately 80% should be correct [1]. Modern neural networks, including LLMs, systematically violate this property, exhibiting overconfidence where predicted probabilities exceed actual accuracy [1].

This miscalibration is particularly problematic for applications in healthcare, law, and autonomous systems, where overconfident incorrect predictions can lead to consequential errors. While post-hoc calibration methods like temperature scaling [1] effectively reduce calibration error, they apply a global temperature adjustment that may not account for varying uncertainty across individual predictions. Recent work has explored input-dependent temperature adjustment [6, 7, 8], but these approaches lack a principled theoretical foundation connecting temperature to predictive uncertainty.

This paper explores whether treating predictive uncertainty as thermodynamic entropy—drawing on the mathematical equivalence between the softmax function and the Boltzmann distribution—can inspire new calibration approaches. The key insight is that temperature in softmax distributions plays an analogous role to thermodynamic temperature in statistical mechanics: it controls the entropy (dispersion) of the probability distribution over classes [3, 12].

### 1.1 Problem Statement

Given a classifier that produces logits $z_i$ for each class $i$, the standard approach applies a global temperature scaling:

$$p_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

where $T > 0$ is a scalar temperature parameter optimized on a validation set to minimize Expected Calibration Error (ECE) [1].

The limitation of this approach is that a single temperature $T$ must balance calibration across all predictions, regardless of each sample's intrinsic difficulty or ambiguity. Intuitively, easy examples (where the correct class is clear from the input) and ambiguous examples (where multiple interpretations are plausible) may benefit from different temperature adjustments.

### 1.2 Proposed Approach

We propose Thermodynamic Entropy Calibration (TEC), which computes per-sample temperatures based on two uncertainty indicators [ARTIFACT:art_Oc5BxFWZU7a3]:

1. **Predictive entropy** $H(p) = -\sum_i p_i \log p_i$: Higher entropy indicates greater uncertainty
2. **Decision margin** $m = p_{(1)} - p_{(2)}$: The difference between the top two predicted probabilities (higher margin = more confident)

The per-sample temperature is computed as:

$$T_i = T_0 \cdot (1 + \alpha \cdot H(p_i) + \beta \cdot (1 - m_i))$$

where $T_0$, $\alpha$, and $\beta$ are hyperparameters tuned on a validation set.

This formulation has a physical interpretation: samples with high entropy (analogous to high thermodynamic entropy) or low margin (analogous to low energy difference between states) receive higher temperatures, producing flatter, more conservative probability distributions.

[FIGURE:fig1]

### 1.3 Summary of Contributions

This paper makes the following contributions:

1. We introduce Thermodynamic Entropy Calibration (TEC), a physics-inspired post-hoc calibration method that adjusts per-sample temperature based on predictive entropy and decision margin.

2. We provide a comprehensive literature review establishing the mathematical connections between softmax distributions, Boltzmann distributions, and entropy measures in information theory and statistical mechanics.

3. We evaluate TEC against uncalibrated baselines and standard temperature scaling on synthetic miscalibrated data, finding that TEC provides meaningful calibration improvement (33.4% ECE reduction) while maintaining classification accuracy.

4. We discuss the theoretical implications of treating predictive uncertainty as thermodynamic entropy and outline limitations of the current approach that motivate future work on inference-time temperature annealing.

## 2 Related Work

### 2.1 Calibration Methods for Neural Networks

Temperature scaling, introduced by Guo et al. [1], is the simplest and most widely used post-hoc calibration method for modern neural networks. It optimizes a single scalar temperature parameter $T$ by minimizing Negative Log-Likelihood (NLL) on a validation set. Despite its simplicity, temperature scaling often outperforms more complex methods like vector scaling and matrix scaling [1].

Recent extensions have proposed more flexible calibration approaches:

- **Dirichlet calibration** [5] generalizes temperature scaling to natively handle multi-class settings using Dirichlet distributions, improving calibration especially when class-conditional miscalibration patterns exist.

- **Parameterized Temperature Scaling (PTS)** [6] computes prediction-specific temperatures using a small neural network, reducing calibration error by approximately 30% over standard temperature scaling on vision tasks.

- **Adaptive Temperature Scaling (ATS)** [7, 8] predicts temperature scaling parameters for each input (or each token in language models), addressing the limitation that a global temperature cannot account for varying calibration needs across inputs.

Our method differs from these approaches in its use of physics-inspired principles: rather than learning temperature adjustments from data alone, we derive the functional form of per-sample temperature from the thermodynamic analogy between predictive distributions and Boltzmann distributions.

### 2.2 Entropy-Based Uncertainty Estimation

Entropy is a fundamental measure of uncertainty in probability distributions. In Bayesian neural networks, the entropy of the predictive distribution quantifies total uncertainty (sum of aleatoric and epistemic uncertainty) [11].

For LLMs, recent work has adapted entropy-based uncertainty estimation to the generative setting:

- **Predictive entropy** [2] computes $PE(x) = H(Y|x) = -\int p(y|x) \ln p(y|x) dy$ over multiple generated samples, measuring uncertainty in generated outputs.

- **Semantic entropy** [2] addresses the observation that LLMs can generate semantically equivalent but lexically different responses. By clustering semantically equivalent samples and computing entropy over meaning clusters rather than individual tokens, semantic entropy provides better uncertainty estimates than token-level entropy.

- **Length-normalized entropy** [2] normalizes log-probabilities by sequence length to address the issue that longer generations accumulate more uncertainty.

Our approach uses predictive entropy (computed from the classifier's output distribution rather than generated samples) as one component of per-sample temperature adjustment, connecting entropy-based uncertainty to the thermodynamic interpretation of temperature.

### 2.3 Thermodynamic Principles in Machine Learning

The connection between information theory and statistical mechanics has been recognized since the work of Jaynes [13]. The key mathematical equivalences are:

1. **Boltzmann distribution = Softmax**: The Boltzmann distribution from statistical mechanics, $p_i = \frac{1}{Z} e^{-\beta E_i}$ where $\beta = 1/T$, is mathematically identical to the softmax function with logits $z_i = -E_i$ (negative energies) [3, 12].

2. **Gibbs entropy = Shannon entropy**: The Gibbs entropy formula $S = -k_B \sum_i p_i \ln p_i$ has the same mathematical form as Shannon entropy $H = -\sum_i p_i \log p_i$, differing only in physical units ($k_B$ is Boltzmann's constant) [13].

These equivalences suggest that techniques from statistical mechanics might inform machine learning practice. For example, simulated annealing [14] uses a temperature schedule to escape local optima in optimization problems—a concept that could be adapted to temperature scheduling during LLM inference.

However, existing work using temperature schedules in LLMs focuses on reinforcement learning exploration (e.g., Exploratory Annealed Decoding [4]) rather than calibration. To our knowledge, no prior work combines temperature scaling with temperature annealing during inference for improved calibration, representing the novelty of our approach [ARTIFACT:art_EQYpVcsEAvw1].

### 2.4 Calibration Metrics and Benchmarks

The standard metric for classification calibration is Expected Calibration Error (ECE) [1], which partitions predictions into $M$ bins based on confidence and computes the weighted average of calibration gaps:

$$ECE = \sum_{m=1}^M \frac{|B_m|}{n} |acc(B_m) - conf(B_m)|$$

where $B_m$ is the set of predictions in bin $m$, and $acc(B_m)$ and $conf(B_m)$ are the accuracy and average confidence in that bin.

Other metrics include:

- **Brier Score** [15]: Mean squared difference between predicted probabilities and one-hot encoded true labels, ranging from 0 (perfect) to 1 (worst).

- **Negative Log-Likelihood (NLL)**: Measures the average log-probability assigned to the true class, with lower values indicating better calibration.

- **Maximum Calibration Error (MCE)** [1]: The worst-case calibration gap across bins, focusing on the largest miscalibration.

Benchmarks for evaluating LLM calibration include TriviaQA and CoQA (used in semantic uncertainty work [2]), GLUE and SuperGLUE [17] (general language understanding), and TruthfulQA [18] (measuring truthfulness).

## 3 Methods

### 3.1 Thermodynamic Entropy Calibration

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

This formulation ensures that samples with high entropy (uncertain predictions) or low margin (close competition between top classes) receive higher temperatures, producing flatter, more conservative probability distributions.

**Step 3: Apply temperature adjustment.**

$$\tilde{p}_i = \text{softmax}(z_i / T_i) \quad \text{(calibrated probabilities)}$$

[FIGURE:fig2]

### 3.2 Physical Interpretation

The method draws on the following physical analogies:

- **Logits as negative energies**: Setting $E_{i,k} = -z_{i,k}$ (negative logit for class $k$) makes the softmax distribution identical to the Boltzmann distribution $p_{i,k} \propto e^{-E_{i,k}/T_i}$.

- **Temperature as thermal energy**: In statistical mechanics, higher temperature flattens the Boltzmann distribution, allowing the system to explore higher-energy states. Similarly, higher $T_i$ flattens the predictive distribution, reducing confidence.

- **Entropy as disorder**: Higher predictive entropy corresponds to higher thermodynamic entropy (more disorder). The temperature adjustment $T_i \propto H(p_i)$ increases temperature for high-entropy (high-uncertainty) predictions.

- **Margin as energy gap**: A large margin $m_i$ indicates a clear preference for one class (analogous to a large energy gap between ground and excited states). Small margin $\rightarrow$ low energy gap $\rightarrow$ higher temperature.

### 3.3 Hyperparameter Tuning

The hyperparameters $T_0$, $\alpha$, and $\beta$ are tuned on a validation set to minimize Negative Log-Likelihood (NLL):

$$\mathcal{L}(T_0, \alpha, \beta) = -\frac{1}{n_{val}} \sum_{i=1}^{n_{val}} \log \tilde{p}_{i, y_i}$$

where $y_i$ is the true label for validation sample $i$.

In our implementation, we use grid search over:
- $T_0 \in \{0.5, 0.75, 1.0, 1.25, 1.5, 2.0\}$
- $\alpha \in \{0.0, 0.25, 0.5, 0.75, 1.0\}$
- $\beta \in \{0.0, 0.25, 0.5\}$

### 3.4 Baseline Methods

We compare TEC against two baselines:

1. **Uncalibrated**: Direct softmax probabilities from logits without any temperature adjustment.

2. **Temperature Scaling** [1]: Global temperature scaling with a single parameter $T$ optimized on the validation set:

$$p_i^{(TS)} = \text{softmax}(z_i / T_{opt})$$

where $T_{opt} = \arg\min_T \text{NLL}(T)$ on the validation set.

## 4 Experiments

### 4.1 Experimental Setup

**Dataset.** We use synthetic miscalibrated data mimicking the SST-2 sentiment classification dataset [17]. The synthetic data consists of 872 samples with 2 classes (negative/positive sentiment). We intentionally introduce miscalibration by generating overconfident predictions: the model is more confident than its actual accuracy warrants [ARTIFACT:art_Oc5BxFWZU7a3].

The data is split into train (60%, 523 samples), validation (20%, 174 samples), and test (20%, 175 samples) sets.

**Evaluation Metrics.** We report:
- **Expected Calibration Error (ECE)** [1]: Lower is better (0 = perfectly calibrated).
- **Brier Score** [15]: Lower is better (0 = perfect predictions).
- **Negative Log-Likelihood (NLL)**: Lower is better.
- **Accuracy**: Percentage of correct predictions.

**Implementation.** Our method is implemented in Python using NumPy for numerical computation. We use SciPy's `minimize_scalar` for optimizing the global temperature in temperature scaling. Reliability diagrams are generated using Matplotlib [ARTIFACT:art_Oc5BxFWZU7a3].

### 4.2 Main Results

Table 1 presents the main results comparing uncalibrated baseline, temperature scaling, and Thermodynamic Entropy Calibration (TEC).

| Method | ECE | Brier Score | NLL | Accuracy |
|--------|-----|-------------|-----|----------|
| Uncalibrated | 0.243 | 0.247 | 1.250 | 74.9% |
| Temperature Scaling | **0.031** | **0.188** | **0.563** | 74.9% |
| Thermodynamic Entropy | 0.162 | 0.215 | 0.685 | 74.9% |

Table 1: Calibration performance on synthetic miscalibrated SST-2 data. Temperature Scaling achieves the best calibration (lowest ECE, Brier, NLL). TEC provides meaningful improvement over uncalibrated baseline (33.4% ECE reduction) while maintaining accuracy.

**Key findings:**

1. **Temperature scaling is highly effective** for this dataset, reducing ECE from 0.243 to 0.031 (87.1% reduction). The optimal global temperature is $T_{opt} = 4.53$, indicating that the uncalibrated model is significantly overconfident.

2. **TEC provides moderate improvement** over uncalibrated baseline, reducing ECE from 0.243 to 0.162 (33.4% reduction). The optimal hyperparameters are $T_0 = 2.0$, $\alpha = 1.0$, $\beta = 0.3$.

3. **All methods maintain accuracy.** The classification accuracy (74.9%) is identical across methods, confirming that calibration adjustments do not degrade predictive performance.

[FIGURE:fig3]

### 4.3 Reliability Diagrams

Reliability diagrams visually assess calibration by plotting accuracy vs. confidence in bins. A perfectly calibrated model falls on the diagonal line.

Figure 2 shows reliability diagrams for the three methods. The uncalibrated model (Figure 2a) exhibits substantial overconfidence: predictions in the 0.9-1.0 confidence bin have only ~75% accuracy. Temperature scaling (Figure 2b) produces near-perfect calibration, with all bins close to the diagonal. TEC (Figure 2c) reduces overconfidence but does not achieve the same level of calibration as temperature scaling.

[FIGURE:fig4]

### 4.4 Analysis

**Why does temperature scaling outperform TEC on this dataset?**

The superior performance of temperature scaling suggests that the miscalibration in this dataset is relatively uniform across samples: a global temperature adjustment adequately corrects the overconfidence. TEC's per-sample temperature adjustment may be unnecessary when all predictions are similarly miscalibrated.

Additionally, the synthetic dataset may not fully capture the diverse uncertainty patterns present in real LLM predictions. In practice, some examples are genuinely ambiguous (e.g., sentiment classification for reviews with mixed opinions), while others are clear-cut. TEC is designed to handle this heterogeneity, but the benefit may not manifest when miscalibration is uniform.

**When might TEC provide greater benefit?**

We hypothesize that TEC will outperform temperature scaling in scenarios with heterogeneous miscalibration:
- Datasets with varying difficulty (easy and hard examples)
- Multi-class settings where some classes are inherently more confusable
- Out-of-distribution detection where confidence should be well-calibrated

Future work should evaluate TEC on real LLM embeddings and diverse datasets to test this hypothesis.

**Interpretability of the physics analogy.**

While TEC's performance is currently modest compared to temperature scaling, the method offers interpretability through its physics analogy. Practitioners can examine the per-sample temperatures $T_i$ and understand how entropy and margin influence calibration. This interpretability may be valuable for debugging and building trust in high-stakes applications.

## 5 Discussion

### 5.1 Theoretical Implications

The mathematical equivalence between softmax distributions and Boltzmann distributions suggests deeper connections between machine learning and statistical mechanics. Our work takes a step toward operationalizing this connection for practical benefit (calibration), but several theoretical questions remain:

1. **Is Shannon entropy the correct analog for thermodynamic entropy in classification?** While the mathematical forms are identical, thermodynamic entropy satisfies the Second Law of Thermodynamics (it never decreases in a closed system), whereas Shannon entropy does not have this property [13]. The physical interpretation of "temperature" in softmax distributions should be interpreted as a mathematical analogy rather than a claim of physical identity.

2. **What is the optimal functional form for per-sample temperature?** Our formulation $T_i = T_0 \cdot (1 + \alpha H(p_i) + \beta(1-m_i))$ is motivated by physical intuition but not derived from first principles. Alternative formulations (e.g., using only entropy, or using different combinations of uncertainty metrics) may prove more effective.

3. **Can inference-time temperature annealing improve calibration?** Our current method applies post-hoc calibration to fixed logits. An intriguing direction for future work is to anneal temperature during sequence generation, drawing on simulated annealing concepts from optimization. This would require integrating calibration objectives into the decoding process.

### 5.2 Limitations

**Evaluation on synthetic data.** Our experiments use synthetic miscalibrated data rather than real LLM embeddings. While this allows controlled evaluation, it may not fully capture the calibration challenges in production LLM systems. The performance of TEC on real data remains to be evaluated.

**Modest improvement over baseline.** On the current dataset, TEC provides only moderate calibration improvement compared to temperature scaling. This may be because (a) the dataset has uniform miscalibration that a global temperature corrects adequately, or (b) our hyperparameter tuning or functional form is suboptimal.

**Hyperparameter sensitivity.** TEC introduces two additional hyperparameters ($\alpha$ and $\beta$) beyond the base temperature $T_0$. This increases the risk of overfitting on small validation sets. Future work should explore more robust hyperparameter estimation techniques.

**Binary classification only.** Our evaluation focuses on binary sentiment classification (SST-2). The method should be evaluated on multi-class datasets (e.g., AG News with 4 classes, DBpedia with 14 classes) to ensure the approach generalizes.

### 5.3 Future Work

**Evaluation on diverse datasets.** We have prepared five standardized text classification datasets for comprehensive evaluation: SST-2 (binary), QNLI (binary), AG News (4 classes), MNLI (3 classes), and DBpedia (14 classes) [ARTIFACT:art_SSmr6ZrIe2PQ]. Evaluating TEC on these datasets will provide a more complete picture of its effectiveness.

**Inference-time temperature annealing.** The most intriguing future direction is to anneal temperature during sequence generation rather than applying post-hoc calibration. Drawing on simulated annealing [14], we could start with high temperature (exploring diverse generations) and gradually decrease temperature (converging to confident predictions). The annealing schedule could be informed by real-time uncertainty estimates.

**Connection to semantic entropy.** Combining TEC with semantic entropy [2] is a promising direction. Semantic entropy clusters semantically equivalent generations and computes entropy over meaning clusters. Adjusting temperature based on semantic entropy (rather than token-level entropy) may better capture uncertainty in generative LLM tasks.

**Theoretical analysis.** A deeper theoretical analysis of the connection between information-theoretic and thermodynamic entropy in the context of neural network calibration could motivate improved calibration objectives. For example, minimizing the thermodynamic free energy $F = U - TS$ (internal energy minus temperature times entropy) might provide a principled calibration loss function.

## 6 Conclusion

This paper introduced Thermodynamic Entropy Calibration (TEC), a physics-inspired post-hoc calibration method that adjusts per-sample temperature based on predictive entropy and decision margin. By drawing on the mathematical equivalence between softmax distributions and Boltzmann distributions, TEC provides an interpretable approach to confidence calibration.

Our evaluation on synthetic miscalibrated data shows that while standard temperature scaling achieves the best calibration performance (ECE = 0.031), TEC still provides meaningful improvement over uncalibrated baselines (ECE = 0.162 vs. 0.243 uncalibrated, a 33.4% reduction). All methods maintain classification accuracy, confirming that calibration adjustments need not compromise predictive performance.

The primary contribution of this work is not the empirical results alone, but the introduction of a physics-inspired framework for thinking about calibration. By connecting predictive uncertainty to thermodynamic entropy, we open new avenues for developing calibration methods grounded in statistical mechanics principles.

Future work should focus on: (1) evaluating TEC on diverse real-world datasets with varying numbers of classes, (2) developing inference-time temperature annealing schedules that adapt dynamically during generation, and (3) combining TEC with semantic entropy for improved uncertainty quantification in generative LLM tasks.

As LLMs see increasing deployment in high-stakes applications, well-calibrated confidence estimates are essential for building trustworthy AI systems. Physics-inspired calibration methods like TEC represent a promising direction for achieving this goal.

## References

[1] Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings of the 34th International Conference on Machine Learning (ICML)*.

[2] Kuhn, L., Gal, Y., and Farquhar, S. (2023). Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation. In *Proceedings of the 11th International Conference on Learning Representations (ICLR)*.

[3] Physics Stack Exchange (2023). Softmax function - relation to statistical mechanics. https://physics.stackexchange.com/questions/669314/softmax-function-relation-to-stat-mech

[4] Yang, A., et al. (2024). Let it calm: Exploratory annealed decoding for verifiable reinforcement learning. https://yangalan123.github.io/ead_rlvr/

[5] Kull, M., Perello-Nieto, M., Kängsepp, M., Silva Filho, T., Song, H., and Flach, P. (2019). Beyond temperature scaling: Obtaining well-calibrated multi-class probabilities with Dirichlet calibration. *Advances in Neural Information Processing Systems (NeurIPS)*, 32.

[6] Tomani, C., Gruber, S., Erdem, M. E., Cremers, D., and Buettner, F. (2021). Parameterized temperature scaling for boosting the expressive power of convolutional neural network architectures. *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)*.

[7] Joy, T., Pinto, F., Lim, S. N., Torr, P. H., and Dokania, P. K. (2023). Sample-dependent adaptive temperature scaling for improved calibration. In *Proceedings of the AAAI Conference on Artificial Intelligence*, 37(12).

[8] Xie, H., Qing, Y., Huang, Y., and Xiao, Y. (2024). Calibrating language models with adaptive temperature scaling. *arXiv preprint arXiv:2409.19817*.

[9] Tian, K., Mitchell, E., Zhou, A., Sharma, A., Rafailov, R., Yao, H., and Finn, C. (2023). Just ask for calibration: Strategies for eliciting calibrated confidence estimates from language models. *arXiv preprint arXiv:2305.14975*.

[10] Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379-423.

[11] Gal, Y. and Ghahramani, Z. (2016). Dropout as a Bayesian approximation: Representing model uncertainty in deep learning. In *Proceedings of the 33rd International Conference on Machine Learning (ICML)*.

[12] Towards AI (2023). The softmax function every transformer uses is the Boltzmann distribution, not inspired by it. https://pub.towardsai.net/the-softmax-function-every-transformer-uses-is-the-boltzmann-distribution-not-inspired-by-it-not-080fb2036918

[13] Wikipedia contributors (2023). Entropy in thermodynamics and information theory. https://en.wikipedia.org/wiki/Entropy_in_thermodynamics_and_information_theory

[14] Wikipedia contributors (2023). Simulated annealing. https://en.wikipedia.org/wiki/Simulated_annealing

[15] Wikipedia contributors (2023). Brier score. https://en.wikipedia.org/wiki/Brier_score

[16] Joshi, M., Choi, E., Weld, D. S., and Zettlemoyer, L. (2017). TriviaQA: A large scale distantly supervised challenge dataset for reading comprehension. In *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (ACL)*.

[17] Wang, A., Singh, A., Michael, J., Hill, F., Levy, O., and Bowman, S. (2018). GLUE: A multi-task benchmark and analysis platform for natural language understanding. *arXiv preprint arXiv:1804.07461*.

[18] Lin, S., Hilton, J., and Evans, O. (2021). TruthfulQA: Measuring how models mimic human falsehoods. *arXiv preprint arXiv:2109.07914*.

</current_paper>

<reviewer_feedback>
Paper reviewer feedback from the previous iteration. Your strategy MUST address these critiques.
Prioritize major issues — these are the most impactful improvements to make.

- [MAJOR] (evidence) The evaluation is conducted exclusively on synthetic miscalibrated data mimicking SST-2, not on real LLM embeddings. The paper acknowledges this limitation (Section 5.2, first paragraph) but proceeds with only synthetic evaluation. Synthetic data allows controlled evaluation but does not demonstrate that the method works on real LLMs facing real calibration challenges. Importantly, the authors have already collected 5 diverse text classification datasets (artifact art_SSmr6ZrIe2PQ) but did not use them in the experiments.
  Action: Evaluate TEC on real LLM embeddings using the collected datasets (SST-2, QNLI, AG News, MNLI, DBpedia). The datasets are already standardized and ready for use. At minimum, evaluate on SST-2 using a pre-trained model (e.g., DistilBERT) to generate real logits. This is critical for demonstrating that TEC works on real data, not just synthetic examples. Expected score impact: +2-3 points (major blocker for acceptance).
- [MAJOR] (novelty) The paper does not clearly establish novelty over existing adaptive temperature scaling methods. Joy et al. (2023) and Xie et al. (2024) both propose sample-dependent/adaptive temperature scaling. The paper mentions these works in Section 2.1 but claims TEC differs by using 'physics-inspired principles' rather than 'learning temperature adjustments from data alone.' However, the TEC formula T_i = T_0 * (1 + alpha * H(p) + beta * (1 - m)) is essentially a heuristic that could be viewed as a simplified version of the neural network approach in Tomani et al. (2021). The 'physics-inspired' framing is interesting but does not constitute a clear algorithmic novelty.
  Action: Clearly differentiate TEC from ATS (Joy et al. 2023) and PTS (Tomani et al. 2021). Specific suggestions: (1) Compare TEC directly to ATS on the same datasets - does the physics-inspired heuristic outperform the learned approach? (2) Ablate the contribution of the physics framing - is TEC better than simply using entropy + margin as features in a small neural network (as in PTS)? (3) If the key novelty is inference-time temperature annealing (Section 5.3), then implement that and compare to post-hoc methods. Expected score impact: +1-2 points.
- [MAJOR] (evidence) TEC underperforms standard temperature scaling by a large margin: ECE = 0.162 for TEC vs. 0.031 for temperature scaling (87.1% reduction for TS vs. 33.4% for TEC). The paper acknowledges this (Section 4.4) and hypothesizes that TEC might benefit heterogeneous miscalibration scenarios, but this hypothesis is not tested. The current results suggest that the per-sample temperature adjustment in TEC is actually harmful for this dataset - a global temperature works better. Without evidence that TEC outperforms in heterogeneous settings, the empirical contribution is weak.
  Action: Test the hypothesis that TEC benefits heterogeneous miscalibration scenarios: (1) Create or find datasets with varying difficulty/ambiguity, (2) Evaluate on multi-class datasets where some classes are more confusable (e.g., AG News), (3) Test on out-of-distribution data where confidence should be well-calibrated. If TEC does not outperform TS on these challenging scenarios, then the paper needs to reframe the contribution (e.g., as an interpretability tool rather than a calibration improvement method). Expected score impact: +2 points.
- [MAJOR] (scope) The evaluation is limited to binary classification (SST-2 sentiment) on synthetic data. The method's applicability to multi-class settings (where calibration is often more challenging) is not demonstrated. The paper mentions in Section 5.2 that evaluation on multi-class datasets 'should be evaluated' but does not do so. The collected datasets include AG News (4 classes), MNLI (3 classes), and DBpedia (14 classes) - these should be used.
  Action: Evaluate TEC on multi-class datasets, especially DBpedia (14 classes) where calibration is challenging. Multi-class calibration often exhibits class-conditional miscalibration patterns that global temperature scaling cannot correct (motivating Dirichlet calibration). This is a good test for whether per-sample temperature helps. Expected score impact: +1-2 points.
- [MINOR] (methodology) The hyperparameter tuning uses grid search over a limited space (T_0 in {0.5, 0.75, 1.0, 1.25, 1.5, 2.0}, alpha in {0.0, 0.25, 0.5, 0.75, 1.0}, beta in {0.0, 0.25, 0.5}). The optimal T_0 = 2.0 is at the boundary of the search space, suggesting the search space may be too constrained. Additionally, using NLL as the tuning criterion may not be optimal for calibration - ECE or Brier score might be better objectives.
  Action: Expand the grid search space for T_0 (e.g., up to 5.0 or 10.0) since the optimal temperature for temperature scaling is T=4.53, and TEC uses T_0 as a base temperature. Consider tuning hyperparameters to minimize ECE rather than NLL, since the goal is calibration not likelihood. Expected score impact: +0.5 point.
- [MINOR] (clarity) The introduction claims 'no prior work combines temperature scaling with temperature annealing during inference for improved calibration' (Section 1.2 and related work). However, the current method (TEC) is post-hoc calibration applied to fixed logits - it does NOT anneal temperature during inference. Temperature annealing during inference is mentioned only as future work (Section 5.3). This creates confusion about what the paper's actual contribution is.
  Action: Clarify the contribution: (1) If the paper is about post-hoc calibration (current implementation), then remove or downplay references to inference-time temperature annealing in the introduction and related work, (2) If inference-time annealing is the key contribution, then implement it and move it from 'future work' to the main method. The current version straddles both and creates confusion. Expected score impact: +0.5 point.
- [MINOR] (rigor) The paper claims '33.4% ECE reduction' for TEC (Section 4.2, Table 1), but this is misleading because the baseline ECE is very high (0.243). A more informative comparison would report: (1) calibration error reduction relative to temperature scaling (TEC achieves 0.162 vs 0.031 for TS - TS is 5x better), (2) statistical significance of the improvement over uncalibrated baseline (only 175 test samples - is the improvement significant?), (3) variance across multiple random seeds/splits.
  Action: Add statistical significance testing (bootstrap or multiple random splits) to verify that TEC's improvement over uncalibrated baseline is statistically significant. Report variance/confidence intervals for ECE and other metrics. Compare TEC to temperature scaling more directly - acknowledge that TS outperforms TEC and explain under what conditions TEC might be preferable. Expected score impact: +0.5 point.
- [MINOR] (methodology) The synthetic data generation process (Section 4.1, implemented in generate_synthetic_data function) intentionally introduces miscalibration. However, the type of miscalibration introduced (uniform overconfidence correctable by global temperature) is favorable to temperature scaling and unfavorable to per-sample methods like TEC. The paper should use more diverse miscalibration patterns to test when TEC is beneficial.
  Action: Generate synthetic data with heterogeneous miscalibration: (1) easy examples are well-calibrated, hard examples are overconfident, (2) class-conditional miscalibration (some classes more overconfident than others), (3) outlier examples with very high confidence but wrong predictions. Evaluate whether TEC handles these patterns better than global temperature scaling. Expected score impact: +0.5-1 point.
</reviewer_feedback>

<task>
Generate 1 research strategy for THIS iteration.

**ARTIFACT LIMIT: Each strategy may contain AT MOST 3 artifact directions.** Focus on the highest-impact artifacts. Quality over quantity.

Each strategy should:
1. Define a clear OBJECTIVE - what novel contribution we're building toward
2. Plan artifacts to execute NOW - specify type, objective, approach, and depends_on for each
3. Account for parallel execution - all strategies and all planned artifacts run simultaneously, their artifacts are combined into one shared pool


</task><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_strat/gen_strat_1/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactDep": {
      "description": "A single dependency on an existing artifact, with a short type label.\n\n``id`` and ``label`` are LLM-generated at strategy time. ``label`` is free-text but\nshort \u2014 a word or two naming the type of dependency, not a sentence.\n\n``relation_type`` and ``relation_rationale`` are populated later, in upd_hypo,\nusing the MultiCite citation-function typology (Lauscher et al., NAACL 2022).\nThey are absent at strategy time and may stay absent for legacy runs.",
      "properties": {
        "id": {
          "description": "ID of an existing artifact this artifact depends on",
          "title": "Id",
          "type": "string"
        },
        "label": {
          "description": "Short free-text label naming the type of this dependency (a word or two, not a sentence)",
          "title": "Label",
          "type": "string"
        }
      },
      "required": [
        "id",
        "label"
      ],
      "title": "ArtifactDep",
      "type": "object"
    },
    "ArtifactDirection": {
      "description": "High-level direction for an artifact to execute this iteration.\n\nID is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).",
      "properties": {
        "type": {
          "description": "Type of artifact to create",
          "enum": [
            "experiment",
            "research",
            "proof",
            "evaluation",
            "dataset"
          ],
          "title": "Type",
          "type": "string"
        },
        "objective": {
          "description": "What we want to achieve with this artifact",
          "title": "Objective",
          "type": "string"
        },
        "approach": {
          "description": "High-level direction/method",
          "title": "Approach",
          "type": "string"
        },
        "depends_on": {
          "description": "Existing artifacts this depends on, each with a short type label",
          "items": {
            "$ref": "#/$defs/ArtifactDep"
          },
          "title": "Depends On",
          "type": "array"
        }
      },
      "required": [
        "type",
        "objective",
        "approach"
      ],
      "title": "ArtifactDirection",
      "type": "object"
    },
    "Strategy": {
      "description": "A research strategy.\n\nContent fields have LLMPrompt + LLMStructOut markers.\n``id`` is code-assigned (LLMPrompt only \u2014 visible in prompts, not LLM-generated).\n\nID format: gen_strat_idx{N}",
      "properties": {
        "title": {
          "description": "Strategy name in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "objective": {
          "description": "The novel contribution we're building toward",
          "title": "Objective",
          "type": "string"
        },
        "rationale": {
          "description": "Why this strategy is promising",
          "title": "Rationale",
          "type": "string"
        },
        "artifact_directions": {
          "description": "Artifacts to execute THIS iteration",
          "items": {
            "$ref": "#/$defs/ArtifactDirection"
          },
          "title": "Artifact Directions",
          "type": "array"
        },
        "expected_outcome": {
          "description": "What we'll have after this iteration's artifacts complete",
          "title": "Expected Outcome",
          "type": "string"
        },
        "summary": {
          "default": "",
          "description": "Brief summary of the strategy and its expected contribution",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "title",
        "objective",
        "rationale",
        "artifact_directions",
        "expected_outcome"
      ],
      "title": "Strategy",
      "type": "object"
    }
  },
  "description": "Top-level wrapper for LLM strategy generation output.",
  "properties": {
    "strategies": {
      "description": "List of generated strategies",
      "items": {
        "$ref": "#/$defs/Strategy"
      },
      "title": "Strategies",
      "type": "array"
    }
  },
  "required": [
    "strategies"
  ],
  "title": "Strategies",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_strat/gen_strat_1/.sdk_openhands_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-07-18 16:33:00 UTC

```
Better uncertainty calibration for LLM classifiers
```

### [3] SKILL-INPUT — aii-handbook-auto-multi-agent-llm-systems · 2026-07-18 16:33:12 UTC

The agent loaded the **aii-handbook-auto-multi-agent-llm-systems** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

```
---
name: aii-handbook-auto-multi-agent-llm-systems
description: "Verified field handbook for multi-agent LLM systems (MAS) research. ALWAYS read before ANY multi-agent-LLM research work — ideation/novelty assessment, study planning, experiment/eval design, write-up, or review; do NOT do any of these from priors alone (the frontier moved fast through H1-2026 and several obvious-looking directions are saturated). Triggers: multi-agent systems / MAS, agent orchestration or topology, multi-agent debate, mixture-of-agents, inter-agent communication or protocols (MCP/A2A), MAS failure analysis / attribution / self-evolution, MAS benchmarks, cost or token economics of agent systems. NOT for: building single-agent apps, framework API how-tos (AutoGen / LangGraph / CrewAI usage), classical non-LLM multi-agent systems (MARL, robotics, agent-based social simulation), or generic prompting questions."
---

<!-- GENERATED by amg-handbook-forge — DRAFT for expert review. generated: 2026-07-07 · next_check:
     2026-10 (volatile.md half-life ≈ months). ✓x=exec · [Sn]=cited · ⚠️=candidate. Row fails → `STALE: <what>` in place. -->

# Multi-agent LLM systems — field handbook

## Overview

Scope: task-solving LLM multi-agent systems (classical non-LLM MARL and societal simulation are different
literatures). The star is the SUBSTRATE below — a dated, source-anchored map of where the field stands mid-2026,
with an explicit do-not-redo list. The only lens is open questions; nothing here prescribes a direction. Every
[Sn] resolves to a verbatim quote in [SOURCES.md](SOURCES.md); date-sensitive figures live in [volatile.md](volatile.md).

## Organizing principles (how the field reasons)

- The newest synthesis organizes the field as the LIFE progression — Lay the capability foundation → Integrate
  through collaboration → Find faults through attribution → Evolve through self-improvement — with the F→E
  handoff as its named weak link [S2].
- The failure locus is coordination, not member capability: errors propagate across agents and interaction
  rounds, are hard to diagnose, and rarely feed back into structure [S2] [S1].
- The field's working null hypothesis is economic: token spend, not architecture, explains most performance
  variance, so any structural claim is judged against matched-compute aggregation [S3] [S7].
- That null now has a theory: at a fixed reasoning-token budget with perfect context use, a single agent is more
  information-efficient (Data Processing Inequality — each handoff can only lose information); MAS is predicted
  competitive only where context use degrades or more compute is spent [S6].
- Verification is treated as easier than generation, so verifier count is a live test-time scaling axis [S15] —
  but self-evaluation without an external signal is known to fail and can degrade answers [S16].
- Inter-agent natural language is a chosen tradeoff, not a given: interpretable and overseeable, but argued
  structurally misaligned with the vector spaces models compute in (information loss, behavioral drift) [S18].

## Frontier (recency-weighted)

### Structure vs matched compute (weight-capped here — the saturated core, see repeller)

- First systematic multi-agent-debate evaluation (5 MAD methods × 9 benchmarks × 4 models): MAD often fails to
  beat single-agent CoT / Self-Consistency even at much higher inference compute; the one robust lever found is
  model heterogeneity, named a universal antidote [S7] (2025-02, rev 2025-06).
- The critique now has a theory, not just benchmarks: the Data Processing Inequality argument predicts exactly
  when MAS becomes competitive — degraded single-agent context use, or extra compute [S6] (2026-04).

### Topology & orchestration

- Adaptive/learned MAS optimized per-benchmark show "topological overfitting" (no cross-domain transfer) and
  "illusory coordination" (surface accuracy while interactions diverge from intended behavior) [S9] (2026-04).
- Live counter-current: task-adaptive topology routing (parallel / sequential / hierarchical / hybrid per task)
  reports 12–23% over static single-topology baselines at identical models — single-author preprint, directly
  clashing with [S9]; see Open questions [S10] (2026-02).

### Failure, attribution & repair

- MAST is the field's failure instrument — exact figures (commonly mis-recalled): taxonomy built from 150 traces
  (kappa = 0.88), 14 modes / 3 categories; MAST-Data = 1600+ annotated traces, 7 frameworks [S1] (2025-03, rev 2025-10).
- Failure attribution (which agent, which step) is formalized and benchmarked — and far from solved: the best
  automated method reaches 53.5% (Who&When, ICML 2025 Spotlight) [S12] (2025-04).
- Verifier/critic agents act with a DELAY, so false claims propagate before correction — yielding instability
  thresholds and optimal corrector placement (single-author preprint) [S13] (2026-06).
- E-stage methods arriving: TPGO treats the MAS as a graph of optimizable nodes and derives textual feedback
  from execution traces to pinpoint failures and suggest granular edits [S14] (2026-04).

### Communication & interop

- The latent-communication thread passes continuous hidden states between agents on the premise that
  downsampling thought to discrete tokens loses information — a heavily occupied lane [S17] (2025-11).
- Protocol scope split a reviewer expects you to know: MCP = model↔tools/data (a single open standard replacing
  per-source connectors); A2A = agent↔agent, explicitly complementary to MCP [S4] (2024-11) · [S5] (2025-04).

### Evaluation & economics

- MAS eval has moved past final accuracy: MultiAgentBench (ACL 2025) scores collaboration quality with
  milestone-based KPIs and compares coordination protocols (star / chain / tree / graph) [S20] (2025-03).
- First independent (non-vendor) cost-accuracy Pareto: over 4 orchestration patterns × 5 LLMs on 10,000
  financial documents, reflexive tops F1 (0.943) at 2.3× cost; hierarchical supervisor-worker sits on the
  Pareto frontier (F1 0.921 at 1.4×) [S21] (2026-03).

## Recent (~1–2 yr, compressed)

- Multi-Agent Verification: scale the NUMBER of off-the-shelf aspect verifiers (binary approve/reject, no
  training) as the test-time axis — verification, not more debate rounds [S15] (2025-02).
- The two production-craft poles, both vendor-staked (2025-06): Cognition — reliability = context engineering on
  ONE thread [S19]; Anthropic — MAS pays off on parallel-heavy, context-exceeding, tool-heavy tasks at ~15× token cost [S3].
- Position line naming the comms tension: NL is structurally misaligned with LLM vector spaces —
  interpretability bought at an information cost [S18] (2025-06).

## Durable core (the few foundations that still hold)

- Du et al. 2023 — the founding "debate improves reasoning" result; the baseline the skeptic line attacks [S23].
- Mixture-of-Agents — layered aggregation, each layer reads all prior-layer outputs; 65.1 vs 57.5 (GPT-4 Omni)
  on AlpacaEval 2.0 — read as aggregation until cost-matched [S22].
- MetaGPT — canonical role-crew/SOP assembly line; the hand-designed baseline learned methods must beat [S24].
- LLMs cannot reliably self-correct reasoning without external feedback (ICLR 2024) [S16].
- ADAS — the learned-topology transfer CLAIM (a meta agent programs new agents in code; claims cross-domain
  robustness) — now directly contested, see Open questions [S11].
- "More Agents Is All You Need" — agent-count scaling via sampling-and-voting; reread today as self-consistency [S25].

## Already crowded — go ELSEWHERE (do-not-redo)

The blank space is NOT in these lanes; each is saturated through H1-2026:

- Compute-matched "does MAS beat a single agent per $": benchmark wave + DPI theory + newest entrant showing
  auto-generated MAS underperform CoT-SC at up to 10× the cost — the field's loudest thread [S6] [S8].
- Adaptive/learned topology AND its rebuttal: both the method line and the "topological overfitting / illusory
  coordination" critique are published [S10] [S9].
- Failure attribution (which agent/step): named benchmark plus a dense 2026 follow-on wave [S12].
- Latent / vector inter-agent communication (hidden-state, KV-cache variants) — already has a unifying survey [S17].
- Self-evolving / self-improving MAS: dense H1-2026 wave of frameworks that learn to evolve from execution
  feedback, plus a dedicated survey [S14].
- Building new interop protocols: MCP + A2A are standardized, vendor-backed, foundation-governed — compose on
  them instead of proposing another [S4] [S5].

## Open questions the field hasn't answered (the whole lens — the reader answers in their own way)

1. Once inference compute, sample aggregation, and context-window relief are controlled, what residual — if
   any — do the agentic ingredients (roles, personas, turn-taking, inter-agent dialogue) contribute, and on
   which task families? The theory predicts MAS wins only under degraded context use or extra compute [S6] [S7];
   no result yet isolates the residual itself.
2. What makes a critique or verification signal genuinely EXTERNAL? Self-correction fails without external
   feedback [S16], task verification is one of MAST's three failure categories [S1] — so does a same-family
   peer critic count as external, and where exactly is the boundary?
3. Same object, opposite 2026 verdicts: task-adaptive topology reports +12–23% at identical models [S10], while
   independent evaluation finds adaptive MAS overfit topologically with illusory coordination [S9], and the
   claimed cross-domain transfer of searched designs [S11] is measured as no advantage over CoT-SC [S8]. Under
   what conditions does learned structure transfer, and what evaluation separates real coordination from
   surface accuracy?
4. Why do diagnosed failures rarely translate into structural self-improvement [S2]? Attribution is benchmarked
   (best 53.5% [S12]) and typed blame signals exist [S1] — what is missing between a localized, typed fault and
   a safe structural change (the survey's own closed-loop agenda [S2])?
5. Can MAS reliability be predicted before running rather than measured after? Error propagation is the named
   failure locus [S2], delay effects already yield instability thresholds and corrector-placement results [S13],
   and a 1600+-trace corpus exists to fit against [S1] — yet there is no compositional account mapping
   per-agent error rates + topology to system reliability.
6. Is model-pool heterogeneity the actual mechanism behind reported multi-agent gains? It is the quoted
   "universal antidote" and the named reopening condition for the buried debate line [S7] — would a
   matched-compute heterogeneous pool beat self-consistency over the single best model?

## What counts as DEEP here (taste)

| Naive move | Expert judgment/move | Why (failure prevented) | tier | src |
|---|---|---|---|---|
| Ship another MAS framework: +X% on one benchmark, unmatched compute, no failure analysis | The rewarded move is a reusable diagnostic instrument — MAST, "the first Multi-Agent System Failure Taxonomy"; recognition = independent adoption (IBM applied it to turn raw ITBench traces into structured failure signatures) | problematizes-nothing — the field's own critique names weak baselines / limited coverage as the incremental signature | L·B | [S1] [S26] [S7] |
| Homogeneous multi-agent debate as a reasoning booster | Buried (2025-02→06): MAD often loses to CoT/Self-Consistency at higher compute. Reopening condition, per the same paper: model-heterogeneous pools at matched compute | dead-end | L | [S7] |
| Intrinsic self-correction — an agent repairing its own reasoning with no external signal | Buried (2023-10, ICLR 2024): performance can even degrade after self-correction. Reopens only with an external correction signal (tools, execution, ground truth); whether a same-family peer counts is unresolved | dead-end | L | [S16] |
| "More homogeneous agents = collaboration advance" (agent-count scaling) | Buried: the effect is sampling-and-voting — reproducible by self-consistency, and single-agent is information-optimal at matched budget. Reopens if structured, communicating agents beat a matched-token aggregation-only arm | dead-end | L | [S25] [S7] [S6] |

Science-vs-application, as this field draws it: the science bar is a matched-compute, failure-analyzed,
mechanism-attributing claim (the critique's demand to rethink evaluation and stop overvaluing MAD as-is [S7]);
a working framework with a headline delta and no failure analysis is application-tier [S7] [S1].

## Critical rules (execution · eval · validity)

| Naive move | Expert judgment/move | Why (failure prevented) | tier | src |
|---|---|---|---|---|
| Compare the MAS against one weak single call, or at unmatched spend | Designing the comparison: equalize TOTAL tokens and $ across arms; report accuracy-vs-cost, expecting MAD-loses-to-CoT/SC as the outcome to beat | wrong-result — the gain may be purchased compute, not method | L | [S7] [S6] |
| Attribute a win to collaboration/structure directly | Before claiming structure: add a matched-token aggregation-only arm (same N samples + vote/judge, no roles or dialogue); structure must beat THAT | wrong-result — aggregation alone reproduces debate-like gains | L | [S7] [S25] |
| Mix model pools freely, or test a single model | Choosing pools: run homogeneous and heterogeneous pools as an explicit factor — heterogeneity is the named confound and lever | wrong-result — pool diversity, not the mechanism, may carry the gain | L | [S7] |
| Report top-line accuracy only | Reporting: annotate traces against MAST (14 modes / 3 categories) and give the failure-mode distribution; add collaboration/process metrics, not just completion | wasted-cost — unactionable eval; reads incremental in 2026 | L | [S1] [S20] |
| Claim MAS superiority in general | Writing the claim: scope to the predicted-win regime (degraded single-agent context use, or more compute [S6]; value covering ~15× tokens [S3]) and name where it should NOT help (shared-context work) | wrong-result — overclaim against the known boundary invites the skeptic line | L·B·C | [S6] [S3] [S19] |
| Review a "new MAS framework" on its own terms | Reviewing: map it onto the settled canon — debate, MoA/voting, role-crews, learned topology search — and demand the explicit delta vs the nearest | wrong-result — re-skins ship as novel | L | [S23] [S22] [S24] [S11] |

## Decision guide

- Shared-context, dependency-dense work (most coding): single thread + context engineering is the
  production-proven pole [S19]; go multi-agent where single-agent context use degrades or more compute is
  justified [S6] and task value covers ~15× tokens [S3]. Both poles are vendor-staked — see SOURCES.
- Picking an orchestration pattern under a budget: the one independent Pareto study puts hierarchical
  supervisor-worker on the cost-accuracy frontier (F1 0.921 at 1.4×), reflexive best-but-2.3× — scoped to
  financial-document extraction [S21].
- Spending test-time compute: verifier COUNT is a demonstrated scaling axis [S15]; more debate rounds is not
  [S7]; a critique signal must be external to count [S16].
- Verifier placement: verification acts with delay, so false claims propagate before correction —
  placement/timing, not mere presence, is the lever (single-author framing) [S13].
- Interop plumbing: MCP for model↔tools/data, A2A for agent↔agent — explicitly complementary; pick by scope
  rather than conflating them [S4] [S5].

## Ground rules (known-lane — terse)

- MAS ≈ 15× chat tokens; token usage alone ≈ 80% of variance — vendor-internal, single-origin figures [S3].
- Settled canon a novelty claim must clear: multi-agent debate [S23] · MoA / layered aggregation [S22] ·
  role-crews / SOP pipelines [S24] · learned topology search [S11].
- MAST's three failure categories: system design issues · inter-agent misalignment · task verification [S1].
- MoA's 65.1 vs 57.5 (AlpacaEval 2.0) is an aggregation result — cost-match before citing it as a multi-agent win [S22].

## Reference documentation

- **[volatile.md](volatile.md)** — every date/version-sensitive figure above (trace counts, SOTA numbers,
  cost anchors, the crowded list's shelf life); re-check before relying on any number.
- **[SOURCES.md](SOURCES.md)** — provenance: every [Sn] with tier, reliable-for scope, and verbatim quote.

## Candidate lane  ⚠️ (expert to resolve — NOT verified)

- ⚠️ "Attribution→repair is now tractable" is INFERRED, not quoted: typed blame signals + a 1600+-trace corpus
  exist [S1] and the survey names the F→E gap and a closed-loop agenda [S2], but no fetched source states the
  repair loop is newly enabled; known E-stage work optimizes orchestration rather than closing
  attribution-driven, non-regression-verified repair. Confirm: a 2026 paper citing attribution artifacts as its
  enabler and verifying non-regression. Refute: such a paper exists → treat this lane as crowded too.
- ⚠️ "Compositional reliability theory is uncrowded" rests on a single scan: adjacent work exists (delay /
  instability thresholds [S13]) but no per-agent-error→system-reliability composition theory was found — low
  confidence. Confirm or refute with a fresh search for a MAS reliability-calculus paper before investing.
- ⚠️ Taste anchor is substituted: the DEEP exemplar's award/meta-review rationale was not recoverable (review
  page access-gated), so the taste row rests on adoption-by-reference (IBM applying MAST [S26]) rather than a
  committee rationale. Confirm: recover the venue meta-review or an equivalent award rationale and check it
  names the same separating cue.
```
