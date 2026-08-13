"""Focused controls for the bounded QC-to-Process-Tracing investigation spine."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from mixed_methods_workbench.investigation_spine import (
    EXPECTED_FIXTURE_DIGESTS,
    FIXTURE_ROOT,
    InvestigationSpineError,
    investigation_spine_payload,
    load_investigation_spine,
)

HTML_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "mixed_methods_workbench"
    / "static"
    / "investigation_spine.html"
)
DASHBOARD_PATH = HTML_PATH.with_name("method_dashboard.html")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _mutable_fixtures(tmp_path: Path) -> Path:
    target = tmp_path / "investigation_spine"
    shutil.copytree(FIXTURE_ROOT, target)
    return target


def _rewrite_json(path: Path, payload: object) -> str:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return _sha256(path)


def test_spine_exposes_one_plain_language_investigation() -> None:
    spine = load_investigation_spine()

    assert spine.title == "Why did PsychosisBank use controlled access?"
    assert "P5" not in spine.title
    assert spine.status == "unresolved"
    assert spine.evidence_item_count == 24
    assert len(spine.sources) == 3
    assert [stage.owner for stage in spine.journey] == [
        "Qualitative Coding",
        "Process Tracing",
        "Process Tracing",
        "Qualitative Coding",
    ]
    assert spine.journey[-1].status == "retained_unconfirmed"
    assert "does not confirm" in spine.result_headline
    assert "P5" not in spine.result_summary
    assert all("P5" not in item for item in spine.unresolved_questions)
    assert len(spine.next_evidence) == 3


def test_spine_preserves_embedded_and_reference_only_custody() -> None:
    spine = load_investigation_spine()
    refs = {item.artifact_id: item for item in spine.artifact_refs}

    assert refs["qualitative-explanation"].content_sha256 == EXPECTED_FIXTURE_DIGESTS[
        "qualitative_explanation.json"
    ]
    assert refs["qualitative-explanation"].object_identity == "P5 / p5-v1"
    assert refs["independent-case-sources"].availability == "embedded"
    assert refs["process-tracing-return"].availability == "embedded"
    assert (
        refs["p5-psychosisbank-case-20260811a/run-exact-p5/result_blocked_prepublication.json"].availability
        == "producer_retained_reference"
    )
    assert all(len(item.content_sha256) == 64 for item in spine.artifact_refs)


def test_fixture_digest_mutation_fails_loud(tmp_path: Path) -> None:
    fixtures = _mutable_fixtures(tmp_path)
    path = fixtures / "qualitative_explanation.json"
    path.write_bytes(path.read_bytes() + b"\n")

    with pytest.raises(InvestigationSpineError, match="digest mismatch"):
        load_investigation_spine(fixtures)


def test_unsupported_schema_fails_after_authenticity_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixtures = _mutable_fixtures(tmp_path)
    path = fixtures / "process_tracing_return.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["schema_version"] = "pt_theory_test_return_v2"
    monkeypatch.setitem(EXPECTED_FIXTURE_DIGESTS, path.name, _rewrite_json(path, payload))

    with pytest.raises(InvestigationSpineError, match="schema_version"):
        load_investigation_spine(fixtures)


def test_missing_source_reference_fails_loud(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixtures = _mutable_fixtures(tmp_path)
    path = fixtures / "independent_case_sources.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["source_candidates"] = payload["source_candidates"][:-1]
    monkeypatch.setitem(EXPECTED_FIXTURE_DIGESTS, path.name, _rewrite_json(path, payload))

    with pytest.raises(InvestigationSpineError, match="does not resolve"):
        load_investigation_spine(fixtures)


def test_blocked_result_cannot_force_theory_revision(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixtures = _mutable_fixtures(tmp_path)
    path = fixtures / "process_tracing_return.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["theory_update"]["disposition"] = "revision_required"
    monkeypatch.setitem(EXPECTED_FIXTURE_DIGESTS, path.name, _rewrite_json(path, payload))

    with pytest.raises(InvestigationSpineError, match="indeterminate"):
        load_investigation_spine(fixtures)


def test_json_projection_matches_the_browser_contract() -> None:
    payload = investigation_spine_payload()
    html = HTML_PATH.read_text(encoding="utf-8")
    dashboard = DASHBOARD_PATH.read_text(encoding="utf-8")

    assert payload["schema_version"] == "mmw.investigation_spine.p5.v1"
    assert "Why did PsychosisBank use controlled access?" not in html
    assert "Why did PsychosisBank use controlled access?" == payload["title"]
    assert "/api/investigation/psychosisbank-disclosure" in html
    assert "This is a useful inconclusive result." in html
    assert "What would make the explanation testable" in html
    assert "P5" not in html
    assert "See an explanation tested with a new case" in dashboard
    assert "/investigation/psychosisbank-disclosure" in dashboard
