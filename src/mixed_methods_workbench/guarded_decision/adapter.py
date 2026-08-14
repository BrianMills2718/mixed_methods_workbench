"""Dispatch-neutral guarded-decision mechanics for the registered Plan 242 test."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping

from data_contracts.composition import ExecutionResult, OutcomeKind
from pydantic import BaseModel

from .models import (
    GuardedDecisionOutcome,
    GuardedDecisionReceipt,
    GuardedDecisionRequest,
    GuardedDecisionResult,
    NativeDecision,
)

ContentResolver = Callable[[str], bytes]
NativePolicy = Callable[[GuardedDecisionRequest], NativeDecision]


def sha256_bytes(content: bytes) -> str:
    return f"sha256:{hashlib.sha256(content).hexdigest()}"


def fingerprint(value: object) -> str:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json")
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8")
    return sha256_bytes(encoded)


def mapping_resolver(contents: Mapping[str, bytes]) -> ContentResolver:
    """Build a fail-loud exact-reference resolver for tests and local integrations."""

    def resolve(ref: str) -> bytes:
        try:
            return contents[ref]
        except KeyError as exc:
            raise LookupError(f"unresolved artifact reference: {ref}") from exc

    return resolve


def execute_guarded_decision(
    request: GuardedDecisionRequest,
    *,
    resolve_content: ContentResolver,
    native_policy: NativePolicy,
) -> GuardedDecisionResult:
    """Verify exact bindings, dispatch once, and preserve the native disposition."""

    request_digest = fingerprint(request)
    mismatches: list[str] = []
    for label, ref, expected in (
        ("target", request.target.ref, request.target.content_digest),
        ("prior_state", request.prior_state.ref, request.prior_state.content_digest),
        ("policy", request.policy.policy_id, request.policy.policy_content_digest),
        ("decision_record", request.decision_record.ref, request.decision_record.content_digest),
    ):
        try:
            actual = sha256_bytes(resolve_content(ref))
        except LookupError:
            mismatches.append(f"guarded-decision.unresolved-{label}/1")
            continue
        if actual != expected:
            mismatches.append(f"guarded-decision.{label}-digest-mismatch/1")

    for ref in request.required_evidence_refs:
        try:
            resolve_content(ref)
        except LookupError:
            mismatches.append("guarded-decision.unresolved-evidence/1")

    if mismatches:
        return _result(
            request=request,
            request_digest=request_digest,
            decision=NativeDecision(
                outcome=GuardedDecisionOutcome.REFUSED,
                semantic_reason_codes=tuple(sorted(set(mismatches))),
            ),
            traversed=("neutral_binding",),
        )

    decision = native_policy(request)
    return _result(
        request=request,
        request_digest=request_digest,
        decision=decision,
        traversed=("neutral_binding", "native_policy"),
    )


def _result(
    *,
    request: GuardedDecisionRequest,
    request_digest: str,
    decision: NativeDecision,
    traversed: tuple[str, ...],
) -> GuardedDecisionResult:
    outcome_map = {
        GuardedDecisionOutcome.VALIDATED: OutcomeKind.EXECUTION_SUCCEEDED,
        GuardedDecisionOutcome.REFUSED: OutcomeKind.INVOCATION_REJECTED,
        GuardedDecisionOutcome.UNRESOLVED: OutcomeKind.EXECUTION_FAILED,
        GuardedDecisionOutcome.FAILED: OutcomeKind.EXECUTION_FAILED,
    }
    reasons = tuple(f"{code}/1" if "/" not in code else code for code in decision.semantic_reason_codes)
    execution = ExecutionResult(
        execution_id=f"guarded-decision:{request.request_id}",
        invocation_fingerprint=request_digest,
        outcome=outcome_map[decision.outcome],
        reason_ids=reasons,
    )
    receipt = GuardedDecisionReceipt(
        request_digest=request_digest,
        target_content_digest=request.target.content_digest,
        policy_content_digest=request.policy.policy_content_digest,
        decision_record_digest=request.decision_record.content_digest,
        traversed_boundaries=traversed,
        execution_result=execution,
        native_disposition_ref=decision.native_disposition_ref,
    )
    proposed = request.proposed_transition if decision.outcome is GuardedDecisionOutcome.VALIDATED else None
    return GuardedDecisionResult(
        outcome=decision.outcome,
        proposed_transition=proposed,
        native_disposition_ref=decision.native_disposition_ref,
        receipt_ref=fingerprint(receipt),
        receipt=receipt,
        semantic_reason_codes=decision.semantic_reason_codes,
    )
