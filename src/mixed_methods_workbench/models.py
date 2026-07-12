"""Pydantic contracts that preserve method distinctions in the DEMO-C1 slice."""

from __future__ import annotations

import hashlib
from pathlib import PurePosixPath
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


SHA256_PATTERN = r"^[0-9a-f]{64}$"
DEMO_LIMITS = {
    "Synthetic demonstration only.",
    "Not empirical evidence.",
    "Not methodological-validity evidence.",
    "Not mixed-methods evidence.",
}


class StrictModel(BaseModel):
    """Reject producer-shaped fields that the reviewed contract did not authorize."""

    model_config = ConfigDict(extra="forbid")


class CompatibleModel(BaseModel):
    """Accept compatible producer extensions while requiring supported semantics."""

    model_config = ConfigDict(extra="ignore")


class SourceSegment(StrictModel):
    """Bind one exact synthetic passage to stable document offsets and bytes."""

    segment_id: str = Field(min_length=1)
    document_id: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(gt=0)
    text: str = Field(min_length=1)
    text_sha256: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_exact_span(self) -> SourceSegment:
        """Reject offsets or hashes that cannot identify the displayed passage exactly."""
        if self.end_char - self.start_char != len(self.text):
            raise ValueError("segment offsets must span the exact text length")
        digest = hashlib.sha256(self.text.encode("utf-8")).hexdigest()
        if self.text_sha256 != digest:
            raise ValueError("segment text_sha256 must match the exact text bytes")
        return self


class DemoDocument(StrictModel):
    """Group synthetic source segments under one stable source identity."""

    document_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_kind: Literal["leadership_memo", "staff_interview", "implementation_log"]
    segments: list[SourceSegment] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_segment_ownership(self) -> DemoDocument:
        """Ensure every nested segment belongs to this document and is uniquely named."""
        ids = [segment.segment_id for segment in self.segments]
        if len(ids) != len(set(ids)):
            raise ValueError("document segment IDs must be unique")
        if any(segment.document_id != self.document_id for segment in self.segments):
            raise ValueError("segment document_id must match its containing document")
        return self


class ControlledDemoPacket(StrictModel):
    """Define the only source universe that DEMO-C1 method fixtures may analyze."""

    schema_version: Literal[1]
    artifact_status: Literal["synthetic_demo_fixture"]
    packet_id: str = Field(min_length=1)
    research_question: str = Field(min_length=1)
    documents: list[DemoDocument] = Field(min_length=1)
    claim_limits: list[str] = Field(min_length=4)

    @model_validator(mode="after")
    def validate_packet_scope(self) -> ControlledDemoPacket:
        """Require unique IDs and the complete software-only claim boundary."""
        document_ids = [document.document_id for document in self.documents]
        if len(document_ids) != len(set(document_ids)):
            raise ValueError("demo document IDs must be unique")
        segment_ids = [
            segment.segment_id for document in self.documents for segment in document.segments
        ]
        if len(segment_ids) != len(set(segment_ids)):
            raise ValueError("demo segment IDs must be globally unique")
        if not DEMO_LIMITS.issubset(set(self.claim_limits)):
            raise ValueError("demo packet must carry every required synthetic claim limit")
        return self

    def segment_ids(self) -> set[str]:
        """Return the exact segment universe used for method step-down validation."""
        return {segment.segment_id for document in self.documents for segment in document.segments}


class DemoFixtureEntry(StrictModel):
    """Inventory one committed synthetic DEMO-C1 payload and its exact bytes."""

    path: str = Field(min_length=1)
    sha256: str = Field(pattern=SHA256_PATTERN)
    origin_kind: Literal["workbench_synthetic"]
    evidence_grade: Literal["C-synthetic-contract-only"]
    intended_invariant: str = Field(min_length=1)
    claim_limits: list[str] = Field(min_length=1)


