"""Source-bound receipt for one connected PsychosisBank synthesis execution."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from .investigation_verification import (
    MODEL as CHECK_MODEL,
)
from .investigation_verification import (
    PROMPT_PATH,
    ChallengeOutput,
)
from .investigation_verification import (
    TASK as CHECK_TASK,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUN_ROOT = PROJECT_ROOT / "examples" / "runs" / "psychosisbank-synthesis-20260923"
RECEIPT_NAME = "connected_run_receipt.json"
INPUT_FILES = (
    "qc_theory_input.json",
    "case_source_packet.json",
    "case_corpus.txt",
    "pt-generated/result_blocked_prepublication.json",
    "pt-generated/central_claim_review.json",
    "pt-generated/pt_export_v2.json",
    "pt/partition_resolution.json",
)


class ConnectedRunError(ValueError):
    """The connected execution cannot be shown as a verified run."""


class _Consumer(BaseModel):
    model_config = ConfigDict(extra="ignore")


class _Owned(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class _Hypothesis(_Consumer):
    hypothesis_id: str
    description: str


class _Verdict(_Consumer):
    hypothesis_id: str
    status: str
    reasoning: str
    key_evidence_for: list[str]
    key_evidence_against: list[str]


class _Evidence(_Consumer):
    evidence_id: str
    source_id: str | None
    source_quote: str | None


class _Conclusion(_Consumer):
    status: str
    leading_hypothesis_ids: list[str]
    public_headline_eligible: bool
    public_headline_reason: str


class _Inference(_Consumer):
    mode: str
    status: str
    rationale: str


class _Integrity(_Consumer):
    status: str
    incomplete_reasons: list[str]


class _Scope(_Consumer):
    claim_limits: list[str]
    limitations: list[str]


class _Producer(_Consumer):
    git_commit: str | None


class _Provenance(_Consumer):
    result_json_sha256: str
    source_text_sha256: str


class ProcessTracingExport(_Consumer):
    schema_version: Literal["pt_export_v2"]
    producer: _Producer
    artifact_provenance: _Provenance
    research_question: str
    hypotheses: list[_Hypothesis]
    verdicts: list[_Verdict]
    evidence: list[_Evidence]
    comparative_conclusion: _Conclusion
    inference_provenance: _Inference
    methodology_integrity: _Integrity
    source_scope: _Scope
    limitations: list[str]


class RunAttempt(_Owned):
    trace_id: str
    route: str
    outcome: Literal["blocked_partition", "blocked_publication"]
    evidence_path: str
    evidence_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class ConnectedRunReceipt(_Owned):
    schema_version: Literal["mmw.psychosisbank_connected_run.v1"]
    run_id: Literal["psychosisbank-synthesis-20260923"]
    generated_at: str
    qc_input_state: Literal["reused_reviewed_proposition"]
    qc_producer_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    pt_producer_revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    input_digests: dict[str, str]
    attempts: list[RunAttempt] = Field(min_length=2)
    check_model: str
    check_trace_id: str
    check_cost_usd: float = Field(ge=0)
    check_prompt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    review_state: Literal["blocked_publication_pending_researcher_review"]
    publication_block_reason: str = Field(min_length=20)
    challenge: ChallengeOutput


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_export(root: Path = RUN_ROOT) -> ProcessTracingExport:
    """Consume the producer's versioned public export, never its internal schema."""
    path = root / "pt-generated" / "pt_export_v2.json"
    try:
        export = ProcessTracingExport.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ConnectedRunError(f"Process Tracing export unavailable or invalid: {exc}") from exc
    try:
        result_digest = _digest(root / "pt-generated" / "result_blocked_prepublication.json")
        corpus_digest = _digest(root / "case_corpus.txt")
    except OSError as exc:
        raise ConnectedRunError(f"Process Tracing source artifact unavailable: {exc}") from exc
    if export.artifact_provenance.result_json_sha256 != result_digest:
        raise ConnectedRunError("Process Tracing export does not bind the result bytes")
    if export.artifact_provenance.source_text_sha256 != corpus_digest:
        raise ConnectedRunError("Process Tracing export does not bind the frozen corpus")
    if not export.producer.git_commit:
        raise ConnectedRunError("Process Tracing producer revision is missing")
    return export


def _validate_challenge(challenge: ChallengeOutput, export: ProcessTracingExport) -> None:
    expected = [item.hypothesis_id for item in export.verdicts]
    observed = [item.finding_id for item in challenge.findings]
    if observed != expected:
        raise ConnectedRunError("independent challenge must review every verdict in source order")
    evidence = {item.evidence_id for item in export.evidence if item.source_quote}
    if any(set(item.evidence_ids) - evidence for item in challenge.findings):
        raise ConnectedRunError("independent challenge cites an unavailable source quote")


