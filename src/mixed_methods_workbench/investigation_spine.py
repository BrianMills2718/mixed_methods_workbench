"""One bounded QC-to-Process-Tracing investigation shown as a cohesive journey."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

FIXTURE_ROOT = (
    Path(__file__).resolve().parents[2] / "examples" / "fixtures" / "investigation_spine"
)

EXPECTED_FIXTURE_DIGESTS = {
    "qualitative_explanation.json": "52e5a5bef8575b3b006c61bda6e2947858ff1c5d27a16c6fed9319130a5e0ce2",
    "independent_case_sources.json": "dc33be62aed976033d2ad5bf6a22456819649cfd7f02fab6857306d5165e2d8b",
    "process_tracing_return.json": "513be8d2718f2a5176a8d6d1be6074efe851f3cb9e04d6091453d4848e532a8e",
}


class InvestigationSpineError(ValueError):
    """Raised when the bounded cross-project journey cannot be trusted."""


class _ConsumerModel(BaseModel):
    """Compatible consumer: validate the fields this projection actually uses."""

    model_config = ConfigDict(extra="ignore")


class _OutputModel(BaseModel):
    """Strict Workbench-owned projection boundary."""

    model_config = ConfigDict(extra="forbid")


class ProducerRef(_ConsumerModel):
    repository: str
    revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    source_route: str
    proposition_id: Literal["P5"]
    proposition_version_id: Literal["p5-v1"]


class Proposition(_ConsumerModel):
    id: Literal["P5"]
    version_id: Literal["p5-v1"]
    authoritative_statement: str = Field(min_length=40)


class QualitativeExplanation(_ConsumerModel):
    schema_version: Literal["qc-p5-process-tracing-input/1"]
    research_question: str = Field(min_length=20)
    observation_unit: str = Field(min_length=10)
    proposition: Proposition
    producer: ProducerRef
    observable_implications: list[str] = Field(min_length=1)
    rival_explanations: list[str] = Field(min_length=1)
    excluded_inferences: list[str] = Field(min_length=1)


class SourceCandidate(_ConsumerModel):
    source_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_group: str = Field(min_length=1)
    source_kind: str = Field(min_length=1)
    locator: HttpUrl


class SourceGap(_ConsumerModel):
    missing_source_class: str = Field(min_length=1)
    why_it_matters: str = Field(min_length=1)
    expected_location: str = Field(min_length=1)
    priority: Literal["high", "medium", "low"]


class IndependentCaseSources(_ConsumerModel):
    case_name: str = Field(min_length=1)
    research_question: str = Field(min_length=20)
    focal_window: str = Field(min_length=1)
    outcome: str = Field(min_length=1)
    source_candidates: list[SourceCandidate] = Field(min_length=1)
    known_gaps: list[SourceGap] = Field(min_length=1)
    limitations: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def _unique_sources(self) -> IndependentCaseSources:
        source_ids = [item.source_id for item in self.source_candidates]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("independent case packet duplicates source IDs")
        return self


class ArtifactBinding(_ConsumerModel):
    artifact_id: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class TheoryTarget(_ConsumerModel):
    repository: Literal["qualitative_coding"]
    revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    theory_version: Literal["p5-v1"]
    proposition_id: Literal["P5"]
    authoritative_wording: str = Field(min_length=40)
    hypothesis_id: str = Field(min_length=1)


class CaseScope(_ConsumerModel):
    case_name: str
    research_question: str
    focal_window: str
    outcome: str
    selection_and_scope_limits: list[str] = Field(min_length=1)


class SourceSummary(_ConsumerModel):
    source_id: str
    title: str
    source_group: str
    source_kind: str
    status: str
    evidence_count: int = Field(ge=0)


class EvidenceAnchor(_ConsumerModel):
    evidence_id: str
    source_id: str


class EvidencePacket(_ConsumerModel):
    source_count: int = Field(ge=1)
    evidence_count: int = Field(ge=1)
    sources: list[SourceSummary] = Field(min_length=1)
    selected_evidence: list[EvidenceAnchor] = Field(min_length=1)
    high_priority_gaps: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def _validate_sources(self) -> EvidencePacket:
        source_ids = [item.source_id for item in self.sources]
        evidence_ids = [item.evidence_id for item in self.selected_evidence]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError("Process Tracing return duplicates source IDs")
        if len(evidence_ids) != len(set(evidence_ids)):
            raise ValueError("Process Tracing return duplicates evidence IDs")
        if self.source_count != len(self.sources):
            raise ValueError("Process Tracing source count does not match source rows")
        if {item.source_id for item in self.selected_evidence} - set(source_ids):
            raise ValueError("selected evidence references an unknown source")
        return self


class PublicationFailure(_ConsumerModel):
    claim_id: str
    claim_text: str
    reasoning: str


class PublicationGate(_ConsumerModel):
    status: Literal["accepted", "blocked"]
    public_conclusion_status: Literal["available", "withheld_pending_repair"]
    failed_claims: list[PublicationFailure]

    @model_validator(mode="after")
    def _coherent_gate(self) -> PublicationGate:
        if self.status == "blocked" and (
            self.public_conclusion_status != "withheld_pending_repair"
            or not self.failed_claims
        ):
            raise ValueError("blocked publication must remain withheld with a failed claim")
        if self.status == "accepted" and (
            self.public_conclusion_status != "available" or self.failed_claims
        ):
            raise ValueError("accepted publication gate has contradictory failure state")
        return self


class HypothesisAppraisal(_ConsumerModel):
    hypothesis_id: str
    is_theory_target: bool
    status: str


class MethodAppraisal(_ConsumerModel):
    theory_evidence_relationship: Literal["independent"]
    publication_gate: PublicationGate
    target_status: str
    hypothesis_appraisals: list[HypothesisAppraisal] = Field(min_length=1)
    rival_pairs_without_discriminators: list[tuple[str, str]]

    @model_validator(mode="after")
    def _single_target(self) -> MethodAppraisal:
        targets = [item for item in self.hypothesis_appraisals if item.is_theory_target]
        if len(targets) != 1 or targets[0].status != self.target_status:
            raise ValueError("method appraisal needs one target matching target_status")
        return self


class ReviewedFinding(_ConsumerModel):
    finding_id: str
    wording: str
    evidence_ids: list[str] = Field(min_length=1)


class UnresolvedQuestion(_ConsumerModel):
    question_id: str
    wording: str
    source_gap_labels: list[str]


class TheoryUpdate(_ConsumerModel):
    disposition: Literal[
        "retain_unconfirmed", "revision_required", "rejection_proposed", "withhold"
    ]
    headline: str
    summary: str
    findings: list[ReviewedFinding] = Field(min_length=1)
    unresolved: list[UnresolvedQuestion] = Field(min_length=1)
    excluded_inferences: list[str] = Field(min_length=1)


class ProcessTracingReturn(_ConsumerModel):
    schema_version: Literal["pt_theory_test_return_v1"]
    return_id: str
    producer_repository: Literal["process_tracing"]
    analysis_repository_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    result_artifact: ArtifactBinding
    central_review_artifact: ArtifactBinding
    theory_input_receipt_artifact: ArtifactBinding
    target: TheoryTarget
    case_scope: CaseScope
    evidence_packet: EvidencePacket
    method_appraisal: MethodAppraisal
    theory_update: TheoryUpdate


class ArtifactRef(_OutputModel):
    artifact_id: str
    object_identity: str
    title: str
    producer: str
    semantic_owner: str
    artifact_type: str
    schema_version: str | None
    content_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    producer_revision: str | None
    availability: Literal["embedded", "producer_retained_reference"]
    native_route: str | None
    custody_note: str


class JourneyStage(_OutputModel):
    number: int = Field(ge=1)
    title: str
    owner: str
    status: Literal["accepted_input", "new_evidence", "unresolved", "retained_unconfirmed"]
    question_answered: str
    outcome: str
    artifact_ids: list[str] = Field(min_length=1)


class EvidenceSourceView(_OutputModel):
    source_id: str
    source_url: HttpUrl
    title: str
    source_kind: str
    evidence_count: int


class EvidenceNeed(_OutputModel):
    label: str
    why_it_matters: str
    likely_location: str
    priority: Literal["high", "medium", "low"]


class InvestigationSpine(_OutputModel):
    schema_version: Literal["mmw.investigation_spine.p5.v1"]
    investigation_id: Literal["psychosisbank-disclosure-explanation"]
    title: str
    status: Literal["unresolved"]
    status_label: str
    research_question: str
    case_name: str
    focal_window: str
    observed_outcome: str
    plain_language_explanation: str
    result_headline: str
    result_summary: str
    journey: list[JourneyStage] = Field(min_length=4, max_length=4)
    sources: list[EvidenceSourceView] = Field(min_length=1)
    evidence_item_count: int = Field(ge=1)
    supported_findings: list[str] = Field(min_length=1)
    unresolved_questions: list[str] = Field(min_length=1)
    next_evidence: list[EvidenceNeed] = Field(min_length=1)
    publication_block_reason: str
    do_not_infer: list[str] = Field(min_length=1)
    artifact_refs: list[ArtifactRef] = Field(min_length=1)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _public_text(value: str) -> str:
    """Replace the bounded producer's internal proposition ID in reader-facing prose."""

    return value.replace("P5", "the disclosure-burden explanation")


