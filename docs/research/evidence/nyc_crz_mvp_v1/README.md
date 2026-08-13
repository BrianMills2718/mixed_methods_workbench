# NYC-CRZ-MVP-v1 Frozen Evidence

This directory contains the two immutable, public-data snapshots accepted for
the first New York City congestion-pricing MVP vertical. The controlling
question, document-byte manifest, claim boundaries, and refusal rules are in
[`nyc_crz_source_freeze.md`](../../nyc_crz_source_freeze.md).

## Frozen queries

`t6yz_first_year_daily_by_group_class.csv` was returned by:

```text
GET https://data.ny.gov/resource/t6yz-b64h.csv
$select=toll_date,detection_group,vehicle_class,sum(crz_entries) as crz_entries,sum(excluded_roadway_entries) as excluded_roadway_entries
$where=toll_date between '2025-01-05T00:00:00.000' and '2025-12-31T00:00:00.000'
$group=toll_date,detection_group,vehicle_class
$order=toll_date,detection_group,vehicle_class
$limit=50000
```

It contains 25,992 data rows: 361 dates × 12 detection groups × 6 vehicle
classes. Neither measure has a missing value. SHA-256:
`01dec3a0a1effc26aacf57ba8c4474775fb4db73149c462d4f40432e6e323bd3`.

`sayj_transit_context_2024_2025.csv` was returned by:

```text
GET https://data.ny.gov/resource/sayj-mze2.csv
$select=date,mode,count
$where=date between '2024-01-01T00:00:00.000' and '2025-12-31T00:00:00.000' and mode in('Subway','Bus','LIRR','MNR','AAR','SIR')
$order=date,mode
$limit=10000
```

It contains 4,386 data rows: 731 dates × 6 transit modes. `count` has no
missing value in this subset. SHA-256:
`373f3f855d09da65079ee2918667cda2ebd4f533e0928802033be4e5888270bd`.

The corresponding raw Socrata metadata and HTTP response headers are retained
beside each CSV. The response headers establish retrieval time, schema, ETag,
and the source's last-modified time. The metadata is a snapshot, not a license.

## Permitted interpretation

- The vehicle-entry table supports reproducible descriptive aggregation for
  the first operating year.
- The transit table supplies contextual comparison only. Its pre-period does
  not by itself identify a congestion-pricing effect.
- The program-specific entry series starts on the intervention date, so no
  causal counterfactual may be imputed from it.
- The underlying entry dataset explicitly says it must not be used to
  calculate program revenue.
- Any silent source, query, schema, or content-digest change invalidates this
  freeze and requires a new packet version.

## Integrity checks

For the vehicle table, a CSV-aware direct sum of the frozen columns is
178,203,234 CRZ entries and 23,461,361 excluded-roadway entries. These are
checksum-like recomputation receipts, not substantive conclusions or unique
vehicles. A plain delimiter-based sum is invalid because quoted detection-group
labels contain commas.

The current public snapshot differs slightly from the monthly values frozen in
Table 2-1 of the first evaluation report. The exact month-level comparison and
the separate published-versus-recomputed totals are retained in
[`report_table_2_1_drift_receipt.json`](report_table_2_1_drift_receipt.json).
Consumers must preserve `report_observed_at_publication` separately from
`current_snapshot_recomputed`; the live dataset is not an exact reproduction of
the report's publication-time observation table.
