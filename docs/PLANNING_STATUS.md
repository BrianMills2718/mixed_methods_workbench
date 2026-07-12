# Current Planning Status

Status: canonical current-phase and authorization guide
Updated: 2026-07-12

## Current Phase: DEMO-C1 Complete; No Active Implementation Slice

The current task is to clarify and reconcile the project's strategy,
methodological scope, architecture, dependencies, version order, decisions, and
open questions so future implementation can begin from a coherent plan.

No product implementation phase, numbered release, or local implementation
slice is active. No engine integration, adapter, API, UI, schema migration, or
upstream-engine task is authorized by these documents alone. The completed
`T0-PROV` evidence does not authorize another T0 item.

Brian's 2026-07-12 “proceed,” given directly after the exact `DEMO-C1`
authorization request, authorized the local fixture implementation documented
in `docs/plans/demo_c1_local_contract_fixture_implementation.md`. It is
complete: typed synthetic QC/PT/GT-I contracts, assembly, CLI/Make surfaces,
fixture provenance, and both-sign controls are present. Producer repositories,
live runs, API/UI, final-corpus selection, and later capabilities remain
separately authorized.

## Completed Authorization: T0-PROV

The user supplied the prior handoff, including the exact next action:

> “close the T0 provenance-complete fixture inventory gap without starting
> engine integration.”

The user's current instruction then said exactly:

> “please inveistgae and set up clear long term plans then proceed until the
> mixed method work bench is sota or beyond in all areas”

The handoff alone is not authority. The direct phrase “then proceed,” applied to
the supplied named next action, authorizes the local T0 provenance-inventory
subslice after investigation and planning. The canonical authorization record,
scope, evidence target, and failure modes are in
`docs/plans/current_t0_truthful_fixture_inventory.md`.

The bounded slice was independently signed off at evaluated commit
`f26bc6ade93c475c7ebc4ca608e796a9b9fe2f1a`; the decision record is
`docs/runs/2026-07-12-t0-prov-eval-signoff.md`. W2 inventory provenance is
A/test, while fixture contents remain C and broader T0 remains partial/F.

This completed exception does **not** close or authorize all of T0/0.0. It does
not permit producer-repository changes, real exports, production schemas,
adapters, UI, APIs, evaluation machinery, a 0.1 case, or a SOTA claim. Every
later slice still requires separate named authorization.

Current work may:

- clarify the north star and what the product must eventually cover;
- reconcile conflicting or stale planning documents;
- describe future release order and dependencies;
- record architectural decisions, contract sketches, risks, and unresolved
  decisions;
- make the documentation legible to a future implementing agent and to a
  non-coding reviewer.

Brian's 2026-07-12 direction authorized a documentation-only reconciliation of
the long-term capability order. ADR 0004 now makes the controlled QC/PT/GT
demonstration the first future functional slice, defers final corpus selection
until after that demonstration, assigns OntoCanon and DIGIMON optional
infrastructure roles, and places source-backed theory recommendation before
Theory Forge's formalize/compile/run workflow. This changes future sequencing;
it does not activate any implementation slice.

Current work must not:

- start any other version 0.0 work, version 0.1, or a later implementation
  slice;
- modify `qualitative_coding`, `process_tracing`, `grounded-research`,
  `theory-forge`, or another dependency for this workbench;
- build adapters, production schemas, orchestration, APIs, UI, evaluation
  machinery, or live research pipelines;
- interpret a roadmap sequence, acceptance criterion, or “future next step” as
  authorization to execute it.

