# ADR 0001: Compose Method Engines Before Merging Repos

Date: 2026-06-25

## Status

Accepted for planning scaffold.

## Context

`qualitative_coding` and `process_tracing` overlap around evidence, source
scope, claims, disconfirmation, mixed-methods causal reasoning, and auditable
research artifacts. They also have different invariants:

- `qualitative_coding` owns broad qualitative coding, grounded/thematic stages,
  segment coverage, claim ledgers, human review, QDA export, and qualitative
  evaluation scaffolds.
- `process_tracing` owns Van-Evera-style causal inference: source packets,
  rival hypotheses, evidence-by-hypothesis likelihood vectors, deterministic
  comparative support updates, absence checks, and causal reports.

Merging repos now would blur these invariants and produce a large horizontal
integration before any user-visible workbench slice exists.

## Decision

Create `mixed_methods_workbench` as an integration planning surface and eventual
workbench shell. Compose method engines through typed contracts before moving or
merging implementation code.

The first implementation target, when started, should be a vertical walking
skeleton that reads one completed `qualitative_coding` artifact and one
completed `process_tracing` artifact, normalizes them into shared evidence and
research-question contracts, and renders a unified review/report mockup.

## Alternatives Considered

- Merge `process_tracing` into `qualitative_coding`: rejected because the causal
  inference invariants and Bayesian math would become a sub-feature of a broader
  coding repo, obscuring method boundaries.
- Merge `qualitative_coding` into `process_tracing`: rejected because the broad
  qualitative and QDA workbench is larger than process tracing.
- Keep only loose narrative alignment: rejected because shared contracts are
  needed before agents can safely build across both projects.

## Consequences

- The workbench shell can evolve without destabilizing either method engine.
- Shared contracts become the first integration product.
- Future code movement remains possible, but only after a vertical slice proves
  which boundaries should harden.

## Supersession

Supersede this ADR only after at least one vertical workbench slice exists and a
review shows that a repo merge would reduce complexity without violating either
engine's method invariants.

