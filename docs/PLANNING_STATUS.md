# Current Planning Status

Status: canonical current-phase guide
Updated: 2026-07-10

## Current Phase: Documentation Only

The current task is to clarify and reconcile the project's strategy,
methodological scope, architecture, dependencies, version order, decisions, and
open questions so future implementation can begin from a coherent plan.

No product implementation phase is active. No numbered version, engine-integration
slice, adapter, API, UI, schema migration, or upstream-engine task is authorized
for execution by these documents alone.

Current work may:

- clarify the north star and what the product must eventually cover;
- reconcile conflicting or stale planning documents;
- describe future release order and dependencies;
- record architectural decisions, contract sketches, risks, and unresolved
  decisions;
- make the documentation legible to a future implementing agent and to a
  non-coding reviewer.

Current work must not:

- start version 0.0, 0.1, or any later implementation slice;
- modify `qualitative_coding`, `process_tracing`, `grounded-research`,
  `theory-forge`, or another dependency for this workbench;
- build adapters, production schemas, orchestration, APIs, UI, evaluation
  machinery, or live research pipelines;
- interpret a roadmap sequence, acceptance criterion, or “future next step” as
  authorization to execute it.

Implementation begins only after Brian explicitly authorizes a named slice or
asks to move from planning into implementation. At that point, the first action
is a fresh state review: confirm upstream status, revisit open decisions, turn
the selected future slice into a current implementation plan, and record its
acceptance evidence.

## What “Plan 003” Means

`docs/plans/003_integration_versioning_and_clean_state.md` is simply the third
planning artifact created in this repository. The number is historical filing,
not a version number, command, priority signal, or authorization boundary.

Its plain-language role is **Detailed Future Integration and Versioning
Blueprint**. It records what implementation could eventually do and in what
order. It is not a current task list.

## How the Documents Fit Together

| Document | Question it answers | Current authority |
|---|---|---|
| `PROJECT.md` | Why should this project exist? | Canonical product thesis. |
| `docs/PLANNING_STATUS.md` | What work is authorized now? | Canonical current-phase boundary. |
| `docs/MIXED_METHODS_CAPABILITY_MAP.md` | What must the eventual product cover? | Canonical scope inventory. |
| `docs/ROADMAP.md` | In what future release order should that scope be pursued? | Canonical future sequence, not an active schedule. |
| `docs/CAPABILITY_DEPENDENCY_GRAPH.md` | What must be true before later capabilities may become product claims? | Canonical sequencing and claim-licensing aid, not an active task list. |
| `docs/plans/003_integration_versioning_and_clean_state.md` | What would the first future implementation phases require? | Detailed future blueprint; not authorized. |
| `docs/ARCHITECTURE.md` | What does the initial QC/PT concept look like? | Preliminary architecture, subject to revalidation. |
| `contracts/shared_contracts.md` | What might cross-engine artifacts contain? | Contract sketch only, not a production schema. |
| `docs/CONCERNS.md` | What risks and unresolved decisions must remain visible? | Live planning concern register. |
| `docs/coverage_report.md` | What does the existing synthetic scaffold actually prove? | Evidence baseline only. |
| `docs/plans/001_walking_skeleton.md` | What was the original first-slice proposal? | Future proposal, not authorized. |
| `docs/plans/002_engine_stability_and_integration_readiness.md` | What did the June 2026 dependency review find? | Historical evidence, not current state. |

## Planning Completion Condition

The documentation phase is ready for Brian's review when:

- the north star and full capability scope are understandable;
- the future release/dependency order is explicit;
- current facts, future proposals, and unresolved decisions are visibly
  distinct;
- no planning document implies that implementation is underway or authorized;
- a future implementing agent can identify the required fresh-state review and
  the decisions that must be confirmed before coding.

Planning readiness does not mean implementation readiness.

## Sources Consulted

> Sources: `README.md`; `PROJECT.md`; `CLAUDE.md`;
> `contracts/shared_contracts.md`; `docs/ARCHITECTURE.md`;
> `docs/CONCERNS.md`; `docs/IMPLEMENTING_AGENT_NOTES.md`;
> `docs/CAPABILITY_DEPENDENCY_GRAPH.md`;
> `docs/MIXED_METHODS_CAPABILITY_MAP.md`; `docs/ROADMAP.md`;
> `docs/adr/0001_method_engines_not_monorepo.md`;
> `docs/adr/0002_broad_north_star_versioned_thin_slices.md`;
> `docs/coverage_report.md`; `docs/plans/001_walking_skeleton.md`;
> `docs/plans/002_engine_stability_and_integration_readiness.md`;
> `docs/plans/003_integration_versioning_and_clean_state.md`;
> `docs/wiki_manifest.yaml`;
> `examples/fixtures/workbench_contract_v1/README.md`;
> `examples/integration_payload_mockup.md`.
> `docs/coverage_report.json` and the JSON files under
> `examples/fixtures/workbench_contract_v1/` were not consulted because they are
> machine-readable mirrors/fixtures and contain no additional planning-authority
> statements.
>
> Status: current-phase clarification requested by Brian on 2026-07-09 and
> extended with a claim-licensing dependency graph on 2026-07-10.
