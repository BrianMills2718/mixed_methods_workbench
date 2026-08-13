# Phase 3 portfolio decomposition

Status: active documentation/research phase; 14-method denominator adopted

Brian approved the 14-method alternative on 2026-08-13. The denominator is
`phase2b-proposal-0.3` (`P01`–`P13`) plus `P14`, theory-testing Process Tracing
in one bounded case. Exact variant descriptions remain in
[`../method_portfolio.md`](../method_portfolio.md).

[`WORK_PLAN.md`](WORK_PLAN.md) explains the lane boundaries and stop rules.
[`work_graph.json`](work_graph.json) is the machine-consumed WorkUnitV1 graph;
Phase 3 claims must bind to one ready unit. [`validation_receipt.md`](validation_receipt.md)
records validation of the graph itself, not evidence that a method has been
decomposed. `scripts/validate_phase3_work_graph.py` supplements the generic
WorkUnitV1 validator with exact denominator and transition invariants.

The three research lanes own disjoint method directories under `methods/`.
`P3-CONTROL` alone owns receipts and lifecycle transitions; `P3-INTEGRATE`
alone owns shared manifests and reports. The Process Tracing
topology prototype merged at `1fd01bc` and is pinned read-only implementation
evidence; it neither defines the `P14` ideal nor owns its decomposition.

Phase 3 does not authorize collisions, adjudication, coverage claims, schema or
vocabulary adoption, shared infrastructure, product changes, or producer
changes.
