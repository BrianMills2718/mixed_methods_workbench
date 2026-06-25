# Mixed Methods Workbench

## Goal

Build a methodology-aware qualitative and mixed-methods research workbench that
can ingest research evidence and produce high-quality, auditable research
artifacts: qualitative codes, grounded claims, rival explanations, causal
support assessments, negative cases, source-scope caveats, review packets, and
publishable exports.

The workbench should use existing engines rather than prematurely merging their
repos:

- `~/projects/qualitative_coding` supplies the qualitative evidence substrate:
  ingestion, coding, span grounding, segment universe, claim ledger,
  negative-case review, adjudication packages, QDA export, and broad
  qualitative/mixed-methods evaluation scaffolding.
- `~/projects/process_tracing` supplies the causal inference engine:
  source packets, rival hypotheses, diagnostic evidence, likelihood vectors,
  deterministic Bayesian comparative support, absence checks, source coverage,
  and process-tracing reports.

## Product Thesis

Qualitative and mixed-methods research is constrained by two bottlenecks:

1. the human labor required for coding, memoing, comparison, disconfirmation,
   source review, adjudication, and report production; and
2. the technical barrier that keeps many qualitative workflows from using
   quantitative pattern analysis, causal reasoning, and reproducible audit
   infrastructure.

The workbench should automate the labor-intensive parts with LLMs and
programmatic verification while making quantitative and causal methods available
inside the same research workflow. The target is beyond-SOTA research automation
across the integrated bundle, not a narrower "LLM coding tool" or a single
method implementation.

## Current Status

Planning scaffold only. This repo records the integration frame, architecture,
contracts, concern register, and slice roadmap. It is not yet an implementation
repo and does not claim to produce research outputs.

## Canonical Docs

- `docs/ARCHITECTURE.md` - design-plan artifact for the workbench shell.
- `docs/adr/0001_method_engines_not_monorepo.md` - decision to compose method
  engines through contracts before any repo merge.
- `contracts/shared_contracts.md` - initial cross-engine contract sketch.
- `docs/plans/001_walking_skeleton.md` - first vertical slice plan.
- `docs/CONCERNS.md` - live concern register.

