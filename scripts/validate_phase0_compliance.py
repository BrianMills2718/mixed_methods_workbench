#!/usr/bin/env python3
"""Validate the rev-5.1 Phase 0 migration and disagreement records."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/research/method_decomposition"
LEGACY = BASE / "codex_phase0/steps.yaml"
MIGRATION = BASE / "migration_ac27ab2.md"
COMPARISON = BASE / "comparison_v0.md"
DISAGREEMENTS = BASE / "disagreements.md"
REVIEW = BASE / "codex_independent_review.md"

REV5_FIELDS = {
    "method_id",
    "step_id",
    "verb",
    "label",
    "workflow_role",
    "operation_kind",
    "actor_chain",
    "inputs",
    "outputs",
    "parameters",
    "preconditions",
    "conclusion_supported",
    "failure_output",
    "method_owned_semantics",
    "evidence_basis",
    "execution_status",
    "representation_status",
    "implementation_ref",
    "optional",
    "repeatable",
}


def legacy_rows() -> dict[str, dict]:
    document = yaml.safe_load(LEGACY.read_text())
    rows: dict[str, dict] = {}
    for workflow, body in document["workflows"].items():
        for row in body["steps"]:
            assert row["step_id"] not in rows, f"duplicate legacy ID: {row['step_id']}"
            rows[row["step_id"]] = {"workflow": workflow, "row": row}
    return rows


def migration_records() -> dict[str, dict]:
    text = MIGRATION.read_text()
    matches = list(
        re.finditer(
            r"^### `(?P<id>[^`]+)`[^\n]*\n\n```yaml\n(?P<yaml>.*?)\n```$",
            text,
            re.MULTILINE | re.DOTALL,
        )
    )
    records: dict[str, dict] = {}
    for match in matches:
        step_id = match.group("id")
        assert step_id not in records, f"duplicate migration ID: {step_id}"
        records[step_id] = yaml.safe_load(match.group("yaml"))
    return records


def comparison_areas() -> list[str]:
    text = COMPARISON.read_text()
    start = text.index("| Area | Candidate A |")
    areas: list[str] = []
    for line in text[start:].splitlines()[2:]:
        if not line.startswith("|"):
            break
        areas.append(line.split("|")[1].strip())
    return areas


def disagreement_rows() -> list[list[str]]:
    text = DISAGREEMENTS.read_text()
    start = text.index("| ID | Area and candidate difference |")
    rows: list[list[str]] = []
    for line in text[start:].splitlines()[2:]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    return rows


def validate_migration() -> None:
    source = legacy_rows()
    migrated = migration_records()
    assert len(source) == 77, f"expected 77 legacy rows, found {len(source)}"
    assert set(migrated) == set(source), "migration IDs do not exactly cover legacy IDs"
    for step_id, record in migrated.items():
        expected = source[step_id]
        assert record["legacy_workflow"] == expected["workflow"], step_id
        assert record["original_values"] == expected["row"], step_id
        assigned = record["assigned_rev5_values"]
        assert set(assigned) == REV5_FIELDS, f"{step_id}: incomplete rev-5 fields"
        assert assigned["step_id"] == step_id
        assert record["unexpressible_or_loss_notes"], f"{step_id}: loss notes required"
        assert assigned["failure_output"].startswith("migration_unresolved"), step_id
    assert migrated["pt.06"]["assigned_rev5_values"]["execution_status"] == "manually_performed"
    assert migrated["pt.06"]["assigned_rev5_values"]["actor_chain"] == ["human_reviewer"]
    assert migrated["pt_acq.03"]["assigned_rev5_values"]["execution_status"] == "manually_performed"
    assert migrated["qc_gt.02"]["assigned_rev5_values"]["execution_status"] == "software_executable"


def validate_disagreements() -> None:
    areas = comparison_areas()
    rows = disagreement_rows()
    assert len(areas) == 40, f"expected 40 comparison areas, found {len(areas)}"
    assert len(rows) == 40, f"expected 40 disagreement rows, found {len(rows)}"
    assert [row[0] for row in rows] == [f"D{i:02d}" for i in range(1, 41)]
    classes = {row[2] for row in rows}
    assert classes == {"factual", "methodological", "unsettled"}, classes
    for expected_area, row in zip(areas, rows, strict=True):
        identifier, area, classification, evidence, disposition, escalation = row
        assert area.startswith(f"**{expected_area}:**"), (
            f"{identifier}: expected ordered comparison area {expected_area!r}"
        )
        assert evidence and disposition
        if classification == "factual":
            references = re.findall(r"`([^`]+)`", evidence)
            assert references, f"{identifier}: factual row lacks code references"
            assert all(re.match(r"[^@`]+@[0-9a-f]{7,40}:[^:`]+:\d+", ref) for ref in references), (
                f"{identifier}: factual row has an unpinned repository file:line reference"
            )
        elif classification == "methodological":
            assert re.search(r"\(\d{4}\)", evidence), (
                f"{identifier}: methodological row lacks source+edition/year evidence"
            )
        else:
            assert "Yes" in escalation, f"{identifier}: unsettled row is not escalated"


def validate_independent_review() -> None:
    assert REVIEW.exists(), "independent Codex review artifact is missing"
    text = REVIEW.read_text()
    for token in (
        "reviewed_commit:",
        "independent_reviewer:",
        "77",
        "40",
        "Disposition:",
    ):
        assert token in text, f"independent review missing {token!r}"


def main() -> None:
    validate_migration()
    validate_disagreements()
    validate_independent_review()
    print("Phase 0 rev-5.1 compliance artifacts validate: 77 migrations, 40 disagreements, independent review present.")


if __name__ == "__main__":
    main()