class DemoFixtureManifest(StrictModel):
    """Make the positive fixture inventory, commands, and claim boundary explicit."""

    schema_version: Literal[1]
    artifact_status: Literal["synthetic_demo_fixture"]
    authoring_repository: Literal["mixed_methods_workbench"]
    files: list[DemoFixtureEntry] = Field(min_length=5)
    validation_commands: list[str] = Field(min_length=2)
    claim_limits: list[str] = Field(min_length=4)

    @model_validator(mode="after")
    def validate_inventory_contract(self) -> DemoFixtureManifest:
        """Require unique entries and the complete synthetic-only claim boundary."""
        paths = [entry.path for entry in self.files]
        if len(paths) != len(set(paths)):
            raise ValueError("DEMO-C1 manifest paths must be unique")
        for raw_path in paths:
            path = PurePosixPath(raw_path)
            if path.is_absolute() or len(path.parts) != 1 or path.suffix.casefold() != ".json":
                raise ValueError("DEMO-C1 manifest paths must be flat relative JSON filenames")
        if not DEMO_LIMITS.issubset(set(self.claim_limits)):
            raise ValueError("DEMO-C1 manifest must carry every synthetic claim limit")
        return self


class MethodEnvelope(StrictModel):
    """Carry shared provenance without flattening method-owned inference objects."""

    schema_version: Literal[1]
    artifact_status: Literal["synthetic_demo_fixture"]
    packet_id: str = Field(min_length=1)
    producer: str = Field(min_length=1)
    claim_limits: list[str] = Field(min_length=1)


class QCClaim(StrictModel):
    """Represent a qualitative interpretation with supporting and qualifying passages."""

    claim_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    supporting_segment_ids: list[str] = Field(min_length=1)
    contrary_segment_ids: list[str]
    review_status: Literal["needs_human_review", "retained", "revised", "rejected"]


class QCPattern(StrictModel):
    """Describe a recurring or contrasting framing without causal inference."""

    pattern_id: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    segment_ids: list[str] = Field(min_length=1)
    interpretation: Literal["descriptive_only"]


class StrictQCExport(MethodEnvelope):
    """Strict synthetic producer shape for qualitative evidence and interpretations."""

    method: Literal["qualitative_coding"]
    corpus_segment_ids: list[str] = Field(min_length=1)
    claims: list[QCClaim] = Field(min_length=1)
    patterns: list[QCPattern] = Field(min_length=1)
    memo_ids: list[str] = Field(min_length=1)


class RivalHypothesis(StrictModel):
    """Name one process-tracing rival, including the required residual rival."""

    hypothesis_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    is_residual: bool


class PTEvidence(StrictModel):
    """Bind one observation to rivals without storing a generic truth probability."""

    evidence_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    segment_ids: list[str] = Field(min_length=1)
    hypothesis_ids: list[str] = Field(min_length=2)


class ComparativeSupport(StrictModel):
    """Keep ordinal within-case support distinct from probability of truth."""

    ranked_hypothesis_ids: list[str] = Field(min_length=2)
    sensitivity: Literal["low", "medium", "high"]
    verdict: str = Field(min_length=1)


class StrictPTExport(MethodEnvelope):
    """Strict synthetic producer shape for rival process-tracing assessment."""

    method: Literal["process_tracing"]
    hypotheses: list[RivalHypothesis] = Field(min_length=2)
    evidence: list[PTEvidence] = Field(min_length=1)
    comparative_support: ComparativeSupport
    source_gaps: list[str]

    @model_validator(mode="after")
    def validate_rivals(self) -> StrictPTExport:
        """Require a coherent rival set, residual, evidence references, and ranking."""
        ids = [hypothesis.hypothesis_id for hypothesis in self.hypotheses]
        if len(ids) != len(set(ids)):
            raise ValueError("PT hypothesis IDs must be unique")
        if sum(hypothesis.is_residual for hypothesis in self.hypotheses) != 1:
            raise ValueError("PT export must contain exactly one residual hypothesis")
        id_set = set(ids)
        if set(self.comparative_support.ranked_hypothesis_ids) != id_set:
            raise ValueError("PT comparative ranking must contain every rival exactly once")
        for evidence in self.evidence:
            if not set(evidence.hypothesis_ids).issubset(id_set):
                raise ValueError("PT evidence references an unknown hypothesis")
        forbidden = ("probability of truth", "percent probability", "% probability")
        if any(term in self.comparative_support.verdict.lower() for term in forbidden):
            raise ValueError("PT verdict must not state probability of truth")
        return self


class ComparisonIteration(StrictModel):
    """Preserve how a GT-inspired category changed across source comparisons."""

    iteration: int = Field(ge=1)
    segment_id: str = Field(min_length=1)
    action: Literal["created", "revised", "narrowed", "confirmed"]
    note: str = Field(min_length=1)