def load_connected_run(root: Path = RUN_ROOT) -> tuple[ConnectedRunReceipt, ProcessTracingExport]:
    """Validate retained inputs, both attempts, and the fresh model challenge."""
    export = load_export(root)
    try:
        receipt = ConnectedRunReceipt.model_validate_json(
            (root / RECEIPT_NAME).read_text(encoding="utf-8")
        )
    except (OSError, ValueError) as exc:
        raise ConnectedRunError(f"connected run receipt unavailable or invalid: {exc}") from exc
    try:
        observed = {name: _digest(root / name) for name in INPUT_FILES}
    except OSError as exc:
        raise ConnectedRunError(f"connected run input unavailable: {exc}") from exc
    if receipt.input_digests != observed:
        raise ConnectedRunError("connected run inputs changed")
    if receipt.check_prompt_sha256 != _digest(PROMPT_PATH):
        raise ConnectedRunError("independent challenge prompt changed")
    if receipt.check_model != CHECK_MODEL:
        raise ConnectedRunError("independent challenge model changed")
    if receipt.pt_producer_revision != export.producer.git_commit:
        raise ConnectedRunError("Process Tracing producer revision changed")
    for attempt in receipt.attempts:
        path = (root / attempt.evidence_path).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ConnectedRunError("run attempt evidence escapes the run root")
        try:
            digest = _digest(path)
        except OSError as exc:
            raise ConnectedRunError(f"run attempt evidence unavailable: {exc}") from exc
        if digest != attempt.evidence_sha256:
            raise ConnectedRunError("run attempt evidence changed")
    if [item.outcome for item in receipt.attempts] != ["blocked_partition", "blocked_publication"]:
        raise ConnectedRunError("run attempt sequence changed")
    _validate_challenge(receipt.challenge, export)
    return receipt, export


def connected_run_payload(root: Path = RUN_ROOT) -> dict[str, object]:
    """Project the fresh run without promoting its model output into a finding."""
    receipt, export = load_connected_run(root)
    evidence = {
        item.evidence_id: {"source_id": item.source_id, "source_quote": item.source_quote}
        for item in export.evidence if item.source_quote
    }
    return {
        "run_id": receipt.run_id,
        "qc_input_state": receipt.qc_input_state,
        "attempts": [item.model_dump() for item in receipt.attempts],
        "research_question": export.research_question,
        "conclusion": export.comparative_conclusion.model_dump(),
        "inference": export.inference_provenance.model_dump(),
        "methodology": export.methodology_integrity.model_dump(),
        "claim_limits": export.source_scope.claim_limits,
        "hypotheses": [item.model_dump() for item in export.hypotheses],
        "verdicts": [item.model_dump() for item in export.verdicts],
        "challenge": receipt.challenge.model_dump(),
        "cited_evidence": evidence,
        "check_model": receipt.check_model,
        "check_trace_id": receipt.check_trace_id,
        "review_state": receipt.review_state,
        "publication_block_reason": receipt.publication_block_reason,
        "planning_receipt": load_planning_receipt(root).model_dump(),
    }


