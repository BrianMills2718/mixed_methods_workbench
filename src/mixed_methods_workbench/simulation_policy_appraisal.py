"""Consume one authentic simulation comparison without turning it into policy proof.

This fixture-local adapter is a boundary probe, not a shared simulation or
appraisal contract. Cybernetic Influence owns the retained runs. The Workbench
owns the narrow transformation and the refusal to recommend from generated
evidence alone.
"""

from __future__ import annotations

import hashlib
import json
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

FIXTURE_ROOT = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "fixtures"
    / "simulation_policy_appraisal"
)
SOURCE_COMPARISON_PATH = FIXTURE_ROOT / "source_comparison.json"
EXPECTED_FIXTURE_SHA256 = "2b86684ab49affc17998f287756fca222998e14d055f500f5ab232730f2daecb"


class AppraisalModel(BaseModel):
    """Reject undeclared fields and accidental mutation at the probe boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class SimulationCondition(StrEnum):
    """The three frozen conditions in the authentic clean triad."""

    BASELINE = "baseline"
    CAPACITY_CONFLICT = "capacity_conflict"
    CAPACITY_CONFLICT_WITH_VERIFIED_ALLOCATION = (
        "capacity_conflict_with_verified_allocation"
    )


class ComparisonSource(AppraisalModel):
    """Identity and acquisition context for the observed producer route."""

    api_url: str
    retrieved_at: str
    producer_repository: Literal["cybernetic_influence_v3"]
    producer_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    projection_method: str


class SimulationRunProjection(AppraisalModel):
    """Compact projection of one complete authentic retained simulation row."""

    run_id: str = Field(pattern=r"^run_[0-9a-f]+$")
    source_row_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    created_at: str
    status: Literal["completed"]
    scenario: Literal["regional_outbreak"]
    profile: Literal["position_context"]
    condition: SimulationCondition
    producer_condition: str
    execution: Literal["live"]
    agent_count: Literal[12]
    rounds_completed: Literal[3]
    model_calls: Literal[36]
    model: str
    reasoning_effort: Literal["medium"]
    llm_client_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    outcome: Literal["joint_response_approved", "no_joint_response"]
    final_decisions: dict[str, int] = Field(min_length=1)
    final_requests: dict[str, int] = Field(min_length=1)
    final_risks: dict[str, int] = Field(min_length=1)
    exercise_injects: list[str]
    stabilization_events: list[str]

    @model_validator(mode="after")
    def require_complete_tallies(self) -> SimulationRunProjection:
        for label, tally in (
            ("decision", self.final_decisions),
            ("request", self.final_requests),
            ("risk", self.final_risks),
        ):
            if any(value <= 0 for value in tally.values()):
                raise ValueError(f"{label} tally counts must be positive")
            if sum(tally.values()) != self.agent_count:
                raise ValueError(f"{label} tally must account for all simulated roles")
        return self


class SimulationComparisonFixture(AppraisalModel):
    """Frozen consumer view of the clean authentic outbreak triad."""

    schema_id: Literal["cybernetic_influence.outbreak_comparison_projection"]
    schema_version: Literal["0.1.0"]
    artifact_status: Literal["authentic_pinned_projection"]
    source: ComparisonSource
    evidence_origin: Literal["model_generated"]
    scenario: Literal["regional_outbreak"]
    applicability: str
    prohibited_inferences: list[str] = Field(min_length=1)
    runs: list[SimulationRunProjection] = Field(min_length=3, max_length=3)

    @model_validator(mode="after")
    def require_exact_authentic_comparison(self) -> SimulationComparisonFixture:
        by_condition = {run.condition: run for run in self.runs}
        required = set(SimulationCondition)
        if len(by_condition) != len(self.runs) or set(by_condition) != required:
            raise ValueError("fixture requires exactly one run per required condition")

        expected_runs = {
            SimulationCondition.BASELINE: (
                "run_8924342b56ce",
                "63eca0df24ec42c86302e4e5be82af550e33b21ff99fb614a92f7c29279ec7e7",
            ),
            SimulationCondition.CAPACITY_CONFLICT: (
                "run_946a10a820fc",
                "a3079cc3493ae5ab8f0f170716889dad194a611bfe02bb3fe918d6e0c79054c4",
            ),
            SimulationCondition.CAPACITY_CONFLICT_WITH_VERIFIED_ALLOCATION: (
                "run_05acbaea1137",
                "78f87ac4b68b306d12036e44142d016aad639f87156fa21f8262bc523e907870",
            ),
        }
        for condition, (run_id, row_digest) in expected_runs.items():
            run = by_condition[condition]
            if (run.run_id, run.source_row_sha256) != (run_id, row_digest):
                raise ValueError(f"{condition.value} run identity or source digest changed")

        baseline = by_condition[SimulationCondition.BASELINE]
        pressure = by_condition[SimulationCondition.CAPACITY_CONFLICT]
        stabilized = by_condition[
            SimulationCondition.CAPACITY_CONFLICT_WITH_VERIFIED_ALLOCATION
        ]
        if baseline.outcome != "joint_response_approved" or baseline.final_decisions != {
            "support": 12
        }:
            raise ValueError("baseline run must retain unanimous simulated approval")
        if pressure.outcome != "no_joint_response" or pressure.final_decisions != {
            "conditional": 1,
            "defer": 11,
        }:
            raise ValueError("capacity-conflict run must retain non-approval")
        if pressure.stabilization_events:
            raise ValueError("capacity-conflict run cannot contain a stabilization event")
        if stabilized.outcome != "joint_response_approved" or stabilized.final_decisions != {
            "support": 12
        }:
            raise ValueError("stabilized run must retain unanimous simulated approval")
        if stabilized.stabilization_events != [
            "round_2_verified_minimum_capacity_package"
        ]:
            raise ValueError("stabilized run must retain the verified allocation event")
        if pressure.exercise_injects != stabilized.exercise_injects:
            raise ValueError("pressure and stabilization runs must retain matched conflicts")
        if len({run.model for run in self.runs}) != 1 or len(
            {run.llm_client_revision for run in self.runs}
        ) != 1:
            raise ValueError("the triad must retain compatible model and client metadata")
        return self


class AppraisalConclusion(AppraisalModel):
    """A methodological refusal plus the useful action still licensed."""

    status: Literal["insufficient_for_recommendation"]
    permitted_use: Literal["investigate_design_candidate"]
    headline: str
    rationale: str


class SimulationPolicyAppraisal(AppraisalModel):
    """Workbench-owned transformation of generated evidence into a bounded input."""

    schema_id: Literal["workbench.simulation_informed_appraisal"]
    schema_version: Literal["0.1.0"]
    appraisal_id: Literal["regional-outbreak-allocation-probe-v1"]
    artifact_status: Literal["development_boundary_probe"]
    source_fixture_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    evidence_origin: Literal["model_generated"]
    transformation: Literal["simulation_comparison_to_policy_appraisal"]
    policy_question: str
    candidate_action: str
    model_conditional_finding: str
    applicability: str
    conclusion: AppraisalConclusion
    evidence_needed: list[str] = Field(min_length=1)
    non_claims: list[str] = Field(min_length=1)


class SimulationPolicyAppraisalArtifact(AppraisalModel):
    """One API/UI payload retaining producer evidence and appraisal limits."""

    source_comparison: SimulationComparisonFixture
    appraisal: SimulationPolicyAppraisal


def load_simulation_policy_appraisal() -> SimulationPolicyAppraisalArtifact:
    """Validate the pinned source projection and derive the bounded appraisal."""

    fixture_bytes = SOURCE_COMPARISON_PATH.read_bytes()
    fixture_sha256 = hashlib.sha256(fixture_bytes).hexdigest()
    if fixture_sha256 != EXPECTED_FIXTURE_SHA256:
        raise ValueError("simulation comparison fixture SHA-256 does not match")
    comparison = SimulationComparisonFixture.model_validate(json.loads(fixture_bytes))
    appraisal = SimulationPolicyAppraisal(
        schema_id="workbench.simulation_informed_appraisal",
        schema_version="0.1.0",
        appraisal_id="regional-outbreak-allocation-probe-v1",
        artifact_status="development_boundary_probe",
        source_fixture_sha256=fixture_sha256,
        evidence_origin="model_generated",
        transformation="simulation_comparison_to_policy_appraisal",
        policy_question=(
            "Should a verified minimum-capacity allocation package be investigated "
            "as part of a regional outbreak coordination protocol?"
        ),
        candidate_action=(
            "Design and evaluate a transparent 48-hour package that protects national "
            "minimums, commits mobile laboratory and clinical capacity, retains a "
            "regional reserve, and publishes delivery receipts."
        ),
        model_conditional_finding=(
            "In these retained simulated conditions, the modeled capacity conflict "
            "coincided with loss of coalition approval, and adding the modeled verified "
            "allocation package coincided with restored unanimous approval."
        ),
        applicability=comparison.applicability,
        conclusion=AppraisalConclusion(
            status="insufficient_for_recommendation",
            permitted_use="investigate_design_candidate",
            headline="Investigate the allocation package; do not recommend adoption yet.",
            rationale=(
                "The comparison makes the package a plausible design candidate inside "
                "this model. It supplies no observed real-world effect, feasibility, "
                "cost, legal, distributional, or implementation evidence."
            ),
        ),
        evidence_needed=[
            "Operational capacity and logistics data from a bounded real coordination setting.",
            "Stakeholder evidence on whether the allocation rules and receipt reporting are acceptable and legitimate.",
            "Legal and institutional review of authority, mandates, procurement, data custody, and cross-border commitments.",
            "Cost, distributional, failure-mode, and implementation analysis against feasible alternatives.",
            "Empirical evaluation or exercises capable of challenging the simulated mechanism and its assumptions.",
        ],
        non_claims=list(comparison.prohibited_inferences),
    )
    return SimulationPolicyAppraisalArtifact(
        source_comparison=comparison,
        appraisal=appraisal,
    )


def simulation_policy_appraisal_payload() -> dict[str, object]:
    """Return the exact JSON-compatible artifact used by browser and agents."""

    return load_simulation_policy_appraisal().model_dump(mode="json")
