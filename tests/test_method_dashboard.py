"""Focused controls for the METHOD-DASH-C1 question-first study router."""

from __future__ import annotations

from http import HTTPStatus
from pathlib import Path

import pytest
from pydantic import ValidationError

from mixed_methods_workbench.method_dashboard import (
    EXAMPLES,
    AnalyticAim,
    ComparisonScope,
    EvidenceKind,
    StartingPoint,
    StudyBrief,
    dashboard_catalog,
    route_study,
)
from mixed_methods_workbench.method_dashboard_server import catalog_payload, route_payload

HTML_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "mixed_methods_workbench"
    / "static"
    / "method_dashboard.html"
)


def _example(example_id: str) -> StudyBrief:
    return next(example.brief for example in EXAMPLES if example.example_id == example_id)


def _route_ids(brief: StudyBrief) -> set[str]:
    return {route.method.method_id for route in route_study(brief).routes}


def test_catalog_exposes_representative_profiles_and_policy_spine() -> None:
    """Keep the first dashboard tied to the reviewed atlas breadth and workflow."""
    catalog = dashboard_catalog()
    assert len(catalog.methods) == 16
    assert [stage.stage_id for stage in catalog.stages] == [
        "frame",
        "review",
        "design",
        "analyze",
        "integrate",
        "appraise",
        "learn",
    ]
    assert set(catalog.aims) == set(AnalyticAim)
    assert len(catalog.aim_options) == len(AnalyticAim)
    assert len(catalog.starting_point_options) == len(StartingPoint)
    assert len(catalog.scope_options) == len(ComparisonScope)
    assert len(catalog.evidence_options) == len(EvidenceKind)
    assert all(option.description and option.help_text for option in catalog.aim_options)
    assert next(option for option in catalog.aim_options if option.value == "interpret").label == (
        "Understand what it means to people"
    )
    assert len(catalog.capability_tiers) == 3
    assert len(catalog.architecture_stress_tests) == 5
    assert [item.rank for item in catalog.architecture_stress_tests] == [1, 2, 3, 4, 5]
    assert catalog.architecture_stress_tests[0].stress_test_id == "policy_options_to_decision"
    assert catalog.architecture_stress_tests[-1].stress_test_id == "prediction_to_monitoring"
    assert all(item.falsifiable_assumptions for item in catalog.architecture_stress_tests)
    assert all(item.stop_rule for item in catalog.architecture_stress_tests)


def test_policy_decision_composes_analysis_and_appraisal_paths() -> None:
    """Prove a multi-aim policy question does not collapse into one policy method."""
    plan = route_study(_example("city_heat_policy"))
    route_ids = {route.method.method_id for route in plan.routes}
    assert {
        "evidence_synthesis",
        "forecasting",
        "simulation",
        "policy_appraisal",
        "robust_decision",
        "network_analysis",
    } <= route_ids
    assert "process_tracing" not in route_ids
    assert any("decision authority" in item for item in plan.missing_design_information)
    assert any("prediction target" in item for item in plan.missing_design_information)


def test_within_case_explanation_routes_to_pt_not_population_effects() -> None:
    """Preserve Process Tracing's bounded qualitative causal role."""
    brief = _example("program_failure")
    route_ids = _route_ids(brief)
    assert "process_tracing" in route_ids
    assert "thematic_analysis" in route_ids
    assert "grounded_theory" in route_ids
    assert "causal_models" in route_ids
    assert "causal_effects" not in route_ids
    pt_route = next(route for route in route_study(brief).routes if route.method.method_id == "process_tracing")
    assert pt_route.missing_requirements == []
    assert "a population average treatment effect" in pt_route.method.cannot_establish


def test_literature_first_study_can_stop_at_evidence_synthesis() -> None:
    """Keep literature review as a legitimate complete study, not only preparation."""
    plan = route_study(_example("remote_work_review"))
    assert plan.routes[0].method.method_id == "evidence_synthesis"
    assert plan.routes[0].missing_requirements == []
    assert "policy_appraisal" not in {route.method.method_id for route in plan.routes}


