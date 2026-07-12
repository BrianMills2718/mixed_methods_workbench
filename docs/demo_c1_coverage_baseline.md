# DEMO-C1 Coverage Baseline

Generated: 2026-07-12  
Status: historical pre-implementation visibility baseline

## Grade Distribution

| Grade | Count | Percent |
|---|---:|---:|
| A | 0 | 0% |
| B | 0 | 0% |
| C | 0 | 0% |
| D | 8 | 100% |
| F | 0 | 0% |

Overall grade: **D**

The approved static mockup is product-direction evidence, not runtime fixture
evidence. It therefore remains D/doc rather than being promoted to C.

## Requirements

| ID | Requirement | Grade | Evidence class | Closes when |
|---|---|---|---|---|
| C1 | Controlled packet hashes/anchors/bindings validate | D | doc | typed fixture plus automated both-sign controls |
| C2 | QC remains qualitative and source-traceable | D | doc | typed fixture plus leakage/anchor controls |
| C3 | PT retains rival-comparison semantics | D | doc | typed fixture plus residual/truth-probability controls |
| C4 | GT-I exposes development without saturation overclaim | D | doc | typed fixture plus provenance/overclaim controls |
| C5 | Links are neutral, typed, and target native objects | D | doc | typed fixture plus relationship/target controls |
| C6 | Review packet preserves three lanes and source step-down | D | doc | assembled fixture plus missing-lane/reference controls |
| C7 | CLI/Make surface is agent-drivable and fail-loud | D | doc | executable commands plus exit/diagnostic tests |
| C8 | Fixture provenance and claim limits are exhaustive | D | doc | manifest validation plus stale/unlisted/escalation controls |

## Missing Controls

All eight rows lack executable positive and negative controls because `DEMO-C1`
is not implemented. None may be wired into `make check` yet.

## What Closes the Rows

Authorize `DEMO-C1`, then implement the vertical Harbor fixture path in the
order stated by `docs/plans/demo_c1_local_contract_fixture_implementation.md`.
Promotion must follow D → C/fixture → schema-validated/B where applicable →
A/test; no grade moves merely because the mockup was approved.

`DEMO-C1` was subsequently authorized and completed. The current generated
state is in `docs/coverage_report.md`; these eight rows are now A/test for
synthetic contract behavior only.
