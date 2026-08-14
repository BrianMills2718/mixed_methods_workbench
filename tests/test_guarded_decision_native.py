"""Pinned native-consumer evidence for the bounded Plan 242 experiment.

Run only with exact checkouts supplied through PLAN242_PT_ROOT and
PLAN242_QC_ROOT.  This is intentionally an integration test, not a substitute
for ordinary portable Workbench unit tests.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
from itertools import combinations
from pathlib import Path

import pytest

PT_ROOT = os.environ.get("PLAN242_PT_ROOT")
QC_ROOT = os.environ.get("PLAN242_QC_ROOT")
if PT_ROOT is None or QC_ROOT is None:
    pytest.skip("requires exact PLAN242_PT_ROOT and PLAN242_QC_ROOT", allow_module_level=True)

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
    GuardedDecisionOutcome,
    GuardedDecisionRequest,
    NativeDecision,
    PolicyBinding,
    execute_guarded_decision,
    mapping_resolver,
    sha256_bytes,
)

PT_PIN = "ce87f630546a9193c999943aeb3319940e89cc95"
QC_PIN = "68ac10eb3d7588bed547b89d58f0186db3f9ac85"
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
    raise RuntimeError("Plan 242 native integration test requires the registered exact repository pins")


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
    rivals = tuple(f"qc-f1-{identifier[:20]}" for identifier in QC_FOREIGN_IDS[:3])
    predictions = {rival: f"qc-pred-{identifier[:20]}" for rival, identifier in zip(rivals, QC_FOREIGN_IDS)}
    return PartitionAudit(
        research_question_adequate=True,
        rival_pairs=[_pair(a, b, predictions[a], predictions[b]) for a, b in combinations(rivals, 2)],
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
    prefix: str, *, target: bytes, policy: bytes, decision: bytes
) -> tuple[GuardedDecisionRequest, dict[str, bytes]]:
    contents = {
        f"{prefix}:target": target,
        f"{prefix}:state": f"{prefix} state".encode(),
        f"{prefix}:policy": policy,
        f"{prefix}:decision": decision,
        f"{prefix}:evidence": f"{prefix} evidence".encode(),
    }
    prior_digest = sha256_bytes(contents[f"{prefix}:state"])
    request = GuardedDecisionRequest(
        request_id=f"plan242-{prefix}",
        target=ArtifactBinding(ref=f"{prefix}:target", content_digest=sha256_bytes(contents[f"{prefix}:target"])),
        prior_state=ArtifactBinding(ref=f"{prefix}:state", content_digest=prior_digest),
        policy=PolicyBinding(
            policy_id=f"{prefix}:policy",
            policy_version="plan242-pinned-native",
            policy_content_digest=sha256_bytes(contents[f"{prefix}:policy"]),
        ),
        decision_record=ArtifactBinding(ref=f"{prefix}:decision", content_digest=sha256_bytes(decision)),
        decision_actor_or_system_ref="plan242:integration-harness",
        proposed_transition=_transition(prior_digest),
        required_evidence_refs=(f"{prefix}:evidence",),
    )
    return request, contents


def test_pt_native_positive_and_qc_derived_near_homonym_reach_native_gate() -> None:
    space = _native_space()
    positive = _adequate_audit()
    request, contents = _request(
        "pt-positive",
        target=space.model_dump_json().encode(),
        policy=(Path(PT_ROOT) / "pt/pass_partition.py").read_bytes(),
        decision=positive.model_dump_json().encode(),
    )

    def accepts(_: GuardedDecisionRequest) -> NativeDecision:
        require_adequate_partition(
            HypothesisSpace.model_validate_json(contents["pt-positive:target"]),
            PartitionAudit.model_validate_json(contents["pt-positive:decision"]),
        )
        return NativeDecision(
            outcome=GuardedDecisionOutcome.VALIDATED,
            native_disposition_ref="pt:pass3-eligible",
        )

    result = execute_guarded_decision(request, resolve_content=mapping_resolver(contents), native_policy=accepts)
    assert result.outcome is GuardedDecisionOutcome.VALIDATED
    assert result.receipt.traversed_boundaries == ("neutral_binding", "native_policy")

    foreign = _foreign_pt_audit()
    request, contents = _request(
        "pt-foreign",
        target=space.model_dump_json().encode(),
        policy=(Path(PT_ROOT) / "pt/pass_partition.py").read_bytes(),
        decision=foreign.model_dump_json().encode(),
    )

    def rejects(_: GuardedDecisionRequest) -> NativeDecision:
        bound_audit = PartitionAudit.model_validate_json(contents["pt-foreign:decision"])
        with pytest.raises(PartitionBlockedError):
            require_adequate_partition(
                HypothesisSpace.model_validate_json(contents["pt-foreign:target"]), bound_audit
            )
        return NativeDecision(
            outcome=GuardedDecisionOutcome.REFUSED,
            semantic_reason_codes=_pt_codes(bound_audit.decision_blockers),
            native_disposition_ref="pt:pass3-blocked",
        )

    result = execute_guarded_decision(request, resolve_content=mapping_resolver(contents), native_policy=rejects)
    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert result.semantic_reason_codes == PT_CODES
    assert result.receipt.traversed_boundaries == ("neutral_binding", "native_policy")


def test_qc_native_positive_and_pt_derived_near_homonym_reach_native_gate() -> None:
    qc_root = Path(QC_ROOT)
    candidate = qc_root / "docs/fixtures/f1/candidate_run_v1.json"
    review_path = qc_root / "docs/fixtures/f1/review_decisions_v1.json"
    review = load_coding_review(review_path)
    request, contents = _request(
        "qc-positive",
        target=candidate.read_bytes(),
        policy=(qc_root / "qc_clean/core/f1_framing_review.py").read_bytes(),
        decision=review_path.read_bytes(),
    )

    def accepts(_: GuardedDecisionRequest) -> NativeDecision:
        assert candidate.read_bytes() == contents["qc-positive:target"]
        bound_review = F1CodingReviewPackage.model_validate_json(contents["qc-positive:decision"])
        bundle = finalize_f1_bundle(
            candidate_path=candidate, review=bound_review, bundle_id="qc-f1-framing-observations-v1"
        )
        assert len(bundle.observations) == 16
        return NativeDecision(outcome=GuardedDecisionOutcome.VALIDATED, native_disposition_ref="qc:bundle-finalized")

    result = execute_guarded_decision(request, resolve_content=mapping_resolver(contents), native_policy=accepts)
    assert result.outcome is GuardedDecisionOutcome.VALIDATED

    payload = review.model_dump(mode="json")
    payload["review_id"] = "plan242-pt-derived-near-homonym-v1"
    payload["decisions"] = [
        CellReviewDecision(candidate_id=identifier, decision="accepted", rationale="Registered semantic control.").model_dump(mode="json")
        for identifier in QC_FOREIGN_IDS
    ]
    foreign = F1CodingReviewPackage.model_validate(payload)
    request, contents = _request(
        "qc-foreign",
        target=candidate.read_bytes(),
        policy=(qc_root / "qc_clean/core/f1_framing_review.py").read_bytes(),
        decision=foreign.model_dump_json().encode(),
    )

    def rejects(_: GuardedDecisionRequest) -> NativeDecision:
        assert candidate.read_bytes() == contents["qc-foreign:target"]
        bound_review = F1CodingReviewPackage.model_validate_json(contents["qc-foreign:decision"])
        with pytest.raises(DecisionUniverseMismatchError):
            finalize_f1_bundle(
                candidate_path=candidate, review=bound_review, bundle_id="qc-f1-framing-observations-v1"
            )
        return NativeDecision(
            outcome=GuardedDecisionOutcome.REFUSED,
            semantic_reason_codes=("qc.decision_universe_mismatch",),
            native_disposition_ref="qc:decision-universe-mismatch",
        )

    result = execute_guarded_decision(request, resolve_content=mapping_resolver(contents), native_policy=rejects)
    assert result.outcome is GuardedDecisionOutcome.REFUSED
    assert result.semantic_reason_codes == ("qc.decision_universe_mismatch",)
    assert result.receipt.traversed_boundaries == ("neutral_binding", "native_policy")
