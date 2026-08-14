"""Strict contracts for the F1 source-bound framing measurement seam.

This module owns document-by-function observations and their coding review.  It
does not own Entman theory semantics, source bytes, cross-document comparison,
or scientific findings.  The fixed 4×4 denominator is intentional: missing
model output can never be reinterpreted as an absent framing function.
"""

from __future__ import annotations

import hashlib
import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

F1ResourceId = Literal[
    "odni-2024-08-19-joint",
    "odni-2024-09-18-joint",
    "doj-2024-09-26-indictment",
    "treasury-2024-09-27-sanctions",
]
F1FunctionId = Literal[
    "problem_definition",
    "causal_diagnosis",
    "moral_evaluation",
    "treatment_recommendation",
]
ObservationStatus = Literal["present", "absent", "ambiguous", "not_observable"]

F1_RESOURCES: tuple[F1ResourceId, ...] = (
    "odni-2024-08-19-joint",
    "odni-2024-09-18-joint",
    "doj-2024-09-26-indictment",
    "treasury-2024-09-27-sanctions",
)
F1_FUNCTIONS: tuple[F1FunctionId, ...] = (
    "problem_definition",
    "causal_diagnosis",
    "moral_evaluation",
    "treatment_recommendation",
)
REQUIRED_EXCLUDED_CLAIMS = frozenset(
    {
        "agency effects",
        "audience effects",
        "communicator intent",
        "truth of allegations",
        "prevalence",
    }
)

_SHA256_PATTERN = r"^[0-9a-f]{64}$"
_COMMIT_PATTERN = r"^[0-9a-f]{40}$"


