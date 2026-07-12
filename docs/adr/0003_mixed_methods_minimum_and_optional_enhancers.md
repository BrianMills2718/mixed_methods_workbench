# ADR 0003: Mixed-Methods Minimum and Optional Enhancers

Status: accepted for planning
Date: 2026-07-12

## Context

The capability graph and roadmap made Grounded Research (`GR`) adjudication and
Theory Forge (`TF`) operationalization hard prerequisites for the first genuine
mixed-methods row (`MM`). That edge is not implied by the definition of mixed
methods and conflicts with ADR 0002 and Plan 003, which define the minimum as
intentional integration of qualitative and quantitative strands.

Adjudication and explicit theory operationalization can strengthen a study, and
some named designs will require them. Neither is universally required to
connect, build, merge, embed, or transform qualitative and quantitative work.
Making both universal prerequisites would conflate product breadth with method
validity and could block the first observed mixed-methods slice on unrelated
producer readiness.

The current 1.0 release profile separately declares theory operationalization
as a product capability. That makes TF a 1.0 dependency under the current scope,
but still not a prerequisite for the first `MM` claim.

## Decision

1. The minimum dependency for `MM` is a governed real qualitative foundation
   (`R01`) plus a validated quantitative-text strand (`QT`) and an explicit,
   evaluated qual–quant integration operation.
2. `GR` and `TF` branch after `R01` as parallel method-scoped enhancers.
3. A release, study, or benchmark that claims adjudication must pass the `GR`
   gate. One that claims theory operationalization or theory-guided revision
   must pass the `TF` gate.
4. Under the current 1.0 profile, TF must pass before `V10` because that profile
   promises theory operationalization. GR remains optional unless a later 1.0
   profile explicitly includes automated adjudication.
5. Version labels describe planned product milestones; they do not create
   methodological dependency edges. A future release plan may reorder optional
   0.2/0.3 work without weakening any claim gate.

## Consequences

- The critical path to the first true mixed-methods case becomes
  `T0 -> GOV -> QC + PT -> R01 -> QT -> MM`.
- GR or TF can proceed earlier when separately authorized, but their existence
  cannot license a generic mixed-methods claim.
- The capability graph, roadmap, checklist, goal map, and SOTA scorecard must
  distinguish the first `MM` gate from the wider `V10` release profile.
- Every benchmark declares which optional capabilities are in scope; missing
  optional capabilities are reported rather than averaged into another score.

## Rejected Alternatives

- **Keep GR and TF as universal `MM` prerequisites.** Rejected because it adds
  services that are not constitutive of mixed methods and turns producer timing
  into a methodological definition.
- **Remove GR and TF from the roadmap.** Rejected because disagreement
  adjudication and explicit theory operationalization are important declared
  product capabilities.
- **Treat every optional feature as non-blocking for 1.0.** Rejected because a
  release must actually satisfy the capabilities it declares; the current 1.0
  profile explicitly includes theory operationalization.

## Evidence

- `docs/adr/0002_broad_north_star_versioned_thin_slices.md`
- `docs/plans/003_integration_versioning_and_clean_state.md`
- `~/projects/investigations/mixed_methods_workbench/2026-07-12-sota-program-baseline.md`
- `.claude/tasks/research_sota_landscape.md`
- [NIH Best Practices for Mixed Methods Research](https://obssr.od.nih.gov/sites/g/files/mnhszr296/files/Best_Practices_for_Mixed_Methods_Research.pdf)
- [Mixed Methods Integration Quality Framework](https://journals.sagepub.com/doi/full/10.1177/15586898241257555)
