#!/usr/bin/env python3
"""Run negative controls for the workbench fixture validator."""

from __future__ import annotations

import json
import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path

from validate_fixtures import DEFAULT_FIXTURE_DIR, validate_fixture_dir


Mutation = Callable[[Path], None]


def main() -> None:
    """Confirm known-invalid fixture mutations fail validation."""
    controls: list[tuple[str, Mutation]] = [
        ("forbidden_generic_confidence", _add_forbidden_generic_confidence),
        ("missing_assertion_estimand", _remove_assertion_estimand),
        ("manifest_hash_mismatch", _break_manifest_hash),
    ]
    failures: list[str] = []

    for name, mutate in controls:
        if not _control_fails(name, mutate):
            failures.append(name)

    if failures:
        raise SystemExit(f"ERROR: negative controls unexpectedly passed: {failures}")

    print(f"Fixture negative controls passed ({len(controls)} controls).")


def _control_fails(name: str, mutate: Mutation) -> bool:
    with tempfile.TemporaryDirectory(prefix=f"mmw-negative-{name}-") as temp_dir:
        fixture_dir = Path(temp_dir) / "fixture"
        shutil.copytree(DEFAULT_FIXTURE_DIR, fixture_dir)
        mutate(fixture_dir)
        try:
            validate_fixture_dir(fixture_dir)
        except SystemExit:
            return True
        return False


def _add_forbidden_generic_confidence(fixture_dir: Path) -> None:
    path = fixture_dir / "qc_handoff_stub.json"
    payload = _read_json(path)
    payload["generic_confidence"] = 0.9
    _write_json(path, payload)


def _remove_assertion_estimand(fixture_dir: Path) -> None:
    path = fixture_dir / "workbench_synthesis_stub.json"
    payload = _read_json(path)
    del payload["analytic_assertions"][0]["estimand_kind"]
    _write_json(path, payload)


def _break_manifest_hash(fixture_dir: Path) -> None:
    path = fixture_dir / "manifest.json"
    payload = _read_json(path)
    payload["files"][0]["sha256"] = "0" * 64
    _write_json(path, payload)


def _read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise TypeError(f"Expected object JSON root: {path}")
    return payload


def _write_json(path: Path, payload: dict) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
