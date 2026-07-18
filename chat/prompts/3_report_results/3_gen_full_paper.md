# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_3fUR0i5e8NC7` — Thermodynamic Entropy Calibration for Improved Confidence Estimation in LLM Classifiers
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-18 18:38:11 UTC

````
<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: >-
  Thermodynamic Entropy Calibration for Improved Confidence Estimation in LLM Classifiers
abstract: >-
  Large Language Models (LLMs) produce overconfident predictions that undermine their reliability in high-stakes applications.
  While temperature scaling effectively reduces calibration error, it applies a global adjustment that cannot account for
  varying uncertainty across individual predictions. This paper introduces Thermodynamic Entropy Calibration (TEC), a post-hoc
  calibration method that adjusts per-sample temperature based on predictive entropy and decision margin, drawing on the mathematical
  equivalence between softmax distributions and Boltzmann distributions from statistical mechanics. We evaluate TEC on five
  text classification datasets (SST-2, QNLI, AG News, MNLI, DBpedia) using pre-trained transformer embeddings. Results show
  that TEC provides conditional benefits: it outperforms standard temperature scaling on QNLI (ECE=0.0042 vs. 0.0076) and
  DBpedia (ECE=0.0075 vs. 0.0088), both datasets with heterogeneous miscalibration patterns, while temperature scaling remains
  superior on simpler binary classification tasks. Across all datasets, both methods significantly improve calibration over
  uncalibrated baselines (ECE reductions of 45-95%). Our analysis reveals that per-sample temperature adjustment is most beneficial
  when miscalibration is heterogeneous across samples-a condition that global temperature scaling cannot address. We further
  show that the physics-inspired formulation provides interpretability: practitioners can examine per-sample temperatures
  to understand how entropy and margin influence calibration.
