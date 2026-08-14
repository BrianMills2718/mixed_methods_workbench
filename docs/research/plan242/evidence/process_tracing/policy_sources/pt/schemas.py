"""Data contracts for all pipeline passes."""

from __future__ import annotations

import hashlib
import math
import re
from typing import Annotated, ClassVar, Literal, Optional, cast
from pydantic import BaseModel, ConfigDict, Field, model_validator

from pt.source_packet import SourceCoverageReport, SourcePacketSummary

DiagnosticType = Literal["hoop", "smoking_gun", "doubly_decisive", "straw_in_the_wind"]
EvidenceType = Literal["empirical", "interpretive"]
Severity = Literal["damaging", "notable", "minor"]
RefinementType = Literal["sharpen_mechanism", "add_prediction", "reframe", "merge_suggestion"]
ContrastDimension = Literal[
    "timing",
    "sequence",
    "necessity",
    "sufficiency",
    "control",
    "mechanism",
    "actor_substitutability",
    "outcome",
    "other",
]
PredictionAssessment = Literal["observed", "contradicted"]
PredictionDirectness = Literal["direct", "indirect"]
VerdictStatus = Literal[
    "strongly_supported", "supported", "weakened", "eliminated", "indeterminate"
]
RankStability = Literal["stable", "unstable", "not_assessed"]
PartitionQuality = Literal["adequate", "needs_review"]
RefinementStatus = Literal["not_requested", "no_changes", "applied"]
InferenceMode = Literal[
    "theory_first",
    "discovery_evaluation_split",
    "exploratory_full_corpus",
]
TheoryEvidenceRelationship = Literal[
    "independent",
    "same_case_reuse",
    "unknown",
]
InferenceStatus = Literal[
    "confirmatory_eligible_theory_first",
    "confirmatory_eligible_discovery_evaluation_split",
    "exploratory_post_selection",
    "legacy_unclassified",
]
InferenceReadoutKind = Literal[
    "confirmatory_comparative_support",
    "exploratory_appraisal",
    "unclassified_unavailable",
]
LikelihoodPolicyId = Literal[
    "uncapped_continuous_relevance",
    "legacy_general_20_1",
    "legacy_type_specific_5_1_20_1",
    "legacy_floor_0_4_and_type_caps",
]
LikelihoodPolicyClass = Literal["headline_estimand", "legacy_sensitivity"]
RelevanceTreatment = Literal["continuous_log_discount", "hard_floor_then_log_discount"]
SourceGenre = Literal[
    "overview",              # secondary overview / encyclopedia / textbook
    "primary_document",      # primary historical document (letter, treaty, edict)
    "speech",                # speech or oral statement
    "legal_constitutional",  # law, constitution, decree, procedural rules, office design
    "memoir",                # memoir, diary, personal account
    "parliamentary_record",  # parliamentary or assembly debate record
    "secondary_analysis",    # academic analysis or scholarly interpretation
    "news_dispatch",         # contemporary newspaper or dispatch
    "other",
]
DateConfidence = Literal["high", "medium", "low"]
TraceProductionRelevance = Literal[
    "direct",    # evidence IS a causal trace (the mechanism acting)
    "indirect",  # evidence points to a trace (circumstantial)
    "background",  # contextual; not a direct causal trace
]
DiscriminatorStrength = Literal["decisive", "strong", "limited"]
# decisive: |log(LR_h1/LR_h2)| >= log(5) ≈ 1.61
# strong:   |log(LR_h1/LR_h2)| >= log(2) ≈ 0.69
LineageType = Literal[
    "duplicate",       # verbatim or near-verbatim copy of the same passage
    "shared_source",   # different quotes from the same document or section
    "same_event",      # different descriptions of the same historical event
    "same_mechanism",  # different expressions of the same causal process
    "other",
]


class InferenceReadoutPolicy(BaseModel):
    """Public claim ceiling derived from the recorded inference status.

    Internal Bayesian artifacts remain available for audit even when this policy
    forbids publishing normalized support or hypothesis verdicts.
    """

    model_config = ConfigDict(extra="forbid")

    kind: InferenceReadoutKind
    label: str
    normalized_comparative_support_available: bool
    hypothesis_verdicts_available: bool
    explanation: str
    next_step: str

    @model_validator(mode="after")
    def _availability_is_coherent(self) -> "InferenceReadoutPolicy":
        if (
            self.normalized_comparative_support_available
            != self.hypothesis_verdicts_available
        ):
            raise ValueError(
                "comparative support and posterior-calibrated verdict availability "
                "must move together"
            )
        if self.kind == "confirmatory_comparative_support":
            if not self.normalized_comparative_support_available:
                raise ValueError("confirmatory readout must expose comparative support")
        elif self.normalized_comparative_support_available:
            raise ValueError("non-confirmatory readout cannot expose comparative support")
        return self


class LikelihoodPolicySpec(BaseModel):
    """Named deterministic policy applied after raw likelihood elicitation."""

    model_config = ConfigDict(extra="forbid")

    policy_id: LikelihoodPolicyId
    label: str
    policy_class: LikelihoodPolicyClass
    relevance_treatment: RelevanceTreatment = "continuous_log_discount"
    relevance_floor: float = Field(default=0.0, ge=0.0, le=1.0)
    general_pairwise_cap: Optional[float] = Field(default=None, gt=1.0)
    interpretive_pairwise_cap: Optional[float] = Field(default=None, gt=1.0)
    binding_headline: bool
    rationale: str


class EvidenceLikelihoodPolicyLineage(BaseModel):
    """Reconstructable raw-to-effective likelihood transformation for one item."""

    evidence_id: str
    raw_relative_likelihoods: dict[str, float]
    centered_raw_likelihood_ratios: dict[str, float]
    relevance: float = Field(ge=0.0, le=1.0)
    effective_likelihood_ratios: dict[str, float]
    applied_pairwise_cap: Optional[float] = Field(default=None, gt=1.0)
    transformations: list[str]


class LikelihoodPolicyScenarioResult(BaseModel):
    """Conclusion-level result under one named non-headline policy scenario."""

    policy_id: LikelihoodPolicyId
    label: str
    ranking: list[str]
    comparative_support: dict[str, float]
    top_hypothesis_id: Optional[str] = None
    rank_changed_from_primary: bool
    max_absolute_support_shift: float = Field(ge=0.0, le=1.0)
    narrative_reassessment_required: bool = Field(
        description=(
            "True when any support value or rank changes, so persisted verdict or "
            "strength prose cannot be carried forward without fresh review."
        )
    )


class LikelihoodPolicySensitivity(BaseModel):
    """Whether named legacy policies materially alter the primary conclusion."""

    primary_policy_id: LikelihoodPolicyId
    scenarios: list[LikelihoodPolicyScenarioResult]
    any_rank_change: bool
    max_absolute_support_shift: float = Field(ge=0.0, le=1.0)
SourceSpanAttribution = Literal[
    "explicit_marker",
    "carried_marker_context",
    "unassigned",
    "unpacketized",
]
EvidenceExclusionReason = Literal[
    "hypothesis_generation",
    "prior_input",
    "post_selection_refinement",
    "same_case_theory_reuse",
]
PriorMethod = Literal["uniform", "researcher"]
DiscriminatorFailureClass = Literal[
    "shared_prediction",
    "compatible_with_both",
    "indirect_only",
    "counterfactual_not_identified",
    "wrong_causal_stage",
    "temporal_mismatch",
    "source_quote_mismatch",
    "trace_production_confound",
    "other",
]
DiscriminatorAuditBasis = Literal[
    "predeclared_prediction",
    "distinct_same_case_observation",
    "inductively_discovered_clue",
    "trace_production_expectation",
    "shared_compatibility",
    "unsupported_assertion",
]
DependenceLevel = Literal["claim", "event", "source", "author"]
MechanismStageType = Literal[
    "precondition",
    "initiation",
    "escalation",
    "decision",
    "implementation",
    "consolidation",
    "outcome",
]
MechanismStageStatus = Literal["observed", "partially_observed", "unresolved"]
MechanismEdgeStatus = Literal[
    "observed_sequence",
    "supported_causal_link",
    "contested_causal_link",
    "unresolved_link",
]
MechanismStageAuditDisposition = Literal["accepted", "material_revision_required"]
MechanismEdgeAuditDisposition = Literal["accepted", "weaken"]
MechanismRepairConstraintDisposition = Literal["satisfied", "unsatisfied"]
MechanismEvidenceAssessment = Literal[
    "direct_transition",
    "contested_transition",
    "temporal_order_only",
    "endpoint_only",
    "contradictory",
    "absent",
]
MechanismOmissionSeverity = Literal["advisory", "material"]
MechanismOmissionTarget = Literal["stage", "transition"]
MechanismOmissionGrounding = Literal[
    "directly_observed",
    "endpoint_only",
    "prediction_only",
]


# ── Pass 1: Extraction ──────────────────────────────────────────────

class Actor(BaseModel):
    id: str = Field(description="Unique identifier, e.g. 'actor_louis_xvi'")
    name: str
    description: str


class Event(BaseModel):
    id: str = Field(description="Unique identifier, e.g. 'evt_storming_bastille'")
    description: str
    date: Optional[str] = Field(
        default=None,
        description="Date or period in the source's own terms.",
    )
    normalized_year: Optional[int] = Field(
        default=None,
        description=(
            "Gregorian/CE year used only for deterministic temporal ordering. Convert "
            "non-Gregorian source dates when the correspondence is safely inferable; "
            "use negative integers for BCE years and null when unresolved."
        ),
    )
    location: Optional[str] = None


class Mechanism(BaseModel):
    id: str = Field(description="Unique identifier, e.g. 'mech_fiscal_crisis'")
    description: str


class Evidence(BaseModel):
    id: str = Field(description="Unique identifier, e.g. 'evi_tax_records'")
    description: str
    source_text: str = Field(
        description=(
            "Direct quote from the input text; preserve source markers, document labels, "
            "speaker labels, and citation labels when they appear in the quoted span"
        )
    )
    source_id: Optional[str] = Field(
        default=None,
        description=(
            "Stable identifier for the source document containing this exact quote. "
            "Assigned from source-packet custody or a validated segmented-source "
            "document; null is retained only for legacy or anonymous plain-text inputs."
        ),
    )
    source_span_id: Optional[str] = Field(
        default=None,
        description=(
            "System-assigned immutable source-span identifier used to materialize "
            "source_text in fresh extraction runs."
        ),
    )
    source_quote: Optional[str] = Field(
        default=None,
        description=(
            "Exact distinctive quote used to resolve source_span_id and anchor the "
            "evidence description. Required for fresh producer results."
        ),
    )
    evidence_type: EvidenceType = Field(
        default="empirical",
        description="'empirical' for facts/events/actions, 'interpretive' for historian arguments/scholarly claims"
    )
    approximate_date: Optional[str] = Field(
        default=None,
        description=(
            "Approximate date in the source's own terms, preserving labels such as "
            "'19 Brumaire, Year VIII' rather than silently rewriting them."
        ),
    )
    normalized_year: Optional[int] = Field(
        default=None,
        description=(
            "Gregorian/CE year used only for deterministic temporal comparison. Convert "
            "non-Gregorian source dates when the correspondence is safely inferable; "
            "use negative integers for BCE years and null when unresolved."
        ),
    )
    date_confidence: Optional[DateConfidence] = Field(
        default=None,
        description=(
            "'high' = explicit date in the text; 'medium' = approximate or inferred from context; "
            "'low' = only a rough period or no date at all"
        ),
    )
    source_group: Optional[str] = Field(
        default=None,
        description=(
            "Short label for the source section or document within the input text where this "
            "evidence appears, e.g. 'Background section', 'Primary source A', 'Witness testimony'. "
            "Use the same label for all evidence drawn from the same source block so that "
            "cross-source comparison is possible."
        ),
    )
    source_genre: Optional[SourceGenre] = Field(
        default=None,
        description=(
            "Genre of the source this evidence comes from. "
            "Use 'overview' for secondary/encyclopedia/textbook summaries, "
            "'primary_document' for original historical documents, "
            "'speech' for speeches or oral statements, "
            "'legal_constitutional' for laws, constitutions, decrees, "
            "'memoir' for diaries or personal accounts, "
            "'parliamentary_record' for assembly/parliamentary debates, "
            "'secondary_analysis' for academic interpretations, "
            "'news_dispatch' for contemporary press, 'other' otherwise."
        ),
    )
    trace_production_relevance: Optional[TraceProductionRelevance] = Field(
        default=None,
        description=(
            "'direct' = this evidence IS a causal trace (the mechanism visibly acting); "
            "'indirect' = this evidence points to a trace but is circumstantial; "
            "'background' = contextual, not a direct causal trace."
        ),
    )


class CausalEdge(BaseModel):
    source_id: str
    target_id: str
    relationship: str = Field(description="Nature of the causal link")
    support_evidence_ids: list[str] = Field(
        default_factory=list,
        description=(
            "Source-grounded evidence IDs supporting this process relationship. "
            "Fresh extraction edges require at least one ID; legacy and directly "
            "span-grounded refinement edges may leave this empty."
        ),
    )
    source_text_support: Optional[str] = Field(
        default=None,
        description="Exact immutable source span supporting a refinement-added edge.",
    )
    support_source_id: Optional[str] = Field(
        default=None,
        description="Stable packet source ID for source_text_support.",
    )
    support_source_span_id: Optional[str] = Field(
        default=None,
        description="System-assigned source-span ID for source_text_support.",
    )
    support_quote: Optional[str] = Field(
        default=None,
        description="Exact quote anchoring a directly span-grounded causal edge.",
    )


class TextHypothesis(BaseModel):
    id: str
    description: str
    source_text: str = Field(description="Quote from text where this hypothesis appears or is implied")
    source_id: Optional[str] = Field(
        default=None,
        description="Stable source-packet identifier for the quoted causal claim.",
    )
    source_span_id: Optional[str] = Field(
        default=None,
        description="System-assigned immutable source-span identifier for source_text.",
    )
    source_quote: Optional[str] = Field(
        default=None,
        description="Exact quote anchoring this corpus-derived causal claim.",
    )


