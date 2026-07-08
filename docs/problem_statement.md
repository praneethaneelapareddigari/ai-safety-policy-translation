# Problem Statement

## Background

Two benchmark projects in this portfolio measure LLM safety along
different axes:

- **Cross-Lingual LLM Safety Evaluation (SentinelAI)** — does refusal
  behavior for unsafe requests hold up consistently across languages
  (English, Hindi, Mandarin, Tamil, Malay)?
- **Prompt Injection & Jailbreak Robustness Benchmark** — how effective
  are different guardrail strategies (prompt hardening, self-reflection,
  constitutional critique, LLM-as-judge, ensemble, multi-stage
  verification) against prompt-injection and jailbreak attacks?

Both produce technical findings. Neither, on its own, tells an
organization deploying an LLM system what to actually *do* with that
information. That gap — between "here is a measured safety property" and
"here is a concrete deployment or evaluation practice a team should
adopt" — is what this project addresses.

## What this project is

A synthesis layer that translates empirical findings from the two
benchmark repos above into deployment and evaluation recommendations,
grounded specifically in what those experiments actually measured — not
general AI policy commentary.

## What this project is explicitly not

- Not a position paper on AI regulation, government policy, or specific
  legislation (e.g. the EU AI Act). Single-project, weekend-scale
  benchmarks are the wrong evidence base for claims at that level — see
  `limitations.md`.
- Not a claim that these two benchmarks are comprehensive or
  representative of "LLM safety" in general.
- Not written before the underlying benchmarks have real (non-mock,
  non-pilot-only) results to synthesize — see Status below.

## Status

**This repository is currently a scaffold, not a finished synthesis.**
`evidence_synthesis.md` and every recommendation document in `docs/` are
structured but explicitly marked where they are waiting on real
experimental results from the sibling repos (see each file's own status
banner). Publishing firm recommendations before that evidence exists
would mean presenting speculation as findings — exactly what this project
is designed to avoid. See the root `README.md` Roadmap for what's
blocking each section.
