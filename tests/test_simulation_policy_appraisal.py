"""Authentic simulation-to-policy-appraisal boundary and presentation checks."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from mixed_methods_workbench import simulation_policy_appraisal as appraisal_module
from mixed_methods_workbench.method_dashboard_server import simulation_appraisal_payload
from mixed_methods_workbench.simulation_policy_appraisal import (
    SOURCE_COMPARISON_PATH,
    SimulationComparisonFixture,
    load_simulation_policy_appraisal,
)

HTML_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "mixed_methods_workbench"
    / "static"
    / "simulation_policy_appraisal.html"
)


def _fixture_dict() -> dict[str, object]:
    return json.loads(SOURCE_COMPARISON_PATH.read_text(encoding="utf-8"))


def test_authentic_triad_becomes_only_model_conditional_appraisal_evidence() -> None:
    artifact = load_simulation_policy_appraisal()
    fixture = artifact.source_comparison
    appraisal = artifact.appraisal

    assert fixture.evidence_origin == "model_generated"
    assert {run.run_id for run in fixture.runs} == {
        "run_8924342b56ce",
        "run_946a10a820fc",
        "run_05acbaea1137",
    }
    assert sum(run.model_calls for run in fixture.runs) == 108
    assert appraisal.evidence_origin == "model_generated"
    assert appraisal.conclusion.status == "insufficient_for_recommendation"
    assert appraisal.conclusion.permitted_use == "investigate_design_candidate"
    assert "coincided" in appraisal.model_conditional_finding
    assert "caused" not in appraisal.model_conditional_finding


def test_source_row_digest_canonicalization_is_declared() -> None:
    fixture = load_simulation_policy_appraisal().source_comparison
    assert "sorted compact UTF-8 JSON followed by one newline" in (
        fixture.source.projection_method
    )


def test_duplicate_condition_fails_loud() -> None:
    payload = _fixture_dict()
    payload["runs"][1]["condition"] = payload["runs"][0]["condition"]
    with pytest.raises(ValidationError, match="exactly one run per required condition"):
        SimulationComparisonFixture.model_validate(payload)


def test_changed_simulated_outcome_fails_loud() -> None:
    payload = _fixture_dict()
    pressure = next(run for run in payload["runs"] if run["condition"] == "capacity_conflict")
    pressure["outcome"] = "joint_response_approved"
    with pytest.raises(ValidationError, match="capacity-conflict run must retain non-approval"):
        SimulationComparisonFixture.model_validate(payload)


def test_observed_evidence_label_fails_loud() -> None:
    payload = _fixture_dict()
    payload["evidence_origin"] = "observed"
    with pytest.raises(ValidationError):
        SimulationComparisonFixture.model_validate(payload)


def test_fixture_byte_corruption_fails_before_serving(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    payload = _fixture_dict()
    payload["applicability"] = "Altered after the fixture digest was frozen."
    corrupt_path = tmp_path / "source_comparison.json"
    corrupt_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    monkeypatch.setattr(appraisal_module, "SOURCE_COMPARISON_PATH", corrupt_path)
    with pytest.raises(ValueError, match="fixture SHA-256"):
        appraisal_module.load_simulation_policy_appraisal()


def test_api_and_browser_use_the_same_typed_artifact() -> None:
    payload = simulation_appraisal_payload()
    assert payload == load_simulation_policy_appraisal().model_dump(mode="json")
    html = HTML_PATH.read_text(encoding="utf-8")
    assert payload["appraisal"]["model_conditional_finding"] not in html
    assert "/api/appraisal/simulation-outbreak" in html


def test_browser_explains_what_happened_and_why_it_is_not_a_recommendation() -> None:
    html = HTML_PATH.read_text(encoding="utf-8")
    assert "A simulation result enters policy appraisal" in html
    assert "What happened inside the model" in html
    assert "Why this does not select a real policy" in html
    assert "Evidence needed before a recommendation" in html
    assert "model-generated evidence" in html


def test_routes_stay_on_the_existing_dashboard_service() -> None:
    server_source = Path(appraisal_module.__file__).with_name(
        "method_dashboard_server.py"
    ).read_text(encoding="utf-8")
    assert '"/appraisal/simulation-outbreak"' in server_source
    assert '"/api/appraisal/simulation-outbreak"' in server_source
