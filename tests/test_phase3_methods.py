"""Focused structural validation of Phase 3 method decompositions (scripts/validate_phase3_methods.py)."""
from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_phase3_methods as v  # noqa: E402

SPEC = Path(os.environ.get("MMW_DECOMPOSITION_SPEC", Path.home() / "code/_docs/METHOD_DECOMPOSITION_HANDOFF.md"))
# No skip: without the pinned spec the controlled verb and type lists cannot be checked.
assert SPEC.is_file() and hashlib.sha256(SPEC.read_bytes()).hexdigest() == v.SPEC_SHA256, \
    f"pinned rev 5.1 spec not found at {SPEC}; set MMW_DECOMPOSITION_SPEC"
VERBS, TYPES = v.spec_lists(SPEC)


def copy_method(tmp_path: Path, name: str = "p01") -> Path:
    target = tmp_path / name
    shutil.copytree(v.METHODS / name, target)
    return target


def edit(path: Path, fn) -> None:
    doc = yaml.safe_load(path.read_text())
    fn(doc)
    path.write_text(yaml.safe_dump(doc, sort_keys=False))


def test_spec_lists_are_read_from_the_pinned_spec():
    assert {"compare", "refuse", "simulate", "appraise_source"} <= VERBS and len(VERBS) == 35
    assert {"estimand", "review_event", "design_parameters"} <= TYPES


def test_a_wrong_spec_is_refused(tmp_path):
    bad = tmp_path / "spec.md"
    bad.write_text("not the spec")
    with pytest.raises(SystemExit, match="not Plan #4's pinned"):
        v.spec_lists(bad)


def test_a_complete_decomposition_passes():
    errors, _ = v.check_method(v.METHODS / "p01", VERBS, TYPES)
    assert errors == []


def test_missing_verb_and_bare_slots_fail(tmp_path):
    m = copy_method(tmp_path)
    def strip(doc):
        doc["moves"][0].pop("verb")
        doc["moves"][0]["inputs"] = ["bare_name"]
    edit(m / "method_records.yaml", strip)
    errors, _ = v.check_method(m, VERBS, TYPES)
    assert any("lacks verb" in e for e in errors) and any("is not a named slot" in e for e in errors)


def test_an_input_with_an_output_only_role_fails(tmp_path):
    m = copy_method(tmp_path)
    edit(m / "method_records.yaml", lambda d: d["moves"][0]["inputs"][0].update(role="trace"))
    errors, _ = v.check_method(m, VERBS, TYPES)
    assert any("role 'trace'" in e for e in errors)


def test_a_dangling_connection_and_an_untyped_one_fail(tmp_path):
    m = copy_method(tmp_path)
    def bad(doc):
        doc["connections"][0]["to"] = "p01.move.nowhere"
        doc["connections"][1]["connection_type"] = "flows_into"
    edit(m / "connections.yaml", bad)
    errors, _ = v.check_method(m, VERBS, TYPES)
    assert any("is not a record" in e for e in errors) and any("is not one of the five" in e for e in errors)


def test_uncertainty_needs_a_known_status_and_an_effect(tmp_path):
    m = copy_method(tmp_path)
    def bad(doc):
        doc["judgments"][0]["status"] = "probable"
        doc["judgments"][1].pop("downstream_effect")
    edit(m / "uncertainty.yaml", bad)
    errors, _ = v.check_method(m, VERBS, TYPES)
    assert any("status 'probable'" in e for e in errors) and any("no downstream_effect" in e for e in errors)


def test_a_missing_file_fails(tmp_path):
    m = copy_method(tmp_path)
    (m / "uncertainty.yaml").unlink()
    errors, _ = v.check_method(m, VERBS, TYPES)
    assert errors == ["p01: missing uncertainty.yaml"]