class SourceSpan(BaseModel):
    """System-generated immutable passage used by grounded producer contracts."""

    id: str = Field(description="System-assigned source-span identifier.")
    source_text: str = Field(description="Exact contiguous passage from the input corpus.")
    source_text_sha256: str = Field(
        description="SHA-256 digest of the UTF-8 encoded source_text."
    )
    allowed_source_ids: list[str] = Field(
        default_factory=list,
        description="Packet source IDs permitted by deterministic marker context.",
    )
    attribution: SourceSpanAttribution = Field(
        description="How packet source attribution was determined for this span."
    )

    @model_validator(mode="after")
    def _valid_digest(self) -> "SourceSpan":
        expected = hashlib.sha256(self.source_text.encode("utf-8")).hexdigest()
        if self.source_text_sha256 != expected:
            raise ValueError(
                f"source span {self.id} digest does not match its source_text"
            )
        return self


class SegmentedSourceSummary(BaseModel):
    """Lineage for an upstream segmented-source handoff used by Pass 1."""

    model_config = ConfigDict(extra="forbid")

    producer_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    source_document_id: str = Field(pattern=r"^srcdoc1_[0-9a-f]{24}$")
    source_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    segmentation_plan_id: str = Field(pattern=r"^segplan1_[0-9a-f]{24}$")
    segmentation_plan_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    atom_count: int = Field(ge=1)
    work_unit_count: int = Field(ge=1)
    maximum_work_unit_characters: int = Field(ge=1)


def _require_unique_ids(ids: list[str], label: str) -> None:
    seen: set[str] = set()
    dups: set[str] = set()
    for i in ids:
        if i in seen:
            dups.add(i)
        seen.add(i)
    if dups:
        raise ValueError(f"duplicate {label} ids: {sorted(dups)}")


class SourceAnchorExclusion(BaseModel):
    """One model suggestion withheld because exact source grounding failed."""

    model_config = ConfigDict(extra="forbid")

    item_key: str = Field(
        description="Typed extraction item key, such as evidence:evi_example."
    )
    item_label: str
    claim: str
    rejected_quote: str
    matching_source_span_ids: list[str] = Field(default_factory=list)
    reason: Literal["repair_failed_unique_anchor"] = "repair_failed_unique_anchor"


class ExtractionResult(BaseModel):
    summary: str = Field(description="2-3 sentence summary of the text")
    actors: list[Actor] = []
    events: list[Event] = []
    mechanisms: list[Mechanism] = []
    evidence: list[Evidence] = []
    hypotheses_in_text: list[TextHypothesis] = []
    causal_edges: list[CausalEdge] = []
    source_spans: list[SourceSpan] = Field(
        default_factory=list,
        description=(
            "System-generated source-span catalog for fresh runs; empty only for "
            "legacy artifacts."
        ),
    )
    source_anchor_exclusions: list[SourceAnchorExclusion] = Field(
        default_factory=list,
        description=(
            "Extraction suggestions excluded after one typed repair attempt because "
            "no exact quote identified one admissible immutable source span."
        ),
    )

    @model_validator(mode="after")
    def _unique_extraction_ids(self) -> "ExtractionResult":
        _require_unique_ids([e.id for e in self.evidence], "evidence")
        _require_unique_ids([a.id for a in self.actors], "actor")
        _require_unique_ids([e.id for e in self.events], "event")
        _require_unique_ids([m.id for m in self.mechanisms], "mechanism")
        _require_unique_ids([h.id for h in self.hypotheses_in_text], "text hypothesis")
        _require_unique_ids([span.id for span in self.source_spans], "source span")
        _require_unique_ids(
            [
                item.item_key
                for item in getattr(self, "source_anchor_exclusions", [])
            ],
            "source anchor exclusion",
        )
        if self.source_spans:
            span_by_id = {span.id: span for span in self.source_spans}
            grounded_items: list[Evidence | TextHypothesis] = [
                *self.evidence,
                *self.hypotheses_in_text,
            ]
            missing_span_ids = sorted(
                item.id for item in grounded_items if not item.source_span_id
            )
            if missing_span_ids:
                raise ValueError(
                    "fresh extraction items lack source_span_id: "
                    f"{missing_span_ids}"
                )
            unknown_span_ids = {
                item.id: item.source_span_id
                for item in grounded_items
                if item.source_span_id not in span_by_id
            }
            if unknown_span_ids:
                raise ValueError(
                    "extraction items reference unknown source spans: "
                    f"{unknown_span_ids}"
                )
            mismatched_text = sorted(
                item.id
                for item in grounded_items
                if item.source_span_id in span_by_id
                and item.source_text != span_by_id[item.source_span_id].source_text
            )
            if mismatched_text:
                raise ValueError(
                    "extraction item text does not match selected source span: "
                    f"{mismatched_text}"
                )
            invalid_packet_sources = {
                item.id: {
                    "span": item.source_span_id,
                    "source_id": item.source_id,
                    "allowed": span_by_id[item.source_span_id].allowed_source_ids,
                }
                for item in grounded_items
                if item.source_span_id in span_by_id
                and span_by_id[item.source_span_id].attribution != "unpacketized"
                and item.source_id
                not in span_by_id[item.source_span_id].allowed_source_ids
            }
            if invalid_packet_sources:
                raise ValueError(
                    "extraction item source IDs conflict with source-span attribution: "
                    f"{invalid_packet_sources}"
                )

        typed_ids = {
            "actor": {actor.id for actor in self.actors},
            "event": {event.id for event in self.events},
            "mechanism": {mechanism.id for mechanism in self.mechanisms},
            "evidence": {evidence.id for evidence in self.evidence},
            "text hypothesis": {hypothesis.id for hypothesis in self.hypotheses_in_text},
        }
        id_owners: dict[str, list[str]] = {}
        for kind, ids in typed_ids.items():
            for node_id in ids:
                id_owners.setdefault(node_id, []).append(kind)
        cross_type_duplicates = {
            node_id: owners for node_id, owners in id_owners.items() if len(owners) > 1
        }
        if cross_type_duplicates:
            raise ValueError(
                f"extraction node ids collide across types: {cross_type_duplicates}"
            )

        known_ids = set(id_owners)
        dangling_edges = [
            f"{edge.source_id}->{edge.target_id}"
            for edge in self.causal_edges
            if edge.source_id not in known_ids or edge.target_id not in known_ids
        ]
        if dangling_edges:
            raise ValueError(
                "causal edges reference nodes absent from the extraction: "
                f"{sorted(dangling_edges)}"
            )
        return self


# ── Pass 2: Hypothesis Space ────────────────────────────────────────

class Prediction(BaseModel):
    id: str = Field(description="Unique identifier, e.g. 'pred_fiscal_01'")
    description: str = Field(description="What we would expect to observe if the hypothesis is true")


class Hypothesis(BaseModel):
    id: str = Field(description="Unique identifier, e.g. 'h1'")
    description: str
    source: Literal["text", "generated"] = Field(
        description="'text' if formulated from corpus evidence, 'generated' if a rival"
    )
    generation_evidence_ids: list[str] = Field(
        default_factory=list,
        description=(
            "System-recorded extracted evidence ids visible while this hypothesis was "
            "formulated. All visible items remain auditable but are excluded from "
            "likelihood updating; the model cannot narrow this exposure record."
        ),
    )
    generation_rationale: str = Field(
        description=(
            "Why this hypothesis entered the rival set and, for generated rivals, "
            "the theory or contrast that generated it."
        )
    )
    theoretical_basis: str = Field(description="Why this hypothesis is plausible")
    causal_mechanism: str = Field(description="The proposed causal chain")
    observable_predictions: list[Prediction] = Field(
        description="What evidence we would expect to find if this hypothesis is true"
    )


class HypothesisSpace(BaseModel):
    research_question: str
    hypotheses: list[Hypothesis]

    @model_validator(mode="after")
    def _unique_hypothesis_ids(self) -> "HypothesisSpace":
        _require_unique_ids([h.id for h in self.hypotheses], "hypothesis")
        _require_unique_ids(
            [
                prediction.id
                for hypothesis in self.hypotheses
                for prediction in hypothesis.observable_predictions
            ],
            "observable prediction",
        )
        return self


class InferenceDesign(BaseModel):
    """Pre-analysis contract governing corpus exposure and update eligibility."""

    model_config = ConfigDict(extra="forbid")

    mode: InferenceMode = Field(
        default="exploratory_full_corpus",
        description="Declared corpus-exposure design for hypothesis formulation.",
    )
    discovery_source_ids: list[str] = Field(
        default_factory=list,
        description="Packet source IDs exposed during split-design hypothesis discovery.",
    )
    evaluation_source_ids: list[str] = Field(
        default_factory=list,
        description="Packet source IDs withheld from formulation and reserved for evaluation.",
    )
    theory_material_sha256: str | None = Field(
        default=None,
        pattern=r"^[0-9a-f]{64}$",
        description=(
            "System-bound SHA-256 of theory/design material supplied to formulation; "
            "null when no theory material was supplied."
        ),
    )
    theory_evidence_relationship: TheoryEvidenceRelationship = Field(
        default="independent",
        description=(
            "Whether supplied theory was developed independently of the evidence "
            "used in this run. same_case_reuse and unknown block independent "
            "confirmation and comparative updating."
        ),
    )
    rationale: str = Field(
        default="No pre-analysis separation was supplied; treat the run as exploratory.",
        description="Researcher-facing rationale for the selected exposure design.",
    )

    @model_validator(mode="after")
    def _validate_declared_roles(self) -> "InferenceDesign":
        _require_unique_ids(self.discovery_source_ids, "discovery source")
        _require_unique_ids(self.evaluation_source_ids, "evaluation source")
        overlap = set(self.discovery_source_ids) & set(self.evaluation_source_ids)
        if overlap:
            raise ValueError(
                "discovery and evaluation source roles must be disjoint: "
                f"{sorted(overlap)}"
            )
        if self.mode == "discovery_evaluation_split":
            if not self.discovery_source_ids or not self.evaluation_source_ids:
                raise ValueError(
                    "discovery_evaluation_split requires non-empty discovery and "
                    "evaluation source ids"
                )
        elif self.discovery_source_ids or self.evaluation_source_ids:
            raise ValueError(
                f"{self.mode} does not accept discovery or evaluation source ids"
            )
        if not self.rationale.strip():
            raise ValueError("inference design rationale must not be blank")
        return self


class HypothesisGenerationView(BaseModel):
    """Exact extracted evidence serialized into hypothesis generation and repair."""

    model_config = ConfigDict(extra="forbid")

    mode: InferenceMode
    extraction_evidence_ids: list[str] | None = Field(
        default=None,
        description=(
            "Immutable IDs of every extracted evidence item available when the "
            "hypothesis-generation view was built. Null marks legacy lineage."
        ),
    )
    extraction_source_assignments: dict[str, str | None] | None = Field(
        default=None,
        description=(
            "Immutable evidence-to-source assignments at hypothesis-generation time. "
            "Null marks legacy lineage."
        ),
    )
    visible_source_ids: list[str] = Field(default_factory=list)
    visible_evidence_ids: list[str] = Field(default_factory=list)
    visible_evidence: list[Evidence] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_view(self) -> "HypothesisGenerationView":
        _require_unique_ids(self.visible_source_ids, "visible source")
        _require_unique_ids(self.visible_evidence_ids, "visible generation evidence")
        if (self.extraction_evidence_ids is None) != (
            self.extraction_source_assignments is None
        ):
            raise ValueError(
                "generation-time evidence ids and source assignments must both be "
                "present or both be null"
            )
        if self.extraction_evidence_ids is not None:
            _require_unique_ids(
                self.extraction_evidence_ids,
                "generation-time extraction evidence",
            )
            if set(self.extraction_source_assignments or {}) != set(
                self.extraction_evidence_ids
            ):
                raise ValueError(
                    "generation-time source assignments must cover every extraction "
                    "evidence id exactly"
                )
        materialized_ids = [item.id for item in self.visible_evidence]
        if self.visible_evidence_ids != materialized_ids:
            raise ValueError(
                "visible_evidence_ids must exactly match visible_evidence order"
            )
        if self.mode == "theory_first" and self.visible_evidence:
            raise ValueError("theory_first hypothesis generation cannot expose evidence")
        return self


class PriorSpecification(BaseModel):
    """Declared prior inputs, separate from evidence used for likelihood updates."""

    method: PriorMethod
    weights: dict[str, float] = Field(
        description="Positive prior weight for every declared hypothesis; normalization is automatic."
    )
    rationale: str = Field(description="Why this prior method and these relative weights were chosen.")
    evidence_ids: list[str] = Field(
        default_factory=list,
        description=(
            "Extracted corpus evidence used to inform a researcher prior. These items are "
            "excluded from likelihood updating to prevent double use."
        ),
    )
    external_source_refs: list[str] = Field(
        default_factory=list,
        description="External base-rate or theoretical sources used to inform the prior.",
    )

    @model_validator(mode="after")
    def _valid_weights_and_provenance(self) -> "PriorSpecification":
        if not self.weights:
            raise ValueError("prior specification must contain at least one hypothesis weight")
        invalid = {
            hyp_id: weight
            for hyp_id, weight in self.weights.items()
            if not math.isfinite(weight) or weight <= 0
        }
        if invalid:
            raise ValueError(f"prior weights must be finite and positive: {invalid}")
        if not self.rationale.strip():
            raise ValueError("prior rationale must not be blank")
        _require_unique_ids(self.evidence_ids, "prior evidence")
        _require_unique_ids(self.external_source_refs, "prior external source")
        if self.method == "uniform":
            if len(set(self.weights.values())) != 1:
                raise ValueError("uniform prior must assign equal weights")
            if self.evidence_ids or self.external_source_refs:
                raise ValueError("uniform prior cannot declare evidentiary inputs")
        return self

    def validate_for(
        self,
        hypothesis_ids: list[str],
        evidence_ids: list[str],
    ) -> "PriorSpecification":
        expected_hypotheses = set(hypothesis_ids)
        actual_hypotheses = set(self.weights)
        if actual_hypotheses != expected_hypotheses:
            raise ValueError(
                "prior hypothesis coverage mismatch: "
                f"missing {sorted(expected_hypotheses - actual_hypotheses)}, "
                f"extra {sorted(actual_hypotheses - expected_hypotheses)}"
            )
        unknown_evidence = set(self.evidence_ids) - set(evidence_ids)
        if unknown_evidence:
            raise ValueError(
                f"prior specification references unknown evidence ids: {sorted(unknown_evidence)}"
            )
        return self

    @classmethod
    def uniform(cls, hypothesis_ids: list[str]) -> "PriorSpecification":
        return cls(
            method="uniform",
            weights={hypothesis_id: 1.0 for hypothesis_id in hypothesis_ids},
            rationale="Equal prior weights; no corpus evidence or external source informed the prior.",
        )


