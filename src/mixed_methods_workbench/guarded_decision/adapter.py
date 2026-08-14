"""Dispatch-neutral guarded-decision mechanics for the registered Plan 242 test."""

from __future__ import annotations

import hashlib
import subprocess
from collections.abc import Callable, Mapping
from pathlib import Path

import data_contracts.composition as composition_contract
from data_contracts.composition import ExecutionResult, OutcomeKind
from pydantic import BaseModel

from .models import (
    ArtifactBinding,
    GuardedDecisionEvidenceBundle,
    GuardedDecisionOutcome,
    GuardedDecisionReceipt,
    GuardedDecisionRequest,
    GuardedDecisionResult,
    NativeDecision,
    NativeExecutionEvidenceManifest,
    PolicyManifest,
    canonical_digest,
    canonical_json_bytes,
)

ContentResolver = Callable[[str], bytes]
NativePolicy = Callable[[GuardedDecisionRequest], NativeDecision]


def sha256_bytes(content: bytes) -> str:
    return f"sha256:{hashlib.sha256(content).hexdigest()}"


def fingerprint(value: BaseModel) -> str:
    return canonical_digest(value)


def observed_composition_contract_revision() -> str:
    """Bind receipts to the actually imported, tracked composition package."""

    module_path = Path(composition_contract.__file__).resolve()
    try:
        repo_root = Path(
            subprocess.check_output(
                ["git", "-C", str(module_path.parent), "rev-parse", "--show-toplevel"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        )
        relative_package = module_path.parent.relative_to(repo_root)
        revision = subprocess.check_output(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        dirty = subprocess.check_output(
            ["git", "-C", str(repo_root), "status", "--porcelain", "--", str(relative_package)],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, ValueError) as exc:
        raise RuntimeError("cannot verify imported Data Contracts revision") from exc
    if dirty:
        raise RuntimeError("imported Data Contracts composition package differs from HEAD")
    return revision


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
    composition_contract_revision = observed_composition_contract_revision()
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

    for binding in request.required_evidence_bindings:
        try:
            actual = sha256_bytes(resolve_content(binding.artifact.ref))
        except LookupError:
            mismatches.append("guarded-decision.unresolved-evidence/1")
            continue
        if actual != binding.artifact.content_digest:
            mismatches.append("guarded-decision.evidence-digest-mismatch/1")
            continue
        if binding.role == "native_execution_manifest":
            mismatches.extend(
                _verify_native_execution_manifest(
                    binding.artifact,
                    request=request,
                    resolve_content=resolve_content,
                )
            )

    try:
        policy_bytes = resolve_content(request.policy.policy_id)
        policy_manifest = PolicyManifest.model_validate_json(policy_bytes)
        if canonical_json_bytes(policy_manifest.model_dump(mode="json")) != policy_bytes:
            mismatches.append("guarded-decision.policy-manifest-noncanonical/1")
        for source_binding in policy_manifest.source_bindings:
            try:
                actual = sha256_bytes(resolve_content(source_binding.ref))
            except LookupError:
                mismatches.append("guarded-decision.unresolved-policy-source/1")
                continue
            if actual != source_binding.content_digest:
                mismatches.append("guarded-decision.policy-source-digest-mismatch/1")
    except (LookupError, ValueError):
        mismatches.append("guarded-decision.policy-manifest-invalid/1")

    if request.proposed_transition.prior_state_fingerprint != request.prior_state.content_digest:
        mismatches.append("guarded-decision.transition-prior-state-mismatch/1")
    if mismatches:
        return _result(
            request=request,
            request_digest=request_digest,
            decision=NativeDecision(
                outcome=GuardedDecisionOutcome.REFUSED,
                semantic_reason_codes=tuple(sorted(set(mismatches))),
            ),
            traversed=("neutral_binding",),
            composition_contract_revision=composition_contract_revision,
        )

    decision = native_policy(request)
    manifests = tuple(
        binding
        for binding in request.required_evidence_bindings
        if binding.role == "native_execution_manifest"
    )
    if manifests:
        execution_manifest = NativeExecutionEvidenceManifest.model_validate_json(
            resolve_content(manifests[0].artifact.ref)
        )
        if execution_manifest.native_disposition_ref != decision.native_disposition_ref:
            decision = NativeDecision(
                outcome=GuardedDecisionOutcome.REFUSED,
                semantic_reason_codes=(
                    "guarded-decision.execution-manifest-disposition-mismatch/1",
                ),
            )
    return _result(
        request=request,
        request_digest=request_digest,
        decision=decision,
        traversed=("neutral_binding", "native_policy"),
        composition_contract_revision=composition_contract_revision,
    )


def _result(
    *,
    request: GuardedDecisionRequest,
    request_digest: str,
    decision: NativeDecision,
    traversed: tuple[str, ...],
    composition_contract_revision: str,
) -> GuardedDecisionResult:
    outcome_map = {
        GuardedDecisionOutcome.VALIDATED: OutcomeKind.EXECUTION_SUCCEEDED,
        GuardedDecisionOutcome.REFUSED: OutcomeKind.EXECUTION_FAILED,
        GuardedDecisionOutcome.UNRESOLVED: OutcomeKind.EXECUTION_FAILED,
        GuardedDecisionOutcome.FAILED: OutcomeKind.EXECUTION_FAILED,
    }
    reasons = tuple(
        f"{code}/1" if "/" not in code else code for code in decision.semantic_reason_codes
    )
    execution = ExecutionResult(
        execution_id=f"guarded-decision:{request.request_id}",
        invocation_fingerprint=request_digest,
        outcome=outcome_map[decision.outcome],
        reason_ids=reasons,
    )
    receipt = GuardedDecisionReceipt(
        request_digest=request_digest,
        composition_contract_revision=composition_contract_revision,
        target_content_digest=request.target.content_digest,
        policy_content_digest=request.policy.policy_content_digest,
        decision_record_digest=request.decision_record.content_digest,
        evidence_bindings=request.required_evidence_bindings,
        traversed_boundaries=traversed,
        execution_result=execution,
        native_disposition_ref=decision.native_disposition_ref,
    )
    proposed = (
        request.proposed_transition
        if decision.outcome is GuardedDecisionOutcome.VALIDATED
        else None
    )
    return GuardedDecisionResult(
        outcome=decision.outcome,
        proposed_transition=proposed,
        native_disposition_ref=decision.native_disposition_ref,
        receipt_ref=fingerprint(receipt),
        receipt=receipt,
        semantic_reason_codes=decision.semantic_reason_codes,
    )


def _verify_native_execution_manifest(
    binding: ArtifactBinding,
    *,
    request: GuardedDecisionRequest,
    resolve_content: ContentResolver,
) -> list[str]:
    """Verify generic execution-evidence structure and transitive custody."""

    artifact = binding
    try:
        manifest_bytes = resolve_content(artifact.ref)
        manifest = NativeExecutionEvidenceManifest.model_validate_json(manifest_bytes)
        if canonical_json_bytes(manifest.model_dump(mode="json")) != manifest_bytes:
            return ["guarded-decision.execution-manifest-noncanonical/1"]
    except (LookupError, ValueError):
        return ["guarded-decision.execution-manifest-invalid/1"]

    reasons: list[str] = []
    if manifest.target_binding != request.target:
        reasons.append("guarded-decision.execution-manifest-target-mismatch/1")
    if manifest.decision_record_binding != request.decision_record:
        reasons.append("guarded-decision.execution-manifest-decision-mismatch/1")
    transitive = [("native-output", manifest.native_output_binding)]
    if manifest.trace_binding is not None:
        transitive.append(
            ("trace-store-snapshot", manifest.trace_binding.trace_store_snapshot_binding)
        )
    for label, nested in transitive:
        try:
            actual = sha256_bytes(resolve_content(nested.ref))
        except LookupError:
            reasons.append(f"guarded-decision.unresolved-{label}/1")
            continue
        if actual != nested.content_digest:
            reasons.append(f"guarded-decision.{label}-digest-mismatch/1")
    return reasons


def verify_evidence_bundle(
    bundle: GuardedDecisionEvidenceBundle,
    *,
    resolve_content: ContentResolver,
    expected_bundle_digest: str | None = None,
) -> None:
    """Fail loud when a persisted bundle cannot be replayed byte-for-byte."""

    if expected_bundle_digest is not None and canonical_digest(bundle) != expected_bundle_digest:
        raise ValueError("bundle digest does not match canonical bundle bytes")
    manifest_reasons = _verify_native_execution_manifest(
        bundle.native_execution_manifest_binding,
        request=bundle.request,
        resolve_content=resolve_content,
    )
    evidence_reasons: list[str] = []
    for label, artifact in (
        ("target", bundle.request.target),
        ("prior-state", bundle.request.prior_state),
        ("decision-record", bundle.request.decision_record),
    ):
        try:
            actual = sha256_bytes(resolve_content(artifact.ref))
        except LookupError:
            evidence_reasons.append(f"guarded-decision.unresolved-{label}/1")
            continue
        if actual != artifact.content_digest:
            evidence_reasons.append(f"guarded-decision.{label}-digest-mismatch/1")
    try:
        policy_bytes = resolve_content(bundle.request.policy.policy_id)
        if sha256_bytes(policy_bytes) != bundle.request.policy.policy_content_digest:
            evidence_reasons.append("guarded-decision.policy-digest-mismatch/1")
        else:
            policy_manifest = PolicyManifest.model_validate_json(policy_bytes)
            if canonical_json_bytes(policy_manifest.model_dump(mode="json")) != policy_bytes:
                evidence_reasons.append("guarded-decision.policy-manifest-noncanonical/1")
            for source_binding in policy_manifest.source_bindings:
                try:
                    actual = sha256_bytes(resolve_content(source_binding.ref))
                except LookupError:
                    evidence_reasons.append("guarded-decision.unresolved-policy-source/1")
                    continue
                if actual != source_binding.content_digest:
                    evidence_reasons.append("guarded-decision.policy-source-digest-mismatch/1")
    except (LookupError, ValueError):
        evidence_reasons.append("guarded-decision.policy-manifest-invalid/1")
    for binding in bundle.resolved_evidence_bindings:
        try:
            actual = sha256_bytes(resolve_content(binding.artifact.ref))
        except LookupError:
            evidence_reasons.append("guarded-decision.unresolved-evidence/1")
            continue
        if actual != binding.artifact.content_digest:
            evidence_reasons.append("guarded-decision.evidence-digest-mismatch/1")
    manifest_bytes = resolve_content(bundle.native_execution_manifest_binding.ref)
    execution_manifest = NativeExecutionEvidenceManifest.model_validate_json(manifest_bytes)
    if execution_manifest.native_disposition_ref != bundle.native_disposition_ref:
        evidence_reasons.append("guarded-decision.execution-manifest-disposition-mismatch/1")
    reasons = tuple(sorted(set(manifest_reasons + evidence_reasons)))
    if reasons:
        raise ValueError("bundle custody verification failed: " + ", ".join(reasons))


def write_evidence_bundle(path: Path, bundle: GuardedDecisionEvidenceBundle) -> str:
    """Persist canonical bytes once; refuse to rewrite successor evidence in place."""

    payload = canonical_json_bytes(bundle.model_dump(mode="json"))
    digest = sha256_bytes(payload)
    if path.exists():
        if path.read_bytes() != payload:
            raise FileExistsError(f"refusing to replace immutable evidence bundle: {path}")
        return digest
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return digest


def load_evidence_bundle(path: Path) -> GuardedDecisionEvidenceBundle:
    """Load a canonical bundle and reject alternate byte serializations."""

    payload = path.read_bytes()
    bundle = GuardedDecisionEvidenceBundle.model_validate_json(payload)
    if canonical_json_bytes(bundle.model_dump(mode="json")) != payload:
        raise ValueError("evidence bundle is not canonical plan242-json-v1")
    return bundle