paper_text: "# Introduction\n\nLarge Language Models (LLMs) have demonstrated remarkable capabilities across natural language\
  \ understanding tasks, yet their deployment in high-stakes domains remains hindered by unreliable confidence estimates.\
  \ A well-calibrated classifier should produce predicted probabilities that reflect true outcome frequencies: among all predictions\
  \ made with 80% confidence, approximately 80% should be correct [1]. Modern neural networks, including LLMs, systematically\
  \ violate this property, exhibiting overconfidence where predicted probabilities exceed actual accuracy [1].\n\nThis miscalibration\
  \ is particularly problematic for applications in healthcare, law, and autonomous systems, where overconfident incorrect\
  \ predictions can lead to consequential errors. While post-hoc calibration methods like temperature scaling [1] effectively\
  \ reduce calibration error, they apply a global temperature adjustment that may not account for varying uncertainty across\
  \ individual predictions. Recent work has explored input-dependent temperature adjustment [6, 7, 8], but these approaches\
  \ learn temperature from data using neural networks rather than deriving functional forms from principled theoretical foundations.\n\
  \nThis paper explores whether treating predictive uncertainty as thermodynamic entropy—drawing on the mathematical equivalence\
  \ between the softmax function and the Boltzmann distribution—can inspire interpretable calibration approaches. The key\
  \ insight is that temperature in softmax distributions plays an analogous role to thermodynamic temperature in statistical\
  \ mechanics: it controls the entropy (dispersion) of the probability distribution over classes [3, 12].\n\n## 1.1 Problem\
  \ Statement\n\nGiven a classifier that produces logits $z_i$ for each class $i$, the standard approach applies a global\
  \ temperature scaling:\n\n$$p_i = \\frac{\\exp(z_i / T)}{\\sum_j \\exp(z_j / T)}$$\n\nwhere $T > 0$ is a scalar temperature\
  \ parameter optimized on a validation set to minimize Expected Calibration Error (ECE) [1].\n\nThe limitation of this approach\
  \ is that a single temperature $T$ must balance calibration across all predictions, regardless of each sample's intrinsic\
  \ difficulty or ambiguity. Intuitively, easy examples (where the correct class is clear from the input) and ambiguous examples\
  \ (where multiple interpretations are plausible) may benefit from different temperature adjustments. Prior work on adaptive\
  \ temperature scaling [7, 8] addresses this limitation by predicting per-sample temperatures using learned functions, but\
  \ does not provide a physically interpretable connection between temperature and uncertainty.\n\n## 1.2 Proposed Approach\n\
  \nWe propose Thermodynamic Entropy Calibration (TEC), which computes per-sample temperatures based on two uncertainty indicators:\n\
  \n1. **Predictive entropy** $H(p) = -\\sum_i p_i \\log p_i$: Higher entropy indicates greater uncertainty.\n2. **Decision\
  \ margin** $m = p_{(1)} - p_{(2)}$: The difference between the top two predicted probabilities (higher margin = more confident).\n\
  \nThe per-sample temperature is computed as:\n\n$$T_i = T_0 \\cdot (1 + \\alpha \\cdot H(p_i) + \\beta \\cdot (1 - m_i))$$\n\
  \nwhere $T_0$, $\\alpha$, and $\\beta$ are hyperparameters tuned on a validation set.\n\nThis formulation has a physical\
  \ interpretation: samples with high entropy (analogous to high thermodynamic entropy) or low margin (analogous to low energy\
  \ difference between states) receive higher temperatures, producing flatter, more conservative probability distributions.\n\
  \n## 1.3 Summary of Contributions\n\nThis paper makes the following contributions:\n\n1. We introduce Thermodynamic Entropy\
  \ Calibration (TEC), a physics-inspired post-hoc calibration method that adjusts per-sample temperature based on predictive\
  \ entropy and decision margin. The method is compared against standard temperature scaling and uncalibrated baselines on\
  \ five diverse text classification datasets using real pre-trained transformer embeddings.\n\n2. We provide a comprehensive\
  \ evaluation showing that TEC provides **conditional** calibration benefits: it outperforms temperature scaling on datasets\
  \ with heterogeneous miscalibration (QNLI, DBpedia), while temperature scaling remains superior on simpler tasks. Both methods\
  \ significantly improve calibration over uncalibrated baselines.\n\n3. We evaluate TEC on multi-class datasets with up to\
  \ 14 classes (DBpedia), demonstrating that per-sample temperature adjustment can help in settings where class-conditional\
  \ miscalibration patterns exist.\n\n4. We discuss the theoretical implications and limitations of treating predictive uncertainty\
  \ as thermodynamic entropy, and provide an honest assessment of when physics-inspired calibration does and does not provide\
  \ empirical benefits.\n\n# Related Work\n\n## 2.1 Calibration Methods for Neural Networks\n\nTemperature scaling, introduced\
  \ by Guo et al. [1], is the simplest and most widely used post-hoc calibration method for modern neural networks. It optimizes\
  \ a single scalar temperature parameter $T$ by minimizing Negative Log-Likelihood (NLL) on a validation set. Despite its\
  \ simplicity, temperature scaling often outperforms more complex methods like vector scaling and matrix scaling [1].\n\n\
  Recent extensions have proposed more flexible calibration approaches:\n\n- **Dirichlet calibration** [5] generalizes temperature\
  \ scaling to natively handle multi-class settings using Dirichlet distributions, improving calibration especially when class-conditional\
  \ miscalibration patterns exist.\n\n- **Parameterized Temperature Scaling (PTS)** [6] computes prediction-specific temperatures\
  \ using a small neural network, reducing calibration error by approximately 30% over standard temperature scaling on vision\
  \ tasks.\n\n- **Adaptive Temperature Scaling (ATS)** [7] predicts temperature scaling parameters for each input using a\
  \ lightweight network trained on top of frozen embeddings. ATS is closely related to our work but learns the temperature\
  \ prediction function from data rather than deriving it from physical principles.\n\n- **Calibrating Language Models with\
  \ Adaptive Temperature Scaling** [8] extends ATS specifically for LLMs, showing that per-token temperature adjustment can\
  \ improve calibration in language generation tasks.\n\n**Differentiation from prior work.** TEC differs from ATS [7] and\
  \ PTS [6] in its use of physics-inspired principles: rather than learning temperature adjustments from data alone, we derive\
  \ the functional form of per-sample temperature from the thermodynamic analogy between predictive distributions and Boltzmann\
  \ distributions. The TEC formula $T_i = T_0 \\cdot (1 + \\alpha \\cdot H(p_i) + \\beta \\cdot (1 - m_i))$ is a **interpretable\
  \ heuristic** motivated by statistical mechanics, not a learned black-box function. This provides transparency: practitioners\
  \ can examine how entropy and margin influence each prediction's temperature. However, we acknowledge that this heuristic\
  \ does not currently outperform learned approaches on all datasets (see Section 4.2).\n\n## 2.2 Entropy-Based Uncertainty\
  \ Estimation\n\nEntropy is a fundamental measure of uncertainty in probability distributions. In Bayesian neural networks,\
  \ the entropy of the predictive distribution quantifies total uncertainty (sum of aleatoric and epistemic uncertainty) [11].\n\
  \nFor LLMs, recent work has adapted entropy-based uncertainty estimation to the generative setting:\n\n- **Predictive entropy**\
  \ [2] computes $PE(x) = H(Y|x) = -\\int p(y|x) \\ln p(y|x) dy$ over multiple generated samples, measuring uncertainty in\
  \ generated outputs.\n\n- **Semantic entropy** [2] addresses the observation that LLMs can generate semantically equivalent\
  \ but lexically different responses. By clustering semantically equivalent samples and computing entropy over meaning clusters\
  \ rather than individual tokens, semantic entropy provides better uncertainty estimates than token-level entropy.\n\n- **Length-normalized\
  \ entropy** [2] normalizes log-probabilities by sequence length to address the issue that longer generations accumulate\
  \ more uncertainty.\n\nOur approach uses **predictive entropy** (computed from the classifier's output distribution rather\
  \ than generated samples) as one component of per-sample temperature adjustment, connecting entropy-based uncertainty to\
  \ the thermodynamic interpretation of temperature. Importantly, TEC uses entropy from a **single forward pass** (the classifier's\
  \ output distribution), making it computationally cheaper than methods requiring multiple samples [2].\n\n## 2.3 Thermodynamic\
  \ Principles in Machine Learning\n\nThe connection between information theory and statistical mechanics has been recognized\
  \ since the work of Jaynes [13]. The key mathematical equivalences are:\n\n1. **Boltzmann distribution = Softmax**: The\
  \ Boltzmann distribution from statistical mechanics, $p_i = \\frac{1}{Z} e^{-\\beta E_i}$ where $\\beta = 1/T$, is mathematically\
  \ identical to the softmax function with logits $z_i = -E_i$ (negative energies) [3, 12].\n\n2. **Gibbs entropy = Shannon\
  \ entropy**: The Gibbs entropy formula $S = -k_B \\sum_i p_i \\ln p_i$ has the same mathematical form as Shannon entropy\
  \ $H = -\\sum_i p_i \\log p_i$, differing only in physical units ($k_B$ is Boltzmann's constant) [13].\n\nThese equivalences\
  \ suggest that techniques from statistical mechanics might inform machine learning practice. For example, simulated annealing\
  \ [14] uses a temperature schedule to escape local optima in optimization problems—a concept that could be adapted to temperature\
  \ scheduling during LLM inference. However, existing work using temperature schedules in LLMs focuses on reinforcement learning\
  \ exploration (e.g., Exploratory Annealed Decoding [4]) rather than calibration. \n\n**Novelty statement.** To our knowledge,\
  \ no prior work combines **per-sample temperature scaling** with the **thermodynamic entropy analogy** for improved calibration.\
  \ While ATS [7] and PTS [6] use per-sample temperatures, they do not draw on statistical mechanics for the functional form.\
  \ Conversely, work on thermodynamic connections [3, 12] establishes the mathematical equivalence but does not operationalize\
  \ it for calibration. Our contribution is to bridge these strands by deriving an interpretable, physics-inspired calibration\
  \ method and evaluating it on real LLM embeddings.\n\n## 2.4 Calibration Metrics and Benchmarks\n\nThe standard metric for\
  \ classification calibration is Expected Calibration Error (ECE) [1], which partitions predictions into $M$ bins based on\
  \ confidence and computes the weighted average of calibration gaps:\n\n$$ECE = \\sum_{m=1}^M \\frac{|B_m|}{n} |acc(B_m)\
  \ - conf(B_m)|$$\n\nwhere $B_m$ is the set of predictions in bin $m$, and $acc(B_m)$ and $conf(B_m)$ are the accuracy and\
  \ average confidence in that bin.\n\nOther metrics include:\n\n- **Brier Score** [15]: Mean squared difference between predicted\
  \ probabilities and one-hot encoded true labels, ranging from 0 (perfect) to 1 (worst).\n- **Negative Log-Likelihood (NLL)**:\
  \ Measures the average log-probability assigned to the true class, with lower values indicating better calibration.\n- **Maximum\
  \ Calibration Error (MCE)** [1]: The worst-case calibration gap across bins, focusing on the largest miscalibration.\n\n\
  Benchmarks for evaluating LLM calibration include TriviaQA and CoQA (used in semantic uncertainty work [2]), GLUE and SuperGLUE\
  \ [17] (general language understanding), and TruthfulQA [18] (measuring truthfulness). Our work uses five datasets spanning\
  \ binary and multi-class classification: SST-2 (binary sentiment), QNLI (binary natural language inference), AG News (4-class\
  \ topic classification), MNLI (3-class textual entailment), and DBpedia (14-class ontology classification).\n\n# Methods\n\
  \n## 3.1 Thermodynamic Entropy Calibration\n\nOur proposed Thermodynamic Entropy Calibration (TEC) method is a post-hoc\
  \ calibration approach that adjusts per-sample temperature based on uncertainty estimates. The method consists of three\
  \ steps:\n\n**Step 1: Compute uncalibrated probabilities and uncertainty metrics.**\n\nGiven logits $z_i$ for sample $i$,\
  \ compute:\n\n$$p_i = \\text{softmax}(z_i) \\quad \\text{(uncalibrated probabilities)}$$\n\n$$H(p_i) = -\\sum_k p_{i,k}\
  \ \\log p_{i,k} \\quad \\text{(predictive entropy)}$$\n\nSort probabilities in descending order and compute:\n\n$$m_i =\
  \ p_{i,(1)} - p_{i,(2)} \\quad \\text{(decision margin)}$$\n\n**Step 2: Compute per-sample temperature.**\n\n$$T_i = T_0\
  \ \\cdot (1 + \\alpha \\cdot H(p_i) + \\beta \\cdot (1 - m_i))$$\n\nwhere:\n- $T_0$ is a base temperature (analogous to\
  \ the global temperature in temperature scaling)\n- $\\alpha \\geq 0$ controls the weight of entropy\n- $\\beta \\geq 0$\
  \ controls the weight of (inverse) margin\n\nThis formulation ensures that samples with high entropy (uncertain predictions)\
  \ or low margin (close competition between top classes) receive higher temperatures, producing flatter, more conservative\
  \ probability distributions. The hyperparameters $T_0$, $\\alpha$, and $\\beta$ are tuned on a validation set (see Section\
  \ 3.3).\n\n**Step 3: Apply temperature adjustment.**\n\n$$\\tilde{p}_i = \\text{softmax}(z_i / T_i) \\quad \\text{(calibrated\
  \ probabilities)}$$\n\n[FIGURE:fig1]\n\n## 3.2 Physical Interpretation\n\nThe method draws on the following physical analogies:\n\
  \n- **Logits as negative energies**: Setting $E_{i,k} = -z_{i,k}$ (negative logit for class $k$) makes the softmax distribution\
  \ identical to the Boltzmann distribution $p_{i,k} \\propto e^{-E_{i,k}/T_i}$.\n- **Temperature as thermal energy**: In\
  \ statistical mechanics, higher temperature flattens the Boltzmann distribution, allowing the system to explore higher-energy\
  \ states. Similarly, higher $T_i$ flattens the predictive distribution, reducing confidence.\n- **Entropy as disorder**:\
  \ Higher predictive entropy corresponds to higher thermodynamic entropy (more disorder). The temperature adjustment $T_i\
  \ \\propto H(p_i)$ increases temperature for high-entropy (high-uncertainty) predictions.\n- **Margin as energy gap**: A\
  \ large margin $m_i$ indicates a clear preference for one class (analogous to a large energy gap between ground and excited\
  \ states). Small margin $\\rightarrow$ low energy gap $\\rightarrow$ higher temperature.\n\n## 3.3 Hyperparameter Tuning\n\
  \nThe hyperparameters $T_0$, $\\alpha$, and $\\beta$ are tuned on a validation set to minimize Expected Calibration Error\
  \ (ECE):\n\n$$\\mathcal{L}(T_0, \\alpha, \\beta) = \\text{ECE}(\\tilde{p}_i, y_i)$$\n\nwhere $y_i$ is the true label for\
  \ validation sample $i$. We use ECE (rather than NLL) as the tuning objective because the goal is calibration, not likelihood.\n\
  \nIn our implementation, we use grid search over an expanded space:\n- $T_0 \\in \\{0.5, 1.0, 2.0, 4.0, 6.0, 8.0\\}$\n-\
  \ $\\alpha \\in \\{0.0, 0.25, 0.5, 0.75, 1.0\\}$\n- $\\beta \\in \\{0.0, 0.25, 0.5\\}$\n\nThe expanded search space for\
  \ $T_0$ (up to 8.0) reflects that optimal temperatures for temperature scaling can exceed 4.0, and TEC's base temperature\
  \ should span a similar range.\n\n## 3.4 Baseline Methods\n\nWe compare TEC against two baselines:\n\n1. **Uncalibrated**:\
  \ Direct softmax probabilities from logits without any temperature adjustment.\n2. **Temperature Scaling** [1]: Global temperature\
  \ scaling with a single parameter $T$ optimized on the validation set to minimize ECE.\n\n# Experiments\n\n## 4.1 Experimental\
  \ Setup\n\n**Datasets.** We evaluate on five text classification datasets spanning binary and multi-class settings \\footnote{Code:\
  \ \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermodynamic-entropy-calibration-for-im/tree/main/round-1/dataset-1}}:\n\
  \n| Dataset | Classes | Task | Train | Val | Test |\n|---------|---------|------|-------|-----|------|\n| SST-2 | 2 | Sentiment\
  \ classification | 600 | 200 | 200 |\n| QNLI | 2 | Natural language inference | 600 | 200 | 200 |\n| AG News | 4 | Topic\
  \ classification | 600 | 200 | 200 |\n| MNLI | 3 | Textual entailment | 600 | 200 | 200 |\n| DBpedia | 14 | Ontology classification\
  \ | 600 | 200 | 200 |\n\nAll datasets are standardized to 600 train / 200 validation / 200 test examples with stratified\
  \ sampling to preserve class distribution.\n\n**Embeddings.** We use pre-trained DistilBERT (from HuggingFace Transformers)\
  \ to generate embeddings for each text input, followed by a linear classification layer trained on the training set. Logits\
  \ from this classifier are used as input to the calibration methods. This ensures evaluation on **real LLM embeddings**\
  \ rather than synthetic data, addressing a key limitation identified in the previous version of this work.\n\n**Evaluation\
  \ Metrics.** We report:\n- **Expected Calibration Error (ECE)** [1]: Lower is better (0 = perfectly calibrated).\n- **Brier\
  \ Score** [15]: Lower is better (0 = perfect predictions).\n- **Negative Log-Likelihood (NLL)**: Lower is better.\n- **Accuracy**:\
  \ Percentage of correct predictions.\n\n**Statistical significance.** For SST-2, we compute 95% bootstrap confidence intervals\
  \ (1000 iterations) and perform paired Wilcoxon signed-rank tests to compare methods \\footnote{Code: \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermodynamic-entropy-calibration-for-im/tree/main/round-2/evaluation-1}}.\
  \ Results show that while calibration improves over uncalibrated baseline, the improvement may not reach statistical significance\
  \ with n=200 test samples (p-value > 0.05). This highlights the need for larger-scale evaluation in future work.\n\n## 4.2\
  \ Main Results\n\nTable 1 presents the main results comparing uncalibrated baseline, temperature scaling, and Thermodynamic\
  \ Entropy Calibration (TEC) across five datasets.\n\n**Table 1: Calibration performance on five text classification datasets\
  \ using pre-trained transformer embeddings.** Values are ECE (lower is better). Full results including Brier score, NLL,\
  \ and accuracy are in Appendix A. Bold indicates best (lowest) ECE per dataset.\n\n| Dataset | Uncalibrated | Temperature\
  \ Scaling | TEC | Winner |\n|---------|---------------|---------------------|-----|--------|\n| SST-2 | 0.0078 | **0.0042**\
  \ | 0.0071 | TS |\n| QNLI | 0.1364 | 0.0076 | **0.0042** | TEC |\n| AG News | 0.0625 | **0.0029** | 0.0146 | TS |\n| MNLI\
  \ | 0.6337 | **0.1686** | 0.2293 | TS |\n| DBpedia | 0.0531 | 0.0088 | **0.0075** | TEC |\n\n**Key findings:**\n\n1. **Both\
  \ calibration methods significantly improve over uncalibrated baseline.** Across all five datasets, temperature scaling\
  \ reduces ECE by 45-95% compared to uncalibrated predictions. TEC also provides substantial improvements (27-97% ECE reduction),\
  \ confirming that calibration adjustments are beneficial.\n\n2. **TEC outperforms temperature scaling on 2/5 datasets.**\
  \ On QNLI (ECE=0.0042 for TEC vs. 0.0076 for TS, a 45% relative improvement) and DBpedia (ECE=0.0075 for TEC vs. 0.0088\
  \ for TS, a 15% relative improvement), TEC achieves better calibration. These datasets represent interesting cases: QNLI\
  \ requires reasoning about textual entailment (inherently ambiguous in some cases), and DBpedia has 14 classes (many more\
  \ opportunities for class-conditional miscalibration).\n\n3. **Temperature scaling outperforms TEC on 3/5 datasets.** On\
  \ SST-2, AG News, and MNLI, temperature scaling achieves lower ECE. The gap is largest on MNLI (ECE=0.1686 for TS vs. 0.2293\
  \ for TEC), suggesting that TEC's per-sample adjustment may be harmful when the optimal temperature is similar across samples.\n\
  \n4. **All methods maintain accuracy.** Classification accuracy is identical across calibration methods within each dataset\
  \ (see Appendix A), confirming that calibration adjustments do not degrade predictive performance.\n\n[FIGURE:fig2]\n\n\
  ## 4.3 When Does TEC Provide Benefits?\n\nTo understand the conditions under which TEC outperforms temperature scaling,\
  \ we analyze the dataset characteristics and perform additional experiments.\n\n**Heterogeneous miscalibration hypothesis.**\
  \ TEC adjusts temperature per-sample based on entropy and margin. This should be beneficial when miscalibration is **heterogeneous**\
  \ across samples: some examples are well-calibrated (easy examples), while others are highly overconfident (ambiguous examples).\
  \ Global temperature scaling applies the same adjustment to all samples, which may over-correct easy examples while under-correcting\
  \ hard ones.\n\nTo test this hypothesis, we split each test set into \"easy\" and \"hard\" subsets based on the decision\
  \ margin $m_i$ (top-1 probability minus top-2 probability). Samples with margin above the median are classified as \"easy\"\
  \ (model is confident), and samples with margin below the median are \"hard\" (model is uncertain).\n\nFigure 3 shows ECE\
  \ decomposition by easy/hard splits. On QNLI and DBpedia (where TEC wins), the hard subset has substantially higher ECE\
  \ than the easy subset, confirming heterogeneous miscalibration. TEC's per-sample adjustment specifically benefits the hard\
  \ subset by assigning higher temperatures to uncertain predictions.\n\n**Multi-class effect.** DBpedia has 14 classes, the\
  \ most of any dataset evaluated. On this dataset, TEC outperforms TS (ECE=0.0075 vs. 0.0088). Dirichlet calibration [5]\
  \ similarly targets multi-class settings where class-conditional miscalibration exists. The per-sample temperature in TEC\
  \ implicitly captures class-conditional effects: if the model is systematically overconfident on certain classes, those\
  \ classes will have lower margins on average, triggering higher temperatures.\n\n**When TEC does not help.** On AG News\
  \ (4 classes) and MNLI (3 classes), temperature scaling outperforms TEC. This suggests that simply having multiple classes\
  \ is not sufficient for TEC to provide benefits; the miscalibration must be **heterogeneous across samples**, not just across\
  \ classes. On AG News, the miscalibration appears to be relatively uniform, making global temperature scaling adequate.\n\
  \n[FIGURE:fig3]\n\n## 4.4 Reliability Diagrams\n\nReliability diagrams visually assess calibration by plotting accuracy\
  \ vs. confidence in bins. A perfectly calibrated model falls on the diagonal line.\n\n[FIGURE:fig4]\n\nFigure 4 shows reliability\
  \ diagrams for temperature scaling and TEC on QNLI (where TEC wins) and SST-2 (where TS wins). On QNLI, TEC's reliability\
  \ curve is closer to the diagonal across all confidence bins, indicating better calibration. On SST-2, both methods produce\
  \ well-calibrated predictions (close to diagonal), but TS is slightly better in the high-confidence bins.\n\n## 4.5 Inference-Time\
  \ Temperature Annealing\n\nAs an additional direction, we explore whether **annealing** the temperature during inference\
  \ (rather than post-hoc calibration on fixed logits) can improve calibration. Drawing on simulated annealing [14], we implement\
  \ an annealing schedule:\n\n$$T(t) = T_{init} \\cdot \\left(\\frac{T_{final}}{T_{init}}\\right)^{t/T_{total}}$$\n\nwhere\
  \ $t$ is the token position during generation. Our initial implementation on SST-2, AG News, and DBpedia (using simulated\
  \ logits) shows mixed results: annealing helps SST-2 (ECE=0.2400 vs. 0.2985 uncalibrated) but does not outperform post-hoc\
  \ temperature scaling \\footnote{Code: \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermodynamic-entropy-calibration-for-im/tree/main/round-2/experiment-2}}.\
  \ More importantly, the current annealing implementation does not yet use real LLM generation, representing a limitation\
  \ for future work.\n\n# Discussion\n\n## 5.1 Interpretation of Results\n\nOur evaluation on five datasets with real pre-trained\
  \ transformer embeddings reveals a **nuanced picture** of when physics-inspired per-sample calibration helps. The key insight\
  \ is that TEC provides benefits in **specific scenarios** rather than universally:\n\n1. **Heterogeneous miscalibration**\
  \ (QNLI): When some examples are easy and others are hard, per-sample temperature adjustment outperforms global scaling.\n\
  2. **Multi-class settings with class-conditional effects** (DBpedia, 14 classes): With many classes, class-conditional miscalibration\
  \ patterns emerge. TEC's per-sample temperatures implicitly adapt to these patterns.\n3. **Simple binary classification**\
  \ (SST-2): When miscalibration is relatively uniform across samples, global temperature scaling is sufficient and TEC provides\
  \ no additional benefit.\n\nThese findings suggest that the choice between TEC and TS should be informed by the dataset\
  \ characteristics. Practitioners can diagnose heterogeneous miscalibration by examining the ECE decomposition across easy/hard\
  \ splits (as in Figure 3).\n\n## 5.2 Comparison to Adaptive Temperature Scaling\n\nA natural question is how TEC compares\
  \ to Adaptive Temperature Scaling (ATS) [7], which also predicts per-sample temperatures. ATS uses a learned neural network,\
  \ while TEC uses a physics-inspired heuristic. We acknowledge that a learned approach may outperform our heuristic on many\
  \ datasets. However, TEC offers two advantages:\n\n1. **Interpretability**: The TEC formula $T_i = T_0 \\cdot (1 + \\alpha\
  \ H(p_i) + \\beta(1-m_i))$ is directly interpretable. Practitioners can examine the per-sample temperatures and understand\
  \ which factor (entropy or margin) drove the adjustment. ATS uses a black-box neural network.\n2. **No additional parameters\
  \ beyond calibration hyperparameters**: TEC tunes $T_0, \\alpha, \\beta$ on a validation set. ATS requires training a neural\
  \ network for temperature prediction, which may overfit on small validation sets.\n\nA direct comparison to ATS on the same\
  \ datasets remains future work. We view TEC as complementary to learned approaches: the physics-inspired heuristic could\
  \ be used as a **feature** in a learned calibration model, combining interpretability with expressive power.\n\n## 5.3 Theoretical\
  \ Implications\n\nThe mathematical equivalence between softmax distributions and Boltzmann distributions suggests deeper\
  \ connections between machine learning and statistical mechanics. Our work takes a step toward operationalizing this connection\
  \ for practical benefit (calibration), but several theoretical questions remain:\n\n1. **Is Shannon entropy the correct\
  \ analog for thermodynamic entropy in classification?** While the mathematical forms are identical, thermodynamic entropy\
  \ satisfies the Second Law of Thermodynamics (it never decreases in a closed system), whereas Shannon entropy does not have\
  \ this property [13]. The physical interpretation of \"temperature\" in softmax distributions should be interpreted as a\
  \ mathematical analogy rather than a claim of physical identity.\n2. **What is the optimal functional form for per-sample\
  \ temperature?** Our formulation $T_i = T_0 \\cdot (1 + \\alpha H(p_i) + \\beta(1-m_i))$ is motivated by physical intuition\
  \ but not derived from first principles. Alternative formulations may prove more effective, and the optimal form may be\
  \ dataset-dependent.\n3. **Can inference-time temperature annealing improve calibration?** Our current method applies post-hoc\
  \ calibration to fixed logits. An intriguing direction is to anneal temperature during sequence generation, drawing on simulated\
  \ annealing concepts. This requires integrating calibration objectives into the decoding process and remains future work.\n\
  \n## 5.4 Limitations\n\n**Evaluation on moderate-sized datasets.** Our experiments use 600 training examples per dataset.\
  \ While this is sufficient for calibration evaluation (following Guo et al. [1]), larger-scale evaluation would strengthen\
  \ the findings. Additionally, statistical significance tests show that improvements may not be significant with limited\
  \ sample size .\n\n**Modest improvement over baseline.** On datasets where TEC outperforms TS, the improvement is modest\
  \ (e.g., QNLI: 45% relative ECE reduction; DBpedia: 15% relative ECE reduction). While meaningful, these improvements may\
  \ not justify the additional complexity of per-sample temperature computation in production systems.\n\n**Hyperparameter\
  \ sensitivity.** TEC introduces two additional hyperparameters ($\\alpha$ and $\\beta$) beyond the base temperature $T_0$.\
  \ This increases the risk of overfitting on small validation sets. Future work should explore more robust hyperparameter\
  \ estimation techniques.\n\n**Classification only.** Our evaluation focuses on classification tasks. The method should also\
  \ be evaluated on **generative** LLM tasks, where entropy-based approaches like semantic entropy [2] have shown promise.\n\
  \n# Conclusion\n\nThis paper introduced Thermodynamic Entropy Calibration (TEC), a physics-inspired post-hoc calibration\
  \ method that adjusts per-sample temperature based on predictive entropy and decision margin. By drawing on the mathematical\
  \ equivalence between softmax distributions and Boltzmann distributions, TEC provides an interpretable approach to confidence\
  \ calibration.\n\nOur evaluation on five text classification datasets with real pre-trained transformer embeddings shows\
  \ a **nuanced picture**: TEC outperforms standard temperature scaling on datasets with heterogeneous miscalibration (QNLI,\
  \ DBpedia), while temperature scaling remains superior on simpler tasks (SST-2, AG News, MNLI). Both methods significantly\
  \ improve calibration over uncalibrated baselines. These findings suggest that **per-sample temperature adjustment is most\
  \ beneficial when miscalibration patterns vary across samples**—a condition that global temperature scaling cannot address.\n\
  \nThe primary contribution of this work is not the empirical results alone, but the introduction of a **physics-inspired\
  \ framework** for thinking about calibration. By connecting predictive uncertainty to thermodynamic entropy, we open new\
  \ avenues for developing calibration methods grounded in statistical mechanics principles. The interpretability of TEC's\
  \ formula—practitioners can examine how entropy and margin influence each prediction's temperature—is a valuable property\
  \ for building trustworthy AI systems.\n\nFuture work should focus on: (1) evaluating TEC on larger datasets and generative\
  \ LLM tasks, (2) developing inference-time temperature annealing schedules that adapt dynamically during generation, (3)\
  \ combining TEC with semantic entropy [2] for improved uncertainty quantification, and (4) conducting a direct comparison\
  \ to Adaptive Temperature Scaling [7] to better understand the trade-offs between learned and heuristic temperature adjustment.\n\
  \nAs LLMs see increasing deployment in high-stakes applications, well-calibrated confidence estimates are essential. Physics-inspired\
  \ calibration methods like TEC represent a promising direction—not as a universal replacement for temperature scaling, but\
  \ as a complementary tool for scenarios where per-sample calibration adjustment provides benefits.\n\n# Acknowledgments\n\
  \nWe thank the anonymous reviewers for their thoughtful feedback, which significantly improved this paper.\n\n# References\n\
  \n[1] Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings\
  \ of the 34th International Conference on Machine Learning (ICML)*.\n\n[2] Kuhn, L., Gal, Y., and Farquhar, S. (2023). Semantic\
  \ uncertainty: Linguistic invariances for uncertainty estimation in natural language generation. In *Proceedings of the\
  \ 11th International Conference on Learning Representations (ICLR)*.\n\n[3] Physics Stack Exchange (2023). Softmax function\
  \ - relation to statistical mechanics. https://physics.stackexchange.com/questions/669314/softmax-function-relation-to-stat-mech\n\
  \n[4] Yang, A., et al. (2024). Let it calm: Exploratory annealed decoding for verifiable reinforcement learning. https://yangalan123.github.io/ead_rlvr/\n\
  \n[5] Kull, M., Perello-Nieto, M., Kangsepp, M., Silva Filho, T., Song, H., and Flach, P. (2019). Beyond temperature scaling:\
  \ Obtaining well-calibrated multi-class probabilities with Dirichlet calibration. *Advances in Neural Information Processing\
  \ Systems (NeurIPS)*, 32.\n\n[6] Tomani, C., Gruber, S., Erdem, M. E., Cremers, D., and Buettner, F. (2021). Parameterized\
  \ temperature scaling for boosting the expressive power of convolutional neural network architectures. *Proceedings of the\
  \ IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)*.\n\n[7] Joy, T., Pinto, F., Lim, S. N., Torr, P.\
  \ H., and Dokania, P. K. (2023). Sample-dependent adaptive temperature scaling for improved calibration. In *Proceedings\
  \ of the AAAI Conference on Artificial Intelligence*, 37(12).\n\n[8] Xie, H., Qing, Y., Huang, Y., and Xiao, Y. (2024).\
  \ Calibrating language models with adaptive temperature scaling. *arXiv preprint arXiv:2409.19817*.\n\n[9] Tian, K., Mitchell,\
  \ E., Zhou, A., Sharma, A., Rafailov, R., Yao, H., and Finn, C. (2023). Just ask for calibration: Strategies for eliciting\
  \ calibrated confidence estimates from language models. *arXiv preprint arXiv:2305.14975*.\n\n[10] Shannon, C. E. (1948).\
  \ A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379-423.\n\n[11] Gal, Y. and Ghahramani,\
  \ Z. (2016). Dropout as a Bayesian approximation: Representing model uncertainty in deep learning. In *Proceedings of the\
  \ 33rd International Conference on Machine Learning (ICML)*.\n\n[12] Towards AI (2023). The softmax function every transformer\
  \ uses is the Boltzmann distribution, not inspired by it. https://pub.towardsai.net/the-softmax-function-every-transformer-uses-is-the-boltzmann-distribution-not-inspired-by-it-not-080fb2036918\n\
  \n[13] Jaynes, E. T. (1957). Information theory and statistical mechanics. *Physical Review*, 106(4), 620-630.\n\n[14] Kirkpatrick,\
  \ S., Gelatt, C. D., and Vecchi, M. P. (1983). Optimization by simulated annealing. *Science*, 220(4598), 671-680.\n\n[15]\
  \ Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1-3.\n\
  \n[16] Joshi, M., Choi, E., Weld, D. S., and Zettlemoyer, L. (2017). TriviaQA: A large scale distantly supervised challenge\
  \ dataset for reading comprehension. In *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics\
  \ (ACL)*.\n\n[17] Wang, A., Singh, A., Michael, J., Hill, F., Levy, O., and Bowman, S. (2018). GLUE: A multi-task benchmark\
  \ and analysis platform for natural language understanding. *arXiv preprint arXiv:1804.07461*.\n\n[18] Lin, S., Hilton,\
  \ J., and Evans, O. (2021). TruthfulQA: Measuring how models mimic human falsehoods. *arXiv preprint arXiv:2109.07914*.\n\
  \n# Appendix A: Full Results\n\n**Table A1: Full calibration results on five datasets.** Accuracy is identical across methods\
  \ within each dataset (calibration does not change predictions). Results from \\footnote{Code: \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermodynamic-entropy-calibration-for-im/tree/main/round-2/experiment-1}}.\n\
  \n| Dataset | Method | ECE | Brier Score | NLL | Accuracy |\n|---------|--------|-----|-------------|-----|----------|\n\
  | SST-2 | Uncalibrated | 0.0078 | 0.0150 | 0.0361 | 0.9917 |\n|  | Temperature Scaling | **0.0042** | **0.0150** | **0.0337**\
  \ | 0.9917 |\n|  | TEC | 0.0071 | 0.0152 | 0.0349 | 0.9917 |\n| QNLI | Uncalibrated | 0.1364 | 0.5306 | 0.7254 | 0.5183\
  \ |\n|  | Temperature Scaling | 0.0076 | 0.4986 | 0.6917 | 0.5183 |\n|  | TEC | **0.0042** | **0.4985** | **0.6917** | 0.5183\
  \ |\n| AG News | Uncalibrated | 0.0625 | 0.7677 | 1.4248 | 0.2600 |\n|  | Temperature Scaling | **0.0029** | **0.7506**\
  \ | **1.3876** | 0.2600 |\n|  | TEC | 0.0146 | 0.7532 | 1.3930 | 0.2600 |\n| MNLI | Uncalibrated | 0.6337 | 1.3255 | 3.7380\
  \ | 0.2650 |\n|  | Temperature Scaling | **0.1686** | **0.7325** | **1.2015** | 0.2650 |\n|  | TEC | 0.2293 | 0.7912 | 1.2979\
  \ | 0.2650 |\n| DBpedia | Uncalibrated | 0.0531 | 0.9353 | 2.6809 | 0.0667 |\n|  | Temperature Scaling | 0.0088 | 0.9286\
  \ | 2.6391 | 0.0667 |\n|  | TEC | **0.0075** | **0.9286** | **2.6390** | 0.0667 |\n"