# ── Pass 2.5: Partition Audit ────────────────────────────────────────

class PredictionContrast(BaseModel):
    """One concrete opposed prediction pair that makes two hypotheses testable."""

    h1_prediction_id: str = Field(
        description="Prediction owned by RivalPairAudit.h1_id."
    )
    h2_prediction_id: str = Field(
        description="Prediction owned by RivalPairAudit.h2_id."
    )
    contrast_dimension: ContrastDimension = Field(
        description="Causal dimension on which the two predictions conflict."
    )
    reasoning: str = Field(
        min_length=8,
        description="Why observing one prediction makes the other less likely."
    )

class RivalPairAudit(BaseModel):
    h1_id: str = Field(description="First hypothesis id in the rival pair")
    h2_id: str = Field(description="Second hypothesis id in the rival pair")
    overlap_concern: bool = Field(
        description=(
            "True if the decisive claims substantially overlap. This is a hard partition "
            "failure only when the pair has no valid opposed prediction contrast."
        )
    )
    complementary_concern: bool = Field(
        description=(
            "True if the decisive claims may both hold. Coexisting background conditions "
            "alone do not trigger this flag, and a valid opposed prediction makes the "
            "concern advisory rather than a hard partition failure."
        )
    )
    absorptive_concern: bool = Field(
        description=(
            "True if one decisive claim can absorb the other unchanged. Absorbing a rival's "
            "background factor while contradicting its necessity, sufficiency, control, "
            "sequence, or counterfactual claim is not fatal absorption."
        )
    )
    prediction_contrasts: list[PredictionContrast] = Field(
        default_factory=list,
        description=(
            "Concrete opposed prediction pairs. Code validates ownership and derives "
            "discriminator_count from this list."
        ),
    )
    discriminator_count: int = Field(
        default=0,
        ge=0,
        description=(
            "Pipeline-derived count of valid prediction_contrasts. A legacy nonzero "
            "count without concrete contrasts does not pass the partition gate."
        ),
    )
    concern_detail: str = Field(
        description="Brief explanation of the most serious concern for this pair; empty string if no flags are set"
    )


class PartitionAudit(BaseModel):
    research_question_adequate: bool = Field(
        description="True if the research question targets a single outcome with genuinely rival causal explanations; False if compound, tautological, or under-specified"
    )
    rival_pairs: list[RivalPairAudit] = Field(
        description="One entry per unordered (h_i, h_j) pair — every hypothesis paired with every other"
    )
    hypotheses_flagged: list[str] = Field(
        description="Hypothesis IDs flagged as broad, tautological, complementary, or absorptive"
    )
    overall_quality: PartitionQuality = Field(
        description=(
            "Pipeline-derived verdict: 'adequate' when every pair has a valid opposed "
            "prediction and no structural blocker; otherwise 'needs_review'."
        )
    )
    cap_applied: bool = Field(
        default=False,
        description="Set by the pipeline when overall_quality is needs_review; signals that downstream support scores may be inflated by partition problems"
    )
    decision_blockers: list[str] = Field(
        default_factory=list,
        description=(
            "Deterministic reasons this partition cannot enter diagnostic testing. "
            "The pipeline derives this field from pair coverage and the typed audit."
        ),
    )
    decision_warnings: list[str] = Field(
        default_factory=list,
        description=(
            "Pipeline-derived nonfatal risks, including overlap, complementarity, or "
            "absorption concerns for pairs that nevertheless have valid opposed predictions."
        ),
    )
    summary: str = Field(
        description="2-3 sentence adversarial assessment: strongest remaining concern, whether the winning hypothesis could absorb rivals, and whether the focal window is adequate"
    )


class PartitionAttempt(BaseModel):
    attempt: int = Field(ge=1)
    action: str = Field(
        description="The transition that produced this audit, such as initial_audit or automated_repair_1"
    )
    hypothesis_space: Optional[HypothesisSpace] = Field(
        default=None,
        description=(
            "Exact candidate hypothesis space evaluated by this audit. Required for fresh "
            "runs; null is accepted only so legacy artifacts remain parseable."
        ),
    )
    audit: PartitionAudit


class PartitionResolution(BaseModel):
    status: Literal["repairing", "accepted", "blocked"]
    attempts: list[PartitionAttempt] = Field(default_factory=list)
    final_audit: PartitionAudit

    @model_validator(mode="after")
    def _final_audit_matches_history(self) -> "PartitionResolution":
        if self.attempts and self.attempts[-1].audit != self.final_audit:
            raise ValueError("partition final audit must match the last recorded attempt")
        return self


# ── Pass 3: Testing ─────────────────────────────────────────────────

class PredictionClassification(BaseModel):
    prediction_id: str
    hypothesis_id: str
    diagnostic_type: DiagnosticType = Field(
        description="One of: hoop, smoking_gun, doubly_decisive, straw_in_the_wind"
    )
    necessity_reasoning: str = Field(
        description="Why passing this test is or is not necessary for the hypothesis"
    )
    sufficiency_reasoning: str = Field(
        description="Why passing this test is or is not sufficient for the hypothesis"
    )


class HypothesisLikelihood(BaseModel):
    """Relative likelihood of one evidence item under one hypothesis.

    Values are on a common positive scale across all hypotheses for the *same*
    evidence item — only the ratios between hypotheses matter. Equal values across
    hypotheses ⇒ the evidence is uninformative. Eliciting the whole vector at once
    (rather than independent pairwise ratios) is what keeps the likelihoods
    coherent: every pairwise ratio is derived from one vector, so reciprocity and
    transitivity hold by construction.
    """
    hypothesis_id: str
    relative_likelihood: float = Field(
        gt=0.0,
        allow_inf_nan=False,
        description="Relative likelihood P(E|H) of THIS evidence under THIS hypothesis, "
        "on a common positive scale shared by all hypotheses for this evidence item. "
        "Larger = this hypothesis predicts this evidence more strongly. Equal across "
        "hypotheses = uninformative. Must be a finite positive number.",
    )
    diagnostic_type: DiagnosticType = Field(
        description="Van Evera label for how this evidence bears on this hypothesis: "
        "'hoop', 'smoking_gun', 'doubly_decisive', or 'straw_in_the_wind'.",
    )


class EvidencePredictionLink(BaseModel):
    """Typed lineage from one source-grounded item to an observable prediction."""

    hypothesis_id: str
    prediction_id: str
    assessment: PredictionAssessment = Field(
        description="Whether this evidence directly observes or contradicts the prediction."
    )
    directness: PredictionDirectness = Field(
        description=(
            "Whether the passage itself bears on the prediction. Direct links provide "
            "stronger provenance, but semantic audit—not this field—decides discrimination."
        )
    )
    reasoning: str = Field(
        min_length=8,
        description="Why this source-grounded item bears on the named prediction."
    )


class EvidenceLikelihood(BaseModel):
    """One evidence item's likelihood vector across all competing hypotheses."""
    evidence_id: str
    hypothesis_likelihoods: list[HypothesisLikelihood] = Field(
        description="Exactly one entry per hypothesis — the relative likelihood of this "
        "evidence under each, on a shared scale.",
    )
    relevance: float = Field(
        default=1.0, ge=0.0, le=1.0,
        description="How relevant/discriminating this evidence is (temporal proximity, "
        "causal domain, specificity). 0.0=irrelevant and therefore neutral; values "
        "above zero continuously discount the centered log-likelihood contribution.",
    )
    justification: str = Field(
        description="Why these relative likelihoods — covering both the causal story and how "
        "the evidence was produced (solicited/recorded/survived).",
    )
    prediction_links: list[EvidencePredictionLink] = Field(
        default_factory=list,
        description=(
            "Exact observable predictions this item observes or contradicts. These links "
            "provide provenance but do not serve as a universal eligibility gate."
        ),
    )


class EvidenceCluster(BaseModel):
    """A group of evidence items that are NOT conditionally independent.

    Items sharing the same source/document lineage, the same originating event, or
    the same underlying fact carry overlapping information; multiplying their
    likelihoods would double-count. The Bayesian update collapses each cluster to a
    single effective observation (log-average of member vectors).
    """
    evidence_ids: list[str] = Field(
        description="Two or more evidence ids that share a source, event, mechanism, or "
        "underlying sub-narrative and therefore carry overlapping (non-independent) information."
    )
    reason: str = Field(description="Why these items are dependent (shared source/event/mechanism).")
    lineage_type: Optional[LineageType] = Field(
        default=None,
        description=(
            "Structured classification of the dependence cause. "
            "'duplicate' = verbatim or near-verbatim copy; "
            "'shared_source' = different quotes from the same document/section; "
            "'same_event' = different descriptions of the same historical event; "
            "'same_mechanism' = different expressions of the same causal process; "
            "'other' = none of the above. "
            "Set this so the audit can verify that each cluster has a visible lineage explanation."
        ),
    )
    dependence_strength: float = Field(
        default=1.0, ge=0.0, le=1.0, allow_inf_nan=False,
        description="How redundant the members are (0=independent, 1=fully redundant). "
        "1.0 for duplicates/same-source copies; ~0.5–0.8 for items about the same event or "
        "mechanism that still add some independent signal. Sets the cluster's effective "
        "observation count k_eff = k / (1 + (k-1)*dependence_strength).",
    )


class TraceDependenceGroup(BaseModel):
    """One dependence factor in an ordered trace-production hierarchy."""

    group_id: str = Field(
        pattern=r"^[A-Za-z0-9_-]+$",
        description="Stable identifier unique within this dependence model.",
    )
    level: DependenceLevel
    evidence_ids: list[str] = Field(
        min_length=2,
        description="Distinct evidence IDs sharing this production lineage.",
    )
    reason: str = Field(
        min_length=8,
        description="Why these items are dependent at the declared level.",
    )
    dependence_strength: float = Field(
        ge=0.0,
        le=1.0,
        allow_inf_nan=False,
        description=(
            "Exchangeable correlation used at this level. Zero preserves the "
            "child effective count; one collapses the group to one observation."
        ),
    )

    @model_validator(mode="after")
    def _distinct_members(self) -> "TraceDependenceGroup":
        if len(self.evidence_ids) != len(set(self.evidence_ids)):
            raise ValueError(
                f"dependence group {self.group_id} contains duplicate evidence IDs"
            )
        return self


class TraceDependenceModel(BaseModel):
    """Nested claim -> event -> source -> author dependence factors."""

    groups: list[TraceDependenceGroup] = Field(default_factory=list)
    level_order: list[DependenceLevel] = Field(
        default_factory=lambda: cast(
            list[DependenceLevel], ["claim", "event", "source", "author"]
        )
    )

    @model_validator(mode="after")
    def _validate_hierarchy(self) -> "TraceDependenceModel":
        expected_order: list[DependenceLevel] = [
            "claim",
            "event",
            "source",
            "author",
        ]
        if self.level_order != expected_order:
            raise ValueError(
                "dependence level order must be claim, event, source, author"
            )
        group_ids = [group.group_id for group in self.groups]
        if len(group_ids) != len(set(group_ids)):
            raise ValueError("dependence group IDs must be unique")

        order = {level: index for index, level in enumerate(expected_order)}
        for index, left in enumerate(self.groups):
            left_ids = set(left.evidence_ids)
            for right in self.groups[index + 1 :]:
                right_ids = set(right.evidence_ids)
                overlap = left_ids & right_ids
                if not overlap:
                    continue
                if left.level == right.level:
                    raise ValueError(
                        "evidence cannot overlap within the same dependence level: "
                        f"{left.group_id}, {right.group_id}"
                    )
                narrower, broader = (
                    (left, right)
                    if order[left.level] < order[right.level]
                    else (right, left)
                )
                if not set(narrower.evidence_ids).issubset(
                    set(broader.evidence_ids)
                ):
                    raise ValueError(
                        "partial cross-level overlap is not a valid dependence "
                        f"hierarchy: {narrower.group_id}, {broader.group_id}"
                    )
        return self


class EvidenceExclusion(BaseModel):
    """Visible evidence deliberately neutralized to prevent inferential double use."""

    evidence_id: str
    reasons: list[EvidenceExclusionReason]
    related_hypothesis_ids: list[str] = Field(default_factory=list)
    explanation: str


class AcceptedSemanticComparison(BaseModel):
    """One independently accepted evidence-by-rival differential."""

    evidence_id: str
    h1_id: str
    h2_id: str
    basis: DiscriminatorAuditBasis


class TestingResult(BaseModel):
    __test__: ClassVar[bool] = False

    evidence_likelihoods: list[EvidenceLikelihood] = Field(
        description="Per-evidence likelihood vectors across all hypotheses.",
    )
    dependence_clusters: list[EvidenceCluster] = Field(
        default_factory=list,
        description="Groups of conditionally-dependent evidence items. Each cluster is "
        "collapsed to one effective observation in the update to avoid double-counting. "
        "Items not in any cluster are treated as independent.",
    )
    dependence_model: Optional[TraceDependenceModel] = Field(
        default=None,
        description=(
            "Ordered claim/event/source/author dependence model for fresh runs. "
            "Legacy artifacts may retain only dependence_clusters."
        ),
    )
    prediction_classifications: list[PredictionClassification] = Field(
        default_factory=list,
        description="Complete Van Evera classification of every hypothesis prediction.",
    )
    evidence_exclusions: list[EvidenceExclusion] = Field(
        default_factory=list,
        description=(
            "Evidence retained for auditability but assigned an equal likelihood vector and "
            "zero relevance because it informed hypothesis generation, the prior, or a "
            "same-corpus post-selection refinement."
        ),
    )
    semantic_audit_complete: bool = Field(
        default=False,
        description=(
            "True when every non-equal raw comparison was independently reviewed and "
            "this artifact contains only the accepted comparison graph."
        ),
    )
    accepted_semantic_comparisons: list[AcceptedSemanticComparison] = Field(
        default_factory=list,
        description="Exact direct comparisons retained by the semantic audit.",
    )


