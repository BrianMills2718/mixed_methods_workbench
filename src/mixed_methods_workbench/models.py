"""Pydantic contracts that preserve method distinctions in the DEMO-C1 slice."""

from __future__ import annotations

import hashlib
from pathlib import PurePosixPath
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


SHA256_PATTERN = r"^[0-9a-f]{64}$"
DEMO_LIMITS = frozenset(
    {
        "Synthetic demonstration only.",
        "Not empirical evidence.",
        "Not methodological-validity evidence.",
        "Not mixed-methods evidence.",
    }
)
QC_LIMITS = frozenset(
    {
        "Synthetic QC shape only.",
        "No process-tracing comparative support.",
        "Qualitative interpretation is not causal proof.",
    }
)
PT_LIMITS = frozenset(
    {
        "Synthetic PT shape only.",
        "Comparative support is not probability of truth.",
        "No population causal effect is estimated.",
    }
)
GT_LIMITS = frozenset(
    {
        "Synthetic GT-inspired shape only.",
        "No theoretical sampling was executed.",
        "No substantive theory is validated.",
    }
)
GT_METHOD_LIMITS = frozenset(
    {
        "Not full grounded theory.",
        "Category adequacy diagnostics are not saturation proof.",
    }
)
MANIFEST_COMMANDS = (
    "make validate-demo-fixtures",
    "make validate-demo-controls",
)
MANIFEST_INVARIANTS = {
    "packet.json": "One stable synthetic source universe binds all three method lanes.",
    "qc.json": "QC interpretations remain anchored and contain no PT inference fields.",
    "pt.json": "PT preserves rival comparative support without probability-of-truth language.",
    "gt_inspired.json": (
        "GT-inspired development remains traceable without full-GT or saturation claims."
    ),
    "links.json": (
        "Cross-method links remain neutral references rather than evidentiary aggregation."
    ),
}
MANIFEST_ENTRY_LIMITS = {
    "packet.json": frozenset({"Not a real corpus.", "Not empirical evidence."}),
    "qc.json": frozenset({"Not a qualitative_coding export.", "Not qualitative evidence."}),
    "pt.json": frozenset({"Not a process_tracing export.", "Not process-tracing evidence."}),
    "gt_inspired.json": frozenset(
        {"Not a qualitative_coding export.", "Not full grounded theory."}
    ),
    "links.json": frozenset({"Not mixed-methods integration.", "No generic confidence score."}),
}


def _require_exact_strings(actual: list[str], expected: frozenset[str], context: str) -> None:
    """Reject missing, duplicate, or escalatory prose on a closed claim boundary."""
    if len(actual) != len(expected) or set(actual) != expected:
        raise ValueError(f"{context} must exactly match its reviewed claim boundary")


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
    content: str = Field(min_length=1)
    content_sha256: str = Field(pattern=SHA256_PATTERN)
    segments: list[SourceSegment] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_segment_ownership(self) -> DemoDocument:
        """Ensure every nested segment belongs to this document and is uniquely named."""
        ids = [segment.segment_id for segment in self.segments]
        if len(ids) != len(set(ids)):
            raise ValueError("document segment IDs must be unique")
        if any(segment.document_id != self.document_id for segment in self.segments):
            raise ValueError("segment document_id must match its containing document")
        digest = hashlib.sha256(self.content.encode("utf-8")).hexdigest()
        if digest != self.content_sha256:
            raise ValueError("document content_sha256 must match the exact content bytes")
        for segment in self.segments:
            if self.content[segment.start_char : segment.end_char] != segment.text:
                raise ValueError("segment offsets must resolve to exact text in document content")
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
        _require_exact_strings(self.claim_limits, DEMO_LIMITS, "demo packet claim_limits")
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
        if set(paths) != set(MANIFEST_INVARIANTS):
            raise ValueError("DEMO-C1 manifest must list the reviewed five-file payload exactly")
        for entry in self.files:
            if entry.intended_invariant != MANIFEST_INVARIANTS[entry.path]:
                raise ValueError(f"DEMO-C1 manifest invariant mismatch: {entry.path}")
            _require_exact_strings(
                entry.claim_limits,
                MANIFEST_ENTRY_LIMITS[entry.path],
                f"DEMO-C1 manifest claim_limits for {entry.path}",
            )
        if tuple(self.validation_commands) != MANIFEST_COMMANDS:
            raise ValueError("DEMO-C1 manifest validation_commands must match reviewed commands")
        _require_exact_strings(self.claim_limits, DEMO_LIMITS, "DEMO-C1 manifest claim_limits")
        return self


