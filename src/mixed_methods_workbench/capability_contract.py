"""Expose one bounded cross-method capability without flattening method meaning.

The compatibility evidence was produced in Project Meta and normalized in the
Process Tracing review host. This Workbench consumer pins those bytes, validates
the common anchor, and explains the distinct Grounded Theory and Process
Tracing adapters. It does not adopt a universal capability schema.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "fixtures"
    / "capability_contracts"
    / "evidence_anchor_compatibility_v0.json"
)
FIXTURE_SOURCE_REPOSITORY = "BrianMills2718/process_tracing"
FIXTURE_SOURCE_REVISION = "0433a1b31a1eaee8793c43184558c18c48ef84ed"
FIXTURE_SOURCE_PATH = "pt/fixtures/evidence_anchor_compatibility_v0.json"
EXPECTED_FIXTURE_SHA256 = "3bf582ce91485f29909469fd560663cb55422b5383e3a87e16e70389fc31cf3f"
SOURCE_CONTRACT_REVISION = "22a2d5a60b61e084eb2670a78ec93ab65ac43aa2"
SOURCE_CONTRACT_SHA256 = "a81e1dffb83bdac4edc7b6ff9093a9ef27d7501281273fe31e4c05f0217e44bb"


class CapabilityModel(BaseModel):
    """Reject undeclared fields at this experimental consumer boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class SourceContractRef(CapabilityModel):
    repository_id: Literal["project-meta"]
    revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    path: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    decision: Literal["candidate_compatible"]


class ArtifactLineage(CapabilityModel):
    role: str
    path: str
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class RecordLineage(CapabilityModel):
    repository_id: Literal["qualitative_coding", "process_tracing"]
    inspected_repository_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    producer_revision_status: Literal["recorded", "unrecorded"]
    artifacts: list[ArtifactLineage] = Field(min_length=1)


class EvidenceAnchor(CapabilityModel):
    """The common output: source identity and context, not interpretation."""

    anchor_id: str
    source_resource_id: str
    source_locator: str
    source_unit_id: str
    locator_kind: Literal["character_span", "immutable_span"]
    locator_value: str
    selection_match: Literal["exact", "whitespace_normalized"]
    selected_text: str
    selected_text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    context_text: str
    context_text_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    review_state: Literal["model_generated", "human_reviewed"]
    lineage_ref: str

    @model_validator(mode="after")
    def require_verified_binding(self) -> EvidenceAnchor:
        if _sha256(self.selected_text) != self.selected_text_sha256:
            raise ValueError("selected_text_hash_mismatch")
        if _sha256(self.context_text) != self.context_text_sha256:
            raise ValueError("context_hash_mismatch")
        selected = self.selected_text
        context = self.context_text
        if self.selection_match == "whitespace_normalized":
            selected = _normalize_whitespace(selected)
            context = _normalize_whitespace(context)
        if selected not in context:
            raise ValueError("selected_text_not_in_context")
        if self.locator_kind == "character_span":
            match = re.fullmatch(r"(\d+):(\d+)", self.locator_value)
            if match is None or int(match.group(2)) - int(match.group(1)) != len(
                self.selected_text
            ):
                raise ValueError("locator_mismatch")
        elif self.locator_value != self.source_unit_id:
            raise ValueError("locator_mismatch")
        return self


class GroundedTheoryPayload(CapabilityModel):
    incident_index: int = Field(ge=1)
    open_code: str
    meaning: str


class ProcessTracingPayload(CapabilityModel):
    evidence_id: str
    case_id: str
    evidence_type: str
    source_genre: str
    temporal_context: str
    trace_production_relevance: str


class GroundedTheoryRecord(CapabilityModel):
    record_id: str
    method_id: Literal["grounded_theory"]
    record_kind: Literal["qualitative_coding.grounded_theory_incident"]
    title: str
    analytic_role: str
    method_payload: GroundedTheoryPayload
    method_specific_fields: list[
        Literal["incident_index", "open_code", "meaning"]
    ] = Field(min_length=3, max_length=3)
    lineage: RecordLineage
    anchors: list[EvidenceAnchor] = Field(min_length=1)


