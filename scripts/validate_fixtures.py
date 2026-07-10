#!/usr/bin/env python3
"""Validate mixed-methods workbench fixture contracts.

The current repo is a planning scaffold, so this validator intentionally uses
only the Python standard library. It checks the synthetic contract fixtures that
future engine-produced fixtures must replace.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, cast


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE_DIR = REPO_ROOT / "examples" / "fixtures" / "workbench_contract_v1"

FORBIDDEN_GENERIC_FIELDS = {
    "probability_of_truth",
    "truth_probability",
    "confidence_score",
    "generic_confidence",
}

QC_FORBIDDEN_INFERENCE_FIELDS = FORBIDDEN_GENERIC_FIELDS | {
    "posterior",
    "final_posterior",
    "hypothesis_posterior",
    "hypothesis_posteriors",
    "bayesian_update",
    "bayesian_updates",
    "likelihood_vector",
    "likelihood_vectors",
    "evidence_likelihoods",
    "comparative_support",
}

REQUIRED_FILES = {
    "qc_handoff_stub.json",
    "pt_export_stub.json",
    "theory_operationalization_stub.json",
    "workbench_synthesis_stub.json",
}


def main() -> None:
    """Run all fixture checks and fail loudly on the first invalid condition."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture-dir",
        type=Path,
        default=DEFAULT_FIXTURE_DIR,
        help="Fixture directory containing manifest.json and contract JSON files.",
    )
    args = parser.parse_args()
    validate_fixture_dir(args.fixture_dir)
    print("Fixture contract validation passed.")


def validate_fixture_dir(fixture_dir: Path) -> None:
    """Validate one fixture directory."""
    manifest = _read_json(fixture_dir / "manifest.json")
    _require(manifest.get("schema_version") == 1, "manifest schema_version must be 1")
    _require(
        manifest.get("artifact_status") == "synthetic_contract_fixture",
        "manifest artifact_status must mark fixtures as synthetic_contract_fixture",
    )

    files = manifest.get("files")
    if not isinstance(files, list):
        raise SystemExit("ERROR: manifest files must be a list")
    seen = {entry.get("path") for entry in files if isinstance(entry, dict)}
    missing = sorted(REQUIRED_FILES - seen)
    _require(not missing, f"manifest missing required fixture files: {missing}")

    for entry in files:
        _validate_manifest_entry(fixture_dir, entry)

    synthesis = _read_json(fixture_dir / "workbench_synthesis_stub.json")
    _validate_synthesis(synthesis)

    for path in REQUIRED_FILES:
        payload = _read_json(fixture_dir / path)
        forbidden_fields = (
            QC_FORBIDDEN_INFERENCE_FIELDS
            if path == "qc_handoff_stub.json"
            else FORBIDDEN_GENERIC_FIELDS
        )
        _assert_no_forbidden_fields(payload, path, forbidden_fields)


def _validate_manifest_entry(fixture_dir: Path, entry: object) -> None:
    if not isinstance(entry, dict):
        raise SystemExit("ERROR: manifest file entries must be objects")
    relative_path = entry.get("path")
    _require(
        isinstance(relative_path, str) and bool(relative_path),
        "file entry path is required",
    )
    if not isinstance(relative_path, str):
        raise AssertionError("relative_path was narrowed above")
    path = fixture_dir / relative_path
    _require(path.is_file(), f"fixture file does not exist: {relative_path}")
    expected_hash = entry.get("sha256")
    _require(isinstance(expected_hash, str) and len(expected_hash) == 64, f"{relative_path} needs sha256")
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    _require(actual_hash == expected_hash, f"{relative_path} hash mismatch: {actual_hash}")
    evidence_grade = entry.get("evidence_grade")
    _require(
        evidence_grade == "C-synthetic-contract-only",
        f"{relative_path} evidence_grade must be C-synthetic-contract-only",
    )