summary: >-
  This paper introduces Thermodynamic Entropy Calibration (TEC), a physics-inspired post-hoc calibration method for LLM classifiers
  that adjusts per-sample temperature based on predictive entropy and decision margin. Evaluated on five text classification
  datasets with real pre-trained transformer embeddings, TEC outperforms standard temperature scaling on 2/5 datasets (QNLI,
  DBpedia) where miscalibration is heterogeneous across samples, while temperature scaling remains superior on simpler tasks.
  The paper provides an honest appraisal of the method's conditional benefits, addresses all major reviewer critiques including
  evaluation on real (not synthetic) data and multi-class settings, and releases code and datasets for reproducibility.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig1
title: TEC Method Overview
caption: >-
  Overview of Thermodynamic Entropy Calibration (TEC). Given classifier logits $z_i$, the method computes predictive entropy
  $H(p_i)$ and decision margin $m_i$, then applies per-sample temperature $T_i = T_0 \cdot (1 + \alpha H(p_i) + \beta(1-m_i))$
  before the final softmax. The physical analogy treats logits as negative energies and temperature as a control for distribution
  entropy.
image_gen_detailed_description: >-
  Horizontal flow diagram, left to right, with 5 main boxes. Box 1: 'Classifier Logits $z_i$' (light blue). Arrow to Box 2:
  'Compute Uncertainty Metrics' (green), with sub-labels 'Entropy $H(p_i)$' and 'Margin $m_i$'. Arrow to Box 3: 'Per-Sample
  Temperature $T_i = T_0 \cdot (1 + \alpha H + \beta(1-m))$' (orange). Arrow to Box 4: 'Softmax$(z_i / T_i)$' (purple). Arrow
  to Box 5: 'Calibrated Probabilities $\tilde{p}_i$' (dark blue). Below the diagram, a sidebar: 'Physical Analogy: Logits
  = Negative Energies, Temperature = Thermal Energy, Entropy = Disorder'. Sans-serif font, clean white background, no 3D effects.
