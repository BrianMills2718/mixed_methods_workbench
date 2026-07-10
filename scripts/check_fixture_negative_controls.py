#!/usr/bin/env python3
"""Run negative controls for the workbench fixture validator."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

from validate_fixtures import DEFAULT_FIXTURE_DIR, validate_fixture_dir


Mutation = Callable[[Path], None]


def main() -> None:
    """Confirm known-invalid fixture mutations fail validation."""
    controls: list[tuple[str, Mutation, str]] = [
        (
            "forbidden_generic_confidence",
            _add_forbidden_generic_confidence,
            "contains forbidden field: generic_confidence",
        ),
        (
            "pt_support_leaked_into_qc",
            _add_comparative_support_to_qc,
            "contains forbidden field: comparative_support",
        ),
        (
            "missing_assertion_estimand",
            _remove_assertion_estimand,
            "assertion lacks estimand_kind",
        ),
        (
            "theory_presented_as_evidence",
            _add_theory_as_evidence,
            "theory operationalization cannot be empirical evidence",
        ),
        (
            "theory_presented_as_assertion",
            _add_theory_as_assertion,
            "theory object cannot be an analytic assertion",
        ),
        ("manifest_hash_mismatch", _break_manifest_hash, "hash mismatch"),
    ]
    failures: list[str] = []

    for name, mutate, expected_error in controls:
        if not _control_fails(name, mutate, expected_error):
            failures.append(name)

    if failures:
        raise SystemExit(f"ERROR: negative controls unexpectedly passed: {failures}")

    print(f"Fixture negative controls passed ({len(controls)} controls).")


def _control_fails(name: str, mutate: Mutation, expected_error: str) -> bool:
    """Return true only when the mutation reaches its intended validator gate."""
    with tempfile.TemporaryDirectory(prefix=f"mmw-negative-{name}-") as temp_dir:
        fixture_dir = Path(temp_dir) / "fixture"
        shutil.copytree(DEFAULT_FIXTURE_DIR, fixture_dir)
        mutate(fixture_dir)
        try:
            validate_fixture_dir(fixture_dir)
        except SystemExit as error:
            return expected_error in str(error)
        return False


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
            entry["sha256"] = hashlib.sha256(
                (fixture_dir / fixture_name).read_bytes()
            ).hexdigest()
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
