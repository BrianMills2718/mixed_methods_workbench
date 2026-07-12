#!/usr/bin/env python3
"""Prove the W2 coverage grade changes when its evidence is removed."""

from __future__ import annotations

import tempfile
from pathlib import Path

from check_coverage import (
    build_report,
    check_generated_reports,
    run_w2_evidence_removal_control,
    run_w2_malformed_json_control,
)


def main() -> None:
    """Run the real positive path and one evidence-removal negative control."""
    report = build_report()
    positive = next(
        row
        for row in report["requirements"]
        if row["id"] == "W2-fixture-inventory"
    )
    if positive["evidence_grade"] != "A":
        raise SystemExit(
            "ERROR: canonical W2 positive control did not derive A: "
            f"{positive['evidence_notes']}"
        )
    print(f"PASS w2_evidence_present: {positive['evidence_notes']}")

    diagnostic = run_w2_evidence_removal_control()
    print(f"PASS w2_evidence_removed: {diagnostic}")

    malformed_diagnostic = run_w2_malformed_json_control()
    print(f"PASS w2_malformed_json: {malformed_diagnostic}")

    with tempfile.TemporaryDirectory(prefix="mmw-coverage-stale-report-") as temp_dir:
        temp_path = Path(temp_dir)
        report_md = temp_path / "coverage_report.md"
        report_json = temp_path / "coverage_report.json"
        report_md.write_text("stale markdown\n", encoding="utf-8")
        report_json.write_text('{"stale": true}\n', encoding="utf-8")
        try:
            check_generated_reports(
                report,
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

    print("Coverage negative controls passed (3 controls).")
if __name__ == "__main__":
    main()