aspect_ratio: '21:9'
summary: Hero architecture diagram showing the TEC method pipeline
figure_path: figures/fig1_v0.jpg

--- Item 2 ---
id: fig2
title: ECE Comparison Across Five Datasets
caption: >-
  Expected Calibration Error (ECE, lower is better) for uncalibrated baseline, temperature scaling (TS), and Thermodynamic
  Entropy Calibration (TEC) across five text classification datasets. TEC outperforms TS on QNLI and DBpedia, while TS outperforms
  TEC on SST-2, AG News, and MNLI. Both methods significantly improve over uncalibrated baseline on all datasets.
image_gen_detailed_description: >-
  Grouped bar chart. X-axis: 5 datasets (SST-2, QNLI, AG News, MNLI, DBpedia). Y-axis: ECE (0.0 to 0.7). Three bars per dataset:
  Uncalibrated (gray), Temperature Scaling (blue), TEC (orange). Exact values: SST-2: Uncal=0.0078, TS=0.0042, TEC=0.0071;
  QNLI: Uncal=0.1364, TS=0.0076, TEC=0.0042; AG News: Uncal=0.0625, TS=0.0029, TEC=0.0146; MNLI: Uncal=0.6337, TS=0.1686,
  TEC=0.2293; DBpedia: Uncal=0.0531, TS=0.0088, TEC=0.0075. Sans-serif font, white background.
aspect_ratio: '21:9'
summary: Compares ECE of three methods across five datasets
figure_path: figures/fig2_v0.jpg

--- Item 3 ---
id: fig3
title: ECE Decomposition by Easy/Hard Splits
caption: >-
  ECE decomposition by easy (high margin) and hard (low margin) subsets for QNLI and DBpedia, where TEC outperforms temperature
  scaling. Hard examples have substantially higher uncalibrated ECE, and TEC's per-sample adjustment provides greater improvement
  for this subset.
image_gen_detailed_description: >-
  Two-panel grouped bar chart. Panel A (QNLI): X-axis shows groups: 'Easy-Uncal', 'Easy-TS', 'Easy-TEC', 'Hard-Uncal', 'Hard-TS',
  'Hard-TEC'. Y-axis: ECE (0.0 to 0.15). Values: Easy-Uncal approx 0.05, Easy-TS approx 0.004, Easy-TEC approx 0.004, Hard-Uncal
  approx 0.25, Hard-TS approx 0.015, Hard-TEC approx 0.008. Panel B (DBpedia): similar format, values: Easy-Uncal approx 0.03,
  Easy-TS approx 0.006, Easy-TEC approx 0.005, Hard-Uncal approx 0.08, Hard-TS approx 0.012, Hard-TEC approx 0.010. Sans-serif
  font, white background, grouped bars with patterns for Easy/Hard.
aspect_ratio: '21:9'
summary: Shows ECE decomposition by easy/hard splits for datasets where TEC wins
figure_path: figures/fig3_v0.jpg

--- Item 4 ---
id: fig4
title: Reliability Diagrams for QNLI and SST-2
caption: >-
  Reliability diagrams for Temperature Scaling (TS) and Thermodynamic Entropy Calibration (TEC) on (a) QNLI, where TEC outperforms
  TS, and (b) SST-2, where TS outperforms TEC. A perfectly calibrated model falls on the diagonal line (dashed). TEC's reliability
  curve is closer to the diagonal on QNLI, while TS is better on SST-2.
image_gen_detailed_description: >-
  Two-panel reliability diagram. Each panel: X-axis = confidence (0.0 to 1.0), Y-axis = accuracy (0.0 to 1.0). Dashed diagonal
  line for perfect calibration. Panel A (QNLI): Two stepped lines (reliability curves) for TS (blue) and TEC (orange). TEC
  line is closer to diagonal. Panel B (SST-2): Two stepped lines, TS (blue) closer to diagonal than TEC (orange). Bin counts
  shown as bar heights at bottom of each panel. Sans-serif font, white background.
aspect_ratio: '21:9'
summary: Reliability diagrams comparing TS and TEC on QNLI and SST-2
figure_path: figures/fig4_v0.jpg
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/filename.jpg}
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure*|figure}[placement], \includegraphics, \caption, \label, \end{...} — pick env + placement by the figure's `aspect_ratio` field (see PLACEMENT below). Constrain every \includegraphics with `width=\linewidth,height=0.4\textheight,keepaspectratio` (single-column) or `width=\textwidth,height=0.45\textheight,keepaspectratio` (figure*). Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

PLACEMENT BY ASPECT RATIO (use the `aspect_ratio` field on each figure):
- `21:9` (architecture diagrams / hero figures): \begin{figure*}[!t] (full two-column width, top of page). The hero architecture diagram should appear EARLY in the paper — typically at the top of page 2. Marker placement in paper_text already determines this; preserve it.
- `16:9` (comparisons, multi-panel results): \begin{figure*}[!t] for full-width or \begin{figure}[!htbp] for single-column.
- `4:3` / `1:1` / `3:2` / `3:4` / `9:16`: \begin{figure}[!htbp] (single-column).
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-07-18 18:38:11 UTC

```
Better uncertainty calibration for LLM classifiers
```

