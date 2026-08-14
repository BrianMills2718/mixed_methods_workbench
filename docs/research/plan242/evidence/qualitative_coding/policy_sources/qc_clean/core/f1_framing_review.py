"""Apply explicit coding review to an F1 candidate run and export the ledger.

Review decisions are separate from model proposals so an accepted or revised
observation is never inferred merely from successful structured generation.
The final bundle remains coding-level evidence; it does not claim scientific
review or a cross-document finding.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from qc_clean.core.f1_framing import (
    CandidateRecord,
    F1FramingObservationBundle,
    F1FunctionId,
    F1ResourceId,
    F1_FUNCTIONS,
    F1_RESOURCES,
    FramingObservation,
    MeasurementReview,
    MeasurementRunIdentity,
    ObservationStatus,
    REQUIRED_EXCLUDED_CLAIMS,
    StrictModel,
)
from qc_clean.core.f1_framing_runner import F1CandidateRunPackage

_SHA256_PATTERN = r"^[0-9a-f]{64}$"


class DecisionUniverseMismatchError(ValueError):
    """The exhaustive review decisions do not name the bound candidate universe."""


class CellReviewDecision(StrictModel):
    """Accept one candidate or replace its substantive coding fields explicitly."""

    candidate_id: str = Field(min_length=1)
    decision: Literal["accepted", "revised"]
    rationale: str = Field(min_length=1)
    final_status: ObservationStatus | None = None
    final_window_ids: list[str] | None = None
    final_rationale: str | None = None
    final_alternative_readings: list[str] | None = None
    final_uncertainty_notes: list[str] | None = None

    @model_validator(mode="after")
    def validate_revision_fields(self) -> "CellReviewDecision":
        """Require a complete replacement only when the reviewer revises a cell."""

        replacement = (
            self.final_status,
            self.final_window_ids,
            self.final_rationale,
            self.final_alternative_readings,
            self.final_uncertainty_notes,
        )
        if self.decision == "revised" and any(value is None for value in replacement):
            raise ValueError("revised decisions require every final coding field")
        if self.decision == "accepted" and any(value is not None for value in replacement):
            raise ValueError("accepted decisions cannot silently replace candidate fields")
        return self


class F1CodingReviewPackage(StrictModel):
    """Bind exhaustive coding review to one exact candidate-run file."""

    schema_version: Literal[1]
    review_id: str = Field(min_length=1)
    candidate_run_sha256: str = Field(pattern=_SHA256_PATTERN)
    reviewer_id: str = Field(min_length=1)
    reviewed_at: str = Field(min_length=1)
    coverage_reviewed_resource_ids: list[F1ResourceId]
    decisions: list[CellReviewDecision]
    raw_source_content_included: Literal[False]
    scientific_review_status: Literal["not_performed"]

    @model_validator(mode="after")
    def validate_review_denominator(self) -> "F1CodingReviewPackage":
        """Require exactly four coverage reviews and sixteen unique decisions."""

        if set(self.coverage_reviewed_resource_ids) != set(F1_RESOURCES):
            raise ValueError("review must cover all four F1 instruments")
        candidate_ids = [row.candidate_id for row in self.decisions]
        if len(candidate_ids) != 16 or len(set(candidate_ids)) != 16:
            raise ValueError("review must contain sixteen unique cell decisions")
        return self


def load_candidate_run(path: Path) -> F1CandidateRunPackage:
    """Load a strict content-free candidate package."""

    return F1CandidateRunPackage.model_validate_json(path.read_text(encoding="utf-8"))


def load_coding_review(path: Path) -> F1CodingReviewPackage:
    """Load a strict coding-review package."""

    return F1CodingReviewPackage.model_validate_json(path.read_text(encoding="utf-8"))


def finalize_f1_bundle(
    *,
    candidate_path: Path,
    review: F1CodingReviewPackage,
    bundle_id: str,
) -> F1FramingObservationBundle:
    """Join one exact candidate run with exhaustive explicit review decisions."""

    candidate_bytes = candidate_path.read_bytes()
    if hashlib.sha256(candidate_bytes).hexdigest() != review.candidate_run_sha256:
        raise ValueError("coding review does not bind the supplied candidate run")
    run = F1CandidateRunPackage.model_validate_json(candidate_bytes)
    candidate_by_id = {row.candidate_id: row for row in run.candidates}
    decision_by_id = {row.candidate_id: row for row in review.decisions}
    if set(candidate_by_id) != set(decision_by_id):
        raise DecisionUniverseMismatchError(
            "review decisions must match the complete candidate run"
        )

    records: list[CandidateRecord] = []
    observations: list[FramingObservation] = []
    for candidate in run.candidates:
        decision = decision_by_id[candidate.candidate_id]
        records.append(
            CandidateRecord(
                candidate_id=candidate.candidate_id,
                resource_id=candidate.resource_id,
                function_id=candidate.function_id,
                proposed_status=candidate.proposed_status,
                proposed_window_ids=candidate.proposed_window_ids,
                rationale=candidate.rationale,
                alternative_readings=candidate.alternative_readings,
                uncertainty_notes=candidate.uncertainty_notes,
                disposition=decision.decision,
            )
        )
        status = decision.final_status or candidate.proposed_status
        window_ids = (
            decision.final_window_ids
            if decision.final_window_ids is not None
            else candidate.proposed_window_ids
        )
        rationale = decision.final_rationale or candidate.rationale
        alternatives = (
            decision.final_alternative_readings
            if decision.final_alternative_readings is not None
            else candidate.alternative_readings
        )
        uncertainty = (
            decision.final_uncertainty_notes
            if decision.final_uncertainty_notes is not None
            else candidate.uncertainty_notes
        )
        observations.append(
            FramingObservation(
                observation_id=(
                    f"observation-{candidate.resource_id}-{candidate.function_id}"
                ),
                resource_id=candidate.resource_id,
                function_id=candidate.function_id,
                status=status,
                evidence_window_ids=window_ids,
                coverage_id=f"coverage-{candidate.resource_id}",
                rationale=rationale,
                alternative_readings=alternatives,
                uncertainty_notes=uncertainty,
                candidate_id=candidate.candidate_id,
                review=MeasurementReview(
                    decision=decision.decision,
                    reviewer_id=review.reviewer_id,
                    reviewed_at=review.reviewed_at,
                    rationale=decision.rationale,
                ),
            )
        )
    reviewed_coverage = [row.model_copy(update={"reviewed": True}) for row in run.coverage_records]
    return F1FramingObservationBundle(
        schema_version=1,
        bundle_id=bundle_id,
        run=MeasurementRunIdentity(
            run_id=run.run_id,
            packet_id=run.packet_id,
            packet_sha256=run.packet_sha256,
            study_id=run.study_id,
            study_specification_sha256=run.study_specification_sha256,
            theory_artifact_id=run.theory_artifact_id,
            theory_artifact_sha256=run.theory_artifact_sha256,
            prompt_sha256=run.prompt_sha256,
            requested_model=run.requested_model,
            execution_models=run.execution_models,
            configuration_id=run.configuration_id,
            code_commit=run.code_commit,
            trace_id=run.trace_id,
            max_budget_usd=run.max_budget_usd,
            cash_cost_usd=run.cash_cost_usd,
            input_tokens=run.input_tokens,
            output_tokens=run.output_tokens,
            started_at=run.started_at,
            completed_at=run.completed_at,
        ),
        window_registry=run.window_registry,
        coverage_records=reviewed_coverage,
        candidate_records=records,
        observations=observations,
        excluded_claims=sorted(REQUIRED_EXCLUDED_CLAIMS),
        raw_source_content_included=False,
        scientific_review_status="not_performed",
    )
