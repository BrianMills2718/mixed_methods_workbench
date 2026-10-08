# Mixed Methods Workbench

`AGENTS.md` is the sole authored instruction source for Claude Code and Codex in this repository.

This is the integration authority for a broad text-centered mixed-methods
workbench built in thin, versioned slices. Read
`docs/SYSTEM_GOAL_AND_CAPABILITY_ARCHITECTURE.md`,
`docs/CAPABILITY_ADOPTION_MAP.md`, `docs/ROADMAP.md`,
`docs/CAPABILITY_DEPENDENCY_GRAPH.md`,
`docs/PRE_IMPLEMENTATION_CHECKLIST.md`,
`docs/MIXED_METHODS_CAPABILITY_MAP.md`, and
`docs/PLANNING_STATUS.md` before planning. For current state as of
2026-09-06, start with `docs/runs/2026-09-06-state-assessment-and-next-agent-brief.md`.

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

Brian approved a first-principles architecture reset on 2026-08-13. The current
critical path is: verify existing capability owners and adoption; map the flat
method inventories to generic execution forms, reusable research primitives,
method-owned protocols, and study workflows; freeze the ecosystem-subordinate
composition/evidence-round-trip profile; then refactor the existing NYC
structured extraction as the first authentic consumer of a reusable action.
Do not add another case-specific vertical or implement a universal schema,
runtime, ontology, or method planner. Brian accepted the three NYC review
statements (prediction wording, hearing-concern wording, bounded quantitative
comparison) on 2026-08-14; the immutable record is
`docs/research/nyc_crz_human_disposition.json` at `c95488c`. Plan #5 therefore
marks `NYC-QC-1` as ready, and a QC-side lane for it exists unmerged at
`qualitative_coding` branch `nyc-crz-six-hearing-qc`. That readiness conflicts
with the 2026-08-13 reset's phase order; the conflict, the evidence, and the
recommended resolution are in `docs/runs/2026-09-06-state-assessment-and-next-agent-brief.md`. Brian chose Path A on 2026-09-06: finish `NYC-QC-1`, `NYC-INTEGRATE-1`, and
`NYC-MVP-REVIEW-1` first; the shared-action refactor follows.

The Workbench is the application/integration authority, not the ecosystem
architecture authority. Project Meta owns the cross-project artifact and
composition architecture, Data Contracts owns the neutral action grammar,
`llm_client` owns model execution, and method repositories own their protocols
and inference. OntoCanon owns governed semantic assertions; DIGIMON owns graph
materialization and retrieval. Both remain optional to an MVP path unless the
study question needs them.

