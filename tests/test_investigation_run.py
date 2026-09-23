"""A fresh PT run may be reviewed without escaping its publication block."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from mixed_methods_workbench.investigation_run import (
    RUN_ROOT,
    ConnectedRunError,
    connected_run_payload,
    load_connected_run,
)
from mixed_methods_workbench.investigation_spine import investigation_spine_payload


def test_native_run_and_model_check_are_bound_but_not_promoted() -> None:
    receipt, export = load_connected_run()
    payload = connected_run_payload()
    assert [item.outcome for item in receipt.attempts] == [
        "blocked_partition", "blocked_publication"
    ]
    assert export.comparative_conclusion.public_headline_eligible is False
    assert receipt.review_state == "blocked_publication_pending_researcher_review"
    assert receipt.check_cost_usd > 0
    assert [item.finding_id for item in receipt.challenge.findings] == [
        item.hypothesis_id for item in export.verdicts
    ]
    evidence = {item.evidence_id for item in export.evidence if item.source_quote}
    assert all(set(item.evidence_ids) <= evidence for item in receipt.challenge.findings)
    assert payload["publication_block_reason"]
    assert investigation_spine_payload()["connected_run"]["run_id"] == receipt.run_id


def test_reused_qc_input_mutation_invalidates_connected_run(tmp_path: Path) -> None:
    root = tmp_path / "run"
    shutil.copytree(RUN_ROOT, root)
    path = root / "qc_theory_input.json"
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(ConnectedRunError, match="inputs changed"):
        load_connected_run(root)


def test_unknown_challenge_citation_is_rejected(tmp_path: Path) -> None:
    root = tmp_path / "run"
    shutil.copytree(RUN_ROOT, root)
    path = root / "connected_run_receipt.json"
    receipt = json.loads(path.read_text(encoding="utf-8"))
    receipt["challenge"]["findings"][0]["evidence_ids"].append("unseen-source")
    path.write_text(json.dumps(receipt), encoding="utf-8")
    with pytest.raises(ConnectedRunError, match="unavailable source quote"):
        load_connected_run(root)


def test_review_page_names_both_guards_and_the_human_boundary() -> None:
    html = (
        Path(__file__).resolve().parents[1]
        / "src/mixed_methods_workbench/static/investigation_spine.html"
    ).read_text(encoding="utf-8")
    assert "Stopped at rival-partition gate" in html
    assert "Stopped at publication guardrail" in html
    assert "researcher review is still pending" in html
