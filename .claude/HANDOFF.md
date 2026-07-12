# Mixed Methods Workbench Handoff

## Current Truth

This repository is the integration and planning authority. It remains in
documentation-only mode; no implementation slice or product release is active.

ADR 0004 now governs the long-term order:

```text
truthful baseline -> controlled demo -> separate QC/PT/GT lanes
-> integrated qualitative review
-> optional OntoCanon projection and DIGIMON navigation
-> source-backed theory recommendation and human selection
-> Theory Forge operationalization and executed-run seams
-> final corpus selection/governance -> observed core validation
-> quantitative text -> explicit mixed-methods integration
-> portfolio, evaluation, and adaptive frontier
```

The final validation corpus is deliberately deferred until the workbench has
demonstrated useful software behavior. FRUS remains a researched candidate,
not a selected case. Governance is still mandatory before empirical claims.

## Boundaries That Must Survive

- QC, PT, and grounded theory are separate method-native engines/profiles.
  Grounded theory is not the `grounded-research` adjudication project.
- OntoCanon governs reviewed assertions, ontology packs, identity, provenance,
  review/promotion, and exports. Projection is optional and never replaces the
  method-native artifact.
- DIGIMON projects and retrieves graph/evidence views. It does not perform
  method inference, and a future slice must pin a supported contract/commit.
- The theory recommender searches a curated library and academic sources.
  LLM knowledge may generate leads only; a researcher approves the shortlist.
- Theory Forge formalizes a paper, compiles a theory-specific pipeline, and
  runs staged analysis. The workbench needs both a frozen
  `TheoryOperationalizationArtifact` and a future typed
  `TheoryApplicationRun`; it must not consume live compiler internals.
- A QC/PT/GT review is multi-method qualitative, not mixed methods. A mixed-
  methods claim requires an explicit qualitative-quantitative integration
  operation and bounded meta-inference.

## Evidence Truth

`T0-PROV` remains independently signed off at
`f26bc6ade93c475c7ebc4ca608e796a9b9fe2f1a`. W2 inventory provenance is A,
fixture shapes are C, legacy scaffold coverage is overall D, and broader T0 and
program evidence remain F. The planning rewrite does not move those grades.

## Current DEMO Planning Boundary

Brian's “ok proceed” activated the named `DEMO` planning slice. The current
requirements, diagrams, contract stubs, failure modes, evidence criteria, and
GT-I dependency subplan are in `docs/plans/current_demo_method_core.md`. The
review journey is rendered in `docs/plans/demo_method_core_mockup.md` and
`notebooks/demo_method_core_plan.ipynb`.

The mockup approval gate now blocks implementation. The evidence-backed owner
recommendation is `qualitative_coding`, labeled grounded-theory-inspired until
real theoretical sampling and D8 expert evidence license anything stronger.
Producer mutation remains separately authorized.

## Required Reading

1. `docs/adr/0004_demo_first_method_core_and_knowledge_infrastructure.md`
2. `docs/PLANNING_STATUS.md`
3. `docs/ROADMAP.md`
4. `docs/CAPABILITY_DEPENDENCY_GRAPH.md`
5. `docs/MIXED_METHODS_CAPABILITY_MAP.md`
6. `docs/PRE_IMPLEMENTATION_CHECKLIST.md`
7. `docs/CONCERNS.md`
8. `plan/goals/2026-07-12-sota-or-beyond.md`
9. `~/projects/investigations/mixed_methods_workbench/2026-07-12-theory-forge-role-and-integration.md`
10. `~/projects/investigations/mixed_methods_workbench/2026-07-12-ontocanon-digimon-capability-review.md`

## Sanity Checks

```bash
make help
make check
make coverage
make coverage-json
git status --short --branch
```

Expected: 41 fixture controls, 3 coverage controls, pure JSON transport, legacy
coverage 1 A / 0 B / 2 C / 5 D / 0 F (overall D), and a clean synchronized
branch. These checks do not establish producer readiness or methodological
validity.
