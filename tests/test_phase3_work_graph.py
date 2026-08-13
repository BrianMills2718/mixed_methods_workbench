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


def test_rejects_duplicate_method_ownership() -> None:
    document = copy.deepcopy(load_graph())
    source = unit(document, "P3-RESEARCH-A")["conflict_surfaces"][0]
    unit(document, "P3-RESEARCH-B")["conflict_surfaces"].append(source)
    assert any("p01 through p14 exactly once" in error for error in validate_graph(document))


def test_rejects_missing_method_ownership() -> None:
    document = copy.deepcopy(load_graph())
    lane = unit(document, "P3-RESEARCH-C")
    lane["conflict_surfaces"] = [
        surface for surface in lane["conflict_surfaces"]
        if not surface["target"].endswith("/p13")
    ]
    assert any("p01 through p14 exactly once" in error for error in validate_graph(document))


def test_rejects_missing_hard_dependency() -> None:
    document = copy.deepcopy(load_graph())
    unit(document, "P3-INTEGRATE")["dependencies"].pop()
    assert any("hard gates" in error for error in validate_graph(document))


def test_rejects_writable_pt_product_evidence() -> None:
    document = copy.deepcopy(load_graph())
    lane = unit(document, "P3-RESEARCH-A")
    next(
        surface for surface in lane["conflict_surfaces"]
        if "pt-topology" in surface.get("coordination_key", "")
    )["access"] = "exclusive"
    assert any("read-only" in error for error in validate_graph(document))


def test_rejects_pt_evidence_as_method_authority() -> None:
    document = copy.deepcopy(load_graph())
    lane = unit(document, "P3-RESEARCH-A")
    next(item for item in lane["inputs"] if item["id"] == "process-tracing-topology-prototype")["revision"] = "merged@1fd01bc"
    assert any("non-method-authority" in error for error in validate_graph(document))


def test_rejects_ready_integration_before_accepted_receipts() -> None:
    document = copy.deepcopy(load_graph())
    integration = unit(document, "P3-INTEGRATE")
    integration["claimability"] = "ready_for_execution"
    integration["readiness"]["status"] = "ready"
    integration["readiness"]["failed_guards"] = []
    integration["status"] = "ready"
    errors = validate_graph(document)
    assert any("cannot be ready before" in error for error in errors)
    assert any("completion evidence" in error for error in errors)


def test_rejects_accepted_lane_without_exact_receipt() -> None:
    document = copy.deepcopy(load_graph())
    lane = unit(document, "P3-RESEARCH-A")
    lane["status"] = "accepted"
    assert any("exact CompletionReceipt" in error for error in validate_graph(document))
