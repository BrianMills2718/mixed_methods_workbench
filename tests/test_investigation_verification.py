"""The second-model challenge stays bound to the exact P5 evidence packet."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from mixed_methods_workbench.investigation_spine import FIXTURE_ROOT, investigation_spine_payload
from mixed_methods_workbench.investigation_verification import (
    VerificationError,
    load_verification,
)


def _receipt_copy(tmp_path: Path) -> Path:
    target = tmp_path / "investigation_spine"
    shutil.copytree(FIXTURE_ROOT, target)
    return target


def _edit_receipt(root: Path, change) -> None:
    path = root / "independent_verification.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    change(value)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_authentic_challenge_covers_exact_findings_and_citations() -> None:
    receipt = load_verification()
    payload = investigation_spine_payload()
    assert receipt.review_state == "model_challenge_pending_human_review"
    assert receipt.cost_usd > 0
    assert [item.finding_id for item in receipt.challenge.findings] == [
        "documented_burdens_and_responses",
        "multiple_options_not_one_rule",
        "controlled_access_outcome",
    ]
    excerpts = {item["evidence_id"] for item in payload["independent_verification_excerpts"]}
    assert excerpts
    assert all(set(item.evidence_ids) <= excerpts for item in receipt.challenge.findings)
    assert payload["independent_verification"]["trace_id"] == receipt.trace_id
    assert payload["publication_block_reason"]


def test_changed_input_binding_is_rejected(tmp_path: Path) -> None:
    root = _receipt_copy(tmp_path)
    _edit_receipt(root, lambda data: data["input_digests"].update({"process_tracing_return.json": "0" * 64}))
    with pytest.raises(VerificationError, match="input digests"):
        load_verification(root)


def test_unknown_citation_is_rejected(tmp_path: Path) -> None:
    root = _receipt_copy(tmp_path)
    _edit_receipt(root, lambda data: data["challenge"]["findings"][0]["evidence_ids"].append("unknown-evidence"))
    with pytest.raises(VerificationError, match="unknown evidence"):
        load_verification(root)


def test_missing_finding_is_rejected(tmp_path: Path) -> None:
    root = _receipt_copy(tmp_path)
    _edit_receipt(root, lambda data: data["challenge"]["findings"].pop())
    with pytest.raises(VerificationError, match="every finding"):
        load_verification(root)


def test_challenge_page_keeps_human_review_and_excerpts_visible() -> None:
    html = (
        Path(__file__).resolve().parents[1]
        / "src/mixed_methods_workbench/static/investigation_spine.html"
    ).read_text(encoding="utf-8")
    assert "Bounded support in excerpts" in html
    assert "Inspect cited excerpts" in html
    assert 'id="verification-section"' in html
    assert 'byId("verification-section").hidden = false' in html
