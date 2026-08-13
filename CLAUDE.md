# Mixed Methods Workbench

This is the integration authority for a broad text-centered mixed-methods
workbench built in thin, versioned slices. Read `docs/ROADMAP.md`,
`docs/CAPABILITY_DEPENDENCY_GRAPH.md`,
`docs/PRE_IMPLEMENTATION_CHECKLIST.md`,
`docs/MIXED_METHODS_CAPABILITY_MAP.md`, and
`docs/PLANNING_STATUS.md` before planning. The current product critical path is
one cohesive policy investigation through an MVP, not further method-catalog
expansion. The Investigation Spine checkpoint is complete. The Mist Trail
source gate concluded that Mist Trail is useful for bounded pre-decision
option appraisal but cannot serve as the sole MVP flagship. The replacement
screen selected New York City's Congestion Relief Zone tolling program. The
exact source freeze is now complete in
`docs/research/nyc_crz_source_freeze.md`; the next product slice is one reviewed
prediction, one hearing concern, and one frozen descriptive aggregate in the
existing Investigation Spine. Do not expand the corpus, claim causality, or
generalize its local seams before that slice is observed. Brian
accepted the Phase 2 discovery format on
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
Phase 3 is paused as supporting research while product integration controls.
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
- `~/projects/qualitative_coding/docs/PROJECT_THEORY_AND_GOALS.md`
- `~/projects/process_tracing/CLAUDE.md`
- `~/projects/process_tracing/docs/PROJECT_THEORY_AND_GOALS.md`
- `~/projects/process_tracing/docs/SOTA_PLUS_TARGET_ARCHITECTURE.md`
- `~/projects/grounded-research/CLAUDE.md`
- `~/projects/grounded-research/docs/ROADMAP.md`
- `~/projects/theory-forge/CLAUDE.md`
- `~/projects/theory-forge/docs/adr/0003-ac14-integration-deferred.md`
- `docs/ROADMAP.md`
- `docs/CAPABILITY_DEPENDENCY_GRAPH.md`
- `docs/PRE_IMPLEMENTATION_CHECKLIST.md`
- `docs/PLANNING_STATUS.md`
- `plan/goals/2026-07-12-sota-or-beyond.md`
- `docs/SOTA_EVIDENCE_SCORECARD.md`
- `docs/MIXED_METHODS_CAPABILITY_MAP.md`
- `docs/plans/current_t0_truthful_fixture_inventory.md`
- `docs/plans/003_integration_versioning_and_clean_state.md`
