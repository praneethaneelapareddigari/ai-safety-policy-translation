"""
scripts/pull_evidence.py

The core tool that keeps this project evidence-driven rather than
opinion-driven: it reads results directly from the sibling benchmark
repos (technical-ai-safety-experiment, SentinelAI) and renders them as
markdown evidence tables for docs/evidence_synthesis.md -- so every claim
in this repo traces back to a specific file, row, and number in a sibling
repo, not to a paraphrase of memory.

Safety gate (the important part)
---------------------------------
technical-ai-safety-experiment tags every result row with
`data_provenance: SIMULATED` when it comes from the mock model fleet, and
its own analysis layer (evaluation/statistics.py) refuses to summarize
that data as a finding without --allow-mock. This script enforces the
same rule one level up: it REFUSES to render SIMULATED rows into a policy
evidence table unless --allow-mock is passed explicitly, and even then it
stamps the output with a loud "NOT REAL EVIDENCE" banner. This is the
mechanism that prevents this project from accidentally citing synthetic
demo data as if it were a real finding about model safety.

SentinelAI's Pilot v1 data is real (not synthetic), but small-sample and
carries known measurement caveats (see that repo's README). This script
does not block it, but always attaches those caveats to any rendered
table so they can't be silently dropped when quoted here.
"""

from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

SENTINELAI_CAVEATS = [
    "28-prompt pilot sample -- validates pipeline functionality, not generalizable safety claims (not sufficient to confirm or reject H1).",
    "Non-English refusal rates are confirmed to be unreliable lower bounds: the rule-based classifier under-detects refusals in Hindi/Tamil/Malay (see that repo's README, Caveats & Known Limitations).",
    "Tamil results are additionally confounded by degraded generation/translation quality, independent of the refusal question.",
]


def load_tase_summary(path: Path) -> tuple[list[dict], str]:
    """Load technical-ai-safety-experiment's results/tables/summary.json.
    Returns (rows, data_provenance)."""
    data = json.loads(path.read_text())
    return data.get("summary", []), data.get("data_provenance", "UNKNOWN")


def load_sentinelai_refusal_csv(path: Path) -> list[dict]:
    """Load SentinelAI's results/csv/refusal_rate.csv."""
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def render_tase_evidence_markdown(rows: list[dict], provenance: str, allow_mock: bool) -> str:
    if provenance == "SIMULATED" and not allow_mock:
        return (
            "> **BLOCKED: this source is `data_provenance: SIMULATED` (mock model fleet).**\n"
            "> Refusing to render as policy evidence. Re-run with `--allow-mock` only if you "
            "explicitly want a loudly-labeled placeholder for pipeline testing -- never for an "
            "actual recommendation.\n"
        )

    lines = []
    if provenance == "SIMULATED":
        lines.append("> ⚠️ **NOT REAL EVIDENCE — SIMULATED / MOCK MODEL DATA.** "
                      "Rendered only because `--allow-mock` was passed. Do not cite "
                      "any number below in an actual policy recommendation.\n")
    lines.append("| Model | Defense | ASR | DSR |")
    lines.append("|---|---|---|---|")
    for r in rows:
        asr = r.get("attack_success_rate")
        dsr = r.get("defense_success_rate")
        asr_s = f"{asr*100:.1f}%" if isinstance(asr, (int, float)) else "n/a"
        dsr_s = f"{dsr*100:.1f}%" if isinstance(dsr, (int, float)) else "n/a"
        lines.append(f"| {r.get('model_name','?')} | {r.get('defense_name','?')} | {asr_s} | {dsr_s} |")
    return "\n".join(lines) + "\n"


def render_sentinelai_evidence_markdown(rows: list[dict]) -> str:
    lines = ["> **Caveats that apply to every number below** (see SentinelAI README for full detail):"]
    for c in SENTINELAI_CAVEATS:
        lines.append(f"> - {c}")
    lines.append("")
    if not rows:
        return "\n".join(lines) + "\n(no rows loaded)\n"
    headers = list(rows[0].keys())
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "---|" * len(headers))
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(h, "")) for h in headers) + " |")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", choices=["tase", "sentinelai"], required=True)
    ap.add_argument("--path", required=True, help="path to the sibling repo's results file")
    ap.add_argument("--out", required=True, help="markdown file to write")
    ap.add_argument("--allow-mock", action="store_true",
                     help="required to render tase evidence tagged data_provenance=SIMULATED")
    args = ap.parse_args()

    path = Path(args.path)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.source == "tase":
        rows, provenance = load_tase_summary(path)
        md = render_tase_evidence_markdown(rows, provenance, args.allow_mock)
    else:
        rows = load_sentinelai_refusal_csv(path)
        md = render_sentinelai_evidence_markdown(rows)

    out_path.write_text(md)
    print(f"Wrote evidence table to {out_path}")


if __name__ == "__main__":
    main()
