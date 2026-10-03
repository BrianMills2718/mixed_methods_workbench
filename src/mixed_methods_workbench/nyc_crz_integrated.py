"""Authentic NYC CRZ mixed-methods integration over method-owned artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .nyc_crz_evidence_slice import nyc_crz_evidence_slice_payload
from .nyc_crz_quantitative import nyc_crz_quantitative_audit_payload

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = PROJECT_ROOT / "examples" / "fixtures" / "nyc_crz_integrated"
BINDING_PATH = FIXTURE_ROOT / "qc_binding.json"


class NycCrzIntegrationError(ValueError):
    """Raised when an accepted producer artifact or integration boundary is invalid."""


class _Consumer(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)


class QcAnchor(_Consumer):
    anchor_id: str
    artifact_id: str
    pdf_page_index: int
    printed_line_start: int
    printed_line_end: int
    quote_text: str
    quote_hash: str


class QcHandoff(_Consumer):
    schema_version: Literal["qc.nyc_crz_describe_handoff.v1"]
    package_type: Literal["qualitative_coding.nyc_crz_describe"]
    project_id: str
    produced_by_commit: str
    findings: list[dict[str, Any]]
    anchors: dict[str, QcAnchor]
    non_claims: list[str]
    methodology: str


class AnalystItem(_Consumer):
    review_item_id: str
    item_type: Literal[
        "substantive_finding", "boundary_case", "unresolved_negative_case_search"
    ]
    source_candidate_ids: list[str]
    proposed_text: str
    supporting_anchor_ids: list[str]
    contrary_anchor_ids: list[str]
    human_decision: Literal["approved"]


class ApprovedAnalystReview(_Consumer):
    schema_version: Literal["qc.nyc_crz_analyst_review.v1"]
    status: Literal["human_review_approved"]
    source_handoff_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    method_boundary: list[str]
    items: list[AnalystItem]
    human_review: dict[str, Any]

    @model_validator(mode="after")
    def _accepted_shape(self) -> "ApprovedAnalystReview":
        kinds = [item.item_type for item in self.items]
        if len(self.items) != 14:
            raise ValueError("approved NYC review must contain exactly 14 bounded items")
        if kinds.count("substantive_finding") != 12:
            raise ValueError("approved NYC review must preserve 12 substantive findings")
        if kinds.count("boundary_case") != 1:
            raise ValueError("approved NYC review must preserve one boundary case")
        if kinds.count("unresolved_negative_case_search") != 1:
            raise ValueError("approved NYC review must preserve unresolved negative-case search")
        return self


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise NycCrzIntegrationError(f"cannot read pinned artifact: {path.name}") from exc


def load_accepted_qc(root: Path = FIXTURE_ROOT) -> tuple[QcHandoff, ApprovedAnalystReview, dict[str, Any]]:
    binding = _load_json(root / "qc_binding.json")
    if binding.get("review_state") != "human_review_approved":
        raise NycCrzIntegrationError("QC binding is not human approved")
    artifacts = {item["role"]: item for item in binding.get("artifacts", [])}
    expected_roles = {"method_owned_handoff", "human_approved_analyst_review"}
    if set(artifacts) != expected_roles:
        raise NycCrzIntegrationError("QC binding roles are incomplete")
    handoff_path = root / artifacts["method_owned_handoff"]["path"]
    review_path = root / artifacts["human_approved_analyst_review"]["path"]
    for role, path in (("method_owned_handoff", handoff_path), ("human_approved_analyst_review", review_path)):
        observed = _sha256(path)
        expected = artifacts[role]["sha256"]
        if observed != expected:
            raise NycCrzIntegrationError(
                f"QC artifact digest mismatch for {role}: expected {expected}, observed {observed}"
            )
    try:
        handoff = QcHandoff.model_validate(_load_json(handoff_path))
        review = ApprovedAnalystReview.model_validate(_load_json(review_path))
    except ValueError as exc:
        raise NycCrzIntegrationError(f"invalid accepted QC artifact: {exc}") from exc
    if review.source_handoff_sha256 != artifacts["method_owned_handoff"]["sha256"]:
        raise NycCrzIntegrationError("approved review does not bind the pinned method handoff")
    anchor_ids = set(handoff.anchors)
    for item in review.items:
        if set(item.supporting_anchor_ids + item.contrary_anchor_ids) - anchor_ids:
            raise NycCrzIntegrationError(
                f"approved review item has unresolved evidence anchors: {item.review_item_id}"
            )
    return handoff, review, binding


def nyc_crz_integrated_payload(root: Path = FIXTURE_ROOT) -> dict[str, object]:
    handoff, review, binding = load_accepted_qc(root)
    extraction = nyc_crz_evidence_slice_payload()
    quantitative = nyc_crz_quantitative_audit_payload()

    substantive = [x.model_dump(mode="json") for x in review.items if x.item_type == "substantive_finding"]
    boundary = next(x for x in review.items if x.item_type == "boundary_case")
    unresolved = next(x for x in review.items if x.item_type == "unresolved_negative_case_search")

    integration = [
        {
            "kind": "convergence",
            "statement": (
                "The accepted agency prediction and the descriptive first-year comparison point "
                "in the same reduction direction, while the qualitative record contains some "
                "passages discussing potential traffic or emissions benefits."
            ),
            "limit": "Directional convergence is not a causal-effect estimate or a prevalence claim.",
        },
        {
            "kind": "complementarity",
            "statement": (
                "The qualitative strand adds concerns about financial burden, transit alternatives, "
                "transparency, exemptions, toll caps, and implementation conditions that the traffic "
                "entry arithmetic does not measure."
            ),
            "limit": "Qualitative hearing evidence characterizes the admitted corpus, not the population.",
        },
        {
            "kind": "divergence",
            "statement": (
                "The descriptive comparison is about 11.39% below the agency No Action baseline, "
                "which is smaller than the agency's 13.4% pre-implementation prediction."
            ),
            "limit": "This comparison uses the agency frame and does not independently reconstruct its counterfactual.",
        },
        {
            "kind": "silence",
            "statement": (
                "Neither strand establishes net policy benefit: the quantitative strand is silent "
                "on lived burdens and the qualitative strand does not identify causal traffic effects "
                "or population prevalence."
            ),
            "limit": "No cross-method scalar confidence score or autonomous policy recommendation is produced.",
        },
    ]

    return {
        "schema_version": "mmw.nyc_crz_integrated.v1",
        "investigation_id": "nyc-congestion-relief-zone-first-year",
        "status": "integration_complete_pending_mvp_review",
        "qualitative": {
            "owner": "qualitative_coding",
            "producer_revision": binding["producer_revision"],
            "handoff_sha256": review.source_handoff_sha256,
            "review_status": review.status,
            "methodology": handoff.methodology,
            "findings": substantive,
            "boundary_case": boundary.model_dump(mode="json"),
            "unresolved": unresolved.model_dump(mode="json"),
            "anchors": {key: value.model_dump(mode="json") for key, value in handoff.anchors.items()},
            "claim_limits": handoff.non_claims,
        },
        "extraction_baseline": extraction,
        "quantitative": quantitative,
        "integration": integration,
        "policy_appraisal": {
            "status": "needs_human_priorities",
            "decision": None,
            "reason": (
                "Evidence integration does not supply human-owned criterion weights or priority "
                "judgments required for a retain/change/monitor appraisal."
            ),
        },
        "baseline_vs_federated": {
            "baseline": (
                "The capable baseline could compare the agency prediction with descriptive traffic "
                "arithmetic and retain one accepted medical-access concern, but lacked a complete "
                "method-owned six-hearing qualitative account."
            ),
            "federated": (
                "The federated view now preserves a human-approved six-hearing qualitative result, "
                "exact source anchors, native method ownership, review standing, an explicit boundary "
                "case, and an unresolved negative-case-search result alongside the quantitative audit."
            ),
            "improves": [
                "reconstruction and source traceability",
                "native method semantics and human review standing",
                "visibility of variation and unresolved states",
                "revision-ready dependency bindings through exact artifact hashes",
            ],
            "does_not_improve": [
                "underlying evidence quality",
                "causal identification",
                "population representativeness or prevalence",
                "policy value judgments or priority weights",
            ],
            "architecture_result": (
                "No universal analytical IR, O-to-A ontology, revision engine, or generic warrant "
                "calculus was required for this integration."
            ),
        },
    }
