---
plan_id: "mixed_methods_workbench#psychosisbank-planning-receipt"
dependencies:
  - "AUTH"
  - "existing PsychosisBank Investigation Spine"
dependencies_reviewed: "2026-09-23"
---

# PsychosisBank source-bound planning receipt

Status: prepared implementation plan; no code is authorized by this document.

## Authorization and outcome

Brian's active goal is to deliver and publicly verify one workflow from a human
question through governed agentic planning, qualitative analysis, Process
Tracing, independent checking, and human review. This slice addresses only the
missing planning-record boundary for the existing PsychosisBank example.

The receipt must make one bounded choice inspectable:

> Given the PsychosisBank controlled-access question and its three frozen public
> sources, preserve the reviewed qualitative proposition as a candidate,
> test competing explanations with Process Tracing, retain the independent
> challenge as advisory, and direct the reviewer not to publish a causal claim
> until contemporaneous decision records are available.

It does not make an LLM choose a method, execute a producer, or turn the
unresolved result into a recommendation.

## Scope

In scope for a later claimed implementation slice:

- one typed, source-bound `planning_receipt.json` beside the connected run;
- validation that binds its question, source packet, reviewed QC input,
  Process Tracing export, independent-challenge boundary, and terminal human
  decision to exact digests;
- one read-only projection on the existing Investigation Spine page and JSON
  endpoint; and
- focused corruption controls for changed inputs, invented source coverage,
  an unbounded causal claim, or a missing human-review boundary.

Out of scope:

- qualitative_coding or process_tracing changes, fresh model calls, rerunning
  the case, generic planning/orchestration infrastructure, shared schemas,
  method selection claims, deployment, and publication of a causal finding.

## Contract sketch

```text
human question + decision context
  -> frozen source packet and known gaps
  -> reviewed QC candidate proposition
  -> Process Tracing route, claim limits, and terminal result
  -> independent challenge provenance and advisory boundary
  -> human decision: withhold causal publication; seek named records
```

Required fields are: schema version, investigation ID, question, decision
context, source/input digests, method-owner revisions, selected method roles,
prohibited inferences, terminal review state, next evidence, and exact links
to the existing retained artifacts. The receipt must reject extra fields and
must never contain raw producer internals as a new public contract.

## Acceptance evidence

| Criterion | Evidence |
| --- | --- |
| The plan is pinned to the exact evidence universe and method artifacts. | Positive digest validation and changed-input negative control. |
| It distinguishes planning from substantive inference. | Typed roles and explicit non-claims; no model call in the consumer. |
| It preserves the publication block and a human-owned decision. | Negative control rejects an accepted causal conclusion or absent review boundary. |
| Browser and JSON views present the same receipt. | Focused endpoint/UI-parity test and rendered local review. |

## Preconditions and stop points

- Re-check the active `goal/psychosisbank-fresh-qc` lane before touching the
  run directory; it currently owns the run evidence and its changes must be
  consumed only after it publishes a stable receipt.
- Stop if the fresh-QC lane changes the source packet or Process Tracing export
  without a corresponding stable digest update.
- Stop before deployment or any claim that the causal explanation is supported.

## Next implementation sequence

1. Wait for, or read, the fresh-QC lane's stable receipt and exact digests.
2. Implement the strict receipt and its integrity checks in a non-overlapping
   claimed lane.
3. Add the read-only JSON/browser projection.
4. Run focused contract, corruption, endpoint, and rendered checks.
5. Prepare a portfolio release candidate that links to the review surface;
   public deployment remains a separate authorization boundary.
