# Current Planning Status

Status: canonical current-phase and authorization guide
Updated: 2026-08-13; correction note added 2026-09-06; bounded portfolio note added 2026-09-23; NYC pause added 2026-10-04

## NYC lane paused (2026-10-04)

> **NYC lane paused — Brian, 2026-10-04.** Do not continue `NYC-MVP-REVIEW-1`
> or extend the NYC vertical. Brian's personal plan
> (`weekly-plans/personal/THIS_WEEK.md`, Priority 1) records that he did not
> knowingly choose NYC as the use case ("not sure he had decided it, or at least
> not on purpose"). A 2026-10-04 review of the pinned Qualitative Coding result
> found its evidence is single printed transcript lines (72 quotes averaging 49
> characters) with no speaker attribution, and its 14 findings carry one
> blanket approval rather than item-level review; treat it as unreviewed.
> Qualitative Coding is speed-running its grounded-theory finish instead (its
> `docs/CURRENT_STATE_AND_ROADMAP.md`, "Speed-run to finish"). The Path A text
> below is the earlier record.

## Bounded PsychosisBank portfolio demonstration (2026-09-23)

Brian separately authorized an independent second-model check of the existing
Open Science → Qualitative Coding → Process Tracing PsychosisBank demonstration.
The Workbench retains one source-bound, advisory challenge in
`examples/fixtures/investigation_spine/independent_verification.json` and
shows each finding's verdict, cited excerpts, and remaining source gap on the
existing review page. The retained result remains inconclusive and blocked
from publication. The second model saw selected excerpts, not full documents;
its output remains pending researcher review and does not alter any
method-owned finding or create a reusable adjudication capability. This
portfolio demonstration does not change the NYC Path A critical path below.
On 2026-09-23, the three public source URLs returned bytes matching all three
frozen source digests in `independent_case_sources.json`. A source-context audit
found that the selected quote for Finding 3 omits the antecedent of “this
level”; the exact-hash TalkBank policy names it “Controlled access.” The page
links each cited excerpt to its original source and states this distinction.

Brian then authorized one connected run. The reviewed QC P5 theory input was
reused; no new QC analysis or review was performed. Native Process Tracing ran
twice against the frozen three-source corpus. Its frozen-rivals route stopped
at the rival-partition audit. Its theory-first route passed that audit but
stopped at the terminal central-claim review because generated claims included
unsupported funding attribution and sequence language. The supported public
`pt_export_v2` is retained with the blocked native result, audit artifacts,
exact input bytes, trace IDs, and a fresh Gemini 3.1 Pro challenge in
`examples/runs/psychosisbank-synthesis-20260923/`. The challenge is advisory.
The Investigation Spine presents both stops, the diagnostic comparison,
source-linked challenge excerpts, and the pending researcher review boundary.
No causal conclusion is ready for publication. This bounded portfolio run does
not change the NYC Path A critical path.

## Current Phase: Finish the NYC vertical (Path A, approved 2026-09-06)

Brian approved Path A of `docs/runs/2026-09-06-state-assessment-and-next-agent-brief.md` on
2026-09-06: execute `NYC-QC-1` on `qualitative_coding` branch
`nyc-crz-six-hearing-qc`, hand its artifact to Brian for acceptance, then
`NYC-INTEGRATE-1` and `NYC-MVP-REVIEW-1`. The capability-architecture phases
below (A–D) resume afterwards; they are not the current critical path. The
section that follows is retained as the 2026-08-13 wording it replaces.

## Prior Phase (2026-08-13): Capability Architecture and Adoption Gate

Brian approved the first-principles initiative reset recorded in
[`SYSTEM_GOAL_AND_CAPABILITY_ARCHITECTURE.md`](SYSTEM_GOAL_AND_CAPABILITY_ARCHITECTURE.md).
The evidence-backed current inventory and reuse decisions are in
[`CAPABILITY_ADOPTION_MAP.md`](CAPABILITY_ADOPTION_MAP.md).

The immediate sequence is:

1. reconcile current capability owners, callable seams, and authentic consumer
   evidence, including Data Contracts, `llm_client`, Open Web Retrieval, QC,
   Process Tracing, Theory Forge, Grounded Research, OntoCanon, DIGIMON, SB
   Ontologies, and any governed computational-social-science owner;
2. preserve the distinction among generic execution forms, reusable research
   primitives, method-owned protocols, and study workflows;
3. freeze a Project Meta-subordinate method-operation composition and complete
   evidence-round-trip profile rather than creating a competing Workbench
   ecosystem architecture;
4. prepare the narrow Workbench consumer design for
   `ExtractStructuredCandidates`; and
5. only after that design is adopted, refactor the existing NYC extraction as
   its first authentic consumer.

Current work may update architecture, capability/adoption evidence, roadmap,
and the exact next bounded design. It may not implement the extraction action,
modify producer repositories, promote a Workbench-local contract into Data
Contracts, or start another policy vertical without a separately adopted
implementation packet.

The former Plan #6 candidate at
`origin/capability-kernel-design-candidate@f64b613c` remains useful donor
material, but it is not adopted unchanged. Its exact-reference, guarded-action,
review-authority, and consumer-runtime concepts require crosswalk to existing
Project Meta, Data Contracts, OntoCanon, DIGIMON, and method-owner authority.

The Phase 1 compact-versus-independent 70/90-operation disagreement remains
supporting research evidence. It must not be resolved merely by assigning both
inventories to the same generic execution label.

## NYC Candidate: Current State (updated 2026-09-24)

**Brian's decision boundary is already resolved, twice.** On 2026-08-14 he
accepted all three review statements (`docs/research/nyc_crz_human_disposition.json`
at commit `c95488c`: the agency-prediction wording, the hearing-concern wording,
and the bounded quantitative comparison), which marked `NYC-QC-1` ready. On
2026-09-06 he chose Path A: finish `NYC-QC-1`, `NYC-INTEGRATE-1`, and
`NYC-MVP-REVIEW-1` before the shared-action refactor. Neither of those is an
open question. Do not re-ask Brian to review the three statements or re-decide
the path; both already happened.

**What is actually blocking progress is stalled implementation, not a pending
decision.** The QC-side lane on `qualitative_coding` branch
`nyc-crz-six-hearing-qc` has 24 real commits (corpus receipt, source-unit
receipt, medical-access canary receipt, coverage-stability check) but stopped
mid-review on 2026-09-14 in a `paused_for_review` state, was never merged, has
no PR, and its coordination claim expired 2026-09-15 with no follow-up
(surfaced 2026-09-24; see `project-meta` issue #2155 for why the stale-claim
detector didn't catch this). The worktree is also now behind `main` and needs
reconciling before the QC review can resume.

Two other Plan #5 units are merged on canonical `main` and technically
complete, but do **not** themselves constitute analytical acceptance (passing
Pydantic/anchor/arithmetic/browser/runtime checks is not acceptance):

- `NYC-EXTRACT-1` at `6403fcf` — verifies exact Reevaluation 2 and hearing PDF
  bytes, binds one prediction and one hearing concern to exact source units.
- `NYC-QUANT-1` at `103be94` — recomputes 12 monthly observations from the
  frozen 25,992-row vehicle-entry snapshot and compares against the agency's
  No Action baseline. Binds the canonical drift-receipt digest
  `0961133cc6a6441a944f00a45a7574e58a69bd0ca51fc2cb70da67540083f578`
  (an earlier `5c6af2bd...` value was wrong provenance, now corrected).

**Current NYC critical path (2026-10-02):** `NYC-QC-1` is complete and
human-approved at Qualitative Coding revision
`5560ce71546a30dc6aa4a264dacbce3028b005eb`. Workbench pins the method
handoff and approved analyst review by exact SHA-256 under
`examples/fixtures/nyc_crz_integrated/`. `NYC-INTEGRATE-1` now exposes the
accepted qualitative result beside the extraction baseline and quantitative
audit on the existing NYC route, with explicit convergence, complementarity,
divergence, and silence records. The policy appraisal intentionally remains
`needs_human_priorities`; integration does not invent retain/change/monitor
weights or a recommendation.

The next decision boundary is `NYC-MVP-REVIEW-1`: review the integrated
investigation and decide whether to accept the MVP presentation and whether to
supply explicit policy-appraisal priorities. See
`docs/runs/2026-10-02-nyc-integrate-1.md` for the baseline-vs-federated
comparison and verification boundary.

<details>
<summary>History (superseded 2026-09-06/2026-09-14/2026-09-24 — kept for provenance, not current status)</summary>

The section below was written 2026-08-13, before the 2026-08-14 acceptance and
2026-09-06 Path A decision described above. It is retained verbatim as a
record of what the plan looked like at that point; do not read it as current.

> Plan #5 remains preserved at
> [`005_nyc_crz_mvp.md`](plans/005_nyc_crz_mvp.md) and its machine-consumed
> [`5_nyc_crz_mvp_work_graph.json`](plans/5_nyc_crz_mvp_work_graph.json), but
> it is paused while the capability architecture and adoption gate controls.
> The remaining Plan #5 decision boundary is Brian's attributable disposition
> of three review statements... `NYC-QC-1` remains blocked until the
> extraction semantics and reviewed fields are accepted. `NYC-INTEGRATE-1`
> remains blocked until extraction, QC, and quantitative artifacts are
> accepted.

The 2026-09-06 assessment that first flagged this contradiction is
`docs/runs/2026-09-06-state-assessment-and-next-agent-brief.md`. The Plan 242
guarded-decision seam (`src/mixed_methods_workbench/guarded_decision/`,
evidence under `research/plan242/`) also exists and is not reflected above.

</details>

## Completed Phase: Product Integration Assessment

On 2026-08-13 Brian raised the concern that independently developed QC,
Process Tracing, theory, simulation, and method-catalog work might not converge
into one cohesive product. He then approved a repository-grounded integration
assessment and a shift of the immediate critical path away from broad method
decomposition.

The controlling assessment is
[`EVIDENCE_TO_ACTION_PRODUCT_INTEGRATION_MAP.md`](EVIDENCE_TO_ACTION_PRODUCT_INTEGRATION_MAP.md).
It assigns the Workbench an investigation spine and unified user journey while
keeping analytical judgments and validity rules in their method-owned engines.

Current work may:

- verify current producer capabilities and exact cross-project seams;
- define the smallest Workbench-owned investigation, artifact-reference,
  derivation, review-state, and open-question mechanics;
- select and source-check one understandable policy-analysis flagship;
- preserve completed Phase 3 research batches as supporting evidence; and
- preserve the named Investigation Spine implementation contract and its
  product boundary.

Current work must not:

- resume broad Phase 3 decomposition, collision analysis, or capability
  promotion as the product critical path;
- implement a shared schema, generic adapter framework, or producer migration;
- rerun QC, Process Tracing, Theory Forge, or simulation analyses merely to
  populate the Workbench;
- treat the Open Science/P5 example as the general policy-analysis flagship;
  or
- infer authorization for any implementation beyond the separately approved
  Investigation Spine.

## Supporting Phase: Phase 3 Portfolio Decomposition (completed 2026-10-08)

Phase 3 completed 2026-10-08: all three lanes were reviewed, corrected and accepted with receipts (`lane_receipts/`), and `P3-INTEGRATE` validated all 14 decompositions (`integration_report.md`, `validation_report.json`, `portfolio_manifest.yaml`; 14 of 14 pass). This establishes 14 source-frozen, structurally valid decompositions only: no collision, adjudication, coverage or reusable-capability claim.

Brian lifted the Phase 3 pause on 2026-10-08 (observation-to-action-metamodel `ROADMAP_AGENT_MODEL.md` row 5a): the pause waited behind the NYC product-integration lane, which he paused on 2026-10-04 (PR #41), and on 2026-10-07 he approved the cross-method crosswalk that reads the integrated 14. The paragraphs below record the paused state as it stood on 2026-08-13.


Brian approved the 14-method Phase 3 denominator on 2026-08-13. The exact
denominator is `phase2b-proposal-0.3` (`P01`–`P13`) plus the separately named,
non-substitutable theory-testing Process Tracing variant (`P14`). The canonical
coordination identity is Plan #4. Its lane boundaries are in
[`4_phase3_portfolio_decomposition.md`](research/method_decomposition/phase3/4_phase3_portfolio_decomposition.md)
and its machine-consumed graph is
[`4_phase3_portfolio_decomposition_work_graph.json`](research/method_decomposition/phase3/4_phase3_portfolio_decomposition_work_graph.json).

Phase 3 is documentation-only method research: freeze the exact variant and
authoritative sources, then produce three-level records, typed connections, and
explicit uncertainty accounting for all 14 methods. It does not authorize
Phase 4 collision candidates, Phase 5 adjudication, Phase 6 coverage or
automation claims, a shared production schema, infrastructure, producer
changes, or product implementation.

The four former Phase 3 Codex sessions were consolidated into the current
Workbench coordinator on 2026-08-13. Their claims and worktrees are closed;
their unmerged work remains recoverable at exact pushed refs:

- `P3-RESEARCH-A`: `origin/phase3-research-a` at
  `6262b4da513d2a3e5dd094c47a9284c12572603c`, independently reviewed `PASS`
  and retained in `completion_review`, not accepted;
- `P3-RESEARCH-B`: `origin/phase3-research-b` at
  `f8044648075468411d20bee1bfe71fec5c2023bf`, retained as
  `changes_requested` with its exact correction instructions; and
- `P3-RESEARCH-C`: `origin/phase3-research-c` at
  `0fd05c25f54f8acdbf54689aef4aaf3c0661a7aa`, independently re-reviewed
  `PASS` and retained in `completion_review`, not accepted.

The superseded `P3-CONTROL` session is also closed. Plan #4 graph revision 4
binds these submitted revisions and makes every Phase 3 lane non-claimable
while the product-integration pause remains active. No receipt, acceptance,
integration, or methodological promotion follows from consolidation. An
explicit decision to lift the pause must first make `P3-CONTROL` available;
only that control unit may then review exact evidence, issue later receipts,
and advance lifecycle state.

The approved denominator and completed research checkpoints remain valid.
Additional lane execution and integration are paused until the product
integration assessment and first visible Investigation Spine determine which
method-decomposition questions are actually decision-relevant.

The Process Tracing topology prototype merged at `1fd01bc`; its product lane is
complete. That pinned revision is read-only implementation evidence for `P14`:
it does not own the method frame or count as a completed Phase 3 decomposition.

## Prior Phase: Method-Capability Discovery; Phase 0 Reconciled

The code-derived Phase 0 candidate is merged at `c3d31aac`. It records four
observed systems, five primary analytic variants, and six workflow graphs as 77
source-linked steps: 67 executable, eight represented manual, and two
incomplete. This is accepted as bounded research evidence about the inspected
implementations, not as an adopted universal capability model.

The separately produced candidate was corrected, its drifted Process Tracing
claims were reverified at `4450d2e`, and the controlled comparison is recorded
in
[`docs/research/method_decomposition/comparison_v0.md`](research/method_decomposition/comparison_v0.md).
The comparison found a plausible small shared shell for identity, custody,
typed boundaries, validation, review state, lineage, refusal, and projection;
analytic judgments and workflow topology remain method-owned. This is planning
guidance, not schema adoption.

The workbench may now continue method-capability discovery and catalog work,
but it must not normalize the RAND catalog into a canonical ontology,
generalize a shared schema from labels, or add a capability merely to increase
coverage. A shared capability requires two authentic compatible
producer/consumer seams. The three evidence mismatches in the comparison are
replayed only when a near-term decision depends on them.

This phase is documentation and research only. It does not authorize product
code, producer changes, adapters, schema adoption, or another evaluation run.

## Completed Exception: Simulation Result to Policy Appraisal

Brian explicitly approved the bounded stress test in
[`current_simulation_to_policy_appraisal_probe.md`](plans/current_simulation_to_policy_appraisal_probe.md)
on 2026-08-13. The Workbench now consumes a pinned projection of three
authentic Cybernetic Influence simulation runs and presents the comparison as
model-generated input to a policy appraisal. The result deliberately refuses
to recommend adoption: it licenses only investigation of the modeled verified
allocation package and names the real-world evidence still required.

This exception changed only the Workbench consumer. It did not modify or adopt
a Cybernetic Influence contract, treat simulation output as observed evidence,
generalize a shared schema, deploy the interface, or authorize another product
slice. The implementation and source-check evidence are recorded in
[`simulation_to_policy_appraisal_receipt.md`](plans/simulation_to_policy_appraisal_receipt.md).

## Prior Phase: MT-D1 Mist Trail Decision Review Implemented; Review Pending

Brian authorized the bounded implementation in
[`mist_trail_policy_decision_vertical.md`](plans/mist_trail_policy_decision_vertical.md)
on 2026-08-12. `MT-D1` adds one manually reviewed, hash-bound A/B/C policy
appraisal to the existing Method Dashboard service. Its typed packet, matching
JSON route, and plain-language browser view separate source consequences from
demonstrative human priorities and end in a value-sensitive, evidence-limited
conditional result.

This remains a development fixture. It is not an NPS decision, legal/NEPA
analysis, formal public comment, generic decision engine, shared contract, or
evidence that the selected option is empirically best. The official PDF bytes
are not committed, so exact passage text remains unavailable; reviewed source
summaries and page/section locators are shown instead.

## Prior Phase: METHOD-DASH-C2 Implemented; Re-review Pending

Brian's first review of `METHOD-DASH-C1` found that the primary form required
too much methodological knowledge. The implemented bounded correction is
[`method_dash_c2_plain_language.md`](plans/method_dash_c2_plain_language.md).
It changed user-facing labels, explanations, accessible optional tooltips, and
result language while preserving the typed brief and routing behavior. It did
not expand the method catalog, alter method-selection rules, invoke producer
engines, or claim validated stakeholder comprehension.

## Prior Phase: METHOD-DASH-C1 Implemented; Local Review Pending

Brian's 2026-08-12 approval explicitly authorized a bounded dashboard-shaped
methodology increment. The active slice is
[`method_dash_c1.md`](plans/method_dash_c1.md): a local question-first study
planner over the reviewed analytic-method atlas and think-tank research spine.

This slice added typed method profiles, transparent route construction, a local
browser surface, matching JSON operations, focused tests, and exact run/review
instructions inside this repository. It does not call or modify producer
engines, adopt a universal method ontology, create a shared production
contract, deploy a service, or claim automated substantive method selection.

This section supersedes the older blanket documentation-only pause only for
`METHOD-DASH-C1`. All other implementation remains outside the current
authorization.

## Prior Phase: DEMO-C1 Complete; No Active Implementation Slice

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
| --- | --- | --- |
| `docs/research/method_decomposition/codex_phase0/README.md` | What did the independently reviewed code-derived decomposition observe, and how will it be compared later? | Current bounded research evidence and comparison procedure; not an adopted capability model. |
| `docs/plans/method_dash_c1.md` | What did the local methodology dashboard prototype implement and explicitly exclude? | Completed bounded implementation record for `METHOD-DASH-C1`. |
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

> Sources: `README.md`; `PROJECT.md`; `AGENTS.md`;
> `contracts/shared_contracts.md`; `docs/ARCHITECTURE.md`;
> `docs/CONCERNS.md`; `docs/IMPLEMENTING_AGENT_NOTES.md`;
> `docs/CAPABILITY_DEPENDENCY_GRAPH.md`;
> `docs/PRE_IMPLEMENTATION_CHECKLIST.md`;
> `docs/research/method_decomposition/codex_phase0/README.md` and its linked
> evidence and comparison rubric;
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
> extended with claim-licensing controls on 2026-07-10, updated with the exact
> `T0-PROV` authorization boundary and independent closure on 2026-07-12, and
> reconciled to the merged Phase 0 method-capability evidence on 2026-08-12.