class GTCategory(StrictModel):
    """Represent a provisional category and its observable development gaps."""

    category_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    properties: list[str] = Field(min_length=1)
    dimensions: list[str] = Field(min_length=1)
    supporting_segment_ids: list[str] = Field(min_length=1)
    comparison_trace: list[ComparisonIteration] = Field(min_length=1)
    adequacy_status: Literal["underdeveloped", "developing", "adequate"]
    adequacy_gaps: list[str]


class GTMemo(StrictModel):
    """Attach an interpretive memo to categories and exact comparison passages."""

    memo_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    category_ids: list[str] = Field(min_length=1)
    segment_ids: list[str] = Field(min_length=1)


class StrictGTInspiredExport(MethodEnvelope):
    """Strict synthetic shape for GT-inspired development without saturation claims."""

    method: Literal["grounded_theory_inspired"]
    categories: list[GTCategory] = Field(min_length=1)
    memos: list[GTMemo] = Field(min_length=1)
    next_sampling_suggestions: list[str] = Field(min_length=1)
    methodological_limits: list[str] = Field(min_length=2)

    @model_validator(mode="after")
    def validate_gt_claim_discipline(self) -> StrictGTInspiredExport:
        """Require explicit limits and coherent category/memo comparison provenance."""
        required = {
            "Not full grounded theory.",
            "Category adequacy diagnostics are not saturation proof.",
        }
        if not required.issubset(set(self.methodological_limits)):
            raise ValueError("GT-inspired export must state no-full-GT and no-saturation limits")
        category_ids = {category.category_id for category in self.categories}
        if len(category_ids) != len(self.categories):
            raise ValueError("GT category IDs must be unique")
        for memo in self.memos:
            if not set(memo.category_ids).issubset(category_ids):
                raise ValueError("GT memo references an unknown category")
        return self


class CompatibleQCView(CompatibleModel):
    """Consume supported QC semantics while tolerating future compatible extras."""

    schema_version: Literal[1]
    packet_id: str
    method: Literal["qualitative_coding"]
    claims: list[QCClaim]
    patterns: list[QCPattern]
    claim_limits: list[str]


class CompatiblePTView(CompatibleModel):
    """Consume supported PT semantics without importing producer internals."""

    schema_version: Literal[1]
    packet_id: str
    method: Literal["process_tracing"]
    hypotheses: list[RivalHypothesis]
    evidence: list[PTEvidence]
    comparative_support: ComparativeSupport
    source_gaps: list[str]
    claim_limits: list[str]


class CompatibleGTInspiredView(CompatibleModel):
    """Consume supported GT-inspired semantics while retaining method limits."""

    schema_version: Literal[1]
    packet_id: str
    method: Literal["grounded_theory_inspired"]
    categories: list[GTCategory]
    memos: list[GTMemo]
    next_sampling_suggestions: list[str]
    methodological_limits: list[str]
    claim_limits: list[str]


class ObjectRef(StrictModel):
    """Identify one native method object without copying or rewriting it."""

    method: Literal["qualitative_coding", "process_tracing", "grounded_theory_inspired"]
    object_id: str = Field(min_length=1)


class CrossMethodLink(StrictModel):
    """Relate native objects neutrally without asserting evidentiary support."""

    link_id: str = Field(min_length=1)
    source: ObjectRef
    relationship: Literal["addresses", "challenges", "contextualizes", "unresolved"]
    target: ObjectRef
    reviewer_meaning: str = Field(min_length=1)


class CoreDemoReviewPacket(StrictModel):
    """Provide a three-lane review view with exact step-down and no scalar synthesis."""

    schema_version: Literal[1]
    artifact_status: Literal["synthetic_demo_fixture"]
    packet: ControlledDemoPacket
    qc: CompatibleQCView
    pt: CompatiblePTView
    gt_inspired: CompatibleGTInspiredView
    links: list[CrossMethodLink] = Field(min_length=1)
    claim_limits: list[str] = Field(min_length=4)

    @model_validator(mode="after")
    def validate_review_scope(self) -> CoreDemoReviewPacket:
        """Keep every lane bound to one packet and preserve the synthetic claim boundary."""
        packet_ids = {
            self.packet.packet_id,
            self.qc.packet_id,
            self.pt.packet_id,
            self.gt_inspired.packet_id,
        }
        if len(packet_ids) != 1:
            raise ValueError("all review lanes must bind to the same controlled packet")
        if not DEMO_LIMITS.issubset(set(self.claim_limits)):
            raise ValueError("review packet must carry every required synthetic claim limit")
        return self
