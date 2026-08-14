from __future__ import annotations

from pathlib import Path

import pytest
from data_contracts.composition import (
    ActionKind,
    ControlTransitionContract,
    ControlTransitionMode,
    DecisionSource,
    EffectKind,
    OutcomeKind,
    ProposedTransition,
)
from pydantic import ValidationError

from mixed_methods_workbench.guarded_decision import (
    ArtifactBinding,
    EvidenceBinding,
    GuardedDecisionEvidenceBundle,
    GuardedDecisionOutcome,
    GuardedDecisionRequest,
    GuardedDecisionRequestV2,
    GuardedDecisionResult,
    NativeDecision,
    NativeExecutionEvidenceManifest,
    NativeExecutionKind,
    PolicyBinding,
    PolicyManifest,
    TraceBinding,
    TraceStoreSnapshot,
    canonical_digest,
    canonical_json_bytes,
    execute_guarded_decision,
    load_evidence_bundle,
    mapping_resolver,
    replay_evidence_bundle,
    sha256_bytes,
    verify_evidence_bundle,
    write_evidence_bundle,
)


def _transition(state: str) -> ProposedTransition:
    return ProposedTransition(
        transition_id="transition-1",
        invocation_id="invocation-1",
        manifest_digest="sha256:" + "2" * 64,
        pack_id="workbench.guarded-decision/1",
        pack_version="1.0.0",
        action_id="workbench.guarded-decision/1",
        descriptor_version="1.0.0",
        decision_source=DecisionSource.HARNESS,
        action_kind=ActionKind.CONTROL,
        control_transition=ControlTransitionContract(mode=ControlTransitionMode.STATE_PRESERVING),
        effect_kind=EffectKind.PURE,
        outcome=OutcomeKind.EXECUTION_SUCCEEDED,
        prior_state_fingerprint=state,
        resulting_state_fingerprint=state,
    )


@pytest.fixture
def contents() -> dict[str, bytes]:
    values = {
        "target:1": b"target bytes",
        "state:1": b"prior state bytes",
        "policy-source:1": b"native rules",
        "decision:1": b"native decision record",
        "evidence:1": b"required evidence",
    }
    manifest = PolicyManifest(
        canonicalization_profile="plan242-json-v1",
        policy_name="fixture.native-rules",
        repository_revision="1" * 40,
        source_bindings=(
            ArtifactBinding(
                ref="policy-source:1",
                content_digest=sha256_bytes(values["policy-source:1"]),
            ),
        ),
    )
    values["policy:1"] = canonical_json_bytes(manifest.model_dump(mode="json"))
    return values


def _request(contents: dict[str, bytes]) -> GuardedDecisionRequest:
    prior_state_digest = sha256_bytes(contents["state:1"])
    return GuardedDecisionRequest(
        request_id="request-1",
        target=ArtifactBinding(ref="target:1", content_digest=sha256_bytes(contents["target:1"])),
        prior_state=ArtifactBinding(ref="state:1", content_digest=prior_state_digest),
        policy=PolicyBinding(
            policy_id="policy:1",
            policy_version="native-revision-1",
            policy_content_digest=sha256_bytes(contents["policy:1"]),
        ),
        decision_record=ArtifactBinding(
            ref="decision:1", content_digest=sha256_bytes(contents["decision:1"])
        ),
        decision_actor_or_system_ref="actor:reviewer-1",
        proposed_transition=_transition(prior_state_digest),
        required_evidence_bindings=(
            EvidenceBinding(
                role="supporting_evidence",
                artifact=ArtifactBinding(
                    ref="evidence:1",
                    content_digest=sha256_bytes(contents["evidence:1"]),
                ),
            ),
        ),
    )


@pytest.mark.parametrize("native_ref", ["pt:resolution-1", "qc:reviewed-bundle-1"])
def test_both_native_signs_share_the_neutral_path(
    contents: dict[str, bytes], native_ref: str
) -> None:
    request = _request(contents)

    def native_policy(_: GuardedDecisionRequest) -> NativeDecision:
        return NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED,
            native_disposition_ref=native_ref,
        )

    result = execute_guarded_decision(
        request,
        resolve_content=mapping_resolver(contents),
        native_policy=native_policy,
    )

    assert result.outcome is GuardedDecisionOutcome.VALIDATED
    assert result.proposed_transition == request.proposed_transition
    assert result.native_disposition_ref == native_ref
    assert result.receipt.traversed_boundaries == ("neutral_binding", "native_policy")
    assert result.receipt.execution_result.outcome is OutcomeKind.EXECUTION_SUCCEEDED