def _read_pinned(root: Path, name: str) -> tuple[object, str]:
    path = root / name
    if not path.is_file():
        raise InvestigationSpineError(f"required investigation artifact is missing: {name}")
    observed = _sha256(path)
    expected = EXPECTED_FIXTURE_DIGESTS[name]
    if observed != expected:
        raise InvestigationSpineError(
            f"investigation artifact digest mismatch for {name}: expected {expected}, "
            f"observed {observed}"
        )
    try:
        return json.loads(path.read_text(encoding="utf-8")), observed
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise InvestigationSpineError(f"invalid JSON in investigation artifact: {name}") from exc


def load_investigation_spine(root: Path = FIXTURE_ROOT) -> InvestigationSpine:
    """Validate and project the exact completed P5 round trip without rerunning it."""

    try:
        explanation_raw, explanation_digest = _read_pinned(root, "qualitative_explanation.json")
        sources_raw, sources_digest = _read_pinned(root, "independent_case_sources.json")
        return_raw, return_digest = _read_pinned(root, "process_tracing_return.json")
        explanation = QualitativeExplanation.model_validate(explanation_raw)
        sources = IndependentCaseSources.model_validate(sources_raw)
        result = ProcessTracingReturn.model_validate(return_raw)
    except InvestigationSpineError:
        raise
    except (ValueError, TypeError) as exc:
        raise InvestigationSpineError(f"invalid investigation boundary: {exc}") from exc

    if explanation.research_question != sources.research_question:
        raise InvestigationSpineError("qualitative explanation and case packet questions disagree")
    if sources.research_question != result.case_scope.research_question:
        raise InvestigationSpineError("case packet and Process Tracing result questions disagree")
    if (
        sources.case_name != result.case_scope.case_name
        or sources.focal_window != result.case_scope.focal_window
        or sources.outcome != result.case_scope.outcome
    ):
        raise InvestigationSpineError("case identity changed across the Process Tracing boundary")
    if (
        explanation.proposition.id != result.target.proposition_id
        or explanation.proposition.version_id != result.target.theory_version
        or explanation.proposition.authoritative_statement != result.target.authoritative_wording
        or explanation.producer.revision != result.target.revision
    ):
        raise InvestigationSpineError("qualitative explanation identity changed during testing")

    packet_source_ids = {item.source_id for item in sources.source_candidates}
    result_source_ids = {item.source_id for item in result.evidence_packet.sources}
    if packet_source_ids != result_source_ids:
        raise InvestigationSpineError("Process Tracing result does not resolve the frozen source packet")

    selected_evidence_ids = {
        item.evidence_id for item in result.evidence_packet.selected_evidence
    }
    missing_evidence = {
        evidence_id
        for finding in result.theory_update.findings
        for evidence_id in finding.evidence_ids
        if evidence_id not in selected_evidence_ids
    }
    if missing_evidence:
        raise InvestigationSpineError("returned finding references unavailable selected evidence")

    gate = result.method_appraisal.publication_gate
    if (
        result.method_appraisal.target_status == "indeterminate"
        and result.theory_update.disposition != "retain_unconfirmed"
    ):
        raise InvestigationSpineError(
            "indeterminate Process Tracing result must retain the explanation unconfirmed"
        )
    if gate.status == "blocked" and result.theory_update.disposition in {
        "revision_required",
        "rejection_proposed",
    }:
        raise InvestigationSpineError(
            "publication-blocked Process Tracing result cannot force theory revision"
        )
    if gate.status != "blocked":
        raise InvestigationSpineError("this bounded journey requires its exact blocked result")

    source_gaps = {item.missing_source_class: item for item in sources.known_gaps}
    source_candidates = {item.source_id: item for item in sources.source_candidates}
    if set(result.evidence_packet.high_priority_gaps) - set(source_gaps):
        raise InvestigationSpineError("returned evidence need is absent from the source packet")

    embedded_refs = [
        ArtifactRef(
            artifact_id="qualitative-explanation",
            object_identity=(
                f"{explanation.proposition.id} / {explanation.proposition.version_id}"
            ),
            title="Frozen qualitative explanation",
            producer="process_tracing intake fixture",
            semantic_owner="qualitative_coding",
            artifact_type="qualitative_explanation_input",
            schema_version=explanation.schema_version,
            content_sha256=explanation_digest,
            producer_revision=explanation.producer.revision,
            availability="embedded",
            native_route=explanation.producer.source_route,
            custody_note="Exact producer-authored QC proposition frozen by Process Tracing before case appraisal.",
        ),
        ArtifactRef(
            artifact_id="independent-case-sources",
            object_identity=sources.case_name,
            title="PsychosisBank/TalkBank source packet",
            producer="process_tracing",
            semantic_owner="process_tracing",
            artifact_type="source_packet",
            schema_version=None,
            content_sha256=sources_digest,
            producer_revision=result.analysis_repository_revision,
            availability="embedded",
            native_route=None,
            custody_note="Exact three-source packet used for the bounded independent case appraisal.",
        ),
        ArtifactRef(
            artifact_id="process-tracing-return",
            object_identity=result.return_id,
            title="Publication-aware Process Tracing return",
            producer="process_tracing",
            semantic_owner="process_tracing",
            artifact_type="theory_test_return",
            schema_version=result.schema_version,
            content_sha256=return_digest,
            producer_revision=result.analysis_repository_revision,
            availability="embedded",
            native_route="/public/example/data/p5-theory-test-return",
            custody_note="Exact return bytes are identical in the pinned Process Tracing and QC fixtures.",
        ),
    ]
    retained_refs = [
        ArtifactRef(
            artifact_id=binding.artifact_id,
            object_identity=binding.artifact_id,
            title=title,
            producer="process_tracing",
            semantic_owner="process_tracing",
            artifact_type=artifact_type,
            schema_version=None,
            content_sha256=binding.sha256,
            producer_revision=result.analysis_repository_revision,
            availability="producer_retained_reference",
            native_route=None,
            custody_note="The producer return binds this artifact by ID and digest; its bytes are not copied into the Workbench.",
        )
        for binding, title, artifact_type in (
            (result.theory_input_receipt_artifact, "Theory input receipt", "theory_input_receipt"),
            (result.result_artifact, "Blocked prepublication result", "process_tracing_result"),
            (result.central_review_artifact, "Central claim review", "publication_review"),
        )
    ]

    failed_claim = gate.failed_claims[0]
    high_priority_needs = [source_gaps[label] for label in result.evidence_packet.high_priority_gaps]
    return InvestigationSpine(
        schema_version="mmw.investigation_spine.p5.v1",
        investigation_id="psychosisbank-disclosure-explanation",
        title="Why did PsychosisBank use controlled access?",
        status="unresolved",
        status_label="The new case was informative, but it did not settle the explanation.",
        research_question=result.case_scope.research_question,
        case_name=result.case_scope.case_name,
        focal_window=result.case_scope.focal_window,
        observed_outcome=result.case_scope.outcome,
        plain_language_explanation=explanation.proposition.authoritative_statement,
        result_headline="The evidence fits the explanation, but does not confirm it.",
        result_summary=_public_text(result.theory_update.summary),
        journey=[
            JourneyStage(
                number=1,
                title="Qualitative research proposed an explanation",
                owner="Qualitative Coding",
                status="accepted_input",
                question_answered="What explanation should be tested in a different case?",
                outcome=explanation.proposition.authoritative_statement,
                artifact_ids=["qualitative-explanation"],
            ),
            JourneyStage(
                number=2,
                title="A different case supplied new evidence",
                owner="Process Tracing",
                status="new_evidence",
                question_answered="What happened in a named project that was not used to create the explanation?",
                outcome=(
                    f"{result.evidence_packet.evidence_count} evidence items from "
                    f"{result.evidence_packet.source_count} sources documented relevant barriers, "
                    "response options, and the controlled-access outcome."
                ),
                artifact_ids=["independent-case-sources"],
            ),
            JourneyStage(
                number=3,
                title="Process Tracing compared competing explanations",
                owner="Process Tracing",
                status="unresolved",
                question_answered="Did burden-sensitive deliberation explain the choice better than rules or established routine?",
                outcome=_public_text(result.theory_update.summary),
                artifact_ids=["process-tracing-return", result.result_artifact.artifact_id],
            ),
            JourneyStage(
                number=4,
                title="The explanation stayed open",
                owner="Qualitative Coding",
                status="retained_unconfirmed",
                question_answered="What should happen to the original explanation now?",
                outcome=(
                    "Keep it as an unconfirmed candidate and collect the missing decision records; "
                    "do not treat the case as confirmation or rejection."
                ),
                artifact_ids=["process-tracing-return"],
            ),
        ],
        sources=[
            EvidenceSourceView(
                source_id=item.source_id,
                source_url=source_candidates[item.source_id].locator,
                title=item.title,
                source_kind=item.source_kind.replace("_", " "),
                evidence_count=item.evidence_count,
            )
            for item in result.evidence_packet.sources
        ],
        evidence_item_count=result.evidence_packet.evidence_count,
        supported_findings=[_public_text(item.wording) for item in result.theory_update.findings],
        unresolved_questions=[
            _public_text(item.wording) for item in result.theory_update.unresolved
        ],
        next_evidence=[
            EvidenceNeed(
                label=item.missing_source_class,
                why_it_matters=item.why_it_matters,
                likely_location=item.expected_location,
                priority=item.priority,
            )
            for item in high_priority_needs
        ],
        publication_block_reason=(
            f'The draft statement “{failed_claim.claim_text}” was withheld because '
            f"{failed_claim.reasoning}"
        ),
        do_not_infer=[_public_text(item) for item in result.theory_update.excluded_inferences],
        artifact_refs=embedded_refs + retained_refs,
    )


def investigation_spine_payload(root: Path = FIXTURE_ROOT) -> dict[str, object]:
    """Return the same typed projection consumed by the browser."""
    payload = load_investigation_spine(root).model_dump(mode="json")
    from .investigation_verification import RECEIPT_PATH, _case_inputs, load_verification

    receipt_path = root / RECEIPT_PATH.name
    if receipt_path.exists():
        payload["independent_verification"] = load_verification(root).model_dump(mode="json")
        _, excerpts = _case_inputs(root)
        payload["independent_verification_excerpts"] = [item.model_dump() for item in excerpts]
    else:
        payload["independent_verification"] = None
        payload["independent_verification_excerpts"] = []
    from .investigation_run import RECEIPT_NAME, RUN_ROOT, connected_run_payload

    payload["connected_run"] = (
        connected_run_payload()
        if root.resolve() == FIXTURE_ROOT.resolve() and (RUN_ROOT / RECEIPT_NAME).exists()
        else None
    )
    return payload
