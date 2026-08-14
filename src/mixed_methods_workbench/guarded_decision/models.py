"""Strict owner-local contracts for the Plan 242 guarded-decision experiment."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated

from data_contracts.composition import ExecutionResult, ProposedTransition
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Digest = Annotated[str, StringConstraints(pattern=r"^sha256:[a-f0-9]{64}$")]


class FrozenModel(BaseModel):
    """Reject undeclared fields and mutation at the provisional seam."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class ArtifactBinding(FrozenModel):
    """An opaque native reference bound to exact bytes."""

    ref: str = Field(min_length=1)
    content_digest: Digest


class PolicyBinding(FrozenModel):
    """Exact identity of the native rules governing one dispatch."""

    policy_id: str = Field(min_length=1)
    policy_version: str = Field(min_length=1)
    policy_content_digest: Digest


class GuardedDecisionRequest(FrozenModel):
    """The frozen neutral request; it contains no method discriminator."""

    request_id: str = Field(min_length=1)
    target: ArtifactBinding
    prior_state: ArtifactBinding
    policy: PolicyBinding
    decision_record: ArtifactBinding
    decision_actor_or_system_ref: str = Field(min_length=1)
    proposed_transition: ProposedTransition
    required_evidence_refs: tuple[str, ...] = ()

    @model_validator(mode="after")
    def canonical_evidence(self) -> GuardedDecisionRequest:
        if tuple(sorted(set(self.required_evidence_refs))) != self.required_evidence_refs:
            raise ValueError("required_evidence_refs must be canonical and duplicate-free")
        return self


class GuardedDecisionOutcome(StrEnum):
    VALIDATED = "validated"
    REFUSED = "refused"
    UNRESOLVED = "unresolved"
    FAILED = "failed"


class NativeDecision(FrozenModel):
    """Facts returned by a method-owned callback after native validation."""

    outcome: GuardedDecisionOutcome
    native_disposition_ref: str | None = None
    semantic_reason_codes: tuple[str, ...] = ()

    @model_validator(mode="after")
    def outcome_shape(self) -> NativeDecision:
        if tuple(sorted(set(self.semantic_reason_codes))) != self.semantic_reason_codes:
            raise ValueError("semantic_reason_codes must be canonical and duplicate-free")
        if self.outcome is GuardedDecisionOutcome.VALIDATED and self.semantic_reason_codes:
            raise ValueError("validated native decision cannot carry refusal reasons")
        if self.outcome is not GuardedDecisionOutcome.VALIDATED and not self.semantic_reason_codes:
            raise ValueError("non-validated native decision requires semantic_reason_codes")
        return self


class GuardedDecisionReceipt(FrozenModel):
    """Neutral traversal receipt; native artifacts remain authoritative."""

    request_digest: Digest
    target_content_digest: Digest
    policy_content_digest: Digest
    decision_record_digest: Digest
    traversed_boundaries: tuple[str, ...]
    execution_result: ExecutionResult
    native_disposition_ref: str | None = None


class GuardedDecisionResult(FrozenModel):
    outcome: GuardedDecisionOutcome
    proposed_transition: ProposedTransition | None = None
    native_disposition_ref: str | None = None
    receipt_ref: Digest
    receipt: GuardedDecisionReceipt
    semantic_reason_codes: tuple[str, ...] = ()

    @model_validator(mode="after")
    def outcome_shape(self) -> GuardedDecisionResult:
        validated = self.outcome is GuardedDecisionOutcome.VALIDATED
        if validated and self.proposed_transition is None:
            raise ValueError("validated result requires proposed_transition")
        if validated and self.semantic_reason_codes:
            raise ValueError("validated result cannot carry refusal reasons")
        if not validated and self.proposed_transition is not None:
            raise ValueError("non-validated result cannot propose a transition")
        if not validated and not self.semantic_reason_codes:
            raise ValueError("non-validated result requires semantic_reason_codes")
        return self
