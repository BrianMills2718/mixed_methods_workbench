#!/usr/bin/env python3
"""Run negative controls for the workbench fixture validator."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from validate_fixtures import DEFAULT_FIXTURE_DIR, REPO_ROOT, validate_fixture_dir


Mutation = Callable[[Path], None]


def run_negative_controls(*, emit_diagnostics: bool = True) -> int:
    """Run every fixture control and return the executed control count."""
    controls: list[tuple[str, Mutation, str, bool]] = [
        (
            "forbidden_generic_confidence",
            _add_forbidden_generic_confidence,
            "contains forbidden field: generic_confidence",
            False,
        ),
        (
            "pt_support_leaked_into_qc",
            _add_comparative_support_to_qc,
            "contains forbidden field: comparative_support",
            False,
        ),
        (
            "missing_assertion_estimand",
            _remove_assertion_estimand,
            "assertion lacks estimand_kind",
            False,
        ),
        (
            "theory_presented_as_evidence",
            _add_theory_as_evidence,
            "theory operationalization cannot be empirical evidence",
            False,
        ),
        (
            "theory_presented_as_assertion",
            _add_theory_as_assertion,
            "theory object cannot be an analytic assertion",
            False,
        ),
        ("manifest_hash_mismatch", _break_manifest_hash, "hash mismatch", False),
        (
            "unlisted_json_artifact",
            _add_unlisted_json_artifact,
            "manifest has unlisted JSON fixture files: ['unlisted_stub.json']",
            False,
        ),
        (
            "nested_unlisted_json_artifact",
            _add_nested_unlisted_json_artifact,
            "manifest has unlisted JSON fixture files: ['nested/unlisted.json']",
            False,
        ),
        (
            "uppercase_nested_unlisted_json_artifact",
            _add_uppercase_nested_unlisted_json_artifact,
            "manifest has unlisted JSON fixture files: ['two/levels/rogue.JSON']",
            False,
        ),
        (
            "dotfile_json_artifact",
            _add_dotfile_json_artifact,
            "manifest has unlisted JSON fixture files: ['.JSON']",
            False,
        ),
        (
            "missing_manifest_entry",
            _remove_manifest_entry,
            "manifest has unlisted JSON fixture files: ['qc_handoff_stub.json']",
            False,
        ),
        (
            "listed_missing_artifact",
            _add_listed_missing_artifact,
            "manifest lists missing JSON fixture files: ['ghost_stub.json']",
            False,
        ),
        (
            "duplicate_manifest_entry",
            _duplicate_manifest_entry,
            "manifest has duplicate file entries: ['qc_handoff_stub.json']",
            False,
        ),
        (
            "duplicate_json_key",
            _add_duplicate_json_key,
            "duplicate JSON key: purpose",
            False,
        ),
        (
            "malformed_manifest_json",
            _malform_manifest_json,
            "invalid JSON in manifest.json",
            False,
        ),
        (
            "fixture_directory_symlink",
            _add_fixture_directory_symlink,
            "fixture directory contains unsupported symlinks: ['linked']",
            False,
        ),
        (
            "missing_origin_kind",
            _remove_origin_kind,
            "origin_kind must be workbench_synthetic",
            False,
        ),
        (
            "unsupported_origin_kind",
            _set_unsupported_origin_kind,
            "origin_kind must be workbench_synthetic",
            False,
        ),
        (
            "missing_claim_limits",
            _remove_claim_limits,
            "claim_limits must be a non-empty string list",
            False,
        ),
        (
            "not_substring_is_not_exclusion",
            _replace_limits_with_not_substring,
            "claim_limits must disclose synthetic status and an explicit Not exclusion",
            False,
        ),
        (
            "generic_claim_limits",
            _replace_limits_with_generic_exclusions,
            "claim_limits must match its reviewed file-specific exclusions",
            False,
        ),
        (
            "second_entry_generic_claim_limits",
            _replace_second_entry_limits_with_generic_exclusions,
            "pt_export_stub.json claim_limits must match its reviewed file-specific exclusions",
            False,
        ),
        (
            "contradictory_claim_limits",
            _replace_limits_with_contradiction,
            "claim_limits must match its reviewed file-specific exclusions",
            False,
        ),
        (
            "generic_intended_invariant",
            _replace_invariant_with_generic_text,
            "intended_invariant must match its reviewed file-specific invariant",
            False,
        ),
        (
            "synthetic_grade_escalation",
            _escalate_synthetic_grade,
            "evidence_grade must be C-synthetic-contract-only",
            False,
        ),
        (
            "manifest_claim_escalation",
            _escalate_manifest_claims,
            "manifest claim_limits must match the reviewed synthetic-only exclusions",
            False,
        ),
        (
            "manifest_purpose_escalation",
            _escalate_manifest_purpose,
            "manifest purpose must match the reviewed synthetic contract purpose",
            False,
        ),
        (
            "manifest_replacement_gate_escalation",
            _escalate_replacement_gate,
            "manifest replacement_gates must match the reviewed real-export boundaries",
            False,
        ),
        (
            "entry_unknown_readiness_claim",
            _add_entry_readiness_claim,
            "manifest file entry contains unknown fields: ['readiness_claim']",
            False,
        ),
        (
            "manifest_unknown_readiness_claim",
            _add_manifest_readiness_claim,
            "manifest contains unknown fields: ['readiness_claim']",
            False,
        ),
        (
            "arbitrary_head_as_content_commit",
            _replace_content_commit_with_head,
            "last_content_commit mismatch",
            True,
        ),
        (
            "recovered_bytes_differ",
            _change_fixture_bytes_without_git_source,
            "recovered Git bytes hash mismatch",
            True,
        ),
        (
            "stale_validation_file_hash",
            _stale_validation_file_hash,
            "validation_observation file hashes do not match current manifest entries",
            False,
        ),
        (
            "stale_validator_hash",
            _stale_validator_hash,
            "validation_observation validator hash mismatch",
            False,
        ),
        (
            "stale_control_hash",
            _stale_control_hash,
            "validation_observation control hashes do not match current control scripts",
            False,
        ),
        (
            "missing_control_result",
            _remove_control_result,
            "validation_observation control_result must be pass",
            False,
        ),
        (
            "stale_evidence_deriver_hash",
            _stale_evidence_deriver_hash,
            "validation_observation evidence deriver hash does not match current code",
            False,
        ),
        (
            "missing_validation_observation",
            _remove_validation_observation,
            "manifest validation_observation must be an object",
            False,
        ),
        (
            "future_validation_observation",
            _set_future_validation_observation,
            "validation_observation observed_at must not be in the future",
            False,
        ),
        (
            "predates_manifest_validation_observation",
            _set_predates_manifest_validation_observation,
            "validation_observation observed_at must not predate manifest creation",
            False,
        ),
    ]
    for name, mutate, expected_error, verify_repository_provenance in controls:
        diagnostic = _run_control(
            name,
            mutate,
            expected_error,
            verify_repository_provenance=verify_repository_provenance,
        )
        if emit_diagnostics:
            print(f"PASS {name}: {diagnostic}")

    if emit_diagnostics:
        print(f"Fixture negative controls passed ({len(controls)} controls).")
    return len(controls)


def main() -> None:
    """Confirm known-invalid fixture mutations fail validation."""
    run_negative_controls()


def _run_control(
    name: str,
    mutate: Mutation,
    expected_error: str,
    *,
    verify_repository_provenance: bool,
) -> str:
    """Return the exact diagnostic only when a control reaches its target."""
    with tempfile.TemporaryDirectory(prefix=f"mmw-negative-{name}-") as temp_dir:
        fixture_dir = Path(temp_dir) / "fixture"
        shutil.copytree(DEFAULT_FIXTURE_DIR, fixture_dir)
        mutate(fixture_dir)
        try:
            validate_fixture_dir(
                fixture_dir,
                verify_repository_provenance=verify_repository_provenance,
            )
        except SystemExit as error:
            diagnostic = str(error)
            if expected_error not in diagnostic:
                raise SystemExit(
                    f"ERROR: negative control {name} reached wrong diagnostic: "
                    f"{diagnostic}"
                ) from error
            return diagnostic
        raise SystemExit(f"ERROR: negative control unexpectedly passed: {name}")


def _add_forbidden_generic_confidence(fixture_dir: Path) -> None:
    path = fixture_dir / "qc_handoff_stub.json"
    payload = _read_json(path)
    payload["generic_confidence"] = 0.9
    _write_json(path, payload)
    _refresh_manifest_hash(fixture_dir, path.name)


def _remove_assertion_estimand(fixture_dir: Path) -> None:
    path = fixture_dir / "workbench_synthesis_stub.json"
    payload = _read_json(path)
    del payload["analytic_assertions"][0]["estimand_kind"]
    _write_json(path, payload)
    _refresh_manifest_hash(fixture_dir, path.name)


def _add_comparative_support_to_qc(fixture_dir: Path) -> None:
    path = fixture_dir / "qc_handoff_stub.json"
    payload = _read_json(path)
    payload["comparative_support"] = {"invalid": "PT inference leaked into QC"}
    _write_json(path, payload)
    _refresh_manifest_hash(fixture_dir, path.name)


def _break_manifest_hash(fixture_dir: Path) -> None:
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["files"][0]["sha256"] = "0" * 64
    _write_json(path, payload)


def _add_unlisted_json_artifact(fixture_dir: Path) -> None:
    """Add a valid JSON artifact that the manifest does not list."""
    _write_json(fixture_dir / "unlisted_stub.json", {"synthetic": True})


def _add_nested_unlisted_json_artifact(fixture_dir: Path) -> None:
    """Add an unlisted JSON artifact below the fixture root."""
    nested_dir = fixture_dir / "nested"
    nested_dir.mkdir()
    _write_json(nested_dir / "unlisted.json", {"synthetic": True})


def _add_uppercase_nested_unlisted_json_artifact(fixture_dir: Path) -> None:
    """Add a deeply nested case-variant JSON artifact outside the inventory."""
    nested_dir = fixture_dir / "two" / "levels"
    nested_dir.mkdir(parents=True)
    _write_json(nested_dir / "rogue.JSON", {"synthetic": True})


def _add_dotfile_json_artifact(fixture_dir: Path) -> None:
    """Add a case-variant JSON dotfile whose suffix API returns empty."""
    _write_json(fixture_dir / ".JSON", {"synthetic": True})


def _remove_manifest_entry(fixture_dir: Path) -> None:
    """Remove one real artifact entry while leaving its file in place."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["files"] = [
        entry
        for entry in payload["files"]
        if entry["path"] != "qc_handoff_stub.json"
    ]
    _write_json(path, payload)


