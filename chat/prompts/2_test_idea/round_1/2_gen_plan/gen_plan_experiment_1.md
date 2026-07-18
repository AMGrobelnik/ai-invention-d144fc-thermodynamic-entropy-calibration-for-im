# gen_plan_experiment_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_plan`
> Run: `run_3fUR0i5e8NC7` — Thermodynamic Entropy Calibration for Improved Confidence Estimation in LLM Classifiers
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_experiment_1` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-18 15:17:39 UTC

````
<hypothesis>
kind: hypothesis
title: Calibrate LLM uncertainty via thermodynamic entropy
hypothesis: >-
  Modeling predictive uncertainty as thermodynamic entropy and applying temperature-based annealing during inference will
  produce better-calibrated confidence scores for LLM classifiers.
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
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter1_dir3
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
</artifact_direction>



<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
  - gpu: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → 4090 → 5090)
  - cpu_heavy: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json`.
````

### [2] HUMAN-USER prompt · 2026-07-18 15:17:39 UTC

```
Better uncertainty calibration for LLM classifiers
```

### [3] SKILL-INPUT — aii-web-research-tools · 2026-07-18 15:18:03 UTC

The agent loaded the **aii-web-research-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-research-tools
description: "Comprehensive web research toolkit — use whenever a task needs MORE than a handful of WebSearch/WebFetch calls (multi-source literature reviews, deep verification across many pages, paper/PDF mining, cross-referencing claims, building bibliographies). Not for single quick lookups — use raw WebSearch/WebFetch for those. Adds aii_web_tools__fetch_grep for exact regex extraction over HTML or PDFs (arXiv, journals) with context windows, beyond what WebFetch's lossy summary returns. Trigger: any extensive/comprehensive/deep research task, literature review, multi-source investigation, verify many citations, arxiv, paper, PDF, exact quote, methodology, table value, regex."
---

## Available Web Tools

Three levels of web tools:

1. **WebSearch** — broad discovery. Returns titles, URLs, snippets. Cheapest. Use first to scan the landscape.
2. **WebFetch** — read a specific page. LLM summarizes it. HTML only. May miss specific details.
3. **aii_web_tools__fetch_grep** — exact text extraction from HTML or PDF. Regex matching with context windows.
   Use for precise details, methodology, or when WebFetch missed something.
   Key params: pattern (required), max_matches (default 20), context_chars (default 200 per side).

**Workflow:** WebSearch → WebFetch for gist → aii_web_tools__fetch_grep for exact details or PDFs.

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-research-tools"
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [4] SYSTEM-USER prompt · 2026-07-18 15:30:19 UTC

`````
YOUR PREVIOUS SESSION WAS INTERRUPTED: A single operation exceeded the 720s message timeout. Each individual operation must complete within 720s. Do NOT mock, skip, or compromise your execution — still do the real work. Try to make operations run faster if possible. If a command genuinely takes longer than 720s, split it into sequential parts that each complete within the time limit.

Last messages before interruption:
  - [agent_response]: I notice the JSON file is incomplete - I'm missing the required `fallback_plan` and `testing_plan` fields, and the JSON structure isn't properly closed. Let me fix this and provide a complete, valid JSON file.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "str_replace",
  "path": "/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json",
  "file_text": null,
  "old_str": "   ```\"\n  }\n}",
  "new_str": "   ```\",\n  \n  \"fallback_plan\":
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "No replacement was performed, old_str ````\"\n  }\n}` did not appear verbatim in /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.
  - [agent_think]: The JSON file I created has issues - it's not properly formatted because I didn't close the JSON structure correctly. The implementation_pseudocode field has a very long string that ends with ``` but then the JSON structure isn't properly closed with the required fields.

Let me view the current fil
  - [agent_response]: Let me view the current file to understand the issue and then fix it properly.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": null
}
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "Here's the result of running `cat -n` on /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json:\n     1\t{\n     2\t  \"title\": \
  - [agent_think]: The file is missing the `fallback_plan` and `testing_plan` fields, and the JSON is not properly structured. Looking at the current file, I can see that:

1. The `implementation_pseudocode` field ends with a ``` at line 5
2. There's no `fallback_plan` field
3. There's no `testing_plan` field
4. The J
  - [agent_response]: I see the issue - the JSON file is incomplete and missing the required `fallback_plan` and `testing_plan` fields. Let me recreate the file with proper JSON structure.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "str_replace",
  "path": "/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json",
  "file_text": null,
  "old_str": "   ```\"\n  }\n}",
  "new_str": "   ```\",\n  \n  \"fallback_plan\":
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "No replacement was performed, old_str ````\"\n  }\n}` did not appear verbatim in /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.
  - [agent_think]: The issue is that the file ends with ````"\n  }\n}` but I'm not matching it exactly. Let me look at the exact end of the file again. Looking at the output, the file ends with:

