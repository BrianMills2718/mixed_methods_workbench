import json
import shutil
from pathlib import Path

import pytest

from mixed_methods_workbench.nyc_crz_integrated import (
    FIXTURE_ROOT,
    NycCrzIntegrationError,
    load_accepted_qc,
    nyc_crz_integrated_payload,
)


def test_accepted_qc_binding_preserves_review_and_unresolved_state():
    handoff, review, binding = load_accepted_qc()
    assert binding["producer_revision"] == "5560ce71546a30dc6aa4a264dacbce3028b005eb"
    assert review.status == "human_review_approved"
    assert len(review.items) == 14
    assert sum(x.item_type == "substantive_finding" for x in review.items) == 12
    assert sum(x.item_type == "boundary_case" for x in review.items) == 1
    assert sum(x.item_type == "unresolved_negative_case_search" for x in review.items) == 1
    assert handoff.anchors


def test_digest_mutation_fails_closed(tmp_path: Path):
    target = tmp_path / "fixture"
    shutil.copytree(FIXTURE_ROOT, target)
    handoff = target / "qc" / "nyc_crz_describe_v1_handoff.json"
    handoff.write_text(handoff.read_text() + "\n", encoding="utf-8")
    with pytest.raises(NycCrzIntegrationError, match="digest mismatch"):
        load_accepted_qc(target)


def test_unapproved_review_fails_closed(tmp_path: Path):
    target = tmp_path / "fixture"
    shutil.copytree(FIXTURE_ROOT, target)
    binding_path = target / "qc_binding.json"
    binding = json.loads(binding_path.read_text())
    binding["review_state"] = "pending_human_review"
    binding_path.write_text(json.dumps(binding), encoding="utf-8")
    with pytest.raises(NycCrzIntegrationError, match="not human approved"):
        load_accepted_qc(target)


def test_integrated_payload_preserves_method_boundaries_and_no_recommendation():
    payload = nyc_crz_integrated_payload()
    assert payload["status"] == "integration_complete_pending_mvp_review"
    assert payload["qualitative"]["review_status"] == "human_review_approved"
    assert len(payload["qualitative"]["findings"]) == 12
    assert payload["qualitative"]["unresolved"]["item_type"] == "unresolved_negative_case_search"
    assert payload["policy_appraisal"]["status"] == "needs_human_priorities"
    assert payload["policy_appraisal"]["decision"] is None
    assert {x["kind"] for x in payload["integration"]} == {
        "convergence", "complementarity", "divergence", "silence"
    }
    limits = " ".join(payload["qualitative"]["claim_limits"]).lower()
    assert "prevalence" in limits or "representative" in limits
    assert payload["quantitative"]["claim_boundary"]["causal_status"] == "not_identified"


def test_federated_comparison_does_not_claim_method_validity_improvement():
    comparison = nyc_crz_integrated_payload()["baseline_vs_federated"]
    assert "underlying evidence quality" in comparison["does_not_improve"]
    assert "causal identification" in comparison["does_not_improve"]
    assert "policy value judgments or priority weights" in comparison["does_not_improve"]