The Investigation Spine checkpoint is complete. Mist Trail remains a bounded
secondary appraisal example. NYC Congestion Relief Zone remains the stable MVP
example after the infrastructure gate, with its exact source freeze preserved.
Brian accepted the Phase 2 discovery format on
2026-08-13: method phase → analytical move → execution action, with
`operation_kind` at Levels 2 and 3, typed connections, six authority roles,
information origins, temporal/access/version guards, and exact anchors. Existing
verbs remain a coarse discovery input, and `analysis_plan` remains provisional
for further testing rather than an adopted shared enum. Brian selected the
14-method Phase 3 denominator on 2026-08-13: `phase2b-proposal-0.3` plus the
non-substitutable theory-testing Process Tracing variant. The adopted
coordination identity is Plan #4, with its canonical graph at
`docs/research/method_decomposition/phase3/4_phase3_portfolio_decomposition_work_graph.json`.
Phase 3 authorizes documentation-only decomposition of those frozen variants.
It does not adopt a universal production schema, authorize Phase 4 collision
scoring, Phase 5 adjudication, coverage or capability promotion, shared
infrastructure, or product implementation. `METHOD-DASH-C1/C2`, `MT-D1`,
`T0-PROV`, and local `DEMO-C1` are completed bounded slices; none closes
producer readiness or method validity.
Brian lifted the Phase 3 pause on 2026-10-08 (observation-to-action-metamodel `ROADMAP_AGENT_MODEL.md` row 5a): the pause waited behind the NYC product-integration lane, which he paused on 2026-10-04 (PR #41), and on 2026-10-07 he approved the cross-method crosswalk that reads the integrated 14. `P3-CONTROL` is ready: it reviews lane evidence, issues receipts and advances lane states; integration follows acceptance of all three lanes. Phase 3 completed 2026-10-08: all three lanes were reviewed, corrected and accepted with receipts (`lane_receipts/`), and `P3-INTEGRATE` validated all 14 decompositions (`integration_report.md`, `validation_report.json`, `portfolio_manifest.yaml`; 14 of 14 pass). This establishes 14 source-frozen, structurally valid decompositions only: no collision, adjudication, coverage or reusable-capability claim.
Do not begin another implementation merely because a roadmap or future slice
exists, and do not move code from an engine into this repo unless Brian
explicitly authorizes a named implementation slice.

## Operating Rules

- Keep this repo as the integration authority: study/product frame, method
  boundaries, consumer contracts, version compatibility, integration policy,
  roadmap, and concern register.
- Treat `qualitative_coding`, `process_tracing`, `grounded-research`, future
  `theory-forge`, and a future quantitative-text adapter as producers with their
  own invariants and claim discipline.
- Do not claim this workbench is implemented until a vertical slice exists.
- `METHOD-DASH-C1` may add local method profiles, question-first routing, a
  browser review surface, matching JSON operations, and focused tests. It may
  not invoke producer engines, adopt shared contracts, deploy, or claim
  automated substantive method selection. Completed `T0-PROV` evidence does
  not authorize another T0 item. Plans 001 and 003 describe future work and do
  not authorize it.
- Every cross-repo seam must use Pydantic-style typed contracts; no raw `dict`
  or ad hoc JSON at durable boundaries.
- Before adding an implementation, identify the current capability owner and
  record `reuse`, `wrap`, `extend`, `supersede`, `keep_method_owned`, `defer`,
  `explicit_exception`, or `missing`, plus authentic consumer evidence.
- Treat prompt-plus-schema as a generic semantic execution form, not as a
  complete research method. Preserve method-owned state, ordering, evidence
  exposure, validators, review authority, feedback loops, and claim limits.
- Preserve method distinctions:
  - qualitative coding discovers and anchors patterns/claims in a corpus;
  - process tracing tests rival causal explanations within a source scope;
  - theory operationalization guides analysis but is not empirical evidence;
  - mixed-methods integration intentionally connects, builds, merges, or embeds
    qualitative and quantitative strands and produces bounded meta-inferences.
- Do not flatten process tracing into generic qualitative coding, and do not
  force all qualitative work into process-tracing hypothesis tests.
- Do not call QC plus PT “mixed methods”; version 0.1 is multi-method
  qualitative. Version 0.4 is the first planned true mixed-methods slice.
- Producers own strict export schemas. Workbench adapters own permissive,
  compatible consumers. Fail on unsupported major versions.
- Synthetic fixtures license at most C-grade shape claims.
- DEMO-C1 synthetic contract behavior may be A/test while its payload content
  remains C; its package is under `src/mixed_methods_workbench/`, fixtures under
  `examples/fixtures/demo_c1/`, and tests under `tests/`.

## Commands

Current scaffold checks:

```bash
make help
make check
make coverage
make validate-demo-fixtures
make validate-demo-controls
make assemble-demo-review
make method-dashboard
make test-method-dashboard
```

`make check` is not an engine-readiness or methodological-validity gate.

## References

- `~/projects/qualitative_coding/CLAUDE.md`
- `~/code/qualitative_coding/docs/PROJECT_THEORY_AND_GOALS.md`
- `~/projects/process_tracing/CLAUDE.md`
- `~/projects/process_tracing/docs/PROJECT_THEORY_AND_GOALS.md`
- `~/projects/process_tracing/docs/SOTA_PLUS_TARGET_ARCHITECTURE.md`
- `~/projects/grounded-research/CLAUDE.md`
- `~/code/grounded-research/docs/ROADMAP.md`
- `~/projects/theory-forge/CLAUDE.md`
- `~/projects/theory-forge/docs/adr/0003-ac14-integration-deferred.md`
- `docs/ROADMAP.md`
- `docs/SYSTEM_GOAL_AND_CAPABILITY_ARCHITECTURE.md`
- `docs/CAPABILITY_ADOPTION_MAP.md`
- `docs/CAPABILITY_DEPENDENCY_GRAPH.md`
- `docs/PRE_IMPLEMENTATION_CHECKLIST.md`
- `docs/PLANNING_STATUS.md`
- `plan/goals/2026-07-12-sota-or-beyond.md`
- `docs/SOTA_EVIDENCE_SCORECARD.md`
- `docs/MIXED_METHODS_CAPABILITY_MAP.md`
- `docs/plans/current_t0_truthful_fixture_inventory.md`
- `docs/plans/003_integration_versioning_and_clean_state.md`
