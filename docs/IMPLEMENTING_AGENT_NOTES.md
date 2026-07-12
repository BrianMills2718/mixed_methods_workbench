# Future Implementing Agent Notes

Status: future integration reference — only local `T0-PROV` is currently authorized

This file captures high-confidence work and larger repo-local notes from the
2026-06-26 worktree review. It is intentionally conservative: the workbench is
not ready for adapters, UI, or live engine orchestration.

## High-Confidence Work Now

For the current documentation-first phase:

- Keep `docs/plans/001_walking_skeleton.md` marked as a future proposal.
- Use `docs/PLANNING_STATUS.md` for the current authorization boundary and the
  detailed blueprint only for future sequencing. Plan 002 is historical.
- Execute only `docs/plans/current_t0_truthful_fixture_inventory.md`; its W2
  inventory proof does not authorize another T0 item, engine work, or adapters.
- If Brian later authorizes another implementation slice, run
  `docs/PRE_IMPLEMENTATION_CHECKLIST.md` before creating code, adapters,
  schemas, APIs, UI, or upstream tasks.
- Keep `docs/CONCERNS.md` current when new engine-readiness facts appear.
- Preserve `examples/integration_payload_mockup.md` as invented example data
  until real fixture exports exist.
- Do not import engine internals into this repo.
- Do not build a workbench UI or adapters until QC and PT exports are versioned
  and fixture-backed **and** Brian has explicitly authorized implementation.

## Repo-Local Notes For Later Implementing Agents

### `qualitative_coding`

After a separately named producer authorization, consider a small repo-local
slice that:

- refreshes and records repository state before claiming readiness (QC was
  clean in the read-only 2026-07-12 snapshot);
- selects one canonical QC export fixture for the workbench;
- validates that fixture with the strict QC handoff/export command;
- records source hashes, producer commit, scope, anchors, claims,
  patterns/candidates, caveats, and evidence grade;
- keeps PT inference fields out of QC exports.

Do not add likelihood vectors, posteriors, or comparative-support fields to QC.

### `process_tracing`

After a separately named producer authorization, consider a repo-local slice
that:

- fixes the documented `make check` runtime surface so it uses repo-local Python;
- decides the fate of untracked `workbench/`;
- designs and implements `pt_export_v1` as the workbench-safe export seam;
- includes source scope, hypotheses, comparative support, absence findings,
  verdicts, run metadata, caveats, schema version, and artifact provenance;
- proves the export with one fixture and tests.

Do not ask the workbench to parse `result.json` or import `pt.schemas`.

### `theory-forge`

The 2026-07-12 read-only investigation found a clean v14 runtime and tested
optional v15 extension but no workbench export. Before any integration work:

- refresh current health/check status and version authority;
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
pre-implementation checklist has passed and the included engine exports each
provide:

- `schema_version`;
- producer repo and commit;
- source artifact path and hash;
- validation command and result;
- explicit scope/caveat fields;
- fixture data committed or otherwise durably recoverable;
- a clear statement of what claim the artifact licenses and what it does not.
