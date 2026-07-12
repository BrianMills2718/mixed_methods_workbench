# Mixed Methods Workbench

## Goal

Build a methodology-aware qualitative and mixed-methods research workbench that
can ingest research evidence and produce high-quality, auditable research
artifacts: qualitative codes, grounded claims, rival explanations, causal
support assessments, negative cases, source-scope caveats, review packets, and
publishable exports.

The broad north star is preserved through the version ladder in
`docs/ROADMAP.md`. The workbench should compose existing engines rather than
prematurely merging their repos:

- `~/projects/qualitative_coding` supplies the qualitative evidence substrate:
  ingestion, coding, span grounding, segment universe, claim ledger,
  negative-case review, adjudication packages, QDA export, and broad
  qualitative/mixed-methods evaluation scaffolding.
- `~/projects/process_tracing` supplies the causal inference engine:
  source packets, rival hypotheses, diagnostic evidence, likelihood vectors,
  deterministic Bayesian comparative support, absence checks, source coverage,
  and process-tracing reports.
- `~/projects/theory-forge` is a future theory-operationalization producer, not a
  current workbench dependency: it may later supply constructs, mechanisms,
  hypotheses, observables, measures, assumptions, scope conditions, and compiled
  metadata through a typed artifact.
- `~/projects/grounded-research` is the future disagreement and evidence-
  adjudication engine: it may accept contested claim bundles and return
  independent analyses, verification actions, disagreement classifications,
  and human-reviewable dispositions.
- quantitative text analysis has no settled engine owner. The roadmap
  provisionally recommends established libraries behind a narrow adapter for
  one real exploratory-sequential design before considering shared-engine
  extraction.

## Product Thesis

Qualitative and mixed-methods research is constrained by two bottlenecks:

1. the human labor required for coding, memoing, comparison, disconfirmation,
   source review, adjudication, and report production; and
2. the technical barrier that keeps many qualitative workflows from using
   quantitative pattern analysis, causal reasoning, and reproducible audit
   infrastructure.

The workbench should automate the labor-intensive parts with LLMs and
programmatic verification while making quantitative and causal methods available
inside the same research workflow. The target is beyond-SOTA research
infrastructure across the integrated bundle, not a narrower "LLM coding tool"
or a single method implementation. The defensible frontier is rigorous
cross-method provenance, contradiction-seeking, adaptive source/sampling
decisions, and a disciplined division of labor among programmatic checks,
agents, and researchers.

## Current Status

Planning scaffold with an initial synthetic verification surface. Current
executable coverage is 1 A, 0 B, 2 C, 5 D, and 0 F; overall D. The A applies
only to independently signed W2 inventory provenance at
`docs/runs/2026-07-12-t0-prov-eval-signoff.md`; fixture contents remain C and
broader T0/program evidence remains F. No product version, engine integration,
or implementation slice is active. See `docs/PLANNING_STATUS.md` for the exact
boundary.

## Canonical Docs

- `docs/ROADMAP.md` - north star, release ladder, dependencies, and critical
  path for future implementation.
- `docs/PLANNING_STATUS.md` - what work is and is not authorized in the current
  phase.
- `plan/goals/2026-07-12-sota-or-beyond.md` - active long-term outcomes,
  dependency map, work packages, and transcript-demonstrable completion rule.
- `docs/SOTA_EVIDENCE_SCORECARD.md` - current external floors, incumbent
  baselines, evidence grades, and bounded SOTA claim rule.
- `docs/CAPABILITY_DEPENDENCY_GRAPH.md` - capability ordering, dependencies,
  success criteria, verification artifacts, and claim-licensing gates.
- `docs/PRE_IMPLEMENTATION_CHECKLIST.md` - required fresh-state review and
  current-plan gate before any future authorized implementation slice.
- `docs/MIXED_METHODS_CAPABILITY_MAP.md` - complete methodological/product scope
  and ownership gaps.
- `docs/plans/003_integration_versioning_and_clean_state.md` - detailed future
  implementation blueprint for versions 0.0 and 0.1; not a current task list.
- `docs/plans/current_t0_truthful_fixture_inventory.md` - completed bounded
  plan and evidence record for the `T0-PROV` subslice only.
- `docs/ARCHITECTURE.md` - initial QC/PT architecture artifact, subordinate to
  the current planning status and roadmap where they differ.
- `docs/adr/0001_method_engines_not_monorepo.md` - decision to compose method
  engines through contracts before any repo merge.
- `docs/adr/0003_mixed_methods_minimum_and_optional_enhancers.md` - claim-scoped
  GR/TF dependency decision.
- `contracts/shared_contracts.md` - initial cross-engine contract sketch.
- `docs/plans/002_engine_stability_and_integration_readiness.md` - historical
  dependency assessment retained for provenance.
- `docs/plans/001_walking_skeleton.md` - version 0.1 vertical-slice detail,
  retained as a future proposal.
- `docs/CONCERNS.md` - live concern register.
