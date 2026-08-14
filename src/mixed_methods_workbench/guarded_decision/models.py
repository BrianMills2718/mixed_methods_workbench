"""Strict owner-local contracts for the Plan 242 guarded-decision experiment."""

from __future__ import annotations

import hashlib
import json
import unicodedata
from enum import StrEnum
from typing import Annotated

from data_contracts.composition import ExecutionResult, OutcomeKind, ProposedTransition
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Digest = Annotated[str, StringConstraints(pattern=r"^sha256:[a-f0-9]{64}$")]


def canonical_digest(value: BaseModel) -> str:
    encoded = canonical_json_bytes(value.model_dump(mode="json"))
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def canonical_json_bytes(value: object) -> bytes:
    """Serialize the bounded plan242-json-v1 profile."""

    def normalize(item: object) -> object:
        if isinstance(item, str):
            return unicodedata.normalize("NFC", item)
        if isinstance(item, float):
            raise TypeError("plan242-json-v1 forbids floating-point values")
        if isinstance(item, dict):
            return {normalize(key): normalize(nested) for key, nested in item.items()}
        if isinstance(item, (list, tuple)):
            return [normalize(nested) for nested in item]
        return item

    return json.dumps(
        normalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


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


class PolicyManifest(FrozenModel):
    """Exact native policy sources bound by the plan242-json-v1 profile."""

    canonicalization_profile: str = Field(pattern=r"^plan242-json-v1$")
    policy_name: str = Field(min_length=1)
    repository_revision: str = Field(pattern=r"^[a-f0-9]{40}$")
    source_bindings: tuple[ArtifactBinding, ...]

    @model_validator(mode="after")
    def canonical_sources(self) -> PolicyManifest:
        refs = tuple(binding.ref for binding in self.source_bindings)
        if refs != tuple(sorted(set(refs))):
            raise ValueError("source_bindings must be sorted and duplicate-free")
        if not refs:
            raise ValueError("policy manifest requires at least one source binding")
        return self


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
        if self.proposed_transition.outcome is not OutcomeKind.EXECUTION_SUCCEEDED:
            raise ValueError("candidate proposed_transition must represent execution success")
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
    composition_contract_revision: str = Field(min_length=40, max_length=40)
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
        expected_execution = (
            OutcomeKind.EXECUTION_SUCCEEDED if validated else OutcomeKind.EXECUTION_FAILED
        )
        if self.receipt.execution_result.outcome is not expected_execution:
            raise ValueError("receipt execution outcome does not match guarded result")
        if self.receipt.native_disposition_ref != self.native_disposition_ref:
            raise ValueError("receipt native disposition does not match guarded result")
        normalized_reasons = tuple(
            f"{code}/1" if "/" not in code else code for code in self.semantic_reason_codes
        )
        if self.receipt.execution_result.reason_ids != normalized_reasons:
            raise ValueError("receipt execution reasons do not match guarded result")
        if self.receipt_ref != canonical_digest(self.receipt):
            raise ValueError("receipt_ref must bind the exact receipt")
        return self
