"""Focused checks for the bounded Process Tracing topology consumer."""

from __future__ import annotations

from copy import deepcopy

import pytest
from pydantic import ValidationError

from mixed_methods_workbench.method_topology import (
    EXPECTED_FIXTURE_SHA256,
    PRODUCER_REVISION,
    ConnectionKind,
    MethodTopologyProjection,
    load_process_tracing_topology,
    process_tracing_topology_payload,
)


def test_pinned_method_owned_topology_loads_with_all_material_shapes() -> None:
    artifact = load_process_tracing_topology()

    assert artifact.custody.producer_revision == PRODUCER_REVISION
    assert artifact.custody.artifact_sha256 == EXPECTED_FIXTURE_SHA256
    assert artifact.custody.relationship == "hash_bound_derived_fixture"
    assert {connection.connection_kind for connection in artifact.topology.connections} == set(
        ConnectionKind
    )
    assert {outcome.outcome_kind for outcome in artifact.topology.terminal_outcomes} == {
        "bounded_result",
        "qualified_result",
        "refusal",
        "acquisition_agenda",
    }
    assert any(
        connection.connection_kind is ConnectionKind.FEEDBACK
        and connection.creates_successor_version
        for connection in artifact.topology.connections
    )


def test_topology_rejects_missing_feedback_semantics() -> None:
    raw = load_process_tracing_topology().topology.model_dump(mode="json")
    corrupted = deepcopy(raw)
    corrupted["connections"] = [
        connection
        for connection in corrupted["connections"]
        if connection["connection_kind"] != "feedback"
    ]

    with pytest.raises(ValidationError, match="every declared connection kind"):
        MethodTopologyProjection.model_validate(corrupted)


def test_topology_rejects_dangling_connection_endpoint() -> None:
    raw = load_process_tracing_topology().topology.model_dump(mode="json")
    corrupted = deepcopy(raw)
    corrupted["connections"][0]["target_ref"] = "pt.move.nonexistent"

    with pytest.raises(ValidationError, match="endpoint"):
        MethodTopologyProjection.model_validate(corrupted)


def test_agent_payload_matches_browser_contract() -> None:
    payload = process_tracing_topology_payload()

    assert payload["custody"]["producer_revision"] == PRODUCER_REVISION
    assert payload["topology"]["method_id"] == (
        "process_tracing.single_case_rival_explanations"
    )
    assert len(payload["topology"]["moves"]) == 14
    assert len(payload["topology"]["connections"]) == 30
