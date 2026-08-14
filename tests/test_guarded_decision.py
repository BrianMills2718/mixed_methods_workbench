from __future__ import annotations

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
    GuardedDecisionOutcome,
    GuardedDecisionRequest,
    GuardedDecisionResult,
    NativeDecision,
    PolicyBinding,
    PolicyManifest,
    canonical_json_bytes,
    execute_guarded_decision,
    mapping_resolver,
    sha256_bytes,
)

DATA_CONTRACTS_PIN = "d845be0c5813ab26e9bf2f1eaf4473a262ac541b"


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
        prior_state=ArtifactBinding(
            ref="state:1", content_digest=prior_state_digest
        ),
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
        required_evidence_refs=("evidence:1",),
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
        composition_contract_revision=DATA_CONTRACTS_PIN,
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
        composition_contract_revision=DATA_CONTRACTS_PIN,
    )

    assert calls == 1
    assert expected in result.semantic_reason_codes
    assert result.receipt.traversed_boundaries == ("neutral_binding", "native_policy")
    assert result.proposed_transition is None


@pytest.mark.parametrize("corrupt", ["target", "policy", "policy_source", "transition"])
def test_corrupt_binding_refuses_before_native_dispatch(
    contents: dict[str, bytes], corrupt: str
) -> None:
    request = _request(contents)
    if corrupt == "target":
        request = request.model_copy(
            update={"target": request.target.model_copy(update={"content_digest": "sha256:" + "0" * 64})}
        )
    elif corrupt == "policy":
        request = request.model_copy(
            update={"policy": request.policy.model_copy(update={"policy_content_digest": "sha256:" + "0" * 64})}
        )
    elif corrupt == "policy_source":
        contents["policy-source:1"] = b"corrupt native rules"
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
        composition_contract_revision=DATA_CONTRACTS_PIN,
    )

    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert result.receipt.traversed_boundaries == ("neutral_binding",)
    assert any("mismatch" in code for code in result.semantic_reason_codes)


def test_request_has_no_nominal_method_dispatch_field(contents: dict[str, bytes]) -> None:
    fields = set(GuardedDecisionRequest.model_fields)
    assert fields.isdisjoint({"method_id", "repository", "action_label", "record_type"})


def test_semantically_equivalent_noncanonical_policy_bytes_fail_closed(
    contents: dict[str, bytes],
) -> None:
    request = _request(contents)
    pretty = b'{\n  "source_bindings": [{"ref": "policy-source:1", "content_digest": "' + sha256_bytes(
        contents["policy-source:1"]
    ).encode() + b'"}],\n  "repository_revision": "' + b"1" * 40 + b'",\n  "policy_name": "fixture.native-rules",\n  "canonicalization_profile": "plan242-json-v1"\n}'
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
        composition_contract_revision=DATA_CONTRACTS_PIN,
    )

    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert result.semantic_reason_codes == (
        "guarded-decision.policy-manifest-noncanonical/1",
    )


def test_result_rejects_a_tampered_receipt_reference(contents: dict[str, bytes]) -> None:
    result = execute_guarded_decision(
        _request(contents),
        resolve_content=mapping_resolver(contents),
        native_policy=lambda _: NativeDecision(outcome=GuardedDecisionOutcome.VALIDATED),
        composition_contract_revision=DATA_CONTRACTS_PIN,
    )
    payload = result.model_dump(mode="json")
    payload["receipt_ref"] = "sha256:" + "0" * 64

    with pytest.raises(ValidationError, match="receipt_ref must bind the exact receipt"):
        GuardedDecisionResult.model_validate(payload)
