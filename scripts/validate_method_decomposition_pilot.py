#!/usr/bin/env python3
"""Validate the Phase 1 method-decomposition discovery artifacts.

Passing this validator means the unresolved candidate and its losses are
structurally auditable. It does not establish semantic completeness, method
validity, or readiness for collision analysis.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

DEFAULT_BASE = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "research"
    / "method_decomposition"
    / "phase1_pilot"
)

CONTROLLED_VERBS = {
    "acquire",
    "aggregate",
    "annotate",
    "appraise_source",
    "calibrate",
    "code",
    "compare",
    "conceptualize",
    "construct",
    "define",
    "derive",
    "estimate",
    "extract",
    "identify",
    "measure",
    "perturb",
    "rank",
    "refuse",
    "review",
    "screen",
    "search",
    "simulate",
    "synthesize",
    "test",
    "value",
}
CONTROLLED_TYPES = {
    "analysis_plan",
    "appraisal",
    "case",
    "case_set",
    "claim",
    "code",
    "code_system",
    "concept",
    "configuration",
    "consequence",
    "criterion",
    "dataset",
    "design_parameters",
    "diagnostic_item",
    "estimand",
    "estimate",
    "evidence_item",
    "finding",
    "gap",
    "memo",
    "model",
    "model_run",
    "option",
    "recommendation",
    "review_event",
    "review_protocol",
    "rival_explanation",
    "screening_decision",
    "segment",
    "source_document",
    "theory",
    "uncertainty_note",
}
SLOT_KEYS = {"slot", "type", "role", "cardinality", "optional"}
SLOT_ROLES = {"subject", "context", "criteria", "result", "byproduct", "trace"}
CARDINALITIES = {"one", "many", "optional_one"}
EDGE_TYPES = {
    "alternative_path",
    "branch",
    "join",
    "loop_back",
    "optional_return",
    "sequence",
    "terminal",
}
GAP_DISPOSITIONS = {
    "missing_artifact_or_operation",
    "shared_input_not_carried",
    "control_dependency",
}
RECONCILIATION_DISPOSITIONS = {
    "represented",
    "compressed",
    "compressed_with_loss",
    "missing",
}


def _load(path: Path, errors: list[str]) -> dict[str, Any]:
    if not path.is_file():
        errors.append(f"missing required file: {path}")
        return {}
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:  # fail loud with the source path
        errors.append(f"cannot parse {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"expected mapping at document root: {path}")
        return {}
    return value


def _has_path(adjacency: dict[str, set[str]], start: str, target: str) -> bool:
    pending = [start]
    seen: set[str] = set()
    while pending:
        node = pending.pop()
        if node == target:
            return True
        if node in seen:
            continue
        seen.add(node)
        pending.extend(adjacency.get(node, ()))
    return False


def validate(base: Path = DEFAULT_BASE) -> list[str]:
    errors: list[str] = []
    ledger = _load(base / "step_ledger.yaml", errors)
    graph = _load(base / "workflow_edges.yaml", errors)
    gaps = _load(base / "structural_gaps.yaml", errors)
    rerun_dir = base / "blind_reruns"
    manifest = _load(rerun_dir / "manifest.yaml", errors)
    inventory = _load(rerun_dir / "step_inventory.yaml", errors)
    reconciliation = _load(rerun_dir / "reconciliation.yaml", errors)
    if errors:
        return errors

    if ledger.get("status") != "unresolved_granularity_candidate":
        errors.append("step ledger must remain unresolved_granularity_candidate")
    if graph.get("status") != "unresolved_granularity_candidate":
        errors.append("workflow graph must remain unresolved_granularity_candidate")
    if gaps.get("status") != "blocks_collision":
        errors.append("structural gaps must block collision")
    if reconciliation.get("status") != "unresolved_losses_block_collision":
        errors.append("reconciliation losses must block collision")

    required_step_keys = {
        "method_id",
        "step_id",
        "verb",
        "label",
        "workflow_role",
        "operation_kind",
        "actor_chain",
        "execution_status",
        "representation_status",
        "implementation_ref",
        "inputs",
        "outputs",
        "parameters",
        "preconditions",
        "conclusion_supported",
        "failure_output",
        "method_owned_semantics",
        "evidence_basis",
        "optional",
        "repeatable",
    }
    steps = ledger.get("steps", [])
    if not isinstance(steps, list):
        errors.append("step_ledger.steps must be a list")
        steps = []
    step_by_id: dict[str, dict[str, Any]] = {}
    methods: set[str] = set()
    for index, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"step {index} is not a mapping")
            continue
        missing = required_step_keys - step.keys()
        if missing:
            errors.append(f"{step.get('step_id', index)} missing keys: {sorted(missing)}")
        step_id = step.get("step_id")
        if not isinstance(step_id, str):
            errors.append(f"step {index} has invalid step_id")
            continue
        if step_id in step_by_id:
            errors.append(f"duplicate step_id: {step_id}")
        step_by_id[step_id] = step
        methods.add(str(step.get("method_id")))
        if step.get("verb") not in CONTROLLED_VERBS:
            errors.append(f"{step_id} uses uncontrolled verb {step.get('verb')!r}")
        if step.get("operation_kind") not in {
            "analytic",
            "methodological_support",
            "runtime_delivery",
        }:
            errors.append(f"{step_id} has invalid operation_kind")
        if not isinstance(step.get("actor_chain"), list) or not step.get("actor_chain"):
            errors.append(f"{step_id} requires a non-empty actor_chain")
        for direction in ("inputs", "outputs"):
            slots = step.get(direction, [])
            if not isinstance(slots, list):
                errors.append(f"{step_id}.{direction} must be a list")
                continue
            for slot in slots:
                if not isinstance(slot, dict):
                    errors.append(f"{step_id}.{direction} contains a non-mapping slot")
                    continue
                if set(slot) != SLOT_KEYS:
                    errors.append(
                        f"{step_id}.{direction}.{slot.get('slot')} has keys {sorted(slot)}"
                    )
                if slot.get("type") not in CONTROLLED_TYPES:
                    errors.append(f"{step_id} uses uncontrolled type {slot.get('type')!r}")
                if slot.get("role") not in SLOT_ROLES:
                    errors.append(f"{step_id} uses invalid role {slot.get('role')!r}")
                if slot.get("cardinality") not in CARDINALITIES:
                    errors.append(f"{step_id} uses invalid cardinality {slot.get('cardinality')!r}")
                if not isinstance(slot.get("optional"), bool):
                    errors.append(
                        f"{step_id}.{direction}.{slot.get('slot')} optional must be boolean"
                    )

    edges = graph.get("edges", [])
    if not isinstance(edges, list):
        errors.append("workflow_edges.edges must be a list")
        edges = []
    adjacency: dict[str, set[str]] = defaultdict(set)
    no_overlap: set[tuple[str, str]] = set()
    for index, edge in enumerate(edges):
        required = {"method_id", "from_step", "to_step", "edge_type", "condition", "required"}
        if not isinstance(edge, dict):
            errors.append(f"edge {index} is not a mapping")
            continue
        missing = required - edge.keys()
        if missing:
            errors.append(f"edge {index} missing keys: {sorted(missing)}")
        source = edge.get("from_step")
        target = edge.get("to_step")
        if source not in step_by_id or target not in step_by_id:
            errors.append(f"edge {source}->{target} has unresolved endpoint")
            continue
        if edge.get("method_id") != step_by_id[source].get("method_id") or edge.get(
            "method_id"
        ) != step_by_id[target].get("method_id"):
            errors.append(f"edge {source}->{target} crosses or misstates method ownership")
        if edge.get("edge_type") not in EDGE_TYPES:
            errors.append(f"edge {source}->{target} has invalid edge_type")
        if not isinstance(edge.get("required"), bool):
            errors.append(f"edge {source}->{target} required must be boolean")
        if edge.get("edge_type") == "loop_back" and (
            not edge.get("loop_termination")
            or edge.get("termination_authority") not in {"human", "system", "either"}
        ):
            errors.append(f"loop_back {source}->{target} lacks termination contract")
        adjacency[source].add(target)
        if edge.get("required"):
            out_types = {slot["type"] for slot in step_by_id[source].get("outputs", [])}
            in_types = {slot["type"] for slot in step_by_id[target].get("inputs", [])}
            if not out_types.intersection(in_types):
                no_overlap.add((source, target))

    topologies = graph.get("topologies", [])
    topology_by_method: dict[str, dict[str, Any]] = {}
    topology_keys = {
        "method_id",
        "shape",
        "required_cycles",
        "optional_cycles",
        "prohibited_cycles",
        "prohibited_edges",
        "entry_points",
        "terminal_points",
    }
    for item in topologies if isinstance(topologies, list) else []:
        if not isinstance(item, dict):
            errors.append("topology entry is not a mapping")
            continue
        missing = topology_keys - item.keys()
        if missing:
            errors.append(f"topology {item.get('method_id')} missing keys: {sorted(missing)}")
        method_id = item.get("method_id")
        if method_id in topology_by_method:
            errors.append(f"duplicate topology for {method_id}")
        topology_by_method[method_id] = item
        for point in item.get("entry_points", []) + item.get("terminal_points", []):
            if point not in step_by_id:
                errors.append(f"topology {method_id} references missing point {point}")
    if set(topology_by_method) != methods:
        errors.append(
            f"topology methods differ from ledger methods: {set(topology_by_method) ^ methods}"
        )

    for step_id, step in step_by_id.items():
        if step.get("repeatable") and not any(
            _has_path(adjacency, neighbor, step_id) for neighbor in adjacency.get(step_id, ())
        ):
            errors.append(f"repeatable step {step_id} is not in a directed cycle")

    gap_rows = gaps.get("required_edge_gaps", [])
    classified_pairs: set[tuple[str, str]] = set()
    for row in gap_rows if isinstance(gap_rows, list) else []:
        pair = (row.get("from_step"), row.get("to_step"))
        if pair in classified_pairs:
            errors.append(f"duplicate structural-gap classification {pair}")
        classified_pairs.add(pair)
        if row.get("disposition") not in GAP_DISPOSITIONS:
            errors.append(f"invalid structural-gap disposition for {pair}")
        if not str(row.get("explanation", "")).strip():
            errors.append(f"structural gap {pair} lacks explanation")
    if no_overlap != classified_pairs:
        errors.append(
            "required no-overlap edges and structural-gap classifications differ: "
            f"missing={sorted(no_overlap - classified_pairs)} extra={sorted(classified_pairs - no_overlap)}"
        )
    missing_capabilities = gaps.get("known_missing_capabilities", [])
    if not missing_capabilities or any(
        row.get("blocks_collision") is not True for row in missing_capabilities
    ):
        errors.append("every known missing capability must explicitly block collision")
    source_scope_mismatches = gaps.get("source_scope_mismatches", [])
    if not source_scope_mismatches:
        errors.append("known source-scope mismatch is not recorded")
    for mismatch in source_scope_mismatches:
        compact_step = mismatch.get("compact_step")
        if compact_step not in step_by_id:
            errors.append(f"source-scope mismatch references missing step {compact_step}")
        if mismatch.get("blocks_collision") is not True:
            errors.append(f"source-scope mismatch {compact_step} must block collision")
        if not str(mismatch.get("mismatch", "")).strip():
            errors.append(f"source-scope mismatch {compact_step} lacks explanation")

    if manifest.get("status") != "audit_rerun_not_original":
        errors.append("blind-rerun manifest must deny original-report status")
    for artifact in manifest.get("artifacts", []):
        path = rerun_dir / artifact.get("path", "")
        if not path.is_file():
            errors.append(f"blind-rerun artifact missing: {path.name}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != artifact.get("sha256"):
            errors.append(f"blind-rerun artifact digest mismatch: {path.name}")

    inventory_methods = inventory.get("methods", [])
    inventory_steps: dict[str, set[str]] = {}
    inventory_counts: dict[str, int] = {}
    all_blind_ids: set[tuple[str, str]] = set()
    for item in inventory_methods if isinstance(inventory_methods, list) else []:
        method_id = item.get("method_id")
        ids = [row.get("step_id") for row in item.get("steps", [])]
        if len(ids) != len(set(ids)):
            errors.append(f"duplicate rerun step within {method_id}")
        inventory_steps[method_id] = set(ids)
        inventory_counts[method_id] = len(ids)
        for step_id in ids:
            pair = (method_id, step_id)
            if pair in all_blind_ids:
                errors.append(f"duplicate rerun step: {pair}")
            all_blind_ids.add(pair)
    declared_counts = {
        row.get("method_id"): row.get("operation_count") for row in manifest.get("methods", [])
    }
    if inventory_counts != declared_counts:
        errors.append(
            f"manifest method counts differ from inventory: {declared_counts} != {inventory_counts}"
        )
    if sum(inventory_counts.values()) != manifest.get("total_operations"):
        errors.append("manifest total_operations differs from inventory")

    seen_mappings: set[tuple[str, str]] = set()
    loss_count = 0
    mappings = reconciliation.get("mappings", {})
    for method_id, rows in mappings.items() if isinstance(mappings, dict) else []:
        for row in rows if isinstance(rows, list) else []:
            pair = (method_id, row.get("blind_step"))
            if pair in seen_mappings:
                errors.append(f"duplicate reconciliation mapping: {pair}")
            seen_mappings.add(pair)
            disposition = row.get("disposition")
            if disposition not in RECONCILIATION_DISPOSITIONS:
                errors.append(f"invalid reconciliation disposition for {pair}")
            compact_rows = row.get("compact_rows")
            if not isinstance(compact_rows, list):
                errors.append(f"reconciliation {pair} compact_rows must be a list")
                continue
            for compact_id in compact_rows:
                if compact_id not in step_by_id:
                    errors.append(
                        f"reconciliation {pair} references missing compact row {compact_id}"
                    )
                elif step_by_id[compact_id].get("method_id") != method_id:
                    errors.append(f"reconciliation {pair} crosses method boundary at {compact_id}")
            if disposition == "missing" and compact_rows:
                errors.append(f"missing reconciliation {pair} must not claim compact rows")
            if disposition != "missing" and not compact_rows:
                errors.append(f"non-missing reconciliation {pair} requires compact rows")
            if (
                disposition in {"compressed", "compressed_with_loss", "missing"}
                and not str(row.get("reason", "")).strip()
            ):
                errors.append(f"reconciliation {pair} requires a reason")
            if disposition in {"compressed_with_loss", "missing"}:
                loss_count += 1
    if seen_mappings != all_blind_ids:
        errors.append(
            "reconciliation does not cover rerun inventory exactly: "
            f"missing={sorted(all_blind_ids - seen_mappings)} extra={sorted(seen_mappings - all_blind_ids)}"
        )
    if set(mappings) != set(inventory_steps):
        errors.append("reconciliation method set differs from rerun inventory")
    if loss_count == 0:
        errors.append("unresolved reconciliation unexpectedly contains no losses")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", type=Path, default=DEFAULT_BASE)
    args = parser.parse_args()
    errors = validate(args.base_dir.resolve())
    if errors:
        print("FAIL: Phase 1 pilot is not structurally auditable")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "PASS: artifact is structurally audited and collision-blocked; "
        "this does not mean semantic completeness or method validity."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
