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
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, cast


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE_DIR = REPO_ROOT / "examples" / "fixtures" / "workbench_contract_v1"
MANIFEST_NAME = "manifest.json"
MANIFEST_SCHEMA_VERSION = 2
SUPPORTED_ORIGIN_KIND = "workbench_synthetic"
AUTHORING_REPOSITORY = "mixed_methods_workbench"
VALIDATOR_RELATIVE_PATH = Path("scripts/validate_fixtures.py")

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


def validate_fixture_dir(
    fixture_dir: Path,
    *,
    verify_repository_provenance: bool = True,
) -> None:
    """Validate one fixture directory and its recoverable source evidence.

    Repository provenance may be disabled only by semantic negative controls
    whose temporary byte mutation cannot exist in Git. Production validation
    always uses the default and verifies the exact last-content commit.
    """
    manifest = _read_json(fixture_dir / MANIFEST_NAME)
    _require(
        manifest.get("schema_version") == MANIFEST_SCHEMA_VERSION,
        f"manifest schema_version must be {MANIFEST_SCHEMA_VERSION}",
    )
    _require(
        manifest.get("artifact_status") == "synthetic_contract_fixture",
        "manifest artifact_status must mark fixtures as synthetic_contract_fixture",
    )

    files = manifest.get("files")
    if not isinstance(files, list):
        raise SystemExit("ERROR: manifest files must be a list")

    listed_paths = [_manifest_entry_path(entry) for entry in files]
    duplicate_paths = sorted(
        path for path in set(listed_paths) if listed_paths.count(path) > 1
    )
    _require(not duplicate_paths, f"manifest has duplicate file entries: {duplicate_paths}")

    actual_paths = {
        path.name
        for path in fixture_dir.glob("*.json")
        if path.name != MANIFEST_NAME
    }
    listed_path_set = set(listed_paths)
    missing_required = sorted(REQUIRED_FILES - actual_paths)
    _require(
        not missing_required,
        f"fixture directory missing required files: {missing_required}",
    )
    unlisted = sorted(actual_paths - listed_path_set)
    _require(not unlisted, f"manifest has unlisted JSON fixture files: {unlisted}")
    listed_missing = sorted(listed_path_set - actual_paths)
    _require(
        not listed_missing,
        f"manifest lists missing JSON fixture files: {listed_missing}",
    )

    entry_hashes: dict[str, str] = {}

    for entry in files:
        relative_path, actual_hash = _validate_manifest_entry(
            fixture_dir,
            entry,
            verify_repository_provenance=verify_repository_provenance,
        )
        entry_hashes[relative_path] = actual_hash

    _validate_validation_observation(manifest, entry_hashes)

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


def _manifest_entry_path(entry: object) -> str:
    """Return one safe manifest path before inventory set comparison."""
    if not isinstance(entry, dict):
        raise SystemExit("ERROR: manifest file entries must be objects")
    relative_path = entry.get("path")
    _require(
        isinstance(relative_path, str) and bool(relative_path),
        "file entry path is required",
    )
    if not isinstance(relative_path, str):
        raise AssertionError("relative_path was narrowed above")
    _require(
        Path(relative_path).name == relative_path
        and relative_path.endswith(".json")
        and relative_path != MANIFEST_NAME,
        f"file entry path must be a fixture JSON filename: {relative_path}",
    )
    return relative_path


def _validate_manifest_entry(
    fixture_dir: Path,
    entry: object,
    *,
    verify_repository_provenance: bool,
) -> tuple[str, str]:
    """Validate one synthetic entry and return its current content identity."""
    relative_path = _manifest_entry_path(entry)
    if not isinstance(entry, dict):
        raise AssertionError("entry was narrowed by _manifest_entry_path")
    path = fixture_dir / relative_path
    _require(path.is_file(), f"fixture file does not exist: {relative_path}")
    expected_hash = entry.get("sha256")
    _require(
        isinstance(expected_hash, str)
        and re.fullmatch(r"[0-9a-f]{64}", expected_hash) is not None,
        f"{relative_path} needs lowercase sha256",
    )
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    _require(actual_hash == expected_hash, f"{relative_path} hash mismatch: {actual_hash}")
    evidence_grade = entry.get("evidence_grade")
    _require(
        evidence_grade == "C-synthetic-contract-only",
        f"{relative_path} evidence_grade must be C-synthetic-contract-only",
    )
    _validate_synthetic_origin(
        entry,
        relative_path=relative_path,
        current_hash=actual_hash,
        verify_repository_provenance=verify_repository_provenance,
    )
    return relative_path, actual_hash


