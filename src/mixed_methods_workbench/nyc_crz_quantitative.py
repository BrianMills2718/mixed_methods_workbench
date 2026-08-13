"""Reproducible NYC congestion-pricing descriptive comparison.

The audit recomputes public entry-event aggregates and replays the agency
publication drift receipt. It intentionally does not turn the agency's
No-Action baseline into an independently identified causal counterfactual.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_ROOT = PROJECT_ROOT / "docs" / "research" / "evidence" / "nyc_crz_mvp_v1"
MANIFEST_PATH = EVIDENCE_ROOT / "source_manifest.json"
VEHICLE_PATH = EVIDENCE_ROOT / "t6yz_first_year_daily_by_group_class.csv"
METADATA_PATH = EVIDENCE_ROOT / "t6yz_metadata.json"
HEADERS_PATH = EVIDENCE_ROOT / "t6yz_response_headers.txt"
DRIFT_PATH = EVIDENCE_ROOT / "report_table_2_1_drift_receipt.json"

EXPECTED_DIGESTS = {
    "source_manifest.json": "63dd0ec70180800e4678572570f97514849633eaa16284b706ea66615b0e63dc",
    "t6yz_first_year_daily_by_group_class.csv": "01dec3a0a1effc26aacf57ba8c4474775fb4db73149c462d4f40432e6e323bd3",
    "t6yz_metadata.json": "eabcbb927cff3e4023fe8b15b89e786f537b8e7ed20693b0da960d13eae41fdf",
    "t6yz_response_headers.txt": "afc73a688c3f9836152d33b8cbe0057764df1183d8516d0be87ea698a88a8a32",
    # Plan #5 currently names 5c6af2bd... for this input. That value is
    # not the canonical file digest; fail-loud execution pins the bytes below.
    "report_table_2_1_drift_receipt.json": "0961133cc6a6441a944f00a45a7574e58a69bd0ca51fc2cb70da67540083f578",
}


class NycCrzQuantitativeError(ValueError):
    """Raised when a frozen input or quantitative invariant fails."""


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class FrozenQuery(_StrictModel):
    select: Literal[
        "toll_date,detection_group,vehicle_class,sum(crz_entries) as crz_entries,sum(excluded_roadway_entries) as excluded_roadway_entries"
    ]
    where: Literal[
        "toll_date between '2025-01-05T00:00:00.000' and '2025-12-31T00:00:00.000'"
    ]
    group: Literal["toll_date,detection_group,vehicle_class"]
    order: Literal["toll_date,detection_group,vehicle_class"]
    limit: Literal[50000]


class FrozenTabularQueryReceipt(_StrictModel):
    schema_version: Literal["mmw.frozen_tabular_query_receipt.v0.1"]
    packet_id: Literal["NYC-CRZ-MVP-v1"]
    artifact_id: Literal["t6yz_first_year_daily_by_group_class"]
    dataset_id: Literal["t6yz-b64h"]
    endpoint: Literal["https://data.ny.gov/resource/t6yz-b64h.csv"]
    retrieved_at: Literal["2026-08-13T19:40:23Z"]
    source_last_modified: Literal["2026-08-13T18:29:49Z"]
    etag: str = Field(min_length=10)
    query: FrozenQuery
    input_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    metadata_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    response_headers_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    row_count: int = Field(ge=0)
    column_count: int = Field(ge=1)
    missing_measure_rows: int = Field(ge=0)
    coverage_start: Literal["2025-01-05"]
    coverage_end: Literal["2025-12-31"]
    observed_days: int = Field(ge=1)
    transformation: Literal[
        "sum integer crz_entries and excluded_roadway_entries by toll_date, then by calendar month"
    ]
    output_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")

    @model_validator(mode="after")
    def _matches_frozen_shape(self) -> FrozenTabularQueryReceipt:
        if (
            self.row_count,
            self.column_count,
            self.missing_measure_rows,
            self.observed_days,
        ) != (25_992, 5, 0, 361):
            raise ValueError("frozen_query_shape_mismatch")
        return self


class MonthlySnapshotObservation(_StrictModel):
    month: str = Field(pattern=r"^2025-(0[1-9]|1[0-2])$")
    observed_days: int = Field(ge=1, le=31)
    combined_entry_events: int = Field(ge=0)
    mean_daily_entry_events: float = Field(ge=0)
    mean_daily_entry_events_rounded: int = Field(ge=0)
    evidence_kind: Literal["observed_public_data"]


class DriftMonth(_StrictModel):
    month: str = Field(pattern=r"^2025-(0[1-9]|1[0])$")
    report_observed_at_publication: int = Field(ge=0)
    current_snapshot_recomputed_rounded: int = Field(ge=0)
    delta_current_minus_report: int
    report_baseline: int = Field(ge=0)

    @model_validator(mode="after")
    def _delta_is_reproducible(self) -> DriftMonth:
        if (
            self.current_snapshot_recomputed_rounded
            - self.report_observed_at_publication
            != self.delta_current_minus_report
        ):
            raise ValueError("monthly_drift_delta_mismatch")
        return self


class DriftReplay(_StrictModel):
    report_table: Literal["Table 2-1"]
    report_pdf_page_index_zero_based: Literal[16]
    report_printed_page_label: Literal["9"]
    receipt_input_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    months: list[DriftMonth] = Field(min_length=10, max_length=10)
    months_with_nonzero_delta: int = Field(ge=0)
    report_published_fewer_entries: int = Field(ge=0)
    current_snapshot_recomputed_fewer_entries: int = Field(ge=0)
    delta_current_minus_report: int
    replay_status: Literal["exact"]

    @model_validator(mode="after")
    def _matches_frozen_drift_totals(self) -> DriftReplay:
        observed = (
            self.months_with_nonzero_delta,
            self.report_published_fewer_entries,
            self.current_snapshot_recomputed_fewer_entries,
            self.delta_current_minus_report,
        )
        if observed != (5, 21_610_350, 21_616_596, 6_246):
            raise ValueError("frozen_drift_total_mismatch")
        return self


class PredictedObservedAudit(_StrictModel):
    prediction_percent_reduction: float
    prediction_scenario: Literal["Phase 1 ($9 peak auto toll)"]
    prediction_basis: Literal["No Action"]
    prediction_assertion_source: Literal["agency"]
    prediction_review_status: Literal["source_value_not_promoted_as_human_reviewed_extraction"]
    comparison_coverage_start: Literal["2025-01-05"]
    comparison_coverage_end: Literal["2025-10-31"]
    agency_baseline_entry_events: int = Field(ge=0)
    current_snapshot_entry_events: int = Field(ge=0)
    current_snapshot_fewer_entry_events: int = Field(ge=0)
    current_snapshot_percent_below_agency_baseline: float
    difference_from_prediction_percentage_points: float
    report_publication_percent_below_agency_baseline: float
    agency_frame_reading: str

    @model_validator(mode="after")
    def _matches_frozen_comparison(self) -> PredictedObservedAudit:
        observed = (
            self.prediction_percent_reduction,
            self.agency_baseline_entry_events,
            self.current_snapshot_entry_events,
            self.current_snapshot_fewer_entry_events,
        )
        if observed != (13.4, 189_820_100, 168_203_504, 21_616_596):
            raise ValueError("frozen_predicted_observed_comparison_mismatch")
        return self


class QuantitativeClaimBoundary(_StrictModel):
    evidence_status: Literal["descriptive_arithmetic_audit"]
    causal_status: Literal["not_identified"]
    counterfactual_status: Literal["agency_derived_not_independently_reconstructable"]
    unit_status: Literal["entry_events_not_unique_vehicles"]
    publication_version_status: Literal["current_snapshot_differs_from_report_publication_values"]
    may_say: list[str] = Field(min_length=2)
    must_not_say: list[str] = Field(min_length=4)

    @model_validator(mode="after")
    def _required_refusals(self) -> QuantitativeClaimBoundary:
        required = ("causal effect", "revenue", "unique vehicles", "exact reproduction")
        joined = " ".join(self.must_not_say).lower()
        if any(term not in joined for term in required):
            raise ValueError("quantitative_claim_boundary_missing_required_refusal")
        return self


class NycCrzQuantitativeAudit(_StrictModel):
    schema_version: Literal["mmw.nyc_crz_quantitative_audit.v0.1"]
    investigation_id: Literal["nyc-congestion-relief-zone-first-year"]
    status: Literal["reproducible_descriptive_audit"]
    query_receipt: FrozenTabularQueryReceipt
    monthly_observations: list[MonthlySnapshotObservation] = Field(
        min_length=12, max_length=12
    )
    drift_replay: DriftReplay
    predicted_observed_audit: PredictedObservedAudit
    claim_boundary: QuantitativeClaimBoundary

    @model_validator(mode="after")
    def _receipt_binds_output(self) -> NycCrzQuantitativeAudit:
        observed_digest = canonical_sha256(
            [item.model_dump(mode="json") for item in self.monthly_observations]
        )
        if observed_digest != self.query_receipt.output_sha256:
            raise ValueError("transformation_output_digest_mismatch")
        current = {item.month: item for item in self.monthly_observations}
        for row in self.drift_replay.months:
            if (
                current[row.month].mean_daily_entry_events_rounded
                != row.current_snapshot_recomputed_rounded
            ):
                raise ValueError("drift_receipt_does_not_replay_current_snapshot")
        return self


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _read_pinned_json(path: Path) -> object:
    expected = EXPECTED_DIGESTS[path.name]
    observed = file_sha256(path)
    if observed != expected:
        raise NycCrzQuantitativeError(
            f"frozen input digest mismatch for {path.name}: expected {expected}, observed {observed}"
        )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise NycCrzQuantitativeError(f"invalid frozen JSON: {path.name}") from exc


def _pinned_non_json_digest(path: Path) -> str:
    expected = EXPECTED_DIGESTS[path.name]
    observed = file_sha256(path)
    if observed != expected:
        raise NycCrzQuantitativeError(
            f"frozen input digest mismatch for {path.name}: expected {expected}, observed {observed}"
        )
    return observed


def _headers() -> dict[str, str]:
    _pinned_non_json_digest(HEADERS_PATH)
    headers: dict[str, str] = {}
    for line in HEADERS_PATH.read_text(encoding="utf-8").splitlines()[1:]:
        if ":" in line:
            name, value = line.split(":", 1)
            headers[name.strip().lower()] = value.strip()
    return headers


def _monthly_observations(path: Path = VEHICLE_PATH) -> tuple[list[MonthlySnapshotObservation], int, int]:
    _pinned_non_json_digest(path)
    monthly_daily: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    row_count = 0
    missing_measure_rows = 0
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != [
            "toll_date",
            "detection_group",
            "vehicle_class",
            "crz_entries",
            "excluded_roadway_entries",
        ]:
            raise NycCrzQuantitativeError("vehicle snapshot schema mismatch")
        for row in reader:
            row_count += 1
            if not row["crz_entries"] or not row["excluded_roadway_entries"]:
                missing_measure_rows += 1
                continue
            date = row["toll_date"][:10]
            monthly_daily[date[:7]][date] += int(row["crz_entries"]) + int(
                row["excluded_roadway_entries"]
            )
    observations = []
    for month, daily in sorted(monthly_daily.items()):
        total = sum(daily.values())
        mean = total / len(daily)
        observations.append(
            MonthlySnapshotObservation(
                month=month,
                observed_days=len(daily),
                combined_entry_events=total,
                mean_daily_entry_events=mean,
                mean_daily_entry_events_rounded=round(mean),
                evidence_kind="observed_public_data",
            )
        )
    if row_count != 25992 or missing_measure_rows != 0 or len(observations) != 12:
        raise NycCrzQuantitativeError("vehicle snapshot shape or missingness mismatch")
    return observations, row_count, missing_measure_rows


def load_nyc_crz_quantitative_audit() -> NycCrzQuantitativeAudit:
    """Recompute all arithmetic from exact inputs and enforce the claim boundary."""

    try:
        manifest = _read_pinned_json(MANIFEST_PATH)
        _read_pinned_json(METADATA_PATH)
        drift_raw = _read_pinned_json(DRIFT_PATH)
        if not isinstance(manifest, dict) or not isinstance(drift_raw, dict):
            raise TypeError("frozen manifest and drift receipt must be objects")
        snapshot = next(
            item
            for item in manifest["data_snapshots"]
            if item["artifact_id"] == "t6yz_first_year_daily_by_group_class"
        )
        observations, row_count, missing_rows = _monthly_observations()
        observation_by_month = {item.month: item for item in observations}
        drift_months = [DriftMonth.model_validate(item) for item in drift_raw["months"]]
        nonzero = sum(item.delta_current_minus_report != 0 for item in drift_months)
        if nonzero != 5:
            raise ValueError("unexpected_nonzero_drift_month_count")
        for item in drift_months:
            if (
                observation_by_month[item.month].mean_daily_entry_events_rounded
                != item.current_snapshot_recomputed_rounded
            ):
                raise ValueError("drift_receipt_current_snapshot_value_mismatch")

        jan_oct_days = sum(observation_by_month[item.month].observed_days for item in drift_months)
        if jan_oct_days != 300:
            raise ValueError("jan_oct_coverage_day_mismatch")
        agency_baseline_total = sum(
            item.report_baseline * observation_by_month[item.month].observed_days
            for item in drift_months
        )
        current_total = sum(
            observation_by_month[item.month].combined_entry_events for item in drift_months
        )
        current_fewer = agency_baseline_total - current_total
        totals = drift_raw["january_through_october"]
        if current_fewer != totals[
            "current_snapshot_recomputed_fewer_entries_using_report_baselines"
        ]:
            raise ValueError("current_snapshot_fewer_entries_mismatch")
        report_fewer = totals["report_published_fewer_entries"]

        query = snapshot["query"]
        headers = _headers()
        output_digest = canonical_sha256(
            [item.model_dump(mode="json") for item in observations]
        )
        receipt = FrozenTabularQueryReceipt(
            schema_version="mmw.frozen_tabular_query_receipt.v0.1",
            packet_id="NYC-CRZ-MVP-v1",
            artifact_id="t6yz_first_year_daily_by_group_class",
            dataset_id="t6yz-b64h",
            endpoint=snapshot["endpoint"],
            retrieved_at=snapshot["retrieved_at"],
            source_last_modified=snapshot["source_last_modified"],
            etag=headers["etag"],
            query=FrozenQuery(
                select=query["$select"],
                where=query["$where"],
                group=query["$group"],
                order=query["$order"],
                limit=query["$limit"],
            ),
            input_sha256=EXPECTED_DIGESTS[VEHICLE_PATH.name],
            metadata_sha256=EXPECTED_DIGESTS[METADATA_PATH.name],
            response_headers_sha256=EXPECTED_DIGESTS[HEADERS_PATH.name],
            row_count=row_count,
            column_count=snapshot["columns"],
            missing_measure_rows=missing_rows,
            coverage_start="2025-01-05",
            coverage_end="2025-12-31",
            observed_days=sum(item.observed_days for item in observations),
            transformation=(
                "sum integer crz_entries and excluded_roadway_entries by toll_date, "
                "then by calendar month"
            ),
            output_sha256=output_digest,
        )
        replay = DriftReplay(
            report_table=drift_raw["report_locator"]["table"],
            report_pdf_page_index_zero_based=drift_raw["report_locator"][
                "pdf_page_index_zero_based"
            ],
            report_printed_page_label=drift_raw["report_locator"]["printed_page_label"],
            receipt_input_sha256=EXPECTED_DIGESTS[DRIFT_PATH.name],
            months=drift_months,
            months_with_nonzero_delta=nonzero,
            report_published_fewer_entries=report_fewer,
            current_snapshot_recomputed_fewer_entries=current_fewer,
            delta_current_minus_report=totals["delta_current_minus_report"],
            replay_status="exact",
        )
        current_percent = current_fewer / agency_baseline_total * 100
        report_percent = report_fewer / agency_baseline_total * 100
        comparison = PredictedObservedAudit(
            prediction_percent_reduction=13.4,
            prediction_scenario="Phase 1 ($9 peak auto toll)",
            prediction_basis="No Action",
            prediction_assertion_source="agency",
            prediction_review_status="source_value_not_promoted_as_human_reviewed_extraction",
            comparison_coverage_start="2025-01-05",
            comparison_coverage_end="2025-10-31",
            agency_baseline_entry_events=agency_baseline_total,
            current_snapshot_entry_events=current_total,
            current_snapshot_fewer_entry_events=current_fewer,
            current_snapshot_percent_below_agency_baseline=current_percent,
            difference_from_prediction_percentage_points=13.4 - current_percent,
            report_publication_percent_below_agency_baseline=report_percent,
            agency_frame_reading=(
                "Within the agency's own No Action comparison frame, the current frozen "
                "snapshot arithmetic is about 11.39% below the agency baseline through "
                "October, roughly 2.01 percentage points below the 13.4% Phase 1 prediction. "
                "This compares entry events with an agency-derived baseline; it does not "
                "independently estimate a policy effect."
            ),
        )
        boundary = QuantitativeClaimBoundary(
            evidence_status="descriptive_arithmetic_audit",
            causal_status="not_identified",
            counterfactual_status="agency_derived_not_independently_reconstructable",
            unit_status="entry_events_not_unique_vehicles",
            publication_version_status="current_snapshot_differs_from_report_publication_values",
            may_say=[
                "The current frozen snapshot supports reproducible descriptive entry-event aggregation.",
                "Within the agency comparison frame, current Jan-Oct arithmetic is about 11.39% below its No Action baseline.",
                "Five monthly rounded values changed after the report's publication snapshot, producing a 6,246-entry difference in the fewer-entry total.",
            ],
            must_not_say=[
                "This arithmetic identifies the causal effect of congestion pricing.",
                "Entry events are unique vehicles.",
                "The public entry table can calculate program revenue.",
                "The current snapshot is an exact reproduction of the report's publication-time observations.",
                "The agency-derived counterfactual was independently reconstructed from open data.",
            ],
        )
        return NycCrzQuantitativeAudit(
            schema_version="mmw.nyc_crz_quantitative_audit.v0.1",
            investigation_id="nyc-congestion-relief-zone-first-year",
            status="reproducible_descriptive_audit",
            query_receipt=receipt,
            monthly_observations=observations,
            drift_replay=replay,
            predicted_observed_audit=comparison,
            claim_boundary=boundary,
        )
    except NycCrzQuantitativeError:
        raise
    except (KeyError, StopIteration, TypeError, ValueError) as exc:
        raise NycCrzQuantitativeError(f"invalid NYC quantitative boundary: {exc}") from exc


def nyc_crz_quantitative_audit_payload() -> dict[str, object]:
    return load_nyc_crz_quantitative_audit().model_dump(mode="json")
