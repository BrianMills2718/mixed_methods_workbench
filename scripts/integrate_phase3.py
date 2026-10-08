#!/usr/bin/env python3
"""P3-INTEGRATE: validate the 14 accepted Phase 3 decompositions as one portfolio (Plan #4).

Writes the unit's three outputs from the committed graph and Git history:
- portfolio_manifest.yaml (JSON-compatible YAML): each of p01-p14 once, its owner lane, the accepted evidence commit
  named by that lane's CompletionReceipt, and the SHA-256 of its five artifacts at that commit;
- validation_report.json: deterministic checks per method and for the portfolio, plus whole-portfolio negative controls;
- integration_report.md: the same result in words, with any defect returned to its owning lane.

Checks: exact denominator; every method owned by the lane that accepted it; five artifacts present at the evidence
commit and unchanged since; the structural check (scripts/validate_phase3_methods.py) with zero errors; and no
out-of-scope claim (a collision verdict, adjudication, coverage or promotion result, shared schema or implementation
authorization), detected structurally by field names and verdict tokens, never by reading prose.
Integration does not repair or normalize method-owned semantics. `--check` exits 1 if the committed outputs are stale.

Usage: python3 scripts/integrate_phase3.py --spec <pinned rev 5.1 spec> [--check]
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_phase3_methods as vm  # noqa: E402

PHASE3 = "docs/research/method_decomposition/phase3"
GRAPH = f"{PHASE3}/4_phase3_portfolio_decomposition_work_graph.json"
OUT = {"manifest": ROOT / PHASE3 / "portfolio_manifest.yaml", "report": ROOT / PHASE3 / "validation_report.json",
       "markdown": ROOT / PHASE3 / "integration_report.md"}
LANES = {"P3-RESEARCH-A": ["p01", "p02", "p03", "p04", "p14"], "P3-RESEARCH-B": ["p06", "p07", "p08", "p09"],
         "P3-RESEARCH-C": ["p05", "p10", "p11", "p12", "p13"]}
EXPECTED = [f"p{n:02d}" for n in range(1, 15)]
FORBIDDEN_KEYS = ("collision_verdict", "collision_group", "adjudication", "verdict", "capability_promotion",
                  "promotion", "coverage_result", "coverage_estimate", "shared_schema", "implementation_authorization")
VERDICT_TOKENS = {"same_capability", "shared_shell", "different_capability"}
PARTICIPATION = {"none", "level_2_only", "level_3_only"}


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout


def git_bytes(*args: str) -> bytes | None:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=False)
    return r.stdout if r.returncode == 0 else None


def out_of_scope(doc: Any, where: str) -> list[str]:
    """Structural scan: forbidden field names, verdict tokens as values, participation outside the allowed set."""
    found: list[str] = []
    def walk(o: Any, path: str) -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                lk = str(k).lower()
                if any(lk == f or lk.startswith(f + "_") or lk.endswith("_" + f) for f in FORBIDDEN_KEYS):
                    found.append(f"{where}: out-of-scope field {path}.{k}")
                if lk == "collision_participation" and str(v) not in PARTICIPATION:
                    found.append(f"{where}: collision_participation {v!r} at {path} is not one of {sorted(PARTICIPATION)}")
                walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, x in enumerate(o):
                walk(x, f"{path}[{i}]")
        elif isinstance(o, str) and o.strip().lower() in VERDICT_TOKENS:
            found.append(f"{where}: adjudication verdict {o!r} at {path}")
    walk(doc, "")
    return found


def denominator_errors(directories: list[str]) -> list[str]:
    """The method directories must be exactly p01-p14, each once."""
    errors = []
    dupes = sorted({d for d in directories if directories.count(d) > 1})
    if dupes:
        errors.append(f"duplicated method directories: {', '.join(dupes)}")
    missing, extra = sorted(set(EXPECTED) - set(directories)), sorted(set(directories) - set(EXPECTED))
    if missing:
        errors.append(f"missing methods: {', '.join(missing)}")
    if extra:
        errors.append(f"extra methods: {', '.join(extra)}")
    return errors


def accepted_evidence(graph: dict) -> tuple[dict[str, str], list[str]]:
    evidence, errors = {}, []
    units = {u["id"]: u for u in graph["units"]}
    for lane in LANES:
        u = units[lane]
        receipts = [i for i in u["inputs"] if i["kind"] == "CompletionReceipt"]
        if u["status"] != "accepted" or len(receipts) != 1:
            errors.append(f"{lane} is {u['status']}, not accepted with one CompletionReceipt: return to {lane}")
            continue
        evidence[lane] = receipts[0]["revision"].split("evidence=")[1].split(";")[0]
    return evidence, errors


def build(spec: Path) -> dict[Path, str]:
    verbs, types = vm.spec_lists(spec)
    graph = json.loads((ROOT / GRAPH).read_text())
    evidence, errors = accepted_evidence(graph)
    head = git("rev-parse", "HEAD").strip()
    methods, checks = [], []
    owners = {m: lane for lane, ms in LANES.items() for m in ms}
    if sorted(owners) != EXPECTED or len(owners) != 14:
        errors.append("lane ownership does not cover p01-p14 exactly once")
    on_disk = sorted(p.name for p in (ROOT / PHASE3 / "methods").iterdir() if p.is_dir())
    errors += denominator_errors(on_disk)
    for m in EXPECTED:
        lane = owners[m]
        row: dict[str, Any] = {"method_id": m, "owner_unit": lane, "evidence_commit": evidence.get(lane), "artifacts": {}}
        problems: list[str] = []
        if lane not in evidence:
            problems.append(f"{lane} has no accepted evidence commit")
        else:
            for f in vm.FILES:
                path = f"{PHASE3}/methods/{m}/{f}"
                at_evidence = git_bytes("show", f"{evidence[lane]}:{path}")
                now = (ROOT / path).read_bytes() if (ROOT / path).is_file() else None
                if at_evidence is None:
                    problems.append(f"{path} absent at evidence commit {evidence[lane][:12]}")
                    continue
                row["artifacts"][f] = hashlib.sha256(at_evidence).hexdigest()
                if now != at_evidence:
                    problems.append(f"{path} changed after acceptance at {evidence[lane][:12]}")
        errs, warns = vm.check_method(ROOT / PHASE3 / "methods" / m, verbs, types)
        problems += errs
        for f in vm.FILES:
            p = ROOT / PHASE3 / "methods" / m / f
            if f.endswith(".yaml") and p.is_file():
                problems += out_of_scope(yaml.safe_load(p.read_text()), f"{m}/{f}")
        row["structural_warnings"] = warns
        methods.append(row)
        checks.append({"method_id": m, "owner_unit": lane, "passed": not problems,
                       "defects_returned_to_owner": problems})
    # Whole-portfolio negative controls: each injected defect must be caught.
    sample = yaml.safe_load((ROOT / PHASE3 / "methods/p01/method_records.yaml").read_text())
    injected = copy.deepcopy(sample)
    injected["moves"][0]["collision_verdict"] = "same_capability"
    controls = [
        {"control": "an injected collision verdict is refused", "caught": bool(out_of_scope(injected, "control"))},
        {"control": "an injected coverage result is refused",
         "caught": bool(out_of_scope({"coverage_result": {"methods_covered": 14}}, "control"))},
        {"control": "a missing method fails the denominator", "caught": bool(denominator_errors(EXPECTED[:-1]))},
        {"control": "a duplicated method fails the denominator", "caught": bool(denominator_errors(EXPECTED + ["p01"]))},
        {"control": "an extra method fails the denominator", "caught": bool(denominator_errors(EXPECTED + ["p15"]))},
        {"control": "the real denominator passes", "caught": not denominator_errors(EXPECTED)},
    ]
    if not all(c["caught"] for c in controls):
        errors.append("a negative control was not caught")
    passed = not errors and all(c["passed"] for c in checks)
    report = {"record_type": "Phase3ValidationReport", "unit_id": "P3-INTEGRATE", "graph": GRAPH,
              "spec_sha256": vm.SPEC_SHA256, "denominator": EXPECTED, "result": "pass" if passed else "fail",
              "portfolio_errors": errors, "methods": checks, "negative_controls": controls,
              "non_claims": ["no collision candidates, verdicts or adjudication", "no coverage or automation result",
                             "no shared schema adopted", "no implementation authorized",
                             "no reusable capability established"]}
    manifest = {"record_type": "Phase3PortfolioManifest", "unit_id": "P3-INTEGRATE", "plan": "Plan #4",
                "denominator": "phase2b-proposal-0.3 (P01-P13) plus P14, approved by Brian 2026-08-13",
                "methods": methods}
    failed = [c for c in checks if not c["passed"]]
    md = [f"# Phase 3 integration report (P3-INTEGRATE, Plan #4)", "",
          f"Result: **{'PASS' if passed else 'FAIL'}**: {sum(c['passed'] for c in checks)} of 14 methods pass; "
          f"{len(errors)} portfolio error(s); {sum(c['caught'] for c in controls)} of {len(controls)} negative controls caught.", "",
          "Generated by `scripts/integrate_phase3.py` from the committed work graph and each lane's accepted evidence "
          "commit; `portfolio_manifest.yaml` lists every method's evidence commit and artifact hashes and "
          "`validation_report.json` holds every check.", "",
          "| Method | Owner | Evidence commit | Result |", "| --- | --- | --- | --- |"]
    for row, c in zip(methods, checks):
        md.append(f"| {row['method_id']} | {row['owner_unit']} | {(row['evidence_commit'] or 'not accepted')[:12]} | "
                  f"{'pass' if c['passed'] else 'returned to owner: ' + '; '.join(c['defects_returned_to_owner'][:3])} |")
    md += ["", "## Portfolio checks", ""] + ([f"- {e}" for e in errors] or ["- denominator p01–p14 exactly once; every method owned by the lane that accepted it"])
    md += ["", "## What this does not establish", ""] + [f"- {n}" for n in report["non_claims"]] + [""]
    if failed or errors:
        md.insert(4, "Defects are returned to the owning lane; integration does not repair or normalize method-owned records.\n")
    return {OUT["manifest"]: json.dumps(manifest, indent=2) + "\n", OUT["report"]: json.dumps(report, indent=2) + "\n",
            OUT["markdown"]: "\n".join(md)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--spec", default=os.environ.get("MMW_DECOMPOSITION_SPEC"), required=os.environ.get("MMW_DECOMPOSITION_SPEC") is None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    files = build(Path(a.spec))
    result = json.loads(files[OUT["report"]])["result"]
    if a.check:
        stale = [p.name for p, t in files.items() if not p.exists() or p.read_text() != t]
        ok = not stale and result == "pass"
        print(f"RESULT: {'PASS' if ok else 'FAIL'} (exit {0 if ok else 1}) integration={result} stale={stale}")
        return 0 if ok else 1
    for p, t in files.items():
        p.write_text(t)
    print(f"RESULT: {'PASS' if result == 'pass' else 'FAIL'} (exit {0 if result == 'pass' else 1}) integration={result} wrote {', '.join(p.name for p in files)}")
    return 0 if result == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
