#!/usr/bin/env python3
"""Validate Phase 3 coordination invariants beyond generic WorkUnitV1."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

EXPECTED_METHODS = {
    "P3-RESEARCH-A": {"p01", "p02", "p03", "p04", "p14"},
    "P3-RESEARCH-B": {"p06", "p07", "p08", "p09"},
    "P3-RESEARCH-C": {"p05", "p10", "p11", "p12", "p13"},
}
CONTROL_ID = "P3-CONTROL"
INTEGRATION_ID = "P3-INTEGRATE"
GRAPH_PATH = "docs/research/method_decomposition/phase3/work_graph.json"
RECEIPT_ROOT = "docs/research/method_decomposition/phase3/lane_receipts"
PT_EVIDENCE_ID = "process-tracing-topology-prototype"
PT_EVIDENCE_REVISION = "merged@1fd01bc;not-method-authority"


def _method_id(target: str) -> str | None:
    prefix = "docs/research/method_decomposition/phase3/methods/"
    suffix = target.removeprefix(prefix) if target.startswith(prefix) else ""
    return suffix if re.fullmatch(r"p\d{2}", suffix) else None


def _valid_receipt_revision(revision: str) -> bool:
    match = re.fullmatch(
        rf"{re.escape(RECEIPT_ROOT)}/[^@]+\.yaml@"
        r"evidence=([0-9a-f]{40});receipt=([0-9a-f]{40})",
        revision,
    )
    return match is not None and match.group(1) != match.group(2)


def validate_graph(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    units = document.get("units")
    if not isinstance(units, list):
        return ["root must contain a units array"]
    by_id = {unit.get("id"): unit for unit in units if isinstance(unit, dict)}
    expected_units = {*EXPECTED_METHODS, CONTROL_ID, INTEGRATION_ID}
    if set(by_id) != expected_units or len(units) != 5:
        errors.append(f"units must be exactly {sorted(expected_units)}")

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
        if unit.get("status") == "accepted":
            receipts = [
                item for item in unit.get("inputs", [])
                if item.get("kind") == "CompletionReceipt" and item.get("id") == unit_id
            ]
            revision = str(receipts[0].get("revision", "")) if len(receipts) == 1 else ""
            if len(receipts) != 1 or not _valid_receipt_revision(revision):
                errors.append(f"{unit_id} accepted status requires distinct evidence and receipt commits")

    expected_all = {f"p{number:02d}" for number in range(1, 15)}
    if set(all_methods) != expected_all or len(all_methods) != 14:
        errors.append("exclusive method ownership must contain p01 through p14 exactly once")

    control = by_id.get(CONTROL_ID, {})
    if control.get("claimability") != "ready_for_execution" or control.get("status") != "ready":
        errors.append("P3-CONTROL must be ready_for_execution with ready status")
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
    args = parser.parse_args()
    errors = validate_graph(json.loads(args.graph.read_text(encoding="utf-8")))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("valid Phase 3 coordination graph: 5 units, 14 exclusive methods")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