@pytest.mark.parametrize(
    ("reason_codes", "expected"),
    [
        (
            (
                "pt.invalid_prediction_ownership",
                "pt.missing_rival_pairs",
                "pt.unknown_hypothesis_ids",
            ),
            "pt.unknown_hypothesis_ids",
        ),
        (("qc.decision_universe_mismatch",), "qc.decision_universe_mismatch"),
    ],
)
def test_semantic_near_homonyms_reach_the_injected_native_validator(
    contents: dict[str, bytes], reason_codes: tuple[str, ...], expected: str
) -> None:
    calls = 0

    def native_policy(_: GuardedDecisionRequest) -> NativeDecision:
        nonlocal calls
        calls += 1
        return NativeDecision(
            outcome=GuardedDecisionOutcome.REFUSED,
            semantic_reason_codes=reason_codes,
        )

    result = execute_guarded_decision(
        _request(contents),
        resolve_content=mapping_resolver(contents),
        native_policy=native_policy,
    )

    assert calls == 1
    assert expected in result.semantic_reason_codes
    assert result.receipt.traversed_boundaries == ("neutral_binding", "native_policy")
    assert result.proposed_transition is None


@pytest.mark.parametrize("corrupt", ["target", "policy", "policy_source", "evidence", "transition"])
def test_corrupt_binding_refuses_before_native_dispatch(
    contents: dict[str, bytes], corrupt: str
) -> None:
    request = _request(contents)
    if corrupt == "target":
        request = request.model_copy(
            update={
                "target": request.target.model_copy(update={"content_digest": "sha256:" + "0" * 64})
            }
        )
    elif corrupt == "policy":
        request = request.model_copy(
            update={
                "policy": request.policy.model_copy(
                    update={"policy_content_digest": "sha256:" + "0" * 64}
                )
            }
        )
    elif corrupt == "policy_source":
        contents["policy-source:1"] = b"corrupt native rules"
    elif corrupt == "evidence":
        contents["evidence:1"] = b"corrupt required evidence"
    else:
        request = request.model_copy(
            update={
                "proposed_transition": request.proposed_transition.model_copy(
                    update={"prior_state_fingerprint": "sha256:" + "0" * 64}
                )
            }
        )

    def forbidden(_: GuardedDecisionRequest) -> NativeDecision:
        raise AssertionError("native policy must not run after corrupt binding")

    result = execute_guarded_decision(
        request,
        resolve_content=mapping_resolver(contents),
        native_policy=forbidden,
    )

    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert result.receipt.traversed_boundaries == ("neutral_binding",)
    assert any("mismatch" in code for code in result.semantic_reason_codes)


def test_receipt_copies_exact_evidence_bindings(contents: dict[str, bytes]) -> None:
    request = _request(contents)
    result = execute_guarded_decision(
        request,
        resolve_content=mapping_resolver(contents),
        native_policy=lambda _: NativeDecision(outcome=GuardedDecisionOutcome.VALIDATED),
    )

    assert result.receipt.evidence_bindings == request.required_evidence_bindings


def _llm_manifest_request(
    contents: dict[str, bytes],
) -> tuple[GuardedDecisionRequest, NativeExecutionEvidenceManifest]:
    request = _request(contents)
    contents["native-output:1"] = b'{"outcome":"adequate"}'
    response_raw = '{"research_question_adequate":true}'
    response_digest = sha256_bytes(response_raw.encode())
    call_snapshot_raw = '{"snapshot_version":3}'
    call_fingerprint = sha256_bytes(canonical_json_bytes({"snapshot_version": 3}))
    snapshot = TraceStoreSnapshot(
        schema_version="plan242-trace-store-snapshot/1",
        source_store_digest="sha256:" + "7" * 64,
        source_row_id=4,
        timestamp="2026-08-14T00:00:00+00:00",
        project="fixture-project",
        caller="fixture-caller",
        task="fixture-task",
        trace_id="trace:fixture-1",
        logical_call_id="4",
        call_fingerprint=call_fingerprint,
        response_digest=response_digest,
        runtime_revision="6" * 40,
        model_ref="fixture:model",
        finish_reason="stop",
        execution_path="fixture",
        retry_count=0,
        schema_hash="fixture-schema",
        response_format_type="structured",
        call_snapshot_raw=call_snapshot_raw,
        response_raw=response_raw,
    )
    contents["trace-snapshot:1"] = canonical_json_bytes(snapshot.model_dump(mode="json"))
    manifest = NativeExecutionEvidenceManifest(
        schema_version="plan242-native-execution-evidence/1",
        consumer_id="fixture-consumer",
        consumer_revision="3" * 40,
        execution_kind=NativeExecutionKind.LLM,
        target_binding=request.target,
        decision_record_binding=request.decision_record,
        native_output_binding=ArtifactBinding(
            ref="native-output:1",
            content_digest=sha256_bytes(contents["native-output:1"]),
        ),
        native_disposition_ref="fixture:adequate",
        trace_binding=TraceBinding(
            trace_id="trace:fixture-1",
            logical_call_id="4",
            call_fingerprint=call_fingerprint,
            response_digest=response_digest,
            trace_store_snapshot_binding=ArtifactBinding(
                ref="trace-snapshot:1",
                content_digest=sha256_bytes(contents["trace-snapshot:1"]),
            ),
            runtime_revision="6" * 40,
            model_ref="fixture:model",
        ),
    )
    contents["execution-manifest:1"] = canonical_json_bytes(manifest.model_dump(mode="json"))
    evidence = (
        EvidenceBinding(
            role="native_execution_manifest",
            artifact=ArtifactBinding(
                ref="execution-manifest:1",
                content_digest=sha256_bytes(contents["execution-manifest:1"]),
            ),
        ),
        *request.required_evidence_bindings,
    )
    return request.model_copy(update={"required_evidence_bindings": evidence}), manifest