# -- Pass 3a: Independent discriminator audit -----------------------

class DiscriminatorContrastContext(BaseModel):
    """One accepted opposed prediction pair materialized for quote-level review."""

    h1_prediction_id: str
    h1_prediction_description: str
    h2_prediction_id: str
    h2_prediction_description: str
    contrast_dimension: ContrastDimension
    reasoning: str


class DiscriminatorCandidate(BaseModel):
    """One non-equal evidence-by-rival likelihood comparison requiring review."""

    candidate_id: str
    evidence_id: str
    evidence_description: str
    evidence_source_text: str
    source_id: Optional[str] = None
    source_span_id: Optional[str] = None
    approximate_date: Optional[str] = None
    h1_id: str
    h1_description: str
    h1_causal_mechanism: str
    h2_id: str
    h2_description: str
    h2_causal_mechanism: str
    favored_hypothesis_id: str
    h1_relative_likelihood: float = Field(default=1.0, gt=0, allow_inf_nan=False)
    h2_relative_likelihood: float = Field(default=1.0, gt=0, allow_inf_nan=False)
    raw_likelihood_ratio: float = Field(ge=1.0, allow_inf_nan=False)
    aligned_prediction_ids: list[str] = Field(default_factory=list)
    proposed_prediction_links: list[EvidencePredictionLink] = Field(
        default_factory=list
    )
    accepted_prediction_contrasts: list[DiscriminatorContrastContext] = Field(
        default_factory=list
    )
    pass3_justification: str


class AcceptedDiscriminatorJudgment(BaseModel):
    disposition: Literal["accepted"]
    candidate_id: str
    evidence_id: str
    h1_id: str
    h2_id: str
    basis: DiscriminatorAuditBasis = "predeclared_prediction"
    reasoning: str = Field(min_length=8)

    @model_validator(mode="after")
    def _accepted_basis_is_differential(self) -> "AcceptedDiscriminatorJudgment":
        if self.basis in {"shared_compatibility", "unsupported_assertion"}:
            raise ValueError(f"accepted discriminator cannot use basis {self.basis}")
        return self


class RejectedDiscriminatorJudgment(BaseModel):
    disposition: Literal["rejected"]
    candidate_id: str
    evidence_id: str
    h1_id: str
    h2_id: str
    basis: DiscriminatorAuditBasis = "unsupported_assertion"
    failure_class: DiscriminatorFailureClass
    reasoning: str = Field(min_length=8)
    repair_instruction: str = Field(min_length=8)


DiscriminatorJudgment = Annotated[
    AcceptedDiscriminatorJudgment | RejectedDiscriminatorJudgment,
    Field(discriminator="disposition"),
]


class DiscriminatorAudit(BaseModel):
    """Complete independent semantic review bound to one testing artifact."""

    testing_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    inference_mode: InferenceMode = "theory_first"
    candidates: list[DiscriminatorCandidate] = Field(default_factory=list)
    judgments: list[DiscriminatorJudgment] = Field(default_factory=list)
    reviewer_model: str
    decision_blockers: list[str] = Field(default_factory=list)
    accepted_count: int = Field(default=0, ge=0)
    rejected_count: int = Field(default=0, ge=0)
    summary: str

    @model_validator(mode="after")
    def _validate_candidate_coverage(self) -> "DiscriminatorAudit":
        candidate_ids = [candidate.candidate_id for candidate in self.candidates]
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("discriminator audit contains duplicate candidate ids")
        judgment_ids = [judgment.candidate_id for judgment in self.judgments]
        if len(judgment_ids) != len(set(judgment_ids)):
            raise ValueError("discriminator audit contains duplicate judgment ids")
        if set(judgment_ids) != set(candidate_ids):
            raise ValueError(
                "discriminator audit candidate coverage mismatch: "
                f"missing {sorted(set(candidate_ids) - set(judgment_ids))}, "
                f"extra {sorted(set(judgment_ids) - set(candidate_ids))}"
            )

        candidate_by_id = {
            candidate.candidate_id: candidate for candidate in self.candidates
        }
        for judgment in self.judgments:
            candidate = candidate_by_id[judgment.candidate_id]
            identity = (judgment.evidence_id, judgment.h1_id, judgment.h2_id)
            expected = (candidate.evidence_id, candidate.h1_id, candidate.h2_id)
            if identity != expected:
                raise ValueError(
                    "discriminator judgment identity mismatch for "
                    f"'{judgment.candidate_id}': {identity} != {expected}"
                )

        self.accepted_count = sum(
            judgment.disposition == "accepted" for judgment in self.judgments
        )
        self.rejected_count = len(self.judgments) - self.accepted_count
        self.decision_blockers = [
            (
                f"{judgment.candidate_id} ({judgment.evidence_id}, "
                f"{judgment.h1_id}<->{judgment.h2_id}): "
                f"{judgment.failure_class}: {judgment.reasoning}"
            )
            for judgment in self.judgments
            if judgment.disposition == "rejected"
        ]
        return self


class DiscriminatorAuditAttempt(BaseModel):
    attempt: int = Field(ge=1)
    action: str
    testing_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    audit: DiscriminatorAudit

    @model_validator(mode="after")
    def _hash_matches_audit(self) -> "DiscriminatorAuditAttempt":
        if self.testing_sha256 != self.audit.testing_sha256:
            raise ValueError("discriminator attempt hash must match its audit hash")
        return self


class DiscriminatorAuditResolution(BaseModel):
    status: Literal["repairing", "accepted", "blocked"]
    attempts: list[DiscriminatorAuditAttempt] = Field(default_factory=list)
    final_audit: DiscriminatorAudit
    effective_testing: Optional[TestingResult] = Field(
        default=None,
        description=(
            "Audited likelihood artifact used downstream. The original TestingResult "
            "remains unchanged and is bound by final_audit.testing_sha256."
        ),
    )

    @model_validator(mode="after")
    def _validate_resolution(self) -> "DiscriminatorAuditResolution":
        if self.attempts and self.attempts[-1].audit != self.final_audit:
            raise ValueError(
                "discriminator final audit must match the last recorded attempt"
            )
        if (
            self.status == "accepted"
            and self.final_audit.decision_blockers
            and self.effective_testing is None
        ):
            raise ValueError("accepted discriminator resolution cannot contain blockers")
        if self.status == "blocked" and not self.final_audit.decision_blockers:
            raise ValueError("blocked discriminator resolution requires a blocker")
        return self


class MechanismPredictionContrastRef(BaseModel):
    """Compact reference to one accepted opposed-prediction contrast."""

    h1_prediction_id: str
    h2_prediction_id: str
    contrast_dimension: ContrastDimension


class MechanismAcceptedDiscriminatorContext(BaseModel):
    """One terminal accepted discriminator without repeated corpus prose."""

    candidate_id: str
    evidence_id: str
    h1_id: str
    h2_id: str
    favored_hypothesis_id: str
    raw_likelihood_ratio: float = Field(ge=1.0, allow_inf_nan=False)
    basis: DiscriminatorAuditBasis
    aligned_prediction_ids: list[str] = Field(default_factory=list)
    accepted_prediction_contrasts: list[MechanismPredictionContrastRef] = Field(
        default_factory=list
    )
    audit_reasoning: str = Field(min_length=8)


class MechanismRejectedDiscriminatorContext(BaseModel):
    """One prior rejection that constrains mechanism interpretation."""

    attempt: int = Field(ge=1)
    testing_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    candidate_id: str
    evidence_id: str
    h1_id: str
    h2_id: str
    favored_hypothesis_id: str
    basis: DiscriminatorAuditBasis
    aligned_prediction_ids: list[str] = Field(default_factory=list)
    failure_class: DiscriminatorFailureClass
    audit_reasoning: str = Field(min_length=8)
    repair_instruction: str = Field(min_length=8)


class MechanismDiscriminatorAttemptSummary(BaseModel):
    """Counts and lineage for one complete discriminator-audit attempt."""

    attempt: int = Field(ge=1)
    testing_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    reviewer_model: str
    accepted_count: int = Field(ge=0)
    rejected_count: int = Field(ge=0)


class MechanismDiscriminatorContext(BaseModel):
    """Integrity-bound discriminator decisions supplied to the mechanism critic."""

    resolution_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    terminal_testing_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    attempts: list[MechanismDiscriminatorAttemptSummary] = Field(min_length=1)
    accepted: list[MechanismAcceptedDiscriminatorContext] = Field(
        default_factory=list
    )
    prior_rejections: list[MechanismRejectedDiscriminatorContext] = Field(
        default_factory=list
    )


# ── Bayesian Update ─────────────────────────────────────────────────

class EvidenceUpdate(BaseModel):
    evidence_id: str
    prediction_id: Optional[str] = None
    prediction_ids: list[str] = Field(
        default_factory=list,
        description="Direct prediction IDs carried by this evidence or pooled evidence unit.",
    )
    likelihood_ratio: float
    prior: float
    posterior: float


class HypothesisPosterior(BaseModel):
    hypothesis_id: str
    prior: float
    updates: list[EvidenceUpdate]
    final_posterior: float
    robustness: str = Field(
        default="unknown",
        description="Mechanically computed: 'robust' if posterior driven by few decisive LRs, "
        "'fragile' if driven by many small LRs"
    )
    top_drivers: list[str] = Field(
        default_factory=list,
        description="Evidence IDs of the top 3 most influential LR updates (|log(LR)| largest)"
    )


class SensitivityEntry(BaseModel):
    hypothesis_id: str
    baseline_posterior: float
    posterior_low: float = Field(description="Posterior when top drivers are perturbed against this hypothesis")
    posterior_high: float = Field(description="Posterior when top drivers are perturbed for this hypothesis")
    rank_stable: bool = Field(description="True if this hypothesis keeps its rank across all perturbations")


class PriorSensitivity(BaseModel):
    """Whether the ranking survives reasonable changes to the prior."""
    top_hypothesis_id: str
    stable_under_prior_perturbation: bool = Field(
        description="True if the top-ranked hypothesis stays top when each hypothesis's "
        "prior is independently up- and down-weighted by the perturbation factor."
    )
    perturbation_factor: float = Field(
        default=2.0, description="Multiplicative factor applied to each prior."
    )


class DependenceLevelSummary(BaseModel):
    """Effective-evidence reduction produced by one hierarchy level."""

    level: DependenceLevel
    input_effective_count: float = Field(ge=0.0, allow_inf_nan=False)
    output_effective_count: float = Field(ge=0.0, allow_inf_nan=False)
    group_count: int = Field(ge=0)


class BayesianResult(BaseModel):
    posteriors: list[HypothesisPosterior]
    ranking: list[str] = Field(description="Hypothesis IDs ordered by final posterior, highest first")
    sensitivity: list[SensitivityEntry] = Field(
        default_factory=list,
        description="How posteriors change when the most influential LRs are perturbed ±50%"
    )
    prior_sensitivity: Optional[PriorSensitivity] = Field(
        default=None,
        description="Whether the top-ranked hypothesis is robust to changes in the prior."
    )
    dependence_summary: list[DependenceLevelSummary] = Field(
        default_factory=list,
        description=(
            "Raw-to-effective observation counts after each ordered dependence level. "
            "Empty for legacy flat-cluster updates."
        ),
    )
    likelihood_policy: Optional[LikelihoodPolicySpec] = Field(
        default=None,
        description="Named deterministic policy used for this headline update.",
    )
    likelihood_lineage: list[EvidenceLikelihoodPolicyLineage] = Field(
        default_factory=list,
        description="Raw vector, centering, relevance, and effective LR for each item.",
    )
    policy_sensitivity: Optional[LikelihoodPolicySensitivity] = Field(
        default=None,
        description="Conclusion changes under named legacy cap scenarios.",
    )


# ── Pass 3.6: Diagnostic Test Matrix (deterministic derivation) ─────

class RivalDiscriminator(BaseModel):
    """One evidence item that discriminates between a specific rival pair."""
    evidence_id: str = Field(description="ID of the discriminating evidence item")
    log_lr_h1_over_h2: float = Field(
        description="log(LR_h1 / LR_h2) using effective LRs from the testing matrix. "
        "Positive means the evidence favors h1 over h2; negative favors h2."
    )
    favors: Literal["h1", "h2"] = Field(
        description="Which hypothesis this evidence favors: 'h1' or 'h2'."
    )
    strength: DiscriminatorStrength = Field(
        description=(
            "Magnitude descriptor only: 'decisive' at 5x or greater, 'strong' at "
            "2x or greater, and 'limited' below 2x. No category is an eligibility gate."
        )
    )
    diagnostic_type_h1: Optional[DiagnosticType] = Field(
        default=None,
        description="Van Evera type assigned by the LLM for this evidence under h1.",
    )
    diagnostic_type_h2: Optional[DiagnosticType] = Field(
        default=None,
        description="Van Evera type assigned by the LLM for this evidence under h2.",
    )
    prediction_links: list[EvidencePredictionLink] = Field(
        default_factory=list,
        description=(
            "Optional predeclared-prediction provenance. Semantic eligibility is supplied "
            "by the independently audited effective testing artifact, not by this list."
        ),
    )


class RivalPairDiagnostic(BaseModel):
    """Discriminator summary for one rival hypothesis pair."""
    h1_id: str
    h2_id: str
    discriminators: list[RivalDiscriminator] = Field(
        description="Semantically accepted evidence items with a non-equal effective likelihood."
    )
    discriminator_count: int = Field(
        ge=0,
        description="Number of discriminating evidence items for this pair.",
    )
    grade_capped: bool = Field(
        description="True if discriminator_count == 0; an A-level claim requires at least one "
        "source-grounded discriminator per rival pair."
    )


