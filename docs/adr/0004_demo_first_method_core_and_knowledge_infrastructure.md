# ADR 0004: Demonstrate the Method Core Before Selecting the Validation Corpus

Status: accepted for planning; no implementation authorized
Date: 2026-07-12

## Context

The prior roadmap made selection and governance of a final public case the
first gate to useful functionality. It also postponed grounded theory, treated
Theory Forge mainly as a static operationalization export, and did not assign
clear roles to OntoCanon or DIGIMON. That order asks a consequential research
choice to carry the risk of an unproven product.

Brian directed that corpus selection happen after the workbench has shown that
its workflow works, that qualitative coding (QC), process tracing (PT), and
grounded theory (GT) form the initial method core, and that theory
recommendation and Theory Forge follow that core. A subsequent repository
review established that OntoCanon and DIGIMON supply reusable knowledge
governance and graph-retrieval infrastructure but do not own method inference.

## Decision

1. Build the first proof on a small synthetic or rights-clear open
   demonstration packet. It licenses software-workflow claims only. It cannot
   license empirical, methodological-validity, or SOTA claims.
2. Demonstrate three separate method-native lanes first: QC, PT, and GT.
   Grounded theory is a qualitative methodology and is not the
   `grounded-research` project, which remains an optional adjudication service.
3. Preserve each producer's strict native artifact as the source of truth.
   The workbench owns compatible consumers, orchestration, review, and
   cross-method linkage.
4. Reuse OntoCanon only for optional reviewed-claim projection, provenance,
   identity, ontology-pack governance, review/promotion, and governed exports.
   A projection never replaces the originating QC/PT/GT artifact.
5. Reuse DIGIMON downstream of governed source/assertion data for graph
   projection, evidence navigation, retrieval, ranking, and analytics. Each
   result must step down to the original source and method-native finding.
6. Add theory recommendation after the core method demonstration. Candidate
   discovery uses, in order: a curated theory library, source-backed academic
   search, and LLM prior knowledge only to propose leads or queries. A human
   approves the shortlist and selection; uncited model recall is not a theory
   record.
7. Treat Theory Forge as a compile-and-run method engine: paper to formal
   schema, schema to compiled theory-specific pipeline, and pipeline to staged
   analysis. The workbench should eventually consume two separate frozen,
   producer-owned seams: `TheoryOperationalizationArtifact` and a future typed
   `TheoryApplicationRun`. It must not import live compiler/runtime internals.
8. Select and govern the final validation corpus only after the demo review
   packet passes. Governance remains mandatory before any empirical claim.
9. Add quantitative-text measurement and explicit qualitative-quantitative
   integration after the qualitative core and theory workflow. A minimal
   mixed-methods claim does not logically require Theory Forge, but the planned
   product sequence includes it before the first full validation program.
10. These documents remain planning authority only. A named implementation
    slice and fresh entry review are still required before code or producer
    changes.

## Capability Order

```text
truthful baseline
  -> controlled demonstration packet
  -> QC + PT + GT method-native demo lanes
  -> integrated qualitative review packet
  -> optional OntoCanon projection + DIGIMON evidence navigation
  -> source-backed theory recommendation + human selection
  -> Theory Forge operationalization + executed-run seams
  -> final corpus selection/governance
  -> observed QC/PT/GT validation
  -> quantitative-text strand
  -> explicit mixed-methods integration
  -> comparative evaluation and adaptive frontier
```

OntoCanon/DIGIMON may be prototyped in parallel once method-native artifacts
exist, but neither blocks a useful QC/PT/GT lane. Final corpus governance may
also be researched earlier; it becomes a blocking gate only when the program
moves from software demonstration to empirical validation.

## Consequences

- The existing FRUS recommendation remains a candidate for later validation,
  not the next implementation gate.
- GT moves from the late method portfolio into the first functional core. Its
  producer ownership and strict export contract are unresolved stop points.
- `grounded-research` retains a distinct optional adjudication role.
- Theory Forge requires an additional run-export design beyond its existing
  planned operationalization seam.
- The workbench avoids rebuilding governed assertion, graph, and retrieval
  infrastructure, while avoiding lossy conversion of method objects into a
  universal graph schema.

## Rejected Alternatives

- **Choose the final case first.** Rejected because corpus choice, licensing,
  and study design should follow a demonstrated workflow, not substitute for
  one.
- **Flatten QC, PT, and GT into one analysis object.** Rejected because their
  inferential objects and validity obligations differ.
- **Use OntoCanon or DIGIMON as the analysis engine.** Rejected because they
  govern/project/retrieve knowledge; they do not perform the method-native
  inference.
- **Let the LLM choose a theory from memory.** Rejected because theory identity,
  scope, and interpretation must be source-backed and reviewable.
- **Represent Theory Forge as a mechanism/indicator form.** Rejected because
  it omits the formalize-compile-run pipeline and its stage trace.

## Evidence and Synthesis Provenance

Directly consulted for this decision:

- `PROJECT.md`, `CLAUDE.md`, `.claude/HANDOFF.md`, and
  `.claude/handoff.yml`;
- `docs/ROADMAP.md`, `docs/CAPABILITY_DEPENDENCY_GRAPH.md`,
  `docs/MIXED_METHODS_CAPABILITY_MAP.md`, `docs/PLANNING_STATUS.md`,
  `docs/PRE_IMPLEMENTATION_CHECKLIST.md`, `docs/CONCERNS.md`, and
  `docs/plans/003_integration_versioning_and_clean_state.md`;
- `docs/adr/0003_mixed_methods_minimum_and_optional_enhancers.md`;
- `plan/goals/2026-07-12-sota-or-beyond.md`;
- `.claude/tasks/research_artifact_authority.md`,
  `.claude/tasks/research_producer_readiness.md`,
  `.claude/tasks/research_sota_landscape.md`,
  `.claude/tasks/research_gov_case_options.md`, and
  `.claude/tasks/research_qt_first_task_options.md`;
- `docs/decisions/2026-07-12-first-governed-case.md` and
  `docs/decisions/2026-07-12-first-quantitative-text-strand.md`;
- `~/projects/investigations/mixed_methods_workbench/2026-07-12-sota-program-baseline.md`;
- `~/projects/investigations/mixed_methods_workbench/2026-07-12-theory-forge-role-and-integration.md`;
- `~/projects/investigations/mixed_methods_workbench/2026-07-12-ontocanon-digimon-capability-review.md`;
- `~/projects/investigations/cross-project/2026-06-21-mixed-methods-ecosystem-assessment.md`;
- `~/projects/investigations/cross-project/2026-06-21-theory-forge-coupling.md`.

Machine-readable mirrors and fixture payloads were enumerated but not used to
decide product order because they add shape evidence, not planning authority.
