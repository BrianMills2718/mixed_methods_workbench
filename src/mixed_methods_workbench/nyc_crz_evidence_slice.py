"""First authentic, review-gated NYC congestion-pricing evidence slice.

This module deliberately separates a reusable structural capability (extract a
typed candidate and bind it to exact source text) from later method-owned
interpretation.  A valid model response remains a candidate until an
attributable human decision promotes it.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

CandidateId = Literal[
    "prediction-reevaluation-2-objective-2",
    "concern-hearing-2022-08-25-medical-access",
]

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = PROJECT_ROOT / "examples" / "fixtures" / "nyc_crz_evidence_slice"
VEHICLE_DATA_PATH = (
    PROJECT_ROOT
    / "docs"
    / "research"
    / "evidence"
    / "nyc_crz_mvp_v1"
    / "t6yz_first_year_daily_by_group_class.csv"
)
EXPECTED_VEHICLE_DATA_SHA256 = (
    "01dec3a0a1effc26aacf57ba8c4474775fb4db73149c462d4f40432e6e323bd3"
)

# Filled with exact committed fixture bytes. Mutation is an invalidation, not a
# request to accept newer content.
EXPECTED_FIXTURE_DIGESTS: dict[str, str] = {
    "candidate_extraction.json": "efe2865af363d3d749b07e1e94007bfba5c1d49d3b9409ad5608361e749e1768",
    "source_units.json": "974a95ec812e730c1cf74da03926eecd87674167e3f0137ae91ca1099fad881b",
    "canary_run_receipt.json": "1cc75a9200a3c303007b16da907c18dae22f8e431eb6cc4943555d2c94d70a77",
    "review_packet.json": "bee66d1d2da24c2a65d9207de48f4a266df1849f06e451995591b5bac3ea3122",
}


class NycCrzEvidenceSliceError(ValueError):
    """Raised when provenance, binding, review, or frozen data cannot be trusted."""


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class SourceDocumentReceipt(_StrictModel):
    packet_id: Literal["NYC-CRZ-MVP-v1"]
    artifact_id: Literal["reevaluation_2", "hearing_2022_08_25"]
    official_url: str
    expected_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    observed_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    expected_bytes: int = Field(gt=0)
    observed_bytes: int = Field(gt=0)
    verified_at: str
    exact_byte_verified: Literal[True]

    @model_validator(mode="after")
    def _verified(self) -> SourceDocumentReceipt:
        if self.expected_sha256 != self.observed_sha256:
            raise ValueError("source_digest_mismatch")
        if self.expected_bytes != self.observed_bytes:
            raise ValueError("source_byte_count_mismatch")
        return self


class SourceUnit(_StrictModel):
    source_unit_id: str = Field(min_length=1)
    artifact_id: Literal["reevaluation_2", "hearing_2022_08_25"]
    artifact_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    pdf_page_index: int = Field(ge=0)
    printed_page_label: str | None
    structural_locator: str = Field(min_length=1)
    context_text: str = Field(min_length=20)
    context_text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    derivation: Literal["pypdf_text_extraction_then_deterministic_normalization"]

    @model_validator(mode="after")
    def _context_hash(self) -> SourceUnit:
        if text_sha256(self.context_text) != self.context_text_sha256:
            raise ValueError("context_hash_mismatch")
        return self


class EvidenceAnchor(_StrictModel):
    anchor_id: str = Field(min_length=1)
    source_unit_id: str = Field(min_length=1)
    source_artifact_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    selected_text: str = Field(min_length=8)
    selected_text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    context_text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    selection_match: Literal["exact", "whitespace_normalized"]
    occurrence_index: Literal[0]
    review_state: Literal["model_generated_pending_human_review"]
    lineage_ref: CandidateId


class CandidatePrediction(_StrictModel):
    candidate_id: Literal["prediction-reevaluation-2-objective-2"]
    source_unit_id: str
    statement: str
    metric: Literal["daily_vehicles_entering_manhattan_cbd"]
    direction: Literal["decrease"]
    expected_change_percent: float
    basis: Literal["No Action"]
    scenario: str
    quote: str
    generated_limit: str


class CandidateConcern(_StrictModel):
    candidate_id: Literal["concern-hearing-2022-08-25-medical-access"]
    source_unit_id: str
    statement: str
    affected_groups: list[str] = Field(min_length=1)
    kind: Literal["access_cost_burden"]
    quote: str
    generated_limit: str


class CandidateExtraction(_StrictModel):
    schema_version: Literal["mmw.document_candidates.v0.1"]
    packet_id: Literal["NYC-CRZ-MVP-v1"]
    assertion_source: Literal["agency_and_hearing_participant"]
    derivation: Literal["llm_structured_extraction"]
    prediction: CandidatePrediction
    concern: CandidateConcern


class RunAttempt(_StrictModel):
    ordinal: int = Field(ge=1, le=3)
    trace_id: str
    logical_call_id: str
    output_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    disposition: Literal[
        "rejected_anchor_binding",
        "rejected_source_unit_scope",
        "retained_pending_human_review",
    ]
    refusal_code: str | None
    note: str


class CanaryRunReceipt(_StrictModel):
    schema_version: Literal["mmw.llm_canary_receipt.v0.1"]
    model_requested: Literal["openrouter/deepseek/deepseek-v4-flash"]
    model_resolved: Literal["openrouter/deepseek/deepseek-v4-flash"]
    prompt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    schema_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    prediction_context_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    concern_context_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    cache_hit: Literal[False]
    prompt_tokens: int = Field(ge=1)
    completion_tokens: int = Field(ge=1)
    total_cost_usd: float = Field(ge=0)
    cost_source: Literal["provider_reported"]
    attempts: list[RunAttempt] = Field(min_length=3, max_length=3)


class FieldDisposition(_StrictModel):
    field_path: Literal["prediction.generated_limit", "concern.generated_limit"]
    status: Literal["rejected"]
    reason: str


class ReviewDecision(_StrictModel):
    status: Literal["pending_human_review", "rejected", "accepted"]
    reviewer_kind: Literal["human"]
    decision_ref: str | None = None
    decided_at: str | None = None
    field_dispositions: list[FieldDisposition]
    publication_disposition: Literal["withhold_until_human_review"]

    @model_validator(mode="after")
    def _human_acceptance_is_attributable(self) -> ReviewDecision:
        if self.status == "accepted" and (not self.decision_ref or not self.decided_at):
            raise ValueError("accepted_candidate_requires_attributable_human_decision")
        if self.status != "accepted" and self.publication_disposition != "withhold_until_human_review":
            raise ValueError("unaccepted_candidate_must_be_withheld")
        return self


class ReviewPacket(_StrictModel):
    schema_version: Literal["mmw.candidate_review.v0.1"]
    review: ReviewDecision
    proposed_prediction_wording: str
    proposed_concern_wording: str
    deterministic_claim_limits: list[str] = Field(min_length=3)
    review_questions: list[str] = Field(min_length=2)


class DescriptiveAggregate(_StrictModel):
    artifact_id: Literal["t6yz_first_year_daily_by_group_class"]
    artifact_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    coverage_start: str
    coverage_end: str
    observed_days: int = Field(gt=0)
    crz_entries: int = Field(ge=0)
    excluded_roadway_entries: int = Field(ge=0)
    mean_daily_crz_entries: float
    evidence_kind: Literal["observed_public_data"]
    permitted_claim: Literal[
        "Descriptive first-operating-year vehicle-entry aggregation only; not revenue and not a causal effect."
    ]

    @model_validator(mode="after")
    def _matches_frozen_receipt(self) -> DescriptiveAggregate:
        observed = (
            self.coverage_start,
            self.coverage_end,
            self.observed_days,
            self.crz_entries,
            self.excluded_roadway_entries,
        )
        expected = ("2025-01-05", "2025-12-31", 361, 178_203_234, 23_461_361)
        if observed != expected:
            raise ValueError("frozen_vehicle_aggregate_mismatch")
        return self


class NycCrzEvidenceSlice(_StrictModel):
    schema_version: Literal["mmw.nyc_crz_evidence_slice.v0.1"]
    investigation_id: Literal["nyc-congestion-relief-zone-first-year"]
    title: str
    status: Literal["candidate_review_required"]
    status_label: str
    research_question: str
    capability_flow: list[str] = Field(min_length=4)
    source_documents: list[SourceDocumentReceipt] = Field(min_length=2, max_length=2)
    source_units: list[SourceUnit] = Field(min_length=2, max_length=2)
    extraction: CandidateExtraction
    anchors: list[EvidenceAnchor] = Field(min_length=2, max_length=2)
    run_receipt: CanaryRunReceipt
    review_packet: ReviewPacket
    observation: DescriptiveAggregate

    @model_validator(mode="after")
    def _coherent_bindings(self) -> NycCrzEvidenceSlice:
        units = {unit.source_unit_id: unit for unit in self.source_units}
        docs = {doc.artifact_id: doc for doc in self.source_documents}
        if set(docs) != {unit.artifact_id for unit in self.source_units}:
            raise ValueError("source_units_do_not_resolve_verified_documents")
        for unit in self.source_units:
            if unit.artifact_sha256 != docs[unit.artifact_id].observed_sha256:
                raise ValueError("source_unit_artifact_digest_mismatch")
        if self.run_receipt.prediction_context_sha256 != units[
            self.extraction.prediction.source_unit_id
        ].context_text_sha256:
            raise ValueError("prediction_receipt_context_mismatch")
        if self.run_receipt.concern_context_sha256 != units[
            self.extraction.concern.source_unit_id
        ].context_text_sha256:
            raise ValueError("concern_receipt_context_mismatch")
        candidates: list[CandidatePrediction | CandidateConcern] = [
            self.extraction.prediction,
            self.extraction.concern,
        ]
        if {candidate.source_unit_id for candidate in candidates} != set(units):
            raise ValueError("candidate_source_units_do_not_resolve")
        if len(self.anchors) != len(candidates):
            raise ValueError("each_candidate_requires_one_anchor")
        candidate_by_id = {candidate.candidate_id: candidate for candidate in candidates}
        for anchor in self.anchors:
            candidate = candidate_by_id.get(anchor.lineage_ref)
            if candidate is None:
                raise ValueError("anchor_lineage_does_not_resolve")
            unit = units[anchor.source_unit_id]
            doc = docs[unit.artifact_id]
            if anchor.source_unit_id != candidate.source_unit_id:
                raise ValueError("anchor_candidate_source_unit_mismatch")
            if anchor.source_artifact_sha256 != doc.observed_sha256:
                raise ValueError("anchor_source_digest_mismatch")
            if anchor.context_text_sha256 != unit.context_text_sha256:
                raise ValueError("anchor_context_digest_mismatch")
            if anchor.selected_text_sha256 != text_sha256(anchor.selected_text):
                raise ValueError("selected_text_hash_mismatch")
            selected = anchor.selected_text
            context = unit.context_text
            if anchor.selection_match == "whitespace_normalized":
                selected = normalize_whitespace(selected)
                context = normalize_whitespace(context)
            if context.count(selected) != 1:
                raise ValueError("selected_text_must_bind_uniquely")
            if anchor.selected_text != candidate.quote:
                raise ValueError("anchor_must_bind_candidate_quote")
        if self.review_packet.review.status == "accepted":
            raise ValueError("committed_canary_must_remain_pending_human_review")
        return self


def bytes_sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def text_sha256(value: str) -> str:
    return bytes_sha256(value.encode("utf-8"))


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_source_document(
    path: Path, *, expected_sha256: str, expected_bytes: int
) -> tuple[str, int]:
    """Refuse a source before parsing unless both exact-byte checks pass."""

    if not path.is_file():
        raise NycCrzEvidenceSliceError(f"source document is missing: {path.name}")
    observed_bytes = path.stat().st_size
    observed_sha256 = file_sha256(path)
    if observed_bytes != expected_bytes:
        raise NycCrzEvidenceSliceError(
            f"source byte count mismatch: expected {expected_bytes}, observed {observed_bytes}"
        )
    if observed_sha256 != expected_sha256:
        raise NycCrzEvidenceSliceError(
            f"source digest mismatch: expected {expected_sha256}, observed {observed_sha256}"
        )
    return observed_sha256, observed_bytes


def _read_pinned(root: Path, name: str) -> object:
    path = root / name
    if not path.is_file():
        raise NycCrzEvidenceSliceError(f"required NYC artifact is missing: {name}")
    observed = file_sha256(path)
    expected = EXPECTED_FIXTURE_DIGESTS[name]
    if observed != expected:
        raise NycCrzEvidenceSliceError(
            f"NYC artifact digest mismatch for {name}: expected {expected}, observed {observed}"
        )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise NycCrzEvidenceSliceError(f"invalid JSON in NYC artifact: {name}") from exc


def load_vehicle_aggregate(path: Path = VEHICLE_DATA_PATH) -> DescriptiveAggregate:
    """Recompute the smallest frozen descriptive aggregate from exact CSV bytes."""

    observed_digest = file_sha256(path)
    if observed_digest != EXPECTED_VEHICLE_DATA_SHA256:
        raise NycCrzEvidenceSliceError(
            "vehicle snapshot digest mismatch: "
            f"expected {EXPECTED_VEHICLE_DATA_SHA256}, observed {observed_digest}"
        )
    daily: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            date = row["toll_date"][:10]
            daily[date][0] += int(row["crz_entries"])
            daily[date][1] += int(row["excluded_roadway_entries"])
    if not daily:
        raise NycCrzEvidenceSliceError("vehicle snapshot contains no observations")
    crz_entries = sum(values[0] for values in daily.values())
    excluded_entries = sum(values[1] for values in daily.values())
    try:
        return DescriptiveAggregate(
            artifact_id="t6yz_first_year_daily_by_group_class",
            artifact_sha256=observed_digest,
            coverage_start=min(daily),
            coverage_end=max(daily),
            observed_days=len(daily),
            crz_entries=crz_entries,
            excluded_roadway_entries=excluded_entries,
            mean_daily_crz_entries=crz_entries / len(daily),
            evidence_kind="observed_public_data",
            permitted_claim=(
                "Descriptive first-operating-year vehicle-entry aggregation only; "
                "not revenue and not a causal effect."
            ),
        )
    except ValueError as exc:
        raise NycCrzEvidenceSliceError(f"unexpected frozen aggregate: {exc}") from exc


def load_nyc_crz_evidence_slice(root: Path = FIXTURE_ROOT) -> NycCrzEvidenceSlice:
    """Load exact receipts and expose a review-gated, non-methodological projection."""

    try:
        extraction = CandidateExtraction.model_validate(
            _read_pinned(root, "candidate_extraction.json")
        )
        source_payload = _read_pinned(root, "source_units.json")
        receipt = CanaryRunReceipt.model_validate(
            _read_pinned(root, "canary_run_receipt.json")
        )
        review = ReviewPacket.model_validate(_read_pinned(root, "review_packet.json"))
        if not isinstance(source_payload, dict):
            raise TypeError("source_units payload must be an object")
        documents = [
            SourceDocumentReceipt.model_validate(item)
            for item in source_payload["source_documents"]
        ]
        units = [SourceUnit.model_validate(item) for item in source_payload["source_units"]]
        anchors = [EvidenceAnchor.model_validate(item) for item in source_payload["anchors"]]
        observation = load_vehicle_aggregate()
        return NycCrzEvidenceSlice(
            schema_version="mmw.nyc_crz_evidence_slice.v0.1",
            investigation_id="nyc-congestion-relief-zone-first-year",
            title="What does the first year of New York's congestion-pricing record show?",
            status="candidate_review_required",
            status_label="Two source-bound candidates await human review; no finding is accepted yet.",
            research_question=(
                "After the first operating year, which predicted changes and stakeholder "
                "concerns are corroborated, contradicted, or unresolved by reproducible public "
                "evidence, and what should decision-makers retain, change, or monitor?"
            ),
            capability_flow=[
                "verify exact source bytes",
                "extract typed candidates from bounded text",
                "bind each quote uniquely to its source unit",
                "require attributable human review",
                "hand accepted records to method-owned analysis",
            ],
            source_documents=documents,
            source_units=units,
            extraction=extraction,
            anchors=anchors,
            run_receipt=receipt,
            review_packet=review,
            observation=observation,
        )
    except NycCrzEvidenceSliceError:
        raise
    except (KeyError, TypeError, ValueError) as exc:
        raise NycCrzEvidenceSliceError(f"invalid NYC evidence boundary: {exc}") from exc


def nyc_crz_evidence_slice_payload(root: Path = FIXTURE_ROOT) -> dict[str, object]:
    return load_nyc_crz_evidence_slice(root).model_dump(mode="json")