class DiagnosticMatrix(BaseModel):
    """Derived artifact: which evidence items discriminate which rival pairs.

    Computed deterministically from the testing result's likelihood vectors.
    No LLM call required. A grade cap is applied for every pair with zero discriminators.
    """
    rival_pair_diagnostics: list[RivalPairDiagnostic] = Field(
        description="One entry per rival hypothesis pair."
    )
    pairs_without_discriminators: list[list[str]] = Field(
        default_factory=list,
        description="Pairs of [h1_id, h2_id] with zero discriminating evidence items.",
    )
    grade_cap_applied: bool = Field(
        description="True if any rival pair lacks discriminators."
    )


# ── Pass 3b: Absence-of-Evidence ───────────────────────────────────

class AbsenceEvaluation(BaseModel):
    hypothesis_id: str
    prediction_id: str
    missing_evidence: str = Field(description="What predicted evidence is absent from the text")
    reasoning: str = Field(description="Why absence is informative given the text's scope")
    severity: Severity = Field(description="'damaging', 'notable', or 'minor'")
    would_be_extractable: bool = Field(
        description="Would this evidence appear in a text of this scope if it existed?"
    )
    expected_source_genre: Optional[SourceGenre] = Field(
        default=None,
        description=(
            "The genre of source that would typically carry this missing trace — "
            "e.g. 'primary_document' for correspondence, 'parliamentary_record' for debate logs, "
            "'secondary_analysis' for academic interpretation. Populate regardless of "
            "would_be_extractable: even when the current text cannot carry the evidence, "
            "naming the genre tells the researcher what to acquire next."
        ),
    )
    expected_source_location: Optional[str] = Field(
        default=None,
        description=(
            "Specific type of source where this evidence would appear — "
            "e.g. 'police surveillance reports from the Directory period', "
            "'minutes of the Conseil des Cinq-Cents', 'private correspondence of Napoleon'. "
            "Be concrete enough to drive an acquisition decision. Populate whenever "
            "you can name a plausible archive, collection, or document type."
        ),
    )


MissingnessState = Literal[
    "source_silence",
    "absent_from_extraction",
    "absent_from_query",
    "source_opportunity_unsupported",
]


class SourceSilenceOpportunity(BaseModel):
    """One admitted source channel expected to carry a predicted trace."""

    source_id: str = Field(min_length=1)
    trace_if_true_observability: float = Field(gt=0.0, le=1.0)
    false_assertion_probability: float = Field(ge=0.0, lt=1.0)
    reasoning: str = Field(min_length=12)
    limitations: list[str] = Field(default_factory=list)


class SilenceHypothesisLikelihood(BaseModel):
    """Raw probability of observing the exact source silence under one rival."""

    hypothesis_id: str
    source_silence_probability: float = Field(gt=0.0, le=1.0)
    reasoning: str = Field(min_length=12)


class SourceSilenceLikelihood(BaseModel):
    """One coherent rival-complete likelihood vector for a missing trace."""

    finding_id: str = Field(pattern=r"^absence_[A-Za-z0-9_-]+$")
    hypothesis_id: str
    prediction_id: str
    missingness_state: MissingnessState
    query_evidence_ids_checked: list[str] = Field(min_length=1)
    partial_observation_evidence_ids: list[str] = Field(default_factory=list)
    source_opportunities: list[SourceSilenceOpportunity] = Field(default_factory=list)
    hypothesis_likelihoods: list[SilenceHypothesisLikelihood] = Field(min_length=1)
    dependence_group: str | None = None


class SourceSilenceAuditJudgment(BaseModel):
    finding_id: str
    accepted: bool
    missingness_state: MissingnessState
    query_complete: bool
    source_opportunity_supported: bool
    vector_direction_supported: bool
    vector_magnitude_supported: bool
    reasoning: str = Field(min_length=12)


class SourceSilenceAuditResponse(BaseModel):
    """Provider-owned semantic judgments before runtime lineage is attached."""

    judgments: list[SourceSilenceAuditJudgment]


class SourceSilenceAuditResolution(BaseModel):
    candidate_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    testing_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    extraction_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_scope_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    audit_context_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    inference_mode: InferenceMode
    hypothesis_ids: list[str] = Field(min_length=1)
    evidence_ids: list[str] = Field(min_length=1)
    admitted_source_ids: list[str] = Field(min_length=1)
    reviewer_model: str
    judgments: list[SourceSilenceAuditJudgment]


class AbsenceResponse(BaseModel):
    """Provider-owned absence appraisal before runtime lineage is attached."""

    evaluations: list[AbsenceEvaluation] = []
    source_silence_likelihoods: list[SourceSilenceLikelihood] = Field(
        default_factory=list,
        description="Raw source-silence candidates; never update without a matching accepted audit.",
    )


class AbsenceResult(AbsenceResponse):
    """Persisted absence appraisal plus deterministic audit and update artifacts."""

    source_silence_audit_resolution: SourceSilenceAuditResolution | None = None
    absence_adjusted_testing: TestingResult | None = Field(
        default=None,
        description=(
            "Exact inference input formed by appending only independently accepted "
            "source-silence vectors to unchanged audited positive evidence."
        ),
    )
    no_absence_bayesian: BayesianResult | None = Field(
        default=None,
        description="Counterfactual update on unchanged audited positive evidence only.",
    )


NonAdmissionDisposition = Literal[
    "valid_qualitative_only",
    "missed_candidate",
    "borderline_requires_adjudication",
    "invalid_finding",
]


class SourceSilenceNonAdmissionJudgment(BaseModel):
    """Independent disposition of one producer-owned qualitative finding."""

    model_config = ConfigDict(extra="forbid")

    unit_id: str = Field(min_length=1)
    missing_evidence_claim: str = Field(min_length=12)
    disposition: NonAdmissionDisposition
    qualitative_missing_trace_supported: bool
    target_trace_direct_and_observable: bool
    query_complete: Literal[True]
    query_evidence_registry_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    partial_observation_evidence_ids: list[str] = Field(default_factory=list)
    source_opportunities: list[SourceSilenceOpportunity] = Field(default_factory=list)
    hypothesis_likelihoods: list[SilenceHypothesisLikelihood] = Field(default_factory=list)
    dependence_group: str | None = None
    reasoning: str = Field(min_length=24)
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _missed_candidate_is_structurally_complete(
        self,
    ) -> "SourceSilenceNonAdmissionJudgment":
        if self.disposition in {"valid_qualitative_only", "missed_candidate"} and not self.qualitative_missing_trace_supported:
            raise ValueError(
                f"{self.disposition} requires a supported qualitative missing-trace claim"
            )
        if self.disposition == "invalid_finding" and self.qualitative_missing_trace_supported:
            raise ValueError("invalid_finding requires an unsupported qualitative missing-trace claim")
        if self.disposition == "missed_candidate" and (
            not self.target_trace_direct_and_observable
            or self.partial_observation_evidence_ids
            or not self.source_opportunities
            or not self.hypothesis_likelihoods
            or not self.dependence_group
        ):
            raise ValueError(
                "a numerical-candidate disposition requires a direct observable trace, "
                "complete hash-bound query, no partial observation, source opportunity, "
                "complete likelihood vector, and dependence group"
            )
        return self


class SourceSilenceNonAdmissionAuditResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    judgments: list[SourceSilenceNonAdmissionJudgment] = Field(min_length=1)


# ── Pass 5: Refinement (Second Reading) ────────────────────────────

class NewEvidence(BaseModel):
    id: str = Field(description="Must use 'evi_ref_' prefix to distinguish from original extraction")
    description: str
    source_text: str = Field(description="Direct quote from input text")
    source_id: Optional[str] = Field(
        default=None,
        description="Stable source-packet identifier for the quoted passage.",
    )
    source_span_id: Optional[str] = Field(
        default=None,
        description="System-assigned immutable source-span identifier for source_text.",
    )
    source_quote: Optional[str] = Field(
        default=None,
        description="Exact quote used to resolve and anchor source_span_id.",
    )
    evidence_type: EvidenceType = Field(default="empirical", description="'empirical' or 'interpretive'")
    approximate_date: Optional[str] = None
    normalized_year: Optional[int] = Field(
        default=None,
        description=(
            "Gregorian/CE year for deterministic temporal comparison; negative for BCE "
            "and null when the source date cannot be normalized safely."
        ),
    )
    rationale: str = Field(description="Why missed initially, why it matters now")


class ReinterpretedEvidence(BaseModel):
    evidence_id: str
    original_type: EvidenceType
    new_type: EvidenceType
    reinterpretation: str
    updated_description: Optional[str] = None


class NewCausalEdge(BaseModel):
    source_id: str = Field(
        description=(
            "Existing event/actor/mechanism/evidence id, or a new evi_ref_* "
            "evidence id created in this same refinement. Do not use hypothesis ids."
        )
    )
    target_id: str = Field(
        description=(
            "Existing event/actor/mechanism/evidence id, or a new evi_ref_* "
            "evidence id created in this same refinement. Do not use hypothesis ids."
        )
    )
    relationship: str = Field(description="Substantive causal/process relationship, not evidentiary support.")
    source_text_support: str = Field(description="Quote from input text")
    support_source_id: Optional[str] = Field(
        default=None,
        description="Stable source-packet identifier for the supporting quote.",
    )
    support_source_span_id: Optional[str] = Field(
        default=None,
        description=(
            "System-assigned immutable source-span identifier for source_text_support."
        ),
    )
    support_quote: Optional[str] = Field(
        default=None,
        description="Exact quote used to resolve and anchor support_source_span_id.",
    )


class SpuriousExtraction(BaseModel):
    item_id: str = Field(description="Evidence ID or 'source_id->target_id' for edges")
    item_type: Literal["evidence", "causal_edge"] = Field(
        description="'evidence' or 'causal_edge'"
    )
    reason: str


class _HypothesisRefinementBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str = Field(
        description=(
            "Existing hypothesis id for state-changing refinements. For "
            "merge_suggestion, may be an existing id or a descriptive advisory "
            "id naming the proposed merge, e.g. 'h1_h4_merge_suggestion'."
        )
    )
    description: str = Field(description="Why this refinement is warranted")


class SharpenMechanismRefinement(_HypothesisRefinementBase):
    refinement_type: Literal["sharpen_mechanism"]
    updated_causal_mechanism: str = Field(
        min_length=1,
        description="Complete replacement causal mechanism",
    )


class AddPredictionRefinement(_HypothesisRefinementBase):
    refinement_type: Literal["add_prediction"]
    new_predictions: list[Prediction] = Field(min_length=1)


class ReframeHypothesisRefinement(_HypothesisRefinementBase):
    refinement_type: Literal["reframe"]
    updated_description: str = Field(
        min_length=1,
        description="Complete replacement hypothesis description",
    )
    updated_causal_mechanism: str = Field(
        min_length=1,
        description="Complete replacement causal mechanism",
    )


class MergeSuggestionRefinement(_HypothesisRefinementBase):
    refinement_type: Literal["merge_suggestion"]


HypothesisRefinement = Annotated[
    SharpenMechanismRefinement
    | AddPredictionRefinement
    | ReframeHypothesisRefinement
    | MergeSuggestionRefinement,
    Field(discriminator="refinement_type"),
]


class MissingMechanism(BaseModel):
    description: str
    source_text_support: str
    source_id: Optional[str] = Field(
        default=None,
        description="Stable source-packet identifier for the supporting quote.",
    )
    source_span_id: Optional[str] = Field(
        default=None,
        description=(
            "System-assigned immutable source-span identifier for source_text_support."
        ),
    )
    source_quote: Optional[str] = Field(
        default=None,
        description="Exact quote used to resolve and anchor source_span_id.",
    )
    relevant_hypotheses: list[str]


class RefinementResult(BaseModel):
    new_evidence: list[NewEvidence] = []
    reinterpreted_evidence: list[ReinterpretedEvidence] = []
    new_causal_edges: list[NewCausalEdge] = []
    spurious_extractions: list[SpuriousExtraction] = []
    hypothesis_refinements: list[HypothesisRefinement] = []
    missing_mechanisms: list[MissingMechanism] = []
    analyst_notes: str = Field(description="Free-text analytical notes from the refinement pass")

    def has_material_changes(self) -> bool:
        """Return whether applying this delta can change inferential state."""
        state_changing_hypothesis_refinements = any(
            item.refinement_type != "merge_suggestion"
            for item in self.hypothesis_refinements
        )
        return bool(
            self.new_evidence
            or self.reinterpreted_evidence
            or self.new_causal_edges
            or self.spurious_extractions
            or state_changing_hypothesis_refinements
        )


# ── Pass 4: Synthesis ───────────────────────────────────────────────

class MechanismStage(BaseModel):
    """One temporally ordered proposition in the case mechanism."""

    stage_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    sequence_index: int = Field(ge=1)
    label: str = Field(min_length=3, max_length=80)
    description: str = Field(min_length=8)
    approximate_date: Optional[str] = None
    stage_type: MechanismStageType
    status: MechanismStageStatus
    evidence_ids: list[str] = Field(default_factory=list)
    prediction_ids: list[str] = Field(default_factory=list)
    hypothesis_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _require_observed_grounding(self) -> "MechanismStage":
        if not self.evidence_ids:
            raise ValueError(
                "mechanism stage requires accepted-corpus evidence; represent "
                "unobserved predictions and missing traces on unresolved edges "
                "or in the evidence-development agenda"
            )
        if self.status == "unresolved" and not self.prediction_ids:
            raise ValueError(
                "unresolved observed stage requires at least one prediction_id"
            )
        for label, values in (
            ("evidence", self.evidence_ids),
            ("prediction", self.prediction_ids),
            ("hypothesis", self.hypothesis_ids),
        ):
            if len(values) != len(set(values)):
                raise ValueError(f"mechanism stage contains duplicate {label} IDs")
        return self


