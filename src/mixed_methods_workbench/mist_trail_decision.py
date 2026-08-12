"""Typed, source-bound Mist Trail policy-decision development fixture.

The fixture tests whether empirical consequences and human value judgments can
produce a reviewable conditional conclusion without a hidden aggregate score.
It is not an NPS decision, NEPA analysis, or generic decision-engine contract.
"""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

FIXTURE_ROOT = Path(__file__).resolve().parents[2] / "examples" / "fixtures" / "mist_trail_decision"
SOURCE_MANIFEST_PATH = FIXTURE_ROOT / "source_manifest.json"
DECISION_PACKET_PATH = FIXTURE_ROOT / "decision_packet.json"
EXPECTED_EA_SHA256 = "df5304a9116b9dc2093e1f5e2eee61b61adab3c6f65ac8214aca7e685c23cbb0"


class DecisionModel(BaseModel):
    """Reject undeclared fixture fields and accidental mutation."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class CustodyStatus(StrEnum):
    """State whether exact source content is locally available and verified."""

    METADATA_ONLY = "metadata_only"
    HASH_VERIFIED_BYTES = "hash_verified_bytes"


class PassageStatus(StrEnum):
    """Whether exact text may be rendered from the local fixture."""

    PASSAGE_UNAVAILABLE = "passage_unavailable"
    HASH_VERIFIED = "hash_verified"


class Direction(StrEnum):
    """Source-bounded consequence direction without a numeric scale."""

    BENEFIT = "benefit"
    HARM = "harm"
    MIXED = "mixed"
    NEGLIGIBLE = "negligible"
    UNKNOWN = "unknown"


class TimeHorizon(StrEnum):
    """Time scope of one consequence."""

    CONSTRUCTION = "construction"
    LONG_TERM = "long_term"
    BOTH = "both"
    UNSPECIFIED = "unspecified"


class ReviewState(StrEnum):
    """Human review state for a fixture assertion or judgment."""

    REVIEWED = "reviewed"
    UNRESOLVED = "unresolved"


class Importance(StrEnum):
    """Qualitative priority declared by a human, never a numeric weight."""

    LOWER = "lower"
    MATERIAL = "material"
    DECISIVE = "decisive"
    UNRESOLVED = "unresolved"


class JudgmentKind(StrEnum):
    """Keep empirical summaries distinct from normative appraisal choices."""

    FACTUAL = "factual"
    NORMATIVE = "normative"
    MIXED = "mixed"


class ConclusionState(StrEnum):
    """Truthful terminal states for the decision conclusion."""

    CONDITIONAL_RECOMMENDATION = "conditional_recommendation"
    UNRESOLVED = "unresolved"
    REFUSED = "refused"


class SensitivityStatus(StrEnum):
    """Why a conclusion is or is not stable across declared priorities."""

    VALUE_SENSITIVE = "value_sensitive"
    EVIDENCE_LIMITED = "evidence_limited"
    STABLE_ACROSS_DECLARED_LENSES = "stable_across_declared_lenses"


class SourceBinding(DecisionModel):
    """Identify one official source without importing unverified passage text."""

    source_id: str
    title: str
    url: str
    source_type: Literal["project_page", "document_record", "pdf"]
    retrieved_on: str
    byte_size: int | None = Field(default=None, gt=0)
    content_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    custody_status: CustodyStatus
    allowed_uses: list[str] = Field(min_length=1)
    excluded_inferences: list[str] = Field(min_length=1)


class SourceManifest(DecisionModel):
    """Freeze the exact public-source identities used by the development fixture."""

    schema_id: Literal["mist_trail.source_manifest"]
    schema_version: Literal["0.1.0"]
    artifact_status: Literal["development_fixture"]
    sources: list[SourceBinding] = Field(min_length=1)

    @model_validator(mode="after")
    def require_unique_sources(self) -> SourceManifest:
        if len(self.sources) != len({source.source_id for source in self.sources}):
            raise ValueError("source IDs must be unique")
        return self


class SourceAnchor(DecisionModel):
    """Point to a reviewed source window while passage bytes remain unavailable."""

    anchor_id: str
    source_id: str
    page_label: str | None = None
    section: str
    locator: str
    reviewed_summary: str
    passage_status: PassageStatus


class DecisionFrame(DecisionModel):
    """State the decision, authority, analyst role, and non-claims."""

    question: str
    purpose: str
    decision_authority: str
    analyst_role: str
    decision_status: str
    scope: str
    constraints: list[str]
    non_claims: list[str] = Field(min_length=1)


class CommonAction(DecisionModel):
    """Represent an official action shared by B and C without misattribution."""

    action_id: str
    wording: str
    applies_to_option_ids: list[str]
    source_anchor_ids: list[str] = Field(min_length=1)


class Option(DecisionModel):
    """Represent one official alternative and only its option-specific actions."""

    option_id: str
    label: str
    short_label: str
    option_kind: Literal["no_action", "action", "agency_proposed_action"]
    summary: str
    specific_actions: list[str]
    source_anchor_ids: list[str] = Field(min_length=1)


class Criterion(DecisionModel):
    """Separate an empirical comparison question from its value question."""

    criterion_id: str
    label: str
    empirical_question: str
    value_question: str
    source_basis: str


class AffectedInterest(DecisionModel):
    """Name an affected interest without inferring an unsupported preference."""

    interest_id: str
    label: str
    supported_relationship: str
    preference_known: bool


class ConsequenceAssessment(DecisionModel):
    """Bind one option-criterion consequence to source windows and uncertainty."""

    assessment_id: str
    option_id: str
    criterion_id: str
    wording: str
    direction: Direction
    time_horizon: TimeHorizon
    affected_interest_ids: list[str] = Field(min_length=1)
    source_anchor_ids: list[str] = Field(min_length=1)
    source_analysis_method: str
    uncertainty: str
    mitigation_assumed: bool
    review_state: ReviewState


class CriterionJudgment(DecisionModel):
    """Record one demonstrative human priority separately from consequence evidence."""

    judgment_id: str
    criterion_id: str
    importance: Importance
    judgment_kind: JudgmentKind
    rationale: str
    author_role: str
    dissent_or_alternative: str
    change_condition: str


class PriorityLens(DecisionModel):
    """Show how a declared priority changes the conclusion without weights."""

    lens_id: str
    label: str
    priority_statement: str
    decisive_criterion_ids: list[str] = Field(min_length=1)
    result_state: ConclusionState
    preferred_option_id: str | None = None
    rationale: str

    @model_validator(mode="after")
    def align_result_and_option(self) -> PriorityLens:
        has_option = self.preferred_option_id is not None
        if (self.result_state == ConclusionState.CONDITIONAL_RECOMMENDATION) != has_option:
            raise ValueError("only a conditional recommendation may name a preferred option")
        return self


class TradeoffFinding(DecisionModel):
    """Preserve one choice that cannot be resolved without a value judgment."""

    tradeoff_id: str
    wording: str
    option_ids: list[str] = Field(min_length=2)
    assessment_ids: list[str] = Field(min_length=2)


class DecisionConclusion(DecisionModel):
    """State the bounded conclusion and every dependency that makes it conditional."""

    state: ConclusionState
    basis: Literal["workbench_appraisal"]
    headline: str
    recommended_option_id: str | None = None
    rationale: str
    decisive_assessment_ids: list[str] = Field(min_length=1)
    decisive_judgment_ids: list[str] = Field(min_length=1)
    sensitivity_statuses: list[SensitivityStatus] = Field(min_length=1)
    evidence_gaps: list[str]
    next_actions: list[str] = Field(min_length=1)
    non_claims: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def align_state_and_recommendation(self) -> DecisionConclusion:
        has_option = self.recommended_option_id is not None
        if (self.state == ConclusionState.CONDITIONAL_RECOMMENDATION) != has_option:
            raise ValueError("only a conditional recommendation may name a recommended option")
        return self


class ReviewEvent(DecisionModel):
    """Retain the human review disposition of the development artifact."""

    event_id: str
    event_type: Literal["proposed", "reviewed", "accepted", "rejected", "superseded"]
    actor_role: str
    recorded_on: str
    rationale: str


class DecisionPacket(DecisionModel):
    """Bind the complete fixture-local decision review into one immutable payload."""

    schema_id: Literal["mist_trail.decision_packet"]
    schema_version: Literal["0.1.0"]
    packet_id: Literal["mist-trail-decision-v1"]
    artifact_status: Literal["development_fixture"]
    source_manifest_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    frame: DecisionFrame
    source_anchors: list[SourceAnchor]
    common_actions: list[CommonAction]
    options: list[Option]
    criteria: list[Criterion]
    affected_interests: list[AffectedInterest]
    consequence_assessments: list[ConsequenceAssessment]
    criterion_judgments: list[CriterionJudgment]
    priority_lenses: list[PriorityLens]
    tradeoffs: list[TradeoffFinding]
    conclusion: DecisionConclusion
    review_events: list[ReviewEvent]

    @model_validator(mode="after")
    def validate_internal_references(self) -> DecisionPacket:
        def unique(items: list[Any], field: str, label: str) -> set[str]:
            values = [str(getattr(item, field)) for item in items]
            if len(values) != len(set(values)):
                raise ValueError(f"{label} IDs must be unique")
            return set(values)

        option_ids = unique(self.options, "option_id", "option")
        criterion_ids = unique(self.criteria, "criterion_id", "criterion")
        interest_ids = unique(self.affected_interests, "interest_id", "affected interest")
        anchor_ids = unique(self.source_anchors, "anchor_id", "source anchor")
        assessment_ids = unique(self.consequence_assessments, "assessment_id", "assessment")
        judgment_ids = unique(self.criterion_judgments, "judgment_id", "judgment")
        unique(self.common_actions, "action_id", "common action")
        unique(self.priority_lenses, "lens_id", "priority lens")
        unique(self.tradeoffs, "tradeoff_id", "tradeoff")
        unique(self.review_events, "event_id", "review event")

        if option_ids != {"A", "B", "C"}:
            raise ValueError("the fixture requires exactly official alternatives A, B, and C")
        option_kinds = {option.option_id: option.option_kind for option in self.options}
        if option_kinds != {"A": "no_action", "B": "action", "C": "agency_proposed_action"}:
            raise ValueError("official alternative kinds or agency preference were altered")
        for action in self.common_actions:
            if set(action.applies_to_option_ids) != {"B", "C"}:
                raise ValueError("every common action must apply to both B and C")
            if not set(action.source_anchor_ids) <= anchor_ids:
                raise ValueError("common action references an unknown source anchor")
        for option in self.options:
            if not set(option.source_anchor_ids) <= anchor_ids:
                raise ValueError("option references an unknown source anchor")
        expected_pairs = {
            (option_id, criterion_id) for option_id in option_ids for criterion_id in criterion_ids
        }
        observed_pairs = {
            (assessment.option_id, assessment.criterion_id)
            for assessment in self.consequence_assessments
        }
        if observed_pairs != expected_pairs or len(self.consequence_assessments) != len(
            expected_pairs
        ):
            raise ValueError(
                "the fixture requires exactly one assessment for every option-criterion pair"
            )
        for assessment in self.consequence_assessments:
            if (
                assessment.option_id not in option_ids
                or assessment.criterion_id not in criterion_ids
            ):
                raise ValueError("assessment references an unknown option or criterion")
            if not set(assessment.affected_interest_ids) <= interest_ids:
                raise ValueError("assessment references an unknown affected interest")
            if not set(assessment.source_anchor_ids) <= anchor_ids:
                raise ValueError("assessment references an unknown source anchor")
        if {judgment.criterion_id for judgment in self.criterion_judgments} != criterion_ids:
            raise ValueError("every criterion needs exactly one visible human judgment")
        if len(self.criterion_judgments) != len(criterion_ids):
            raise ValueError("every criterion needs exactly one visible human judgment")
        for lens in self.priority_lenses:
            if not set(lens.decisive_criterion_ids) <= criterion_ids:
                raise ValueError("priority lens references an unknown criterion")
            if lens.preferred_option_id is not None and lens.preferred_option_id not in option_ids:
                raise ValueError("priority lens references an unknown preferred option")
        for tradeoff in self.tradeoffs:
            if (
                not set(tradeoff.option_ids) <= option_ids
                or not set(tradeoff.assessment_ids) <= assessment_ids
            ):
                raise ValueError("tradeoff references an unknown option or assessment")
        if (
            self.conclusion.recommended_option_id is not None
            and self.conclusion.recommended_option_id not in option_ids
        ):
            raise ValueError("conclusion references an unknown recommended option")
        if not set(self.conclusion.decisive_assessment_ids) <= assessment_ids:
            raise ValueError("conclusion references an unknown decisive assessment")
        if not set(self.conclusion.decisive_judgment_ids) <= judgment_ids:
            raise ValueError("conclusion references an unknown decisive judgment")
        return self


class MistTrailDecisionArtifact(DecisionModel):
    """Return source custody and decision meaning through one browser/API object."""

    source_manifest: SourceManifest
    packet: DecisionPacket


def _load_json(path: Path) -> object:
    """Read one immutable fixture JSON file without a fallback path."""
    return json.loads(path.read_text(encoding="utf-8"))


def load_mist_trail_decision() -> MistTrailDecisionArtifact:
    """Load and cross-check the exact source manifest and decision packet."""
    manifest_bytes = SOURCE_MANIFEST_PATH.read_bytes()
    manifest = SourceManifest.model_validate(json.loads(manifest_bytes))
    packet = DecisionPacket.model_validate(_load_json(DECISION_PACKET_PATH))
    manifest_sha256 = hashlib.sha256(manifest_bytes).hexdigest()
    if packet.source_manifest_sha256 != manifest_sha256:
        raise ValueError("decision packet source-manifest hash does not match the fixture bytes")
    sources = {source.source_id: source for source in manifest.sources}
    if set(sources) != {"nps-project-page", "nps-document-record", "nps-draft-ea"}:
        raise ValueError("source manifest must contain the exact three approved NPS sources")
    draft_ea = sources["nps-draft-ea"]
    if draft_ea.content_sha256 != EXPECTED_EA_SHA256 or draft_ea.byte_size != 4_495_269:
        raise ValueError("the approved Draft EA identity or hash was altered")
    if any(anchor.source_id not in sources for anchor in packet.source_anchors):
        raise ValueError("source anchor references an unknown source")
    if any(
        anchor.passage_status != PassageStatus.PASSAGE_UNAVAILABLE
        for anchor in packet.source_anchors
    ):
        raise ValueError("exact passages cannot render without separately verified source bytes")
    return MistTrailDecisionArtifact(source_manifest=manifest, packet=packet)


def mist_trail_payload() -> dict[str, object]:
    """Return the exact JSON-compatible artifact used by the browser."""
    return load_mist_trail_decision().model_dump(mode="json")
