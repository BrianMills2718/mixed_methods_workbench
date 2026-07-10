# ADR 0002: Preserve the Broad North Star Through Versioned Thin Slices

Status: accepted
Date: 2026-07-09

## Context

The intended product is deliberately broader than a qualitative-coding tool, a
process-tracing interface, or an LLM research assistant. It aims to support the
full lifecycle of text-centered mixed-methods research: study design, corpus
governance, multiple qualitative traditions, computational and quantitative
text analysis, within-case causal inference, cross-case comparison, theory
operationalization and revision, explicit qualitative-quantitative integration,
human review, reporting, and reproducibility.

That scope is strategically coherent but cannot be implemented or validated as
one release. Narrowing the north star would discard the product's differentiator;
trying to ship the north star at once would produce a shallow collection of
unrelated features and unverifiable methodology claims.

The existing scaffold also conflates three kinds of progress:

1. an artifact shape exists;
2. two qualitative method engines can be reviewed together; and
3. a genuine mixed-methods design intentionally integrates qualitative and
   quantitative strands.

Those are not equivalent.

## Decision

Preserve the broad north star and deliver it as a versioned capability ladder.
Every release must be a thin end-to-end research slice with a named method
design, real inputs, inspectable intermediate artifacts, a useful researcher
output, adversarial controls, and explicit claim limits.

The roadmap uses three nested version surfaces:

- **Product releases** (`0.x`, then `1.0`) describe researcher-visible
  capability.
- **Artifact schemas** use independent semantic versions per producer contract.
- **Method profiles** are versioned rule sets that define valid operations,
  evidence requirements, quality criteria, and report obligations for a
  methodological tradition.

The following boundaries are permanent unless a later ADR replaces them:

- Method engines own method-specific inference and strict producer exports.
- The workbench owns study design, orchestration, compatible consumer adapters,
  cross-method linkage, integration, review, and reporting.
- Shared infrastructure owns generic LLM, retrieval, trace-evaluation, prompt
  evaluation, and truly cross-project data types.
- Theory operationalizations are design/context objects, never empirical
  evidence.
- Qualitative claims, process-tracing comparative support, quantitative
  estimates, and meta-inferences retain distinct estimands and uncertainty
  semantics.
- A release is called **mixed methods** only when it intentionally integrates at
  least one qualitative and one quantitative strand at a declared design point.
  QC plus process tracing alone is multi-method qualitative research.

## Release Rule

A version advances only when its named vertical path is usable and evaluated.
Breadth may be represented as planned method profiles and extension points, but
unvalidated breadth does not license a product claim.

For each version:

```text
study protocol -> governed sources -> method strands -> integration operation
-> review/adjudication -> report/export -> observed evaluation
```

All seven links must be present or explicitly marked out of scope. Synthetic
fixtures can establish shape but cannot advance a release beyond C-grade
evidence.

## Consequences

Positive consequences:

- The ambition remains intact without making any release depend on finishing
  every engine.
- Methodological depth becomes the unit of progress, not feature count.
- A stable workbench can integrate engines incrementally through versioned
  artifacts.
- The product can make honest claims at every stage and still compound toward a
  category-defining system.

Costs and constraints:

- Product, schema, and method-profile versions must be tracked separately.
- Some UI and schema work will be repeated as real slices reveal missing
  concepts.
- The first true mixed-methods release comes after a qualitative causal-review
  foundation; it cannot be claimed by the initial QC/PT slice.
- A quantitative-text analysis owner and first design must be selected before
  the first genuine mixed-methods release.

## Rejected Alternatives

### Reduce the product to qualitative coding plus process tracing

Rejected because it abandons intentional qualitative-quantitative integration,
theory/research design, interoperability, and the broader opportunity.

### Specify the complete universal schema before building slices

Rejected because method behavior and integration quality are partly emergent.
The workbench needs a broad domain vocabulary but promotes contract fields only
after real fixtures exercise them.

### Merge all engine repositories

Rejected by ADR 0001. Repository unity does not create methodological or
contractual coherence.

### Market the first QC/PT integration as mixed methods

Rejected because both strands are qualitative/within-case. The release is
valuable, but the label would be methodologically false.

## References

- `docs/ROADMAP.md`
- `docs/MIXED_METHODS_CAPABILITY_MAP.md`
- `docs/plans/003_integration_versioning_and_clean_state.md`
- `docs/adr/0001_method_engines_not_monorepo.md`
- NIH, *Best Practices for Mixed Methods Research in the Health Sciences*:
  <https://obssr.od.nih.gov/sites/g/files/mnhszr296/files/Best_Practices_for_Mixed_Methods_Research.pdf>
