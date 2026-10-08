#!/usr/bin/env python3
"""Plan #6 method crosswalk: generate the Phase 4 collision groups and check the crosswalk and Phase 5 verdicts.

Reads the 14 accepted Phase 3 records (read-only), `phase4/crosswalk.yaml` (STATO terms per statistical step) and
`phase5/adjudication.yaml` (one rev 5.1 section 10 verdict per multi-method group).

Groups (rev 5.1 section 9), each kept only when its members come from two or more methods:
- `sig:`   canonical signature: verb plus the sorted multiset of (type, role, cardinality, optional) for inputs and
           for outputs, slot names dropped;
- `verb:`  same verb, any signature (catches inconsistent typing);
- `types:` same input and output type sets under two or more verbs (same operation, different vocabulary);
- `stato:` the same exact STATO term (Plan #6 rule 2: an exact shared term matches automatically; ancestors do not).

Usage:
    python3 scripts/crosswalk_phase4.py --skeleton   # write crosswalk.yaml rows with anchors, if it does not exist
    python3 scripts/crosswalk_phase4.py              # write phase4/collisions.json
    python3 scripts/crosswalk_phase4.py --check      # regenerate and check everything; exit 1 on any error
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/research/method_decomposition"
METHODS = BASE / "phase3/methods"
TERMS = BASE / "phase4/stato_terms_2026-04-20.json"
CROSSWALK = BASE / "phase4/crosswalk.yaml"
COLLISIONS = BASE / "phase4/collisions.json"
ADJUDICATION = BASE / "phase5/adjudication.yaml"
STATISTICAL_VERBS = {"estimate", "fit", "test", "calibrate", "aggregate", "measure", "simulate", "project", "derive"}
VERDICTS = {"same_capability", "shared_shell", "different_capability"}


def _defaults(records: dict, kind: str) -> dict:
    d = records.get(f"{kind}_defaults")
    if d is None and isinstance(records.get("defaults"), dict):
        d = records["defaults"].get(kind) or (records["defaults"] if kind == "move" else None)
    return dict(d or {})


def load_steps(methods: Path = METHODS) -> list[dict]:
    steps = []
    for m in sorted(p for p in methods.iterdir() if p.is_dir()):
        records = yaml.safe_load((m / "method_records.yaml").read_text())
        for kind in ("move", "action"):
            base = _defaults(records, kind)
            for row in records.get(f"{kind}s", []):
                r = {**base, **row}
                steps.append({"method": m.name, "record_id": r["record_id"], "level": kind, "verb": r.get("verb"),
                              "inputs": r.get("inputs") or [], "outputs": r.get("outputs") or [],
                              "anchors": list(r.get("exact_anchors") or []), "source_basis": r.get("source_basis"),
                              "permitted_conclusion": r.get("permitted_conclusion"), "label": r.get("label")})
    return steps


def signature(slots: list[dict]) -> list[tuple]:
    return sorted((s["type"], s["role"], s["cardinality"], bool(s.get("optional", False))) for s in slots)


def _gid(prefix: str, key: Any) -> str:
    return f"{prefix}:{hashlib.sha256(json.dumps(key, sort_keys=True).encode()).hexdigest()[:10]}"


def groups(steps: list[dict], crosswalk: dict[str, dict]) -> list[dict]:
    buckets: dict[tuple, dict] = {}
    def add(kind: str, key: Any, step: dict, gid: str, describe: dict) -> None:
        b = buckets.setdefault((kind, json.dumps(key, sort_keys=True)), {"group_id": gid, "kind": kind, **describe, "members": []})
        b["members"].append(f"{step['method']}:{step['record_id']}")
    by_type: dict[tuple, set] = defaultdict(set)
    for s in steps:
        sig = [s["verb"], signature(s["inputs"]), signature(s["outputs"])]
        add("signature", sig, s, _gid("sig", sig), {"verb": s["verb"], "canonical_inputs": sig[1], "canonical_outputs": sig[2]})
        add("verb_only", s["verb"], s, f"verb:{s['verb']}", {"verb": s["verb"]})
        types = [sorted({x[0] for x in sig[1]}), sorted({x[0] for x in sig[2]})]
        add("type_pair", types, s, _gid("types", types), {"input_types": types[0], "output_types": types[1]})
        by_type[json.dumps(types)].add(s["verb"])
        for term in (crosswalk.get(f"{s['method']}:{s['record_id']}", {}).get("stato") or []):
            add("stato_term", term, s, f"stato:{term}", {"stato": term})
    out = []
    for (kind, key), b in sorted(buckets.items()):
        methods = {m.split(":")[0] for m in b["members"]}
        if len(methods) < 2:
            continue
        if kind == "type_pair" and len(by_type[key]) < 2:
            continue                                   # same types under one verb is already a signature/verb group
        b["methods"] = sorted(methods)
        out.append(b)
    return out


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text()) if path.is_file() else None


def check_crosswalk(steps: list[dict], rows: list[dict] | None, terms: dict) -> list[str]:
    if rows is None:
        return [f"{CROSSWALK.name} is missing"]
    errors = []
    by_key = {}
    for r in rows:
        k = f"{r.get('method')}:{r.get('record_id')}"
        if k in by_key:
            errors.append(f"crosswalk lists {k} twice")
        by_key[k] = r
    for s in steps:
        k = f"{s['method']}:{s['record_id']}"
        r = by_key.pop(k, None)
        if r is None:
            errors.append(f"crosswalk lacks {k}")
            continue
        if list(r.get("anchors") or []) != s["anchors"]:
            errors.append(f"{k}: anchors differ from the record's exact_anchors")
        if not isinstance(r.get("statistical"), bool):
            errors.append(f"{k}: statistical must be true or false")
            continue
        if r["statistical"]:
            ids = r.get("stato") or []
            if not ids:
                errors.append(f"{k}: a statistical step needs at least one STATO term")
            for t in ids:
                if t not in terms:
                    errors.append(f"{k}: {t} is not a term of the pinned STATO release")
                elif terms[t]["deprecated"]:
                    errors.append(f"{k}: {t} ({terms[t]['label']}) is deprecated")
            if not (r.get("reason") or "").strip():
                errors.append(f"{k}: a statistical step states why its terms fit")
        else:
            if r.get("stato"):
                errors.append(f"{k}: a non-statistical step carries STATO terms")
            if s["verb"] in STATISTICAL_VERBS and not (r.get("reason") or "").strip():
                errors.append(f"{k}: verb {s['verb']!r} looks statistical; state why it is not")
    errors += [f"crosswalk lists {k}, which is not a Phase 3 step" for k in by_key]
    return errors


def check_adjudication(found: list[dict], rows: list[dict] | None) -> list[str]:
    if rows is None:
        return [f"{ADJUDICATION.name} is missing"]
    errors = []
    by_id = {}
    for r in rows:
        if r.get("group_id") in by_id:
            errors.append(f"adjudication lists {r.get('group_id')} twice")
        by_id[r.get("group_id")] = r
    for g in found:
        r = by_id.pop(g["group_id"], None)
        if r is None:
            errors.append(f"no verdict for {g['group_id']} ({g['kind']}, {', '.join(g['methods'])})")
            continue
        v = r.get("verdict")
        if v not in VERDICTS:
            errors.append(f"{g['group_id']}: verdict {v!r} is not one of {sorted(VERDICTS)}")
            continue
        if len((r.get("justification") or "").split()) < 12:
            errors.append(f"{g['group_id']}: the justification is missing or too short to be one")
        if sorted(r.get("members") or []) != sorted(g["members"]):
            errors.append(f"{g['group_id']}: verdict members differ from the generated group")
        if v == "same_capability":
            hostile = r.get("hostile_method") or ""
            if not hostile or hostile in g["methods"] or not (r.get("hostile_argument") or "").strip():
                errors.append(f"{g['group_id']}: same_capability must name a method outside the group and argue whether it could use it")
        if v == "shared_shell" and not ((r.get("shell_does") or "").strip() and (r.get("delegated") or "").strip()):
            errors.append(f"{g['group_id']}: shared_shell must say what the shell does and what it delegates")
        if v == "different_capability" and not (r.get("what_breaks_if_merged") or "").strip():
            errors.append(f"{g['group_id']}: different_capability must say what breaks if merged")
    errors += [f"adjudication lists {k}, which is not a generated group" for k in by_id]
    return errors


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--skeleton", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    steps = load_steps()
    terms = json.loads(TERMS.read_text())["terms"]
    if a.skeleton:
        if CROSSWALK.exists():
            print(f"RESULT: FAIL (exit 1) {CROSSWALK.name} exists; not overwritten")
            return 1
        rows = [{"method": s["method"], "record_id": s["record_id"], "verb": s["verb"], "label": s["label"],
                 "anchors": s["anchors"], "source_basis": s["source_basis"], "statistical": None, "stato": [],
                 "reason": ""} for s in steps]
        CROSSWALK.write_text(yaml.safe_dump(rows, sort_keys=False, allow_unicode=True, width=120))
        print(f"RESULT: PASS (exit 0) wrote {CROSSWALK.name} skeleton rows={len(rows)}")
        return 0
    rows = load_yaml(CROSSWALK)
    crosswalk = {f"{r['method']}:{r['record_id']}": r for r in rows or []}
    found = groups(steps, crosswalk)
    text = json.dumps({"record_type": "Phase4CollisionGroups", "plan": "Plan #6", "steps": len(steps),
                       "groups": found}, indent=1) + "\n"
    if not a.check:
        COLLISIONS.write_text(text)
        print(f"RESULT: PASS (exit 0) wrote {COLLISIONS.name} groups={len(found)}")
        return 0
    errors = []
    if not COLLISIONS.is_file() or COLLISIONS.read_text() != text:
        errors.append(f"{COLLISIONS.name} is stale: run scripts/crosswalk_phase4.py")
    errors += check_crosswalk(steps, rows, terms)
    errors += check_adjudication(found, load_yaml(ADJUDICATION))
    for e in errors:
        print("ERROR", e)
    kinds = defaultdict(int)
    for g in found:
        kinds[g["kind"]] += 1
    stat = sum(1 for r in rows or [] if r.get("statistical") is True)
    print(f"RESULT: {'FAIL' if errors else 'PASS'} (exit {1 if errors else 0}) steps={len(steps)} statistical={stat} "
          f"groups={len(found)} {dict(sorted(kinds.items()))} errors={len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
