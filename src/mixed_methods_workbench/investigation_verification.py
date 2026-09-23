"""One source-bound, advisory second-model challenge of the pinned P5 case."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .investigation_spine import (
    EXPECTED_FIXTURE_DIGESTS,
    FIXTURE_ROOT,
    ProcessTracingReturn,
    load_investigation_spine,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROMPT_PATH = PROJECT_ROOT / "scripts" / "prompts" / "investigation_verification.yaml"
RECEIPT_PATH = FIXTURE_ROOT / "independent_verification.json"
MODEL = "openrouter/google/gemini-3.1-pro-preview"
TASK = "mixed_methods_workbench.psychosisbank.independent_challenge"


class VerificationError(ValueError):
    """The retained challenge cannot be bound to the pinned investigation."""


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class EvidenceExcerpt(_StrictModel):
    evidence_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_quote: str = Field(min_length=8)


class FindingChallenge(_StrictModel):
    finding_id: str = Field(min_length=1)
    verdict: Literal["bounded_support", "needs_review"]
    reason: str = Field(min_length=20)
    evidence_ids: list[str] = Field(min_length=1)
    source_gap: str | None = None


class ChallengeOutput(_StrictModel):
    findings: list[FindingChallenge] = Field(min_length=1)
    overall_limit: str = Field(min_length=20)


class VerificationReceipt(_StrictModel):
    schema_version: Literal["mmw.independent_challenge.v1"]
    review_state: Literal["model_challenge_pending_human_review"]
    case_id: Literal["psychosisbank-disclosure-explanation"]
    input_digests: dict[str, str]
    prompt_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    schema_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    model_requested: str
    model_resolved: str
    trace_id: str
    generated_at: str
    cost_usd: float = Field(ge=0)
    challenge: ChallengeOutput

    @model_validator(mode="after")
    def _model_identity(self) -> VerificationReceipt:
        if self.model_requested != MODEL or self.model_resolved != MODEL:
            raise ValueError("second-model route differs from the frozen challenge route")
        return self


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _case_inputs(root: Path = FIXTURE_ROOT) -> tuple[ProcessTracingReturn, list[EvidenceExcerpt]]:
    # The existing Workbench contract validates all three pinned artifacts first.
    load_investigation_spine(root)
    raw = json.loads((root / "process_tracing_return.json").read_text(encoding="utf-8"))
    result = ProcessTracingReturn.model_validate(raw)
    excerpts = [
        EvidenceExcerpt.model_validate(
            {key: item[key] for key in ("evidence_id", "source_id", "source_quote")}
        )
        for item in raw["evidence_packet"]["selected_evidence"]
    ]
    source_ids = {item.source_id for item in result.evidence_packet.sources}
    if len({item.evidence_id for item in excerpts}) != len(excerpts):
        raise VerificationError("duplicate evidence excerpt ID")
    if any(item.source_id not in source_ids for item in excerpts):
        raise VerificationError("excerpt names an unknown source")
    return result, excerpts


def _validate_challenge(challenge: ChallengeOutput, result: ProcessTracingReturn) -> None:
    expected = [item.finding_id for item in result.theory_update.findings]
    observed = [item.finding_id for item in challenge.findings]
    if observed != expected:
        raise VerificationError("challenge must review every finding once in source order")
    allowed = {item.evidence_id for item in result.evidence_packet.selected_evidence}
    if any(set(item.evidence_ids) - allowed for item in challenge.findings):
        raise VerificationError("challenge cites an unknown evidence ID")


def load_verification(root: Path = FIXTURE_ROOT) -> VerificationReceipt:
    """Refuse stale or tampered second-model evidence before the UI displays it."""
    result, _ = _case_inputs(root)
    path = root / RECEIPT_PATH.name
    try:
        receipt = VerificationReceipt.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise VerificationError(f"independent challenge is unavailable or invalid: {exc}") from exc
    observed = {name: _digest(root / name) for name in EXPECTED_FIXTURE_DIGESTS}
    if receipt.input_digests != observed:
        raise VerificationError("independent challenge input digests no longer match")
    if receipt.prompt_sha256 != _digest(PROMPT_PATH):
        raise VerificationError("independent challenge prompt changed")
    if receipt.schema_sha256 != _canonical_digest(ChallengeOutput.model_json_schema()):
        raise VerificationError("independent challenge schema changed")
    _validate_challenge(receipt.challenge, result)
    return receipt


def run_verification(*, trace_id: str, max_budget: float, root: Path = FIXTURE_ROOT) -> VerificationReceipt:
    """Call a second model once and retain a bounded candidate for human review."""
    from llm_client import call_llm_structured, render_prompt

    result, excerpts = _case_inputs(root)
    messages = render_prompt(
        PROMPT_PATH,
        question=result.case_scope.research_question,
        conclusion=result.theory_update.summary,
        limits=json.dumps(result.case_scope.selection_and_scope_limits),
        findings=json.dumps([item.model_dump() for item in result.theory_update.findings]),
        excerpts=json.dumps([item.model_dump() for item in excerpts]),
    )
    challenge, metadata = call_llm_structured(
        MODEL,
        messages,
        response_model=ChallengeOutput,
        model_policy="enforce_allowlist",
        model_justification="Independent cross-provider challenge of the existing OpenAI-authored Process Tracing findings",
        reasoning_effort="low",
        task=TASK,
        trace_id=trace_id,
        max_budget=max_budget,
    )
    _validate_challenge(challenge, result)
    return VerificationReceipt(
        schema_version="mmw.independent_challenge.v1",
        review_state="model_challenge_pending_human_review",
        case_id="psychosisbank-disclosure-explanation",
        input_digests={name: _digest(root / name) for name in EXPECTED_FIXTURE_DIGESTS},
        prompt_sha256=_digest(PROMPT_PATH),
        schema_sha256=_canonical_digest(ChallengeOutput.model_json_schema()),
        model_requested=MODEL,
        model_resolved=metadata.model,
        trace_id=trace_id,
        generated_at=datetime.now(UTC).isoformat(),
        cost_usd=metadata.cost,
        challenge=challenge,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace-id", required=True)
    parser.add_argument("--max-budget", required=True, type=float)
    args = parser.parse_args()
    if args.max_budget <= 0:
        parser.error("--max-budget must be positive")
    if RECEIPT_PATH.exists():
        parser.error(f"refusing to overwrite {RECEIPT_PATH}")
    receipt = run_verification(trace_id=args.trace_id, max_budget=args.max_budget)
    RECEIPT_PATH.write_text(receipt.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"trace_id": receipt.trace_id, "cost_usd": receipt.cost_usd,
                      "review_state": receipt.review_state}))


if __name__ == "__main__":
    main()
