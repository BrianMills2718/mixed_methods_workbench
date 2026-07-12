#!/usr/bin/env python3
"""Generate coverage grades for current workbench readiness requirements."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

from validate_fixtures import DEFAULT_FIXTURE_DIR, validate_fixture_dir


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_MD = REPO_ROOT / "docs" / "coverage_report.md"
REPORT_JSON = REPO_ROOT / "docs" / "coverage_report.json"

Grade = Literal["A", "B", "C", "D", "F"]


@dataclass(frozen=True)
class Requirement:
    """One requirement row with current evidence and closure target."""

    id: str
    name: str
    success_criteria: list[str]
    evidence_class: str
    evidence_grade: Grade
    evidence_notes: str
    required_class_for_closure: str
    negative_control: str | None
    next_step: str


REQUIREMENTS: list[Requirement] = [
    Requirement(
        id="W1-contract-stub",
        name="Executable workbench contract stub",
        success_criteria=[
            "synthetic QC/PT/TF/synthesis fixtures exist",
            "manifest records hashes and evidence grades",
            "make check validates the fixtures",
        ],
        evidence_class="fixture",
        evidence_grade="C",
        evidence_notes=(
            "Synthetic JSON fixtures and targeted validator checks demonstrate a candidate seam; "
            "they are not schema-validated producer contracts."
        ),
        required_class_for_closure="test + real producer fixtures",
        negative_control="scripts/check_fixture_negative_controls.py",
        next_step="Replace ad hoc validation with typed producer/consumer schemas and real engine fixtures.",
    ),
    Requirement(
        id="QCX-real-fixture",
        name="Canonical qualitative coding export fixture",
        success_criteria=[
            "real QC fixture includes source scope, hashes, anchors, claims, patterns/candidates, caveats",
            "fixture rejects process-tracing inference fields",
            "producer commit and validation command are recorded",
        ],
        evidence_class="doc",
        evidence_grade="D",
        evidence_notes="Engine-local Plan #242 exists, but no real QC fixture is committed here.",
        required_class_for_closure="schema_validated",
        negative_control=None,
        next_step="Generate a real QC handoff fixture in qualitative_coding, then import/hash it here.",
    ),
    Requirement(
        id="PTX-real-fixture",
        name="Canonical process tracing export v1 fixture",
        success_criteria=[
            "real PT fixture exposes source scope, hypotheses, comparative support, absence findings, verdicts, metadata, caveats",
            "fixture validates without parsing internal result.json",
            "producer commit and validation command are recorded",
        ],
        evidence_class="doc",
        evidence_grade="D",
        evidence_notes="Engine-local Plan #7 exists, but pt_export_v1 is not implemented or committed here.",
        required_class_for_closure="schema_validated",
        negative_control=None,
        next_step="Implement/generate pt_export_v1 in process_tracing, then import/hash it here.",
    ),
    Requirement(
        id="TFX-real-fixture",
        name="Canonical Theory Forge operationalization fixture",
        success_criteria=[
            "real Theory Forge fixture exposes constructs, mechanisms, hypotheses, observables, assumptions, scope conditions, uncertainties, validation obligations",
            "fixture validates without AC runtime",
            "producer commit and validation command are recorded",
        ],
        evidence_class="doc",
        evidence_grade="D",
        evidence_notes="Engine-local Plan #108 exists, but no real TheoryOperationalizationArtifact is committed here.",
        required_class_for_closure="schema_validated",
        negative_control=None,
        next_step="Produce a known-green Theory Forge operationalization export, then import/hash it here.",
    ),
    Requirement(
        id="W3-real-synthesis-payload",
        name="Fixture-backed workbench synthesis payload",
        success_criteria=[
            "payload uses real engine fixtures, not synthetic placeholder rows",
            "payload preserves evidence anchors, scope, estimands, method outputs, caveats, and provenance",
        ],
        evidence_class="fixture",
        evidence_grade="C",
        evidence_notes="Synthetic synthesis payload validates structurally; it is not generated from real engine artifacts.",
        required_class_for_closure="schema_validated",
        negative_control="scripts/check_fixture_negative_controls.py",
        next_step="Replace synthetic inputs with real QC/PT fixtures and rerun validation.",
    ),
    Requirement(
        id="W4-static-review-shell",
        name="Static review shell over real fixture payload",
        success_criteria=[
            "reviewer can trace question to source scope, evidence, QC claim/pattern, PT support, and caveat",
            "review artifact hides none of the method boundaries",
        ],
        evidence_class="doc",
        evidence_grade="D",
        evidence_notes="Planned in Plan 001, but no static review shell exists.",
        required_class_for_closure="fixture",
        negative_control=None,
        next_step="Build only after real QC/PT fixtures replace synthetic contract rows.",
    ),
    Requirement(
        id="MM1-synthesis-quality",
        name="Mixed-methods synthesis quality gates",
        success_criteria=[
            "human/agent review identifies stable failure modes",
            "quality gates are based on fixture readouts, not invented thresholds",
        ],
        evidence_class="doc",
        evidence_grade="D",
        evidence_notes="Exploratory surface; no reviewed real payload exists yet.",
        required_class_for_closure="observed",
        negative_control=None,
        next_step="Run adversarial review after W4 exists over real fixtures.",
    ),
]


def main() -> None:
    """Generate JSON or Markdown coverage output."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    report = _build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    REPORT_MD.write_text(_render_markdown(report), encoding="utf-8")

    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(REPORT_MD.read_text(encoding="utf-8"))


