"""Focused controls for the bounded evidence-anchor capability candidate."""

from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from mixed_methods_workbench.capability_contract import (
    EXPECTED_FIXTURE_SHA256,
    EvidenceAnchorCompatibility,
    evidence_anchor_capability_payload,
    load_evidence_anchor_capability,
)


def test_two_authentic_methods_share_anchor_not_interpretation() -> None:
    artifact = load_evidence_anchor_capability()
    capability = artifact.capability
    demonstration = artifact.demonstration

    assert artifact.custody.artifact_sha256 == EXPECTED_FIXTURE_SHA256
    assert {adapter.method_id for adapter in capability.adapters} == {
        "grounded_theory",
        "process_tracing",
    }
    assert {record.method_id for record in demonstration.records} == {
        "grounded_theory",
        "process_tracing",
    }
    assert [len(record.anchors) for record in demonstration.records] == [4, 1]
    assert "what the passage means" in capability.deliberately_does_not_decide
    assert "whether it supports or challenges a claim" in (
        capability.deliberately_does_not_decide
    )
    for record in demonstration.records:
        assert set(record.method_specific_fields).isdisjoint(demonstration.shared_fields)


def test_corrupt_context_hash_fails_the_shared_capability() -> None:
    raw = load_evidence_anchor_capability().demonstration.model_dump(mode="json")
    corrupted = deepcopy(raw)
    corrupted["records"][0]["anchors"][0]["context_text_sha256"] = "0" * 64

    with pytest.raises(ValidationError, match="context_hash_mismatch"):
        EvidenceAnchorCompatibility.model_validate(corrupted)


def test_method_interpretation_cannot_enter_shared_anchor() -> None:
    raw = load_evidence_anchor_capability().demonstration.model_dump(mode="json")
    corrupted = deepcopy(raw)
    corrupted["shared_fields"].append("meaning")

    with pytest.raises(ValidationError, match="shared_fields_mismatch"):
        EvidenceAnchorCompatibility.model_validate(corrupted)


def test_one_method_cannot_claim_cross_method_compatibility() -> None:
    raw = load_evidence_anchor_capability().demonstration.model_dump(mode="json")
    corrupted = deepcopy(raw)
    corrupted["records"] = [corrupted["records"][0], corrupted["records"][0]]

    with pytest.raises(ValidationError, match="comparison_requires_both_methods"):
        EvidenceAnchorCompatibility.model_validate(corrupted)


def test_agent_payload_matches_the_browser_contract() -> None:
    payload = evidence_anchor_capability_payload()

    assert payload["capability"]["capability_id"] == "evidence.anchor"
    assert payload["capability"]["maturity"] == (
        "candidate_compatible_two_method_probe"
    )
    assert len(payload["demonstration"]["shared_fields"]) == 13