def window_denominator_sha256(window_ids: list[str]) -> str:
    """Hash the sorted exact window-ID denominator for one instrument."""

    encoded = json.dumps(sorted(window_ids), separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


class StrictModel(BaseModel):
    """Fail on undeclared producer fields."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class MeasurementRunIdentity(StrictModel):
    """Bind the output to exact method, source, code, model, and trace inputs."""

    run_id: str = Field(min_length=1)
    packet_id: Literal["css-s0-iran-election-2024-framing-v3-frozen-1"]
    packet_sha256: str = Field(pattern=_SHA256_PATTERN)
    study_id: Literal["css-iran-election-2024-framing"]
    study_specification_sha256: str = Field(pattern=_SHA256_PATTERN)
    theory_artifact_id: Literal["tf-op-framing-theory-entman-1993-f1-v1"]
    theory_artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    prompt_sha256: str = Field(pattern=_SHA256_PATTERN)
    requested_model: str = Field(min_length=1)
    execution_models: list[str] = Field(min_length=1)
    configuration_id: Literal["f1-framing-config-v1"]
    code_commit: str = Field(pattern=_COMMIT_PATTERN)
    trace_id: str = Field(min_length=1)
    max_budget_usd: float = Field(gt=0)
    cash_cost_usd: float = Field(ge=0)
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    started_at: str = Field(min_length=1)
    completed_at: str = Field(min_length=1)


class SourceWindowRef(StrictModel):
    """Carry one exact evidence-window identity without copying its text."""

    window_id: str = Field(min_length=1)
    resource_id: F1ResourceId
    source_artifact_version_id: str = Field(min_length=1)
    source_artifact_sha256: str = Field(pattern=_SHA256_PATTERN)
    source_view_version_id: str = Field(min_length=1)
    source_view_sha256: str = Field(pattern=_SHA256_PATTERN)
    extracted_text_sha256: str = Field(pattern=_SHA256_PATTERN)
    review_status: Literal["verified_derived_text", "unreviewed_ocr"]


class SearchCoverageRecord(StrictModel):
    """Prove what was examined before an absence judgment is allowed."""

    coverage_id: str = Field(min_length=1)
    resource_id: F1ResourceId
    examined_window_ids: list[str] = Field(min_length=1)
    denominator_count: int = Field(gt=0)
    denominator_sha256: str = Field(pattern=_SHA256_PATTERN)
    search_strategy: Literal[
        "exhaustive_window_review", "custody_constraint_review"
    ]
    reviewed: bool

    @model_validator(mode="after")
    def validate_denominator(self) -> "SearchCoverageRecord":
        """Require count and digest to match the declared examined windows."""

        if len(self.examined_window_ids) != len(set(self.examined_window_ids)):
            raise ValueError("examined window IDs must be unique")
        if self.denominator_count != len(self.examined_window_ids):
            raise ValueError("denominator_count must match examined_window_ids")
        if self.denominator_sha256 != window_denominator_sha256(self.examined_window_ids):
            raise ValueError("denominator_sha256 must bind the exact window IDs")
        return self


class CandidateRecord(StrictModel):
    """Preserve one model coding proposal before review or revision."""

    candidate_id: str = Field(min_length=1)
    resource_id: F1ResourceId
    function_id: F1FunctionId
    proposed_status: ObservationStatus
    proposed_window_ids: list[str]
    rationale: str = Field(min_length=1)
    alternative_readings: list[str]
    uncertainty_notes: list[str]
    disposition: Literal["accepted", "revised", "rejected"]


class MeasurementReview(StrictModel):
    """Record the coding-level review decision without claiming scientific approval."""

    decision: Literal["accepted", "revised"]
    reviewer_id: str = Field(min_length=1)
    reviewed_at: str = Field(min_length=1)
    rationale: str = Field(min_length=1)


class FramingObservation(StrictModel):
    """Own one reviewed document-by-function measurement cell."""

    observation_id: str = Field(min_length=1)
    resource_id: F1ResourceId
    function_id: F1FunctionId
    status: ObservationStatus
    evidence_window_ids: list[str]
    coverage_id: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    alternative_readings: list[str]
    uncertainty_notes: list[str]
    candidate_id: str = Field(min_length=1)
    review: MeasurementReview

    @model_validator(mode="after")
    def validate_status_evidence(self) -> "FramingObservation":
        """Keep positive, ambiguous, absent, and unobservable states distinct."""

        if self.status in {"present", "ambiguous"} and not self.evidence_window_ids:
            raise ValueError("present and ambiguous observations require evidence windows")
        if self.status in {"absent", "not_observable"} and self.evidence_window_ids:
            raise ValueError("absent and not_observable observations cannot cite positive evidence")
        if self.status == "not_observable" and not self.uncertainty_notes:
            raise ValueError("not_observable requires an explicit uncertainty note")
        return self


class F1FramingObservationBundle(StrictModel):
    """Export the complete reviewed F1 observation ledger to the CSS application."""

    schema_version: Literal[1]
    bundle_id: str = Field(min_length=1)
    run: MeasurementRunIdentity
    window_registry: list[SourceWindowRef] = Field(min_length=1)
    coverage_records: list[SearchCoverageRecord]
    candidate_records: list[CandidateRecord]
    observations: list[FramingObservation]
    excluded_claims: list[str]
    raw_source_content_included: Literal[False]
    scientific_review_status: Literal["not_performed"]

    @model_validator(mode="after")
    def validate_matrix_and_bindings(self) -> "F1FramingObservationBundle":
        """Require complete matrix, reviewed denominators, and exact local evidence refs."""

        expected_cells = {
            (resource_id, function_id)
            for resource_id in F1_RESOURCES
            for function_id in F1_FUNCTIONS
        }
        observed_cells = {(row.resource_id, row.function_id) for row in self.observations}
        if len(self.observations) != len(expected_cells) or observed_cells != expected_cells:
            raise ValueError("bundle must contain exactly one observation for every F1 cell")

        window_by_id = {row.window_id: row for row in self.window_registry}
        if len(window_by_id) != len(self.window_registry):
            raise ValueError("window IDs must be unique")
        coverage_by_id = {row.coverage_id: row for row in self.coverage_records}
        if len(coverage_by_id) != len(self.coverage_records):
            raise ValueError("coverage IDs must be unique")
        if {row.resource_id for row in self.coverage_records} != set(F1_RESOURCES):
            raise ValueError("each F1 instrument requires one coverage record")

        candidate_by_id = {row.candidate_id: row for row in self.candidate_records}
        if len(candidate_by_id) != len(self.candidate_records):
            raise ValueError("candidate IDs must be unique")

        for coverage in self.coverage_records:
            resource_windows = {
                row.window_id
                for row in self.window_registry
                if row.resource_id == coverage.resource_id
            }
            if set(coverage.examined_window_ids) != resource_windows:
                raise ValueError("coverage must exhaust the registered windows for its resource")

        for observation in self.observations:
            coverage = coverage_by_id.get(observation.coverage_id)
            if coverage is None or coverage.resource_id != observation.resource_id:
                raise ValueError("observation coverage must resolve to the same resource")
            if not coverage.reviewed:
                raise ValueError("every final observation requires reviewed coverage")
            if observation.status == "absent" and (
                coverage.search_strategy != "exhaustive_window_review"
            ):
                raise ValueError("absence requires exhaustive source-window review")
            if observation.status == "not_observable" and (
                coverage.search_strategy != "custody_constraint_review"
            ):
                raise ValueError("not_observable requires a reviewed custody constraint")
            for window_id in observation.evidence_window_ids:
                window = window_by_id.get(window_id)
                if window is None or window.resource_id != observation.resource_id:
                    raise ValueError("evidence window must resolve to the same resource")
                if window.review_status != "verified_derived_text":
                    raise ValueError("positive evidence cannot rely on an unreviewed OCR window")
            candidate = candidate_by_id.get(observation.candidate_id)
            if candidate is None or (
                candidate.resource_id,
                candidate.function_id,
            ) != (observation.resource_id, observation.function_id):
                raise ValueError("observation candidate must resolve to the same matrix cell")

        if set(self.excluded_claims) != REQUIRED_EXCLUDED_CLAIMS:
            raise ValueError("bundle must retain the complete frozen claim exclusions")
        return self
