"""Typed consumer for one method-owned Process Tracing topology projection.

This is a deliberately narrow Workbench adapter. Process Tracing owns the
method record and its semantics; the Workbench verifies the pinned artifact and
adds only producer custody needed by the local review surface.
"""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "fixtures"
    / "method_topology"
    / "process_tracing_v0_1.json"
)
PRODUCER_REPOSITORY = "BrianMills2718/process_tracing"
PRODUCER_REVISION = "928bb55d15b182ac23dedd96c38b9d22f6be3068"
EXPECTED_FIXTURE_SHA256 = "fbabaddb3b2d0316c542d98fa6ed9e9fa0bcabdb07fb8820c34fc91a8c0c4cbf"


class TopologyModel(BaseModel):
    """Reject undeclared fields and accidental mutation at this seam."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class ConnectionKind(StrEnum):
    """Meanings of connections in the method-owned topology."""

    ARTIFACT_FLOW = "artifact_flow"
    CONTROL_GATE = "control_gate"
    FEEDBACK = "feedback"
    RETAINED_CONTEXT = "retained_context"
    PROHIBITED_TRANSITION = "prohibited_transition"


class ImplementationStatus(StrEnum):
    """Observed realization state, kept separate from methodological validity."""

    IMPLEMENTED = "implemented"
    IMPLEMENTED_CONDITIONALLY = "implemented_conditionally"
    HUMAN_REVIEW_AVAILABLE = "human_review_available"


class ReuseDisposition(StrEnum):
    """Producer-owned reuse hypothesis, never an adopted shared capability."""

    METHOD_OWNED = "method_owned"
    SHARED_SHELL_CANDIDATE = "shared_shell_candidate"
    SHARED_MECHANIC_CANDIDATE = "shared_mechanic_candidate"


class MethodPhase(TopologyModel):
    phase_id: str
    label: str
    order: int = Field(ge=1)
    purpose: str


class AnalyticalMove(TopologyModel):
    move_id: str
    phase_id: str
    label: str
    purpose: str
    inputs: list[str] = Field(min_length=1)
    output: str
    method_owned_rule: str
    permitted_conclusion: str
    refusal_or_qualification: str
    performer: str
    judgment_owner: str
    implementation_status: ImplementationStatus
    reuse_disposition: ReuseDisposition
    implementation_refs: list[str] = Field(min_length=1)


class ExecutionAction(TopologyModel):
    action_id: str
    parent_move_id: str
    label: str
    performer: str
    implementation_ref: str


class TerminalOutcome(TopologyModel):
    outcome_id: str
    outcome_kind: Literal[
        "bounded_result", "qualified_result", "refusal", "acquisition_agenda"
    ]
    label: str
    meaning: str


class TopologyConnection(TopologyModel):
    connection_id: str
    connection_kind: ConnectionKind
    source_ref: str
    target_ref: str
    label: str
    condition: str
    creates_successor_version: bool


class MethodTopologyProjection(TopologyModel):
    """Strict projection of the producer-owned PT record used by this PoC."""

    schema_version: Literal["pt.method_topology.v0.1"]
    record_version: Literal["0.1.0"]
    method_id: Literal["process_tracing.single_case_rival_explanations"]
    label: str
    variant: str
    status: Literal["reviewed_prototype_fixture"]
    summary: str
    phases: list[MethodPhase] = Field(min_length=1)
    moves: list[AnalyticalMove] = Field(min_length=1)
    execution_actions: list[ExecutionAction]
    terminal_outcomes: list[TerminalOutcome] = Field(min_length=1)
    connections: list[TopologyConnection] = Field(min_length=1)
    source_authority_refs: list[str] = Field(min_length=1)
    claim_limits: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def require_coherent_topology(self) -> MethodTopologyProjection:
        phase_ids = [phase.phase_id for phase in self.phases]
        move_ids = [move.move_id for move in self.moves]
        outcome_ids = [outcome.outcome_id for outcome in self.terminal_outcomes]
        connection_ids = [connection.connection_id for connection in self.connections]
        action_ids = [action.action_id for action in self.execution_actions]
        for label, identifiers in (
            ("phase", phase_ids),
            ("move", move_ids),
            ("outcome", outcome_ids),
            ("connection", connection_ids),
            ("action", action_ids),
        ):
            if len(identifiers) != len(set(identifiers)):
                raise ValueError(f"{label} identifiers must be unique")

        phase_set = set(phase_ids)
        move_set = set(move_ids)
        node_set = move_set | set(outcome_ids)
        if {move.phase_id for move in self.moves} - phase_set:
            raise ValueError("every move must reference a declared phase")
        if {action.parent_move_id for action in self.execution_actions} - move_set:
            raise ValueError("every execution action must reference a declared move")
        for connection in self.connections:
            if connection.source_ref not in node_set or connection.target_ref not in node_set:
                raise ValueError("every connection endpoint must reference a declared node")
            if connection.connection_kind is ConnectionKind.FEEDBACK:
                if not connection.creates_successor_version:
                    raise ValueError("feedback must create an explicit successor version")
            elif connection.creates_successor_version:
                raise ValueError("only feedback may create a successor version")

        represented_kinds = {connection.connection_kind for connection in self.connections}
        if represented_kinds != set(ConnectionKind):
            raise ValueError("the review fixture must exercise every declared connection kind")
        if not any(outcome.outcome_kind == "refusal" for outcome in self.terminal_outcomes):
            raise ValueError("the topology must expose a method-owned refusal outcome")
        return self


class TopologyCustody(TopologyModel):
    """Workbench custody for the exact producer artifact consumed here."""

    producer_repository: Literal["BrianMills2718/process_tracing"]
    producer_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    artifact_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    relationship: Literal["hash_bound_derived_fixture"]


class MethodTopologyArtifact(TopologyModel):
    custody: TopologyCustody
    topology: MethodTopologyProjection


def load_process_tracing_topology() -> MethodTopologyArtifact:
    """Load the exact producer record and fail if its bytes or semantics drift."""

    fixture_bytes = FIXTURE_PATH.read_bytes()
    digest = hashlib.sha256(fixture_bytes).hexdigest()
    if digest != EXPECTED_FIXTURE_SHA256:
        raise ValueError("Process Tracing topology fixture SHA-256 does not match")
    topology = MethodTopologyProjection.model_validate(json.loads(fixture_bytes))
    return MethodTopologyArtifact(
        custody=TopologyCustody(
            producer_repository="BrianMills2718/process_tracing",
            producer_revision=PRODUCER_REVISION,
            artifact_sha256=digest,
            relationship="hash_bound_derived_fixture",
        ),
        topology=topology,
    )


def process_tracing_topology_payload() -> dict[str, object]:
    """Return the same typed topology consumed by the browser."""

    return load_process_tracing_topology().model_dump(mode="json")
