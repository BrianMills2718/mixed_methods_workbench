# Phase 3 decomposition work plan

Status: adopted coordination plan; execution is limited to `work_graph.json`

## Adopted inputs

- Method-decomposition specification: rev 5.1, SHA-256
  `fbeb0e187f219a11051ba54fee6537b70448611080351044dc49f421e3c16c2f`.
- Accepted Phase 2 discovery format: merge `89e9515`, instrument SHA-256
  `1af191caf0634e99d7195831500ed5cacf79ad8988558ce60fc8083e102e07ff`.
- Portfolio proposal: `phase2b-proposal-0.3`, commit `9e8378c`.
- Human disposition: Brian's direct `approve 14` decision on 2026-08-13,
  selecting `P01`–`P13` plus non-substitutable `P14` Process Tracing.

The graph uses the `standard` profile because three independent research lanes
must converge on one denominator without sharing writable files, while a fifth
control unit owns their completion transitions.

## Units and exclusive outputs

| Unit | Methods | Exclusive paths |
| --- | --- | --- |
| `P3-RESEARCH-A` | `P01` systematic review, `P02` RCT, `P03` DiD, `P04` fsQCA, `P14` Process Tracing | `methods/p01/`, `p02/`, `p03/`, `p04/`, `p14/` |
| `P3-RESEARCH-B` | `P06` survey, `P07` quantitative text, `P08` forecasting, `P09` agent-based simulation | `methods/p06/`, `p07/`, `p08/`, `p09/` |
| `P3-RESEARCH-C` | `P05` grounded theory, `P10` RDM, `P11` option appraisal, `P12` Delphi, `P13` convergent mixed methods | `methods/p05/`, `p10/`, `p11/`, `p12/`, `p13/` |
| `P3-CONTROL` | Evidence review and lifecycle transitions; no methods | `lane_receipts/`, `work_graph.json` |
| `P3-INTEGRATE` | Denominator and format validation only | `portfolio_manifest.yaml`, `integration_report.md`, `validation_report.json` |

Each method directory must contain `frame.yaml`, `sources.md`,
`method_records.yaml`, `connections.yaml`, and `uncertainty.yaml`. The frame
freezes the exact variant, exclusions, applicability boundary, and source
edition/sections before decomposition. Records use the accepted three levels;
connections preserve typed topology; uncertainty distinguishes known, unknown,
contested, and source-limited judgments and states their downstream effect.
Research lanes commit only method evidence. `P3-CONTROL` separately owns each
later `lane_receipts/P3-RESEARCH-*.yaml` receipt and the graph lifecycle.

The research lanes do not read one another's emerging records. `P3-INTEGRATE`
becomes available only after all three are accepted. It checks denominator
completeness, IDs, source pins, required fields, connection integrity,
uncertainty accounting, and absence of out-of-scope claims. It may return a
directory to its owner; it may not repair or normalize method-owned semantics.

## Coordination and stop rules

Every lane requires a canonical registry claim bound to `work_graph.json` and
its exact unit ID. The completed `pt-topology-workbench` product lane merged at
`1fd01bc`; that revision is a read-only evidence surface and grants no Phase 3
ownership.

`P3-CONTROL` is the sole status mechanism and is independently claimable from
the start. The sequence for each research lane is intentionally three commits:

1. The research lane pushes an `evidence_commit` containing only its exclusive
   method paths. It cannot mark itself accepted or write a receipt.
2. `P3-CONTROL` verifies that Git object, its paths, checks, and review evidence,
   then creates a JSON-compatible YAML receipt in a later `receipt_commit`. The
   receipt names `unit_id`, `evidence_commit`, exact `method_paths`, `checks`,
   and `disposition: accepted`. The receipt commit must be a descendant of the
   evidence commit and cannot equal it.
3. In a subsequent `transition_commit`, `P3-CONTROL` exclusively edits
   `work_graph.json`: it changes the lane to `accepted` and adds one
   `CompletionReceipt` input with
   `<receipt-path>@<receipt_commit>`. The focused validator verifies both Git
   objects, the receipt bytes at that commit, its evidence binding and paths,
   ancestry, and that the receipt commit precedes the graph transition.

No research or integration lane edits graph statuses. `P3-INTEGRATE` becomes
`ready_for_execution` only after all three research units are accepted with
verified receipts, its failed guards are cleared, and both validators pass.

Stop and record explicit uncertainty if a source cannot pin the variant, a
record crosses source scope, or the format cannot express the method without
loss. Do not fix that by inventing shared types, combining methods, changing
the denominator, or beginning Phase 4. Completion means 14 source-frozen
decompositions pass integration; it does not mean any reusable capability has
been established.
