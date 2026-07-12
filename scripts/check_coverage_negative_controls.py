#!/usr/bin/env python3
"""Prove the W2 coverage grade changes when its evidence is removed."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from check_coverage import (
    build_report,
    check_generated_reports,
    derive_fixture_inventory_requirement,
)
from validate_fixtures import DEFAULT_FIXTURE_DIR


def main() -> None:
    """Run the real positive path and one evidence-removal negative control."""
    positive = derive_fixture_inventory_requirement()
    if positive.evidence_grade != "A":
        raise SystemExit(
            "ERROR: canonical W2 positive control did not derive A: "
            f"{positive.evidence_notes}"
        )
    print(f"PASS w2_evidence_present: {positive.evidence_notes}")

    with tempfile.TemporaryDirectory(prefix="mmw-coverage-missing-evidence-") as temp_dir:
        fixture_dir = Path(temp_dir) / "fixture"
        shutil.copytree(DEFAULT_FIXTURE_DIR, fixture_dir)
        manifest_path = fixture_dir / "manifest.json"
        manifest = _read_json(manifest_path)
        del manifest["validation_observation"]
        _write_json(manifest_path, manifest)

        negative = derive_fixture_inventory_requirement(fixture_dir)
        expected = "manifest validation_observation must be an object"
        if negative.evidence_grade != "F" or expected not in negative.evidence_notes:
            raise SystemExit(
                "ERROR: W2 evidence-removal control reached wrong result: "
                f"grade={negative.evidence_grade}; notes={negative.evidence_notes}"
            )
        print(f"PASS w2_evidence_removed: {negative.evidence_notes}")

    with tempfile.TemporaryDirectory(prefix="mmw-coverage-stale-report-") as temp_dir:
        temp_path = Path(temp_dir)
        report_md = temp_path / "coverage_report.md"
        report_json = temp_path / "coverage_report.json"
        report_md.write_text("stale markdown\n", encoding="utf-8")
        report_json.write_text('{"stale": true}\n', encoding="utf-8")
        try:
            check_generated_reports(
                build_report(),
                report_md=report_md,
                report_json=report_json,
            )
        except SystemExit as error:
            expected = "generated coverage reports are stale or missing"
            if expected not in str(error):
                raise SystemExit(
                    "ERROR: stale-report control reached wrong diagnostic: "
                    f"{error}"
                ) from error
            print(f"PASS stale_generated_reports: {error}")
        else:
            raise SystemExit("ERROR: stale generated coverage reports passed")

    print("Coverage negative controls passed (2 controls).")


def _read_json(path: Path) -> dict[str, Any]:
    """Read one object-root JSON document used by the temporary control."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"Expected object JSON root: {path}")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write a deterministic temporary control document."""
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