def _add_listed_missing_artifact(fixture_dir: Path) -> None:
    """List an artifact that does not exist on disk."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["files"].append({"path": "ghost_stub.json"})
    _write_json(path, payload)


def _duplicate_manifest_entry(fixture_dir: Path) -> None:
    """Duplicate a real entry so set-based inventory cannot hide it."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["files"].append(dict(payload["files"][0]))
    _write_json(path, payload)


def _add_duplicate_json_key(fixture_dir: Path) -> None:
    """Create an ambiguous manifest with two purpose keys."""
    path = fixture_dir / "manifest.json"
    text = path.read_text(encoding="utf-8")
    duplicate = '  "purpose": "This proves SOTA readiness.",\n'
    path.write_text(
        text.replace('  "purpose":', duplicate + '  "purpose":', 1),
        encoding="utf-8",
    )


def _malform_manifest_json(fixture_dir: Path) -> None:
    """Break JSON syntax so parse failures follow the public error contract."""
    path = fixture_dir / "manifest.json"
    path.write_text('{"schema_version": 2,\n', encoding="utf-8")


def _add_fixture_directory_symlink(fixture_dir: Path) -> None:
    """Add a symlink so inventory traversal semantics cannot be ambiguous."""
    target = fixture_dir / "symlink-target"
    target.mkdir()
    (fixture_dir / "linked").symlink_to(target, target_is_directory=True)