class MechanismEdgeAssessment(BaseModel):
    """Evidence-bounded interpretation of one forward temporal transition."""

    edge_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    source_stage_id: str
    target_stage_id: str
    relationship: str = Field(min_length=1)
    status: MechanismEdgeStatus
    evidence_ids: list[str] = Field(default_factory=list)
    hypothesis_ids: list[str] = Field(min_length=1)
    reasoning: str = Field(min_length=12)
    missing_test: Optional[str] = None

    @model_validator(mode="after")
    def _validate_evidentiary_status(self) -> "MechanismEdgeAssessment":
        if not self.relationship.strip():
            raise ValueError("mechanism edge relationship must not be blank")
        if self.status != "unresolved_link" and not self.evidence_ids:
            raise ValueError("non-unresolved mechanism edge requires evidence")
        if self.status == "unresolved_link" and not (
            self.missing_test and self.missing_test.strip()
        ):
            raise ValueError("unresolved mechanism edge requires missing_test")
        if self.source_stage_id == self.target_stage_id:
            raise ValueError("mechanism edge cannot be a self-loop")
        if len(self.evidence_ids) != len(set(self.evidence_ids)):
            raise ValueError("mechanism edge contains duplicate evidence IDs")
        if len(self.hypothesis_ids) != len(set(self.hypothesis_ids)):
            raise ValueError("mechanism edge contains duplicate hypothesis IDs")
        return self


class MechanismTraceResult(BaseModel):
    """Temporal DAG separating observed sequence from causal interpretation."""

    stages: list[MechanismStage] = Field(min_length=2)
    edges: list[MechanismEdgeAssessment] = Field(min_length=1)
    established_summary: str = Field(min_length=20)
    unresolved_summary: str = Field(min_length=20)

    @model_validator(mode="after")
    def _validate_local_dag(self) -> "MechanismTraceResult":
        _require_unique_ids([stage.stage_id for stage in self.stages], "mechanism stage")
        _require_unique_ids([edge.edge_id for edge in self.edges], "mechanism edge")
        indexes = [stage.sequence_index for stage in self.stages]
        if len(indexes) != len(set(indexes)):
            raise ValueError("mechanism stage sequence indexes must be unique")
        stage_by_id = {stage.stage_id: stage for stage in self.stages}
        unknown_endpoints = [
            edge.edge_id
            for edge in self.edges
            if edge.source_stage_id not in stage_by_id
            or edge.target_stage_id not in stage_by_id
        ]
        if unknown_endpoints:
            raise ValueError(
                f"mechanism edges reference unknown stages: {sorted(unknown_endpoints)}"
            )
        backward = [
            edge.edge_id
            for edge in self.edges
            if stage_by_id[edge.source_stage_id].sequence_index
            >= stage_by_id[edge.target_stage_id].sequence_index
        ]
        if backward:
            raise ValueError(
                f"mechanism edges must point forward in time: {sorted(backward)}"
            )
        pairs = [
            (edge.source_stage_id, edge.target_stage_id) for edge in self.edges
        ]
        if len(pairs) != len(set(pairs)):
            raise ValueError("mechanism trace contains duplicate stage transitions")
        return self


class MechanismStageJudgment(BaseModel):
    """Independent corpus-bounded judgment of one proposed mechanism stage."""

    stage_id: str = Field(description="Exact candidate stage ID reviewed.")
    disposition: MechanismStageAuditDisposition = Field(
        description="Accept the stage or require material full-DAG revision."
    )
    reasoning: str = Field(
        min_length=12,
        description="Corpus-bounded basis for the stage disposition.",
    )
    recommendation: str = Field(
        min_length=1,
        description="Concrete retain, revise, or evidence-development recommendation.",
    )
    evidence_ids: list[str] = Field(
        default_factory=list,
        description="Accepted evidence IDs grounding a material stage criticism.",
    )
    prediction_ids: list[str] = Field(
        default_factory=list,
        description="Frozen prediction IDs grounding a prospective stage criticism.",
    )
    missing_test: Optional[str] = Field(
        default=None,
        description="Concrete trace needed when a material stage concern is not observed.",
    )

    @model_validator(mode="after")
    def _require_material_basis(self) -> "MechanismStageJudgment":
        if not self.recommendation.strip():
            raise ValueError("mechanism stage recommendation must not be blank")
        if len(self.evidence_ids) != len(set(self.evidence_ids)):
            raise ValueError("mechanism stage judgment contains duplicate evidence IDs")
        if len(self.prediction_ids) != len(set(self.prediction_ids)):
            raise ValueError("mechanism stage judgment contains duplicate prediction IDs")
        if self.disposition == "material_revision_required" and not (
            self.evidence_ids
            or self.prediction_ids
            or (self.missing_test and self.missing_test.strip())
        ):
            raise ValueError(
                "material stage judgment requires evidence, a frozen prediction, "
                "or a missing test"
            )
        return self


class MechanismEdgeJudgment(BaseModel):
    """Independent corpus-bounded judgment and conservative edge disposition."""

    edge_id: str = Field(description="Exact candidate edge ID reviewed.")
    disposition: MechanismEdgeAuditDisposition = Field(
        description="Redundant label derived from candidate and recommended statuses."
    )
    recommended_status: MechanismEdgeStatus = Field(
        description="Final corpus-conditional status; may retain or weaken, never strengthen."
    )
    evidence_assessment: MechanismEvidenceAssessment = Field(
        description="Strongest transition evidence actually supplied by the corpus."
    )
    reasoning: str = Field(
        min_length=12,
        description="Corpus-bounded rationale for the recommended edge status.",
    )
    replacement_reasoning: Optional[str] = Field(
        default=None,
        min_length=12,
        description=(
            "Audit-authored, publication-ready final edge reasoning. Fresh "
            "semantic audits must populate this for every edge, including when "
            "status is retained; optionality preserves retained artifact parsing."
        ),
    )
    missing_test: Optional[str] = Field(
        default=None,
        description="Concrete trace needed when the recommended status is unresolved.",
    )

    @model_validator(mode="after")
    def _require_missing_test_for_unresolved(self) -> "MechanismEdgeJudgment":
        if self.replacement_reasoning is not None and not (
            self.replacement_reasoning.strip()
        ):
            raise ValueError("replacement edge reasoning must not be blank")
        if self.recommended_status == "unresolved_link" and not (
            self.missing_test and self.missing_test.strip()
        ):
            raise ValueError(
                "unresolved mechanism audit recommendation requires missing_test"
            )
        return self


class MechanismOmissionFinding(BaseModel):
    """Candidate stage or transition absent from the proposed DAG."""

    finding_id: str = Field(
        pattern=r"^[A-Za-z0-9_-]+$",
        description="Unique ID within this critique.",
    )
    severity: MechanismOmissionSeverity = Field(
        description="Advisory evidence need or material directly observed omission."
    )
    target_type: MechanismOmissionTarget = Field(
        description="Whether the distinct omitted content is a stage or transition."
    )
    grounding: MechanismOmissionGrounding = Field(
        description=(
            "Whether accepted evidence directly observes the omitted stage/transition, "
            "only observes its endpoints, or supplies only a frozen prediction."
        )
    )
    description: str = Field(
        min_length=12,
        description="Exact omitted content and why it is not already represented.",
    )
    evidence_ids: list[str] = Field(
        default_factory=list,
        description="Accepted evidence IDs that ground or bound the finding.",
    )
    hypothesis_ids: list[str] = Field(
        default_factory=list,
        description="Frozen rivals whose interpretation could be affected.",
    )
    prediction_ids: list[str] = Field(
        default_factory=list,
        description="Frozen predictions related to the omitted trace.",
    )
    recommendation: str = Field(
        min_length=12,
        description="Graph correction or source-acquisition recommendation.",
    )
    missing_test: Optional[str] = Field(
        default=None,
        description="Concrete evidence needed when the corpus does not observe the trace.",
    )

    @model_validator(mode="after")
    def _require_corpus_basis_or_test(self) -> "MechanismOmissionFinding":
        if not self.evidence_ids and not self.prediction_ids and not (
            self.missing_test and self.missing_test.strip()
        ):
            raise ValueError(
                "mechanism omission requires evidence, a frozen prediction, or a missing test"
            )
        if self.severity == "material" and (
            self.grounding != "directly_observed" or not self.evidence_ids
        ):
            raise ValueError(
                "material mechanism omission requires directly observed accepted-corpus evidence"
            )
        if (
            self.grounding == "directly_observed"
            and self.evidence_ids
            and self.severity != "material"
        ):
            raise ValueError(
                "directly observed mechanism omission with accepted-corpus evidence "
                "must be material"
            )
        return self


class MechanismRepairConstraintJudgment(BaseModel):
    """Independent judgment of one exact cumulative repair constraint."""

    constraint_id: str = Field(
        pattern=r"^mrc_[0-9a-f]{24}$",
        description="Exact repair-ledger constraint ID reviewed.",
    )
    disposition: MechanismRepairConstraintDisposition = Field(
        description="Whether the candidate semantically satisfies the constraint.",
    )
    satisfied_by_stage_ids: list[str] = Field(
        default_factory=list,
        description="Candidate stages that represent the required content.",
    )
    satisfied_by_edge_ids: list[str] = Field(
        default_factory=list,
        description="Candidate edges that represent the required transition.",
    )
    reasoning: str = Field(
        min_length=12,
        description="Corpus-bounded comparison of the constraint with the candidate.",
    )

    @model_validator(mode="after")
    def _require_unique_references(self) -> "MechanismRepairConstraintJudgment":
        if len(self.satisfied_by_stage_ids) != len(
            set(self.satisfied_by_stage_ids)
        ):
            raise ValueError(
                "mechanism constraint judgment duplicates candidate stage IDs"
            )
        if len(self.satisfied_by_edge_ids) != len(set(self.satisfied_by_edge_ids)):
            raise ValueError(
                "mechanism constraint judgment duplicates candidate edge IDs"
            )
        if self.disposition == "satisfied" and not (
            self.satisfied_by_stage_ids or self.satisfied_by_edge_ids
        ):
            raise ValueError(
                "satisfied mechanism constraint requires a candidate stage or edge"
            )
        return self


class MechanismEdgeProseAudit(BaseModel):
    """Compact independent audit of one exact displayed mechanism edge."""

    model_config = ConfigDict(extra="forbid")

    mechanism_trace_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    edge_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    relationship_disposition: Literal["accepted", "material_revision_required"]
    relationship_reasoning: str = Field(min_length=12)
    evidence_ids: list[str] = Field(min_length=1)
    edge_judgment: MechanismEdgeJudgment
    repair_constraint_judgments: list[MechanismRepairConstraintJudgment]
    overall_assessment: str = Field(min_length=12)

    @model_validator(mode="after")
    def _require_unique_evidence(self) -> "MechanismEdgeProseAudit":
        if len(self.evidence_ids) != len(set(self.evidence_ids)):
            raise ValueError("focused edge prose audit duplicates evidence IDs")
        return self


class MechanismCritique(BaseModel):
    """Independent semantic review of one exact mechanism candidate."""

    mechanism_trace_sha256: str = Field(
        pattern=r"^[0-9a-f]{64}$",
        description="Canonical SHA-256 of the exact candidate DAG.",
    )
    stage_judgments: list[MechanismStageJudgment] = Field(
        description="Exactly one judgment for every candidate stage."
    )
    edge_judgments: list[MechanismEdgeJudgment] = Field(
        description="Exactly one judgment for every candidate edge."
    )
    omission_findings: list[MechanismOmissionFinding] = Field(
        default_factory=list,
        description="Distinct absent stages/transitions or advisory evidence needs.",
    )
    repair_constraint_judgments: list[
        MechanismRepairConstraintJudgment
    ] = Field(
        default_factory=list,
        description=(
            "Exactly one semantic satisfaction judgment for every supplied "
            "cumulative repair constraint."
        ),
    )
    recommended_established_summary: str = Field(
        min_length=20,
        description="Summary limited to what final edge statuses establish.",
    )
    recommended_unresolved_summary: str = Field(
        min_length=20,
        description="Summary of contested/unresolved transitions and next tests.",
    )
    overall_assessment: str = Field(
        min_length=20,
        description="Concise corpus-conditional adequacy assessment.",
    )


class MechanismAuditCorrection(BaseModel):
    """One deterministic edge revision applied from a typed critic judgment."""

    edge_id: str
    from_status: MechanismEdgeStatus
    to_status: MechanismEdgeStatus
    reasoning: str = Field(min_length=12)


class MechanismStageDescriptionPatchOperation(BaseModel):
    """One hash-bound replacement of an audit-rejected stage description."""

    stage_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    expected_stage_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_judgment_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    replacement_description: str = Field(min_length=8)

    @model_validator(mode="after")
    def _require_nonblank_description(
        self,
    ) -> "MechanismStageDescriptionPatchOperation":
        if not self.replacement_description.strip():
            raise ValueError("replacement stage description must not be blank")
        if any(
            ord(character) < 32 and character not in "\n\r\t"
            for character in self.replacement_description
        ):
            raise ValueError(
                "replacement stage description contains an invalid control character"
            )
        return self


class MechanismStageDescriptionPatch(BaseModel):
    """A complete description-only repair for one exact rejected DAG."""

    schema_version: Literal["mechanism-stage-description-patch-v1"] = (
        "mechanism-stage-description-patch-v1"
    )
    base_mechanism_trace_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_critique_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    operations: list[MechanismStageDescriptionPatchOperation] = Field(min_length=1)

    @model_validator(mode="after")
    def _require_unique_stage_targets(self) -> "MechanismStageDescriptionPatch":
        stage_ids = [operation.stage_id for operation in self.operations]
        if len(stage_ids) != len(set(stage_ids)):
            raise ValueError("mechanism stage patch contains duplicate stage targets")
        return self


class MechanismStageDescriptionPatchCritique(BaseModel):
    """Focused independent review of the only objects a stage patch can affect."""

    patch_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    patched_mechanism_trace_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    stage_judgments: list[MechanismStageJudgment]
    incident_edge_judgments: list[MechanismEdgeJudgment]
    repair_constraint_judgments: list[MechanismRepairConstraintJudgment] = Field(
        default_factory=list
    )
    recommended_established_summary: str = Field(min_length=20)
    recommended_unresolved_summary: str = Field(min_length=20)
    overall_assessment: str = Field(min_length=20)