def test_trace_substitution_refuses_before_native_dispatch(
    contents: dict[str, bytes],
) -> None:
    request, _ = _llm_manifest_request(contents)
    original = TraceStoreSnapshot.model_validate_json(contents["trace-snapshot:1"])
    substituted = original.model_copy(update={"trace_id": "trace:different-valid-record"})
    contents["trace-snapshot:1"] = canonical_json_bytes(substituted.model_dump(mode="json"))

    result = execute_guarded_decision(
        request,
        resolve_content=mapping_resolver(contents),
        native_policy=lambda _: (_ for _ in ()).throw(
            AssertionError("native policy must not run after trace substitution")
        ),
    )

    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert result.semantic_reason_codes == (
        "guarded-decision.trace-store-snapshot-digest-mismatch/1",
    )
    assert result.receipt.traversed_boundaries == ("neutral_binding",)


def test_internally_inconsistent_trace_manifest_refuses_before_dispatch(
    contents: dict[str, bytes],
) -> None:
    request, manifest = _llm_manifest_request(contents)
    assert manifest.trace_binding is not None
    mismatched = manifest.model_copy(
        update={
            "trace_binding": manifest.trace_binding.model_copy(
                update={"trace_id": "trace:different-valid-record"}
            )
        }
    )
    contents["execution-manifest:1"] = canonical_json_bytes(mismatched.model_dump(mode="json"))
    manifest_evidence = request.required_evidence_bindings[0].model_copy(
        update={
            "artifact": request.required_evidence_bindings[0].artifact.model_copy(
                update={"content_digest": sha256_bytes(contents["execution-manifest:1"])}
            )
        }
    )
    request = request.model_copy(
        update={
            "required_evidence_bindings": (
                manifest_evidence,
                *request.required_evidence_bindings[1:],
            )
        }
    )

    result = execute_guarded_decision(
        request,
        resolve_content=mapping_resolver(contents),
        native_policy=lambda _: (_ for _ in ()).throw(
            AssertionError("native policy must not run after trace metadata mismatch")
        ),
    )

    assert result.semantic_reason_codes == ("guarded-decision.trace-id-mismatch/1",)


def test_bundle_replay_verifies_transitive_content(contents: dict[str, bytes]) -> None:
    request, manifest = _llm_manifest_request(contents)
    result = execute_guarded_decision(
        request,
        resolve_content=mapping_resolver(contents),
        native_policy=lambda _: NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED,
            native_disposition_ref=manifest.native_disposition_ref,
        ),
    )
    bundle = GuardedDecisionEvidenceBundle(
        bundle_version="plan242-guarded-decision-bundle/1",
        request=request,
        result_and_receipt=result,
        native_execution_manifest_binding=request.required_evidence_bindings[0].artifact,
        resolved_evidence_bindings=request.required_evidence_bindings,
        native_disposition_ref=result.native_disposition_ref,
    )

    verify_evidence_bundle(
        bundle,
        resolve_content=mapping_resolver(contents),
        expected_bundle_digest=canonical_digest(bundle),
    )

    contents["native-output:1"] = b'{"outcome":"substituted"}'
    with pytest.raises(ValueError, match="native-output-digest-mismatch"):
        verify_evidence_bundle(bundle, resolve_content=mapping_resolver(contents))


def test_bundle_writer_is_canonical_and_immutable(
    contents: dict[str, bytes], tmp_path: Path
) -> None:
    request, manifest = _llm_manifest_request(contents)
    result = execute_guarded_decision(
        request,
        resolve_content=mapping_resolver(contents),
        native_policy=lambda _: NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED,
            native_disposition_ref=manifest.native_disposition_ref,
        ),
    )
    bundle = GuardedDecisionEvidenceBundle(
        bundle_version="plan242-guarded-decision-bundle/1",
        request=request,
        result_and_receipt=result,
        native_execution_manifest_binding=request.required_evidence_bindings[0].artifact,
        resolved_evidence_bindings=request.required_evidence_bindings,
        native_disposition_ref=result.native_disposition_ref,
    )
    path = tmp_path / "bundle.json"

    digest = write_evidence_bundle(path, bundle)

    assert digest == canonical_digest(bundle)
    assert load_evidence_bundle(path) == bundle
    assert write_evidence_bundle(path, bundle) == digest
    with pytest.raises(FileExistsError, match="refusing to replace"):
        write_evidence_bundle(
            path,
            bundle.model_copy(update={"bundle_version": "invalid-successor"}),
        )


