#!/usr/bin/env python3
"""Generate the four immutable Plan 242 registration@3 evidence bundles."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from itertools import combinations
from pathlib import Path

PT_PIN = "ce87f630546a9193c999943aeb3319940e89cc95"
QC_PIN = "68ac10eb3d7588bed547b89d58f0186db3f9ac85"
LLM_CLIENT_PIN = "16b9eb19ae6402c23271ee8384c0508dce0f5acd"
PT_TRACE_DB_DIGEST = "sha256:ee3c444b72cbf0b422e08caa3cf7a210f8dd931ac00d3df6f6f06a238bc4143b"
EXPECTED_QC_BUNDLE_DIGEST = "c135da965f0fa61da85aa49008c7fe93711368ac8422c5c83816c69a0346934f"


def _args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pt-root", type=Path, required=True)
    parser.add_argument("--qc-root", type=Path, required=True)
    parser.add_argument("--data-contracts-root", type=Path, required=True)
    parser.add_argument("--trace-db", type=Path, required=True)
    return parser.parse_args()


def _sha(content: bytes) -> str:
    return f"sha256:{hashlib.sha256(content).hexdigest()}"


def _write_once(path: Path, content: bytes) -> None:
    if path.exists():
        if path.read_bytes() != content:
            raise FileExistsError(f"refusing to rewrite evidence artifact: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def main() -> int:
    args = _args()
    repository_root = Path(__file__).resolve().parents[1]
    sys.path[:0] = [
        str(repository_root / "src"),
        str(args.data_contracts_root.resolve() / "src"),
        str(args.pt_root.resolve()),
        str(args.qc_root.resolve()),
    ]

    from data_contracts.composition import (
        ActionKind,
        ControlTransitionContract,
        ControlTransitionMode,
        DecisionSource,
        EffectKind,
        OutcomeKind,
        ProposedTransition,
    )
    from pt.pass_partition import (
        PartitionBlockedError,
        require_adequate_partition,
    )
    from pt.schemas import (
        HypothesisSpace,
        PartitionAudit,
        PredictionContrast,
        RivalPairAudit,
    )
    from qc_clean.core.f1_framing_review import (
        CellReviewDecision,
        DecisionUniverseMismatchError,
        F1CodingReviewPackage,
        finalize_f1_bundle,
        load_coding_review,
    )

    from mixed_methods_workbench.guarded_decision import (
        ArtifactBinding,
        EvidenceBinding,
        GuardedDecisionEvidenceBundle,
        GuardedDecisionOutcome,
        GuardedDecisionRequest,
        NativeDecision,
        NativeExecutionEvidenceManifest,
        NativeExecutionKind,
        PolicyBinding,
        PolicyManifest,
        TraceBinding,
        TraceStoreSnapshot,
        canonical_json_bytes,
        execute_guarded_decision,
        sha256_bytes,
        write_evidence_bundle,
    )

    evidence_root = repository_root / "docs/research/plan242/evidence"

    def ref(path: Path) -> str:
        return path.relative_to(repository_root).as_posix()

    def artifact(path: Path, content: bytes) -> ArtifactBinding:
        _write_once(path, content)
        return ArtifactBinding(ref=ref(path), content_digest=sha256_bytes(content))

    def policy(
        consumer: str,
        fixture_name: str,
        source_root: Path,
        source_prefix: str,
    ) -> tuple[PolicyBinding, dict[str, bytes]]:
        original = PolicyManifest.model_validate_json(
            (repository_root / "tests/fixtures/guarded_decision" / fixture_name).read_bytes()
        )
        bindings = []
        contents: dict[str, bytes] = {}
        for source in original.source_bindings:
            relative = source.ref.removeprefix(source_prefix)
            source_bytes = (source_root / relative).read_bytes()
            if sha256_bytes(source_bytes) != source.content_digest:
                raise RuntimeError(f"registered policy source drift: {source.ref}")
            copied = evidence_root / consumer / "policy_sources" / relative
            binding = artifact(copied, source_bytes)
            bindings.append(binding)
            contents[binding.ref] = source_bytes
        local_manifest = PolicyManifest(
            canonicalization_profile="plan242-json-v1",
            policy_name=original.policy_name,
            repository_revision=original.repository_revision,
            source_bindings=tuple(sorted(bindings, key=lambda item: item.ref)),
        )
        manifest_bytes = canonical_json_bytes(local_manifest.model_dump(mode="json"))
        manifest_path = evidence_root / consumer / "policy_manifest.json"
        manifest_binding = artifact(manifest_path, manifest_bytes)
        contents[manifest_binding.ref] = manifest_bytes
        return (
            PolicyBinding(
                policy_id=manifest_binding.ref,
                policy_version=original.repository_revision,
                policy_content_digest=manifest_binding.content_digest,
            ),
            contents,
        )

    def transition(state_digest: str, case_id: str) -> ProposedTransition:
        return ProposedTransition(
            transition_id=f"transition:{case_id}",
            invocation_id=f"invocation:{case_id}",
            manifest_digest="sha256:" + "2" * 64,
            pack_id="workbench.guarded-decision/1",
            pack_version="1.0.0",
            action_id="workbench.guarded-decision/1",
            descriptor_version="1.0.0",
            decision_source=DecisionSource.HARNESS,
            action_kind=ActionKind.CONTROL,
            control_transition=ControlTransitionContract(
                mode=ControlTransitionMode.STATE_PRESERVING
            ),
            effect_kind=EffectKind.PURE,
            outcome=OutcomeKind.EXECUTION_SUCCEEDED,
            prior_state_fingerprint=state_digest,
            resulting_state_fingerprint=state_digest,
        )

    def persist_case(
        *,
        consumer: str,
        case: str,
        target_bytes: bytes,
        decision_bytes: bytes,
        output_bytes: bytes,
        policy_binding: PolicyBinding,
        policy_contents: dict[str, bytes],
        execution_kind: NativeExecutionKind,
        native_disposition_ref: str,
        native_policy: object,
        trace_binding: TraceBinding | None = None,
        trace_bytes: bytes | None = None,
    ) -> str:
        case_root = evidence_root / consumer / case
        target_binding = artifact(case_root / "target.json", target_bytes)
        state_bytes = canonical_json_bytes({"case": case, "state": "native-decision-pending"})
        prior_binding = artifact(case_root / "prior_state.json", state_bytes)
        decision_binding = artifact(case_root / "decision_record.json", decision_bytes)
        output_binding = artifact(case_root / "native_output.json", output_bytes)
        contents = dict(policy_contents)
        contents.update(
            {
                target_binding.ref: target_bytes,
                prior_binding.ref: state_bytes,
                decision_binding.ref: decision_bytes,
                output_binding.ref: output_bytes,
            }
        )
        if trace_binding is not None:
            assert trace_bytes is not None
            contents[trace_binding.trace_store_snapshot_binding.ref] = trace_bytes
        manifest = NativeExecutionEvidenceManifest(
            schema_version="plan242-native-execution-evidence/1",
            consumer_id=consumer,
            consumer_revision=PT_PIN if consumer == "process_tracing" else QC_PIN,
            execution_kind=execution_kind,
            target_binding=target_binding,
            decision_record_binding=decision_binding,
            native_output_binding=output_binding,
            native_disposition_ref=native_disposition_ref,
            trace_binding=trace_binding,
        )
        manifest_bytes = canonical_json_bytes(manifest.model_dump(mode="json"))
        manifest_binding = artifact(case_root / "native_execution_manifest.json", manifest_bytes)
        contents[manifest_binding.ref] = manifest_bytes
        request = GuardedDecisionRequest(
            request_id=f"plan242-{consumer}-{case}",
            target=target_binding,
            prior_state=prior_binding,
            policy=policy_binding,
            decision_record=decision_binding,
            decision_actor_or_system_ref=f"{consumer}:native-gate",
            proposed_transition=transition(prior_binding.content_digest, f"{consumer}-{case}"),
            required_evidence_bindings=(
                EvidenceBinding(role="native_execution_manifest", artifact=manifest_binding),
            ),
        )
        result = execute_guarded_decision(
            request,
            resolve_content=lambda artifact_ref: contents[artifact_ref],
            native_policy=native_policy,
        )
        bundle = GuardedDecisionEvidenceBundle(
            bundle_version="plan242-guarded-decision-bundle/1",
            request=request,
            result_and_receipt=result,
            native_execution_manifest_binding=manifest_binding,
            resolved_evidence_bindings=request.required_evidence_bindings,
            native_disposition_ref=result.native_disposition_ref,
        )
        digest = write_evidence_bundle(case_root / "bundle.json", bundle)
        _write_once(case_root / "bundle.sha256", f"{digest}\n".encode())
        return digest

    pt_policy, pt_policy_contents = policy(
        "process_tracing",
        "process_tracing_partition_gate_policy.json",
        args.pt_root,
        "pt:source:",
    )
    qc_policy, qc_policy_contents = policy(
        "qualitative_coding",
        "qualitative_coding_f1_finalization_policy.json",
        args.qc_root,
        "qc:source:",
    )

    def pair(h1: str, h2: str, p1: str, p2: str) -> RivalPairAudit:
        return RivalPairAudit(
            h1_id=h1,
            h2_id=h2,
            overlap_concern=False,
            complementary_concern=False,
            absorptive_concern=False,
            prediction_contrasts=[
                PredictionContrast(
                    h1_prediction_id=p1,
                    h2_prediction_id=p2,
                    contrast_dimension="mechanism",
                    reasoning="The predictions imply opposed observable traces.",
                )
            ],
            concern_detail="",
        )

    database_bytes = args.trace_db.read_bytes()
    if _sha(database_bytes) != PT_TRACE_DB_DIGEST:
        raise RuntimeError("retained PT trace store bytes drifted")
    connection = sqlite3.connect(f"file:{args.trace_db.resolve()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    row = connection.execute(
        "select id,timestamp,project,model,response,caller,task,trace_id,"
        "call_fingerprint,call_snapshot,logical_call_id,execution_path,retry_count,"
        "schema_hash,response_format_type,error,finish_reason from llm_calls where id=4"
    ).fetchone()
    if row is None:
        raise RuntimeError("retained PT trace row 4 is missing")
    frozen_trace_fields = {
        "trace_id": "plan242-d/pt-partition-ce87f630-20260814-b",
        "logical_call_id": "llmcall_4b47ed335b2d47b5abb7830565d9f954",
        "call_fingerprint": "58deb67e724113a93fceee4fd2cd2f27f025a3beff3e4ffd08326af0f6fe4d51",
        "model": "openrouter/openai/gpt-5.6-luna",
    }
    for field, expected in frozen_trace_fields.items():
        if row[field] != expected:
            raise RuntimeError(f"retained PT trace {field} drifted")
    if _sha(row["response"].encode()) != (
        "sha256:b64cb12bfa0fa55b8ae59f6fa492140b31a2cc66026a77f195be5ad487a1bf8a"
    ):
        raise RuntimeError("retained PT response bytes drifted")
    call_snapshot = json.loads(row["call_snapshot"])
    user_message = call_snapshot["request"]["messages"][1]["content"]
    hypothesis_marker = user_message.index("## Hypothesis Space")
    hypothesis_start = user_message.index("{", hypothesis_marker)
    hypothesis_payload, _ = json.JSONDecoder().raw_decode(user_message[hypothesis_start:])
    space = HypothesisSpace.model_validate(hypothesis_payload)
    space_bytes = canonical_json_bytes(space.model_dump(mode="json"))
    if (
        _sha(space_bytes)
        != "sha256:ed574377017db1ba7816b75ce628cd3eae4aea31ca6ac522f9b43bf83b155fa2"
    ):
        raise RuntimeError("authentic PT target reconstruction drifted")
    positive_audit = PartitionAudit.model_validate_json(row["response"])
    require_adequate_partition(space, positive_audit)
    positive_audit_bytes = canonical_json_bytes(positive_audit.model_dump(mode="json"))
    if (
        _sha(positive_audit_bytes)
        != "sha256:ac587b2934a0b20c521a614a97eb8a8af0ed2d0af9a9074f61aa3bc0cb2c1a7f"
    ):
        raise RuntimeError("authentic PT audit reconstruction drifted")
    snapshot = TraceStoreSnapshot(
        schema_version="plan242-trace-store-snapshot/1",
        source_store_digest=_sha(database_bytes),
        source_row_id=row["id"],
        timestamp=row["timestamp"],
        project=row["project"],
        caller=row["caller"],
        task=row["task"],
        trace_id=row["trace_id"],
        logical_call_id=row["logical_call_id"],
        call_fingerprint=f"sha256:{row['call_fingerprint']}",
        response_digest=_sha(row["response"].encode()),
        runtime_revision=LLM_CLIENT_PIN,
        model_ref=row["model"],
        finish_reason=row["finish_reason"],
        execution_path=row["execution_path"],
        retry_count=row["retry_count"],
        schema_hash=row["schema_hash"],
        response_format_type=row["response_format_type"],
        error=row["error"],
        call_snapshot_raw=row["call_snapshot"],
        response_raw=row["response"],
    )
    trace_bytes = canonical_json_bytes(snapshot.model_dump(mode="json"))
    trace_path = evidence_root / "process_tracing/positive/trace_snapshot.json"
    trace_artifact = artifact(trace_path, trace_bytes)
    pt_trace = TraceBinding(
        trace_id=snapshot.trace_id,
        logical_call_id=snapshot.logical_call_id,
        call_fingerprint=snapshot.call_fingerprint,
        response_digest=snapshot.response_digest,
        trace_store_snapshot_binding=trace_artifact,
        runtime_revision=snapshot.runtime_revision,
        model_ref=snapshot.model_ref,
    )

    def pt_positive_policy(request: GuardedDecisionRequest) -> NativeDecision:
        require_adequate_partition(
            HypothesisSpace.model_validate_json(
                (repository_root / request.target.ref).read_bytes()
            ),
            PartitionAudit.model_validate_json(
                (repository_root / request.decision_record.ref).read_bytes()
            ),
        )
        return NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED,
            native_disposition_ref="pt:pass3-eligible",
        )

    digests = {
        "process_tracing/positive": persist_case(
            consumer="process_tracing",
            case="positive",
            target_bytes=space_bytes,
            decision_bytes=positive_audit_bytes,
            output_bytes=positive_audit_bytes,
            policy_binding=pt_policy,
            policy_contents=pt_policy_contents,
            execution_kind=NativeExecutionKind.LLM,
            native_disposition_ref="pt:pass3-eligible",
            native_policy=pt_positive_policy,
            trace_binding=pt_trace,
            trace_bytes=trace_bytes,
        )
    }

    qc_candidates = sorted(
        json.loads((args.qc_root / "docs/fixtures/f1/candidate_run_v1.json").read_text())[
            "candidates"
        ],
        key=lambda item: item["candidate_id"],
    )
    source_keys = tuple(
        f"{item['resource_id']}:{item['function_id']}:{item['candidate_id']}"
        for item in qc_candidates[:3]
    )
    rivals = tuple(
        "qc-f1-" + hashlib.sha256(f"qc-f1:{key}".encode()).hexdigest()[:20] for key in source_keys
    )
    predictions = {
        rival: "qc-pred-" + hashlib.sha256(f"qc-f1-pred:{key}".encode()).hexdigest()[:20]
        for rival, key in zip(rivals, source_keys, strict=True)
    }
    foreign_audit = PartitionAudit(
        research_question_adequate=True,
        rival_pairs=[
            pair(a, b, predictions[a], predictions[b]) for a, b in combinations(rivals, 2)
        ],
        hypotheses_flagged=[],
        overall_quality="adequate",
        summary="Schema-valid foreign audit self-reports adequate.",
    )
    try:
        require_adequate_partition(space, foreign_audit)
    except PartitionBlockedError:
        pass
    pt_reason_codes = (
        "pt.invalid_prediction_ownership",
        "pt.missing_rival_pairs",
        "pt.no_valid_prediction_contrast",
        "pt.unknown_hypothesis_ids",
    )
    refusal_output = canonical_json_bytes(
        {
            "native_disposition_ref": "pt:pass3-blocked",
            "outcome": "refused",
            "semantic_reason_codes": pt_reason_codes,
        }
    )
    foreign_audit_bytes = canonical_json_bytes(foreign_audit.model_dump(mode="json"))

    def pt_refusal_policy(request: GuardedDecisionRequest) -> NativeDecision:
        bound_space = HypothesisSpace.model_validate_json(
            (repository_root / request.target.ref).read_bytes()
        )
        audit = PartitionAudit.model_validate_json(
            (repository_root / request.decision_record.ref).read_bytes()
        )
        try:
            require_adequate_partition(bound_space, audit)
        except PartitionBlockedError:
            return NativeDecision(
                outcome=GuardedDecisionOutcome.REFUSED,
                native_disposition_ref="pt:pass3-blocked",
                semantic_reason_codes=pt_reason_codes,
            )
        raise AssertionError("foreign PT audit unexpectedly passed")

    digests["process_tracing/refusal"] = persist_case(
        consumer="process_tracing",
        case="refusal",
        target_bytes=space_bytes,
        decision_bytes=foreign_audit_bytes,
        output_bytes=refusal_output,
        policy_binding=pt_policy,
        policy_contents=pt_policy_contents,
        execution_kind=NativeExecutionKind.DETERMINISTIC,
        native_disposition_ref="pt:pass3-blocked",
        native_policy=pt_refusal_policy,
    )

    candidate_path = args.qc_root / "docs/fixtures/f1/candidate_run_v1.json"
    review_path = args.qc_root / "docs/fixtures/f1/review_decisions_v1.json"
    review = load_coding_review(review_path)
    reviewed_bundle = finalize_f1_bundle(
        candidate_path=candidate_path,
        review=review,
        bundle_id="qc-f1-framing-observations-v1",
    )
    if reviewed_bundle.scientific_review_status != "not_performed":
        raise RuntimeError("QC coding output acquired unsupported scientific review status")
    if reviewed_bundle.raw_source_content_included is not False:
        raise RuntimeError("QC coding output unexpectedly includes raw source content")
    reviewed_bytes = (reviewed_bundle.model_dump_json(indent=2) + "\n").encode()
    if hashlib.sha256(reviewed_bytes).hexdigest() != EXPECTED_QC_BUNDLE_DIGEST:
        raise RuntimeError("QC positive bundle bytes drifted")

    def qc_positive_policy(request: GuardedDecisionRequest) -> NativeDecision:
        bundle = finalize_f1_bundle(
            candidate_path=repository_root / request.target.ref,
            review=F1CodingReviewPackage.model_validate_json(
                (repository_root / request.decision_record.ref).read_bytes()
            ),
            bundle_id="qc-f1-framing-observations-v1",
        )
        if (bundle.model_dump_json(indent=2) + "\n").encode() != reviewed_bytes:
            raise AssertionError("QC native positive output changed")
        return NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED,
            native_disposition_ref="qc:bundle-finalized",
        )

    digests["qualitative_coding/positive"] = persist_case(
        consumer="qualitative_coding",
        case="positive",
        target_bytes=candidate_path.read_bytes(),
        decision_bytes=review_path.read_bytes(),
        output_bytes=reviewed_bytes,
        policy_binding=qc_policy,
        policy_contents=qc_policy_contents,
        execution_kind=NativeExecutionKind.DETERMINISTIC,
        native_disposition_ref="qc:bundle-finalized",
        native_policy=qc_positive_policy,
    )

    foreign_ids = tuple(
        hashlib.sha256(
            f"pt-audit:51635c7939ccc7d11c9af09a2186cbfb925b91ae785132d94f1bf6e547c58c22:{index}".encode()
        ).hexdigest()
        for index in range(16)
    )
    foreign_payload = review.model_dump(mode="json")
    foreign_payload["review_id"] = "plan242-pt-derived-near-homonym-v1"
    foreign_payload["decisions"] = [
        CellReviewDecision(
            candidate_id=identifier,
            decision="accepted",
            rationale="Registered semantic control.",
        ).model_dump(mode="json")
        for identifier in foreign_ids
    ]
    foreign_review = F1CodingReviewPackage.model_validate(foreign_payload)
    foreign_review_bytes = canonical_json_bytes(foreign_review.model_dump(mode="json"))
    qc_refusal_output = canonical_json_bytes(
        {
            "native_disposition_ref": "qc:decision-universe-mismatch",
            "outcome": "refused",
            "semantic_reason_codes": ["qc.decision_universe_mismatch"],
        }
    )

    def qc_refusal_policy(request: GuardedDecisionRequest) -> NativeDecision:
        try:
            finalize_f1_bundle(
                candidate_path=repository_root / request.target.ref,
                review=F1CodingReviewPackage.model_validate_json(
                    (repository_root / request.decision_record.ref).read_bytes()
                ),
                bundle_id="qc-f1-framing-observations-v1",
            )
        except DecisionUniverseMismatchError:
            return NativeDecision(
                outcome=GuardedDecisionOutcome.REFUSED,
                native_disposition_ref="qc:decision-universe-mismatch",
                semantic_reason_codes=("qc.decision_universe_mismatch",),
            )
        raise AssertionError("foreign QC review unexpectedly finalized")

    digests["qualitative_coding/refusal"] = persist_case(
        consumer="qualitative_coding",
        case="refusal",
        target_bytes=candidate_path.read_bytes(),
        decision_bytes=foreign_review_bytes,
        output_bytes=qc_refusal_output,
        policy_binding=qc_policy,
        policy_contents=qc_policy_contents,
        execution_kind=NativeExecutionKind.DETERMINISTIC,
        native_disposition_ref="qc:decision-universe-mismatch",
        native_policy=qc_refusal_policy,
    )

    for case, digest in sorted(digests.items()):
        print(f"generated {case} {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
