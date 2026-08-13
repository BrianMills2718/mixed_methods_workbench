from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_method_decomposition_pilot.py"
PILOT = ROOT / "docs" / "research" / "method_decomposition" / "phase1_pilot"


def _load_validator():
    spec = importlib.util.spec_from_file_location("pilot_validator", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()


def _copy_pilot(tmp_path: Path) -> Path:
    target = tmp_path / "phase1_pilot"
    shutil.copytree(PILOT, target)
    return target


def _rewrite_yaml(path: Path, mutate) -> None:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    mutate(value)
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def test_current_pilot_is_auditable_but_collision_blocked() -> None:
    assert VALIDATOR.validate(PILOT) == []


def test_missing_prohibited_edges_fails(tmp_path: Path) -> None:
    pilot = _copy_pilot(tmp_path)
    graph = pilot / "workflow_edges.yaml"
    _rewrite_yaml(graph, lambda value: value["topologies"][0].pop("prohibited_edges"))
    assert any("prohibited_edges" in error for error in VALIDATOR.validate(pilot))


def test_unclassified_no_overlap_edge_fails(tmp_path: Path) -> None:
    pilot = _copy_pilot(tmp_path)
    gaps = pilot / "structural_gaps.yaml"
    _rewrite_yaml(gaps, lambda value: value["required_edge_gaps"].pop())
    assert any("no-overlap edges" in error for error in VALIDATOR.validate(pilot))


def test_tampered_blind_rerun_fails_digest(tmp_path: Path) -> None:
    pilot = _copy_pilot(tmp_path)
    inventory = pilot / "blind_reruns" / "step_inventory.yaml"
    inventory.write_text(inventory.read_text(encoding="utf-8") + "\n# tampered\n", encoding="utf-8")
    assert any("digest mismatch" in error for error in VALIDATOR.validate(pilot))


def test_missing_reconciliation_row_fails(tmp_path: Path) -> None:
    pilot = _copy_pilot(tmp_path)
    reconciliation = pilot / "blind_reruns" / "reconciliation.yaml"
    _rewrite_yaml(reconciliation, lambda value: value["mappings"]["systematic_review"].pop())
    errors = VALIDATOR.validate(pilot)
    assert any("digest mismatch" in error for error in errors)
    assert any("does not cover rerun inventory exactly" in error for error in errors)


def test_promoted_status_with_known_losses_fails(tmp_path: Path) -> None:
    pilot = _copy_pilot(tmp_path)
    ledger = pilot / "step_ledger.yaml"
    _rewrite_yaml(ledger, lambda value: value.update(status="collision_ready"))
    assert any("must remain unresolved" in error for error in VALIDATOR.validate(pilot))