def _remove_origin_kind(fixture_dir: Path) -> None:
    """Remove the discriminator that distinguishes synthetic provenance."""
    _mutate_first_entry(fixture_dir, lambda entry: entry.pop("origin_kind"))


def _set_unsupported_origin_kind(fixture_dir: Path) -> None:
    """Pretend the synthetic artifact is a not-yet-supported engine export."""
    _mutate_first_entry(
        fixture_dir,
        lambda entry: entry.__setitem__("origin_kind", "engine_export"),
    )


def _remove_claim_limits(fixture_dir: Path) -> None:
    """Remove file-specific exclusions from one inventory entry."""
    _mutate_first_entry(fixture_dir, lambda entry: entry.pop("claim_limits"))


def _replace_limits_with_not_substring(fixture_dir: Path) -> None:
    """Use a word containing 'not' without an explicit exclusion statement."""
    _mutate_first_entry(
        fixture_dir,
        lambda entry: entry.__setitem__(
            "claim_limits",
            ["Synthetic notebook shape only."],
        ),
    )


def _replace_limits_with_generic_exclusions(fixture_dir: Path) -> None:
    """Replace reviewed file-specific limits with generic valid-looking prose."""
    _mutate_first_entry(
        fixture_dir,
        lambda entry: entry.__setitem__(
            "claim_limits",
            ["Synthetic fixture only.", "Not real evidence."],
        ),
    )