class MechanismGraphPatchTransitionInsertion(BaseModel):
    """One hash-bound observed transition resolving an exact omission finding."""

    finding_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    source_finding_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    edge: MechanismEdgeAssessment

    @model_validator(mode="after")
    def _reject_invalid_edge_controls(
        self,
    ) -> "MechanismGraphPatchTransitionInsertion":
        invalid_paths: list[str] = []

        def inspect(value: object, path: str) -> None:
            if isinstance(value, dict):
                for key, item in value.items():
                    inspect(item, f"{path}.{key}")
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    inspect(item, f"{path}[{index}]")
            elif isinstance(value, str) and any(
                ord(character) < 32 and character not in "\n\r\t"
                for character in value
            ):
                invalid_paths.append(path)

        inspect(self.edge.model_dump(mode="python"), "edge")
        if invalid_paths:
            raise ValueError(
                "graph patch edge contains invalid control characters at: "
                + ", ".join(invalid_paths)
            )
        return self


class MechanismGraphPatch(BaseModel):
    """A bounded repair of rejected prose and directly observed transitions."""

    schema_version: Literal["mechanism-graph-patch-v1"] = (
        "mechanism-graph-patch-v1"
    )
    base_mechanism_trace_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_critique_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    stage_operations: list[MechanismStageDescriptionPatchOperation] = Field(
        default_factory=list
    )
    transition_insertions: list[MechanismGraphPatchTransitionInsertion] = Field(
        default_factory=list
    )

    @model_validator(mode="after")
    def _require_unique_nonempty_targets(self) -> "MechanismGraphPatch":
        if not self.stage_operations and not self.transition_insertions:
            raise ValueError("mechanism graph patch requires at least one operation")
        stage_ids = [operation.stage_id for operation in self.stage_operations]
        if len(stage_ids) != len(set(stage_ids)):
            raise ValueError("mechanism graph patch duplicates a stage target")
        finding_ids = [
            insertion.finding_id for insertion in self.transition_insertions
        ]
        if len(finding_ids) != len(set(finding_ids)):
            raise ValueError("mechanism graph patch duplicates an omission finding")
        edge_ids = [insertion.edge.edge_id for insertion in self.transition_insertions]
        if len(edge_ids) != len(set(edge_ids)):
            raise ValueError("mechanism graph patch duplicates an inserted edge ID")
        return self


class MechanismGraphPatchCritique(BaseModel):
    """Focused independent review of every surface a graph patch can affect."""

    patch_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    patched_mechanism_trace_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    stage_judgments: list[MechanismStageJudgment]
    inserted_edge_judgments: list[MechanismEdgeJudgment]
    incident_existing_edge_judgments: list[MechanismEdgeJudgment]
    repair_constraint_judgments: list[MechanismRepairConstraintJudgment] = Field(
        default_factory=list
    )
    recommended_established_summary: str = Field(min_length=20)
    recommended_unresolved_summary: str = Field(min_length=20)
    overall_assessment: str = Field(min_length=20)


class MechanismAuditAttempt(BaseModel):
    """One candidate DAG and its exact independent critique."""

    attempt: int = Field(ge=1)
    action: Literal[
        "initial_audit",
        "omission_repair_audit",
        "stage_description_patch_audit",
        "graph_patch_audit",
    ]
    reviewer_model: str = Field(min_length=1)
    candidate_mechanism_trace: MechanismTraceResult
    candidate_mechanism_trace_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    critique: MechanismCritique
    stage_description_patch: Optional[MechanismStageDescriptionPatch] = Field(
        default=None,
        exclude_if=lambda value: value is None,
    )
    graph_patch: Optional[MechanismGraphPatch] = Field(
        default=None,
        exclude_if=lambda value: value is None,
    )

    @model_validator(mode="after")
    def _bind_patch_to_action(self) -> "MechanismAuditAttempt":
        is_patch_action = self.action == "stage_description_patch_audit"
        if is_patch_action != (self.stage_description_patch is not None):
            raise ValueError(
                "stage-description patch lineage must appear exactly on its audit action"
            )
        is_graph_patch_action = self.action == "graph_patch_audit"
        if is_graph_patch_action != (self.graph_patch is not None):
            raise ValueError(
                "graph patch lineage must appear exactly on its audit action"
            )
        if self.stage_description_patch is not None and self.graph_patch is not None:
            raise ValueError("mechanism audit attempt cannot contain two patch types")
        return self


class MechanismRepairConstraint(BaseModel):
    """Deterministic instruction for repair or accepted-content preservation."""

    constraint_id: str = Field(pattern=r"^mrc_[0-9a-f]{24}$")
    originating_attempt: int = Field(
        ge=0,
        description="Audit attempt that created the constraint; zero means an external binding constraint.",
    )
    constraint_type: Literal[
        "resolve_material_finding",
        "preserve_accepted_stage",
        "enforce_terminal_constraint",
    ]
    target_kind: Literal["stage", "transition"]
    target_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    finding_basis: str = Field(min_length=12)
    required_action: str = Field(min_length=8)
    evidence_ids: list[str] = Field(default_factory=list)
    prediction_ids: list[str] = Field(default_factory=list)
    missing_test: Optional[str] = None
    basis_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def _require_unique_references(self) -> "MechanismRepairConstraint":
        if (self.originating_attempt == 0) != (
            self.constraint_type == "enforce_terminal_constraint"
        ):
            raise ValueError(
                "external mechanism constraints require attempt zero and "
                "enforce_terminal_constraint"
            )
        if len(self.evidence_ids) != len(set(self.evidence_ids)):
            raise ValueError("mechanism repair constraint duplicates evidence IDs")
        if len(self.prediction_ids) != len(set(self.prediction_ids)):
            raise ValueError("mechanism repair constraint duplicates prediction IDs")
        return self


class MechanismRepairContext(BaseModel):
    """Complete repair-and-preservation ledger supplied to a replacement."""

    schema_version: Literal["mechanism-repair-context-v1"] = (
        "mechanism-repair-context-v1"
    )
    constraints: list[MechanismRepairConstraint]


class MechanismAuditResolution(BaseModel):
    """Terminal lineage binding an accepted critic result to the final DAG."""

    status: Literal["accepted", "blocked"]
    attempts: list[MechanismAuditAttempt] = Field(min_length=1)
    repair_constraints: list[MechanismRepairConstraint] = Field(
        default_factory=list,
        description=(
            "Deterministically reconstructed repair-and-preservation ledger."
        ),
    )
    corrections: list[MechanismAuditCorrection] = Field(default_factory=list)
    final_mechanism_trace_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    final_critique: MechanismCritique


class HypothesisVerdict(BaseModel):
    hypothesis_id: str
    status: VerdictStatus = Field(description="'strongly_supported', 'supported', 'weakened', 'eliminated', or 'indeterminate'")
    key_evidence_for: list[str] = Field(description="Evidence IDs that support this hypothesis")
    key_evidence_against: list[str] = Field(description="Evidence IDs that weigh against this hypothesis")
    reasoning: str
    steelman: str = Field(
        description=(
            "The strongest concise case for this hypothesis that is supported by "
            "the supplied evidence and analysis artifacts, even if it was eliminated."
        )
    )
    posterior_robustness: str = Field(
        default="robust",
        description="'robust' if the posterior is driven by a few decisive tests, "
        "'fragile' if driven by accumulation of many small effects that could individually go either way"
    )


class SynthesisResult(BaseModel):
    verdicts: list[HypothesisVerdict]
    comparative_analysis: str = Field(
        description="Concise, artifact-bound comparison of the hypotheses"
    )
    analytical_narrative: str = Field(
        description=(
            "Evidence-bound analytical narrative whose length follows the findings, "
            "including a concise indeterminate result when warranted"
        )
    )
    rank_stability: RankStability = Field(
        default="not_assessed",
        description=(
            "Deterministic interpretation of the leading hypothesis's sensitivity row. "
            "Fresh synthesis producers must copy the pipeline-supplied value exactly."
        ),
    )
    limitations: list[str]
    suggested_further_tests: list[str]


class CentralClaimEntailment(BaseModel):
    """One source-bounded judgment of a central final claim."""

    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    target_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    claim_text: str = Field(min_length=12)
    source_field: Literal[
        "mechanism_established",
        "mechanism_unresolved",
        "verdict_reasoning",
        "comparative_analysis",
        "analytical_narrative",
    ]
    disposition: Literal["entailed", "overstated", "unsupported"]
    support_basis: Literal["source_evidence", "pipeline_artifact"] = Field(
        description="Whether the proposition is supported by an accepted source observation or a supplied deterministic analysis artifact."
    )
    evidence_ids: list[str] = Field(
        default_factory=list,
    )
    artifact_locators: list["ArtifactLocator"] = Field(
        default_factory=list,
    )
    artifact_refs: list[
        Literal[
            "hypothesis_space",
            "absence",
            "testing",
            "bayesian",
            "diagnostic_matrix",
            "discriminator_audit_resolution",
            "mechanism_trace",
            "synthesis",
        ]
    ] = Field(  # type: ignore[assignment]
        default_factory=list,
    )
    reasoning: str = Field(min_length=12)

    @model_validator(mode="after")
    def _require_evidence_for_entailment(self) -> "CentralClaimEntailment":
        if self.disposition == "entailed":
            if self.support_basis == "source_evidence" and not self.evidence_ids:
                raise ValueError("source-evidence entailment requires evidence IDs")
            if self.support_basis == "pipeline_artifact" and not self.artifact_refs:
                raise ValueError("pipeline-artifact entailment requires artifact refs")
            if self.support_basis == "pipeline_artifact" and not self.artifact_locators:
                raise ValueError("pipeline-artifact entailment requires artifact locators")
        if len(self.evidence_ids) != len(set(self.evidence_ids)):
            raise ValueError("central claim duplicates evidence IDs")
        if len(self.artifact_refs) != len(set(self.artifact_refs)):
            raise ValueError("central claim duplicates artifact refs")
        locator_identities = [
            (locator.artifact_ref, locator.json_pointer)
            for locator in self.artifact_locators
        ]
        if len(locator_identities) != len(set(locator_identities)):
            raise ValueError("central claim duplicates artifact locators")
        if self.support_basis == "source_evidence" and self.artifact_refs:
            raise ValueError("source-evidence claim cannot carry artifact refs")
        if self.support_basis == "source_evidence" and self.artifact_locators:
            raise ValueError("source-evidence claim cannot carry artifact locators")
        return self


class ArtifactLocator(BaseModel):
    """One exact JSON Pointer into a supplied deterministic artifact."""

    model_config = ConfigDict(extra="forbid")

    artifact_ref: Literal[
        "hypothesis_space", "absence", "testing", "bayesian", "diagnostic_matrix",
        "discriminator_audit_resolution", "mechanism_trace", "synthesis",
    ]
    json_pointer: str = Field(pattern=r"^/(?:[^~/]|~[01])+(?:/(?:[^~/]|~[01])+)*$")


class CentralClaimInventoryItem(BaseModel):
    """One proposition decomposed from a deterministic final-prose target."""

    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    target_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    claim_text: str = Field(min_length=12)
    source_field: Literal["mechanism_established", "mechanism_unresolved", "verdict_reasoning", "comparative_analysis", "analytical_narrative"]
    target_start: int = Field(ge=0)
    target_end: int = Field(gt=0)
    covered_text: str = Field(min_length=1)

    @model_validator(mode="after")
    def _claim_is_the_covered_final_prose(self) -> "CentralClaimInventoryItem":
        """Prevent an inventory from substituting a new proposition for final prose."""

        if self.claim_text != self.covered_text:
            raise ValueError(
                "central claim inventory claim_text must exactly equal covered_text"
            )
        return self


class CentralClaimInventory(BaseModel):
    """Compact, target-scoped claim decomposition before provenance review."""

    model_config = ConfigDict(extra="forbid")

    claims: list[CentralClaimInventoryItem] = Field(min_length=1)


class CentralClaimReviewTargetManifest(BaseModel):
    """Self-contained provenance for one deterministic final-prose target."""

    model_config = ConfigDict(extra="forbid")

    target_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    source_field: Literal["mechanism_established", "mechanism_unresolved", "verdict_reasoning", "comparative_analysis", "analytical_narrative"]
    target_text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    inventory_input_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    review_input_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    inventory: CentralClaimInventory
    judgment_origin: Literal["fresh", "carried_forward"] = "fresh"
    dependency_sha256: Optional[str] = Field(
        default=None, pattern=r"^[0-9a-f]{64}$"
    )
    source_review_sha256: Optional[str] = Field(
        default=None, pattern=r"^[0-9a-f]{64}$"
    )
    source_review_input_sha256: Optional[str] = Field(
        default=None, pattern=r"^[0-9a-f]{64}$"
    )

    @model_validator(mode="after")
    def _require_carry_forward_lineage(self) -> "CentralClaimReviewTargetManifest":
        if self.judgment_origin == "carried_forward":
            if not self.dependency_sha256:
                raise ValueError("carried-forward review target requires dependency hash")
            if not self.source_review_sha256 or not self.source_review_input_sha256:
                raise ValueError("carried-forward review target requires source review lineage")
        elif self.source_review_sha256 or self.source_review_input_sha256:
            raise ValueError("fresh review target cannot claim carry-forward lineage")
        return self


class CentralClaimReviewManifest(BaseModel):
    """Replayable terminal-review lineage retained with a published result."""

    model_config = ConfigDict(extra="forbid")

    contract_version: Literal["v4", "v5", "v6"]
    inventory_prompt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    review_prompt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    targets: list[CentralClaimReviewTargetManifest] = Field(min_length=1)


