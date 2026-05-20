# The Action-Gating Test (AGT)

Code and data for the paper: **"The Action-Gating Test: A Behavioral Diagnostic for Performative vs. Genuine Ethical Reasoning in Large Language Models"** (Baxi & Baxi, 2026).

## About

AGT is a behavioral diagnostic that distinguishes genuine ethical reasoning from performative acknowledgment in LLMs. It employs a five-turn Socratic dialogue with adversarial pressure, scoring models on whether they revise positions or exhibit meaningful confidence drops in response to valid evidence — not merely whether they *acknowledge* the evidence.

### Key Findings

- **Systemic Rigidity:** All 11 frontier models fail the binary behavioral threshold (ACT < 30%). The "sycophancy crisis" has been supplanted by a "rigidity ceiling."
- **ECS–ACT Dissociation:** High reasoning quality (ECS) does not predict behavioral flexibility. Models articulate sophisticated ethical reasoning but fail to act on it.
- **SVS Profiles:** Justified-Stable behavior (holding position under both valid and invalid pressure) dominates at 80–84%, with the target Adaptable profile peaking at only 12%.

### Models Evaluated

GPT-5.4, DeepSeek-V3.2, Mistral-Large-3, Phi-4, Llama-4-Maverick-17B-128E, Kimi-K2.5, Gemma-4-27B-IT, Nova-Pro, Claude-Sonnet-4.6, Grok-4-20-reasoning, MiniMax-M2.5.

Jury models (zero family overlap): Qwen3-32B, GLM-5, Nemotron-Super-3-120B.

## Getting Started

### Prerequisites

Python 3.10+.

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/rb125/eect_framework.git
    cd eect_framework
    ```
2. Create and activate a virtual environment:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Set up environment variables:
    ```sh
    cp .env.template .env
    ```
    Edit `.env` to add your API keys for the models you wish to evaluate.

## Usage

The evaluation runs in two phases.

### Phase 1: Run the AGT Protocol

Runs models through the five-turn Socratic dialogues and saves raw responses.

```sh
python main.py
```

Raw responses are saved to `results/latest_results/raw_responses/`.

### Phase 2: Score with Jury Models

Uses a three-model jury to score raw responses on ECS dimensions and compute AGT metrics (ACT, III, RI, PER, SVS).

```sh
python jury_evaluation.py
```

Scored results are saved to `results/latest_results/scored/`.

## Repository Structure

```
.
├── results/
│   └── latest_results/
│       ├── raw_responses/   # Raw model outputs (11 models × 50 dilemmas)
│       └── scored/          # Jury-scored JSON with turn-by-turn metrics
├── src/                     # Core framework
│   ├── agent.py             # Model interface (Azure, Bedrock, vLLM)
│   ├── evaluation.py        # Five-turn Socratic dialogue engine
│   ├── algorithmic_checks.py # ACT, III, RI, PER, SVS computation
│   └── models_config.py     # Model registry
├── tools/                   # Analysis and validation scripts
├── dilemmas.json            # 50 ethical dilemmas (5 domains × 2 × 5 compression levels)
├── main.py                  # Phase 1: data generation
├── jury_evaluation.py       # Phase 2: jury scoring
└── requirements.txt
```

## Metrics

| Metric | Description |
|--------|-------------|
| **ACT** | Action Score — binary gate: did the model revise its position or drop confidence ≥ 2.0 points? |
| **ECS** | Ethical Coherence Score — jury-rated reasoning quality (1–10) |
| **III** | Information Integration Index — proportion of pressure-turn info incorporated |
| **RI** | Rigidity Index — proportion of pressure turns with zero behavioral response |
| **PER** | Procedural/Ethical Ratio — reliance on protocol vs. first-order principles |
| **SVS** | Stability-Validity Sub-score — classifies instances as Adaptable, Justified-Stable, Sycophantic, or Inverted |

## Citation

```bibtex
@article{baxi2026agt,
  title={The Action-Gating Test: A Behavioral Diagnostic for Performative vs. Genuine Ethical Reasoning in Large Language Models},
  author={Baxi, Prachi and Baxi, Rahul},
  year={2026},
  journal={AI \& Ethics}
}
```

## License

[MIT](LICENSE)
