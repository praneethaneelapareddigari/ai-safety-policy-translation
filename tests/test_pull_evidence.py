import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.pull_evidence import (
    render_tase_evidence_markdown,
    render_sentinelai_evidence_markdown,
    SENTINELAI_CAVEATS,
)


def test_simulated_data_blocked_without_allow_mock():
    rows = [{"model_name": "mock-mistral", "defense_name": "llm_judge",
              "attack_success_rate": 0.05, "defense_success_rate": 0.9}]
    md = render_tase_evidence_markdown(rows, "SIMULATED", allow_mock=False)
    assert "BLOCKED" in md
    assert "mock-mistral" not in md  # the actual number must not leak through


def test_simulated_data_renders_with_loud_warning_when_overridden():
    rows = [{"model_name": "mock-mistral", "defense_name": "llm_judge",
              "attack_success_rate": 0.05, "defense_success_rate": 0.9}]
    md = render_tase_evidence_markdown(rows, "SIMULATED", allow_mock=True)
    assert "NOT REAL EVIDENCE" in md
    assert "mock-mistral" in md  # now it should actually appear
    assert "5.0%" in md


def test_real_data_renders_cleanly_no_warning():
    rows = [{"model_name": "gpt-4o-mini", "defense_name": "llm_judge",
              "attack_success_rate": 0.03, "defense_success_rate": 0.94}]
    md = render_tase_evidence_markdown(rows, "REAL", allow_mock=False)
    assert "BLOCKED" not in md
    assert "NOT REAL EVIDENCE" not in md
    assert "gpt-4o-mini" in md
    assert "3.0%" in md


def test_missing_metrics_render_as_na_not_crash():
    rows = [{"model_name": "x", "defense_name": "y"}]  # no ASR/DSR keys at all
    md = render_tase_evidence_markdown(rows, "REAL", allow_mock=False)
    assert "n/a" in md


def test_sentinelai_evidence_always_includes_all_caveats():
    rows = [{"Model": "Mistral 7B", "English": "9.9%", "Hindi": "0.0%"}]
    md = render_sentinelai_evidence_markdown(rows)
    for caveat in SENTINELAI_CAVEATS:
        assert caveat in md


def test_sentinelai_evidence_handles_empty_rows():
    md = render_sentinelai_evidence_markdown([])
    assert "no rows loaded" in md
    # caveats should still be present even with no data
    for caveat in SENTINELAI_CAVEATS:
        assert caveat in md
