# gen_paper_text — test_idea

> Phase: `invention_loop` · round 2 · `gen_paper_text`
> Run: `run_3fUR0i5e8NC7` — Thermodynamic Entropy Calibration for Improved Confidence Estimation in LLM Classifiers
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_paper_text` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-18 17:41:56 UTC

````
<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for related-work positioning and how this field frames a genuinely novel contribution.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>
<previous_paper>
STARTING POINT: This is your paper draft from the previous iteration.

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

</previous_paper>

<reviewer_feedback>
STEP 1 — REVIEW: A reviewer evaluated the previous paper draft above and produced this feedback.

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

<pipeline_steps>
STEP 2 — STRATEGY: The pipeline's strategy generator (gen_strat) read the reviewer feedback
and designed a new research strategy to address the critiques.

STEP 3 — PLANNING: The planner (gen_plan) turned the strategy into concrete artifact plans —
specific experiments, datasets, or research tasks to execute.

STEP 4 — EXECUTION: The executor (gen_art) ran those plans and produced the new artifacts
shown in <new_artifacts_this_iteration> below.
</pipeline_steps>

<hypothesis>
STEP 5 — HYPOTHESIS UPDATE: The hypothesis was revised based on evidence from previous iterations.

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

<all_artifacts>
FULL EVIDENCE BASE: All 6 research artifacts across all iterations.

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
NEW THIS ITERATION: These 3 artifacts were created to address the reviewer
feedback. Their findings should be the primary basis for your revisions.

title: TEC vs TS calibration on 5 LLM datasets
summary: >-
  Completed experiment comparing Thermodynamic Entropy Calibration (TEC) vs Temperature Scaling (TS) on 5 text classification
  datasets (SST-2, QNLI, AG News, MNLI, DBpedia) using pre-trained transformers. Methods: (1) Uncalibrated baseline, (2) Temperature
  Scaling, (3) TEC with per-sample temperature based on entropy + margin. Metrics: ECE, Brier score, NLL, Accuracy with bootstrap
  CI (200 samples). Heterogeneous analysis on easy/hard splits by decision margin. Results: TEC outperformed TS on 2/5 datasets
  (QNLI, DBpedia), TS outperformed TEC on 3/5 datasets. Both methods significantly improved calibration over uncalibrated
  baseline. Output saved to method_out.json in exp_gen_sol_out schema format with per-example predictions.
id: art_xdUSFFTTrRuY
type: experiment

title: Temperature Annealing LLM Calibration Experiment
summary: >-
  Implemented and evaluated inference-time temperature annealing for LLM calibration on SST-2, AG News, and DBpedia datasets.
  Compared against Temperature Scaling (TS) and Thermodynamic Entropy Calibration (TEC) baselines. Used simulated logits (NumPy-based
  implementation) to test four methods: uncalibrated baseline, TS, TEC, and Annealing+Softmax. Results on 1000 samples show
  TS reduces ECE by ~56% on SST-2 (0.2985 to 0.1302). Annealing shows mixed results - helps SST-2 (ECE 0.2400 vs 0.2985 uncalibrated)
  but not AG News. All methods maintain similar accuracy while improving calibration. Output validates against exp_gen_sol_out.json
  schema.
id: art_5XrEi0TPtFOf
type: experiment

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
id: art_PHvp8viBEPFq
type: evaluation
</new_artifacts_this_iteration>

<data_files>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_files>

<task>
Write a research paper draft with LaTeX-ready text, BibTeX citations, and figure placeholders.

YOUR TURN (gen_paper_text): Revise the paper.

You are a researcher improving your paper after receiving a conference review.
Take the feedback seriously and make substantive changes, not cosmetic ones.

1. ADDRESS REVIEWER FEEDBACK: For each critique in <reviewer_feedback>, either fix the
   issue in the paper or argue convincingly why it doesn't apply. Major critiques MUST
   be resolved -- they would cause rejection if left unaddressed.
2. USE THE NEW EVIDENCE: The artifacts in <new_artifacts_this_iteration> were created
   specifically to address the reviewer's concerns. Reference their findings to
   strengthen the sections that were flagged as weak.
3. REWRITE, DON'T PATCH: Don't just append new paragraphs. Restructure and rewrite
   the sections the reviewer identified as problematic.
4. MAINTAIN CONSISTENCY: Ensure the paper aligns with the updated hypothesis.
</task>

<figure_instructions>
FIGURE FORMAT: Use [FIGURE:fig_id] markers in paper_text to indicate where each figure goes.
Then provide the full figure specs in the separate `figures` structured output array.
Each figure in the array must have an `id` matching a marker in the text. Set the `aspect_ratio`
field per figure: 21:9 for architecture / pipeline / flow-chart diagrams (the hero figure should
be one of these — place its marker near the END of the Introduction so it floats to the top of
page 2), 16:9 for comparisons / multi-panel results, 4:3 for dense charts, 1:1 for heatmaps /
confusion matrices / scatter plots.

Example in paper_text:
  "...our method achieves state-of-the-art results as shown below.\n\n[FIGURE:fig3]\n\nThe results demonstrate..."

Example in figures array (results comparison):
  {"id": "fig3", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: latency (seconds, 0-5). Values: PostgreSQL=4.6s (red), Bao=2.8s (blue), RLQOpt=2.0s (green). Error bars +/-0.3-0.8. Sans-serif font, white background.", "aspect_ratio": "16:9", "summary": "Compares latency across optimizers"}

Example in figures array (architecture diagram, hero):
  {"id": "fig1", "title": "System Architecture", "caption": "End-to-end pipeline: encoder feeds latents into the planner, which queries the value head before emitting actions.", "image_gen_detailed_description": "Horizontal flow diagram, left to right. Five labeled boxes: 'Input' (gray), 'Encoder' (blue), 'Latent (z, 256-dim)' (light blue, narrow), 'Planner' (green), 'Action Head' (orange). Arrows labeled with shapes. Value head as separate green box below 'Planner', bidirectional arrow. Sans-serif font, clean white background, no 3D.", "aspect_ratio": "21:9", "summary": "Hero architecture diagram"}

CRITICAL: Before writing figure specs, look through artifact workspace output files (*_out.json)
and code to find ALL the exact values. The figure generator cannot read files — every exact number
and value MUST be in the image_gen_detailed_description.
</figure_instructions>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-writing, aii-semscholar-bib.
TODO 2. LITERATURE REVIEW: Use web search tools to research the landscape — search key terms from
<hypothesis> and <all_artifacts>. Then use aii_semscholar_bib__fetch to batch-fetch real
BibTeX entries. Build a comprehensive Related Work section. Do NOT fabricate entries.
TODO 3. READ ARTIFACTS: Before writing each section, READ the relevant artifact source code, output
files, and data in the workspace. Extract concrete implementation details, technical innovations,
algorithmic specifics, and quantitative results. Do NOT write surface-level descriptions.

ARTIFACT REFERENCES: When you reference results, methodology, or findings from a specific artifact,
place an [ARTIFACT:artifact_id] marker inline. These become footnotes linking to the artifact's code
in the GitHub repository (first mention gets a footnote with URL, subsequent mentions are omitted).
Use the exact artifact ID from <all_artifacts>. Place the marker right after the claim it supports.
Example:
  "Our evaluation showed a 15% improvement over baselines [ARTIFACT:art_4f9d2c81ab37]." 
TODO 4. WRITE PAPER: Write the full paper text with [FIGURE:fig_id] markers per <figure_instructions>,
and provide the figure specs in the figures array. Cite with numeric references [1], [2], etc.
At the end of the paper text, include a full bibliography section. Do NOT compile LaTeX or generate
actual image/figure files. Your ONLY output is the structured JSON.
</todos><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FigureSpec": {
      "description": "Figure specification \u2014 structured output from paper writing agent.\n\nThe LLM fills these as a list in PaperText.figures.\nLater converted to Figure objects for viz gen.",
      "properties": {
        "id": {
          "description": "Figure ID matching the [FIGURE:id] marker in paper_text (e.g., 'fig1')",
          "title": "Id",
          "type": "string"
        },
        "title": {
          "description": "Figure title in plain, everyday language \u2014 short and jargon-free. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "caption": {
          "description": "LaTeX figure caption \u2014 appears below the figure in the paper. Should describe what the figure shows and highlight key takeaways.",
          "title": "Caption",
          "type": "string"
        },
        "image_gen_detailed_description": {
          "description": "Detailed image generation prompt \u2014 axes, labels, ALL numeric values, colors, aspect ratio, layout. The image generator cannot read files; this is its ONLY input.",
          "title": "Image Gen Detailed Description",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this figure communicates",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "id",
        "title",
        "caption",
        "image_gen_detailed_description",
        "summary"
      ],
      "title": "FigureSpec",
      "type": "object"
    }
  },
  "description": "Paper text \u2014 structured output from paper writing agent.\n\nStructured output fields (LLMPrompt + LLMStructOut):\n- title, abstract, paper_text, figures, summary\n\npaper_text contains [FIGURE:fig_id] markers for positioning.\nfigures contains the full specs as structured objects.\n\nMetadata fields (plain, set by pipeline code):\n- id",
  "properties": {
    "title": {
      "description": "Paper title \u2014 clear, plain-language, and short so a non-expert understands the main contribution at a glance. Aim for about 6-10 words; avoid jargon and acronyms.",
      "title": "Title",
      "type": "string"
    },
    "abstract": {
      "description": "Paper abstract",
      "title": "Abstract",
      "type": "string"
    },
    "paper_text": {
      "description": "Full paper body text with markdown section headers (# Introduction, # Methods, # Results, # Discussion, # Conclusion). Use [FIGURE:fig_id] markers (e.g. [FIGURE:fig1]) to indicate where each figure should appear.",
      "title": "Paper Text",
      "type": "string"
    },
    "figures": {
      "description": "List of figure specifications. Each must have an id matching a [FIGURE:id] marker in paper_text.",
      "items": {
        "$ref": "#/$defs/FigureSpec"
      },
      "title": "Figures",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the paper's main contribution and findings",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "abstract",
    "paper_text",
    "summary"
  ],
  "title": "PaperText",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/.sdk_openhands_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-07-18 17:41:56 UTC

```
Better uncertainty calibration for LLM classifiers
```

### [3] SKILL-INPUT — aii-paper-writing · 2026-07-18 17:42:04 UTC

The agent loaded the **aii-paper-writing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-writing
description: Academic paper writing guidance for AI research. Covers paper structure, figure placeholders, bibliography building with Semantic Scholar, and citation rules. Does NOT cover LaTeX compilation or figure file generation — see aii-paper-to-latex for that.
---

## Technical Papers

Guidance for the standard "technical paper" format: propose a method/system/framework, evaluate it experimentally, report results. This is the main track at most CS venues (NeurIPS, ICML, ICLR, ACL, AAAI, etc.). Does NOT cover: pure theory/formal proofs, survey papers, position papers, or dataset/benchmark papers — those have different structures.

### Paper Structure

Target 6-8 pages. Use formal academic language, third person. Support claims with evidence from artifacts.

#### Rough Page Budget (8-page paper)

| Section | Pages | Notes |
|---|---|---|
| Abstract | 0.3 | Problem, approach, key result |
| Introduction | 1.0-1.5 | The most important section |
| Related Work | 0.5-1.0 | Beginning or end (see below) |
| Methods | 1.5-2.0 | Architecture fig on page 1 |
| Experiments | 1.5-2.0 | Setup + results + ablations |
| Discussion | 0.5-1.0 | Limitations go here |
| Conclusion | 0.3-0.5 | Do not repeat the abstract |
| References | 0.5-1.0 | Not counted in page limit |

**Critical rule**: A clear new technical contribution must be articulated by page 3 (quarter of the paper). If the reader doesn't know what you did by then, you've lost them.

#### Section Details

**Abstract** (150-250 words): State the problem, your approach, and the main results. Be factual and comprehensive. Do not repeat the abstract word-for-word later in the paper.

**Introduction** — Follow this 5-paragraph structure:

1. **What is the problem?** Define the task concretely.
2. **Why is it interesting and important?** Real-world impact, scale.
3. **Why is it hard?** Why do naive approaches fail?
4. **Why hasn't it been solved before?** What's wrong with prior solutions? How does yours differ?
5. **What are the key components of your approach and results?** Include specific limitations.

End with a "Summary of Contributions" subsection — bullet list of contributions with section references. This doubles as an outline, saving space.

**Related Work** — Placement decision:
- **Beginning** (Section 2): If it can be short yet detailed, or if you need a strong defensive stance against prior work early.
- **End** (before Conclusions): If comparisons require your technical content, or if it can be summarized briefly in the Introduction. Can be titled "Discussion and Related Work."

**Methods/Approach**: Every section tells a story — the story of the results, NOT the story of how you arrived at them. Use top-down description: readers should see where the material is going and be able to skip ahead. Move gory details to appendices.

**Experiments**: Setup (datasets, metrics, baselines) → main results → ablations → analysis. Every claim needs quantitative evidence.

**Discussion**: Interpret results, compare to prior work, state limitations honestly. Limitations should be specific and actionable, not vague disclaimers.

**Conclusion**: Short summarizing paragraph. Do NOT repeat material from the Abstract or Introduction. Make original claims more concrete (e.g., reference quantitative results). Include future work as bullet list — if actively pursuing follow-up, say so to mark territory.

#### Writing Quality Rules

- Define all notation/terminology before use, only once. Group global definitions in Preliminaries.
- Do NOT use nonreferential "this", "that", "these", "it". Always specify the referent. BAD: "This is important because..." GOOD: "This accuracy gap is important because..."
- Do NOT use "etc." unless remaining items are completely obvious. BAD: "We measure volatility, scalability, etc." GOOD: "We measure volatility and scalability."
- Do NOT write "for various reasons" — state the actual reasons.
- "That" is defining, "which" is nondefining. "The algorithms that are easy to implement" vs "The algorithms, which are easy to implement."
- Use italics for definitions and quotes, not for emphasis. Context alone should provide emphasis.

### Figure Format

Figures use a hybrid marker + structured array approach. ALL figures are generated by a separate pipeline step using an AI image model — your `image_gen_detailed_description` is the ONLY input that model sees. It cannot read files or access data. Do NOT generate actual image files yourself (no matplotlib, no PIL, no image generation scripts).

**In paper_text**: Place `[FIGURE:fig_id]` markers where figures should appear.

**In figures array**: Provide full specs as structured objects with these fields:
- `id` — matches the `[FIGURE:id]` marker in paper_text
- `title` — short descriptive title
- `caption` — LaTeX caption that appears below the figure in the paper
- `image_gen_detailed_description` — detailed prompt for the image generator (axes, ALL values, colors, layout)
- `summary` — brief summary of what the figure communicates

Example in paper_text:
```
...our method achieves state-of-the-art results as shown below.

