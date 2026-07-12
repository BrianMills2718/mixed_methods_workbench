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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE_DIR = REPO_ROOT / "examples" / "fixtures" / "workbench_contract_v1"
MANIFEST_NAME = "manifest.json"
MANIFEST_SCHEMA_VERSION = 2
SUPPORTED_ORIGIN_KIND = "workbench_synthetic"
AUTHORING_REPOSITORY = "mixed_methods_workbench"
VALIDATOR_RELATIVE_PATH = Path("scripts/validate_fixtures.py")

MANIFEST_ALLOWED_FIELDS = {
    "schema_version",
    "artifact_status",
    "created",
    "purpose",
    "claim_limits",
    "files",
    "validation_observation",
    "replacement_gates",
}
MANIFEST_ENTRY_ALLOWED_FIELDS = {
    "path",
    "sha256",
    "evidence_grade",
    "origin_kind",
    "authoring_repository",
    "last_content_commit",
    "authoring_path",
    "recovery_command",
    "creation_method",
    "intended_invariant",
    "claim_limits",
}
VALIDATION_OBSERVATION_ALLOWED_FIELDS = {
    "command",
    "control_commands",
    "control_sha256",
    "control_result",
    "evidence_deriver_path",
    "evidence_deriver_sha256",
    "validator_path",
    "validator_sha256",
    "observed_at",
    "result",
    "validated_file_hashes",
}

CONTROL_RELATIVE_PATHS = (
    Path("scripts/check_fixture_negative_controls.py"),
    Path("scripts/check_coverage_negative_controls.py"),
)
EXPECTED_CONTROL_COMMANDS = [
    "python3 scripts/check_fixture_negative_controls.py",
    "python3 scripts/check_coverage_negative_controls.py",
]
EVIDENCE_DERIVER_RELATIVE_PATH = Path("scripts/check_coverage.py")

EXPECTED_MANIFEST_CREATED = "2026-06-26"
EXPECTED_MANIFEST_PURPOSE = (
    "Executable contract target for future engine-produced mixed-methods "
    "workbench fixtures."
)

EXPECTED_INVARIANTS = {
    "qc_handoff_stub.json": (
        "Qualitative handoff shape remains synthetic and excludes "
        "process-tracing inference fields."
    ),
    "pt_export_stub.json": (
        "Process-tracing comparative support remains method-scoped and source "
        "caveats remain visible."
    ),
    "theory_operationalization_stub.json": (
        "Theory operationalization remains context and a test obligation "
        "rather than empirical evidence."
    ),
    "workbench_synthesis_stub.json": (
        "Synthetic QC and PT assertions remain traceable without being "
        "mislabeled as qualitative-quantitative mixed methods."
    ),
}

EXPECTED_CLAIM_LIMITS = {
    "qc_handoff_stub.json": [
        "Synthetic contract shape only.",
        "Not a qualitative_coding engine export.",
        "Not qualitative or mixed-methods evidence.",
    ],
    "pt_export_stub.json": [
        "Synthetic contract shape only.",
        "Not a process_tracing engine export.",
        "Not process-tracing or mixed-methods evidence.",
    ],
    "theory_operationalization_stub.json": [
        "Synthetic contract shape only.",
        "Not a theory-forge engine export.",
        "Not theory validation or empirical evidence.",
    ],
    "workbench_synthesis_stub.json": [
        "Synthetic contract shape only.",
        "Not generated from real engine exports.",
        "Not research-quality or mixed-methods synthesis evidence.",
    ],
}

EXPECTED_MANIFEST_CLAIM_LIMITS = [
    "Synthetic fixture only.",
    "Not qualitative evidence.",
    "Not process-tracing evidence.",
    "Not Theory Forge validation evidence.",
    "Not mixed-methods synthesis evidence.",
]

