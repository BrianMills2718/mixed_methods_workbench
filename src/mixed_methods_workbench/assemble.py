"""Assemble the DEMO-C1 review packet after checking every cross-method seam."""

from __future__ import annotations

from .models import (
    CompatibleGTInspiredView,
    CompatiblePTView,
    CompatibleQCView,
    ControlledDemoPacket,
    CoreDemoReviewPacket,
    CrossMethodLink,
    DEMO_LIMITS,
    StrictGTInspiredExport,
    StrictPTExport,
    StrictQCExport,
)


def assemble_core_demo_review(
    packet: ControlledDemoPacket,
    qc_export: StrictQCExport,
    pt_export: StrictPTExport,
    gt_export: StrictGTInspiredExport,
    links: list[CrossMethodLink],
) -> CoreDemoReviewPacket:
    """Build one review packet only when native IDs and exact source step-down resolve."""
    packet_id = packet.packet_id
    for artifact_name, artifact_packet_id in (
        ("QC", qc_export.packet_id),
        ("PT", pt_export.packet_id),
        ("GT-inspired", gt_export.packet_id),
    ):
        if artifact_packet_id != packet_id:
            raise ValueError(f"{artifact_name} artifact packet_id does not match demo packet")

    segment_ids = packet.segment_ids()
    _validate_qc_segments(qc_export, segment_ids)
    _validate_pt_segments(pt_export, segment_ids)
    _validate_gt_segments(gt_export, segment_ids)
    _validate_links(qc_export, pt_export, gt_export, links)

    return CoreDemoReviewPacket(
        schema_version=1,
        artifact_status="synthetic_demo_fixture",
        packet=packet,
        qc=CompatibleQCView.model_validate(qc_export.model_dump()),
        pt=CompatiblePTView.model_validate(pt_export.model_dump()),
        gt_inspired=CompatibleGTInspiredView.model_validate(gt_export.model_dump()),
        links=links,
        prose_status="synthetic_non_authoritative_human_review_required",
        claim_limits=sorted(DEMO_LIMITS),
    )


def _validate_qc_segments(export: StrictQCExport, segment_ids: set[str]) -> None:
    """Reject QC denominator or anchors outside the controlled packet."""
    if set(export.corpus_segment_ids) != segment_ids:
        raise ValueError("QC corpus denominator must equal the controlled segment universe")
    cited = {
        segment_id
        for claim in export.claims
        for segment_id in [*claim.supporting_segment_ids, *claim.contrary_segment_ids]
    } | {segment_id for pattern in export.patterns for segment_id in pattern.segment_ids}
    if not cited.issubset(segment_ids):
        raise ValueError("QC object references an unknown demo segment")


def _validate_pt_segments(export: StrictPTExport, segment_ids: set[str]) -> None:
    """Reject PT evidence that cannot step down to the controlled packet."""
    cited = {segment_id for evidence in export.evidence for segment_id in evidence.segment_ids}
    if not cited.issubset(segment_ids):
        raise ValueError("PT evidence references an unknown demo segment")


def _validate_gt_segments(export: StrictGTInspiredExport, segment_ids: set[str]) -> None:
    """Reject GT-inspired categories, comparisons, or memos with broken step-down."""
    cited: set[str] = set()
    for category in export.categories:
        cited.update(category.supporting_segment_ids)
        cited.update(iteration.segment_id for iteration in category.comparison_trace)
    for memo in export.memos:
        cited.update(memo.segment_ids)
    if not cited.issubset(segment_ids):
        raise ValueError("GT-inspired object references an unknown demo segment")


def _validate_links(
    qc_export: StrictQCExport,
    pt_export: StrictPTExport,
    gt_export: StrictGTInspiredExport,
    links: list[CrossMethodLink],
) -> None:
    """Reject duplicate links or references to nonexistent method-native objects."""
    link_ids = [link.link_id for link in links]
    if len(link_ids) != len(set(link_ids)):
        raise ValueError("cross-method link IDs must be unique")
    objects = {
        ("qualitative_coding", "qc_claim"): {claim.claim_id for claim in qc_export.claims},
        ("qualitative_coding", "qc_pattern"): {
            pattern.pattern_id for pattern in qc_export.patterns
        },
        ("process_tracing", "pt_hypothesis"): {
            hypothesis.hypothesis_id for hypothesis in pt_export.hypotheses
        },
        ("process_tracing", "pt_evidence"): {
            evidence.evidence_id for evidence in pt_export.evidence
        },
        ("grounded_theory_inspired", "gt_category"): {
            category.category_id for category in gt_export.categories
        },
        ("grounded_theory_inspired", "gt_memo"): {memo.memo_id for memo in gt_export.memos},
    }
    for link in links:
        for ref in (link.source, link.target):
            if ref.object_id not in objects[(ref.method, ref.object_kind)]:
                raise ValueError(
                    "cross-method link references unknown "
                    f"{ref.method}/{ref.object_kind} object {ref.object_id}"
                )
