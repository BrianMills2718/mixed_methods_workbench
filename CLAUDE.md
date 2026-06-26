# Mixed Methods Workbench

This is a planning scaffold for a future qualitative and mixed-methods research
workbench. It composes `qualitative_coding` and `process_tracing` as method
engines through typed contracts. It may later consume `theory-forge` theory
operationalization artifacts, but Theory Forge is not a current runtime
dependency. Do not move code from any engine into this repo until a slice plan
explicitly requires it.

## Operating Rules

- Keep this repo as the integration authority: product frame, boundaries,
  shared contracts, roadmap, and concern register.
- Treat `qualitative_coding`, `process_tracing`, and future `theory-forge`
  integration as dependencies with their own invariants and claim discipline.
- Do not claim this workbench is implemented until a vertical slice exists.
- Every cross-repo seam must use Pydantic-style typed contracts; no raw `dict`
  or ad hoc JSON at durable boundaries.
- Preserve method distinctions:
  - qualitative coding discovers and anchors patterns/claims in a corpus;
  - process tracing tests rival causal explanations within a source scope;
  - mixed-methods synthesis bridges evidence, patterns, hypotheses, and
    quantitative causal/model-selection tools without conflating estimands.
- Do not flatten process tracing into generic qualitative coding, and do not
  force all qualitative work into process-tracing hypothesis tests.

## Commands

No implementation commands yet. Initial repo checks are documentation-only:

```bash
find . -name '*.md' -maxdepth 4 -print
```

## References

- `~/projects/qualitative_coding/CLAUDE.md`
- `~/projects/qualitative_coding/docs/PROJECT_THEORY_AND_GOALS.md`
- `~/projects/process_tracing/CLAUDE.md`
- `~/projects/process_tracing/docs/PROJECT_THEORY_AND_GOALS.md`
- `~/projects/process_tracing/docs/SOTA_PLUS_TARGET_ARCHITECTURE.md`
- `~/projects/theory-forge/CLAUDE.md`
- `~/projects/theory-forge/docs/adr/0003-ac14-integration-deferred.md`
- `docs/plans/002_engine_stability_and_integration_readiness.md`