EXPECTED_REPLACEMENT_GATES = [
    "Each real engine fixture records producer repo, producer commit, source command, package hash, caveats, and validation result.",
    "Real QC fixture validates as a strict QC handoff package and contains no process-tracing inference fields.",
    "Real PT fixture validates as pt_export_v1 and does not require parsing internal result.json.",
    "Real Theory Forge fixture validates as TheoryOperationalizationArtifact and does not require AC runtime.",
]

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
    _require_only_fields(manifest, MANIFEST_ALLOWED_FIELDS, "manifest")
    _require(
        manifest.get("schema_version") == MANIFEST_SCHEMA_VERSION,
        f"manifest schema_version must be {MANIFEST_SCHEMA_VERSION}",
    )
    _require(
        manifest.get("artifact_status") == "synthetic_contract_fixture",
        "manifest artifact_status must mark fixtures as synthetic_contract_fixture",
    )
    _require(
        manifest.get("created") == EXPECTED_MANIFEST_CREATED,
        f"manifest created must be {EXPECTED_MANIFEST_CREATED}",
    )
    _require(
        manifest.get("purpose") == EXPECTED_MANIFEST_PURPOSE,
        "manifest purpose must match the reviewed synthetic contract purpose",
    )
    _require(
        manifest.get("claim_limits") == EXPECTED_MANIFEST_CLAIM_LIMITS,
        "manifest claim_limits must match the reviewed synthetic-only exclusions",
    )
    _require(
        manifest.get("replacement_gates") == EXPECTED_REPLACEMENT_GATES,
        "manifest replacement_gates must match the reviewed real-export boundaries",
    )

    files = manifest.get("files")
    if not isinstance(files, list):
        raise SystemExit("ERROR: manifest files must be a list")

    listed_paths = [_manifest_entry_path(entry) for entry in files]
    duplicate_paths = sorted(
        path for path in set(listed_paths) if listed_paths.count(path) > 1
    )
    _require(not duplicate_paths, f"manifest has duplicate file entries: {duplicate_paths}")

    symlink_paths = sorted(
        path.relative_to(fixture_dir).as_posix()
        for path in fixture_dir.rglob("*")
        if path.is_symlink()
    )
    _require(
        not symlink_paths,
        f"fixture directory contains unsupported symlinks: {symlink_paths}",
    )
    actual_paths = {
        path.relative_to(fixture_dir).as_posix()
        for path in fixture_dir.rglob("*")
        if path.is_file()
        and path.name.casefold().endswith(".json")
        and path != fixture_dir / MANIFEST_NAME
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
    _require_only_fields(entry, MANIFEST_ENTRY_ALLOWED_FIELDS, "manifest file entry")
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
    _require(
        intended_invariant == EXPECTED_INVARIANTS.get(relative_path),
        f"{relative_path} intended_invariant must match its reviewed file-specific invariant",
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
    normalized_limits = [str(limit).strip().casefold() for limit in claim_limits]
    _require(
        any(limit.startswith("synthetic ") for limit in normalized_limits)
        and any(limit.startswith("not ") for limit in normalized_limits),
        f"{relative_path} claim_limits must disclose synthetic status and an explicit Not exclusion",
    )
    _require(
        claim_limits == EXPECTED_CLAIM_LIMITS.get(relative_path),
        f"{relative_path} claim_limits must match its reviewed file-specific exclusions",
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
    _require_only_fields(
        observation,
        VALIDATION_OBSERVATION_ALLOWED_FIELDS,
        "validation_observation",
    )
    _require(
        observation.get("command") == "python3 scripts/validate_fixtures.py",
        "validation_observation command mismatch",
    )
    _require(
        observation.get("control_commands") == EXPECTED_CONTROL_COMMANDS,
        "validation_observation control_commands mismatch",
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
    expected_control_hashes = {
        path.as_posix(): hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()
        for path in CONTROL_RELATIVE_PATHS
    }
    _require(
        observation.get("control_sha256") == expected_control_hashes,
        "validation_observation control hashes do not match current control scripts",
    )
    _require(
        observation.get("control_result") == "pass",
        "validation_observation control_result must be pass",
    )
    _require(
        observation.get("evidence_deriver_path")
        == EVIDENCE_DERIVER_RELATIVE_PATH.as_posix(),
        "validation_observation evidence_deriver_path mismatch",
    )
    expected_deriver_hash = hashlib.sha256(
        (REPO_ROOT / EVIDENCE_DERIVER_RELATIVE_PATH).read_bytes()
    ).hexdigest()
    _require(
        observation.get("evidence_deriver_sha256") == expected_deriver_hash,
        "validation_observation evidence deriver hash does not match current code",
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
        isinstance(observed_at, str),
        "validation_observation observed_at must be timezone-aware ISO 8601",
    )
    if not isinstance(observed_at, str):
        raise AssertionError("observed_at was narrowed above")
    parsed_observed_at = _parse_timezone_aware_iso8601(observed_at)
    _require(
        parsed_observed_at is not None,
        "validation_observation observed_at must be timezone-aware ISO 8601",
    )
    if parsed_observed_at is None:
        raise AssertionError("parsed_observed_at was narrowed above")
    _require(
        parsed_observed_at <= datetime.now(timezone.utc),
        "validation_observation observed_at must not be in the future",
    )
    manifest_created_at = datetime.fromisoformat(
        f"{EXPECTED_MANIFEST_CREATED}T00:00:00+00:00"
    )
    _require(
        parsed_observed_at >= manifest_created_at,
        "validation_observation observed_at must not predate manifest creation",
    )


def _parse_timezone_aware_iso8601(value: str) -> datetime | None:
    """Parse a timestamp only when it contains an explicit UTC offset."""
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


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


def _require_only_fields(
    payload: dict[str, Any],
    allowed_fields: set[str],
    context: str,
) -> None:
    """Reject undeclared fields so alternate claim surfaces cannot bypass review."""
    unknown_fields = sorted(set(payload) - allowed_fields)
    _require(
        not unknown_fields,
        f"{context} contains unknown fields: {unknown_fields}",
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
    """Read one object-root JSON file with stable fail-loud diagnostics."""
    _require(path.is_file(), f"missing JSON file: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload: object = json.load(
                handle,
                object_pairs_hook=_reject_duplicate_json_keys,
            )
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"ERROR: invalid JSON in {path.name}: {error.msg} "
            f"at line {error.lineno} column {error.colno}"
        ) from error
    except UnicodeDecodeError as error:
        raise SystemExit(
            f"ERROR: invalid UTF-8 JSON in {path.name}: byte {error.start}"
        ) from error
    if not isinstance(payload, dict):
        raise SystemExit(f"ERROR: JSON root must be an object: {path}")
    return cast(dict[str, Any], payload)


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build one JSON object while rejecting ambiguous duplicate keys."""
    payload: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in payload, f"duplicate JSON key: {key}")
        payload[key] = value
    return payload


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ERROR: {message}")


if __name__ == "__main__":
    main()
