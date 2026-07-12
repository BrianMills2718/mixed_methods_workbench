"""Invariant-specific negative controls for every DEMO-C1 hard gate."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest
from pydantic import ValidationError

from mixed_methods_workbench.assemble import assemble_core_demo_review
from mixed_methods_workbench.io import FIXTURE_DIR, load_demo_inputs, validate_demo_manifest
from mixed_methods_workbench.models import (
    ControlledDemoPacket,
    CrossMethodLink,
    DemoFixtureManifest,
    StrictGTInspiredExport,
    StrictPTExport,
    StrictQCExport,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def _json(name: str) -> dict[str, object]:
    """Load one positive fixture as a mutable negative-control seed."""
    value = json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_wrong_segment_hash_reaches_hash_invariant() -> None:
    """Reject a source passage whose declared hash does not match exact bytes."""
    raw = _json("packet.json")
    raw["documents"][0]["segments"][0]["text_sha256"] = "0" * 64  # type: ignore[index]
    with pytest.raises(ValidationError, match="text_sha256 must match"):
        ControlledDemoPacket.model_validate(raw)


def test_bad_segment_offset_reaches_span_invariant() -> None:
    """Reject a source passage whose offsets do not span its displayed text."""
    raw = _json("packet.json")
    raw["documents"][0]["segments"][0]["end_char"] = 2  # type: ignore[index]
    with pytest.raises(ValidationError, match="offsets must span"):
        ControlledDemoPacket.model_validate(raw)


def test_shifted_same_length_offsets_must_resolve_in_document() -> None:
    """Reject same-length shifted offsets rather than validating span length by proxy."""
    raw = _json("packet.json")
    segment = raw["documents"][0]["segments"][0]  # type: ignore[index]
    segment["start_char"] = 7
    segment["end_char"] = 68
    with pytest.raises(ValidationError, match="resolve to exact text in document"):
        ControlledDemoPacket.model_validate(raw)


def test_qc_rejects_process_tracing_comparative_support() -> None:
    """Reject PT inference fields added to the strict QC producer shape."""
    raw = _json("qc.json")
    raw["comparative_support"] = {"ranked_hypothesis_ids": ["pt-h1", "pt-h2"]}
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        StrictQCExport.model_validate(raw)


def test_qc_unknown_anchor_reaches_step_down_invariant() -> None:
    """Reject a QC claim that cannot step down to the controlled packet."""
    packet, qc_export, pt_export, gt_export, links = load_demo_inputs()
    broken = qc_export.model_copy(deep=True)
    broken.claims[0].supporting_segment_ids = ["unknown-segment"]
    with pytest.raises(ValueError, match="QC object references an unknown"):
        assemble_core_demo_review(packet, broken, pt_export, gt_export, links)


def test_pt_requires_exactly_one_residual() -> None:
    """Reject a PT rival set that silently omits its residual alternative."""
    raw = _json("pt.json")
    hypotheses = cast(list[dict[str, object]], raw["hypotheses"])
    for hypothesis in hypotheses:
        hypothesis["is_residual"] = False
    with pytest.raises(ValidationError, match="exactly one residual"):
        StrictPTExport.model_validate(raw)


def test_pt_rejects_duplicate_complete_ranking() -> None:
    """Reject a ranking whose set looks complete but repeats a rival."""
    raw = _json("pt.json")
    raw["comparative_support"]["ranked_hypothesis_ids"] = [  # type: ignore[index]
        "pt-h2",
        "pt-h1",
        "pt-h3",
        "pt-h3",
    ]
    with pytest.raises(ValidationError, match="every rival exactly once"):
        StrictPTExport.model_validate(raw)


def test_pt_rejects_duplicate_hypothesis_references_in_evidence() -> None:
    """Reject repeated rival references that satisfy minimum length only by duplication."""
    raw = _json("pt.json")
    raw["evidence"][0]["hypothesis_ids"] = ["pt-h1", "pt-h1"]  # type: ignore[index]
    with pytest.raises(ValidationError, match="hypothesis references must be unique"):
        StrictPTExport.model_validate(raw)


def test_gt_rejects_saturated_field() -> None:
    """Reject an unauthorized boolean that presents a diagnostic as saturation proof."""
    raw = _json("gt_inspired.json")
    raw["saturated"] = True
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        StrictGTInspiredExport.model_validate(raw)


def test_gt_requires_no_full_gt_and_no_saturation_limits() -> None:
    """Reject GT-I output whose caveats omit the central methodological limits."""
    raw = _json("gt_inspired.json")
    raw["methodological_limits"] = ["Synthetic only.", "Requires later review."]
    with pytest.raises(ValidationError, match="methodological_limits must exactly match"):
        StrictGTInspiredExport.model_validate(raw)


def test_gt_unknown_comparison_segment_reaches_step_down_invariant() -> None:
    """Reject comparison history that cannot step down to an exact source passage."""
    packet, qc_export, pt_export, gt_export, links = load_demo_inputs()
    broken = gt_export.model_copy(deep=True)
    broken.categories[0].comparison_trace[0].segment_id = "unknown-segment"
    with pytest.raises(ValueError, match="GT-inspired object references an unknown"):
        assemble_core_demo_review(packet, qc_export, pt_export, broken, links)


def test_gt_rejects_duplicate_comparison_iteration() -> None:
    """Reject repeated iteration numbers that fake an ordered development trace."""
    raw = _json("gt_inspired.json")
    raw["categories"][0]["comparison_trace"][1]["iteration"] = 1  # type: ignore[index]
    with pytest.raises(ValidationError, match="unique, ordered, and contiguous"):
        StrictGTInspiredExport.model_validate(raw)


def test_link_rejects_evidentiary_support_relationship() -> None:
    """Reject a link that turns navigation into cross-method evidentiary support."""
    raw = json.loads((FIXTURE_DIR / "links.json").read_text(encoding="utf-8"))[0]
    raw["relationship"] = "supports"
    with pytest.raises(ValidationError, match="Input should be"):
        CrossMethodLink.model_validate(raw)


def test_link_unknown_target_reaches_native_object_invariant() -> None:
    """Reject a neutral link that points to a nonexistent native method object."""
    packet, qc_export, pt_export, gt_export, links = load_demo_inputs()
    broken = copy.deepcopy(links)
    broken[0].target.object_id = "missing-pt-object"
    with pytest.raises(ValueError, match="unknown process_tracing/pt_hypothesis object"):
        assemble_core_demo_review(packet, qc_export, pt_export, gt_export, broken)


def test_link_rejects_same_method_endpoints() -> None:
    """Reject a valid native reference pair that is not actually cross-method."""
    raw = json.loads((FIXTURE_DIR / "links.json").read_text(encoding="utf-8"))[0]
    raw["target"] = {
        "method": "qualitative_coding",
        "object_kind": "qc_pattern",
        "object_id": "qc-pattern-02",
    }
    with pytest.raises(ValidationError, match="different methods"):
        CrossMethodLink.model_validate(raw)


def test_unsupported_major_version_fails_loudly() -> None:
    """Reject a producer major version the v1 compatible consumer cannot interpret."""
    raw = _json("qc.json")
    raw["schema_version"] = 2
    with pytest.raises(ValidationError, match="Input should be 1"):
        StrictQCExport.model_validate(raw)


def test_foreign_packet_binding_reaches_binding_invariant() -> None:
    """Reject a valid-shaped method artifact bound to another source universe."""
    packet, qc_export, pt_export, gt_export, links = load_demo_inputs()
    broken = pt_export.model_copy(update={"packet_id": "foreign-packet"})
    with pytest.raises(ValueError, match="PT artifact packet_id does not match"):
        assemble_core_demo_review(packet, qc_export, broken, gt_export, links)


def test_manifest_stale_hash_reaches_named_file_invariant(tmp_path: Path) -> None:
    """Reject a manifest whose recorded bytes no longer match one payload."""
    fixture_dir = tmp_path / "demo_c1"
    shutil.copytree(FIXTURE_DIR, fixture_dir)
    packet_path = fixture_dir / "packet.json"
    packet_path.write_text(packet_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="fixture hash mismatch: packet.json"):
        validate_demo_manifest(fixture_dir)


def test_manifest_unlisted_payload_reaches_inventory_invariant(tmp_path: Path) -> None:
    """Reject an extra JSON payload that is absent from the governed inventory."""
    fixture_dir = tmp_path / "demo_c1"
    shutil.copytree(FIXTURE_DIR, fixture_dir)
    (fixture_dir / "rogue.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unlisted=\\['rogue.json'\\]"):
        validate_demo_manifest(fixture_dir)


def test_manifest_nested_uppercase_payload_reaches_inventory_invariant(tmp_path: Path) -> None:
    """Reject nested case-variant JSON so exhaustive inventory cannot be bypassed."""
    fixture_dir = tmp_path / "demo_c1"
    shutil.copytree(FIXTURE_DIR, fixture_dir)
    nested = fixture_dir / "nested"
    nested.mkdir()
    (nested / "rogue.JSON").write_text("{}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="nested/rogue.JSON"):
        validate_demo_manifest(fixture_dir)


def test_manifest_rejects_fixture_symlink(tmp_path: Path) -> None:
    """Reject symlinked payloads whose bytes can change outside the inventory boundary."""
    fixture_dir = tmp_path / "demo_c1"
    shutil.copytree(FIXTURE_DIR, fixture_dir)
    (fixture_dir / "linked.json").symlink_to(fixture_dir / "packet.json")
    with pytest.raises(ValueError, match="unsupported symlinks"):
        validate_demo_manifest(fixture_dir)


def test_packet_rejects_claim_limit_escalation() -> None:
    """Reject an extra claim even when all required synthetic caveats remain."""
    raw = _json("packet.json")
    cast(list[str], raw["claim_limits"]).append("Validated empirical evidence.")
    with pytest.raises(ValidationError, match="exactly match its reviewed claim boundary"):
        ControlledDemoPacket.model_validate(raw)


def test_qc_rejects_claim_limit_escalation() -> None:
    """Reject a QC method-validity claim appended to otherwise correct limits."""
    raw = _json("qc.json")
    cast(list[str], raw["claim_limits"]).append("Validated qualitative method output.")
    with pytest.raises(ValidationError, match="QC claim_limits must exactly match"):
        StrictQCExport.model_validate(raw)


def test_manifest_rejects_claim_limit_escalation() -> None:
    """Reject provenance metadata that contradicts the fixture's C-grade boundary."""
    raw = _json("manifest.json")
    cast(list[str], raw["claim_limits"]).append("Validated empirical evidence.")
    with pytest.raises(ValidationError, match="manifest claim_limits must exactly match"):
        DemoFixtureManifest.model_validate(raw)


def test_cli_invalid_fixture_exits_nonzero_at_intended_invariant(tmp_path: Path) -> None:
    """Exercise the real CLI failure path rather than treating unit validation as a proxy."""
    fixture_dir = tmp_path / "demo_c1"
    shutil.copytree(FIXTURE_DIR, fixture_dir)
    pt_path = fixture_dir / "pt.json"
    raw_pt = json.loads(pt_path.read_text(encoding="utf-8"))
    for hypothesis in raw_pt["hypotheses"]:
        hypothesis["is_residual"] = False
    pt_path.write_text(json.dumps(raw_pt, indent=2) + "\n", encoding="utf-8")
    manifest_path = fixture_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pt_entry = next(entry for entry in manifest["files"] if entry["path"] == "pt.json")
    pt_entry["sha256"] = hashlib.sha256(pt_path.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mixed_methods_workbench.cli",
            "validate",
            "--fixture-dir",
            str(fixture_dir),
        ],
        cwd=REPO_ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "exactly one residual hypothesis" in result.stderr