def _validate_synthetic_origin(
    entry: dict[str, Any],
    *,
    relative_path: str,
    current_hash: str,
    verify_repository_provenance: bool,
) -> None:
    """Require truthful, Git-recoverable provenance for a synthetic fixture."""
    origin_kind = entry.get("origin_kind")
    _require(
        origin_kind == SUPPORTED_ORIGIN_KIND,
        f"{relative_path} origin_kind must be {SUPPORTED_ORIGIN_KIND}",
    )
    _require(
        entry.get("authoring_repository") == AUTHORING_REPOSITORY,
        f"{relative_path} authoring_repository must be {AUTHORING_REPOSITORY}",
    )
    _require(
        entry.get("creation_method") == "hand_authored_synthetic_contract_fixture",
        f"{relative_path} creation_method must identify hand-authored synthetic data",
    )
    intended_invariant = entry.get("intended_invariant")
    _require(
        isinstance(intended_invariant, str) and bool(intended_invariant.strip()),
        f"{relative_path} intended_invariant is required",
    )
    claim_limits = entry.get("claim_limits")
    _require(
        isinstance(claim_limits, list)
        and bool(claim_limits)
        and all(isinstance(limit, str) and bool(limit.strip()) for limit in claim_limits),
        f"{relative_path} claim_limits must be a non-empty string list",
    )
    if not isinstance(claim_limits, list):
        raise AssertionError("claim_limits was narrowed above")
    normalized_limits = " ".join(str(limit).lower() for limit in claim_limits)
    _require(
        "synthetic" in normalized_limits and "not" in normalized_limits,
        f"{relative_path} claim_limits must disclose synthetic status and exclusions",
    )

    canonical_fixture_dir = DEFAULT_FIXTURE_DIR.relative_to(REPO_ROOT)
    expected_authoring_path = (canonical_fixture_dir / relative_path).as_posix()
    authoring_path = entry.get("authoring_path")
    _require(
        authoring_path == expected_authoring_path,
        f"{relative_path} authoring_path must be {expected_authoring_path}",
    )
    last_content_commit = entry.get("last_content_commit")
    _require(
        isinstance(last_content_commit, str)
        and re.fullmatch(r"[0-9a-f]{40}", last_content_commit) is not None,
        f"{relative_path} last_content_commit must be a full Git commit",
    )
    if not isinstance(last_content_commit, str):
        raise AssertionError("last_content_commit was narrowed above")
    expected_recovery_command = f"git show {last_content_commit}:{expected_authoring_path}"
    _require(
        entry.get("recovery_command") == expected_recovery_command,
        f"{relative_path} recovery_command must be {expected_recovery_command}",
    )

    if not verify_repository_provenance:
        return

    observed_last_commit = _run_git_text(
        "log",
        "-1",
        "--format=%H",
        "--",
        expected_authoring_path,
    ).strip()
    _require(
        observed_last_commit == last_content_commit,
        f"{relative_path} last_content_commit mismatch: {observed_last_commit}",
    )
    recovered_bytes = _run_git_bytes(
        "show",
        f"{last_content_commit}:{expected_authoring_path}",
    )
    recovered_hash = hashlib.sha256(recovered_bytes).hexdigest()
    _require(
        recovered_hash == current_hash,
        f"{relative_path} recovered Git bytes hash mismatch: {recovered_hash}",
    )


def _validate_validation_observation(
    manifest: dict[str, Any],
    entry_hashes: dict[str, str],
) -> None:
    """Bind the stored validation observation to current files and validator."""
    observation = manifest.get("validation_observation")
    _require(
        isinstance(observation, dict),
        "manifest validation_observation must be an object",
    )
    if not isinstance(observation, dict):
        raise AssertionError("observation was narrowed above")
    _require(
        observation.get("command") == "python3 scripts/validate_fixtures.py",
        "validation_observation command mismatch",
    )
    _require(
        observation.get("negative_control_command")
        == "python3 scripts/check_fixture_negative_controls.py",
        "validation_observation negative_control_command mismatch",
    )
    _require(
        observation.get("validator_path") == VALIDATOR_RELATIVE_PATH.as_posix(),
        "validation_observation validator_path mismatch",
    )
    expected_validator_hash = observation.get("validator_sha256")
    _require(
        isinstance(expected_validator_hash, str)
        and re.fullmatch(r"[0-9a-f]{64}", expected_validator_hash) is not None,
        "validation_observation validator_sha256 is required",
    )
    validator_hash = hashlib.sha256(
        (REPO_ROOT / VALIDATOR_RELATIVE_PATH).read_bytes()
    ).hexdigest()
    _require(
        validator_hash == expected_validator_hash,
        f"validation_observation validator hash mismatch: {validator_hash}",
    )
    _require(
        observation.get("validated_file_hashes") == entry_hashes,
        "validation_observation file hashes do not match current manifest entries",
    )
    _require(
        observation.get("result") == "pass",
        "validation_observation result must be pass",
    )
    observed_at = observation.get("observed_at")
    _require(
        isinstance(observed_at, str) and _is_timezone_aware_iso8601(observed_at),
        "validation_observation observed_at must be timezone-aware ISO 8601",
    )


def _is_timezone_aware_iso8601(value: str) -> bool:
    """Return whether a timestamp parses and contains an explicit UTC offset."""
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _run_git_text(*args: str) -> str:
    """Run one read-only Git command and return text or fail loudly."""
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def _run_git_bytes(*args: str) -> bytes:
    """Run one read-only Git command and return exact bytes or fail loudly."""
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


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
