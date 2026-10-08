import copy
import json
import subprocess
from pathlib import Path

from scripts.validate_phase3_work_graph import validate_graph

GRAPH = Path("docs/research/method_decomposition/phase3/4_phase3_portfolio_decomposition_work_graph.json")


def load_graph() -> dict:
    return json.loads(GRAPH.read_text(encoding="utf-8"))


def unit(document: dict, unit_id: str) -> dict:
    return next(item for item in document["units"] if item["id"] == unit_id)


def pre_acceptance_graph() -> dict:
    """The canonical graph with accepted lanes returned to ready, for synthetic receipt-history fixtures."""
    document = load_graph()
    for item in document["units"]:
        if item["id"].startswith("P3-RESEARCH") and item["status"] == "accepted":
            item["status"], item["claimability"] = "ready", "ready_for_execution"
            item["inputs"] = [i for i in item["inputs"] if i["kind"] != "CompletionReceipt"]
    return document


def head() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def commit_all(repo: Path, message: str) -> str:
    git(repo, "add", ".")
    git(repo, "commit", "--allow-empty", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def receipt_history(tmp_path: Path, *, mutate: str | None = None) -> tuple[Path, str, str, str]:
    repo = tmp_path / "repo"
    repo.mkdir(parents=True)
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Test")
    git(repo, "config", "user.email", "test@example.invalid")
    methods = ["p01", "p02", "p03", "p04", "p14"]
    for method in methods:
        method_path = repo / "docs/research/method_decomposition/phase3/methods" / method
        method_path.mkdir(parents=True)
        for filename in ("frame.yaml", "sources.md", "method_records.yaml", "connections.yaml", "uncertainty.yaml"):
            if mutate != "missing_artifact" or not (method == "p14" and filename == "frame.yaml"):
                (method_path / filename).write_text("evidence\n", encoding="utf-8")
    evidence = commit_all(repo, "evidence")
    receipt_path = repo / "docs/research/method_decomposition/phase3/lane_receipts/P3-RESEARCH-A.yaml"
    if mutate != "missing_receipt":
        receipt_path.parent.mkdir(parents=True)
        receipt = {
            "unit_id": "WRONG" if mutate == "wrong_content" else "P3-RESEARCH-A",
            "evidence_commit": evidence,
            "method_paths": [f"docs/research/method_decomposition/phase3/methods/{method}" for method in methods],
            "checks": ["focused"],
            "reviewer": "independent-reviewer",
            "disposition": "accepted",
        }
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    receipt_commit = commit_all(repo, "receipt") if mutate != "missing_receipt" else commit_all(repo, "no receipt")
    (repo / "transition.txt").write_text("later\n", encoding="utf-8")
    transition = commit_all(repo, "transition")
    return repo, evidence, receipt_commit, transition


def accepted_lane(document: dict, evidence: str, receipt: str) -> None:
    lane = unit(document, "P3-RESEARCH-A")
    lane["status"] = "accepted"
    lane["inputs"].append({
        "kind": "CompletionReceipt",
        "id": "P3-RESEARCH-A",
        "revision": f"docs/research/method_decomposition/phase3/lane_receipts/P3-RESEARCH-A.yaml@evidence={evidence};receipt={receipt}",
    })


def test_canonical_phase3_graph_passes() -> None:
    document = load_graph()
    assert validate_graph(document, repo=Path("."), transition_revision=head()) == []
    assert {item["spec_revision"] for item in document["units"]} == {"plan-4-phase3-work-graph-v4"}
    assert all(
        sum(
            item.get("kind") == "CoordinationPlan"
            and item.get("id") == "Plan #4"
            for item in work_unit["inputs"]
        ) == 1
        for work_unit in document["units"]
    )


def test_canonical_phase3_graph_preserves_handoffs_without_acceptance() -> None:
    document = load_graph()
    expected = {
        "P3-RESEARCH-A": (
            "ready",
            "ready_for_execution",
            "2f66438517e651ed05ebec39663734d115184dd3",
        ),
        "P3-RESEARCH-B": (
            "ready",
            "ready_for_execution",
            "915c903c67876fb5776744517f63ed9cd8682517",
        ),
        "P3-RESEARCH-C": (
            "ready",
            "ready_for_execution",
            "ef34684b1fc56433da5c9d08c4d0f474f6c596e5",
        ),
    }
    accepted = {"P3-RESEARCH-A", "P3-RESEARCH-B"}          # 2026-10-08 receipts; C remains in rework
    for unit_id, (status, claimability, revision) in expected.items():
        if unit_id in accepted:
            status, claimability = "accepted", "not_applicable"
        lane = unit(document, unit_id)
        submitted = [item for item in lane["inputs"] if item["kind"] == "SubmittedEvidence"]
        assert lane["status"] == status
        assert lane["claimability"] == claimability
        assert lane["readiness"]["status"] == "ready"         # 2026-10-08 control review requested corrections; rework is open to the lane
        reviews = [item for item in lane["inputs"] if item["kind"] == "ControlReview"]
        assert len(reviews) == 1 and Path(reviews[0]["revision"].split(";")[0]).is_file()
        assert len(submitted) == 1
        assert revision in submitted[0]["revision"]
        receipts = [item for item in lane["inputs"] if item["kind"] == "CompletionReceipt"]
        assert len(receipts) == (1 if unit_id in accepted else 0)

    control = unit(document, "P3-CONTROL")
    # The Phase 3 pause was lifted on 2026-10-08 (roadmap row 5a); only the control unit may now advance lanes.
    assert (control["claimability"], control["status"], control["readiness"]["status"]) == (
        "ready_for_execution",
        "ready",
        "ready",
    )
    assert not any("pause" in guard.lower() for item in document["units"] for guard in item["readiness"]["failed_guards"])


def test_rejects_missing_control_unit() -> None:
    document = pre_acceptance_graph()
    document["units"] = [item for item in document["units"] if item["id"] != "P3-CONTROL"]
    assert any("units must be exactly" in error for error in validate_graph(document))


def test_rejects_unready_control() -> None:
    document = pre_acceptance_graph()
    unit(document, "P3-CONTROL")["claimability"] = "blocked_dependencies"
    assert any("must be either" in error for error in validate_graph(document))


def test_rejects_paused_control_without_product_guard() -> None:
    document = pre_acceptance_graph()
    control = unit(document, "P3-CONTROL")                       # a future pause must still name its reason
    control["claimability"], control["status"] = "not_applicable", "blocked"
    control["readiness"] = {"status": "blocked", "required_approval_types": [], "approvals": [], "failed_guards": ["generic pause"]}
    assert any("product-integration guard" in error for error in validate_graph(document))


def test_rejects_noncontrol_graph_owner() -> None:
    document = pre_acceptance_graph()
    unit(document, "P3-INTEGRATE")["conflict_surfaces"].append(
        {"kind": "repository_path", "target": str(GRAPH), "repository": "mixed_methods_workbench", "access": "exclusive"}
    )
    assert any("may not own graph" in error for error in validate_graph(document))


def test_rejects_duplicate_or_missing_method() -> None:
    document = pre_acceptance_graph()
    source = copy.deepcopy(unit(document, "P3-RESEARCH-A")["conflict_surfaces"][0])
    unit(document, "P3-RESEARCH-B")["conflict_surfaces"].append(source)
    assert any("exactly once" in error for error in validate_graph(document))


def test_rejects_mutated_submitted_handoff_revision() -> None:
    document = pre_acceptance_graph()
    lane = unit(document, "P3-RESEARCH-C")
    next(item for item in lane["inputs"] if item["kind"] == "SubmittedEvidence")["revision"] = (
        "git:origin/phase3-research-c@" + "0" * 40 + ";archived-handoff;not-accepted"
    )
    assert any("exact archived submitted evidence" in error for error in validate_graph(document))


def test_rejects_completion_receipt_before_acceptance() -> None:
    document = pre_acceptance_graph()
    lane = unit(document, "P3-RESEARCH-A")
    lane["inputs"].append(
        {
            "kind": "CompletionReceipt",
            "id": "P3-RESEARCH-A",
            "revision": "premature",
        }
    )
    assert any("before accepted status" in error for error in validate_graph(document))


def test_rejects_missing_hard_dependency() -> None:
    document = pre_acceptance_graph()
    unit(document, "P3-INTEGRATE")["dependencies"].pop()
    assert any("hard gates" in error for error in validate_graph(document))


def test_rejects_writable_pt_evidence() -> None:
    document = pre_acceptance_graph()
    lane = unit(document, "P3-RESEARCH-A")
    next(surface for surface in lane["conflict_surfaces"] if "pt-topology" in surface.get("coordination_key", ""))["access"] = "exclusive"
    assert any("read-only" in error for error in validate_graph(document))


def test_rejects_same_evidence_and_receipt_commit() -> None:
    document = pre_acceptance_graph()
    lane = unit(document, "P3-RESEARCH-A")
    lane["status"] = "accepted"
    sha = "a" * 40
    lane["inputs"].append({
        "kind": "CompletionReceipt",
        "id": "P3-RESEARCH-A",
        "revision": f"docs/research/method_decomposition/phase3/lane_receipts/P3-RESEARCH-A.yaml@evidence={sha};receipt={sha}",
    })
    assert any("repository evidence context" in error for error in validate_graph(document))


def test_rejects_fabricated_distinct_commits_without_context() -> None:
    document = pre_acceptance_graph()
    accepted_lane(document, "a" * 40, "b" * 40)
    assert any("repository evidence context" in error for error in validate_graph(document))


def test_accepts_real_verified_receipt_history(tmp_path: Path) -> None:
    repo, evidence, receipt, transition = receipt_history(tmp_path)
    document = pre_acceptance_graph()
    accepted_lane(document, evidence, receipt)
    assert validate_graph(document, repo=repo, transition_revision=transition) == []


def test_rejects_nonexistent_receipt_commit(tmp_path: Path) -> None:
    repo, evidence, _, transition = receipt_history(tmp_path)
    document = pre_acceptance_graph()
    accepted_lane(document, evidence, "f" * 40)
    assert any("does not exist" in error for error in validate_graph(document, repo=repo, transition_revision=transition))


def test_rejects_missing_or_wrong_receipt_content(tmp_path: Path) -> None:
    for mutation, expected in (("missing_receipt", "path is absent"), ("wrong_content", "unit binding")):
        repo, evidence, receipt, transition = receipt_history(tmp_path / mutation, mutate=mutation)
        document = pre_acceptance_graph()
        accepted_lane(document, evidence, receipt)
        assert any(expected in error for error in validate_graph(document, repo=repo, transition_revision=transition))


def test_rejects_missing_evidence_artifact(tmp_path: Path) -> None:
    repo, evidence, receipt, transition = receipt_history(tmp_path, mutate="missing_artifact")
    document = pre_acceptance_graph()
    accepted_lane(document, evidence, receipt)
    assert any("evidence commit lacks" in error for error in validate_graph(document, repo=repo, transition_revision=transition))


def test_rejects_transition_not_later_than_receipt(tmp_path: Path) -> None:
    repo, evidence, receipt, _ = receipt_history(tmp_path)
    document = pre_acceptance_graph()
    accepted_lane(document, evidence, receipt)
    assert any("transition must be later" in error for error in validate_graph(document, repo=repo, transition_revision=receipt))


def test_rejects_receipt_not_descended_from_evidence(tmp_path: Path) -> None:
    repo, evidence, _, _ = receipt_history(tmp_path)
    git(repo, "checkout", "--orphan", "unrelated")
    git(repo, "rm", "-rf", ".")
    receipt_path = repo / "docs/research/method_decomposition/phase3/lane_receipts/P3-RESEARCH-A.yaml"
    receipt_path.parent.mkdir(parents=True)
    methods = ["p01", "p02", "p03", "p04", "p14"]
    receipt_path.write_text(json.dumps({
        "unit_id": "P3-RESEARCH-A",
        "evidence_commit": evidence,
        "method_paths": [f"docs/research/method_decomposition/phase3/methods/{method}" for method in methods],
        "checks": ["focused"],
        "reviewer": "independent-reviewer",
        "disposition": "accepted",
    }), encoding="utf-8")
    receipt = commit_all(repo, "unrelated receipt")
    (repo / "transition.txt").write_text("later\n", encoding="utf-8")
    transition = commit_all(repo, "transition")
    document = pre_acceptance_graph()
    accepted_lane(document, evidence, receipt)
    assert any("must descend from evidence" in error for error in validate_graph(document, repo=repo, transition_revision=transition))


def test_rejects_ready_integration_before_acceptance() -> None:
    document = pre_acceptance_graph()
    integration = unit(document, "P3-INTEGRATE")
    integration["claimability"] = "ready_for_execution"
    integration["readiness"] = {"status": "ready", "required_approval_types": [], "approvals": [], "failed_guards": []}
    integration["status"] = "ready"
    assert any("cannot be ready before" in error for error in validate_graph(document))