def _replace_second_entry_limits_with_generic_exclusions(fixture_dir: Path) -> None:
    """Apply the generic-limit held-out to a non-first manifest entry."""
    _mutate_entry(
        fixture_dir,
        "pt_export_stub.json",
        lambda entry: entry.__setitem__(
            "claim_limits",
            ["Synthetic fixture only.", "Not real evidence."],
        ),
    )


def _replace_limits_with_contradiction(fixture_dir: Path) -> None:
    """Combine a synthetic declaration with a contradictory exclusion."""
    _mutate_first_entry(
        fixture_dir,
        lambda entry: entry.__setitem__(
            "claim_limits",
            ["Synthetic fixture only.", "Not synthetic."],
        ),
    )


def _replace_invariant_with_generic_text(fixture_dir: Path) -> None:
    """Replace a reviewed per-file invariant with generic non-empty text."""
    _mutate_first_entry(
        fixture_dir,
        lambda entry: entry.__setitem__(
            "intended_invariant",
            "Synthetic fixture remains valid.",
        ),
    )


def _escalate_synthetic_grade(fixture_dir: Path) -> None:
    """Attempt to promote synthetic shape evidence above C."""
    _mutate_first_entry(
        fixture_dir,
        lambda entry: entry.__setitem__("evidence_grade", "A"),
    )


def _escalate_manifest_claims(fixture_dir: Path) -> None:
    """Replace global exclusions with an unsupported readiness claim."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["claim_limits"] = [
        "This proves SOTA mixed-methods engine readiness."
    ]
    _write_json(path, payload)


def _escalate_manifest_purpose(fixture_dir: Path) -> None:
    """Replace the reviewed purpose with a product-readiness claim."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["purpose"] = (
        "This proves mixed-methods engine readiness and SOTA quality."
    )
    _write_json(path, payload)


def _escalate_replacement_gate(fixture_dir: Path) -> None:
    """Replace a future boundary with an unsupported current-ready assertion."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["replacement_gates"][0] = "All producers are ready now."
    _write_json(path, payload)


def _add_entry_readiness_claim(fixture_dir: Path) -> None:
    """Add an undeclared claim surface to one file entry."""
    _mutate_first_entry(
        fixture_dir,
        lambda entry: entry.__setitem__(
            "readiness_claim",
            "This is a real process-tracing export.",
        ),
    )


def _add_manifest_readiness_claim(fixture_dir: Path) -> None:
    """Add an undeclared claim surface to the manifest envelope."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["readiness_claim"] = "This workbench is SOTA."
    _write_json(path, payload)


def _replace_content_commit_with_head(fixture_dir: Path) -> None:
    """Substitute arbitrary current HEAD for the exact content commit."""
    head = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    def mutate(entry: dict[str, Any]) -> None:
        entry["last_content_commit"] = head
        entry["recovery_command"] = (
            f"git show {head}:{entry['authoring_path']}"
        )

    _mutate_first_entry(fixture_dir, mutate)


def _change_fixture_bytes_without_git_source(fixture_dir: Path) -> None:
    """Change valid JSON bytes while keeping the recorded Git source fixed."""
    path = fixture_dir / "qc_handoff_stub.json"
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    _refresh_manifest_hash(fixture_dir, path.name)


def _stale_validation_file_hash(fixture_dir: Path) -> None:
    """Make the stored observation refer to different fixture bytes."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["validation_observation"]["validated_file_hashes"][
        "qc_handoff_stub.json"
    ] = "0" * 64
    _write_json(path, payload)


def _stale_validator_hash(fixture_dir: Path) -> None:
    """Make the stored observation refer to different validator bytes."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["validation_observation"]["validator_sha256"] = "0" * 64
    _write_json(path, payload)


