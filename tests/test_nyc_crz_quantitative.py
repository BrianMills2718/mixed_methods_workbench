"""Focused controls for the NYC predicted-versus-observed arithmetic audit."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

import pytest

import mixed_methods_workbench.nyc_crz_quantitative as quant
from mixed_methods_workbench.nyc_crz_quantitative import (
    EXPECTED_DIGESTS,
    NycCrzQuantitativeAudit,
    NycCrzQuantitativeError,
    QuantitativeClaimBoundary,
    load_nyc_crz_quantitative_audit,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_query_receipt_exposes_exact_input_version_shape_and_output() -> None:
    audit = load_nyc_crz_quantitative_audit()
    receipt = audit.query_receipt

    assert receipt.packet_id == "NYC-CRZ-MVP-v1"
    assert receipt.dataset_id == "t6yz-b64h"
    assert receipt.retrieved_at == "2026-08-13T19:40:23Z"
    assert receipt.source_last_modified == "2026-08-13T18:29:49Z"
    assert receipt.row_count == 25_992
    assert receipt.column_count == 5
    assert receipt.missing_measure_rows == 0
    assert receipt.coverage_start == "2025-01-05"
    assert receipt.coverage_end == "2025-12-31"
    assert receipt.observed_days == 361
    assert receipt.input_sha256 == EXPECTED_DIGESTS[
        "t6yz_first_year_daily_by_group_class.csv"
    ]
    assert receipt.output_sha256 == (
        "5446604efb583a19e6bee417c1ffadc319eec08f13da3d8c1f662c2d18142189"
    )
    assert receipt.query.limit == 50_000


def test_monthly_aggregates_recompute_from_frozen_rows() -> None:
    audit = load_nyc_crz_quantitative_audit()
    months = {item.month: item for item in audit.monthly_observations}

    assert len(months) == 12
    assert months["2025-01"].observed_days == 27
    assert months["2025-01"].combined_entry_events == 14_402_715
    assert months["2025-01"].mean_daily_entry_events_rounded == 533_434
    assert months["2025-08"].combined_entry_events == 17_149_762
    assert months["2025-12"].mean_daily_entry_events_rounded == 538_033
    assert sum(item.observed_days for item in months.values()) == 361
    assert sum(item.combined_entry_events for item in months.values()) == 201_664_595


def test_drift_receipt_replays_five_months_and_exact_total_delta() -> None:
    replay = load_nyc_crz_quantitative_audit().drift_replay
    changed = [item for item in replay.months if item.delta_current_minus_report]

    assert [item.month for item in changed] == [
        "2025-01",
        "2025-02",
        "2025-06",
        "2025-07",
        "2025-08",
    ]
    assert replay.months_with_nonzero_delta == 5
    assert replay.report_published_fewer_entries == 21_610_350
    assert replay.current_snapshot_recomputed_fewer_entries == 21_616_596
    assert replay.delta_current_minus_report == 6_246
    assert replay.replay_status == "exact"


def test_prediction_comparison_is_arithmetic_not_causal_attribution() -> None:
    audit = load_nyc_crz_quantitative_audit()
    comparison = audit.predicted_observed_audit
    boundary = audit.claim_boundary

    assert comparison.prediction_percent_reduction == 13.4
    assert comparison.agency_baseline_entry_events == 189_820_100
    assert comparison.current_snapshot_entry_events == 168_203_504
    assert comparison.current_snapshot_percent_below_agency_baseline == pytest.approx(
        11.38793836901361
    )
    assert comparison.difference_from_prediction_percentage_points == pytest.approx(
        2.0120616309863912
    )
    assert "agency-derived baseline" in comparison.agency_frame_reading
    assert "does not independently estimate a policy effect" in comparison.agency_frame_reading
    assert boundary.evidence_status == "descriptive_arithmetic_audit"
    assert boundary.causal_status == "not_identified"
    assert boundary.counterfactual_status == "agency_derived_not_independently_reconstructable"
    assert boundary.unit_status == "entry_events_not_unique_vehicles"


def test_changed_csv_value_is_refused_before_recomputation(tmp_path: Path) -> None:
    mutated = tmp_path / quant.VEHICLE_PATH.name
    shutil.copyfile(quant.VEHICLE_PATH, mutated)
    rows = list(csv.reader(mutated.read_text(encoding="utf-8").splitlines()))
    rows[1][3] = str(int(rows[1][3]) + 1)
    with mutated.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerows(rows)

    with pytest.raises(NycCrzQuantitativeError, match="frozen input digest mismatch"):
        quant._monthly_observations(mutated)


def test_mutated_drift_value_cannot_pass_replay(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    mutated = tmp_path / quant.DRIFT_PATH.name
    payload = json.loads(quant.DRIFT_PATH.read_text(encoding="utf-8"))
    payload["months"][0]["current_snapshot_recomputed_rounded"] += 1
    payload["months"][0]["delta_current_minus_report"] += 1
    mutated.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    monkeypatch.setattr(quant, "DRIFT_PATH", mutated)
    monkeypatch.setitem(EXPECTED_DIGESTS, mutated.name, _sha256(mutated))

    with pytest.raises(
        NycCrzQuantitativeError,
        match="drift_receipt_current_snapshot_value_mismatch",
    ):
        load_nyc_crz_quantitative_audit()


def test_transformation_output_digest_detects_post_recompute_mutation() -> None:
    audit = load_nyc_crz_quantitative_audit()
    payload = audit.model_dump(mode="json")
    payload["monthly_observations"][0]["combined_entry_events"] += 1

    with pytest.raises(ValueError, match="transformation_output_digest_mismatch"):
        NycCrzQuantitativeAudit.model_validate(payload)


def test_causal_effect_label_is_not_a_valid_boundary_state() -> None:
    payload = load_nyc_crz_quantitative_audit().claim_boundary.model_dump(mode="json")
    payload["causal_status"] = "identified_effect"

    with pytest.raises(ValueError, match="causal_status"):
        QuantitativeClaimBoundary.model_validate(payload)


def test_canonical_drift_file_is_pinned_despite_plan_reference_mismatch() -> None:
    actual = _sha256(quant.DRIFT_PATH)

    assert actual == EXPECTED_DIGESTS[quant.DRIFT_PATH.name]
    assert actual != "5c6af2bd776bc79c0e073320f46beb37d2419c2a6712f3c7234780f89836d549"
