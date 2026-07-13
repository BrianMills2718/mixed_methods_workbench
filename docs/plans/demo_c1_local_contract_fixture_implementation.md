# DEMO-C1: Local Typed Contract and Fixture Implementation

Status: completed locally; producer integration not authorized
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

The approved domain model is implemented in three focused modules:

```text
models.py    packet, strict method, compatible review, link, and manifest contracts
assemble.py  cross-contract validation/linking and review assembly
io.py        typed fixture loading, exhaustive manifest validation, safe output
```

Producer-shaped models use `extra="forbid"`. Workbench-compatible consumer
models use `extra="ignore"` but still reject unsupported major versions and
missing required structural semantics. Open explanatory prose is explicitly
`synthetic_non_authoritative_human_review_required`; programmatic validation
does not pretend to establish its methodological meaning. Every public
module/class/function has a why-focused
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
- QC has no PT inference fields; its open prose is non-authoritative;
- PT has at least two unique rivals, exactly one residual, unique evidence
  references, and a complete non-duplicated ranking; verdict prose is
  non-authoritative;
- GT-I carries exact no-saturation/full-GT limitations, ordered comparison
  provenance, and non-authoritative memo/category prose;
- links use only `addresses`, `challenges`, `contextualizes`, `unresolved`;
- no generic score or empirical status exists anywhere in the final payload.

Offline outputs: versioned JSON fixtures with exact hashes and a manifest
recording synthetic origin, validation commands, exact claim limits, and
content hashes. The enclosing Git commit is the provenance record; the manifest
does not embed a self-referential commit hash.

## Acceptance Criteria

| ID | Criterion | Required evidence | Positive control | Negative control |
|---|---|---|---|---|
| C1 | Controlled packet hashes/anchors/bindings validate | A/test | approved Harbor fixture | wrong hash, bad offset, foreign packet ID |
| C2 | QC structure is method-distinct and source-traceable; prose is non-authoritative | A/test | QC Harbor fixture | PT field, duplicate native ID, missing anchor |
| C3 | PT structure retains a unique rival set, residual, evidence references, ranking, and sensitivity; prose is non-authoritative | A/test | PT Harbor fixture | missing residual, duplicate rival/ranking/reference |
| C4 | GT-I structure exposes ordered development and exact method limits; prose is non-authoritative | A/test | GT-I Harbor fixture | duplicate iteration, `saturated=true`, missing exact limits |
| C5 | Links are cross-method, typed by native object kind, and target real objects; explanatory prose is non-authoritative | A/test | approved four-link set | `supports`, same-method endpoints, wrong kind, unknown target |
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

Verification commands:

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

Observed 2026-07-12:

- all positive controls and invariant-specific negative controls passed;
- strict mypy and Ruff passed;
- CLI/Make validation and JSON assembly passed;
- `make check` passed with the prior 41 fixture controls, 3 coverage controls,
  and the DEMO-C1 controls;
- coverage contains 8 A/test DEMO-C1 rows, limited to synthetic contract
  behavior; overall coverage remains D because real producer/review rows remain
  weak.
- independent re-audit passed exact implementation commit `6a8e0b5` after 41
  repository tests and a separate 37-mutation held-out matrix; decision record:
  `docs/runs/2026-07-12-demo-c1-independent-audit.md`.

## Stop Conditions

- Brian has not explicitly authorized `DEMO-C1` implementation.
- A required change touches `qualitative_coding` or `process_tracing`.
- A proposed schema would assert fields not evidenced by the producer review.
- The approved mockup must materially change rather than merely be implemented.
