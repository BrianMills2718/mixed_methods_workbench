# Workbench architecture

## 1. Goals and scope

The Workbench integrates producer exports into inspectable research review surfaces.
It owns consumer contracts and presentation; producer repositories own method engines.
[System model](../planning/SYSTEM_MODEL.md) describes the full repository.

## 2. Constraints

Inputs and outputs are files. Pydantic validates durable consumer records. Existing
studies remain compatible when optional theory context and scholarly appraisal are absent.

## 3. Context

KGAS supplies a pinned historical artifact. A separately attributed appraisal compares
its assertions with a scholarly source; neither arithmetic nor appraisal validates a theory.
Qualitative Coding supplies grounded-theory exports for ordinary study reviews.

## 4. Strategy

Reuse the study page builder for both ordinary studies and standalone theory context.
Retain original artifact values and bind references and receipts by digest.

## 5. Building blocks

[LikeC4 model](model.c4) maps the maintained consumer seam to actual Python modules.
The page command imports the study builder and the theory rendering models.
The study builder lazily imports theory context.
Theory context imports neither the page command nor the study builder.
Generated `.importlinter` enforces these direct import constraints.

## 6. Runtime

The command reads a study definition, validates declared pins and optional appraisal,
builds a typed payload, renders escaped HTML, and writes a hash-bound receipt.
No model calls or method execution occur in this path.

## 7. Deployment

Generated pages and JSON are static files. The builder can serve a local review.
Publishing is a separate action governed by the repository publishing rules.

## 8. Cross-cutting concerns

Explicit provenance limits distinguish source comparison, illustrative calculation,
and empirical evidence. Invalid declared inputs fail closed.

## 9. Decisions

See [decision records](../decisions/) and the maintained OpenSpec capabilities.
Native Lockstep comes from AES canonical revision
`05ee80c1a9cc77f692954b6de09a81ab0d9bdb0a`, pinned in `pyproject.toml` and `uv.lock`.

## 10. Quality requirements

Native trace checks cover maintained `kgas-theory-context` and `kgas-source-appraisal`
requirements and scenarios. Source roots include `src` and `scripts`. Legacy behavior
without OpenSpec requirements remains outside this coverage; existing repo checks remain.

## 11. Risks and debt

This bounded import model covers the changed consumer seam, not every legacy module.
The broader system model retains historical and planned slices with their limitations.

## 12. Glossary

See [domain glossary](../planning/DOMAIN.md). An appraisal is an attributable source
comparison; a theory context is preserved operationalization rather than an observation.