def test_same_evidence_exposure_warns_without_blocking_routes() -> None:
    """Implement the approved circularity treatment as qualification, not refusal."""
    brief = _example("program_failure").model_copy(
        update={"same_evidence_generated_explanation": True}
    )
    plan = route_study(brief)
    assert plan.routes
    assert any("same evidence" in warning.lower() for warning in plan.warnings)
    assert any("independent confirmation" in warning.lower() for warning in plan.warnings)


def test_unsure_scope_names_missing_decision_and_retains_several_paths() -> None:
    """Return design information needed instead of forcing a premature single route."""
    brief = StudyBrief(
        question="Why do implementation outcomes differ, and what might improve them?",
        aims=[AnalyticAim.EXPLAIN, AnalyticAim.INTERVENTION],
        starting_point=StartingPoint.EVIDENCE,
        scope=ComparisonScope.UNSURE,
        evidence=[EvidenceKind.DOCUMENTS, EvidenceKind.STRUCTURED_DATA],
    )
    plan = route_study(brief)
    assert len(plan.routes) >= 5
    assert any("study one case" in item for item in plan.missing_design_information)
    assert {"process_tracing", "comparative_case", "causal_effects", "causal_models"} <= {
        route.method.method_id for route in plan.routes
    }


def test_invalid_selection_combinations_fail_loud() -> None:
    """Reject duplicate selections and contradictory evidence-state declarations."""
    with pytest.raises(ValidationError, match="aims must not contain duplicates"):
        StudyBrief(
            question="What is happening across the selected organizations?",
            aims=[AnalyticAim.DESCRIBE, AnalyticAim.DESCRIBE],
            starting_point=StartingPoint.EVIDENCE,
            evidence=[EvidenceKind.DOCUMENTS],
        )
    with pytest.raises(ValidationError, match="no_evidence_yet cannot be combined"):
        StudyBrief(
            question="What evidence should be collected for this policy study?",
            aims=[AnalyticAim.DESCRIBE],
            starting_point=StartingPoint.POLICY_DECISION,
            evidence=[EvidenceKind.NO_EVIDENCE_YET, EvidenceKind.DOCUMENTS],
        )


def test_json_operations_use_the_same_typed_router() -> None:
    """Give agents parity with the rendered dashboard without a second rule path."""
    catalog = catalog_payload()
    assert catalog["schema_version"] == "method_dashboard.v2"
    status, result = route_payload(_example("program_failure").model_dump(mode="json"))
    assert status == HTTPStatus.OK
    assert result["routes"]
    invalid_status, invalid = route_payload({"question": "too short"})
    assert invalid_status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert invalid["error"] == "The study brief needs correction."


def test_html_exposes_truthful_primary_action_and_views() -> None:
    """Keep the first viewport about researcher intent rather than internal IDs."""
    html = HTML_PATH.read_text(encoding="utf-8")
    assert "Choose an analytical approach without losing sight of the evidence." in html
    assert "Plan an analysis" in html
    assert "Show possible approaches" in html
    assert "See a completed decision example" in html
    assert "does not yet run the selected methods" in html
    assert "Inspectable study map" in html
    assert "What best describes your current situation?" in html
    assert "What will you study or compare?" in html
    assert "What material do you already have?" in html
    assert "Understand what it means to people" in html
    assert "help-trigger" in html
    assert "role=\"tooltip\"" in html
    assert "Source of leverage" not in html
    assert "Explore methods" in html
    assert "nav-advanced" in html
    assert "Architecture" in html
    assert "Stress tests" in html
    assert "Stop rule against taxonomy sprawl" in html
    assert "no universally best method" in html
    assert "Run all methods" not in html
    assert "generic confidence" not in html.lower()
