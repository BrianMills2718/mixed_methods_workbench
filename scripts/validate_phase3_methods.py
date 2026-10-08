#!/usr/bin/env python3
"""Focused structural validation of Phase 3 method decompositions (Plan #4, P3-CONTROL and P3-INTEGRATE checks).

Checks each `methods/pNN/` directory against the accepted Phase 2 discovery format (instrument 89e9515) and the
pinned method-decomposition spec rev 5.1 (its controlled verb and type lists are read from the spec file itself,
whose SHA-256 must match Plan #4's pin). Errors fail the run; warnings are reported for the reviewer.

Passing means a decomposition is structurally complete and internally consistent. It does not establish that the
method is described correctly, that its sources are adequate, or that any step is reusable: that is the reviewer's
judgement against each lane's acceptance criteria.

Usage:
    python3 scripts/validate_phase3_methods.py --spec <METHOD_DECOMPOSITION_HANDOFF.md> [p06 p07 ...]
The spec path may also come from MMW_DECOMPOSITION_SPEC.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
METHODS = ROOT / "docs/research/method_decomposition/phase3/methods"
SPEC_SHA256 = "fbeb0e187f219a11051ba54fee6537b70448611080351044dc49f421e3c16c2f"   # Plan #4 adopted input
FILES = ("frame.yaml", "sources.md", "method_records.yaml", "connections.yaml", "uncertainty.yaml")
OPERATION_KINDS = {"analytic", "methodological_support", "runtime_delivery"}
ORIGINS = {"observed", "reported", "elicited", "interpreted", "derived", "simulated"}
ROLES = ("performer", "judgment_owner", "acceptance_authority", "recommender", "value_goal_authority",
         "decision_authority")
GUARDS = ("temporal", "access", "run_version")
CONNECTION_TYPES = {"artifact_flow", "retained_context", "control_gate", "feedback", "prohibited_transition"}
UNCERTAINTY = {"known", "unknown", "contested", "source_limited"}
SLOT_ROLES_IN = {"subject", "criteria", "context", "prior", "config_data"}
SLOT_ROLES_OUT = {"result", "byproduct", "state_marker", "trace"}
CARDINALITY = {"one", "many", "optional_one", "optional_many"}
MOVE_FIELDS = ("record_id", "level", "label", "verb", "operation_kind", "inputs", "outputs", "information_origin",
               "source_authority_or_inferential_role", "applicability_boundary", "method_owned_rule",
               "permitted_conclusion", "refusal_or_qualification", *ROLES, "implementation_evidence",
               "source_basis", "exact_anchors", "guards")


def spec_lists(path: Path) -> tuple[set[str], set[str]]:
    raw = path.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != SPEC_SHA256:
        raise SystemExit(f"spec {path} has sha256 {got[:16]}, not Plan #4's pinned {SPEC_SHA256[:16]}")
    text = raw.decode()
    def fenced_after(marker: str) -> str:
        i = text.index(marker)
        a = text.index("```", i) + 3
        return text[a:text.index("```", a)]
    verbs = set(fenced_after("## 6. Controlled verb list").split())
    types = set(fenced_after("Types come from the controlled list below").split())
    return verbs, types


def _defaults(records: dict, kind: str) -> dict:
    d = records.get(f"{kind}_defaults")
    if d is None and isinstance(records.get("defaults"), dict):
        d = records["defaults"].get(kind) or (records["defaults"] if kind == "move" else None)
    return dict(d or {})


def _items(doc: dict, *keys: str) -> list:
    for k in keys:
        if isinstance(doc.get(k), list):
            return doc[k]
    return []


def check_method(path: Path, verbs: set[str], types: set[str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    m = path.name
    for f in FILES:
        if not (path / f).is_file():
            errors.append(f"{m}: missing {f}")
    if errors:
        return errors, warnings
    load = lambda f: yaml.safe_load((path / f).read_text()) or {}
    frame, records, conns, unc = load("frame.yaml"), load("method_records.yaml"), load("connections.yaml"), load("uncertainty.yaml")
    if str(records.get("method_id", "")).lower() != m:
        errors.append(f"{m}: method_records.yaml method_id is {records.get('method_id')!r}")

    phases = {p.get("phase_id") or p.get("record_id") or p.get("id") for p in _items(records, "phases")}
    if not phases:
        errors.append(f"{m}: no Level 1 method phases")
    moves, actions = _items(records, "moves"), _items(records, "actions")
    if not moves:
        errors.append(f"{m}: no Level 2 analytical moves")
    if not actions:
        errors.append(f"{m}: no Level 3 execution actions")
    ids: dict[str, str] = {}
    extensions: set[str] = set()
    for kind, rows in (("move", moves), ("action", actions)):
        base = _defaults(records, kind)
        for row in rows:
            r = {**base, **row}
            rid = r.get("record_id", "?")
            if rid in ids:
                errors.append(f"{m}: duplicate record_id {rid}")
            ids[rid] = kind
            missing = [f for f in MOVE_FIELDS if f not in r or r[f] in (None, "", [])]
            if missing:
                errors.append(f"{m}: {rid} lacks {', '.join(missing)}")
            if r.get("verb") and r["verb"] not in verbs:
                errors.append(f"{m}: {rid} verb {r['verb']!r} is not in the spec's controlled verb list")
            if r.get("operation_kind") and r["operation_kind"] not in OPERATION_KINDS:
                errors.append(f"{m}: {rid} operation_kind {r['operation_kind']!r} is not analytic, methodological_support or runtime_delivery")
            bad_origin = set(r.get("information_origin") or []) - ORIGINS
            if bad_origin:
                errors.append(f"{m}: {rid} information_origin {sorted(bad_origin)} not in {sorted(ORIGINS)}")
            for side, roles in (("inputs", SLOT_ROLES_IN), ("outputs", SLOT_ROLES_OUT)):
                for slot in r.get(side) or []:
                    if not isinstance(slot, dict) or not {"slot", "type", "role", "cardinality"} <= set(slot):
                        errors.append(f"{m}: {rid} {side} entry {str(slot)[:40]!r} is not a named slot (slot, type, role, cardinality)")
                        continue
                    if slot["role"] not in roles:
                        errors.append(f"{m}: {rid} {side} slot {slot['slot']} role {slot['role']!r} not in {sorted(roles)}")
                    if slot["cardinality"] not in CARDINALITY:
                        errors.append(f"{m}: {rid} {side} slot {slot['slot']} cardinality {slot['cardinality']!r} not in {sorted(CARDINALITY)}")
                    if slot["type"] not in types:
                        extensions.add(slot["type"])
            g = r.get("guards") or {}
            if isinstance(g, dict):
                missing_g = [x for x in GUARDS if not g.get(x)]
                if missing_g:
                    errors.append(f"{m}: {rid} guards lack {', '.join(missing_g)}")
            parent = r.get("parent_phase") if kind == "move" else r.get("parent_move")
            if kind == "move" and parent not in phases:
                errors.append(f"{m}: {rid} parent_phase {parent!r} is not a phase")
    move_ids = {k for k, v in ids.items() if v == "move"}
    for row in actions:
        if row.get("parent_move") not in move_ids:
            errors.append(f"{m}: action {row.get('record_id')} parent_move {row.get('parent_move')!r} is not a move")
    if extensions:
        notes = (path / "sources.md").read_text() + (path / "frame.yaml").read_text() + (path / "method_records.yaml").read_text()
        unexplained = sorted(t for t in extensions if not re.search(rf"\b{re.escape(t)}\b.{{0,200}}(no existing type|extension|added because|why)", notes, re.I | re.S))
        warnings.append(f"{m}: types outside the spec's list: {', '.join(sorted(extensions))}"
                        + (f" (no stated reason found for {', '.join(unexplained)})" if unexplained else ""))

    edges = _items(conns, "connections", "edges")
    if not edges:
        errors.append(f"{m}: connections.yaml has no connections")
    for e in edges:
        eid = e.get("id", "?")
        t = e.get("connection_type")
        if t not in CONNECTION_TYPES:
            errors.append(f"{m}: connection {eid} type {t!r} is not one of the five")
        for end in ("from", "to"):
            if e.get(end) not in ids:
                errors.append(f"{m}: connection {eid} {end} {e.get(end)!r} is not a record")
        if t == "artifact_flow" and not (e.get("carries") or e.get("artifact")):
            errors.append(f"{m}: artifact_flow {eid} names nothing it carries")
    used = {t for t in (e.get("connection_type") for e in edges)}
    if "prohibited_transition" not in used:
        warnings.append(f"{m}: no prohibited_transition recorded")
    if not isinstance(conns.get("topology"), dict):
        warnings.append(f"{m}: connections.yaml declares no topology block (shape, required/optional cycles)")

    items = _items(unc, "judgments", "items")
    if not items:
        errors.append(f"{m}: uncertainty.yaml has no judgments")
    for u in items:
        if u.get("status") not in UNCERTAINTY:
            errors.append(f"{m}: uncertainty {u.get('id')} status {u.get('status')!r} not in {sorted(UNCERTAINTY)}")
        if not u.get("downstream_effect"):
            errors.append(f"{m}: uncertainty {u.get('id')} states no downstream_effect")
    statuses = {u.get("status") for u in items}
    if "unknown" not in statuses:
        warnings.append(f"{m}: no 'unknown' uncertainty recorded (known, contested and source_limited only)")
    if not frame:
        errors.append(f"{m}: frame.yaml is empty")
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("methods", nargs="*", help="method ids (default: every directory)")
    ap.add_argument("--spec", default=os.environ.get("MMW_DECOMPOSITION_SPEC"), required=os.environ.get("MMW_DECOMPOSITION_SPEC") is None)
    ap.add_argument("--root", default=str(METHODS))
    a = ap.parse_args(argv)
    verbs, types = spec_lists(Path(a.spec))
    root = Path(a.root)
    names = a.methods or sorted(p.name for p in root.iterdir() if p.is_dir())
    errors: list[str] = []
    warnings: list[str] = []
    for n in names:
        e, w = check_method(root / n, verbs, types)
        errors += e
        warnings += w
        print(f"{n}: {'ok' if not e else f'{len(e)} error(s)'}, {len(w)} warning(s)")
    for line in errors:
        print("ERROR", line)
    for line in warnings:
        print("WARN ", line)
    print(f"RESULT: {'FAIL' if errors else 'PASS'} (exit {1 if errors else 0}) methods={len(names)} errors={len(errors)} warnings={len(warnings)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
