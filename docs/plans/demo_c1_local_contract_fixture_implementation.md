# DEMO-C1: Local Typed Contract and Fixture Implementation

Status: ready for authorization; not active  
Parent: `docs/plans/current_demo_method_core.md`  
Mockup: approved by Brian on 2026-07-12  
Target capability: `DEMO`, preparing but not closing `QC-D`, `PT-D`, `GT-D`,
or `CORE-D`

## Outcome

A local, agent-drivable command validates one synthetic controlled packet,
three method-distinct synthetic producer-shaped artifacts, explicit
cross-method links, and one assembled review packet against typed Pydantic
contracts. Positive and negative controls prove that method leakage,
unsupported versions, broken anchors, missing PT residuals, GT saturation
overclaims, generic aggregation, and empirical overclaims fail loudly.

This slice proves contract behavior on synthetic data only. It does not run or
validate QC, PT, or GT-I engines.

## Authorization Boundary

In scope after Brian authorizes `DEMO-C1`:

- establish the repository's Python package/test skeleton in `pyproject.toml`;
- add strict producer-shaped and permissive consumer Pydantic models;
- add synthetic Harbor Agency packet/QC/PT/GT-I/link/review fixtures;
- add pure assembly/validation functions, CLI and Make targets;
- publish coverage before enforcement, then add both-sign controls, then wire
  calibrated checks into `make check`;
- update the notebook from `stub` to `fixture` only where execution proves it.

Out of scope:

- editing or invoking producer repositories;
- adapters over `ProjectState`, PT internals, or live Theory Forge artifacts;
- LLM calls, UI/API servers, OntoCanon/DIGIMON, theory recommendation,
  quantitative text, or final corpus selection;
- any empirical, full-GT, method-validity, mixed-methods, or SOTA claim.

## Derived Schema Boundary

The approved domain model yields four modules rather than one universal model:

```text
demo_packet.py       ControlledDemoPacket, documents, segments, anchors
method_exports.py    strict QC/PT/GT-I synthetic producer-shaped exports
review_packet.py     compatible views, CrossMethodLink, CoreDemoReviewPacket
assemble.py          validation/linking/assembly functions and typed failures
```

Producer-shaped models use `extra="forbid"`. Workbench-compatible consumer
models use `extra="ignore"` but still reject unsupported major versions and
missing required semantics. Every public module/class/function has a why-focused
docstring. No raw `dict`, `Any`, or `**kwargs` crosses a seam.

## Runtime Backward Pass

Final payload: `CoreDemoReviewPacket` containing the packet identity, three
distinct method views, typed neutral links, validation results, step-down
references, and synthetic-only claim limits.

Assembler: `assemble_core_demo_review(packet, qc, pt, gt, links)` validates
versions/bindings, native IDs, exact anchors, per-method rules, link targets,
and claim limits before returning the final payload.

Runtime preconditions:

- all inputs bind to the same packet ID and supported major version;
- all cited anchors and native objects exist;
- QC contains no PT comparative inference;
- PT has at least two rivals including exactly one residual and avoids
  probability-of-truth semantics;
- GT-I carries explicit no-saturation/full-GT limitations and comparison
  provenance;
- links use only `addresses`, `challenges`, `contextualizes`, `unresolved`;
- no generic score or empirical status exists anywhere in the final payload.

Offline outputs: versioned JSON fixtures with exact hashes and a manifest
recording synthetic origin, generator/validation commands, claim limits, and
current content commit after stabilization.

## Acceptance Criteria

| ID | Criterion | Required evidence | Positive control | Negative control |
|---|---|---|---|---|
| C1 | Controlled packet hashes/anchors/bindings validate | A/test | approved Harbor fixture | wrong hash, bad offset, foreign packet ID |
| C2 | QC remains qualitative and source-traceable | A/test | QC Harbor fixture | PT comparative-support field, missing contrary/support anchor |
| C3 | PT retains rival-comparison semantics | A/test | PT Harbor fixture | missing residual, one hypothesis, truth probability wording |
| C4 | GT-I exposes development without saturation overclaim | A/test | GT-I Harbor fixture | missing comparison provenance, `saturated=true`, full-GT claim |
| C5 | Links are neutral, typed, and target real native objects | A/test | approved four-link set | `supports`, numeric weight, unknown target |
| C6 | Review packet keeps three method views and exact step-down | A/test | assembled approved packet | missing lane, missing native/source reference, generic confidence |
| C7 | CLI/Make surface is agent-drivable and fail-loud | A/test | validate/assemble commands exit 0 | invalid fixture exits nonzero with invariant-specific diagnostic |
| C8 | Fixture provenance and claim limits are exhaustive | A/test | manifest inventory | unlisted file, stale hash, empirical claim escalation |

No criterion may enter `make check` until its positive and negative controls
both execute. A gate failure must assert the intended invariant, not merely any
nonzero exit.

## Implementation Order

1. Add the D-only coverage rows and generate the report; commit.
2. Add package/test skeleton and strict/compatible models; keep gates local.
3. Add the controlled packet and three method fixtures.
4. Add assembly/link validation and final review fixture.
5. Add positive and invariant-specific negative controls.
6. Re-grade only rows supported by executed evidence.
7. Wire calibrated controls into `make check`.
8. Run adversarial audit, disposition findings, clean temporary artifacts,
   update concerns/notebook/handoff, commit and push.

## Failure Recovery

| Failure | Action |
|---|---|
| Pydantic cannot represent an open producer field honestly | Keep it outside the durable contract and add a dependency-subplan readout; do not use `Any`. |
| Approved mockup requires data absent from producer substrate | Mark the view unavailable and revise the contract/mockup before adapter work. |
| Positive control fails because the system is unbuilt | Mark readout invalid; do not score it as product failure. |
| Negative control fails for the wrong reason | Repair test setup until the intended diagnostic is reached before enforcement. |
| Local fixture encourages producer-specific assumptions | Remove the assumption or move it behind an explicit compatible-consumer policy. |

## Verification

Planned commands after authorization:

```bash
make demo-coverage
make validate-demo-fixtures
make validate-demo-controls
make assemble-demo-review
make check
pytest -q
mypy --strict src tests
git diff --check
```

## Stop Conditions

- Brian has not explicitly authorized `DEMO-C1` implementation.
- A required change touches `qualitative_coding` or `process_tracing`.
- A proposed schema would assert fields not evidenced by the producer review.
- The approved mockup must materially change rather than merely be implemented.

