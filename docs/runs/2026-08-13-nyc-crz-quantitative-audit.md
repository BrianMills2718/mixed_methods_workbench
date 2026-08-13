# NYC CRZ Predicted-Versus-Observed Arithmetic Audit

**Packet:** `NYC-CRZ-MVP-v1`

**Work unit:** `NYC-QUANT-1`

**State:** reproducible descriptive audit; causal attribution refused

## Outcome

The frozen 25,992-row Open NY snapshot recomputes to 12 monthly observations
covering 361 days. The January-through-October entry-event total is
168,203,504. Against the first evaluation report's agency-derived No Action
baseline total of 189,820,100, the arithmetic difference is 21,616,596 entry
events, or 11.3879% below that baseline.

The frozen pre-implementation Phase 1 prediction is a 13.4% reduction relative
to No Action. Within the agency's own comparison frame, the current snapshot
arithmetic is therefore about 2.0121 percentage points below that prediction.
This is a comparison of entry events with an agency-derived baseline. It is not
an independently identified policy effect, a count of unique vehicles, a
revenue calculation, or an independently reconstructed counterfactual.

## Exact query receipt

- Dataset: `t6yz-b64h`
- Retrieval: `2026-08-13T19:40:23Z`
- Source last modified: `2026-08-13T18:29:49Z`
- Rows: 25,992
- Columns: 5
- Missing measure rows: 0
- Coverage: 2025-01-05 through 2025-12-31
- Observed days: 361
- Input CSV SHA-256: `01dec3a0a1effc26aacf57ba8c4474775fb4db73149c462d4f40432e6e323bd3`
- Metadata SHA-256: `eabcbb927cff3e4023fe8b15b89e786f537b8e7ed20693b0da960d13eae41fdf`
- Response-header SHA-256: `afc73a688c3f9836152d33b8cbe0057764df1183d8516d0be87ea698a88a8a32`
- Canonical monthly-output SHA-256: `5446604efb583a19e6bee417c1ffadc319eec08f13da3d8c1f662c2d18142189`

The transformation sums integer `crz_entries` and
`excluded_roadway_entries` by date and then calendar month. It retains exact
monthly totals, observed-day denominators, unrounded daily means, and rounded
display means.

## Publication-version drift replay

The current frozen snapshot exactly replays the accepted drift receipt:

- nonzero monthly deltas: January, February, June, July, and August;
- report-published fewer-entry total: 21,610,350;
- current-snapshot recomputed fewer-entry total: 21,616,596; and
- current minus report: 6,246 entry events.

The report's publication-time observations and the current API snapshot remain
separate evidence versions. The report's displayed rounded monthly averages do
not independently reconstruct its published total.

## Planning-input discrepancy

Plan #5 currently identifies the drift receipt input as
`sha256:5c6af2bd...`. The canonical file on `main`, unchanged since its source
freeze commit, hashes to
`0961133cc6a6441a944f00a45a7574e58a69bd0ca51fc2cb70da67540083f578`.
The executable audit pins the actual canonical bytes and tests that the two
values are not silently conflated. This is planning-method feedback: the work
graph validator established readiness without verifying that an input revision
matched its referenced repository artifact.

## Verification

- Nine focused tests passed.
- Mutation of one frozen CSV value failed at the input-digest gate.
- A mutated publication-drift value failed against direct recomputation.
- Mutation after transformation failed the output-digest binding.
- `identified_effect` is not a valid causal status.
- Ruff and strict mypy passed for the quantitative module and tests.

## Downstream handoff

`NYC-INTEGRATE-1` may consume this typed audit as a quantitative strand. It
must preserve the agency assertion source, observed-public-data status,
publication-version drift, entry-event unit, coverage dates, and all causal and
counterfactual refusals. No shared quantitative engine is promoted from this
single Workbench-local consumer.