def generate_connected_run(
    *, trace_id: str, max_budget: float, root: Path = RUN_ROOT
) -> ConnectedRunReceipt:
    """Challenge the fresh native export and retain the exact execution chain."""
    from llm_client import call_llm_structured, render_prompt

    export = load_export(root)
    # load_export rejects a missing producer revision; make that invariant visible to mypy.
    assert export.producer.git_commit is not None
    evidence = [
        {"evidence_id": item.evidence_id, "source_id": item.source_id,
         "source_quote": item.source_quote}
        for item in export.evidence if item.source_quote
    ]
    findings = [
        {"finding_id": item.hypothesis_id, "verdict": item.status,
         "reasoning": item.reasoning,
         "evidence_ids": list(dict.fromkeys(item.key_evidence_for + item.key_evidence_against))}
        for item in export.verdicts
    ]
    messages = render_prompt(
        PROMPT_PATH,
        question=export.research_question,
        conclusion=json.dumps(export.comparative_conclusion.model_dump()),
        limits=json.dumps({"source": export.source_scope.claim_limits,
                           "inference": export.inference_provenance.model_dump(),
                           "methodology": export.methodology_integrity.model_dump(),
                           "publication_gate": "blocked by Process Tracing terminal claim review"}),
        findings=json.dumps(findings),
        excerpts=json.dumps(evidence),
    )
    challenge, metadata = call_llm_structured(
        CHECK_MODEL,
        messages,
        response_model=ChallengeOutput,
        model_policy="enforce_allowlist",
        model_justification="Independent cross-provider challenge of a fresh Process Tracing export",
        reasoning_effort="low",
        task=CHECK_TASK,
        trace_id=trace_id,
        max_budget=max_budget,
    )
    _validate_challenge(challenge, export)
    if metadata.model != CHECK_MODEL:
        raise ConnectedRunError("independent challenge resolved to a different model")
    theory = json.loads((root / "qc_theory_input.json").read_text(encoding="utf-8"))
    return ConnectedRunReceipt(
        schema_version="mmw.psychosisbank_connected_run.v1",
        run_id="psychosisbank-synthesis-20260923",
        generated_at=datetime.now(UTC).isoformat(),
        qc_input_state="reused_reviewed_proposition",
        qc_producer_revision=theory["producer"]["revision"],
        pt_producer_revision=export.producer.git_commit,
        input_digests={name: _digest(root / name) for name in INPUT_FILES},
        attempts=[
            RunAttempt(trace_id="mmw-psychosisbank-connected-20260923",
                       route="frozen reviewed rivals", outcome="blocked_partition",
                       evidence_path="pt/partition_resolution.json",
                       evidence_sha256=_digest(root / "pt" / "partition_resolution.json")),
            RunAttempt(trace_id="mmw-psychosisbank-generated-20260923",
                       route="theory-first generated and audited rivals", outcome="blocked_publication",
                       evidence_path="pt-generated/pt_export_v2.json",
                       evidence_sha256=_digest(root / "pt-generated" / "pt_export_v2.json")),
        ],
        check_model=CHECK_MODEL,
        check_trace_id=trace_id,
        check_cost_usd=metadata.cost,
        check_prompt_sha256=_digest(PROMPT_PATH),
        review_state="blocked_publication_pending_researcher_review",
        publication_block_reason=(
            "Process Tracing terminal claim review found unsupported claims and blocked "
            "publication. The exported comparative weights are diagnostics only."
        ),
        challenge=challenge,
    )

PLANNING_RECEIPT_NAME = "planning_receipt.json"


class PlanningReceipt(_Owned):
    """Workbench-owned, source-bound plan for the retained connected run."""

    schema_version: Literal["mmw.psychosisbank_planning_receipt.v1"]
    investigation_id: Literal["psychosisbank-disclosure-explanation"]
    question: str = Field(min_length=20)
    connected_run_receipt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_input_digests: dict[str, str]
    method_roles: dict[Literal["qualitative_coding", "process_tracing", "independent_check"], str]
    prohibited_inferences: list[str] = Field(min_length=1)
    terminal_review_state: Literal["withhold_causal_publication_pending_human_review"]
    human_decision: Literal["withhold_causal_publication"]
    next_evidence: list[str] = Field(min_length=1)


def load_planning_receipt(root: Path = RUN_ROOT) -> PlanningReceipt:
    """Load a plan only when it remains bound to the retained run and its guardrails."""
    receipt, export = load_connected_run(root)
    path = root / PLANNING_RECEIPT_NAME
    try:
        plan = PlanningReceipt.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ConnectedRunError(f"planning receipt unavailable or invalid: {exc}") from exc
    if plan.question != export.research_question:
        raise ConnectedRunError("planning receipt question changed")
    if plan.connected_run_receipt_sha256 != _digest(root / RECEIPT_NAME):
        raise ConnectedRunError("planning receipt does not bind the connected run bytes")
    if plan.source_input_digests != receipt.input_digests:
        raise ConnectedRunError("planning receipt source inputs changed")
    if plan.method_roles["qualitative_coding"] != "candidate proposition; no causal conclusion":
        raise ConnectedRunError("planning receipt changes Qualitative Coding's role")
    if plan.method_roles["process_tracing"] != "test rival explanations within the frozen source scope":
        raise ConnectedRunError("planning receipt changes Process Tracing's role")
    if plan.method_roles["independent_check"] != "advisory challenge; cannot approve a causal conclusion":
        raise ConnectedRunError("planning receipt changes independent-check boundary")
    if not any("causal" in item.casefold() for item in plan.prohibited_inferences):
        raise ConnectedRunError("planning receipt omits the causal-claim prohibition")
    if receipt.review_state != "blocked_publication_pending_researcher_review":
        raise ConnectedRunError("planning receipt cannot override the connected-run review state")
    return plan
