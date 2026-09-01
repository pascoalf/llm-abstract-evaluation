# LLMs as Scientific Abstract Evaluators

This is a small exploratory project developed to strengthen my Python and LLM evaluation skills while investigating the behavior of language models when asked to evaluate scientific text.

The project uses biomedical abstracts as a convenient proxy for scientific documents. Abstracts are short, relatively self-contained, and can be evaluated locally using small open-source language models without substantial computational requirements.

The current objective is to investigate **the variability and stability of LLM-generated evaluation scores**, both across repeated runs of the same model and across different models.

## Experimental setup

Each model is asked to evaluate biomedical abstracts according to three simplified criteria:

* **Clarity**
* **Relevance**
* **Apparent methodological rigor**

A score from **0 (lowest) to 5 (highest)** is generated independently for each criterion. A simple arithmetic mean of the three scores is also calculated as a composite score.

The evaluation prompts are intentionally simple. The purpose of this project is not to construct or validate a rigorous scientific-review system, but to explore the behavior and reproducibility of LLM-based scoring under controlled conditions.

In particular:

* no reference or human-derived scores are used as ground truth;
* the evaluation rubrics are deliberately minimal;
* relevance is not anchored to a specific research question or funding context;
* methodological rigor can only be inferred from information presented in the abstract;
* the composite score is an exploratory summary rather than a validated metric.

A more realistic evaluation system would require richer rubrics, contextual information, calibration examples, domain-specific instructions, and validation against appropriate external criteria.

## Evaluation criteria

### Clarity

| Score | Interpretation      |
| ----: | ------------------- |
|     0 | Extremely unclear   |
|     1 | Very unclear        |
|     2 | Somewhat unclear    |
|     3 | Reasonably clear    |
|     4 | Very clear          |
|     5 | Exceptionally clear |

### Relevance

| Score | Interpretation         |
| ----: | ---------------------- |
|     0 | Not relevant           |
|     1 | Very low relevance     |
|     2 | Somewhat relevant      |
|     3 | Reasonably relevant    |
|     4 | Very relevant          |
|     5 | Exceptionally relevant |

### Apparent methodological rigor

| Score | Interpretation                                           |
| ----: | -------------------------------------------------------- |
|     0 | No identifiable scientific rigor                         |
|     1 | Very low apparent rigor                                  |
|     2 | Limited apparent rigor                                   |
|     3 | Reasonable apparent rigor                                |
|     4 | High apparent rigor, with minor limitations              |
|     5 | Exceptionally rigorous based on the information provided |

## Models

The current experiments use three small instruction-tuned models available through Hugging Face:

* `microsoft/Phi-3-mini-4k-instruct`
* `Qwen/Qwen2.5-3B-Instruct`
* `meta-llama/Llama-3.2-3B-Instruct`

Models are evaluated using the same abstracts, prompts, scoring criteria, and generation settings wherever possible.

## Current questions

The analysis currently focuses on:

1. **Within-model variability** — How much does the score assigned to the same abstract vary across repeated generations?
2. **Stability with increasing repetitions** — How many repeated evaluations are needed before estimates of scoring variability begin to stabilize?
3. **Between-model differences** — Do different models show different levels of scoring variability on the same evaluation task?
4. **Criterion-specific behavior** — Are clarity, relevance, and apparent rigor scored with different levels of consistency?

## Results

*Results and visualizations will be added as the experiments are completed.*

## Scope

This repository is an exploratory Python/LLM project rather than a benchmark of scientific-review quality. The resulting scores should not be interpreted as validated measurements of scientific merit.

The emphasis is instead on building a reproducible workflow for model evaluation and examining how apparently simple LLM-based scoring behaves under repeated testing.
