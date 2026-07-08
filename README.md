# Evidence-Based AI Safety Policy Translation

**Translating empirical findings from LLM safety benchmarks into concrete deployment and evaluation recommendations — grounded in specific measured results, not general commentary.**

[![CI](https://github.com/praneethaneelapareddigari/ai-safety-policy-translation/actions/workflows/ci.yml/badge.svg)](https://github.com/praneethaneelapareddigari/ai-safety-policy-translation/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Status**

- ✅ Framework and evidence-pulling tooling complete and tested
- ⬜ Evidence synthesis — **blocked on real-model results from sibling benchmarks** (see below)
- ⬜ Risk analysis, deployment considerations, recommendations — depend on evidence synthesis
- 📝 Structure drafted throughout `docs/`, explicitly marked pending where evidence doesn't exist yet

> ⚠️ **This project is a scaffold, not a finished synthesis, as of this commit.** Every recommendation document in `docs/` is structured but intentionally left unwritten where it would need real evidence that doesn't exist yet. See [`docs/problem_statement.md`](docs/problem_statement.md), "Status," for why — publishing conclusions ahead of the underlying evidence would defeat the purpose of an evidence-driven project.

## Why this project exists

Two sibling benchmark projects each measure one slice of LLM safety:

| Project | Measures |
|---|---|
| [Cross-Lingual LLM Safety Evaluation (SentinelAI)](https://github.com/praneethaneelapareddigari/SentinelAI) | Does refusal behavior hold up consistently across languages? |
| [Prompt Injection & Jailbreak Robustness Benchmark](https://github.com/praneethaneelapareddigari/technical-ai-safety-experiment) | How effective are different guardrail strategies against adversarial attacks? |

Neither, on its own, tells a team building on an LLM what to actually *do* with that finding. This project is the synthesis layer — but only once there's real evidence to synthesize. See [`docs/problem_statement.md`](docs/problem_statement.md) for the full framing, and [`docs/limitations.md`](docs/limitations.md) for what this project explicitly does not claim to be (not a regulatory position paper, not a comprehensive safety survey).

## How evidence flows into this repo

The mechanism that keeps this project evidence-driven rather than opinion-driven is [`scripts/pull_evidence.py`](scripts/pull_evidence.py): it reads results *directly* from the sibling repos' own output files and renders them as markdown evidence tables. It has a hard safety gate mirroring the one already built into `technical-ai-safety-experiment`:

```bash
# Blocked by default if the source data is data_provenance=SIMULATED (mock model fleet)
python scripts/pull_evidence.py --source tase \
  --path ../technical-ai-safety-experiment/results/tables/summary.json \
  --out evidence/tase_evidence.md

# SentinelAI's pilot data is real but caveated — caveats are attached automatically, always
python scripts/pull_evidence.py --source sentinelai \
  --path ../SentinelAI/results/csv/refusal_rate.csv \
  --out evidence/sentinelai_evidence.md
```

No recommendation in `docs/policy_recommendations.md` is meant to exist without tracing back to a row rendered this way — see that file's "Intended structure and tone" section for the exact pattern every recommendation follows once written.

## Repository Structure

```
ai-safety-policy-translation/
|-- README.md
|-- LICENSE
|-- CITATION.cff
|-- requirements.txt
|-- .github/workflows/ci.yml
|-- docs/
|   |-- problem_statement.md          # scope, what this is / isn't
|   |-- evidence_synthesis.md          # generated tables from sibling repos (pending)
|   |-- risk_analysis.md               # framework, pending evidence
|   |-- deployment_considerations.md   # framework, pending evidence
|   |-- evaluation_recommendations.md  # framework, pending evidence
|   |-- policy_recommendations.md      # framework + required citation pattern
|   |-- limitations.md
|   `-- future_research.md
|-- scripts/
|   `-- pull_evidence.py               # evidence-pulling tool with mock-data safety gate
|-- evidence/                          # generated evidence tables land here (currently empty)
`-- tests/
    `-- test_pull_evidence.py          # covers the safety gate explicitly
```

## Quickstart

```bash
git clone https://github.com/praneethaneelapareddigari/ai-safety-policy-translation
cd ai-safety-policy-translation
pip install -r requirements.txt
pytest tests/ -v
```

Once the sibling repos have real-model results, regenerate the evidence tables with the commands in [How evidence flows into this repo](#how-evidence-flows-into-this-repo) above, then work through `docs/` in order: `evidence_synthesis.md` → `risk_analysis.md` → `deployment_considerations.md` / `evaluation_recommendations.md` → `policy_recommendations.md`.

## Roadmap

- [x] Repository scaffold, evidence-pulling tool, safety gate, tests
- [ ] `technical-ai-safety-experiment` Experiment 03 (real-model runs) — **blocking evidence_synthesis.md**
- [ ] SentinelAI Version 2 (validated classifier, larger sample) — needed before cross-lingual evidence is confirmatory rather than pilot-caveated
- [ ] Write `evidence_synthesis.md` once both above are unblocked
- [ ] Write `risk_analysis.md`, `deployment_considerations.md`, `evaluation_recommendations.md`
- [ ] Write `policy_recommendations.md` — every recommendation cited to a specific evidence row
- [ ] Cross-link to AgentGuard once that project exists (evidence → engineering loop)

## Relationship to Other Projects

| Project | Contribution |
|---|---|
| SentinelAI | Cross-lingual LLM safety evaluation — evidence source |
| Prompt Injection & Jailbreak Robustness Benchmark | Adversarial robustness evaluation — evidence source |
| **This project** | Synthesis layer: evidence → deployment/evaluation guidance |
| AgentGuard | Engineering system implementing guardrails informed by this synthesis *(planned)* |
| [SATYA](https://github.com/praneethaneelapareddigari/hackathon-portfolio/tree/main/completed/satya) | Real-world high-stakes application (government procurement) where this synthesis's deployment recommendations would actually apply once populated |

## License

MIT — see [LICENSE](LICENSE).

## Citation

See [`CITATION.cff`](CITATION.cff).