def _stale_control_hash(fixture_dir: Path) -> None:
    """Make the observation refer to different negative-control code."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    first_control = sorted(
        payload["validation_observation"]["control_sha256"]
    )[0]
    payload["validation_observation"]["control_sha256"][first_control] = "0" * 64
    _write_json(path, payload)


def _remove_control_result(fixture_dir: Path) -> None:
    """Remove the recorded result for the hash-bound control programs."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    del payload["validation_observation"]["control_result"]
    _write_json(path, payload)


def _stale_evidence_deriver_hash(fixture_dir: Path) -> None:
    """Make the observation refer to different coverage-derivation code."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["validation_observation"]["evidence_deriver_sha256"] = "0" * 64
    _write_json(path, payload)


def _remove_validation_observation(fixture_dir: Path) -> None:
    """Remove the byte-bound validation observation entirely."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    del payload["validation_observation"]
    _write_json(path, payload)


def _set_future_validation_observation(fixture_dir: Path) -> None:
    """Move an otherwise valid observation into the future."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["validation_observation"]["observed_at"] = "2099-01-01T00:00:00+00:00"
    _write_json(path, payload)


def _set_predates_manifest_validation_observation(fixture_dir: Path) -> None:
    """Set a valid timestamp that predates the manifest itself."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["validation_observation"]["observed_at"] = "2000-01-01T00:00:00+00:00"
    _write_json(path, payload)


def _mutate_first_entry(
    fixture_dir: Path,
    mutate: Callable[[dict[str, Any]], object],
) -> None:
    """Apply one manifest-only mutation to the first fixture entry."""
    _mutate_entry(fixture_dir, "qc_handoff_stub.json", mutate)


def _mutate_entry(
    fixture_dir: Path,
    fixture_name: str,
    mutate: Callable[[dict[str, Any]], object],
) -> None:
    """Apply one manifest-only mutation to a named fixture entry."""
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    for entry in payload["files"]:
        if entry["path"] == fixture_name:
            mutate(entry)
            _write_json(path, payload)
            return
    raise KeyError(f"Manifest does not inventory fixture: {fixture_name}")


def _add_theory_as_evidence(fixture_dir: Path) -> None:
    path = fixture_dir / "workbench_synthesis_stub.json"
    payload = _read_json(path)
    payload["evidence_records"].append(
        {
            "id": "ev_invalid_theory",
            "evidence_kind": "theory_operationalization",
            "description": "Invalid theory-as-evidence control.",
            "source_anchor_ids": [],
            "limitations": [],
        }
    )
    _write_json(path, payload)
    _refresh_manifest_hash(fixture_dir, path.name)


def _add_theory_as_assertion(fixture_dir: Path) -> None:
    path = fixture_dir / "workbench_synthesis_stub.json"
    payload = _read_json(path)
    payload["analytic_assertions"].append(
        {
            "id": "assert_invalid_theory",
            "assertion_kind": "latent_construct",
            "text": "Invalid theory-as-assertion control.",
            "estimand_kind": "generative_theory_model",
            "scope_id": "scope_synthetic_001",
            "supporting_evidence_ids": [],
            "contrary_evidence_ids": [],
            "status": "draft",
        }
    )
    _write_json(path, payload)
    _refresh_manifest_hash(fixture_dir, path.name)


def _refresh_manifest_hash(fixture_dir: Path, fixture_name: str) -> None:
    """Keep integrity checks neutral so a semantic control reaches its target."""
    manifest_path = fixture_dir / "manifest.json"
    manifest = _read_json(manifest_path)
    for entry in manifest["files"]:
        if entry["path"] == fixture_name:
            fixture_hash = hashlib.sha256(
                (fixture_dir / fixture_name).read_bytes()
            ).hexdigest()
            entry["sha256"] = fixture_hash
            manifest["validation_observation"]["validated_file_hashes"][
                fixture_name
            ] = fixture_hash
            _write_json(manifest_path, manifest)
            return
    raise KeyError(f"Manifest does not inventory fixture: {fixture_name}")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise TypeError(f"Expected object JSON root: {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
