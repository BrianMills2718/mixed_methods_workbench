import copy
import json
from pathlib import Path

from scripts.validate_phase3_work_graph import validate_graph

GRAPH = Path("docs/research/method_decomposition/phase3/work_graph.json")


def load_graph() -> dict:
    return json.loads(GRAPH.read_text(encoding="utf-8"))


def unit(document: dict, unit_id: str) -> dict:
    return next(item for item in document["units"] if item["id"] == unit_id)


def test_canonical_phase3_graph_passes() -> None:
    assert validate_graph(load_graph()) == []


def test_rejects_missing_control_unit() -> None:
    document = load_graph()
    document["units"] = [item for item in document["units"] if item["id"] != "P3-CONTROL"]
    assert any("units must be exactly" in error for error in validate_graph(document))


def test_rejects_unready_control() -> None:
    document = load_graph()
    unit(document, "P3-CONTROL")["claimability"] = "blocked_dependencies"
    assert any("must be ready_for_execution" in error for error in validate_graph(document))


def test_rejects_noncontrol_graph_owner() -> None:
    document = load_graph()
    unit(document, "P3-INTEGRATE")["conflict_surfaces"].append(
        {"kind": "repository_path", "target": str(GRAPH), "repository": "mixed_methods_workbench", "access": "exclusive"}
    )
    assert any("may not own graph" in error for error in validate_graph(document))


def test_rejects_duplicate_or_missing_method() -> None:
    document = load_graph()
    source = copy.deepcopy(unit(document, "P3-RESEARCH-A")["conflict_surfaces"][0])
    unit(document, "P3-RESEARCH-B")["conflict_surfaces"].append(source)
    assert any("exactly once" in error for error in validate_graph(document))


def test_rejects_missing_hard_dependency() -> None:
    document = load_graph()
    unit(document, "P3-INTEGRATE")["dependencies"].pop()
    assert any("hard gates" in error for error in validate_graph(document))


def test_rejects_writable_pt_evidence() -> None:
    document = load_graph()
    lane = unit(document, "P3-RESEARCH-A")
    next(surface for surface in lane["conflict_surfaces"] if "pt-topology" in surface.get("coordination_key", ""))["access"] = "exclusive"
    assert any("read-only" in error for error in validate_graph(document))


def test_rejects_same_evidence_and_receipt_commit() -> None:
    document = load_graph()
    lane = unit(document, "P3-RESEARCH-A")
    lane["status"] = "accepted"
    sha = "a" * 40
    lane["inputs"].append({
        "kind": "CompletionReceipt",
        "id": "P3-RESEARCH-A",
        "revision": f"docs/research/method_decomposition/phase3/lane_receipts/P3-RESEARCH-A.yaml@evidence={sha};receipt={sha}",
    })
    assert any("distinct evidence and receipt" in error for error in validate_graph(document))


def test_rejects_ready_integration_before_acceptance() -> None:
    document = load_graph()
    integration = unit(document, "P3-INTEGRATE")
    integration["claimability"] = "ready_for_execution"
    integration["readiness"] = {"status": "ready", "required_approval_types": [], "approvals": [], "failed_guards": []}
    integration["status"] = "ready"
    assert any("cannot be ready before" in error for error in validate_graph(document))
