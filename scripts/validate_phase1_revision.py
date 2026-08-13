#!/usr/bin/env python3
"""Validate the bounded Phase 1 format-revision candidate."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REVISION = ROOT / "docs/research/method_decomposition/phase1_revision"
PILOT = ROOT / "docs/research/method_decomposition/phase1_pilot"
INSTRUMENT = REVISION / "REVISED_DECOMPOSITION_INSTRUMENT.md"
READOUT = REVISION / "PLAIN_LANGUAGE_READOUT.md"

METHODS = {"grounded_theory", "causal_effect_estimation_rct", "policy_option_appraisal"}
KINDS = {"analytic", "methodological_support", "runtime_delivery"}
LEVELS = {"method_phase", "analytical_move", "execution_action"}
CONNECTION_TYPES = {
    "artifact_flow", "retained_context", "control_gate", "feedback", "prohibited_transition"
}
DISPOSITIONS = {"phase", "analytical_move", "execution_action", "unresolved"}
MOVE_FIELDS = {
    "record_id", "level", "parent_phase", "label", "operation_kind", "inputs", "output",
    "information_origin", "source_authority_or_inferential_role", "applicability_boundary",
    "method_owned_rule", "permitted_conclusion",
    "refusal_or_qualification", "performer", "judgment_owner", "acceptance_authority",
    "recommender", "value_goal_authority", "decision_authority", "source_basis",
    "exact_anchors", "implementation_evidence", "collision_participation",
    "connections_ref", "guards",
}
ACTION_FIELDS = (MOVE_FIELDS - {"parent_phase"}) | {"parent_move"}


def _load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def _pilot_expected_ids() -> dict[str, set[str]]:
    ledger = _load(PILOT / "step_ledger.yaml")
    inventory = _load(PILOT / "blind_reruns/step_inventory.yaml")
    gaps = _load(PILOT / "structural_gaps.yaml")
    compact = {method: set() for method in METHODS}
    for row in ledger["steps"]:
        if row["method_id"] in METHODS:
            compact[row["method_id"]].add(f"compact:{row['step_id']}")
    rerun = {method: set() for method in METHODS}
    for method in inventory["methods"]:
        if method["method_id"] in METHODS:
            rerun[method["method_id"]] = {
                f"rerun:{row['step_id']}" for row in method["steps"]
            }
    gap_ids = {method: set() for method in METHODS}
    prefix_map = {
        "grounded_theory": "gt.",
        "causal_effect_estimation_rct": "rct.",
        "policy_option_appraisal": "pa.",
    }
    for gap in gaps["required_edge_gaps"]:
        for method, prefix in prefix_map.items():
            if gap["from_step"].startswith(prefix):
                gap_ids[method].add(f"gap:{gap['from_step']}->{gap['to_step']}")
    capability_slug = lambda value: re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    for item in gaps["known_missing_capabilities"]:
        if item["method_id"] in METHODS:
            gap_ids[item["method_id"]].add(f"capability:{capability_slug(item['capability'])}")
    return {method: compact[method] | rerun[method] | gap_ids[method] for method in METHODS}


def validate_revision(base: Path = REVISION) -> None:
    records = _load(base / "method_records.yaml")
    graph = _load(base / "connections.yaml")
    dispositions = _load(base / "audit_dispositions.yaml")
    vocabulary = _load(base / "phase2_vocabulary_dispositions.yaml")
    canonical_anchor_ids = {item["source_id"] for item in dispositions["dispositions"]}

    methods = {method["method_id"]: method for method in records["methods"]}
    assert set(methods) == METHODS
    all_records: dict[str, dict] = {}
    for method_id, method in methods.items():
        phase_ids = set()
        method_kinds = set()
        for phase in method["phases"]:
            assert phase["level"] == "method_phase"
            assert phase["collision_participation"] == "none"
            assert set(phase["operation_kinds"]) <= KINDS
            phase_ids.add(phase["phase_id"])
            all_records[phase["phase_id"]] = phase
        for move in method["moves"]:
            assert set(move) >= MOVE_FIELDS, (method_id, move["record_id"], MOVE_FIELDS - set(move))
            assert move["level"] == "analytical_move"
            assert move["parent_phase"] in phase_ids
            assert move["operation_kind"] in KINDS
            assert move["collision_participation"] == "level_2_only"
            assert set(move["guards"]) == {"temporal", "access", "run_version"}
            assert move["source_basis"] and move["exact_anchors"]
            assert set(move["exact_anchors"]) <= canonical_anchor_ids, move["record_id"]
            assert move["record_id"] not in all_records
            all_records[move["record_id"]] = move
            method_kinds.add(move["operation_kind"])
        for action in method["actions"]:
            assert set(action) >= ACTION_FIELDS, (method_id, action["record_id"], ACTION_FIELDS - set(action))
            assert action["level"] == "execution_action"
            assert action["parent_move"] in all_records
            assert action["operation_kind"] in KINDS
            assert action["collision_participation"] == "level_3_only"
            assert action["source_basis"] and action["exact_anchors"]
            assert set(action["exact_anchors"]) <= canonical_anchor_ids, action["record_id"]
            assert action["record_id"] not in all_records
            all_records[action["record_id"]] = action
            method_kinds.add(action["operation_kind"])
        assert method_kinds == KINDS, f"{method_id}: must trace all operation kinds"
        assert set().union(*(set(phase["operation_kinds"]) for phase in method["phases"])) == KINDS

    connections = graph["connections"]
    assert set(graph["connection_types"]) == CONNECTION_TYPES
    assert graph["artifact_flow_defaults"]["transfer_semantics"] == "preserving"
    assert {edge["connection_type"] for edge in connections} == CONNECTION_TYPES
    participants = {edge["from"] for edge in connections} | {edge["to"] for edge in connections}
    for record_id, record in all_records.items():
        if record["level"] != "method_phase":
            assert record_id in participants, f"unconnected record: {record_id}"
    for edge in connections:
        assert edge["from"] in all_records and edge["to"] in all_records, edge["id"]
        if edge["connection_type"] == "artifact_flow" and "adapter_note" not in edge:
            assert edge["from_output"] == edge["carries"] == edge["to_input"], edge["id"]

    expected = _pilot_expected_ids()
    seen = {method: set() for method in METHODS}
    for item in dispositions["dispositions"]:
        assert item["method_id"] in METHODS
        assert item["disposition"] in DISPOSITIONS
        assert item["source_id"] not in seen[item["method_id"]], item["source_id"]
        seen[item["method_id"]].add(item["source_id"])
        if item["disposition"] == "unresolved":
            assert item["target"] is None and item["reason"]
        else:
            assert item["target"] in all_records, item
            expected_level = {"phase": "method_phase"}.get(
                item["disposition"], item["disposition"]
            )
            assert all_records[item["target"]]["level"] == expected_level
    assert seen == expected, {
        method: {"missing": sorted(expected[method] - seen[method]), "extra": sorted(seen[method] - expected[method])}
        for method in METHODS
    }

    assert vocabulary["verbs"]["adoption"] is False
    assert vocabulary["types"]["adoption"] is False
    instrument = INSTRUMENT.read_text(encoding="utf-8")
    readout = READOUT.read_text(encoding="utf-8")
    for text in (instrument, readout):
        assert "three materially different methods" in text
        assert "fourth" in text and "hostile" in text
    assert "Phase 4" in instrument and "Phase 5" in instrument
    assert re.search(r"Level 3 execution\s+actions participate", instrument)
    assert "Phase 2b/Phase 3 portfolio" in instrument
    pressure = (base / "CAPABILITY_PRESSURE_READOUT.md").read_text(encoding="utf-8")
    assert "six authority roles" in pressure.lower()
    assert "three materially different methods" in pressure
    assert "fourth" in pressure and "hostile" in pressure


def main() -> None:
    validate_revision()
    print("Phase 1 revision validates: populated records, typed graph, exact audit coverage, rev-5.1 threshold preserved.")


if __name__ == "__main__":
    main()
