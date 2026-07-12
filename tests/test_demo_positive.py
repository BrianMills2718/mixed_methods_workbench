"""Positive controls for the complete DEMO-C1 synthetic review journey."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from mixed_methods_workbench.assemble import assemble_core_demo_review
from mixed_methods_workbench.io import load_demo_inputs, validate_demo_manifest, write_review_json
from mixed_methods_workbench.models import CompatibleQCView


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_controlled_packet_has_exact_three_segment_universe() -> None:
    """Prove the approved Harbor packet has three hash-validated source passages."""
    packet, _, _, _, _ = load_demo_inputs()
    assert packet.segment_ids() == {"seg-memo-01", "seg-log-01", "seg-interview-01"}


def test_manifest_exhaustively_hashes_five_payloads() -> None:
    """Prove the synthetic origin, exact bytes, and inventory before parsing method data."""
    manifest = validate_demo_manifest()
    assert len(manifest.files) == 5
    assert {entry.origin_kind for entry in manifest.files} == {"workbench_synthetic"}


def test_qc_lane_is_qualitative_and_source_traceable() -> None:
    """Prove the QC fixture preserves denominator, contrary evidence, and review state."""
    packet, qc_export, _, _, _ = load_demo_inputs()
    assert set(qc_export.corpus_segment_ids) == packet.segment_ids()
    assert qc_export.claims[0].contrary_segment_ids == ["seg-log-01"]
    assert qc_export.claims[0].review_status == "needs_human_review"


def test_pt_lane_preserves_rivals_residual_and_comparative_support() -> None:
    """Prove PT keeps a residual rival and method-scoped ordinal ranking."""
    _, _, pt_export, _, _ = load_demo_inputs()
    assert len(pt_export.hypotheses) == 3
    assert sum(hypothesis.is_residual for hypothesis in pt_export.hypotheses) == 1
    assert pt_export.comparative_support.ranked_hypothesis_ids[0] == "pt-h2"
    assert pt_export.comparative_support.sensitivity == "high"


def test_gt_lane_preserves_comparison_development_and_limits() -> None:
    """Prove GT-I exposes category development while explicitly denying saturation proof."""
    _, _, _, gt_export, _ = load_demo_inputs()
    category = gt_export.categories[0]
    assert [item.action for item in category.comparison_trace] == ["created", "revised", "narrowed"]
    assert category.adequacy_status == "developing"
    assert (
        "Category adequacy diagnostics are not saturation proof." in gt_export.methodological_limits
    )


def test_review_assembly_preserves_three_lanes_links_and_step_down() -> None:
    """Prove one payload contains distinct lanes and four neutral cross-method links."""
    packet, qc_export, pt_export, gt_export, links = load_demo_inputs()
    review = assemble_core_demo_review(packet, qc_export, pt_export, gt_export, links)
    assert review.qc.method == "qualitative_coding"
    assert review.pt.method == "process_tracing"
    assert review.gt_inspired.method == "grounded_theory_inspired"
    assert {link.relationship for link in review.links} == {
        "addresses",
        "challenges",
        "contextualizes",
        "unresolved",
    }
    assert review.packet.segment_ids() == packet.segment_ids()
    serialized = review.model_dump_json()
    assert "confidence_score" not in serialized
    assert "generic_confidence" not in serialized


def test_compatible_consumer_ignores_future_extra_field() -> None:
    """Prove consumer compatibility does not weaken required semantic fields."""
    _, qc_export, _, _, _ = load_demo_inputs()
    raw = qc_export.model_dump()
    raw["future_compatible_metadata"] = {"note": "ignored by v1 consumer"}
    view = CompatibleQCView.model_validate(raw)
    assert view.claims[0].claim_id == "qc-claim-07"


def test_open_prose_is_explicitly_non_authoritative() -> None:
    """Prove open annotations cannot silently become validated method conclusions."""
    packet, qc_export, pt_export, gt_export, links = load_demo_inputs()
    qc_export.claims[0].text = "Evidence better supports H2 than H1."
    pt_export.comparative_support.verdict = "H2 is almost certainly true."
    gt_export.memos[0].text = "Sampling was sufficient and no new categories emerged."
    review = assemble_core_demo_review(packet, qc_export, pt_export, gt_export, links)
    expected = "synthetic_non_authoritative_human_review_required"
    assert review.prose_status == expected
    assert review.qc.prose_status == expected
    assert review.pt.prose_status == expected
    assert review.gt_inspired.prose_status == expected
    assert {link.reviewer_meaning_status for link in review.links} == {expected}


def test_review_writer_requires_explicit_force_to_overwrite(tmp_path: Path) -> None:
    """Prove derived evidence is not silently replaced by repeated agent commands."""
    output = tmp_path / "review.json"
    write_review_json(output, '{"version": 1}')
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        write_review_json(output, '{"version": 2}')
    write_review_json(output, '{"version": 2}', force=True)
    assert json.loads(output.read_text(encoding="utf-8")) == {"version": 2}


def test_review_writer_refuses_symlink_even_with_force(tmp_path: Path) -> None:
    """Prove explicit overwrite cannot redirect derived output through a symlink."""
    target = tmp_path / "target.json"
    target.write_text('{"protected": true}\n', encoding="utf-8")
    output = tmp_path / "review.json"
    output.symlink_to(target)
    with pytest.raises(FileExistsError, match="refusing to write through"):
        write_review_json(output, '{"protected": false}', force=True)
    assert json.loads(target.read_text(encoding="utf-8")) == {"protected": True}


def test_cli_validate_positive_control_uses_real_agent_surface() -> None:
    """Prove the documented CLI surface runs the complete positive journey."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT / "src")
    result = subprocess.run(
        [sys.executable, "-m", "mixed_methods_workbench.cli", "validate"],
        cwd=REPO_ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout == "DEMO-C1 fixtures and review assembly passed.\n"
