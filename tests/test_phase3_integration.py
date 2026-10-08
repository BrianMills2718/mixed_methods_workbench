"""P3-INTEGRATE (scripts/integrate_phase3.py): the 14 accepted decompositions validate as one portfolio."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import integrate_phase3 as ip  # noqa: E402

SPEC = Path(os.environ.get("MMW_DECOMPOSITION_SPEC", Path.home() / "code/_docs/METHOD_DECOMPOSITION_HANDOFF.md"))
assert SPEC.is_file(), f"pinned rev 5.1 spec not found at {SPEC}; set MMW_DECOMPOSITION_SPEC"   # no skip


def test_committed_outputs_are_current_and_pass():
    files = ip.build(SPEC)
    for path, text in files.items():
        assert path.read_text() == text, f"{path.name} is stale: run scripts/integrate_phase3.py"
    report = json.loads(files[ip.OUT["report"]])
    assert report["result"] == "pass" and [c["method_id"] for c in report["methods"]] == ip.EXPECTED
    manifest = json.loads(files[ip.OUT["manifest"]])
    assert all(len(m["artifacts"]) == 5 and m["evidence_commit"] for m in manifest["methods"])


def test_a_method_edited_after_acceptance_is_returned_to_its_lane():
    path = ROOT / ip.PHASE3 / "methods/p06/uncertainty.yaml"
    original = path.read_bytes()
    try:
        path.write_bytes(original + b"# edited after acceptance\n")
        report = json.loads(ip.build(SPEC)[ip.OUT["report"]])
        p06 = next(c for c in report["methods"] if c["method_id"] == "p06")
        assert report["result"] == "fail" and not p06["passed"] and p06["owner_unit"] == "P3-RESEARCH-B"
        assert any("changed after acceptance" in d for d in p06["defects_returned_to_owner"])
    finally:
        path.write_bytes(original)


def test_out_of_scope_claims_are_found_structurally_not_in_prose():
    assert ip.out_of_scope({"moves": [{"collision_verdict": "x"}]}, "t")
    assert ip.out_of_scope({"notes": "same_capability"}, "t")
    assert ip.out_of_scope({"collision_participation": "merged"}, "t")
    # method prose that uses the word 'coverage' (survey frame coverage, QCA coverage) is not a coverage claim
    assert not ip.out_of_scope({"method_owned_rule": "coverage gaps remain visible", "collision_participation": "level_2_only"}, "t")


def test_the_denominator_rejects_missing_duplicate_and_extra_methods():
    assert ip.denominator_errors(ip.EXPECTED) == []
    assert ip.denominator_errors(ip.EXPECTED[:-1]) and ip.denominator_errors(ip.EXPECTED + ["p03"]) and ip.denominator_errors(ip.EXPECTED + ["p15"])


def test_a_lane_without_a_receipt_is_not_integrated():
    graph = json.loads((ROOT / ip.GRAPH).read_text())
    lane = next(u for u in graph["units"] if u["id"] == "P3-RESEARCH-C")
    lane["status"] = "ready"
    lane["inputs"] = [i for i in lane["inputs"] if i["kind"] != "CompletionReceipt"]
    evidence, errors = ip.accepted_evidence(graph)
    assert "P3-RESEARCH-C" not in evidence and any("return to P3-RESEARCH-C" in e for e in errors)