def _validate_synthesis(payload: dict[str, Any]) -> None:
    _require(payload.get("schema_version") == 1, "synthesis schema_version must be 1")
    _require(payload.get("artifact_status") == "synthetic_contract_fixture", "synthesis must be synthetic")
    _require(
        payload.get("method_context") == "multi_method_qualitative_review",
        "method_context mismatch",
    )

    anchors = _index(payload, "source_anchors")
    evidence = _index(payload, "evidence_records")
    assertions = _index(payload, "analytic_assertions")
    patterns = _index(payload, "pattern_findings")
    hypothesis_sets = _index(payload, "causal_hypothesis_sets")

    _require(bool(anchors), "synthesis must contain source anchors")
    _require(bool(evidence), "synthesis must contain evidence records")
    _require(bool(assertions), "synthesis must contain analytic assertions")
    _require(bool(patterns), "synthesis must contain pattern findings")
    _require(bool(hypothesis_sets), "synthesis must contain causal hypothesis sets")

    for record in evidence.values():
        _require(
            record.get("evidence_kind") != "theory_operationalization",
            "theory operationalization cannot be empirical evidence",
        )
        anchor_ids = record.get("source_anchor_ids", [])
        _require(isinstance(anchor_ids, list), "source_anchor_ids must be a list")
        if not isinstance(anchor_ids, list):
            raise AssertionError("anchor_ids was narrowed above")
        for anchor_id in anchor_ids:
            _require(anchor_id in anchors, f"evidence references missing anchor: {anchor_id}")

    for assertion in assertions.values():
        _require(
            assertion.get("assertion_kind") not in {"latent_construct", "causal_edge"},
            "theory object cannot be an analytic assertion",
        )
        _require("estimand_kind" in assertion, f"assertion lacks estimand_kind: {assertion.get('id')}")
        supporting_ids = assertion.get("supporting_evidence_ids", [])
        contrary_ids = assertion.get("contrary_evidence_ids", [])
        _require(isinstance(supporting_ids, list), "supporting_evidence_ids must be a list")
        _require(isinstance(contrary_ids, list), "contrary_evidence_ids must be a list")
        if not isinstance(supporting_ids, list) or not isinstance(contrary_ids, list):
            raise AssertionError("evidence id lists were narrowed above")
        for evidence_id in supporting_ids:
            _require(evidence_id in evidence, f"assertion references missing evidence: {evidence_id}")
        for evidence_id in contrary_ids:
            _require(evidence_id in evidence, f"assertion references missing contrary evidence: {evidence_id}")

    for pattern in patterns.values():
        _require(
            pattern.get("causal_interpretation_status") in {
                "descriptive_only",
                "candidate_explanation_generated",
                "tested_by_process_tracing",
                "eligible_for_cross_case_model",
            },
            f"pattern has unsupported causal_interpretation_status: {pattern.get('id')}",
        )

    claim_limits = payload.get("claim_limits")
    _require(
        isinstance(claim_limits, list) and bool(claim_limits),
        "claim_limits are required",
    )
    if not isinstance(claim_limits, list):
        raise AssertionError("claim_limits was narrowed above")
    _require(
        any("synthetic" in str(limit).lower() for limit in claim_limits),
        "claim_limits must say the fixture is synthetic",
    )


def _index(payload: dict[str, Any], key: str) -> dict[str, dict[str, Any]]:
    rows = payload.get(key)
    if not isinstance(rows, list):
        raise SystemExit(f"ERROR: {key} must be a list")
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise SystemExit(f"ERROR: {key} rows must be objects")
        row_id = row.get("id")
        _require(isinstance(row_id, str) and bool(row_id), f"{key} row missing id")
        if not isinstance(row_id, str):
            raise AssertionError("row_id was narrowed above")
        _require(row_id not in indexed, f"duplicate id in {key}: {row_id}")
        indexed[row_id] = row
    return indexed


def _assert_no_forbidden_fields(value: Any, path: str, forbidden_fields: set[str]) -> None:
    """Reject boundary-specific category errors without banning valid PT output."""
    if isinstance(value, dict):
        for key, child in value.items():
            _require(key not in forbidden_fields, f"{path} contains forbidden field: {key}")
            _assert_no_forbidden_fields(child, path, forbidden_fields)
    elif isinstance(value, list):
        for child in value:
            _assert_no_forbidden_fields(child, path, forbidden_fields)


def _read_json(path: Path) -> dict[str, Any]:
    _require(path.is_file(), f"missing JSON file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        payload: object = json.load(handle)
    if not isinstance(payload, dict):
        raise SystemExit(f"ERROR: JSON root must be an object: {path}")
    return cast(dict[str, Any], payload)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ERROR: {message}")


if __name__ == "__main__":
    main()