def test_execution_manifest_binds_native_disposition(
    contents: dict[str, bytes],
) -> None:
    request, _ = _llm_manifest_request(contents)

    result = execute_guarded_decision(
        request,
        resolve_content=mapping_resolver(contents),
        native_policy=lambda _: NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED,
            native_disposition_ref="fixture:different-disposition",
        ),
    )

    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert result.semantic_reason_codes == (
        "guarded-decision.execution-manifest-disposition-mismatch/1",
    )


def test_cold_replay_rejects_methodologically_wrong_persisted_disposition(
    contents: dict[str, bytes],
) -> None:
    request, manifest = _llm_manifest_request(contents)
    persisted = execute_guarded_decision(
        request,
        resolve_content=mapping_resolver(contents),
        native_policy=lambda _: NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED,
            native_disposition_ref=manifest.native_disposition_ref,
        ),
    )
    bundle = GuardedDecisionEvidenceBundle(
        bundle_version="plan242-guarded-decision-bundle/1",
        request=request,
        result_and_receipt=persisted,
        native_execution_manifest_binding=request.required_evidence_bindings[0].artifact,
        resolved_evidence_bindings=request.required_evidence_bindings,
        native_disposition_ref=persisted.native_disposition_ref,
    )

    with pytest.raises(ValueError, match="cold replay result differs"):
        replay_evidence_bundle(
            bundle,
            resolve_content=mapping_resolver(contents),
            native_policy=lambda _: NativeDecision(
                outcome=GuardedDecisionOutcome.REFUSED,
                native_disposition_ref=manifest.native_disposition_ref,
                semantic_reason_codes=("fixture.native-refusal",),
            ),
        )


def test_request_has_no_nominal_method_dispatch_field(contents: dict[str, bytes]) -> None:
    fields = set(GuardedDecisionRequest.model_fields)
    assert fields.isdisjoint({"method_id", "repository", "action_label", "record_type"})


def test_v2_request_is_historical_and_cannot_execute(contents: dict[str, bytes]) -> None:
    request = _request(contents)
    historical = GuardedDecisionRequestV2(
        request_id=request.request_id,
        target=request.target,
        prior_state=request.prior_state,
        policy=request.policy,
        decision_record=request.decision_record,
        decision_actor_or_system_ref=request.decision_actor_or_system_ref,
        proposed_transition=request.proposed_transition,
        required_evidence_refs=("evidence:1",),
    )

    with pytest.raises(ValidationError, match="required_evidence_refs"):
        GuardedDecisionRequest.model_validate(historical.model_dump(mode="json"))


def test_semantically_equivalent_noncanonical_policy_bytes_fail_closed(
    contents: dict[str, bytes],
) -> None:
    request = _request(contents)
    pretty = (
        b'{\n  "source_bindings": [{"ref": "policy-source:1", "content_digest": "'
        + sha256_bytes(contents["policy-source:1"]).encode()
        + b'"}],\n  "repository_revision": "'
        + b"1" * 40
        + b'",\n  "policy_name": "fixture.native-rules",\n  "canonicalization_profile": "plan242-json-v1"\n}'
    )
    contents["policy:pretty"] = pretty
    request = request.model_copy(
        update={
            "policy": request.policy.model_copy(
                update={
                    "policy_id": "policy:pretty",
                    "policy_content_digest": sha256_bytes(pretty),
                }
            )
        }
    )

    result = execute_guarded_decision(
        request,
        resolve_content=mapping_resolver(contents),
        native_policy=lambda _: (_ for _ in ()).throw(
            AssertionError("noncanonical manifest must not dispatch")
        ),
    )

    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert result.semantic_reason_codes == ("guarded-decision.policy-manifest-noncanonical/1",)


def test_result_rejects_a_tampered_receipt_reference(contents: dict[str, bytes]) -> None:
    result = execute_guarded_decision(
        _request(contents),
        resolve_content=mapping_resolver(contents),
        native_policy=lambda _: NativeDecision(outcome=GuardedDecisionOutcome.VALIDATED),
    )
    payload = result.model_dump(mode="json")
    payload["receipt_ref"] = "sha256:" + "0" * 64

    with pytest.raises(ValidationError, match="receipt_ref must bind the exact receipt"):
        GuardedDecisionResult.model_validate(payload)
