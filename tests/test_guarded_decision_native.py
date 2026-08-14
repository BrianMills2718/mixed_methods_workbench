"""Pinned native-consumer evidence for the bounded Plan 242 experiment.

Run only with exact checkouts supplied through PLAN242_PT_ROOT and
PLAN242_QC_ROOT.  This is intentionally an integration test, not a substitute
for ordinary portable Workbench unit tests.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from itertools import combinations
from pathlib import Path

import pytest

PT_ROOT = os.environ.get("PLAN242_PT_ROOT")
QC_ROOT = os.environ.get("PLAN242_QC_ROOT")
if PT_ROOT is None or QC_ROOT is None:
    pytest.skip(
        "requires exact PLAN242_PT_ROOT and PLAN242_QC_ROOT",
        allow_module_level=True,
    )

from pt.pass_partition import PartitionBlockedError, require_adequate_partition
from pt.schemas import (
    Hypothesis,
    HypothesisSpace,
    PartitionAudit,
    Prediction,
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
from test_guarded_decision import _transition

from mixed_methods_workbench.guarded_decision import (
    ArtifactBinding,
    EvidenceBinding,
    GuardedDecisionOutcome,
    GuardedDecisionRequest,
    NativeDecision,
    NativeExecutionEvidenceManifest,
    PolicyBinding,
    PolicyManifest,
    canonical_json_bytes,
    execute_guarded_decision,
    load_evidence_bundle,
    mapping_resolver,
    observed_composition_contract_revision,
    replay_evidence_bundle,
    sha256_bytes,
)

PT_PIN = "ce87f630546a9193c999943aeb3319940e89cc95"
QC_PIN = "68ac10eb3d7588bed547b89d58f0186db3f9ac85"
DATA_CONTRACTS_PIN = "d845be0c5813ab26e9bf2f1eaf4473a262ac541b"
POLICY_MANIFEST_DIGESTS = {
    "process_tracing_partition_gate_policy.json": "sha256:c7eb0aa7cdf0f38120f3c98d47665f35b5b869f3f29e1721ed77634db6353ae3",
    "qualitative_coding_f1_finalization_policy.json": "sha256:7101f302d0b2b5ce20a4992d9ea7d0bc164472616b60e44f3425e6706051bb52",
}
PT_CODES = (
    "pt.invalid_prediction_ownership",
    "pt.missing_rival_pairs",
    "pt.no_valid_prediction_contrast",
    "pt.unknown_hypothesis_ids",
)
QC_FOREIGN_IDS = tuple(
    hashlib.sha256(
        f"pt-audit:51635c7939ccc7d11c9af09a2186cbfb925b91ae785132d94f1bf6e547c58c22:{index}".encode()
    ).hexdigest()
    for index in range(16)
)


def _head(path: str) -> str:
    return subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"], text=True).strip()


if _head(PT_ROOT) != PT_PIN or _head(QC_ROOT) != QC_PIN:
    raise RuntimeError(
        "Plan 242 native integration test requires the registered exact repository pins"
    )
if observed_composition_contract_revision() != DATA_CONTRACTS_PIN:
    raise RuntimeError("Plan 242 test imported the wrong Data Contracts revision")


def _pair(h1: str, h2: str, p1: str, p2: str) -> RivalPairAudit:
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


def _native_space() -> HypothesisSpace:
    return HypothesisSpace(
        research_question="Why did the focal outcome occur?",
        hypotheses=[
            Hypothesis(
                id=f"h{index}",
                description=f"Alternative h{index}",
                source="generated",
                generation_rationale="Theory-derived rival.",
                theoretical_basis="Distinct causal theory.",
                causal_mechanism="Distinct observable process.",
                observable_predictions=[
                    Prediction(id=f"pred_h{index}_01", description=f"Trace unique to h{index}.")
                ],
            )
            for index in range(1, 4)
        ],
    )


def _adequate_audit() -> PartitionAudit:
    ids = ("h1", "h2", "h3")
    return PartitionAudit(
        research_question_adequate=True,
        rival_pairs=[_pair(a, b, f"pred_{a}_01", f"pred_{b}_01") for a, b in combinations(ids, 2)],
        hypotheses_flagged=[],
        overall_quality="adequate",
        summary="Every native rival pair has one owned opposed prediction contrast.",
    )


def _foreign_pt_audit() -> PartitionAudit:
    candidate_path = Path(QC_ROOT) / "docs/fixtures/f1/candidate_run_v1.json"
    candidates = sorted(
        json.loads(candidate_path.read_text())["candidates"], key=lambda row: row["candidate_id"]
    )
    source_keys = tuple(
        f"{row['resource_id']}:{row['function_id']}:{row['candidate_id']}" for row in candidates[:3]
    )
    rivals = tuple(
        "qc-f1-" + hashlib.sha256(f"qc-f1:{key}".encode()).hexdigest()[:20] for key in source_keys
    )
    predictions = {
        rival: "qc-pred-" + hashlib.sha256(f"qc-f1-pred:{key}".encode()).hexdigest()[:20]
        for rival, key in zip(rivals, source_keys)
    }
    return PartitionAudit(
        research_question_adequate=True,
        rival_pairs=[
            _pair(a, b, predictions[a], predictions[b]) for a, b in combinations(rivals, 2)
        ],
        hypotheses_flagged=[],
        overall_quality="adequate",
        summary="Schema-valid foreign audit self-reports adequate.",
    )


def _pt_codes(messages: list[str]) -> tuple[str, ...]:
    codes: set[str] = set()
    for message in messages:
        if message.startswith("rival pairs reference unknown hypothesis ids:"):
            codes.add("pt.unknown_hypothesis_ids")
        if ": invalid prediction contrast(s):" in message:
            codes.add("pt.invalid_prediction_ownership")
        if "no valid concrete prediction contrast" in message:
            codes.add("pt.no_valid_prediction_contrast")
        if message.startswith("missing rival pairs:"):
            codes.add("pt.missing_rival_pairs")
    return tuple(sorted(codes))


def _request(
    prefix: str,
    *,
    target: bytes,
    policy: bytes,
    decision: bytes,
    policy_sources: dict[str, bytes],
) -> tuple[GuardedDecisionRequest, dict[str, bytes]]:
    contents = {
        f"{prefix}:target": target,
        f"{prefix}:state": f"{prefix} state".encode(),
        f"{prefix}:policy": policy,
        f"{prefix}:decision": decision,
        f"{prefix}:evidence": f"{prefix} evidence".encode(),
    }
    contents.update(policy_sources)
    prior_digest = sha256_bytes(contents[f"{prefix}:state"])
    request = GuardedDecisionRequest(
        request_id=f"plan242-{prefix}",
        target=ArtifactBinding(
            ref=f"{prefix}:target", content_digest=sha256_bytes(contents[f"{prefix}:target"])
        ),
        prior_state=ArtifactBinding(ref=f"{prefix}:state", content_digest=prior_digest),
        policy=PolicyBinding(
            policy_id=f"{prefix}:policy",
            policy_version="plan242-pinned-native",
            policy_content_digest=sha256_bytes(contents[f"{prefix}:policy"]),
        ),
        decision_record=ArtifactBinding(
            ref=f"{prefix}:decision", content_digest=sha256_bytes(decision)
        ),
        decision_actor_or_system_ref="plan242:integration-harness",
        proposed_transition=_transition(prior_digest),
        required_evidence_bindings=(
            EvidenceBinding(
                role="supporting_evidence",
                artifact=ArtifactBinding(
                    ref=f"{prefix}:evidence",
                    content_digest=sha256_bytes(contents[f"{prefix}:evidence"]),
                ),
            ),
        ),
    )
    return request, contents


def _policy_manifest(name: str) -> tuple[bytes, PolicyManifest]:
    path = Path(__file__).parent / "fixtures/guarded_decision" / name
    manifest = PolicyManifest.model_validate_json(path.read_bytes())
    canonical = canonical_json_bytes(manifest.model_dump(mode="json"))
    assert sha256_bytes(canonical) == POLICY_MANIFEST_DIGESTS[name]
    return canonical, manifest


def _policy_sources(root: Path, manifest: PolicyManifest, prefix: str) -> dict[str, bytes]:
    return {
        binding.ref: (root / binding.ref.removeprefix(prefix)).read_bytes()
        for binding in manifest.source_bindings
    }


def test_pt_native_positive_and_qc_derived_near_homonym_reach_native_gate() -> None:
    space = _native_space()
    positive = _adequate_audit()
    policy, manifest = _policy_manifest("process_tracing_partition_gate_policy.json")
    request, contents = _request(
        "pt-positive",
        target=space.model_dump_json().encode(),
        policy=policy,
        decision=positive.model_dump_json().encode(),
        policy_sources=_policy_sources(Path(PT_ROOT), manifest, "pt:source:"),
    )
    resolver = mapping_resolver(contents)

    def accepts(bound_request: GuardedDecisionRequest) -> NativeDecision:
        require_adequate_partition(
            HypothesisSpace.model_validate_json(resolver(bound_request.target.ref)),
            PartitionAudit.model_validate_json(resolver(bound_request.decision_record.ref)),
        )
        return NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED,
            native_disposition_ref="pt:pass3-eligible",
        )

    result = execute_guarded_decision(
        request,
        resolve_content=resolver,
        native_policy=accepts,
    )
    assert result.outcome is GuardedDecisionOutcome.VALIDATED
    assert result.receipt.traversed_boundaries == ("neutral_binding", "native_policy")

    foreign = _foreign_pt_audit()
    request, contents = _request(
        "pt-foreign",
        target=space.model_dump_json().encode(),
        policy=policy,
        decision=foreign.model_dump_json().encode(),
        policy_sources=_policy_sources(Path(PT_ROOT), manifest, "pt:source:"),
    )
    resolver = mapping_resolver(contents)

    def rejects(bound_request: GuardedDecisionRequest) -> NativeDecision:
        bound_audit = PartitionAudit.model_validate_json(
            resolver(bound_request.decision_record.ref)
        )
        with pytest.raises(PartitionBlockedError):
            require_adequate_partition(
                HypothesisSpace.model_validate_json(resolver(bound_request.target.ref)),
                bound_audit,
            )
        return NativeDecision(
            outcome=GuardedDecisionOutcome.REFUSED,
            semantic_reason_codes=_pt_codes(bound_audit.decision_blockers),
            native_disposition_ref="pt:pass3-blocked",
        )

    result = execute_guarded_decision(
        request,
        resolve_content=resolver,
        native_policy=rejects,
    )
    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert result.semantic_reason_codes == PT_CODES
    assert result.receipt.traversed_boundaries == ("neutral_binding", "native_policy")


def test_qc_native_positive_and_pt_derived_near_homonym_reach_native_gate(
    tmp_path: Path,
) -> None:
    qc_root = Path(QC_ROOT)
    candidate = qc_root / "docs/fixtures/f1/candidate_run_v1.json"
    review_path = qc_root / "docs/fixtures/f1/review_decisions_v1.json"
    review = load_coding_review(review_path)
    policy, manifest = _policy_manifest("qualitative_coding_f1_finalization_policy.json")
    request, contents = _request(
        "qc-positive",
        target=candidate.read_bytes(),
        policy=policy,
        decision=review_path.read_bytes(),
        policy_sources=_policy_sources(qc_root, manifest, "qc:source:"),
    )
    resolver = mapping_resolver(contents)

    def accepts(bound_request: GuardedDecisionRequest) -> NativeDecision:
        bound_candidate = tmp_path / "positive-candidate.json"
        bound_candidate.write_bytes(resolver(bound_request.target.ref))
        bound_review = F1CodingReviewPackage.model_validate_json(
            resolver(bound_request.decision_record.ref)
        )
        bundle = finalize_f1_bundle(
            candidate_path=bound_candidate,
            review=bound_review,
            bundle_id="qc-f1-framing-observations-v1",
        )
        assert len(bundle.observations) == 16
        return NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED, native_disposition_ref="qc:bundle-finalized"
        )

    result = execute_guarded_decision(
        request,
        resolve_content=resolver,
        native_policy=accepts,
    )
    assert result.outcome is GuardedDecisionOutcome.VALIDATED

    payload = review.model_dump(mode="json")
    payload["review_id"] = "plan242-pt-derived-near-homonym-v1"
    payload["decisions"] = [
        CellReviewDecision(
            candidate_id=identifier, decision="accepted", rationale="Registered semantic control."
        ).model_dump(mode="json")
        for identifier in QC_FOREIGN_IDS
    ]
    foreign = F1CodingReviewPackage.model_validate(payload)
    request, contents = _request(
        "qc-foreign",
        target=candidate.read_bytes(),
        policy=policy,
        decision=foreign.model_dump_json().encode(),
        policy_sources=_policy_sources(qc_root, manifest, "qc:source:"),
    )
    resolver = mapping_resolver(contents)

    def rejects(bound_request: GuardedDecisionRequest) -> NativeDecision:
        bound_candidate = tmp_path / "foreign-candidate.json"
        bound_candidate.write_bytes(resolver(bound_request.target.ref))
        bound_review = F1CodingReviewPackage.model_validate_json(
            resolver(bound_request.decision_record.ref)
        )
        with pytest.raises(DecisionUniverseMismatchError):
            finalize_f1_bundle(
                candidate_path=bound_candidate,
                review=bound_review,
                bundle_id="qc-f1-framing-observations-v1",
            )
        return NativeDecision(
            outcome=GuardedDecisionOutcome.REFUSED,
            semantic_reason_codes=("qc.decision_universe_mismatch",),
            native_disposition_ref="qc:decision-universe-mismatch",
        )

    result = execute_guarded_decision(
        request,
        resolve_content=resolver,
        native_policy=rejects,
    )
    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert result.semantic_reason_codes == ("qc.decision_universe_mismatch",)
    assert result.receipt.traversed_boundaries == ("neutral_binding", "native_policy")


def test_native_callback_consumes_a_substituted_request_reference() -> None:
    policy, manifest = _policy_manifest("process_tracing_partition_gate_policy.json")
    request, contents = _request(
        "pt-reference",
        target=_native_space().model_dump_json().encode(),
        policy=policy,
        decision=_adequate_audit().model_dump_json().encode(),
        policy_sources=_policy_sources(Path(PT_ROOT), manifest, "pt:source:"),
    )
    foreign_space = HypothesisSpace(
        research_question="Why did the focal outcome occur?",
        hypotheses=list(_native_space().hypotheses[:2]),
    )
    contents["pt-reference:substituted-target"] = foreign_space.model_dump_json().encode()
    request = request.model_copy(
        update={
            "target": ArtifactBinding(
                ref="pt-reference:substituted-target",
                content_digest=sha256_bytes(contents["pt-reference:substituted-target"]),
            )
        }
    )
    resolver = mapping_resolver(contents)

    def native_policy(bound_request: GuardedDecisionRequest) -> NativeDecision:
        bound_space = HypothesisSpace.model_validate_json(resolver(bound_request.target.ref))
        bound_audit = PartitionAudit.model_validate_json(
            resolver(bound_request.decision_record.ref)
        )
        with pytest.raises(PartitionBlockedError):
            require_adequate_partition(bound_space, bound_audit)
        return NativeDecision(
            outcome=GuardedDecisionOutcome.REFUSED,
            semantic_reason_codes=_pt_codes(bound_audit.decision_blockers),
            native_disposition_ref="pt:request-reference-substitution-observed",
        )

    result = execute_guarded_decision(
        request,
        resolve_content=resolver,
        native_policy=native_policy,
    )

    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert "pt.unknown_hypothesis_ids" in result.semantic_reason_codes


@pytest.mark.parametrize(
    ("consumer", "case"),
    [
        ("process_tracing", "positive"),
        ("process_tracing", "refusal"),
        ("qualitative_coding", "positive"),
        ("qualitative_coding", "refusal"),
    ],
)
def test_committed_v3_bundle_cold_replays_native_disposition(
    consumer: str,
    case: str,
) -> None:
    repository_root = Path(__file__).parents[1]
    bundle_path = (
        repository_root / "docs/research/plan242/evidence" / consumer / case / "bundle.json"
    )
    bundle = load_evidence_bundle(bundle_path)

    def resolve(ref: str) -> bytes:
        path = (repository_root / ref).resolve()
        if not path.is_relative_to(repository_root):
            raise LookupError(f"evidence ref escapes repository: {ref}")
        try:
            return path.read_bytes()
        except FileNotFoundError as exc:
            raise LookupError(f"unresolved evidence ref: {ref}") from exc

    manifest = NativeExecutionEvidenceManifest.model_validate_json(
        resolve(bundle.native_execution_manifest_binding.ref)
    )

    def pt_policy(request: GuardedDecisionRequest) -> NativeDecision:
        space = HypothesisSpace.model_validate_json(resolve(request.target.ref))
        audit = PartitionAudit.model_validate_json(resolve(request.decision_record.ref))
        try:
            require_adequate_partition(space, audit)
        except PartitionBlockedError:
            reason_codes = _pt_codes(audit.decision_blockers)
            decision = NativeDecision(
                outcome=GuardedDecisionOutcome.REFUSED,
                semantic_reason_codes=reason_codes,
                native_disposition_ref="pt:pass3-blocked",
            )
            expected_output = canonical_json_bytes(
                {
                    "native_disposition_ref": "pt:pass3-blocked",
                    "outcome": "refused",
                    "semantic_reason_codes": reason_codes,
                }
            )
        else:
            decision = NativeDecision(
                outcome=GuardedDecisionOutcome.VALIDATED,
                native_disposition_ref="pt:pass3-eligible",
            )
            expected_output = canonical_json_bytes(audit.model_dump(mode="json"))
        assert expected_output == resolve(manifest.native_output_binding.ref)
        return decision

    def qc_policy(request: GuardedDecisionRequest) -> NativeDecision:
        review = F1CodingReviewPackage.model_validate_json(resolve(request.decision_record.ref))
        try:
            native_bundle = finalize_f1_bundle(
                candidate_path=repository_root / request.target.ref,
                review=review,
                bundle_id="qc-f1-framing-observations-v1",
            )
        except DecisionUniverseMismatchError:
            expected_output = canonical_json_bytes(
                {
                    "native_disposition_ref": "qc:decision-universe-mismatch",
                    "outcome": "refused",
                    "semantic_reason_codes": ["qc.decision_universe_mismatch"],
                }
            )
            assert expected_output == resolve(manifest.native_output_binding.ref)
            return NativeDecision(
                outcome=GuardedDecisionOutcome.REFUSED,
                semantic_reason_codes=("qc.decision_universe_mismatch",),
                native_disposition_ref="qc:decision-universe-mismatch",
            )
        expected_output = (native_bundle.model_dump_json(indent=2) + "\n").encode()
        assert native_bundle.scientific_review_status == "not_performed"
        assert native_bundle.raw_source_content_included is False
        assert hashlib.sha256(expected_output).hexdigest() == (
            "c135da965f0fa61da85aa49008c7fe93711368ac8422c5c83816c69a0346934f"
        )
        assert expected_output == resolve(manifest.native_output_binding.ref)
        return NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED,
            native_disposition_ref="qc:bundle-finalized",
        )

    replayed = replay_evidence_bundle(
        bundle,
        resolve_content=resolve,
        native_policy=pt_policy if consumer == "process_tracing" else qc_policy,
    )

    assert replayed == bundle.result_and_receipt
    if consumer == "process_tracing" and case == "refusal":
        assert replayed.semantic_reason_codes == PT_CODES
    if consumer == "qualitative_coding" and case == "refusal":
        assert replayed.semantic_reason_codes == ("qc.decision_universe_mismatch",)