```
   ```
}
```

So the last few lines are:
- Line 5: `   ```"`
- Line 6: `}`

Wait, looking more carefully at the file co
  - [agent_response]: Let me recreate the entire JSON file with the correct structure. I'll create a complete, valid JSON file with all required fields.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "str_replace",
  "path": "/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json",
  "file_text": null,
  "old_str": "   ```\"\n  }\n}",
  "new_str": "   ```\",\n  \n  \"fallback_plan\":
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "No replacement was performed, old_str ````\"\n  }\n}` did not appear verbatim in /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.
  - [agent_think]: The issue is that the file editor is having trouble matching the exact string. Let me try a different approach - I'll recreate the entire file from scratch with all the required fields properly formatted.

Looking at the current file, I can see it ends with:
```
   ```"
  }
}
```

But the JSON is in
  - [agent_response]: Let me check the exact end of the file and recreate it properly with all required fields.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "view",
  "path": "/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json",
  "file_text": null,
  "old_str": null,
  "new_str": null,
  "insert_line": null,
  "view_range": [
    1,
   
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "NOTE: We only show up to 6 since there're only 6 lines in this file.\nHere's the result of running `cat -n` on /ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.s
  - [agent_think]: The file has 6 lines, and the JSON is incomplete - it's missing the closing quote for the `implementation_pseudocode` field and the remaining required fields (`fallback_plan` and `testing_plan`). 

Looking at line 5, the `implementation_pseudocode` value ends with ````json\n   ```"` which suggests t

CONTINUE FOLLOWING THESE INSTRUCTIONS:

<hypothesis>
kind: hypothesis
title: Calibrate LLM uncertainty via thermodynamic entropy
hypothesis: >-
  Modeling predictive uncertainty as thermodynamic entropy and applying temperature-based annealing during inference will
  produce better-calibrated confidence scores for LLM classifiers.
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
</hypothesis>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: experiment_iter1_dir3
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
</artifact_direction>



<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

EXPERIMENT executor scope:
  Output: method_out.json with results (metrics, predictions, analysis) — the core computational work
  DOES: Implement and run methods/algorithms, compute metrics, compare approaches, produce quantitative results
  DOES NOT: Collect new datasets (depends on DATASET artifacts for input data), write formal proofs
  This is the right artifact for any code that processes data and produces results
</artifact_executor_scope>

<artifact_planning_rules>
EXPERIMENT: Must depend on at least one DATASET. Define clear metrics and baselines before running. Consider trying multiple method variations rather than a single approach.
</artifact_planning_rules>

<compute_profiles>
Choose the compute profile this artifact needs for execution.
Available profiles for experiment artifacts:
  - gpu: 1x NVIDIA RTX A4500, 20GB VRAM, 7 vCPUs, 29GB RAM — ML training, CUDA, large models (fallback: GPUs cheap→expensive: 2000 Ada → A4000 → 4000 Ada → L4 → 4090 → 5090)
  - cpu_heavy: 4 vCPUs, 32GB RAM — large datasets, memory-intensive processing (fallback: CPUs cheap→expensive, then GPU hosts cheap→expensive (all ≥32GB RAM))

Set runpod_compute_profile to one of these exact tier names.
</compute_profiles>
GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "description": "Plan for an EXPERIMENT artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "implementation_pseudocode": {
      "description": "High-level pseudocode for the experiment implementation",
      "title": "Implementation Pseudocode",
      "type": "string"
    },
    "fallback_plan": {
      "description": "What to do if the primary approach fails - alternative methods, simplified versions",
      "title": "Fallback Plan",
      "type": "string"
    },
    "testing_plan": {
      "description": "How to validate the experiment works: start with small/fast tests, look for confirmation signals before running full-scale experiments",
      "title": "Testing Plan",
      "type": "string"
    }
  },
  "required": [
    "title",
    "implementation_pseudocode",
    "fallback_plan",
    "testing_plan"
  ],
  "title": "ExperimentPlan",
  "type": "object"
}
```

IMPORTANT: This task is NOT complete until you Write `/ai-inventor/aii_data/runs/run_3fUR0i5e8NC7/3_invention_loop/iter_1/gen_plan/gen_plan_experiment_1/.sdk_openhands_agent_struct_out.json`.

Better uncertainty calibration for LLM classifiers
`````