class ProcessTracingRecord(CapabilityModel):
    record_id: str
    method_id: Literal["process_tracing"]
    record_kind: Literal["process_tracing.diagnostic_evidence"]
    title: str
    analytic_role: str
    method_payload: ProcessTracingPayload
    method_specific_fields: list[
        Literal[
            "evidence_id",
            "case_id",
            "evidence_type",
            "source_genre",
            "temporal_context",
            "trace_production_relevance",
        ]
    ] = Field(min_length=6, max_length=6)
    lineage: RecordLineage
    anchors: list[EvidenceAnchor] = Field(min_length=1)


EvidenceRecord = Annotated[
    GroundedTheoryRecord | ProcessTracingRecord, Field(discriminator="method_id")
]


class EvidenceAnchorCompatibility(CapabilityModel):
    schema_version: Literal["mixed-method-evidence-anchor-view/v0.1"]
    status: Literal["experimental_consumer"]
    capability_ref: Literal["evidence.anchor"]
    source_contract: SourceContractRef
    records: list[EvidenceRecord] = Field(min_length=2, max_length=2)
    shared_fields: list[str]
    interpretation_boundary: str
    non_claims: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def require_two_method_compatibility(self) -> EvidenceAnchorCompatibility:
        if self.source_contract.revision != SOURCE_CONTRACT_REVISION:
            raise ValueError("source_contract_revision_mismatch")
        if self.source_contract.sha256 != SOURCE_CONTRACT_SHA256:
            raise ValueError("source_contract_hash_mismatch")
        if {record.method_id for record in self.records} != {
            "grounded_theory",
            "process_tracing",
        }:
            raise ValueError("comparison_requires_both_methods")
        if set(self.shared_fields) != set(EvidenceAnchor.model_fields):
            raise ValueError("shared_fields_mismatch")
        shared = set(self.shared_fields)
        for record in self.records:
            if set(record.method_specific_fields) & shared:
                raise ValueError("method_fields_leaked_into_shared_anchor")
            if any(anchor.lineage_ref != record.record_id for anchor in record.anchors):
                raise ValueError("anchor_lineage_mismatch")
        return self


class CapabilityPort(CapabilityModel):
    name: str
    fields: list[str] = Field(min_length=1)
    meaning: str


class MethodAdapter(CapabilityModel):
    method_id: Literal["grounded_theory", "process_tracing"]
    parent_record: str
    method_fields_retained_outside_capability: list[str] = Field(min_length=1)
    downstream_use: str
    forbidden_inference: str


class ModularCapabilitySpec(CapabilityModel):
    capability_id: Literal["evidence.anchor"]
    label: Literal["Bind evidence to an exact source"]
    maturity: Literal["candidate_compatible_two_method_probe"]
    purpose: str
    input_port: CapabilityPort
    operation: str
    output_port: CapabilityPort
    invariants: list[str] = Field(min_length=1)
    refusal_codes: list[str] = Field(min_length=1)
    preserves: list[str] = Field(min_length=1)
    deliberately_does_not_decide: list[str] = Field(min_length=1)
    adapters: list[MethodAdapter] = Field(min_length=2, max_length=2)


class FixtureCustody(CapabilityModel):
    source_repository: Literal["BrianMills2718/process_tracing"]
    source_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    source_path: str
    artifact_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    relationship: Literal["hash_bound_derived_fixture"]


