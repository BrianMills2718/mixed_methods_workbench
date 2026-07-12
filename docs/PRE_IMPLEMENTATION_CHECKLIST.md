# Pre-Implementation Checklist

Status: canonical future entry gate; documentation only
Updated: 2026-07-12

## Purpose

Use this checklist only after Brian explicitly authorizes a named implementation
slice. It converts that authorization into a current, evidence-graded
implementation plan before any code, adapter, schema, API, UI, upstream-engine
change, or live research pipeline starts.

If there is no named slice authorization, stop at planning documentation. The
roadmap, capability graph, and planning files are not enough by themselves.

## Required Inputs

Record these before doing any implementation work:

- Brian's exact authorization text;
- target product release or dependency slice, if named;
- target capability row from `docs/CAPABILITY_DEPENDENCY_GRAPH.md`;
- relevant roadmap or plan section;
- repos in scope and explicitly out of scope;
- expected claim after the slice passes;
- required evidence grade and verification artifact.

Minimal authorization record:

```yaml
authorized_slice:
  instruction: "<Brian's exact words>"
  target_capability_row: "<row id from docs/CAPABILITY_DEPENDENCY_GRAPH.md>"
  target_release_or_dependency: "<0.0, 0.1, QT, etc.>"
  in_scope: []
  out_of_scope: []
  claim_to_license: ""
  required_evidence_grade: ""
```

## Entry Gate

Do these in order. A failed item is a stop point unless the current slice is
explicitly a dependency-resolution slice for that item.

| Step | Required check | Pass condition | If it fails |
|---|---|---|---|
| 1 | Authorization boundary | Exact user instruction names the slice or asks to move from planning into implementation. | Stop; keep work documentation-only. |
| 2 | Current repo state | `mixed_methods_workbench` has recorded branch, HEAD, upstream, clean/dirty state, and active coordination claims. | Record the blocker; do not build on ambiguous state. |
| 3 | Authority order | ADR 0004, `docs/PLANNING_STATUS.md`, `docs/ROADMAP.md`, `docs/CAPABILITY_DEPENDENCY_GRAPH.md`, this checklist, and the relevant plan do not conflict. | Fix docs first or mark stale material superseded. |
| 4 | Capability dependency row | The selected row and all dependency rows have current evidence, success criteria, verification artifact, and claim licensed. | Create a dependency-resolution plan instead of implementing downstream work. |
| 5 | Upstream freshness | Every producer repo in scope has current status, active-claim check, relevant plan/doc review, verification command result, and commit recorded. | Repair or plan in the owning repo; do not consume stale evidence. |
| 6 | Evidence baseline | `make check`, `make coverage`, and relevant manifest/check commands have been run or explicitly marked unavailable with reason. | Do not promote evidence grades or enforce gates. |
| 7 | Scope and non-goals | The current slice says what it will not touch, including upstream repos, engine internals, UI, schemas, or SOTA claims where out of scope. | Narrow the slice before implementation. |
| 8 | Modality split | Deductive parts have acceptance tests; exploratory parts have instruments and readouts; hybrid parts state both. | Rewrite the plan; do not fake thresholds. |
| 9 | Contracts and data flow | Inputs, outputs, failure semantics, artifact versions, hashes, and claim limits are named before coding. | Add a contract mockup or dependency subplan first. |
| 10 | Negative controls | Every criterion promoted to a hard gate has at least one invariant-specific negative control. | Keep it visible as a coverage row, not an enforced gate. |
| 11 | Review and cleanup plan | Done-when includes adversarial audit, finding disposition, concern-register triage, docs update, and clean git state. | Slice is not ready to start. |

## Current Plan Artifact

Before implementation, create or update a current implementation plan that is
separate from future proposals. It must include:

- mission and one-sentence outcome;
- target capability row and dependencies;
- current evidence grades and what would upgrade them;
- exact in-scope files/repos and out-of-scope work;
- acceptance criteria with evidence class and required grade;
- failure modes and what to try next;
- typed contract or mockup inputs/outputs;
- commands to run and expected artifacts;
- adversarial audit checklist;
- cleanup and commit/push requirements;
- stop conditions requiring Brian's decision.

Suggested location:

```text
docs/plans/current_<short_slice_name>.md
```

Do not edit `docs/plans/001_walking_skeleton.md` or
`docs/plans/003_integration_versioning_and_clean_state.md` into active plans.
Those remain future/historical planning artifacts.

## Stop Conditions

Stop and ask Brian before proceeding if:

- the requested slice is not named clearly enough to map to a capability row;
- a dependency row is blocked and the user did not authorize resolving it;
- the work would mutate an upstream engine repo without that repo being in
  scope;
- the slice would require choosing the first public case, quantitative-text
  owner, Theory Forge export, Grounded Research role, or SOTA benchmark design
  and that choice is not already authorized by the current plan;
- a planned release claim would outrun the evidence grade;
- the only available data is synthetic but the slice needs real research
  evidence;
- the implementation would depend on producer internals instead of versioned
  exports;
- the worktree contains overlapping uncommitted changes that cannot be safely
  separated.

## Default Next Slice Logic

When authorization names a release rather than a concrete task, choose the next
slice by dependency truth:

1. If `AUTH` or planning authority is unclear, repair documentation only.
2. If `T0` is incomplete, start with truth/clean-state recovery.
3. If the method-core demo is requested, resolve `DEMO`, `QC-D`, `PT-D`, and
   `GT-D` in dependency order. The demonstration packet may be synthetic or
   rights-clear and licenses software behavior only.
4. Do not make final corpus selection a demo entry gate. Require `GOV` before
   `CORE-V` or any empirical/method-validity claim.
5. If `MM` is requested, do not start until `CORE-V` and `QT` are satisfied.
   Require Grounded Research only when adjudication is claimed. A minimal MM
   design need not use Theory Forge, while the current full-product sequence
   includes `TREC`, `TF-SPEC`, and `TF-RUN`; see ADRs 0003 and 0004.
6. If a SOTA or beyond-SOTA claim is requested, refresh external SOTA and
   incumbent baselines before designing the benchmark.

## Sources Consulted

> Sources: `README.md`; `PROJECT.md`; `CLAUDE.md`;
> `docs/PLANNING_STATUS.md`; `docs/ROADMAP.md`;
> `docs/CAPABILITY_DEPENDENCY_GRAPH.md`;
> `docs/MIXED_METHODS_CAPABILITY_MAP.md`; `docs/CONCERNS.md`;
> `docs/ARCHITECTURE.md`; `docs/IMPLEMENTING_AGENT_NOTES.md`;
> `docs/coverage_report.md`;
> `docs/adr/0001_method_engines_not_monorepo.md`;
> `docs/adr/0002_broad_north_star_versioned_thin_slices.md`;
> `docs/adr/0003_mixed_methods_minimum_and_optional_enhancers.md`;
> `docs/plans/001_walking_skeleton.md`;
> `docs/plans/002_engine_stability_and_integration_readiness.md`;
> `docs/plans/003_integration_versioning_and_clean_state.md`;
> `contracts/shared_contracts.md`;
> `examples/integration_payload_mockup.md`;
> `examples/fixtures/workbench_contract_v1/README.md`;
> `docs/wiki_manifest.yaml`;
> `~/projects/investigations/mixed_methods_workbench/2026-07-12-sota-program-baseline.md`.
>
> Not consulted: JSON fixture files and generated JSON coverage, because this
> checklist is an authorization and planning-control document rather than a
> schema or fixture review.
