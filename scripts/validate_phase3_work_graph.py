#!/usr/bin/env python3
"""Validate Phase 3 coordination invariants beyond generic WorkUnitV1."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

EXPECTED_METHODS = {
    "P3-RESEARCH-A": {"p01", "p02", "p03", "p04", "p14"},
    "P3-RESEARCH-B": {"p06", "p07", "p08", "p09"},
    "P3-RESEARCH-C": {"p05", "p10", "p11", "p12", "p13"},
}
SUBMITTED_EVIDENCE_REVISIONS = {
    "P3-RESEARCH-A": "git:origin/p3-research-a-corrections@2f66438517e651ed05ebec39663734d115184dd3;control-review-2026-10-08;merged-to-main",
    "P3-RESEARCH-B": "git:origin/p3-research-b-corrections@915c903c67876fb5776744517f63ed9cd8682517;control-review-2026-10-08;merged-to-main",
    "P3-RESEARCH-C": "git:origin/p3-research-c-corrections@ef34684b1fc56433da5c9d08c4d0f474f6c596e5;control-review-2026-10-08;merged-to-main",
}
CONTROL_ID = "P3-CONTROL"
INTEGRATION_ID = "P3-INTEGRATE"
GRAPH_PATH = "docs/research/method_decomposition/phase3/4_phase3_portfolio_decomposition_work_graph.json"
RECEIPT_ROOT = "docs/research/method_decomposition/phase3/lane_receipts"
PT_EVIDENCE_ID = "process-tracing-topology-prototype"
PT_EVIDENCE_REVISION = "merged@1fd01bc;not-method-authority"
PLAN_ID = "Plan #4"
PLAN_REVISION = "4_phase3_portfolio_decomposition.md@approved-2026-08-13"
SPEC_REVISION = "plan-4-phase3-work-graph-v4"


def _method_id(target: str) -> str | None:
    prefix = "docs/research/method_decomposition/phase3/methods/"
    suffix = target.removeprefix(prefix) if target.startswith(prefix) else ""
    return suffix if re.fullmatch(r"p\d{2}", suffix) else None


def _receipt_revision(revision: str) -> tuple[str, str, str] | None:
    match = re.fullmatch(
        rf"({re.escape(RECEIPT_ROOT)}/[^@]+\.yaml)@"
        r"evidence=([0-9a-f]{40});receipt=([0-9a-f]{40})",
        revision,
    )
    if match is None or match.group(2) == match.group(3):
        return None
    return match.group(1), match.group(2), match.group(3)


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        check=False,
        text=True,
    )


def _verify_receipt(
    repo: Path,
    transition_revision: str,
    unit_id: str,
    expected_methods: set[str],
    revision: str,
) -> list[str]:
    parsed = _receipt_revision(revision)
    if parsed is None:
        return [f"{unit_id} accepted status requires distinct evidence and receipt commits"]
    path, evidence_commit, receipt_commit = parsed
    expected_path = f"{RECEIPT_ROOT}/{unit_id}.yaml"
    if path != expected_path:
        return [f"{unit_id} receipt path must be {expected_path}"]
    errors: list[str] = []
    for label, commit in (("evidence", evidence_commit), ("receipt", receipt_commit), ("transition", transition_revision)):
        if _git(repo, "cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
            errors.append(f"{unit_id} {label} commit does not exist: {commit}")
    if errors:
        return errors
    if _git(repo, "merge-base", "--is-ancestor", evidence_commit, receipt_commit).returncode != 0:
        errors.append(f"{unit_id} receipt commit must descend from evidence commit")
    if receipt_commit == transition_revision or _git(repo, "merge-base", "--is-ancestor", receipt_commit, transition_revision).returncode != 0:
        errors.append(f"{unit_id} graph transition must be later than receipt commit")
    shown = _git(repo, "show", f"{receipt_commit}:{path}")
    if shown.returncode != 0:
        errors.append(f"{unit_id} receipt path is absent at receipt commit")
        return errors
    try:
        receipt = json.loads(shown.stdout)
    except json.JSONDecodeError:
        errors.append(f"{unit_id} receipt must be JSON-compatible YAML")
        return errors
    expected_paths = sorted(f"docs/research/method_decomposition/phase3/methods/{method}" for method in expected_methods)
    required_files = ("frame.yaml", "sources.md", "method_records.yaml", "connections.yaml", "uncertainty.yaml")
    for method_path in expected_paths:
        for filename in required_files:
            if _git(repo, "cat-file", "-e", f"{evidence_commit}:{method_path}/{filename}").returncode != 0:
                errors.append(f"{unit_id} evidence commit lacks {method_path}/{filename}")
    if receipt.get("unit_id") != unit_id:
        errors.append(f"{unit_id} receipt unit binding mismatches")
    if receipt.get("evidence_commit") != evidence_commit:
        errors.append(f"{unit_id} receipt evidence binding mismatches")
    if receipt.get("method_paths") != expected_paths:
        errors.append(f"{unit_id} receipt method paths mismatch")
    if receipt.get("disposition") != "accepted" or not receipt.get("checks") or not receipt.get("reviewer"):
        errors.append(f"{unit_id} receipt lacks reviewer, accepted disposition, or checks")
    return errors


def validate_graph(
    document: dict[str, Any],
    *,
    repo: Path | None = None,
    transition_revision: str | None = None,
) -> list[str]:
    errors: list[str] = []
    units = document.get("units")
    if not isinstance(units, list):
        return ["root must contain a units array"]
    by_id = {unit.get("id"): unit for unit in units if isinstance(unit, dict)}
    expected_units = {*EXPECTED_METHODS, CONTROL_ID, INTEGRATION_ID}
    if set(by_id) != expected_units or len(units) != 5:
        errors.append(f"units must be exactly {sorted(expected_units)}")

    for unit_id, unit in by_id.items():
        if unit.get("spec_revision") != SPEC_REVISION:
            errors.append(f"{unit_id} must use spec revision {SPEC_REVISION}")
        plan_inputs = [
            item
            for item in unit.get("inputs", [])
            if item.get("kind") == "CoordinationPlan"
        ]
        if (
            len(plan_inputs) != 1
            or plan_inputs[0].get("id") != PLAN_ID
            or plan_inputs[0].get("revision") != PLAN_REVISION
        ):
            errors.append(f"{unit_id} must bind exactly once to {PLAN_ID} at {PLAN_REVISION}")

    all_methods: list[str] = []
    for unit_id, expected in EXPECTED_METHODS.items():
        unit = by_id.get(unit_id, {})
        owned = {
            method_id
            for surface in unit.get("conflict_surfaces", [])
            if surface.get("access") == "exclusive"
            for method_id in [_method_id(str(surface.get("target", "")))]
            if method_id is not None
        }
        if owned != expected:
            errors.append(f"{unit_id} must exclusively own {sorted(expected)}, got {sorted(owned)}")
        all_methods.extend(owned)
        if unit.get("integration_owner_id") != CONTROL_ID:
            errors.append(f"{unit_id} must name {CONTROL_ID} as integration owner")
        submitted = [
            item
            for item in unit.get("inputs", [])
            if item.get("kind") == "SubmittedEvidence" and item.get("id") == unit_id
        ]
        if (
            len(submitted) != 1
            or submitted[0].get("revision") != SUBMITTED_EVIDENCE_REVISIONS[unit_id]
        ):
            errors.append(f"{unit_id} must bind its exact archived submitted evidence revision")
        if unit.get("status") != "accepted" and any(
            item.get("kind") == "CompletionReceipt" for item in unit.get("inputs", [])
        ):
            errors.append(f"{unit_id} cannot bind a CompletionReceipt before accepted status")
        if unit.get("status") == "accepted":
            receipts = [
                item for item in unit.get("inputs", [])
                if item.get("kind") == "CompletionReceipt" and item.get("id") == unit_id
            ]
            revision = str(receipts[0].get("revision", "")) if len(receipts) == 1 else ""
            if len(receipts) != 1:
                errors.append(f"{unit_id} accepted status requires one CompletionReceipt")
            elif repo is None or transition_revision is None:
                errors.append(f"{unit_id} accepted status requires repository evidence context")
            else:
                errors.extend(_verify_receipt(repo, transition_revision, unit_id, expected, revision))

    expected_all = {f"p{number:02d}" for number in range(1, 15)}
    if set(all_methods) != expected_all or len(all_methods) != 14:
        errors.append("exclusive method ownership must contain p01 through p14 exactly once")

    control = by_id.get(CONTROL_ID, {})
    control_state = (
        control.get("claimability"),
        control.get("status"),
        control.get("readiness", {}).get("status"),
    )
    if control_state not in {
        ("ready_for_execution", "ready", "ready"),
        ("not_applicable", "blocked", "blocked"),
    }:
        errors.append(
            "P3-CONTROL must be either ready_for_execution/ready/ready or "
            "not_applicable/blocked/blocked"
        )
    if control_state == ("not_applicable", "blocked", "blocked") and not any(
        "product integration" in guard.lower()
        for guard in control.get("readiness", {}).get("failed_guards", [])
    ):
        errors.append("paused P3-CONTROL must name the product-integration guard")
    if control.get("integration_owner_id") != CONTROL_ID:
        errors.append("P3-CONTROL must own its control mechanism")
    exclusive_control = {
        str(surface.get("target"))
        for surface in control.get("conflict_surfaces", [])
        if surface.get("access") == "exclusive"
    }
    if exclusive_control != {GRAPH_PATH, RECEIPT_ROOT}:
        errors.append("P3-CONTROL must solely and exclusively own graph and receipt surfaces")
    for unit_id, unit in by_id.items():
        if unit_id == CONTROL_ID:
            continue
        for surface in unit.get("conflict_surfaces", []):
            target = str(surface.get("target", ""))
            if surface.get("access") == "exclusive" and (
                target == GRAPH_PATH or target.startswith(RECEIPT_ROOT)
            ):
                errors.append(f"{unit_id} may not own graph or receipt surfaces")

    integration = by_id.get(INTEGRATION_ID, {})
    hard_dependencies = {
        dependency.get("unit_id")
        for dependency in integration.get("dependencies", [])
        if dependency.get("type") == "hard"
        and dependency.get("gate", {}).get("type") == "unit_status"
        and dependency.get("gate", {}).get("required_status") == "accepted"
    }
    if hard_dependencies != set(EXPECTED_METHODS):
        errors.append("P3-INTEGRATE must have accepted-status hard gates from all three research units")
    if integration.get("integration_owner_id") != CONTROL_ID:
        errors.append("P3-INTEGRATE must name P3-CONTROL as integration owner")
    if integration.get("claimability") == "ready_for_execution":
        for unit_id in EXPECTED_METHODS:
            source = by_id.get(unit_id, {})
            if source.get("status") != "accepted":
                errors.append(f"P3-INTEGRATE cannot be ready before {unit_id} is accepted")
            if not any(item.get("kind") == "CompletionReceipt" for item in source.get("inputs", [])):
                errors.append(f"P3-INTEGRATE cannot be ready without {unit_id} completion evidence")
    elif integration.get("claimability") != "blocked_dependencies" or integration.get("status") != "blocked":
        errors.append("P3-INTEGRATE must be blocked or validly ready after all receipts")

    lane_a = by_id.get("P3-RESEARCH-A", {})
    pt_inputs = [item for item in lane_a.get("inputs", []) if item.get("id") == PT_EVIDENCE_ID]
    if len(pt_inputs) != 1 or pt_inputs[0].get("revision") != PT_EVIDENCE_REVISION:
        errors.append("P14 lane must pin merged PT topology evidence as non-method-authority")
    pt_surfaces = [
        surface for surface in lane_a.get("conflict_surfaces", [])
        if "pt-topology" in str(surface.get("coordination_key", ""))
    ]
    if len(pt_surfaces) != 2 or any(surface.get("access") != "read" for surface in pt_surfaces):
        errors.append("both PT topology implementation surfaces must be read-only")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--transition-revision", default="HEAD")
    args = parser.parse_args()
    resolved = _git(args.repo, "rev-parse", args.transition_revision)
    if resolved.returncode != 0:
        print(f"ERROR: transition revision does not exist: {args.transition_revision}")
        return 1
    errors = validate_graph(
        json.loads(args.graph.read_text(encoding="utf-8")),
        repo=args.repo,
        transition_revision=resolved.stdout.strip(),
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("valid Phase 3 coordination graph: 5 units, 14 exclusive methods")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
