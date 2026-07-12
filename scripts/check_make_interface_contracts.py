#!/usr/bin/env python3
"""Exercise machine-facing Make targets through their real composed surface."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, cast


REPO_ROOT = Path(__file__).resolve().parents[1]
COVERAGE_REPORT = REPO_ROOT / "docs" / "coverage_report.json"
COVERAGE_REPORT_MD = REPO_ROOT / "docs" / "coverage_report.md"


def main() -> None:
    """Require pure JSON stdout and prove the print target changes no reports."""
    report_bytes_before = COVERAGE_REPORT.read_bytes()
    report_md_bytes_before = COVERAGE_REPORT_MD.read_bytes()
    result = subprocess.run(
        ["make", "--no-print-directory", "coverage-json"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SystemExit(
            "ERROR: make coverage-json failed: "
            f"stdout={result.stdout!r}; stderr={result.stderr!r}"
        )
    try:
        stdout_payload: object = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise SystemExit(
            "ERROR: make coverage-json stdout is not a single JSON document: "
            f"{error}; prefix={result.stdout[:200]!r}"
        ) from error
    if not isinstance(stdout_payload, dict):
        raise SystemExit("ERROR: make coverage-json JSON root must be an object")

    file_payload: object = json.loads(COVERAGE_REPORT.read_text(encoding="utf-8"))
    if not isinstance(file_payload, dict):
        raise SystemExit("ERROR: generated coverage_report.json root must be an object")
    if stdout_payload != file_payload:
        raise SystemExit(
            "ERROR: make coverage-json stdout differs from coverage_report.json"
        )
    if COVERAGE_REPORT.read_bytes() != report_bytes_before or (
        COVERAGE_REPORT_MD.read_bytes() != report_md_bytes_before
    ):
        raise SystemExit(
            "ERROR: make coverage-json modified a tracked coverage report"
        )
    typed_payload = cast(dict[str, Any], stdout_payload)
    if not isinstance(typed_payload.get("summary"), dict) or not isinstance(
        typed_payload.get("requirements"), list
    ):
        raise SystemExit("ERROR: coverage JSON lacks summary or requirements")

    print(
        "PASS coverage_json_stdout: one JSON document matching "
        f"{COVERAGE_REPORT.relative_to(REPO_ROOT)}"
    )


if __name__ == "__main__":
    main()
