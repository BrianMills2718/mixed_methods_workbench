# NYC CRZ Anchored Extraction Canary

**Packet:** `NYC-CRZ-MVP-v1`

**Work unit:** `NYC-EXTRACT-1`

**State:** structurally valid; **pending human review**
**Executed:** 2026-08-13

## Outcome

One agency prediction candidate and one public-hearing concern candidate were
returned by an authentic shared-`llm_client` structured-output call. Both
retained evidence selections bind uniquely to exact, hash-bound source units.
Neither candidate is an accepted finding. The model-authored `limit` fields
were rejected because they introduced framing not established by their source
units; deterministic Workbench claim limits are carried separately.

This run demonstrates the structural capability:

`verified source bytes -> bounded source unit -> typed candidate -> exact evidence anchor -> human review gate`

It does not demonstrate QC Describe, causal inference, representativeness,
policy appraisal, or a recommendation.

## Exact source gate

| Artifact | Expected and observed bytes | Expected and observed SHA-256 |
| --- | ---: | --- |
| `reevaluation_2` | 1,430,307 | `aee0e0b6c17a8e9585c24a808d2fa77a756b267fe9af326fb577ae181bb28733` |
| `hearing_2022_08_25` | 1,470,785 | `e42cbffeec77b2392cc6e74b36ba8978c08a69f63cfa5a341ee512c6e7a67cf1` |

The live runner verifies both values before importing `pypdf` and parsing the
documents.

## Authentic runtime receipt

- Trace: `mixed_methods_workbench/nyc-crz-mvp-v1/anchored-extraction-canary-3`
- Logical call: `llmcall_ef6303a0551347c38932ba752c1500fd`
- Requested/resolved model: `openrouter/deepseek/deepseek-v4-flash`
- Cache hit: `false`
- Prompt tokens: 329
- Completion tokens: 413
- Cost: `$0.00015477` (`provider_reported`)
- Prompt SHA-256: `53a47c15179f058706f2f25c0e6aded6bf913f7ef4f54c7d1fb581115927aec1`
- Schema SHA-256: `dc6bf96d01205402307d088d6c8cbbe52728a4f77b8baf204039a7dfcfdc2573`
- Prediction context SHA-256: `2a02605d96ea874298de417648c37ab7fa895facb3bda857c43b72697ec06f90`
- Concern context SHA-256: `30fd25e04b5aea4999c09ad3d274ad54cc0636c5ae956e799c0753e7be1b2ff1`

Two earlier authentic attempts are retained in
`examples/fixtures/nyc_crz_evidence_slice/canary_run_receipt.json`:

1. attempt 1 failed exact hearing-quote binding after printed line-number
   normalization;
2. attempt 2 was rejected because the supplied prediction source unit did not
   support the scenario field; and
3. attempt 3 passed schema and binding checks and remains pending human review.

## Frozen descriptive observation

Direct recomputation over the exact frozen Open NY CSV produced:

- coverage: 2025-01-05 through 2025-12-31;
- observed days: 361;
- CRZ entries: 178,203,234;
- excluded-roadway entries: 23,461,361; and
- mean daily CRZ entries: 493,637.7673.

This is a descriptive aggregation, not unique vehicles, revenue, a causal
effect, or an independent reproduction of an agency counterfactual.

## Verification

- Focused pytest result: 15 passed across the new NYC slice and the preserved
  PsychosisBank Investigation Spine tests.
- Negative controls passed for source-byte mutation, pinned-fixture mutation,
  non-binding quote mutation, and acceptance without an attributable human
  decision.
- The live runner reproduced all four retained prompt/schema/context digests
  from exact PDFs without another provider call.
- Fresh headless Chromium checks passed at desktop and 390-pixel mobile widths.
  The NYC candidate state, provenance/interpretation boundary, aggregate, and
  no-accepted-finding language were visible; the PsychosisBank route remained
  functional; no console, page, request, or HTTP response errors occurred.

## Required human decision

The browser and JSON projection intentionally stop at
`pending_human_review`. A reviewer must decide whether each proposed wording
preserves its source's assertion and meaning, then reject it, request a new
derivation, or accept it for downstream method-owned analysis. No automatic
transition is permitted.
