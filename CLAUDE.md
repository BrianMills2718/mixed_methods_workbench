# Mixed Methods Workbench

This is the integration authority for a broad text-centered mixed-methods
workbench built in thin, versioned slices. Read `docs/ROADMAP.md`,
`docs/CAPABILITY_DEPENDENCY_GRAPH.md`,
`docs/PRE_IMPLEMENTATION_CHECKLIST.md`,
`docs/MIXED_METHODS_CAPABILITY_MAP.md`, and
`docs/PLANNING_STATUS.md` before planning. The default current mode is
documentation-only. Do not begin implementation merely because a roadmap or
future slice exists, and do not move code from an engine into this repo unless
Brian explicitly authorizes a named implementation slice.

## Operating Rules

- Keep this repo as the integration authority: study/product frame, method
  boundaries, consumer contracts, version compatibility, integration policy,
  roadmap, and concern register.
- Treat `qualitative_coding`, `process_tracing`, `grounded-research`, future
  `theory-forge`, and a future quantitative-text adapter as producers with their
  own invariants and claim discipline.
- Do not claim this workbench is implemented until a vertical slice exists.
- No implementation version is currently active. Plans 001 and 003 describe
  future work and do not authorize it.
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

## Commands

Current scaffold checks:

```bash
make help
make check
make coverage
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
- `docs/MIXED_METHODS_CAPABILITY_MAP.md`
- `docs/plans/003_integration_versioning_and_clean_state.md`