[FIGURE:fig_1]

The results in Figure 1 demonstrate...
```

Example figure spec in figures array:
```json
{"id": "fig_1", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers on JOB benchmark. RLQOpt achieves 2.3x speedup over PostgreSQL.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: ModelA=0.847, ModelB=0.762, Baseline=0.531. Error bars with std: 0.02, 0.03, 0.05. Sans-serif font, white background.", "summary": "Compares accuracy of proposed methods vs baseline."}
```

Every marker in text MUST have a matching figure in the array, and vice versa.

#### Data Precision Requirement

`image_gen_detailed_description` MUST include exact numbers from artifact output files. Read the actual output files before writing figure specs.

- BAD: "Compare accuracy metrics across configurations"
- GOOD: "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: K=3: 0.765, K=5: 0.729, Baseline: 0.121."

#### Figure vs Table Decision

Do NOT create figures for tabular data (rows/columns of text or numbers). Use `\begin{table}` in LaTeX instead. Figures are for actual visualizations only (charts, plots, diagrams).

#### Figure Placement Strategy

Be intentional with figure ordering. The architectural/method overview figure explaining the proposed approach MUST appear early — in the Introduction or at the start of Methods — so readers can immediately orient themselves. Readers skim papers top-down; if the first figure they see is a results bar chart, they have no mental model for interpreting it.

Recommended ordering:
1. **Architecture/method diagram** — Introduction or early Methods (so readers understand the approach before diving into details)
2. **Conceptual/analogy figures** — Introduction or Methods (to build intuition)
3. **Results figures** (bar charts, line plots, scatter plots) — Results section
4. **Analysis/ablation figures** — Discussion or later Results

#### Guidelines

- Plan 3-6 figures total across the paper
- Place [FIGURE:fig_id] markers INLINE where referenced in text
- Include axes, labels, ALL numeric values in figure descriptions
- Both data-driven figures (bar charts, line plots) and conceptual diagrams (architecture, flowcharts)
- Be as detailed as possible in descriptions: specify aspect ratio, preferred colors, all data values, axis labels, ranges, legend entries, and any other visual details. The more specific the description, the better the generated figure

### Bibliography with Semantic Scholar

Build `./references.bib` using the aii-semscholar-bib skill (real BibTeX from Semantic Scholar):

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in one batch
3. Write the returned .bib text into `./references.bib`

Rules:
- Do NOT fabricate BibTeX entries — always fetch from Semantic Scholar
- If a paper isn't found (very recent preprint), write the entry manually as fallback
- Use `\bibliography{references}` and `\bibliographystyle{plainnat}`
- Do NOT use inline `thebibliography` environment

### Citation Format (for Research Artifacts)

When writing research with numbered citations:

1. Every factual claim MUST have a numbered citation: `[1]`, `[2]`, `[1, 3]`, etc.
2. Each source in the "sources" array MUST have an "index" field
3. The index MUST EXACTLY MATCH citation numbers in the text
4. NEVER cite a number without a matching source index
5. Example: "LLMs show 40% improvement with multi-agent collaboration [1]."
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-07-18 17:42:04 UTC

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

### [5] SKILL-INPUT — aii-web-tools · 2026-07-18 17:42:04 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: web search (Serper/Google), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — Serper.dev for search, html2text + PyMuPDF for fetch, and
   regex grep over the full document text. They work without any built-in web
   tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (Serper.dev / Google)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
```

Returns ranked title / URL / snippet lines. Use it first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````