class MethodEnvelope(StrictModel):
    """Carry shared provenance without flattening method-owned inference objects."""

    schema_version: Literal[1]
    artifact_status: Literal["synthetic_demo_fixture"]
    packet_id: str = Field(min_length=1)
    producer: str = Field(min_length=1)
    prose_status: Literal["synthetic_non_authoritative_human_review_required"]
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

    @model_validator(mode="after")
    def validate_qc_claim_discipline(self) -> StrictQCExport:
        """Close structural QC claims while marking all open prose non-authoritative."""
        _require_exact_strings(self.claim_limits, QC_LIMITS, "QC claim_limits")
        claim_ids = [claim.claim_id for claim in self.claims]
        pattern_ids = [pattern.pattern_id for pattern in self.patterns]
        if len(claim_ids) != len(set(claim_ids)):
            raise ValueError("QC claim IDs must be unique within their native object kind")
        if len(pattern_ids) != len(set(pattern_ids)):
            raise ValueError("QC pattern IDs must be unique within their native object kind")
        return self


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
        ranking = self.comparative_support.ranked_hypothesis_ids
        if (
            len(ranking) != len(id_set)
            or len(ranking) != len(set(ranking))
            or set(ranking) != id_set
        ):
            raise ValueError("PT comparative ranking must contain every rival exactly once")
        for evidence in self.evidence:
            if len(evidence.hypothesis_ids) != len(set(evidence.hypothesis_ids)):
                raise ValueError("PT evidence hypothesis references must be unique")
            if not set(evidence.hypothesis_ids).issubset(id_set):
                raise ValueError("PT evidence references an unknown hypothesis")
        evidence_ids = [evidence.evidence_id for evidence in self.evidence]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("PT evidence IDs must be unique within their native object kind")
        _require_exact_strings(self.claim_limits, PT_LIMITS, "PT claim_limits")
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

    @model_validator(mode="after")
    def validate_comparison_sequence(self) -> GTCategory:
        """Reject duplicated or discontinuous iterations that fake comparison provenance."""
        iterations = [item.iteration for item in self.comparison_trace]
        if iterations != list(range(1, len(iterations) + 1)):
            raise ValueError("GT comparison iterations must be unique, ordered, and contiguous")
        return self


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
        _require_exact_strings(
            self.methodological_limits,
            GT_METHOD_LIMITS,
            "GT-inspired methodological_limits",
        )
        _require_exact_strings(self.claim_limits, GT_LIMITS, "GT-inspired claim_limits")
        category_ids = {category.category_id for category in self.categories}
        if len(category_ids) != len(self.categories):
            raise ValueError("GT category IDs must be unique")
        for memo in self.memos:
            if not set(memo.category_ids).issubset(category_ids):
                raise ValueError("GT memo references an unknown category")
        memo_ids = [memo.memo_id for memo in self.memos]
        if len(memo_ids) != len(set(memo_ids)):
            raise ValueError("GT memo IDs must be unique within their native object kind")
        return self


class CompatibleQCView(CompatibleModel):
    """Consume supported QC semantics while tolerating future compatible extras."""

    schema_version: Literal[1]
    packet_id: str
    method: Literal["qualitative_coding"]
    prose_status: Literal["synthetic_non_authoritative_human_review_required"]
    claims: list[QCClaim]
    patterns: list[QCPattern]
    claim_limits: list[str]


class CompatiblePTView(CompatibleModel):
    """Consume supported PT semantics without importing producer internals."""

    schema_version: Literal[1]
    packet_id: str
    method: Literal["process_tracing"]
    prose_status: Literal["synthetic_non_authoritative_human_review_required"]
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
    prose_status: Literal["synthetic_non_authoritative_human_review_required"]
    categories: list[GTCategory]
    memos: list[GTMemo]
    next_sampling_suggestions: list[str]
    methodological_limits: list[str]
    claim_limits: list[str]


class ObjectRef(StrictModel):
    """Identify one native method object without copying or rewriting it."""

    method: Literal["qualitative_coding", "process_tracing", "grounded_theory_inspired"]
    object_kind: Literal[
        "qc_claim",
        "qc_pattern",
        "pt_hypothesis",
        "pt_evidence",
        "gt_category",
        "gt_memo",
    ]
    object_id: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_method_kind_pair(self) -> ObjectRef:
        """Prevent a native ID from being interpreted as the wrong object kind."""
        allowed = {
            "qualitative_coding": {"qc_claim", "qc_pattern"},
            "process_tracing": {"pt_hypothesis", "pt_evidence"},
            "grounded_theory_inspired": {"gt_category", "gt_memo"},
        }
        if self.object_kind not in allowed[self.method]:
            raise ValueError("native object_kind is incompatible with its method")
        return self


class CrossMethodLink(StrictModel):
    """Relate native objects neutrally without asserting evidentiary support."""

    link_id: str = Field(min_length=1)
    source: ObjectRef
    relationship: Literal["addresses", "challenges", "contextualizes", "unresolved"]
    target: ObjectRef
    reviewer_meaning: str = Field(min_length=1)
    reviewer_meaning_status: Literal["synthetic_non_authoritative_human_review_required"]

    @model_validator(mode="after")
    def validate_cross_method_boundary(self) -> CrossMethodLink:
        """Require genuinely cross-method endpoints; prose remains non-authoritative."""
        if self.source.method == self.target.method:
            raise ValueError("cross-method link endpoints must use different methods")
        return self


class CoreDemoReviewPacket(StrictModel):
    """Provide a three-lane review view with exact step-down and no scalar synthesis."""

    schema_version: Literal[1]
    artifact_status: Literal["synthetic_demo_fixture"]
    packet: ControlledDemoPacket
    qc: CompatibleQCView
    pt: CompatiblePTView
    gt_inspired: CompatibleGTInspiredView
    links: list[CrossMethodLink] = Field(min_length=1)
    prose_status: Literal["synthetic_non_authoritative_human_review_required"]
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
        _require_exact_strings(self.claim_limits, DEMO_LIMITS, "review packet claim_limits")
        _require_exact_strings(
            self.packet.claim_limits,
            DEMO_LIMITS,
            "review source packet claim_limits",
        )
        _require_exact_strings(self.qc.claim_limits, QC_LIMITS, "review QC claim_limits")
        _require_exact_strings(self.pt.claim_limits, PT_LIMITS, "review PT claim_limits")
        _require_exact_strings(
            self.gt_inspired.claim_limits,
            GT_LIMITS,
            "review GT-inspired claim_limits",
        )
        return self
