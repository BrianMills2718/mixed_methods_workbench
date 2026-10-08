"""Plan #6 crosswalk (scripts/crosswalk_phase4.py): groups, STATO checks and section 10 verdict rules."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import crosswalk_phase4 as cx  # noqa: E402

STEPS = cx.load_steps()
TERMS = json.loads(cx.TERMS.read_text())["terms"]


def group_of(steps, key, kind="signature", crosswalk=None):
    for g in cx.groups(steps, crosswalk or {}):
        if g["kind"] == kind and key in g["members"]:
            return g["group_id"]
    return None


def test_all_171_steps_from_14_methods_are_read():
    assert len(STEPS) == 171 and len({s["method"] for s in STEPS}) == 14


def test_a_changed_slot_moves_a_step_between_signature_groups():
    found = [g for g in cx.groups(STEPS, {}) if g["kind"] == "signature"]
    assert found, "expected at least one multi-method signature group"
    member = found[0]["members"][0]
    method, rid = member.split(":", 1)
    steps = copy.deepcopy(STEPS)
    step = next(s for s in steps if s["method"] == method and s["record_id"] == rid)
    before = group_of(steps, member)
    step["inputs"] = step["inputs"] + [{"slot": "extra", "type": "memo", "role": "context", "cardinality": "one", "optional": False}]
    assert before is not None and group_of(steps, member) != before


def test_an_exact_shared_stato_term_groups_steps_but_an_ancestor_does_not():
    a, b = STEPS[0], next(s for s in STEPS if s["method"] != STEPS[0]["method"])
    ka, kb = f"{a['method']}:{a['record_id']}", f"{b['method']}:{b['record_id']}"
    same = {ka: {"stato": ["STATO:0000457"]}, kb: {"stato": ["STATO:0000457"]}}
    assert group_of(STEPS, ka, "stato_term", same) == "stato:STATO:0000457"
    siblings = {ka: {"stato": ["STATO:0000457"]}, kb: {"stato": ["STATO:0000665"]}}   # both under absolute difference
    assert group_of(STEPS, ka, "stato_term", siblings) is None
    assert "STATO:0000614" in TERMS["STATO:0000457"]["parents"] and "STATO:0000614" in TERMS["STATO:0000665"]["parents"]


def rows_for(steps):
    return [{"method": s["method"], "record_id": s["record_id"], "anchors": s["anchors"], "statistical": False,
             "stato": [], "reason": "not statistical"} for s in steps]


def test_unknown_or_missing_stato_terms_fail():
    rows = rows_for(STEPS)
    rows[0].update(statistical=True, stato=["STATO:9999999"], reason="x")
    rows[1].update(statistical=True, stato=[], reason="x")
    errors = cx.check_crosswalk(STEPS, rows, TERMS)
    assert any("not a term of the pinned STATO release" in e for e in errors)
    assert any("needs at least one STATO term" in e for e in errors)


def test_changed_anchors_and_missing_steps_fail():
    rows = rows_for(STEPS)
    rows[0]["anchors"] = ["invented"]
    errors = cx.check_crosswalk(STEPS, rows[:-1], TERMS)
    assert any("anchors differ" in e for e in errors) and any("crosswalk lacks" in e for e in errors)


def test_section_10_rules():
    g = {"group_id": "verb:test", "kind": "verb_only", "methods": ["p01", "p02"], "members": ["p01:a", "p02:b"]}
    long = "this justification is long enough to count as one written reason for the verdict here"
    ok = cx.check_adjudication([g], [{"group_id": "verb:test", "members": g["members"], "verdict": "different_capability",
                                      "justification": long, "what_breaks_if_merged": "the refusal rules"}])
    assert ok == []
    bad = cx.check_adjudication([g], [{"group_id": "verb:test", "members": g["members"], "verdict": "same_capability",
                                       "justification": "short", "hostile_method": "p01"}])
    assert any("too short" in e for e in bad) and any("outside the group" in e for e in bad)
    shell = cx.check_adjudication([g], [{"group_id": "verb:test", "members": g["members"], "verdict": "shared_shell",
                                         "justification": long}])
    assert any("what the shell does" in e for e in shell)
    assert any("no verdict" in e for e in cx.check_adjudication([g], []))


def committed():
    rows = {f"{r['method']}:{r['record_id']}": r for r in cx.load_yaml(cx.CROSSWALK)}
    verdicts = {v["group_id"]: v for v in cx.load_yaml(cx.ADJUDICATION)}
    found = cx.groups(STEPS, rows)
    return rows, verdicts, found


def test_the_committed_crosswalk_and_verdicts_pass_every_check():
    rows, verdicts, found = committed()
    assert cx.check_crosswalk(STEPS, list(rows.values()), TERMS) == []
    assert cx.check_adjudication(found, list(verdicts.values())) == []
    assert len(verdicts) == len(found) and all(v["verdict"] in cx.VERDICTS for v in verdicts.values())


def test_canonical_example_rct_and_did_share_a_signature_group_but_not_a_term():
    rows, verdicts, found = committed()
    itt, did = "p02:p02.action.compute_itt", "p03:p03.action.compute_did"
    assert rows[itt]["stato"] == ["STATO:0000457"] and rows[did]["stato"] == ["STATO:0000665"]   # mean difference vs DiD
    shared = [g for g in found if itt in g["members"] and did in g["members"]]
    kinds = {g["kind"]: g for g in shared}
    assert "signature" in kinds and "stato_term" not in kinds          # grouped by section 9, not by a STATO term
    assert verdicts[kinds["signature"]["group_id"]]["justification"]


def test_canonical_example_the_two_coding_steps_get_written_verdicts():
    rows, verdicts, found = committed()
    for step in ("p05:p05.move.initial_code", "p07:p07.move.annotate"):
        verb_group = next(g for g in found if g["kind"] == "verb_only" and step in g["members"])
        v = verdicts[verb_group["group_id"]]
        assert v["verdict"] == "different_capability" and v["what_breaks_if_merged"].strip()
    assert not any("p05:p05.move.initial_code" in g["members"] and "p07:p07.move.annotate" in g["members"] for g in found)