class CentralClaimEntailmentReview(BaseModel):
    """Terminal source-span review of final mechanism and synthesis prose."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["accepted", "blocked"]
    claims: list[CentralClaimEntailment] = Field(min_length=1)
    overall_assessment: str = Field(min_length=20)
    manifest: CentralClaimReviewManifest | None = None

    @model_validator(mode="after")
    def _status_matches_claims(self) -> "CentralClaimEntailmentReview":
        claim_keys = {
            (claim.target_id, claim.claim_id)
            for claim in self.claims
        }
        if len(claim_keys) != len(self.claims):
            raise ValueError("central claim review duplicates target-scoped claim IDs")
        has_failure = any(
            claim.disposition in {"overstated", "unsupported"}
            for claim in self.claims
        )
        if self.status == "accepted" and has_failure:
            raise ValueError("accepted central claim review contains failed claims")
        if self.status == "blocked" and not has_failure:
            raise ValueError("blocked central claim review requires a failed claim")
        return self


class CentralClaimEntailmentForSynthesis(CentralClaimEntailment):
    """Central claim whose target is synthesis prose, excluding self-support."""

    artifact_refs: list[
        Literal[
            "hypothesis_space",
            "absence",
            "bayesian",
            "diagnostic_matrix",
            "testing",
            "discriminator_audit_resolution",
            "mechanism_trace",
        ]
    ] = Field(  # type: ignore[assignment]
        default_factory=list,
    )


class CentralClaimEntailmentReviewForSynthesis(CentralClaimEntailmentReview):
    """LLM-facing synthesis-target review without the circular artifact option."""

    claims: list[CentralClaimEntailmentForSynthesis] = Field(min_length=1)  # type: ignore[assignment]


class CentralClaimEntailmentForMechanism(CentralClaimEntailment):
    """Mechanism claim that must be directly grounded in accepted evidence."""

    support_basis: Literal["source_evidence"] = "source_evidence"
    artifact_refs: list[str] = Field(default_factory=list, max_length=0)  # type: ignore[assignment]
    artifact_locators: list[ArtifactLocator] = Field(default_factory=list, max_length=0)


class CentralClaimEntailmentReviewForMechanism(CentralClaimEntailmentReview):
    """LLM-facing mechanism-target review without the circular artifact option."""

    claims: list[CentralClaimEntailmentForMechanism] = Field(min_length=1)  # type: ignore[assignment]


class TerminalRepairDirective(BaseModel):
    """One target-scoped correction copied from a blocked terminal review."""

    model_config = ConfigDict(extra="forbid")

    target_kind: Literal["stage", "transition", "synthesis"]
    target_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    accepted_statement: str = Field(min_length=12)
    forbidden_statement: str = Field(min_length=12)
    required_disposition: str = Field(min_length=12)
    evidence_ids: list[str] = Field(default_factory=list)
    prediction_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _require_unique_references(self) -> "TerminalRepairDirective":
        if len(self.evidence_ids) != len(set(self.evidence_ids)):
            raise ValueError("terminal repair directive duplicates evidence IDs")
        if len(self.prediction_ids) != len(set(self.prediction_ids)):
            raise ValueError("terminal repair directive duplicates prediction IDs")
        return self


class TerminalRepairPlan(BaseModel):
    """Complete typed constraint set for one bounded terminal replacement."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["terminal-repair-plan-v1"] = "terminal-repair-plan-v1"
    directives: list[TerminalRepairDirective] = Field(min_length=1)

    @model_validator(mode="after")
    def _require_distinct_directives(self) -> "TerminalRepairPlan":
        identities = [
            (
                directive.target_kind,
                directive.target_id,
                directive.forbidden_statement.casefold(),
            )
            for directive in self.directives
        ]
        if len(identities) != len(set(identities)):
            raise ValueError("terminal repair plan duplicates a target constraint")
        return self


class TerminalProsePatchOperation(BaseModel):
    """One hash-bound replacement of an exact terminal prose target."""

    model_config = ConfigDict(extra="forbid")

    target_kind: Literal["stage", "transition", "synthesis"]
    target_id: str = Field(pattern=r"^[A-Za-z0-9_-]+$")
    source_field: Literal[
        "mechanism_established",
        "mechanism_unresolved",
        "verdict_reasoning",
        "comparative_analysis",
        "analytical_narrative",
    ]
    expected_text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    directive_sha256s: list[str] = Field(min_length=1)
    replacement_text: str = Field(min_length=8)

    @model_validator(mode="after")
    def _require_valid_replacement(self) -> "TerminalProsePatchOperation":
        if not self.replacement_text.strip():
            raise ValueError("terminal prose replacement must not be blank")
        if len(self.directive_sha256s) != len(set(self.directive_sha256s)):
            raise ValueError("terminal prose operation duplicates directive hashes")
        if any(
            not re.fullmatch(r"[0-9a-f]{64}", item)
            for item in self.directive_sha256s
        ):
            raise ValueError("terminal prose operation has an invalid directive hash")
        if any(
            ord(character) < 32 and character not in "\n\r\t"
            for character in self.replacement_text
        ):
            raise ValueError(
                "terminal prose replacement contains an invalid control character"
            )
        return self


class TerminalProsePatch(BaseModel):
    """A complete target-only repair for one exact blocked terminal result."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["terminal-prose-patch-v1"] = "terminal-prose-patch-v1"
    base_mechanism_trace_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    base_synthesis_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_repair_plan_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    operations: list[TerminalProsePatchOperation] = Field(min_length=1)

    @model_validator(mode="after")
    def _require_unique_targets(self) -> "TerminalProsePatch":
        targets = [
            (operation.target_kind, operation.target_id)
            for operation in self.operations
        ]
        if len(targets) != len(set(targets)):
            raise ValueError("terminal prose patch duplicates a target")
        directive_hashes = [
            item
            for operation in self.operations
            for item in operation.directive_sha256s
        ]
        if len(directive_hashes) != len(set(directive_hashes)):
            raise ValueError("terminal prose patch reuses a directive hash")
        return self


# ── Structural Critic (Pass 3.7) ────────────────────────────────────

CriticFindingType = Literal[
    "confound",          # a third variable explains both cause and effect
    "missing_pathway",   # a causal mechanism missing from the extraction
    "void_link",         # a causal edge with no evidentiary support in the matrix
    "too_strong_claim",  # a diagnostic type not justified by the justification text
    "confirmed_link",    # a well-supported causal link worth explicitly affirming
]


class CriticFinding(BaseModel):
    finding_type: CriticFindingType
    target: str = Field(
        description="ID of the evidence item, hypothesis, or causal edge (format: 'src_id->tgt_id') "
        "this finding refers to. Use an exact ID from the input data."
    )
    target_type: Literal["evidence", "hypothesis", "causal_edge"] = Field(
        description="'evidence' for an evidence_id, 'hypothesis' for a hypothesis_id, "
        "'causal_edge' for a 'src_id->tgt_id' edge string."
    )
    severity: Literal["high", "medium", "low"] = Field(
        description="'high' if this likely distorts posterior rankings; 'medium' if worth correcting; "
        "'low' if informational only."
    )
    reasoning: str = Field(description="Why this is a structural problem and what supports the concern.")
    recommendation: str = Field(
        description="Structural action only: collect specific evidence, add/remove a graph edge, "
        "merge hypotheses, or downgrade a diagnostic label. Do NOT suggest specific likelihood values."
    )

    @model_validator(mode="after")
    def _validate_target_consistency(self) -> "CriticFinding":
        if self.target_type == "hypothesis" and "->" in self.target:
            raise ValueError(
                f"target '{self.target}' contains '->' but target_type='hypothesis'. "
                "Use target_type='causal_edge' for edge targets, or split into separate "
                "hypothesis findings."
            )
        if self.target_type == "causal_edge":
            count = self.target.count("->")
            if count == 0:
                raise ValueError(
                    f"target '{self.target}' has no '->' but target_type='causal_edge'. "
                    "Causal edge targets must use format 'source_id->target_id'."
                )
            if count > 1:
                raise ValueError(
                    f"target '{self.target}' contains {count} '->' tokens but causal_edge "
                    "targets must reference exactly one edge: 'source_id->target_id'. "
                    "Multi-hop chains are not valid — create separate findings for each edge."
                )
        return self


class CriticResult(BaseModel):
    findings: list[CriticFinding] = []
    summary: str = Field(description="2-3 sentence overall structural assessment.")
    re_elicitation_needed: bool = Field(
        default=False,
        description="Computed post-parse: True if any finding has severity='high'. "
        "Do not set this field — it is derived automatically.",
    )

    @model_validator(mode="after")
    def _compute_re_elicitation(self) -> "CriticResult":
        """re_elicitation_needed is deterministic: any high-severity finding triggers a re-run."""
        self.re_elicitation_needed = any(f.severity == "high" for f in self.findings)
        return self


class CriticDelta(BaseModel):
    """Per-hypothesis posterior change between base and critic runs."""
    hypothesis_id: str
    posterior_base: float
    posterior_critic: float
    delta: float = Field(description="posterior_critic - posterior_base")
    top_driver_change: list[str] = Field(
        default_factory=list,
        description="Evidence IDs added or removed from top drivers between runs.",
    )
    critic_findings_count: int = Field(
        default=0,
        description="Number of critic findings targeting this hypothesis or its evidence.",
    )


# ── Combined Result ─────────────────────────────────────────────────

class LLMClientRuntimeBinding(BaseModel):
    """Observed shared-client provenance for one governed live run."""

    model_config = ConfigDict(extra="forbid")

    package: str = Field(description="Imported package name.")
    expected_revision: str = Field(
        pattern=r"^[0-9a-f]{40}$",
        description="Exact revision selected by the project runtime manifest.",
    )
    actual_revision: str = Field(
        pattern=r"^[0-9a-f]{40}$",
        description="Git revision observed for the imported package.",
    )
    imported_file: str = Field(description="Resolved imported package file.")
    git_root: str = Field(description="Observed package Git worktree root.")
    tracked_worktree_clean: bool = Field(
        description="Whether tracked package files were unchanged."
    )
    manifest_path: str = Field(description="Resolved runtime manifest path.")
    manifest_sha256: str = Field(
        pattern=r"^[0-9a-f]{64}$",
        description="Digest of the exact manifest used for validation.",
    )

class ProcessTracingResult(BaseModel):
    llm_client_runtime: Optional[LLMClientRuntimeBinding] = Field(
        default=None,
        description=(
            "Exact imported shared-client provenance for governed runs. "
            "Optional only for legacy and deterministic test artifacts."
        ),
    )
    llm_timeout_seconds: Optional[int] = Field(
        default=None,
        gt=0,
        description=(
            "Per-call shared-client hard deadline for governed runs. "
            "Optional only for legacy and deterministic test artifacts."
        ),
    )
    source_text_sha256: Optional[str] = Field(
        default=None,
        description="SHA-256 of the exact input text used for this analysis",
    )
    extraction: ExtractionResult
    hypothesis_space: HypothesisSpace
    inference_design: Optional[InferenceDesign] = Field(
        default=None,
        description="Pre-analysis corpus-exposure and evidence-role contract.",
    )
    segmented_source: Optional[SegmentedSourceSummary] = Field(
        default=None,
        description=(
            "Validated producer and partition lineage when Pass 1 used "
            "producer-owned extraction work units."
        ),
    )
    hypothesis_generation_view: Optional[HypothesisGenerationView] = Field(
        default=None,
        description="Exact evidence exposure recorded at hypothesis formulation.",
    )
    inference_status: InferenceStatus = Field(
        default="legacy_unclassified",
        description="Claim ceiling implied by exposure and post-selection lineage.",
    )
    post_selection_evidence_ids: list[str] = Field(
        default_factory=list,
        description=(
            "Evidence exposed to a material same-corpus refinement and therefore "
            "neutralized in any refined numerical update."
        ),
    )
    prior_specification: Optional[PriorSpecification] = Field(
        default=None,
        description=(
            "Declared prior weights and their provenance. Required for new pipeline results; "
            "optional only so legacy result files can be parsed and rejected with a clear message."
        ),
    )
    testing: TestingResult
    effective_testing: Optional[TestingResult] = Field(
        default=None,
        description=(
            "Separately audited likelihood vectors consumed by updating and reporting. "
            "None only for legacy artifacts whose testing vectors predate semantic audit."
        ),
    )

    @property
    def audited_testing(self) -> TestingResult:
        """Likelihood artifact authorized for inference and public interpretation."""

        return self.effective_testing or self.testing
    mechanism_trace: Optional[MechanismTraceResult] = Field(
        default=None,
        description=(
            "Temporal stage-and-edge assessment for fresh runs. None is retained "
            "only for legacy artifacts produced before the mechanism pass."
        ),
    )
    mechanism_audit_resolution: Optional[MechanismAuditResolution] = Field(
        default=None,
        description=(
            "Independent stage/edge semantic audit bound to the final mechanism "
            "trace. Optional only for legacy artifacts."
        ),
    )
    absence: AbsenceResult
    bayesian: BayesianResult
    synthesis: SynthesisResult
    central_claim_review: Optional[CentralClaimEntailmentReview] = Field(
        default=None,
        description="Terminal source-span entailment review of central final claims.",
    )
    terminal_repair_initial_review: Optional[CentralClaimEntailmentReview] = Field(
        default=None,
        description="Exact blocked review that authorized one terminal replacement.",
    )
    terminal_repair_plan: Optional[TerminalRepairPlan] = Field(
        default=None,
        description="Typed constraints applied to the bounded terminal replacement.",
    )
    source_packet: Optional[SourcePacketSummary] = Field(
        default=None,
        description="Source-packet metadata governing source scope and observability assumptions.",
    )
    source_coverage: Optional[SourceCoverageReport] = Field(
        default=None,
        description="Deterministic packet-source coverage against input text and extracted evidence.",
    )
    partition_audit: Optional[PartitionAudit] = Field(
        default=None,
        description="Pass 2.5: Hypothesis partition audit — flags overlap, complementarity, and absorptive risks before testing.",
    )
    partition_resolution: Optional[PartitionResolution] = Field(
        default=None,
        description="Complete partition audit/repair history and final gate status.",
    )
    discriminator_audit_resolution: Optional[DiscriminatorAuditResolution] = Field(
        default=None,
        description=(
            "Independent mode-scoped semantic audit of every non-equal evidence-by-rival "
            "comparison. Required for fresh results; optional only so "
            "legacy result files remain parseable and can be rejected explicitly."
        ),
    )
    diagnostic_matrix: Optional[DiagnosticMatrix] = Field(
        default=None,
        description="Pass 3.6: Diagnostic test matrix — which evidence items discriminate each rival pair, derived deterministically from likelihood vectors.",
    )
    refinement: Optional[RefinementResult] = None
    is_refined: bool = False
    refinement_status: RefinementStatus = "not_requested"
    critic: Optional[CriticResult] = Field(
        default=None,
        description="Pass 3.7: Structural critic findings — confounds, missing pathways, void links, "
        "too-strong claims, and confirmed links. Populated only when --critic flag is active.",
    )
