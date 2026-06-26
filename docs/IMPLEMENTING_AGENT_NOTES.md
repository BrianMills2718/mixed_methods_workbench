# Implementing Agent Notes

Status: planning note - do not treat this as authorization to build the
workbench.

This file captures high-confidence work and larger repo-local notes from the
2026-06-26 worktree review. It is intentionally conservative: the workbench is
not ready for adapters, UI, or live engine orchestration.

## High-Confidence Work Now

These are safe because they reduce ambiguity without coupling repos:

- Keep `docs/plans/001_walking_skeleton.md` blocked until Plan 002 readiness
  gates pass.
- Keep `docs/plans/002_engine_stability_and_integration_readiness.md` as the
  sequencing authority for workbench integration.
- Keep `docs/CONCERNS.md` current when new engine-readiness facts appear.
- Preserve `examples/integration_payload_mockup.md` as invented example data
  until real fixture exports exist.
- Do not import engine internals into this repo.
- Do not build a workbench UI or adapters until QC and PT exports are versioned
  and fixture-backed.

## Repo-Local Notes For Later Implementing Agents

### `qualitative_coding`

Consider a small repo-local slice that:

- records the current dirty worktree status before claiming readiness;
- selects one canonical QC export fixture for the workbench;
- validates that fixture with the strict QC handoff/export command;
- records source hashes, producer commit, scope, anchors, claims,
  patterns/candidates, caveats, and evidence grade;
- keeps PT inference fields out of QC exports.

Do not add likelihood vectors, posteriors, or comparative-support fields to QC.

### `process_tracing`

Consider a repo-local slice that:

- fixes the documented `make check` runtime surface so it uses repo-local Python;
- decides the fate of untracked `workbench/`;
- designs and implements `pt_export_v1` as the workbench-safe export seam;
- includes source scope, hypotheses, comparative support, absence findings,
  verdicts, run metadata, caveats, schema version, and artifact provenance;
- proves the export with one fixture and tests.

Do not ask the workbench to parse `result.json` or import `pt.schemas`.

### `theory-forge`

Consider a repo-local readiness investigation before any integration work:

- resolve current health/check status;
- reconcile v14/v15 and roadmap/HANDOFF drift;
- identify one green theory that can produce a real fixture;
- draft a `TheoryOperationalizationArtifact` from real schema/manifest fields;
- keep AC8/AC11/AC14/AC15 paths out of the mixed-methods runtime.

The workbench should consume theory operationalization context, not a live Theory
Forge compiler service.

### `ac15`

No current mixed-methods task is recommended.

The only plausible future role is an optional pilot after Theory Forge has a
stable export artifact:

```text
TheoryOperationalizationArtifact -> AC15 structured spec/blueprint -> generated
artifact judged by Theory Forge tests
```

That pilot must not block the workbench and must not become a runtime dependency.

## Larger Tasks To Leave As Notes

Do not start these from `mixed_methods_workbench` until the owning engine exports
exist:

- executable Pydantic workbench contracts;
- QC/PT/TF adapters;
- fixture-backed `WorkbenchSynthesis`;
- static review shell;
- AC15 backend pilot;
- any repo merge or engine code movement.

## Readiness Trigger

A future workbench implementation agent may resume Plan 001 only when the
included engine exports each provide:

- `schema_version`;
- producer repo and commit;
- source artifact path and hash;
- validation command and result;
- explicit scope/caveat fields;
- fixture data committed or otherwise durably recoverable;
- a clear statement of what claim the artifact licenses and what it does not.