class CapabilityContractArtifact(CapabilityModel):
    custody: FixtureCustody
    capability: ModularCapabilitySpec
    demonstration: EvidenceAnchorCompatibility


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def _capability_spec() -> ModularCapabilitySpec:
    anchor_fields = list(EvidenceAnchor.model_fields)
    return ModularCapabilitySpec(
        capability_id="evidence.anchor",
        label="Bind evidence to an exact source",
        maturity="candidate_compatible_two_method_probe",
        purpose=(
            "Create a verifiable source binding that different analytical methods can "
            "consume without sharing an interpretation or evidence-strength scale."
        ),
        input_port=CapabilityPort(
            name="source_selection",
            fields=[
                "source_resource_id",
                "source_locator",
                "source_unit_id",
                "locator_kind",
                "locator_value",
                "selection_match",
                "selected_text",
                "context_text",
                "review_state",
                "lineage_ref",
            ],
            meaning="A selected passage plus the source unit and record it came from.",
        ),
        operation=(
            "Verify text hashes, locator semantics, selection-in-context, source identity, "
            "and parent-record lineage; then return the unchanged source-bound anchor."
        ),
        output_port=CapabilityPort(
            name="verified_evidence_anchor",
            fields=anchor_fields,
            meaning="A source-bound evidence reference carrying identity, context, review, and lineage.",
        ),
        invariants=[
            "Selected and context text hashes match the retained UTF-8 text.",
            "The selected passage occurs inside the declared context under the declared match rule.",
            "The locator identifies the selected span or immutable source unit.",
            "The anchor points back to exactly one parent analytical record.",
            "Method-specific interpretation never enters the common anchor payload.",
        ],
        refusal_codes=[
            "selected_text_hash_mismatch",
            "context_hash_mismatch",
            "selected_text_not_in_context",
            "locator_mismatch",
            "anchor_lineage_mismatch",
            "method_fields_leaked_into_shared_anchor",
        ],
        preserves=[
            "source-resource identity",
            "source-unit identity",
            "exact selection and surrounding context",
            "review state",
            "parent-record lineage",
        ],
        deliberately_does_not_decide=[
            "what the passage means",
            "whether it supports or challenges a claim",
            "how diagnostically probative it is",
            "whether a category or causal explanation is warranted",
        ],
        adapters=[
            MethodAdapter(
                method_id="grounded_theory",
                parent_record="qualitative_coding.grounded_theory_incident",
                method_fields_retained_outside_capability=[
                    "incident_index",
                    "open_code",
                    "meaning",
                ],
                downstream_use=(
                    "The method may compare the incident with other incidents and develop or revise "
                    "categories; the anchor supplies traceability only."
                ),
                forbidden_inference=(
                    "An anchored passage does not by itself confirm a category or establish saturation."
                ),
            ),
            MethodAdapter(
                method_id="process_tracing",
                parent_record="process_tracing.diagnostic_evidence",
                method_fields_retained_outside_capability=[
                    "evidence_id",
                    "case_id",
                    "evidence_type",
                    "source_genre",
                    "temporal_context",
                    "trace_production_relevance",
                ],
                downstream_use=(
                    "The method may appraise the item against every rival and its observable "
                    "predictions; the anchor supplies traceability only."
                ),
                forbidden_inference=(
                    "An anchored passage does not by itself establish a causal mechanism or likelihood."
                ),
            ),
        ],
    )


def load_evidence_anchor_capability() -> CapabilityContractArtifact:
    """Validate the exact two-method fixture and expose the bounded capability."""

    fixture_bytes = FIXTURE_PATH.read_bytes()
    digest = hashlib.sha256(fixture_bytes).hexdigest()
    if digest != EXPECTED_FIXTURE_SHA256:
        raise ValueError("evidence-anchor fixture SHA-256 does not match")
    demonstration = EvidenceAnchorCompatibility.model_validate(json.loads(fixture_bytes))
    return CapabilityContractArtifact(
        custody=FixtureCustody(
            source_repository="BrianMills2718/process_tracing",
            source_revision=FIXTURE_SOURCE_REVISION,
            source_path=FIXTURE_SOURCE_PATH,
            artifact_sha256=digest,
            relationship="hash_bound_derived_fixture",
        ),
        capability=_capability_spec(),
        demonstration=demonstration,
    )


def evidence_anchor_capability_payload() -> dict[str, object]:
    """Return the same typed capability artifact consumed by the browser."""

    return load_evidence_anchor_capability().model_dump(mode="json")