Any further implementation begins only after Brian explicitly authorizes a
named slice or asks to move that slice from planning into implementation. At
that point, the first action is a fresh state review: confirm upstream status,
revisit open decisions, turn the selected future slice into a current
implementation plan, and record its acceptance evidence.

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
| `docs/adr/0004_demo_first_method_core_and_knowledge_infrastructure.md` | Why is the program now demo-first, and what do OntoCanon, DIGIMON, theory recommendation, and Theory Forge own? | Canonical architecture/order decision; not implementation authority. |
| `docs/MIXED_METHODS_CAPABILITY_MAP.md` | What must the eventual product cover? | Canonical scope inventory. |
| `docs/ROADMAP.md` | In what future release order should that scope be pursued? | Canonical future sequence, not an active schedule. |
| `docs/CAPABILITY_DEPENDENCY_GRAPH.md` | What must be true before later capabilities may become product claims? | Canonical sequencing and claim-licensing aid, not an active task list. |
| `docs/PRE_IMPLEMENTATION_CHECKLIST.md` | What must be checked after Brian authorizes a named implementation slice? | Canonical future entry gate; not authorization by itself. |
| `docs/plans/003_integration_versioning_and_clean_state.md` | What would the first future implementation phases require? | Detailed future blueprint; not authorized. |
| `docs/ARCHITECTURE.md` | What does the initial QC/PT concept look like? | Preliminary architecture, subject to revalidation. |
| `contracts/shared_contracts.md` | What might cross-engine artifacts contain? | Contract sketch only, not a production schema. |
| `docs/CONCERNS.md` | What risks and unresolved decisions must remain visible? | Live planning concern register. |
| `docs/coverage_report.md` | What does the existing synthetic scaffold actually prove? | Evidence baseline only. |
| `docs/SOTA_EVIDENCE_SCORECARD.md` | What external floors and proof would license bounded SOTA claims? | Current visibility artifact, not an enforcement gate. |
| `plan/goals/2026-07-12-sota-or-beyond.md` | What long-term outcomes, dependencies, and completion conditions govern the program? | Active long-term goal map; it does not authorize later rows. |
| `docs/decisions/2026-07-12-first-governed-case.md` | What case/source-use options and evidence should Brian decide? | Source-backed decision brief; recommendation only, not a selected case or GOV authorization. |
| `docs/decisions/2026-07-12-first-quantitative-text-strand.md` | What first QT task/owner pattern should Brian decide? | Source-backed decision brief; recommendation only, not a construct, owner assignment, or QT authorization. |
| `docs/plans/current_t0_truthful_fixture_inventory.md` | What did the bounded T0 provenance slice require and prove? | Completed implementation/evidence record; no longer active authority. |
| `docs/plans/current_demo_method_core.md` | What did the authorized DEMO planning slice specify and what blocks implementation? | Approved local journey; `DEMO-C1` and producer work remain separately authorized. |
| `docs/plans/demo_c1_local_contract_fixture_implementation.md` | What did the local typed-contract/fixture slice implement and prove? | Completed DEMO-C1 record; synthetic contract claims only. |
| `docs/demo_c1_coverage_baseline.md` | What DEMO-C1 requirements have evidence before enforcement? | Visibility baseline: 8 D/doc, no enforced gates. |
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
> `docs/PRE_IMPLEMENTATION_CHECKLIST.md`;
> `docs/decisions/2026-07-12-first-governed-case.md`;
> `docs/decisions/2026-07-12-first-quantitative-text-strand.md`;
> `docs/MIXED_METHODS_CAPABILITY_MAP.md`; `docs/ROADMAP.md`;
> `docs/adr/0001_method_engines_not_monorepo.md`;
> `docs/adr/0002_broad_north_star_versioned_thin_slices.md`;
> `docs/adr/0003_mixed_methods_minimum_and_optional_enhancers.md`;
> `docs/SOTA_EVIDENCE_SCORECARD.md`;
> `docs/coverage_report.md`; `docs/plans/001_walking_skeleton.md`;
> `docs/plans/002_engine_stability_and_integration_readiness.md`;
> `docs/plans/003_integration_versioning_and_clean_state.md`;
> `plan/goals/2026-07-12-sota-or-beyond.md`;
> `~/projects/investigations/mixed_methods_workbench/2026-07-12-sota-program-baseline.md`;
> `docs/wiki_manifest.yaml`;
> `examples/fixtures/workbench_contract_v1/README.md`;
> `examples/integration_payload_mockup.md`.
> `docs/coverage_report.json` and the JSON files under
> `examples/fixtures/workbench_contract_v1/` were not consulted because they are
> machine-readable mirrors/fixtures and contain no additional planning-authority
> statements.
>
> Status: current-phase clarification requested by Brian on 2026-07-09,
> extended with claim-licensing controls on 2026-07-10, and updated with the
> exact `T0-PROV` authorization boundary and independent closure on 2026-07-12.
