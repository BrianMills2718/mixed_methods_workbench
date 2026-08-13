#!/usr/bin/env python3
"""Run a live, bounded NYC extraction canary through the shared LLM client.

The script verifies both official PDF files before parsing, binds each returned
quote uniquely to the supplied source unit, and writes no committed fixture.
Its JSON output is a candidate plus an auditable runtime receipt, never a human
review decision.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from mixed_methods_workbench.nyc_crz_evidence_slice import verify_source_document

PREDICTION_UNIT_ID = "reevaluation_2:pdf-page-15:table-2.2:objective-2"
CONCERN_UNIT_ID = "hearing_2022_08_25:pdf-page-82:printed-lines-13-17"
REEVALUATION_SHA256 = "aee0e0b6c17a8e9585c24a808d2fa77a756b267fe9af326fb577ae181bb28733"
HEARING_SHA256 = "e42cbffeec77b2392cc6e74b36ba8978c08a69f63cfa5a341ee512c6e7a67cf1"
REEVALUATION_BYTES = 1_430_307
HEARING_BYTES = 1_470_785
MODEL = "openrouter/deepseek/deepseek-v4-flash"


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Prediction(_StrictModel):
    source_unit_id: Literal["reevaluation_2:pdf-page-15:table-2.2:objective-2"]
    statement: str = Field(
        min_length=40,
        description="Plain-language agency prediction including scenario and comparison basis.",
    )
    metric: Literal["daily_vehicles_entering_manhattan_cbd"]
    expected_direction: Literal["decrease"]
    expected_change_percent: float = Field(
        gt=0, description="Positive magnitude 13.4; direction is stored separately."
    )
    comparison_basis: Literal["No Action"]
    scenario: Literal["Phase 1 ($9 peak auto toll)"]
    exact_evidence_quote: str = Field(
        min_length=30,
        description=(
            "One contiguous clause or row copied from the source unit, with only "
            "whitespace normalized."
        ),
    )
    limit: str = Field(
        min_length=40,
        description="Complete sentence explaining this is not an observed or causal result.",
    )


class Concern(_StrictModel):
    source_unit_id: Literal[
        "hearing_2022_08_25:pdf-page-82:printed-lines-13-17"
    ]
    statement: str = Field(min_length=30, description="Plain-language concern without speaker name.")
    affected_groups: list[str] = Field(
        min_length=1, description="Only groups named or directly described."
    )
    concern_kind: Literal["access_cost_burden"]
    exact_evidence_quote: str = Field(
        min_length=30,
        description=(
            "One contiguous clause copied from the source unit, with only whitespace normalized."
        ),
    )
    limit: str = Field(
        min_length=40,
        description=(
            "Complete sentence explaining one statement does not establish prevalence, "
            "representativeness, or an effect."
        ),
    )


class Bundle(_StrictModel):
    prediction: Prediction
    concern: Concern


def _sha256_json(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _normalize(value: str) -> str:
    return " ".join(value.split())


def _extract_units(reevaluation: Path, hearing: Path) -> tuple[str, str]:
    try:
        from pypdf import PdfReader  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError("pypdf is required for the live canary") from exc

    prediction_page = PdfReader(reevaluation).pages[14].extract_text(
        extraction_mode="layout"
    ) or ""
    prediction_match = re.search(
        r"Daily vehicle reduction \(2023\).+?17\.3%", prediction_page, re.DOTALL
    )
    if prediction_match is None:
        raise RuntimeError("prediction_source_unit_not_found")
    prediction_context = _normalize(
        "Phase 1 ($9 peak auto toll) Criterion: Reduce by 10% (relative to No Action) "
        + prediction_match.group(0)
    )

    hearing_page = PdfReader(hearing).pages[81].extract_text(extraction_mode="layout") or ""
    try:
        printed_lines = hearing_page[hearing_page.index(" 13") : hearing_page.index(" 18")]
    except ValueError as exc:
        raise RuntimeError("concern_source_unit_not_found") from exc
    concern_context = " ".join(
        re.sub(r"^\s*\d{1,2}\s+", "", line).strip()
        for line in printed_lines.splitlines()
        if line.strip()
    )
    if "vulnerable populations would incur additional costs" not in concern_context:
        raise RuntimeError("concern_source_unit_not_found")
    return prediction_context, concern_context


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reevaluation", type=Path, required=True)
    parser.add_argument("--hearing", type=Path, required=True)
    parser.add_argument(
        "--trace-id",
        default="mixed_methods_workbench/nyc-crz-mvp-v1/anchored-extraction-canary-live",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    # This gate intentionally runs before pypdf touches either document.
    verify_source_document(
        args.reevaluation,
        expected_sha256=REEVALUATION_SHA256,
        expected_bytes=REEVALUATION_BYTES,
    )
    verify_source_document(
        args.hearing,
        expected_sha256=HEARING_SHA256,
        expected_bytes=HEARING_BYTES,
    )
    prediction_context, concern_context = _extract_units(args.reevaluation, args.hearing)

    try:
        from llm_client import (  # type: ignore[import-not-found]
            call_llm_structured,
            render_prompt,
        )
        from llm_client.execution.call_contracts import (  # type: ignore[import-not-found]
            StructuredOutputPolicy,
        )
    except ImportError as exc:
        raise RuntimeError(
            "the shared llm_client checkout must be installed in the executing environment"
        ) from exc

    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "nyc_crz_anchored_extraction.yaml"
    messages = render_prompt(
        prompt_path,
        prediction_unit_id=PREDICTION_UNIT_ID,
        prediction_context=prediction_context,
        concern_unit_id=CONCERN_UNIT_ID,
        concern_context=concern_context,
    )
    prompt_sha256 = _sha256_json(messages)
    schema_sha256 = _sha256_json(Bundle.model_json_schema())
    bundle, metadata = call_llm_structured(
        MODEL,
        messages,
        response_model=Bundle,
        model_justification=(
            "Use the current Qualitative Coding structured-extraction route for a bounded "
            "low-cost Workbench seam canary."
        ),
        reasoning_effort="none",
        model_policy="enforce_allowlist",
        structured_output_policy=StructuredOutputPolicy(mode="require_native_json_schema"),
        timeout=90,
        num_retries=1,
        task="mixed_methods_workbench.nyc_crz.structured_extraction_canary",
        trace_id=args.trace_id,
        max_budget=0.25,
    )
    for kind, record, context in (
        ("prediction", bundle.prediction, prediction_context),
        ("concern", bundle.concern, concern_context),
    ):
        occurrences = _normalize(context).count(_normalize(record.exact_evidence_quote))
        if occurrences != 1:
            raise RuntimeError(f"{kind}_quote_binding_failed:{occurrences}")

    candidate = bundle.model_dump(mode="json")
    result = {
        "schema_version": "mmw.live_extraction_canary.v0.1",
        "review_state": "model_generated_pending_human_review",
        "candidate": candidate,
        "receipt": {
            "trace_id": args.trace_id,
            "logical_call_id": metadata.logical_call_id,
            "requested_model": metadata.requested_model,
            "resolved_model": metadata.resolved_model,
            "prompt_sha256": prompt_sha256,
            "schema_sha256": schema_sha256,
            "prediction_context_sha256": _sha256_text(prediction_context),
            "concern_context_sha256": _sha256_text(concern_context),
            "output_sha256": _sha256_json(candidate),
            "usage": metadata.usage,
            "cost": metadata.cost,
            "cost_source": metadata.cost_source,
            "cache_hit": metadata.cache_hit,
            "finish_reason": metadata.finish_reason,
        },
    }
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        if args.output.exists():
            raise RuntimeError(f"refusing to overwrite existing output: {args.output}")
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