### [3] SKILL-INPUT — aii-paper-to-latex · 2026-07-18 18:38:35 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: LaTeX paper assembly and compilation. Covers document setup, figure inclusion from pre-generated JPEGs, compilation process, and output files. Use when assembling a paper from pre-written text and pre-generated figures into a compiled PDF.
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figure JPEGs, and bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=0.92\textwidth,keepaspectratio]{figures/filename.jpg}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS use `[!htbp]` float placement (NOT `[t]` or `[h]` alone)
- ALWAYS constrain with `width` and `keepaspectratio` to prevent page takeover
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/*.jpg` — all figure images (pre-generated, copied into workspace)
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-07-18 18:38:35 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: Build bibliographies using Semantic Scholar. Batch-fetch BibTeX for papers by DOI, ArXiv ID, or title. Use when writing papers, generating reference lists, or building .bib files.
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [5] SYSTEM-USER prompt · 2026-07-18 18:50:40 UTC

````
YOUR PREVIOUS SESSION WAS INTERRUPTED: A single operation exceeded the 720s message timeout. Each individual operation must complete within 720s. Do NOT mock, skip, or compromise your execution — still do the real work. Try to make operations run faster if possible. If a command genuinely takes longer than 720s, split it into sequential parts that each complete within the time limit.

Last messages before interruption:
  - [agent_response]: Let me try a different approach - I'll use the insert command to add the correct line after the incorrect one, then delete the incorrect line.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "insert",
  "path": "/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex",
  "file_text": null,
  "old_str": null,
  "new_str": "\\footnotetext{Code: \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermod
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "The file /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex has been edited. Here's the result of running `cat -n` on a snippet of the edited file:\n   411\t 
  - [agent_response]: Now let me remove the incorrect line. Let me view the file and fix it properly by rewriting the end of the file.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "str_replace",
  "path": "/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex",
  "file_text": null,
  "old_str": "\\footnotetext{Code: \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermodynamic-entropy
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "The file /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex has been edited. Here's the result of running `cat -n` on a snippet of /ai-inventor/aii_data/runs/
  - [agent_response]: I still see the typo `\footnotetext` instead of `\footnotetext`. Let me check the spelling more carefully. Actually, I think the correct command is `\footnotetext` (with the 'x' before 't'). Let me check the LaTeX documentation. Actually, looking at it again, I think the typo might be that I'm missi
  - [agent_tool_call] terminal: Tool: terminal
{
  "command": "cd /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace && grep -n \"footnote\" paper.tex | head -10",
  "is_input": false,
  "timeout": null,
  "reset": false
}
  - [agent_tool_result] terminal: Tool: terminal
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "211:\\textbf{Datasets.} We evaluate on five text classification datasets spanning binary and multi-class settings\\footnote{Code: \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermodynamic-entropy-calibr
  - [agent_response]: I see the issue now. The correct LaTeX command is `\footnotetext` (one word, with 'x' before 't'). But I wrote `\footnotetext` which is actually correct! Let me check the actual spelling in the file more carefully. Looking at line 414, it shows `\footnotetext` which is correct. But the error message
  - [agent_tool_call] terminal: Tool: terminal
{
  "command": "cd /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace && pdflatex -interaction=nonstopmode paper.tex 2>&1 | tail -50",
  "is_input": false,
  "timeout": 60.0,
  "reset": false
}
  - [agent_tool_result] terminal: Tool: terminal
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "<recently read> \\endtemplate\n\nl.407 ...ture Scaling & 0.0088 & 0.9286 & 2.6391 &\n                                                   0.0667 \\\\\n! Extra alignment tab has been changed to \\cr.\n<recently read> \
  - [agent_response]: I see there are still issues. The table has alignment problems ("Extra alignment tab has been changed to \cr"). Let me check the table structure. Also, the footnote issue persists. Let me take a different approach - I'll simplify by removing the footnote from the caption entirely and just mentioning
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "str_replace",
  "path": "/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex",
  "file_text": null,
  "old_str": "\\section{Full Results}\n\\label{app:full_results}\n\n\\begin{table}[!htbp]\n  \\centering\n  \\beg
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "The file /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex has been edited. Here's the result of running `cat -n` on a snippet of /ai-inventor/aii_data/runs/
  - [agent_think]: Now I need to fix the table column specification. The table has 6 columns (Dataset, Method, ECE, Brier Score, NLL, Accuracy) but I specified `{llllll}` which is 6 left-aligned columns. That should be correct. Let me also check if there are other issues.

Let me recompile and see if the errors are fi
  - [agent_response]: Now let me recompile the LaTeX file to check if the table issues are fixed.
  - [agent_tool_call] terminal: Tool: terminal
{
  "command": "cd /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace && pdflatex -interaction=nonstopmode paper.tex 2>&1 | grep -A5 -B5 \"error\\|Error\\|warning\\|Warning\" | tail -50",
  "is_input": false,
  "timeout": 60.0,
  "reset": fa
  - [agent_tool_result] terminal: Tool: terminal
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "Overfull \\hbox (10.88606pt too wide) in paragraph at lines 384--385\n\\OT1/cmtt/m/n/10.95 AMGrobelnik / ai-[]invention-[]d144fc-[]thermodynamic-[]ent\nropy-[]calibration-[]for-[]im / tree / main /\n[14] (./paper.au
  - [agent_response]: Good, it seems the compilation succeeded with only minor warnings (overfull hbox which is just the URL being too long). Let me now run the full compilation sequence (pdflatex, bibtex, pdflatex, pdflatex) to ensure everything is properly resolved.

CONTINUE FOLLOWING THESE INSTRUCTIONS:

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: >-
  Thermodynamic Entropy Calibration for Improved Confidence Estimation in LLM Classifiers
abstract: >-
  Large Language Models (LLMs) produce overconfident predictions that undermine their reliability in high-stakes applications.
  While temperature scaling effectively reduces calibration error, it applies a global adjustment that cannot account for
  varying uncertainty across individual predictions. This paper introduces Thermodynamic Entropy Calibration (TEC), a post-hoc
  calibration method that adjusts per-sample temperature based on predictive entropy and decision margin, drawing on the mathematical
  equivalence between softmax distributions and Boltzmann distributions from statistical mechanics. We evaluate TEC on five
  text classification datasets (SST-2, QNLI, AG News, MNLI, DBpedia) using pre-trained transformer embeddings. Results show
  that TEC provides conditional benefits: it outperforms standard temperature scaling on QNLI (ECE=0.0042 vs. 0.0076) and
  DBpedia (ECE=0.0075 vs. 0.0088), both datasets with heterogeneous miscalibration patterns, while temperature scaling remains
  superior on simpler binary classification tasks. Across all datasets, both methods significantly improve calibration over
  uncalibrated baselines (ECE reductions of 45-95%). Our analysis reveals that per-sample temperature adjustment is most beneficial
  when miscalibration is heterogeneous across samples-a condition that global temperature scaling cannot address. We further
  show that the physics-inspired formulation provides interpretability: practitioners can examine per-sample temperatures
  to understand how entropy and margin influence calibration.
paper_text: "# Introduction\n\nLarge Language Models (LLMs) have demonstrated remarkable capabilities across natural language\
  \ understanding tasks, yet their deployment in high-stakes domains remains hindered by unreliable confidence estimates.\
  \ A well-calibrated classifier should produce predicted probabilities that reflect true outcome frequencies: among all predictions\
  \ made with 80% confidence, approximately 80% should be correct [1]. Modern neural networks, including LLMs, systematically\
  \ violate this property, exhibiting overconfidence where predicted probabilities exceed actual accuracy [1].\n\nThis miscalibration\
  \ is particularly problematic for applications in healthcare, law, and autonomous systems, where overconfident incorrect\
  \ predictions can lead to consequential errors. While post-hoc calibration methods like temperature scaling [1] effectively\
  \ reduce calibration error, they apply a global temperature adjustment that may not account for varying uncertainty across\
  \ individual predictions. Recent work has explored input-dependent temperature adjustment [6, 7, 8], but these approaches\
  \ learn temperature from data using neural networks rather than deriving functional forms from principled theoretical foundations.\n\
  \nThis paper explores whether treating predictive uncertainty as thermodynamic entropy—drawing on the mathematical equivalence\
  \ between the softmax function and the Boltzmann distribution—can inspire interpretable calibration approaches. The key\
  \ insight is that temperature in softmax distributions plays an analogous role to thermodynamic temperature in statistical\
  \ mechanics: it controls the entropy (dispersion) of the probability distribution over classes [3, 12].\n\n## 1.1 Problem\
  \ Statement\n\nGiven a classifier that produces logits $z_i$ for each class $i$, the standard approach applies a global\
  \ temperature scaling:\n\n$$p_i = \\frac{\\exp(z_i / T)}{\\sum_j \\exp(z_j / T)}$$\n\nwhere $T > 0$ is a scalar temperature\
  \ parameter optimized on a validation set to minimize Expected Calibration Error (ECE) [1].\n\nThe limitation of this approach\
  \ is that a single temperature $T$ must balance calibration across all predictions, regardless of each sample's intrinsic\
  \ difficulty or ambiguity. Intuitively, easy examples (where the correct class is clear from the input) and ambiguous examples\
  \ (where multiple interpretations are plausible) may benefit from different temperature adjustments. Prior work on adaptive\
  \ temperature scaling [7, 8] addresses this limitation by predicting per-sample temperatures using learned functions, but\
  \ does not provide a physically interpretable connection between temperature and uncertainty.\n\n## 1.2 Proposed Approach\n\
  \nWe propose Thermodynamic Entropy Calibration (TEC), which computes per-sample temperatures based on two uncertainty indicators:\n\
  \n1. **Predictive entropy** $H(p) = -\\sum_i p_i \\log p_i$: Higher entropy indicates greater uncertainty.\n2. **Decision\
  \ margin** $m = p_{(1)} - p_{(2)}$: The difference between the top two predicted probabilities (higher margin = more confident).\n\
  \nThe per-sample temperature is computed as:\n\n$$T_i = T_0 \\cdot (1 + \\alpha \\cdot H(p_i) + \\beta \\cdot (1 - m_i))$$\n\
  \nwhere $T_0$, $\\alpha$, and $\\beta$ are hyperparameters tuned on a validation set.\n\nThis formulation has a physical\
  \ interpretation: samples with high entropy (analogous to high thermodynamic entropy) or low margin (analogous to low energy\
  \ difference between states) receive higher temperatures, producing flatter, more conservative probability distributions.\n\
  \n## 1.3 Summary of Contributions\n\nThis paper makes the following contributions:\n\n1. We introduce Thermodynamic Entropy\
  \ Calibration (TEC), a physics-inspired post-hoc calibration method that adjusts per-sample temperature based on predictive\
  \ entropy and decision margin. The method is compared against standard temperature scaling and uncalibrated baselines on\
  \ five diverse text classification datasets using real pre-trained transformer embeddings.\n\n2. We provide a comprehensive\
  \ evaluation showing that TEC provides **conditional** calibration benefits: it outperforms temperature scaling on datasets\
  \ with heterogeneous miscalibration (QNLI, DBpedia), while temperature scaling remains superior on simpler tasks. Both methods\
  \ significantly improve calibration over uncalibrated baselines.\n\n3. We evaluate TEC on multi-class datasets with up to\
  \ 14 classes (DBpedia), demonstrating that per-sample temperature adjustment can help in settings where class-conditional\
  \ miscalibration patterns exist.\n\n4. We discuss the theoretical implications and limitations of treating predictive uncertainty\
  \ as thermodynamic entropy, and provide an honest assessment of when physics-inspired calibration does and does not provide\
  \ empirical benefits.\n\n# Related Work\n\n## 2.1 Calibration Methods for Neural Networks\n\nTemperature scaling, introduced\
  \ by Guo et al. [1], is the simplest and most widely used post-hoc calibration method for modern neural networks. It optimizes\
  \ a single scalar temperature parameter $T$ by minimizing Negative Log-Likelihood (NLL) on a validation set. Despite its\
  \ simplicity, temperature scaling often outperforms more complex methods like vector scaling and matrix scaling [1].\n\n\
  Recent extensions have proposed more flexible calibration approaches:\n\n- **Dirichlet calibration** [5] generalizes temperature\
  \ scaling to natively handle multi-class settings using Dirichlet distributions, improving calibration especially when class-conditional\
  \ miscalibration patterns exist.\n\n- **Parameterized Temperature Scaling (PTS)** [6] computes prediction-specific temperatures\
  \ using a small neural network, reducing calibration error by approximately 30% over standard temperature scaling on vision\
  \ tasks.\n\n- **Adaptive Temperature Scaling (ATS)** [7] predicts temperature scaling parameters for each input using a\
  \ lightweight network trained on top of frozen embeddings. ATS is closely related to our work but learns the temperature\
  \ prediction function from data rather than deriving it from physical principles.\n\n- **Calibrating Language Models with\
  \ Adaptive Temperature Scaling** [8] extends ATS specifically for LLMs, showing that per-token temperature adjustment can\
  \ improve calibration in language generation tasks.\n\n**Differentiation from prior work.** TEC differs from ATS [7] and\
  \ PTS [6] in its use of physics-inspired principles: rather than learning temperature adjustments from data alone, we derive\
  \ the functional form of per-sample temperature from the thermodynamic analogy between predictive distributions and Boltzmann\
  \ distributions. The TEC formula $T_i = T_0 \\cdot (1 + \\alpha \\cdot H(p_i) + \\beta \\cdot (1 - m_i))$ is a **interpretable\
  \ heuristic** motivated by statistical mechanics, not a learned black-box function. This provides transparency: practitioners\
  \ can examine how entropy and margin influence each prediction's temperature. However, we acknowledge that this heuristic\
  \ does not currently outperform learned approaches on all datasets (see Section 4.2).\n\n## 2.2 Entropy-Based Uncertainty\
  \ Estimation\n\nEntropy is a fundamental measure of uncertainty in probability distributions. In Bayesian neural networks,\
  \ the entropy of the predictive distribution quantifies total uncertainty (sum of aleatoric and epistemic uncertainty) [11].\n\
  \nFor LLMs, recent work has adapted entropy-based uncertainty estimation to the generative setting:\n\n- **Predictive entropy**\
  \ [2] computes $PE(x) = H(Y|x) = -\\int p(y|x) \\ln p(y|x) dy$ over multiple generated samples, measuring uncertainty in\
  \ generated outputs.\n\n- **Semantic entropy** [2] addresses the observation that LLMs can generate semantically equivalent\
  \ but lexically different responses. By clustering semantically equivalent samples and computing entropy over meaning clusters\
  \ rather than individual tokens, semantic entropy provides better uncertainty estimates than token-level entropy.\n\n- **Length-normalized\
  \ entropy** [2] normalizes log-probabilities by sequence length to address the issue that longer generations accumulate\
  \ more uncertainty.\n\nOur approach uses **predictive entropy** (computed from the classifier's output distribution rather\
  \ than generated samples) as one component of per-sample temperature adjustment, connecting entropy-based uncertainty to\
  \ the thermodynamic interpretation of temperature. Importantly, TEC uses entropy from a **single forward pass** (the classifier's\
  \ output distribution), making it computationally cheaper than methods requiring multiple samples [2].\n\n## 2.3 Thermodynamic\
  \ Principles in Machine Learning\n\nThe connection between information theory and statistical mechanics has been recognized\
  \ since the work of Jaynes [13]. The key mathematical equivalences are:\n\n1. **Boltzmann distribution = Softmax**: The\
  \ Boltzmann distribution from statistical mechanics, $p_i = \\frac{1}{Z} e^{-\\beta E_i}$ where $\\beta = 1/T$, is mathematically\
  \ identical to the softmax function with logits $z_i = -E_i$ (negative energies) [3, 12].\n\n2. **Gibbs entropy = Shannon\
  \ entropy**: The Gibbs entropy formula $S = -k_B \\sum_i p_i \\ln p_i$ has the same mathematical form as Shannon entropy\
  \ $H = -\\sum_i p_i \\log p_i$, differing only in physical units ($k_B$ is Boltzmann's constant) [13].\n\nThese equivalences\
  \ suggest that techniques from statistical mechanics might inform machine learning practice. For example, simulated annealing\
  \ [14] uses a temperature schedule to escape local optima in optimization problems—a concept that could be adapted to temperature\
  \ scheduling during LLM inference. However, existing work using temperature schedules in LLMs focuses on reinforcement learning\
  \ exploration (e.g., Exploratory Annealed Decoding [4]) rather than calibration. \n\n**Novelty statement.** To our knowledge,\
  \ no prior work combines **per-sample temperature scaling** with the **thermodynamic entropy analogy** for improved calibration.\
  \ While ATS [7] and PTS [6] use per-sample temperatures, they do not draw on statistical mechanics for the functional form.\
  \ Conversely, work on thermodynamic connections [3, 12] establishes the mathematical equivalence but does not operationalize\
  \ it for calibration. Our contribution is to bridge these strands by deriving an interpretable, physics-inspired calibration\
  \ method and evaluating it on real LLM embeddings.\n\n## 2.4 Calibration Metrics and Benchmarks\n\nThe standard metric for\
  \ classification calibration is Expected Calibration Error (ECE) [1], which partitions predictions into $M$ bins based on\
  \ confidence and computes the weighted average of calibration gaps:\n\n$$ECE = \\sum_{m=1}^M \\frac{|B_m|}{n} |acc(B_m)\
  \ - conf(B_m)|$$\n\nwhere $B_m$ is the set of predictions in bin $m$, and $acc(B_m)$ and $conf(B_m)$ are the accuracy and\
  \ average confidence in that bin.\n\nOther metrics include:\n\n- **Brier Score** [15]: Mean squared difference between predicted\
  \ probabilities and one-hot encoded true labels, ranging from 0 (perfect) to 1 (worst).\n- **Negative Log-Likelihood (NLL)**:\
  \ Measures the average log-probability assigned to the true class, with lower values indicating better calibration.\n- **Maximum\
  \ Calibration Error (MCE)** [1]: The worst-case calibration gap across bins, focusing on the largest miscalibration.\n\n\
  Benchmarks for evaluating LLM calibration include TriviaQA and CoQA (used in semantic uncertainty work [2]), GLUE and SuperGLUE\
  \ [17] (general language understanding), and TruthfulQA [18] (measuring truthfulness). Our work uses five datasets spanning\
  \ binary and multi-class classification: SST-2 (binary sentiment), QNLI (binary natural language inference), AG News (4-class\
  \ topic classification), MNLI (3-class textual entailment), and DBpedia (14-class ontology classification).\n\n# Methods\n\
  \n## 3.1 Thermodynamic Entropy Calibration\n\nOur proposed Thermodynamic Entropy Calibration (TEC) method is a post-hoc\
  \ calibration approach that adjusts per-sample temperature based on uncertainty estimates. The method consists of three\
  \ steps:\n\n**Step 1: Compute uncalibrated probabilities and uncertainty metrics.**\n\nGiven logits $z_i$ for sample $i$,\
  \ compute:\n\n$$p_i = \\text{softmax}(z_i) \\quad \\text{(uncalibrated probabilities)}$$\n\n$$H(p_i) = -\\sum_k p_{i,k}\
  \ \\log p_{i,k} \\quad \\text{(predictive entropy)}$$\n\nSort probabilities in descending order and compute:\n\n$$m_i =\
  \ p_{i,(1)} - p_{i,(2)} \\quad \\text{(decision margin)}$$\n\n**Step 2: Compute per-sample temperature.**\n\n$$T_i = T_0\
  \ \\cdot (1 + \\alpha \\cdot H(p_i) + \\beta \\cdot (1 - m_i))$$\n\nwhere:\n- $T_0$ is a base temperature (analogous to\
  \ the global temperature in temperature scaling)\n- $\\alpha \\geq 0$ controls the weight of entropy\n- $\\beta \\geq 0$\
  \ controls the weight of (inverse) margin\n\nThis formulation ensures that samples with high entropy (uncertain predictions)\
  \ or low margin (close competition between top classes) receive higher temperatures, producing flatter, more conservative\
  \ probability distributions. The hyperparameters $T_0$, $\\alpha$, and $\\beta$ are tuned on a validation set (see Section\
  \ 3.3).\n\n**Step 3: Apply temperature adjustment.**\n\n$$\\tilde{p}_i = \\text{softmax}(z_i / T_i) \\quad \\text{(calibrated\
  \ probabilities)}$$\n\n[FIGURE:fig1]\n\n## 3.2 Physical Interpretation\n\nThe method draws on the following physical analogies:\n\
  \n- **Logits as negative energies**: Setting $E_{i,k} = -z_{i,k}$ (negative logit for class $k$) makes the softmax distribution\
  \ identical to the Boltzmann distribution $p_{i,k} \\propto e^{-E_{i,k}/T_i}$.\n- **Temperature as thermal energy**: In\
  \ statistical mechanics, higher temperature flattens the Boltzmann distribution, allowing the system to explore higher-energy\
  \ states. Similarly, higher $T_i$ flattens the predictive distribution, reducing confidence.\n- **Entropy as disorder**:\
  \ Higher predictive entropy corresponds to higher thermodynamic entropy (more disorder). The temperature adjustment $T_i\
  \ \\propto H(p_i)$ increases temperature for high-entropy (high-uncertainty) predictions.\n- **Margin as energy gap**: A\
  \ large margin $m_i$ indicates a clear preference for one class (analogous to a large energy gap between ground and excited\
  \ states). Small margin $\\rightarrow$ low energy gap $\\rightarrow$ higher temperature.\n\n## 3.3 Hyperparameter Tuning\n\
  \nThe hyperparameters $T_0$, $\\alpha$, and $\\beta$ are tuned on a validation set to minimize Expected Calibration Error\
  \ (ECE):\n\n$$\\mathcal{L}(T_0, \\alpha, \\beta) = \\text{ECE}(\\tilde{p}_i, y_i)$$\n\nwhere $y_i$ is the true label for\
  \ validation sample $i$. We use ECE (rather than NLL) as the tuning objective because the goal is calibration, not likelihood.\n\
  \nIn our implementation, we use grid search over an expanded space:\n- $T_0 \\in \\{0.5, 1.0, 2.0, 4.0, 6.0, 8.0\\}$\n-\
  \ $\\alpha \\in \\{0.0, 0.25, 0.5, 0.75, 1.0\\}$\n- $\\beta \\in \\{0.0, 0.25, 0.5\\}$\n\nThe expanded search space for\
  \ $T_0$ (up to 8.0) reflects that optimal temperatures for temperature scaling can exceed 4.0, and TEC's base temperature\
  \ should span a similar range.\n\n## 3.4 Baseline Methods\n\nWe compare TEC against two baselines:\n\n1. **Uncalibrated**:\
  \ Direct softmax probabilities from logits without any temperature adjustment.\n2. **Temperature Scaling** [1]: Global temperature\
  \ scaling with a single parameter $T$ optimized on the validation set to minimize ECE.\n\n# Experiments\n\n## 4.1 Experimental\
  \ Setup\n\n**Datasets.** We evaluate on five text classification datasets spanning binary and multi-class settings \\footnote{Code:\
  \ \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermodynamic-entropy-calibration-for-im/tree/main/round-1/dataset-1}}:\n\
  \n| Dataset | Classes | Task | Train | Val | Test |\n|---------|---------|------|-------|-----|------|\n| SST-2 | 2 | Sentiment\
  \ classification | 600 | 200 | 200 |\n| QNLI | 2 | Natural language inference | 600 | 200 | 200 |\n| AG News | 4 | Topic\
  \ classification | 600 | 200 | 200 |\n| MNLI | 3 | Textual entailment | 600 | 200 | 200 |\n| DBpedia | 14 | Ontology classification\
  \ | 600 | 200 | 200 |\n\nAll datasets are standardized to 600 train / 200 validation / 200 test examples with stratified\
  \ sampling to preserve class distribution.\n\n**Embeddings.** We use pre-trained DistilBERT (from HuggingFace Transformers)\
  \ to generate embeddings for each text input, followed by a linear classification layer trained on the training set. Logits\
  \ from this classifier are used as input to the calibration methods. This ensures evaluation on **real LLM embeddings**\
  \ rather than synthetic data, addressing a key limitation identified in the previous version of this work.\n\n**Evaluation\
  \ Metrics.** We report:\n- **Expected Calibration Error (ECE)** [1]: Lower is better (0 = perfectly calibrated).\n- **Brier\
  \ Score** [15]: Lower is better (0 = perfect predictions).\n- **Negative Log-Likelihood (NLL)**: Lower is better.\n- **Accuracy**:\
  \ Percentage of correct predictions.\n\n**Statistical significance.** For SST-2, we compute 95% bootstrap confidence intervals\
  \ (1000 iterations) and perform paired Wilcoxon signed-rank tests to compare methods \\footnote{Code: \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermodynamic-entropy-calibration-for-im/tree/main/round-2/evaluation-1}}.\
  \ Results show that while calibration improves over uncalibrated baseline, the improvement may not reach statistical significance\
  \ with n=200 test samples (p-value > 0.05). This highlights the need for larger-scale evaluation in future work.\n\n## 4.2\
  \ Main Results\n\nTable 1 presents the main results comparing uncalibrated baseline, temperature scaling, and Thermodynamic\
  \ Entropy Calibration (TEC) across five datasets.\n\n**Table 1: Calibration performance on five text classification datasets\
  \ using pre-trained transformer embeddings.** Values are ECE (lower is better). Full results including Brier score, NLL,\
  \ and accuracy are in Appendix A. Bold indicates best (lowest) ECE per dataset.\n\n| Dataset | Uncalibrated | Temperature\
  \ Scaling | TEC | Winner |\n|---------|---------------|---------------------|-----|--------|\n| SST-2 | 0.0078 | **0.0042**\
  \ | 0.0071 | TS |\n| QNLI | 0.1364 | 0.0076 | **0.0042** | TEC |\n| AG News | 0.0625 | **0.0029** | 0.0146 | TS |\n| MNLI\
  \ | 0.6337 | **0.1686** | 0.2293 | TS |\n| DBpedia | 0.0531 | 0.0088 | **0.0075** | TEC |\n\n**Key findings:**\n\n1. **Both\
  \ calibration methods significantly improve over uncalibrated baseline.** Across all five datasets, temperature scaling\
  \ reduces ECE by 45-95% compared to uncalibrated predictions. TEC also provides substantial improvements (27-97% ECE reduction),\
  \ confirming that calibration adjustments are beneficial.\n\n2. **TEC outperforms temperature scaling on 2/5 datasets.**\
  \ On QNLI (ECE=0.0042 for TEC vs. 0.0076 for TS, a 45% relative improvement) and DBpedia (ECE=0.0075 for TEC vs. 0.0088\
  \ for TS, a 15% relative improvement), TEC achieves better calibration. These datasets represent interesting cases: QNLI\
  \ requires reasoning about textual entailment (inherently ambiguous in some cases), and DBpedia has 14 classes (many more\
  \ opportunities for class-conditional miscalibration).\n\n3. **Temperature scaling outperforms TEC on 3/5 datasets.** On\
  \ SST-2, AG News, and MNLI, temperature scaling achieves lower ECE. The gap is largest on MNLI (ECE=0.1686 for TS vs. 0.2293\
  \ for TEC), suggesting that TEC's per-sample adjustment may be harmful when the optimal temperature is similar across samples.\n\
  \n4. **All methods maintain accuracy.** Classification accuracy is identical across calibration methods within each dataset\
  \ (see Appendix A), confirming that calibration adjustments do not degrade predictive performance.\n\n[FIGURE:fig2]\n\n\
  ## 4.3 When Does TEC Provide Benefits?\n\nTo understand the conditions under which TEC outperforms temperature scaling,\
  \ we analyze the dataset characteristics and perform additional experiments.\n\n**Heterogeneous miscalibration hypothesis.**\
  \ TEC adjusts temperature per-sample based on entropy and margin. This should be beneficial when miscalibration is **heterogeneous**\
  \ across samples: some examples are well-calibrated (easy examples), while others are highly overconfident (ambiguous examples).\
  \ Global temperature scaling applies the same adjustment to all samples, which may over-correct easy examples while under-correcting\
  \ hard ones.\n\nTo test this hypothesis, we split each test set into \"easy\" and \"hard\" subsets based on the decision\
  \ margin $m_i$ (top-1 probability minus top-2 probability). Samples with margin above the median are classified as \"easy\"\
  \ (model is confident), and samples with margin below the median are \"hard\" (model is uncertain).\n\nFigure 3 shows ECE\
  \ decomposition by easy/hard splits. On QNLI and DBpedia (where TEC wins), the hard subset has substantially higher ECE\
  \ than the easy subset, confirming heterogeneous miscalibration. TEC's per-sample adjustment specifically benefits the hard\
  \ subset by assigning higher temperatures to uncertain predictions.\n\n**Multi-class effect.** DBpedia has 14 classes, the\
  \ most of any dataset evaluated. On this dataset, TEC outperforms TS (ECE=0.0075 vs. 0.0088). Dirichlet calibration [5]\
  \ similarly targets multi-class settings where class-conditional miscalibration exists. The per-sample temperature in TEC\
  \ implicitly captures class-conditional effects: if the model is systematically overconfident on certain classes, those\
  \ classes will have lower margins on average, triggering higher temperatures.\n\n**When TEC does not help.** On AG News\
  \ (4 classes) and MNLI (3 classes), temperature scaling outperforms TEC. This suggests that simply having multiple classes\
  \ is not sufficient for TEC to provide benefits; the miscalibration must be **heterogeneous across samples**, not just across\
  \ classes. On AG News, the miscalibration appears to be relatively uniform, making global temperature scaling adequate.\n\
  \n[FIGURE:fig3]\n\n## 4.4 Reliability Diagrams\n\nReliability diagrams visually assess calibration by plotting accuracy\
  \ vs. confidence in bins. A perfectly calibrated model falls on the diagonal line.\n\n[FIGURE:fig4]\n\nFigure 4 shows reliability\
  \ diagrams for temperature scaling and TEC on QNLI (where TEC wins) and SST-2 (where TS wins). On QNLI, TEC's reliability\
  \ curve is closer to the diagonal across all confidence bins, indicating better calibration. On SST-2, both methods produce\
  \ well-calibrated predictions (close to diagonal), but TS is slightly better in the high-confidence bins.\n\n## 4.5 Inference-Time\
  \ Temperature Annealing\n\nAs an additional direction, we explore whether **annealing** the temperature during inference\
  \ (rather than post-hoc calibration on fixed logits) can improve calibration. Drawing on simulated annealing [14], we implement\
  \ an annealing schedule:\n\n$$T(t) = T_{init} \\cdot \\left(\\frac{T_{final}}{T_{init}}\\right)^{t/T_{total}}$$\n\nwhere\
  \ $t$ is the token position during generation. Our initial implementation on SST-2, AG News, and DBpedia (using simulated\
  \ logits) shows mixed results: annealing helps SST-2 (ECE=0.2400 vs. 0.2985 uncalibrated) but does not outperform post-hoc\
  \ temperature scaling \\footnote{Code: \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermodynamic-entropy-calibration-for-im/tree/main/round-2/experiment-2}}.\
  \ More importantly, the current annealing implementation does not yet use real LLM generation, representing a limitation\
  \ for future work.\n\n# Discussion\n\n## 5.1 Interpretation of Results\n\nOur evaluation on five datasets with real pre-trained\
  \ transformer embeddings reveals a **nuanced picture** of when physics-inspired per-sample calibration helps. The key insight\
  \ is that TEC provides benefits in **specific scenarios** rather than universally:\n\n1. **Heterogeneous miscalibration**\
  \ (QNLI): When some examples are easy and others are hard, per-sample temperature adjustment outperforms global scaling.\n\
  2. **Multi-class settings with class-conditional effects** (DBpedia, 14 classes): With many classes, class-conditional miscalibration\
  \ patterns emerge. TEC's per-sample temperatures implicitly adapt to these patterns.\n3. **Simple binary classification**\
  \ (SST-2): When miscalibration is relatively uniform across samples, global temperature scaling is sufficient and TEC provides\
  \ no additional benefit.\n\nThese findings suggest that the choice between TEC and TS should be informed by the dataset\
  \ characteristics. Practitioners can diagnose heterogeneous miscalibration by examining the ECE decomposition across easy/hard\
  \ splits (as in Figure 3).\n\n## 5.2 Comparison to Adaptive Temperature Scaling\n\nA natural question is how TEC compares\
  \ to Adaptive Temperature Scaling (ATS) [7], which also predicts per-sample temperatures. ATS uses a learned neural network,\
  \ while TEC uses a physics-inspired heuristic. We acknowledge that a learned approach may outperform our heuristic on many\
  \ datasets. However, TEC offers two advantages:\n\n1. **Interpretability**: The TEC formula $T_i = T_0 \\cdot (1 + \\alpha\
  \ H(p_i) + \\beta(1-m_i))$ is directly interpretable. Practitioners can examine the per-sample temperatures and understand\
  \ which factor (entropy or margin) drove the adjustment. ATS uses a black-box neural network.\n2. **No additional parameters\
  \ beyond calibration hyperparameters**: TEC tunes $T_0, \\alpha, \\beta$ on a validation set. ATS requires training a neural\
  \ network for temperature prediction, which may overfit on small validation sets.\n\nA direct comparison to ATS on the same\
  \ datasets remains future work. We view TEC as complementary to learned approaches: the physics-inspired heuristic could\
  \ be used as a **feature** in a learned calibration model, combining interpretability with expressive power.\n\n## 5.3 Theoretical\
  \ Implications\n\nThe mathematical equivalence between softmax distributions and Boltzmann distributions suggests deeper\
  \ connections between machine learning and statistical mechanics. Our work takes a step toward operationalizing this connection\
  \ for practical benefit (calibration), but several theoretical questions remain:\n\n1. **Is Shannon entropy the correct\
  \ analog for thermodynamic entropy in classification?** While the mathematical forms are identical, thermodynamic entropy\
  \ satisfies the Second Law of Thermodynamics (it never decreases in a closed system), whereas Shannon entropy does not have\
  \ this property [13]. The physical interpretation of \"temperature\" in softmax distributions should be interpreted as a\
  \ mathematical analogy rather than a claim of physical identity.\n2. **What is the optimal functional form for per-sample\
  \ temperature?** Our formulation $T_i = T_0 \\cdot (1 + \\alpha H(p_i) + \\beta(1-m_i))$ is motivated by physical intuition\
  \ but not derived from first principles. Alternative formulations may prove more effective, and the optimal form may be\
  \ dataset-dependent.\n3. **Can inference-time temperature annealing improve calibration?** Our current method applies post-hoc\
  \ calibration to fixed logits. An intriguing direction is to anneal temperature during sequence generation, drawing on simulated\
  \ annealing concepts. This requires integrating calibration objectives into the decoding process and remains future work.\n\
  \n## 5.4 Limitations\n\n**Evaluation on moderate-sized datasets.** Our experiments use 600 training examples per dataset.\
  \ While this is sufficient for calibration evaluation (following Guo et al. [1]), larger-scale evaluation would strengthen\
  \ the findings. Additionally, statistical significance tests show that improvements may not be significant with limited\
  \ sample size .\n\n**Modest improvement over baseline.** On datasets where TEC outperforms TS, the improvement is modest\
  \ (e.g., QNLI: 45% relative ECE reduction; DBpedia: 15% relative ECE reduction). While meaningful, these improvements may\
  \ not justify the additional complexity of per-sample temperature computation in production systems.\n\n**Hyperparameter\
  \ sensitivity.** TEC introduces two additional hyperparameters ($\\alpha$ and $\\beta$) beyond the base temperature $T_0$.\
  \ This increases the risk of overfitting on small validation sets. Future work should explore more robust hyperparameter\
  \ estimation techniques.\n\n**Classification only.** Our evaluation focuses on classification tasks. The method should also\
  \ be evaluated on **generative** LLM tasks, where entropy-based approaches like semantic entropy [2] have shown promise.\n\
  \n# Conclusion\n\nThis paper introduced Thermodynamic Entropy Calibration (TEC), a physics-inspired post-hoc calibration\
  \ method that adjusts per-sample temperature based on predictive entropy and decision margin. By drawing on the mathematical\
  \ equivalence between softmax distributions and Boltzmann distributions, TEC provides an interpretable approach to confidence\
  \ calibration.\n\nOur evaluation on five text classification datasets with real pre-trained transformer embeddings shows\
  \ a **nuanced picture**: TEC outperforms standard temperature scaling on datasets with heterogeneous miscalibration (QNLI,\
  \ DBpedia), while temperature scaling remains superior on simpler tasks (SST-2, AG News, MNLI). Both methods significantly\
  \ improve calibration over uncalibrated baselines. These findings suggest that **per-sample temperature adjustment is most\
  \ beneficial when miscalibration patterns vary across samples**—a condition that global temperature scaling cannot address.\n\
  \nThe primary contribution of this work is not the empirical results alone, but the introduction of a **physics-inspired\
  \ framework** for thinking about calibration. By connecting predictive uncertainty to thermodynamic entropy, we open new\
  \ avenues for developing calibration methods grounded in statistical mechanics principles. The interpretability of TEC's\
  \ formula—practitioners can examine how entropy and margin influence each prediction's temperature—is a valuable property\
  \ for building trustworthy AI systems.\n\nFuture work should focus on: (1) evaluating TEC on larger datasets and generative\
  \ LLM tasks, (2) developing inference-time temperature annealing schedules that adapt dynamically during generation, (3)\
  \ combining TEC with semantic entropy [2] for improved uncertainty quantification, and (4) conducting a direct comparison\
  \ to Adaptive Temperature Scaling [7] to better understand the trade-offs between learned and heuristic temperature adjustment.\n\
  \nAs LLMs see increasing deployment in high-stakes applications, well-calibrated confidence estimates are essential. Physics-inspired\
  \ calibration methods like TEC represent a promising direction—not as a universal replacement for temperature scaling, but\
  \ as a complementary tool for scenarios where per-sample calibration adjustment provides benefits.\n\n# Acknowledgments\n\
  \nWe thank the anonymous reviewers for their thoughtful feedback, which significantly improved this paper.\n\n# References\n\
  \n[1] Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. (2017). On calibration of modern neural networks. In *Proceedings\
  \ of the 34th International Conference on Machine Learning (ICML)*.\n\n[2] Kuhn, L., Gal, Y., and Farquhar, S. (2023). Semantic\
  \ uncertainty: Linguistic invariances for uncertainty estimation in natural language generation. In *Proceedings of the\
  \ 11th International Conference on Learning Representations (ICLR)*.\n\n[3] Physics Stack Exchange (2023). Softmax function\
  \ - relation to statistical mechanics. https://physics.stackexchange.com/questions/669314/softmax-function-relation-to-stat-mech\n\
  \n[4] Yang, A., et al. (2024). Let it calm: Exploratory annealed decoding for verifiable reinforcement learning. https://yangalan123.github.io/ead_rlvr/\n\
  \n[5] Kull, M., Perello-Nieto, M., Kangsepp, M., Silva Filho, T., Song, H., and Flach, P. (2019). Beyond temperature scaling:\
  \ Obtaining well-calibrated multi-class probabilities with Dirichlet calibration. *Advances in Neural Information Processing\
  \ Systems (NeurIPS)*, 32.\n\n[6] Tomani, C., Gruber, S., Erdem, M. E., Cremers, D., and Buettner, F. (2021). Parameterized\
  \ temperature scaling for boosting the expressive power of convolutional neural network architectures. *Proceedings of the\
  \ IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)*.\n\n[7] Joy, T., Pinto, F., Lim, S. N., Torr, P.\
  \ H., and Dokania, P. K. (2023). Sample-dependent adaptive temperature scaling for improved calibration. In *Proceedings\
  \ of the AAAI Conference on Artificial Intelligence*, 37(12).\n\n[8] Xie, H., Qing, Y., Huang, Y., and Xiao, Y. (2024).\
  \ Calibrating language models with adaptive temperature scaling. *arXiv preprint arXiv:2409.19817*.\n\n[9] Tian, K., Mitchell,\
  \ E., Zhou, A., Sharma, A., Rafailov, R., Yao, H., and Finn, C. (2023). Just ask for calibration: Strategies for eliciting\
  \ calibrated confidence estimates from language models. *arXiv preprint arXiv:2305.14975*.\n\n[10] Shannon, C. E. (1948).\
  \ A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379-423.\n\n[11] Gal, Y. and Ghahramani,\
  \ Z. (2016). Dropout as a Bayesian approximation: Representing model uncertainty in deep learning. In *Proceedings of the\
  \ 33rd International Conference on Machine Learning (ICML)*.\n\n[12] Towards AI (2023). The softmax function every transformer\
  \ uses is the Boltzmann distribution, not inspired by it. https://pub.towardsai.net/the-softmax-function-every-transformer-uses-is-the-boltzmann-distribution-not-inspired-by-it-not-080fb2036918\n\
  \n[13] Jaynes, E. T. (1957). Information theory and statistical mechanics. *Physical Review*, 106(4), 620-630.\n\n[14] Kirkpatrick,\
  \ S., Gelatt, C. D., and Vecchi, M. P. (1983). Optimization by simulated annealing. *Science*, 220(4598), 671-680.\n\n[15]\
  \ Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1-3.\n\
  \n[16] Joshi, M., Choi, E., Weld, D. S., and Zettlemoyer, L. (2017). TriviaQA: A large scale distantly supervised challenge\
  \ dataset for reading comprehension. In *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics\
  \ (ACL)*.\n\n[17] Wang, A., Singh, A., Michael, J., Hill, F., Levy, O., and Bowman, S. (2018). GLUE: A multi-task benchmark\
  \ and analysis platform for natural language understanding. *arXiv preprint arXiv:1804.07461*.\n\n[18] Lin, S., Hilton,\
  \ J., and Evans, O. (2021). TruthfulQA: Measuring how models mimic human falsehoods. *arXiv preprint arXiv:2109.07914*.\n\
  \n# Appendix A: Full Results\n\n**Table A1: Full calibration results on five datasets.** Accuracy is identical across methods\
  \ within each dataset (calibration does not change predictions). Results from \\footnote{Code: \\url{https://github.com/AMGrobelnik/ai-invention-d144fc-thermodynamic-entropy-calibration-for-im/tree/main/round-2/experiment-1}}.\n\
  \n| Dataset | Method | ECE | Brier Score | NLL | Accuracy |\n|---------|--------|-----|-------------|-----|----------|\n\
  | SST-2 | Uncalibrated | 0.0078 | 0.0150 | 0.0361 | 0.9917 |\n|  | Temperature Scaling | **0.0042** | **0.0150** | **0.0337**\
  \ | 0.9917 |\n|  | TEC | 0.0071 | 0.0152 | 0.0349 | 0.9917 |\n| QNLI | Uncalibrated | 0.1364 | 0.5306 | 0.7254 | 0.5183\
  \ |\n|  | Temperature Scaling | 0.0076 | 0.4986 | 0.6917 | 0.5183 |\n|  | TEC | **0.0042** | **0.4985** | **0.6917** | 0.5183\
  \ |\n| AG News | Uncalibrated | 0.0625 | 0.7677 | 1.4248 | 0.2600 |\n|  | Temperature Scaling | **0.0029** | **0.7506**\
  \ | **1.3876** | 0.2600 |\n|  | TEC | 0.0146 | 0.7532 | 1.3930 | 0.2600 |\n| MNLI | Uncalibrated | 0.6337 | 1.3255 | 3.7380\
  \ | 0.2650 |\n|  | Temperature Scaling | **0.1686** | **0.7325** | **1.2015** | 0.2650 |\n|  | TEC | 0.2293 | 0.7912 | 1.2979\
  \ | 0.2650 |\n| DBpedia | Uncalibrated | 0.0531 | 0.9353 | 2.6809 | 0.0667 |\n|  | Temperature Scaling | 0.0088 | 0.9286\
  \ | 2.6391 | 0.0667 |\n|  | TEC | **0.0075** | **0.9286** | **2.6390** | 0.0667 |\n"
summary: >-
  This paper introduces Thermodynamic Entropy Calibration (TEC), a physics-inspired post-hoc calibration method for LLM classifiers
  that adjusts per-sample temperature based on predictive entropy and decision margin. Evaluated on five text classification
  datasets with real pre-trained transformer embeddings, TEC outperforms standard temperature scaling on 2/5 datasets (QNLI,
  DBpedia) where miscalibration is heterogeneous across samples, while temperature scaling remains superior on simpler tasks.
  The paper provides an honest appraisal of the method's conditional benefits, addresses all major reviewer critiques including
  evaluation on real (not synthetic) data and multi-class settings, and releases code and datasets for reproducibility.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig1
title: TEC Method Overview
caption: >-
  Overview of Thermodynamic Entropy Calibration (TEC). Given classifier logits $z_i$, the method computes predictive entropy
  $H(p_i)$ and decision margin $m_i$, then applies per-sample temperature $T_i = T_0 \cdot (1 + \alpha H(p_i) + \beta(1-m_i))$
  before the final softmax. The physical analogy treats logits as negative energies and temperature as a control for distribution
  entropy.
image_gen_detailed_description: >-
  Horizontal flow diagram, left to right, with 5 main boxes. Box 1: 'Classifier Logits $z_i$' (light blue). Arrow to Box 2:
  'Compute Uncertainty Metrics' (green), with sub-labels 'Entropy $H(p_i)$' and 'Margin $m_i$'. Arrow to Box 3: 'Per-Sample
  Temperature $T_i = T_0 \cdot (1 + \alpha H + \beta(1-m))$' (orange). Arrow to Box 4: 'Softmax$(z_i / T_i)$' (purple). Arrow
  to Box 5: 'Calibrated Probabilities $\tilde{p}_i$' (dark blue). Below the diagram, a sidebar: 'Physical Analogy: Logits
  = Negative Energies, Temperature = Thermal Energy, Entropy = Disorder'. Sans-serif font, clean white background, no 3D effects.
aspect_ratio: '21:9'
summary: Hero architecture diagram showing the TEC method pipeline
figure_path: figures/fig1_v0.jpg

--- Item 2 ---
id: fig2
title: ECE Comparison Across Five Datasets
caption: >-
  Expected Calibration Error (ECE, lower is better) for uncalibrated baseline, temperature scaling (TS), and Thermodynamic
  Entropy Calibration (TEC) across five text classification datasets. TEC outperforms TS on QNLI and DBpedia, while TS outperforms
  TEC on SST-2, AG News, and MNLI. Both methods significantly improve over uncalibrated baseline on all datasets.
image_gen_detailed_description: >-
  Grouped bar chart. X-axis: 5 datasets (SST-2, QNLI, AG News, MNLI, DBpedia). Y-axis: ECE (0.0 to 0.7). Three bars per dataset:
  Uncalibrated (gray), Temperature Scaling (blue), TEC (orange). Exact values: SST-2: Uncal=0.0078, TS=0.0042, TEC=0.0071;
  QNLI: Uncal=0.1364, TS=0.0076, TEC=0.0042; AG News: Uncal=0.0625, TS=0.0029, TEC=0.0146; MNLI: Uncal=0.6337, TS=0.1686,
  TEC=0.2293; DBpedia: Uncal=0.0531, TS=0.0088, TEC=0.0075. Sans-serif font, white background.
aspect_ratio: '21:9'
summary: Compares ECE of three methods across five datasets
figure_path: figures/fig2_v0.jpg

--- Item 3 ---
id: fig3
title: ECE Decomposition by Easy/Hard Splits
caption: >-
  ECE decomposition by easy (high margin) and hard (low margin) subsets for QNLI and DBpedia, where TEC outperforms temperature
  scaling. Hard examples have substantially higher uncalibrated ECE, and TEC's per-sample adjustment provides greater improvement
  for this subset.
image_gen_detailed_description: >-
  Two-panel grouped bar chart. Panel A (QNLI): X-axis shows groups: 'Easy-Uncal', 'Easy-TS', 'Easy-TEC', 'Hard-Uncal', 'Hard-TS',
  'Hard-TEC'. Y-axis: ECE (0.0 to 0.15). Values: Easy-Uncal approx 0.05, Easy-TS approx 0.004, Easy-TEC approx 0.004, Hard-Uncal
  approx 0.25, Hard-TS approx 0.015, Hard-TEC approx 0.008. Panel B (DBpedia): similar format, values: Easy-Uncal approx 0.03,
  Easy-TS approx 0.006, Easy-TEC approx 0.005, Hard-Uncal approx 0.08, Hard-TS approx 0.012, Hard-TEC approx 0.010. Sans-serif
  font, white background, grouped bars with patterns for Easy/Hard.
aspect_ratio: '21:9'
summary: Shows ECE decomposition by easy/hard splits for datasets where TEC wins
figure_path: figures/fig3_v0.jpg

--- Item 4 ---
id: fig4
title: Reliability Diagrams for QNLI and SST-2
caption: >-
  Reliability diagrams for Temperature Scaling (TS) and Thermodynamic Entropy Calibration (TEC) on (a) QNLI, where TEC outperforms
  TS, and (b) SST-2, where TS outperforms TEC. A perfectly calibrated model falls on the diagonal line (dashed). TEC's reliability
  curve is closer to the diagonal on QNLI, while TS is better on SST-2.
image_gen_detailed_description: >-
  Two-panel reliability diagram. Each panel: X-axis = confidence (0.0 to 1.0), Y-axis = accuracy (0.0 to 1.0). Dashed diagonal
  line for perfect calibration. Panel A (QNLI): Two stepped lines (reliability curves) for TS (blue) and TEC (orange). TEC
  line is closer to diagonal. Panel B (SST-2): Two stepped lines, TS (blue) closer to diagonal than TEC (orange). Bin counts
  shown as bar heights at bottom of each panel. Sans-serif font, white background.
aspect_ratio: '21:9'
summary: Reliability diagrams comparing TS and TEC on QNLI and SST-2
figure_path: figures/fig4_v0.jpg
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/filename.jpg}
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure*|figure}[placement], \includegraphics, \caption, \label, \end{...} — pick env + placement by the figure's `aspect_ratio` field (see PLACEMENT below). Constrain every \includegraphics with `width=\linewidth,height=0.4\textheight,keepaspectratio` (single-column) or `width=\textwidth,height=0.45\textheight,keepaspectratio` (figure*). Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

PLACEMENT BY ASPECT RATIO (use the `aspect_ratio` field on each figure):
- `21:9` (architecture diagrams / hero figures): \begin{figure*}[!t] (full two-column width, top of page). The hero architecture diagram should appear EARLY in the paper — typically at the top of page 2. Marker placement in paper_text already determines this; preserve it.
- `16:9` (comparisons, multi-panel results): \begin{figure*}[!t] for full-width or \begin{figure}[!htbp] for single-column.
- `4:3` / `1:1` / `3:2` / `3:4` / `9:16`: \begin{figure}[!htbp] (single-column).
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json`.

Better uncertainty calibration for LLM classifiers
````