def _build_report() -> dict[str, Any]:
    requirements = [
        *REQUIREMENTS[:4],
        derive_fixture_inventory_requirement(),
        *REQUIREMENTS[4:],
    ]
    rows = [asdict(requirement) for requirement in requirements]
    counts = {grade: 0 for grade in ["A", "B", "C", "D", "F"]}
    for requirement in requirements:
        counts[requirement.evidence_grade] += 1
    total = len(requirements)
    return {
        "summary": {
            "total": total,
            "grade_a": counts["A"],
            "grade_b": counts["B"],
            "grade_c": counts["C"],
            "grade_d": counts["D"],
            "grade_f": counts["F"],
            "overall_grade": _overall_grade(counts),
            "notes": "Current coverage proves a synthetic contract seam, not real engine readiness.",
        },
        "requirements": rows,
    }


def derive_fixture_inventory_requirement(
    fixture_dir: Path = DEFAULT_FIXTURE_DIR,
) -> Requirement:
    """Derive W2 from current bytes, Git provenance, and live validation.

    Failure remains visible as an F row rather than aborting report generation.
    The bounded A claim concerns inventory provenance only; it never promotes
    the synthetic fixture contents above C.
    """
    success_criteria = [
        "every current JSON fixture is listed exactly once and no extra artifact is omitted",
        "every fixture records its hash, synthetic origin, exact last-content Git commit, recovery command, invariant, claim limits, and C grade",
        "the validation observation matches current fixture and validator bytes",
        "coverage changes to F when required inventory evidence is removed",
    ]
    negative_control = (
        "scripts/check_fixture_negative_controls.py + "
        "scripts/check_coverage_negative_controls.py"
    )
    try:
        validate_fixture_dir(fixture_dir)
    except SystemExit as error:
        return Requirement(
            id="W2-fixture-inventory",
            name="Synthetic fixture provenance inventory",
            success_criteria=success_criteria,
            evidence_class="missing",
            evidence_grade="F",
            evidence_notes=f"Live inventory evidence failed: {error}",
            required_class_for_closure="test",
            negative_control=negative_control,
            next_step=(
                "Repair the exact failed provenance/validation evidence; do not "
                "substitute engine provenance for hand-authored synthetic data."
            ),
        )

    manifest_path = fixture_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = manifest["files"]
    distinct_commits = sorted({entry["last_content_commit"] for entry in files})
    return Requirement(
        id="W2-fixture-inventory",
        name="Synthetic fixture provenance inventory",
        success_criteria=success_criteria,
        evidence_class="test",
        evidence_grade="A",
        evidence_notes=(
            f"Live validation proved {len(files)} exhaustively inventoried synthetic "
            f"fixtures recoverable from {len(distinct_commits)} exact last-content "
            "Git commits; file and validator hashes match the recorded observation. "
            "This A applies only to inventory provenance; fixture contents remain C."
        ),
        required_class_for_closure="test (met for synthetic inventory only)",
        negative_control=negative_control,
        next_step=(
            "Keep the inventory current. Real engine exports remain separate "
            "QCX/PTX/TFX requirements and require separately authorized slices."
        ),
    )


def _overall_grade(counts: dict[str, int]) -> str:
    for grade in ["F", "D", "C", "B", "A"]:
        if counts[grade]:
            return grade
    return "A"


def _render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    rows = report["requirements"]
    total = summary["total"]

    lines = [
        "# Mixed Methods Workbench Coverage Report",
        "",
        "Generated by `scripts/check_coverage.py`.",
        "",
        "This report grades current evidence for readiness requirements. It does not claim real engine readiness.",
        "",
        "## Grade Distribution",
        "",
        "| Grade | Count | Percent |",
        "|---|---:|---:|",
    ]
    for grade, key in [("A", "grade_a"), ("B", "grade_b"), ("C", "grade_c"), ("D", "grade_d"), ("F", "grade_f")]:
        count = summary[key]
        percent = int(round((count / total) * 100))
        lines.append(f"| {grade} | {count} | {percent}% |")

    lines.extend([
        "",
        f"Overall grade: **{summary['overall_grade']}**",
        "",
        "## Requirements",
        "",
        "| ID | Requirement | Grade | Evidence class | Evidence notes | Closes when |",
        "|---|---|---|---|---|---|",
    ])
    for row in rows:
        lines.append(
            "| {id} | {name} | {evidence_grade} | {evidence_class} | {evidence_notes} | {required_class_for_closure} |".format(
                **{key: _escape(str(value)) for key, value in row.items()}
            )
        )

    weak_rows = [row for row in rows if row["evidence_grade"] in {"D", "F"}]
    lines.extend([
        "",
        "## Rows Needing Review",
        "",
    ])
    for row in weak_rows:
        lines.append(f"- `{row['id']}`: {row['next_step']}")

    missing_negative = [row for row in rows if row["negative_control"] is None and row["evidence_grade"] in {"C", "D", "F"}]
    lines.extend([
        "",
        "## Missing Negative Controls",
        "",
    ])
    for row in missing_negative:
        lines.append(f"- `{row['id']}`: add a negative control before enforcing this requirement.")

    lines.extend([
        "",
        "## What Closes The Weakest Rows",
        "",
        "1. Generate a real QC handoff fixture and import/hash it here.",
        "2. Generate a real `pt_export_v1` fixture and import/hash it here.",
        "3. Generate a real Theory Forge operationalization fixture only after a known-green theory is selected.",
        "4. Replace the synthetic synthesis payload with one built from real fixtures.",
        "5. Build the static review shell only after the real payload exists.",
        "",
    ])
    return "\n".join(lines)


def _escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    main()
