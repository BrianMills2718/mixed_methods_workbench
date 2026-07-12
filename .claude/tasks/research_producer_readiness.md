# Producer Readiness Investigation

**Freshness timestamp:** 2026-07-12T12:19:29-07:00
**Scope:** Read-only inspection of local producer repositories and local ecosystem metadata.
**Mutation boundary:** This report is the only file written by this lane; no producer repository was modified.
**Verification boundary:** No full test suite, live LLM run, export generation, dependency installation, fetch, or other expensive/side-effecting command was run. Existing source, plans, tests, manifests, ignored local artifacts, Git state, help output, coordination state, and memory were inspected.

## Executive readout

| Producer / strand | Observed state | Workbench readiness conclusion | Confidence |
|---|---|---|---|
| `qualitative_coding` | A strict QC-to-PT package builder, validator, CLI/Make surface, and six focused tests exist. The planned canonical workbench fixture does not exist; the current contract omits codebook/category payloads and provenance fields required by its own workbench plan. | **Reusable contract core; not a proven canonical workbench export.** | High |
| `process_tracing` | Internal result models contain the needed method objects, but Plan 007 remains planned and both `pt/export.py` and `tests/test_export.py` are absent. The checkout also contains untracked `workbench/frontend/node_modules/`. | **Not export-ready. This is the critical release-0.1 producer gap.** | High |
| `theory-forge` | The runtime still selects v14; v15 is a backward-compatible extension/test surface. Plan 107 remains in progress, Plan 108 remains planned, and no workbench export code or fixture exists. A paper-sourced, internally consistent candidate manifest exists for Scale-Free Network Theory, but no matching repo-controlled runtime evidence file surfaced. | **A plausible first fixture candidate exists; export authority and fresh proof remain unresolved.** | High on code/plan state; medium on local compiled-cache health |
| `grounded-research` | A live Tyler-native `handoff.json` path and focused tests exist, but the shipped handoff targets `onto-canon`, has no schema version or producer/hash provenance, and has no workbench-specific contested-claim evaluation. | **Operational adjudication producer; not yet a versioned workbench producer.** | High |
| Future quantitative-text strand | The local project graph has zero entries matching a quantitative-text adapter/owner and the workbench depends only on QC and PT. | **No verifiable owner, adapter, task, or status exists in the project graph.** | High |

The handoff's central claims are therefore confirmed, with one useful refinement: Theory Forge's v14/v15 situation is not a parser dead-end. v14 is the current runtime authority, while v15 adds optional fields and is tested for backward compatibility. The unresolved issue is export provenance and source-version declaration, not basic schema readability.

## Investigation atoms

| ID | Question | Dependencies | Status | Answer |
|---|---|---|---|---|
| A0 | Which named producer repositories exist locally, and which instruction files govern each scope? | None | Complete | All four exact directories exist; `grounded-research` is the on-disk spelling and `grounded_research` is absent. Root `CLAUDE.md` is canonical; each `AGENTS.md` is a generated Codex projection. Grounded Research contains a wording conflict saying the files must mirror exactly although its generated file is explicitly a projection. |
| A1 | What branch, worktree state, and recent history establish each producer's freshness and drift risk? | A0 | Complete | All four branches match their configured upstream at the observed commits. QC, Theory Forge, and Grounded Research are clean. PT has untracked `workbench/frontend/node_modules/`. |
| A2 | What makes `qualitative_coding` integration-ready today? | A0–A1 | Complete | Strict package core and validation surfaces exist; canonical real fixture, complete workbench payload, and provenance-complete manifest do not. |
| A3 | What makes `process_tracing` integration-ready today? | A0–A1 | Complete | Internal fields and live ignored result artifacts exist; public export implementation, tests, fixture, clean state, and reliable canonical check gate do not. |
| A4 | What makes `theory-forge` integration-ready today? | A0–A1 | Complete | Schemas/manifests and candidate theory artifacts exist; Plan 108 export, fixture, source-version authority record, and fresh selected-theory proof do not. |
| A5 | What makes `grounded-research` integration-ready today? | A0–A1 | Complete | Tyler Stage 2/5/6 handoff and trace projection exist; a strict, versioned, provenance-complete workbench contract and workbench-case validation do not. |
| A6 | Do coordination claims or project-scoped memory change readiness? | A0 | Complete | No active global claim matched the four repos. Theory Forge's repo-local claim tool reported no active claims but several orphaned lanes. PT memory adds current operational/schema warnings but no export authorization or implementation. |
| A7 | Does the project graph identify a quantitative-text owner? | None | Complete | No. Exact quantitative-text match count is zero; only `prompt_eval` advertises statistical comparison, which is evaluation infrastructure, not an adapter owner. |
| A8 | Which gaps become program gates? | A2–A7 | Complete | Producer-owned versioned exports and provenance-first real fixtures precede workbench adapters; Grounded Research and Theory Forge are later optional tracks; quantitative-text ownership is required before any genuine mixed-methods claim. |

## Assumptions register

| # | Assumption | Confidence | How verified | Round | Status |
|---|---|---|---|---|---|
| 1 | Repository names in the task correspond to local directories under `~/projects`. | High | `pwd -P` succeeded for the four hyphen/underscore spellings named in this report; `/home/brian/projects/grounded_research` failed because it does not exist. | 1 | Confirmed, with spelling correction |
| 2 | A schema or fixture alone does not prove a producer can emit a conforming live export. | High | Traced each plan to code, callable writer, focused tests, committed/ignored fixtures, and runtime evidence. PT and Theory Forge have plans without export code; QC has code without the planned canonical fixture. | 2 | Confirmed |
| 3 | Clean Git status and recent commits indicate repository freshness, not integration readiness. | High | Three clean repositories still lack their required canonical workbench export/fixture. | 2 | Confirmed |
| 4 | Project graph metadata may name a prospective project without proving an assigned maintainer or implemented adapter. | High | Exact graph query returned zero quantitative-text adapter matches; no adjacent statistical project was reclassified as an owner. | 3 | Confirmed |
| 5 | A `verification.last_result: pass` manifest is sufficient to call a Theory Forge module runtime-green. | Low | Compared manifests to the repo's stronger definition and local function rows. Some in-flight manifests say pass while individual functions remain unverified; the repo requires actual stage execution and evidence. | 3 | **Wrong** — manifest pass is necessary but not sufficient |

## A0–A1: repository authority, Git state, and freshness

### Observed instruction authority

- QC says root `CLAUDE.md` is operational authority and `docs/PROJECT_THEORY_AND_GOALS.md` wins on status/claims; it explicitly forbids unqualified validated/SOTA claims (`/home/brian/projects/qualitative_coding/CLAUDE.md:5`). Its `AGENTS.md` says it is generated from `CLAUDE.md` and `scripts/relationships.yaml` (`/home/brian/projects/qualitative_coding/AGENTS.md:3`).
- PT's root authority defines the workbench method boundary and requires a future versioned adapter instead of importing `pt.schemas` or parsing `result.json` (`/home/brian/projects/process_tracing/CLAUDE.md:39`, `/home/brian/projects/process_tracing/CLAUDE.md:59`). Its `AGENTS.md` is a generated projection (`/home/brian/projects/process_tracing/AGENTS.md:3`).
- Theory Forge says sessions read `SESSION_PROGRESS.md` and identifies 39 runtime-green theories plus 27 schema-only theories (`/home/brian/projects/theory-forge/CLAUDE.md:7`, `/home/brian/projects/theory-forge/CLAUDE.md:15`). Its `AGENTS.md` is generated from root authority (`/home/brian/projects/theory-forge/AGENTS.md:3`). The session tracker is an April Plan 11 completion record, not the current Plan 107/108 authority (`/home/brian/projects/theory-forge/SESSION_PROGRESS.md:1`, `/home/brian/projects/theory-forge/SESSION_PROGRESS.md:120`).
- Grounded Research says root `CLAUDE.md` is canonical and names Tyler's four-file packet as implementation authority (`/home/brian/projects/grounded-research/CLAUDE.md:3`, `/home/brian/projects/grounded-research/CLAUDE.md:6`). Conflict: those same lines say `AGENTS.md` must mirror exactly, while `AGENTS.md` says it is a generated projection (`/home/brian/projects/grounded-research/AGENTS.md:3`, `/home/brian/projects/grounded-research/AGENTS.md:10`). Treat `CLAUDE.md` plus the Tyler packet as authoritative and the generated `AGENTS.md` as a loading projection until this wording is reconciled.

### Observed Git command results

Exact command, run in each repository at 2026-07-12T12:19:29-07:00:

```text
git status --short --branch
git rev-parse HEAD
git rev-list --left-right --count '@{upstream}...HEAD'
```

| Repository | Branch/upstream | HEAD | Ahead/behind | Dirt |
|---|---|---|---|---|
| `qualitative_coding` | `main...origin/main` | `22a948f57a848a8f6ca467757ecf8e2319b993c4` | `0 / 0` | clean |
| `process_tracing` | `master...origin/master` | `352bcfe1e6bec720f816987c51dae9c0fd89fa13` | `0 / 0` | `?? workbench/frontend/node_modules/` |
| `theory-forge` | `main...origin/main` | `21dfc432221ba246b70668d68da07a18d186a435` | `0 / 0` | clean |
| `grounded-research` | `main...origin/main` | `f0f7e341e81ccacdf73cb82dc6f06fdfdf4c8967` | `0 / 0` | clean |

Relevant history:

- QC's workbench commit `e4cf27e3` added only Plan 242 and its index row; current HEAD is a later backup/checkpoint commit. This explains why a workbench plan exists without its fixture.
- PT's workbench commit `82c8abf2` added only Plan 007, the plan index row, and an issue entry. Current HEAD is a later commit adding a separate local workbench application; it did not add `pt_export_v1`.
- Theory Forge's `20a4d44e` added Plan 108; current HEAD changes default models, not the workbench export.
- Grounded Research has July commits after the April plan/status docs, so status claims must be refreshed from code and artifacts rather than inherited solely from dated prose.

### Inference

The repositories are not stale clones, but documentation dates and checkpoint-style commits make branch freshness an insufficient readiness signal. PT's untracked dependency tree must be dispositioned before any producer-owned export slice begins, both to restore clean-state discipline and to avoid confusing the separate PT UI with the cross-repo artifact seam.

## A2: `qualitative_coding`

### Observed facts

1. **Method boundary is explicit.** QC owns coding, char/span anchors, patterns, claims, review, and QDA export; it must not emit PT likelihood/Bayesian semantics (`/home/brian/projects/qualitative_coding/CLAUDE.md:24`). The honest-state ledger calls the package a boundary artifact rather than causal/method-validity evidence (`/home/brian/projects/qualitative_coding/docs/PROJECT_THEORY_AND_GOALS.md:111`).

2. **Plan state has drift, but not in the direction of readiness.** Plans 239, 241, and 242 are all still indexed as planned (`/home/brian/projects/qualitative_coding/docs/plans/CLAUDE.md:5`). Plan 242 is blocked by Plan 241 and says a canonical workbench fixture has not been selected, regenerated, or documented (`/home/brian/projects/qualitative_coding/docs/plans/MIXED_METHODS_WORKBENCH_EXPORT_FIXTURE.md:3`, `/home/brian/projects/qualitative_coding/docs/plans/MIXED_METHODS_WORKBENCH_EXPORT_FIXTURE.md:13`). Plan 241 itself is still marked planned despite extensive implementation checkpoints and unchecked acceptance criteria (`/home/brian/projects/qualitative_coding/docs/plans/SOTA_METHODODOLOGY_PIPELINE_REALIGNMENT.md:1`, `/home/brian/projects/qualitative_coding/docs/plans/SOTA_METHODODOLOGY_PIPELINE_REALIGNMENT.md:138`). This is plan-truth drift, not authorization to proceed.

3. **A strict package implementation exists.** Every package model declares `extra="forbid"`; the package includes scope, document hashes, observed patterns, abductive candidates, analytic claims, anchors, caveats, and a small provenance object (`/home/brian/projects/qualitative_coding/qc_clean/core/process_tracing_handoff.py:37`, `/home/brian/projects/qualitative_coding/qc_clean/core/process_tracing_handoff.py:122`, `/home/brian/projects/qualitative_coding/qc_clean/core/process_tracing_handoff.py:132`). The validator rejects PT inference fields anywhere in the payload (`/home/brian/projects/qualitative_coding/qc_clean/core/process_tracing_handoff.py:23`, `/home/brian/projects/qualitative_coding/qc_clean/core/process_tracing_handoff.py:371`). A writer, loader, and CLI wrapper exist (`/home/brian/projects/qualitative_coding/qc_clean/core/process_tracing_handoff.py:309`, `/home/brian/projects/qualitative_coding/scripts/export_process_tracing_handoff.py:19`).

4. **The contract is narrower than the planned workbench export.** Claim scope is serialized as `dict[str, Any]`, and the package has no codebook/code/category collection (`/home/brian/projects/qualitative_coding/qc_clean/core/process_tracing_handoff.py:104`, `/home/brian/projects/qualitative_coding/qc_clean/core/process_tracing_handoff.py:142`). Provenance records only generation time, state hash, and producer name—no producer commit, export command, package hash, source command, or validation result (`/home/brian/projects/qualitative_coding/qc_clean/core/process_tracing_handoff.py:122`, `/home/brian/projects/qualitative_coding/qc_clean/core/process_tracing_handoff.py:300`). Plan 242 explicitly requires a producer commit and package hash (`/home/brian/projects/qualitative_coding/docs/plans/MIXED_METHODS_WORKBENCH_EXPORT_FIXTURE.md:91`).

5. **Focused validation is real but fixture-only.** Six focused tests cover package shape, dangling pattern/anchor rejection, forbidden PT inference, script CLI, and top-level CLI (`/home/brian/projects/qualitative_coding/tests/test_process_tracing_handoff.py:115`, `/home/brian/projects/qualitative_coding/tests/test_process_tracing_handoff.py:163`, `/home/brian/projects/qualitative_coding/tests/test_process_tracing_handoff.py:175`). Make exposes export and validation targets (`/home/brian/projects/qualitative_coding/Makefile:101`). The canonical `make check` runs deterministic tests, Ruff, and governance checks, but explicitly says type checking is not configured (`/home/brian/projects/qualitative_coding/Makefile:502`).

6. **No canonical workbench fixture exists.** `docs/fixtures/mixed_methods_workbench/` is absent. Three ignored reviewer-demo handoffs exist under `test_output/`; the inspected one is explicitly synthetic, includes provisional confidence values, and has only the small provenance object (`/home/brian/projects/qualitative_coding/test_output/reviewer_demo/handoff/process_tracing_handoff.json:1`, `/home/brian/projects/qualitative_coding/test_output/reviewer_demo/handoff/process_tracing_handoff.json:476`). Its observed SHA-256 was `47e96ae36469f03ae3b777aef123563482018b8bab3f98be3f85ea834e9ab785`; it is not tracked and does not satisfy Plan 242.

### Inference

The existing QC-to-PT package is the best implementation seed, but selecting it unchanged as the canonical workbench export would silently weaken the declared contract: code/category definitions, typed claim-scope structure, producer Git provenance, reproducible generation, and manifest validation evidence would still be missing. It can license a C-grade synthetic shape claim, not producer readiness.

### Readiness gates

1. Reconcile Plan 241's actual status and close or explicitly fence its remaining claim-discipline work before Plan 242.
2. Pre-make the export decision: extend the strict QC-to-PT package into a workbench-safe superset, or create a separate QC workbench artifact. Preserve PT-field rejection either way.
3. Require typed code/category and typed claim-scope fields; keep producer models strict.
4. Generate one governed, non-synthetic export from a declared QC project and record producer commit, exact command, project-state/source hashes, package hash, validation command/result, scope/governance, caveats, and evidence license.
5. Add negative controls for missing commit/hash/validation metadata and forbidden PT semantics before importing a pinned copy into the workbench.

## A3: `process_tracing`

### Observed facts

1. **The intended public boundary is unambiguous.** The workbench may consume comparative support only as intra-case ranking, not truth probability; absence findings cannot enter the Bayesian update; source coverage drives claim limits (`/home/brian/projects/process_tracing/CLAUDE.md:52`). The future seam is `pt_export_v1.json`, not `result.json` (`/home/brian/projects/process_tracing/CLAUDE.md:59`).

2. **Plan 007 is still wholly planned.** It names `pt/export.py`, `tests/test_export.py`, an optional Make target, a live run, and docs/status updates as future work (`/home/brian/projects/process_tracing/docs/plans/007_workbench_export_v1.md:3`, `/home/brian/projects/process_tracing/docs/plans/007_workbench_export_v1.md:54`, `/home/brian/projects/process_tracing/docs/plans/007_workbench_export_v1.md:112`). All acceptance boxes remain unchecked (`/home/brian/projects/process_tracing/docs/plans/007_workbench_export_v1.md:202`). Direct inspection found both `pt/export.py` and `tests/test_export.py` absent; no export fixture file was found.

3. **The internal model can populate most of the plan.** `Evidence` carries direct quote text plus source/document/citation labels when present, but no exact char offsets (`/home/brian/projects/process_tracing/pt/schemas.py:67`). Hypotheses carry mechanisms and observable predictions (`/home/brian/projects/process_tracing/pt/schemas.py:172`). Bayesian state exposes numeric comparative weights, robustness, top drivers, and sensitivity ranges/rank stability (`/home/brian/projects/process_tracing/pt/schemas.py:360`, `/home/brian/projects/process_tracing/pt/schemas.py:376`). Absence findings expose severity, would-be-extractable, expected genre/location, and reasoning (`/home/brian/projects/process_tracing/pt/schemas.py:471`). `ProcessTracingResult` includes source hash, source packet, coverage, partition audit, diagnostic matrix, and synthesis (`/home/brian/projects/process_tracing/pt/schemas.py:700`).

4. **Source provenance is marker-level, not offset-level.** Source packet candidates define exact text markers, and deterministic coverage maps marker occurrences to evidence IDs (`/home/brian/projects/process_tracing/pt/source_packet.py:23`, `/home/brian/projects/process_tracing/pt/source_coverage.py:23`). Therefore, a truthful first export can carry quote text, packet source IDs/markers, and coverage status; it cannot claim exact source offsets without a new producer capability.

5. **Real local result artifacts exist but are internal and ignored.** The inspected Brumaire result/report pair under `output/live_plan003_slice1_brumaire_openrouter_20260622_075208/` had SHA-256 values `405ac298...` and `276dbbfd...`; `output/` is ignored. The source packet and assembled text are tracked and hashed, but no public export was generated. Existing evidence notes explicitly cap the early source-packet run below A because of unresolved source gaps (`/home/brian/projects/process_tracing/evidence/current/Evidence_Plan003_Slice1_SourcePacketContract.md:153`).

6. **The canonical check surface is still a known defect.** `ISSUE-002` records that `make check` used global `pytest`, failed 11 tests, while the repo-local interpreter passed 385 with 2 skips; it also records missing local `mypy` and six global mypy errors (`/home/brian/projects/process_tracing/ISSUES.md:49`). The current Make recipe still invokes bare `pytest` and bare `mypy` (`/home/brian/projects/process_tracing/Makefile:236`). Plan 007 is explicitly blocked on this for final check reliability (`/home/brian/projects/process_tracing/docs/plans/007_workbench_export_v1.md:6`).

7. **Worktree is not clean.** `git status --short` reports untracked `workbench/frontend/node_modules/`. This is dependency output from the separate PT UI, not evidence of a public workbench export.

### Inference

The handoff uncertainty about marker versus offset behavior is now resolved from current code: marker/quote provenance is available; stable char offsets are not. The numeric representation is also available internally, and Plan 007 already chooses an explicitly named comparative-support weight plus sensitivity bounds. What remains is a producer-owned projection with claim limits and semantic labels, not schema discovery.

### Readiness gates

1. Disposition the untracked dependency tree and fix `ISSUE-002` so one repo-local `make check` is trustworthy.
2. Implement strict `pt_export_v1` producer models and a CLI/Make writer without exposing the raw likelihood matrix.
3. Export numeric comparative-support weights only with explicit intra-case semantics, robustness/sensitivity/rank stability, and no generic confidence/probability label.
4. Encode current provenance truthfully as packet source ID/marker + quote text + coverage; either defer offsets or add/test a producer-owned offset capability before promising them.
5. Run one source-packet-backed real case, audit the underlying result/report, generate and validate the public export, and commit a provenance-complete fixture plus invariant-specific negative controls.

## A4: `theory-forge`

### Observed facts

1. **Plan 107 and Plan 108 remain open.** Plan 107 is in progress with all 27 acceptance rows unchecked (`/home/brian/projects/theory-forge/docs/plans/107_phase1_bulk_compilation.md:1`, `/home/brian/projects/theory-forge/docs/plans/107_phase1_bulk_compilation.md:56`). Plan 108 is planned and blocked until Plan 107 is completed or explicitly fenced with a known-green theory (`/home/brian/projects/theory-forge/docs/plans/108_mixed_methods_operationalization_export.md:1`). No `src/theory_forge/contracts/workbench_export.py` and no `docs/fixtures/mixed_methods_workbench/` directory exist; the only `TheoryOperationalizationArtifact` references are in Plan 108.

2. **v14 is runtime authority; v15 is an optional-field extension.** Package code selects `meta_schema_v14.json` (`/home/brian/projects/theory-forge/src/theory_forge/__init__.py:28`). Both strict JSON schemas exist (`/home/brian/projects/theory-forge/src/theory_forge/schemas/meta_schema_v14.json:1`, `/home/brian/projects/theory-forge/src/theory_forge/schemas/meta_schema_v15.json:1`). The v15 test enumerates all 66 theory schemas, validates them against v15, and asserts the v15 fields are optional (`/home/brian/projects/theory-forge/tests/test_v15_schema.py:19`, `/home/brian/projects/theory-forge/tests/test_v15_schema.py:114`). Plan 108 correctly requires recording the source schema version rather than pretending one label covers both (`/home/brian/projects/theory-forge/docs/plans/108_mixed_methods_operationalization_export.md:49`).

3. **Docs and local compiled cache are not one truth surface.** The roadmap says 39 runtime-green and 27 schema-only, last updated April 5 (`/home/brian/projects/theory-forge/docs/ROADMAP.md:3`, `/home/brian/projects/theory-forge/docs/ROADMAP.md:15`). Read-only local-cache counts found 72 directories, 45 manifests, 43 `last_result: pass`, one fail, one without a result, and 27 directories without manifests. Some in-flight manifests say pass while individual functions remain unverified; this is why the repo's definition requires actual stage execution plus evidence, not just a pass label (`/home/brian/projects/theory-forge/CLAUDE.md:21`).

4. **A relatively coherent candidate exists, but proof freshness is incomplete.** The Scale-Free Network Theory manifest is paper-sourced, contains exactly one extraction and one qualitative stage, reports 38 passing tests, and marks its single function verified (`/home/brian/.theory-forge/compiled/scale_free_network_theory_barabasi_1999/manifest.yaml:1`). The roadmap independently describes it as paper-sourced and 2/2 green (`/home/brian/projects/theory-forge/docs/ROADMAP.md:57`). However, no repo-controlled runtime evidence file matching Barabási surfaced; Plan 108 still leaves the first fixture theory open (`/home/brian/projects/theory-forge/docs/plans/108_mixed_methods_operationalization_export.md:96`). This makes it a candidate for fresh verification, not a preselected authority.

5. **The export must remain data-only.** Plan 108 requires constructs, mechanisms, hypotheses/propositions, indicators, assumptions, scope conditions, uncertainty, validation obligations, provenance, and only references to compiled functions/manifests (`/home/brian/projects/theory-forge/docs/plans/108_mixed_methods_operationalization_export.md:45`, `/home/brian/projects/theory-forge/docs/plans/108_mixed_methods_operationalization_export.md:80`). ADR-0003 keeps AC14 deferred and confirms Theory Forge has no Phase 1–3 dependency on it (`/home/brian/projects/theory-forge/docs/adr/0003-ac14-integration-deferred.md:12`). No evidence supports making AC15 a prerequisite.

6. **Project command surface has drift.** `make help` exits with `No rule to make target 'help'`. `make check` runs tests and mypy but no lint despite its description (`/home/brian/projects/theory-forge/Makefile:218`). This does not invalidate existing theory artifacts, but it prevents treating the Make interface as a clean producer readiness gate.

### Inference

The v14/v15 issue should be closed as a version-declaration decision: export the exact selected source schema version and optionally record which compatible meta-schema validators passed. Do not block on converting the runtime wholesale to v15. The larger blocker is choosing and freshly proving one theory whose source provenance, manifest, stage execution, and uncertainties agree.

### Readiness gates

1. Explicitly pause/fence Plan 107 for the export slice or complete it; do not let an indefinite bulk-compilation wave obscure Plan 108 authority.
2. Repair `make help`/`make check` truth or name an explicit verified command set for the selected theory.
3. Select one paper-sourced theory only after a fresh schema validation, manifest inspection, property tests, and non-mocked runtime run produce repo-controlled evidence. Scale-Free Network Theory is the least contradictory candidate observed, not an automatic choice.
4. Define a strict, versioned `TheoryOperationalizationArtifact` with exact v14/v15 source declaration, producer commit, source paper/schema hashes, manifest reference/hash, generated time, package hash, validation commands/results, scope/assumptions/uncertainties, and no live AC dependency.
5. Commit one fixture and negative controls; license it only as theory specification context, never empirical evidence.

## A5: `grounded-research`

### Observed facts

1. **The repo is operational and adjudication-centered.** It accepts raw questions or imported bundles, performs independent analyses, claim-ledger canonicalization, dispute detection, fresh-evidence verification, and export (`/home/brian/projects/grounded-research/CLAUDE.md:19`). The canonical plan says v0.1.0 shipped and maps the live path to `report.md`, `summary.md`, `trace.json`, and `handoff.json` (`/home/brian/projects/grounded-research/docs/PLAN.md:27`, `/home/brian/projects/grounded-research/docs/PLAN.md:35`).

2. **A typed handoff exists, but it is not workbench-versioned.** `TylerDownstreamHandoff` directly contains the question and Stage 2/5/6 artifacts, defaults its target to `onto-canon`, and records only generated time (`/home/brian/projects/grounded-research/src/grounded_research/models.py:308`). The builder and writer preserve those stage artifacts and emit `handoff.json` (`/home/brian/projects/grounded-research/src/grounded_research/export.py:581`, `/home/brian/projects/grounded-research/src/grounded_research/export.py:913`). No explicit strict `ConfigDict(extra="forbid")`, schema version, producer commit, command, input/trace hash, or package hash appears in these public models.

3. **Focused tests prove the internal projection.** Seventeen export tests exist. The key tests prove Tyler trace projection, partial-failure trace emission, and direct preservation of Stage 2/5/6 in the downstream handoff (`/home/brian/projects/grounded-research/tests/test_export.py:1123`, `/home/brian/projects/grounded-research/tests/test_export.py:1175`, `/home/brian/projects/grounded-research/tests/test_export.py:1202`). They do not test a supported workbench schema major, producer provenance, package hash, or contested QC/PT input.

4. **Observed live artifacts are local/ignored and onto-canon-specific.** The inspected cash-transfer handoff has exactly six top-level fields, targets `onto-canon`, and begins with Stage 2 source evidence (`/home/brian/projects/grounded-research/output/workbench_fba66f8df044_does_cash_transfer_programs_reduce_pover/handoff.json:1`). It has no `schema_version`; observed SHA-256 was `dc9dc92e545e9031e3abbbff9d82b5f45741bab01615c68cca23e37fc4c4ab49`. `output/` is ignored, so this is runtime evidence of the internal path, not a durable workbench fixture.

5. **Internal competitive evidence does not establish workbench validity.** The six-question comparison is single-judge, same-team, and uses cached competitor outputs; its own caveats say the sample is too small and not statistically significant (`/home/brian/projects/grounded-research/docs/COMPETITIVE_ANALYSIS.md:5`, `/home/brian/projects/grounded-research/docs/COMPETITIVE_ANALYSIS.md:23`). The plan's claimed current frontier also contains contradictory historical/current statements, including both no open local rows and a later statement that prior closure was inaccurate (`/home/brian/projects/grounded-research/docs/PLAN.md:168`, `/home/brian/projects/grounded-research/docs/PLAN.md:217`). Fresh code/artifact checks must dominate summary prose.

6. **`make check` is not fail-loud.** Pytest is enforced, but Ruff and mypy are each suffixed with `|| true` (`/home/brian/projects/grounded-research/Makefile:34`). This surface cannot certify lint/type readiness.

### Inference

Grounded Research is much closer to being an optional workbench adjudication producer than a blank-slate repo: its core ledger/dispute/trace objects and runtime path exist. The missing work is boundary hardening and evaluation on workbench-shaped contested claims. Reusing `TylerDownstreamHandoff` unchanged would expose an onto-canon-specific, unversioned contract without reproducible provenance.

### Readiness gates

1. Define the workbench adjudication input/output question: which bounded QC/PT conflicts are eligible, what must remain method-specific, and what Grounded Research may update versus annotate.
2. Add a strict, versioned producer projection with supported major, producer/input/trace hashes, exact generation/validation command, package hash, caveats, and no implicit `onto-canon` target.
3. Make lint and mypy real gates or explicitly exclude them with evidence rather than swallowing failures.
4. Curate negative controls and at least one real contested-claim case from future pinned QC/PT fixtures; evaluate arbitration lineage, source grounding, status-change basis, and abstention/unresolved behavior.
5. Keep release 0.2 off the release-0.1 critical path.

## A6: coordination and memory

### Observed commands and results

- `rg -n -i 'qualitative_coding|process_tracing|theory-forge|grounded-research|mixed_methods' ~/.claude/coordination/claims` returned no matches at inspection time.
- Theory Forge's repo-local `python scripts/meta/worktree-coordination/check_claims.py --list` returned `No active claims` and listed several orphaned worktrees. The other three repos expose no repo-local claim script at the checked standard paths.
- `agent-memory recall 'active decisions' --project qualitative_coding` returned generic task outcomes, not an active export decision.
- The same command for PT returned three active operational findings: preferred live E2E model, actual pass ordering, and a warning that internal Pydantic models use default extra-ignore behavior. None authorizes or implements Plan 007.
- Theory Forge and Grounded Research recalls returned generic historical task outcomes, not active export ownership or blockers.

### Inference

There is no current claim collision preventing later producer-owned work. That is a freshness observation, not authorization. Re-run claims and targeted memory immediately before opening any producer implementation slice; Theory Forge's orphaned worktrees also merit cleanup/disposition under its own workflow.

## A7: quantitative-text owner/status

### Observed facts

The project graph describes the workbench as active but dependent only on `qualitative_coding` and `process_tracing` (`/home/brian/projects/project-meta/PROJECT_GRAPH.json:1363`, `/home/brian/projects/project-meta/PROJECT_GRAPH.json:1383`). Exact read-only query:

```text
jq '[.[] | select(all searchable id/name/one_liner/tags/capabilities text matching "quantitative[-_ ]?text|text[-_ ]?quantitative")] | length' PROJECT_GRAPH.json
=> 0
```

A broader capability query found only `prompt_eval` through `statistical-comparison`. That project is evaluation infrastructure, not a declared quantitative-text producer or adapter owner. No graph evidence names a task, corpus, measurement instrument, adapter boundary, maintainer, or implementation status.

### Conclusion

**Null result: there is no verifiable quantitative-text adapter owner in the local project graph as of 2026-07-12.** Do not assign the role to `prompt_eval`, PT cross-case analysis, or any adjacent repo by inference. The workbench remains multi-method qualitative until a human names the task and owner and the strand is independently evaluated.

## Batch contractions

### Contraction 1 — authority and Git state

All four producer repos are identifiable and upstream-synchronized, so missing work is not explained by wrong paths or diverged branches. The remaining search can focus on public artifact seams. PT's untracked dependency tree and Grounded Research's AGENTS wording conflict are localized governance issues, not evidence that exports exist elsewhere.

### Contraction 2 — export implementation

Only QC and Grounded Research have callable export/handoff code today. QC's contract is strict but incomplete for its own workbench plan; Grounded Research's contract is operational but unversioned and onto-canon-specific. PT and Theory Forge have plan-only workbench exports. Therefore the program must not begin by building workbench adapters around internal `result.json`, compiled caches, or ignored handoffs.

### Contraction 3 — evidence and version truth

Existing ignored/live artifacts prove that PT and Grounded Research can produce internal results, not stable cross-repo contracts. Theory Forge's v14/v15 ambiguity contracts to a source-version/provenance decision. The critical evidence gap across all seams is not JSON shape; it is reproducible producer-owned generation plus validation, provenance, negative controls, and claim licensing.

### Contraction 4 — program dependency

Release 0.1 depends on governed source selection plus QC/PT public exports and pinned real fixtures. Grounded Research and Theory Forge remain independent later tracks. A true mixed-methods claim remains blocked by the explicit quantitative-strand ownership null.

## Cross-producer readiness gates, in dependency order

1. **Program/source governance gate:** confirm the first public case, corpus denominator, source identities/hashes, licensing, privacy/publication terms, anchor recoverability, and claim limits.
2. **QC producer gate:** close/fence Plan 241, select the canonical export, generate one provenance-complete real artifact, validate it, and add negative controls.
3. **PT producer gate:** clean state, repair canonical checks, implement strict `pt_export_v1`, generate/audit one source-packet-backed real artifact, and add negative controls.
4. **Pinning gate:** only after both producer gates pass, copy immutable QC/PT fixtures into the workbench with producer commits, source/package hashes, exact commands/results, supported majors, governance, caveats, and licensed claims.
5. **Release-0.1 authorization gate:** real fixtures still do not authorize adapters. Brian must name the implementation slice; then run the workbench pre-implementation checklist. The licensed claim is multi-method qualitative, not mixed methods.
6. **Grounded Research gate (later):** define a workbench-specific adjudication projection and evaluate contested QC/PT claims; do not inherit internal benchmark claims.
7. **Theory Forge gate (later):** fence Plan 107, freshly prove one paper-sourced theory, implement Plan 108's strict data-only artifact, and keep theory separate from evidence.
8. **Quantitative-text gate (required for genuine mixed methods):** Brian names owner, task, estimand/measure, instrument, held-out protocol, leakage controls, item-level links to qualitative constructs, and uncertainty/meta-inference rules. Update the project graph only after that decision is real.

## Conflicts, drift, and null results

| Item | Observed conflict/null | Disposition |
|---|---|---|
| Grounded Research authority wording | `CLAUDE.md` says AGENTS mirrors exactly; generated AGENTS says projection. | Treat CLAUDE/Tyler packet as authority; fix wording before governance enforcement depends on exact equality. |
| QC plan truth | Plan 241 is planned but contains extensive implementation checkpoints; Plan 242 remains blocked and fixture absent. | Reconcile plan state before export implementation. |
| PT check truth | Issue says global-runtime check is unreliable; Makefile still uses bare tools. | Repair before Plan 007 completion. |
| PT provenance | Marker/quote lineage exists; char offsets do not. | V1 must declare marker-level provenance or add an offset capability. |
| Theory Forge versions | Runtime uses v14; all 66 are tested against v15 optional extensions. | Record exact source schema + compatible validators; no wholesale migration assumption. |
| Theory Forge health | Docs say 39/27; local cache contains additional partial/pass/fail artifacts. | Select via fresh end-to-end proof, not directory/manifest count. |
| Grounded Research checks | Ruff/mypy failures are swallowed. | Not a certification gate until fail-loud. |
| Quantitative-text owner | Exact graph match count is zero. | Human decision required; no inferred owner. |
| `grounded_research` directory | Absent. | Canonical local spelling is `grounded-research`. |

## Freshness triggers

Re-run the corresponding checks when any trigger occurs:

| Trigger | Minimum refresh |
|---|---|
| Any producer HEAD changes | Git status/log; relevant plan/index; export code/tests/fixtures; Make help/check recipe. |
| Before opening a producer slice | Global/repo-local claims; targeted `agent-memory recall`; worktree list; upstream divergence. |
| QC Plan 241/242 status changes | Re-evaluate canonical export choice, required fields, fixture provenance, and evidence license. |
| PT `ISSUE-002` or Plan 007 changes | Re-run `make help`, inspect/execute the repaired repo-local gate, and verify public export code/fixture. |
| Theory Forge Plan 107 closes/pauses | Recount canonical runtime-green theories from repo-controlled evidence; select and freshly run the candidate; re-check v14/v15 source declaration. |
| Grounded Research contract/benchmark changes | Verify schema major/provenance and run workbench contested-claim controls rather than inheriting internal scores. |
| Project graph gains a quantitative-text dependency | Verify owning repo, maintainer/decision authority, task, code, test protocol, and status independently. |
| Public SOTA/validity claim is contemplated | Require independent benchmark evidence; none of the inspected artifacts licenses that claim today. |

## Commands consulted

Read-only command families used:

- `git status --short --branch`, `git rev-parse HEAD`, upstream divergence, `git log -5`, `git show --stat`
- `rg --files`, `rg -n`, `find`, `nl -ba`, `sed`, `stat`, `sha256sum`, `jq`
- `make help` only (QC/PT/Grounded succeeded; Theory Forge had no target)
- global claims search and Theory Forge repo-local `check_claims.py --list`
- `agent-memory recall 'active decisions' --project <repo>`

Not run: `make check`, pytest/mypy/Ruff, live LLM pipelines, export writers, install/build commands, network queries, source acquisition, or worktree/claim mutation.

## Primary files consulted

### Workbench / ecosystem

- `/home/brian/projects/mixed_methods_workbench/worktrees/goal-sota-program/.claude/tasks/session_context.md`
- `/home/brian/projects/mixed_methods_workbench/worktrees/goal-sota-program/.claude/HANDOFF.md`
- `/home/brian/projects/mixed_methods_workbench/worktrees/goal-sota-program/.claude/handoff.yml`
- `/home/brian/projects/project-meta/PROJECT_GRAPH.json`

### Qualitative Coding

- `CLAUDE.md`, `AGENTS.md`, `Makefile`
- `docs/PROJECT_THEORY_AND_GOALS.md`
- `docs/plans/CLAUDE.md`, `docs/plans/ACTIVE_SPRINT.md`
- `docs/plans/AGENT_DRIVABLE_SANITIZATION_WORKFLOW.md`
- `docs/plans/SOTA_METHODODOLOGY_PIPELINE_REALIGNMENT.md`
- `docs/plans/MIXED_METHODS_WORKBENCH_EXPORT_FIXTURE.md`
- `docs/plans/completed/PROCESS_TRACING_HANDOFF_PACKAGE.md`
- `qc_clean/core/process_tracing_handoff.py`
- `scripts/export_process_tracing_handoff.py`, `scripts/validate_process_tracing_handoff.py`
- `tests/test_process_tracing_handoff.py`
- ignored `test_output/reviewer_demo/handoff/*.json`

### Process Tracing

- `CLAUDE.md`, `AGENTS.md`, `Makefile`, `ISSUES.md`
- `docs/plans/CLAUDE.md`, `docs/plans/007_workbench_export_v1.md`
- `docs/PROJECT_THEORY_AND_GOALS.md`, `docs/SOTA_PLUS_TARGET_ARCHITECTURE.md`
- `docs/ARTIFACTS.md`, `docs/VALIDATION.md`
- `pt/schemas.py`, `pt/source_packet.py`, `pt/source_coverage.py`
- `evidence/current/Evidence_Plan003_Slice1_SourcePacketContract.md` and other current Plan 003 evidence inventory entries
- `docs/source_packets/18_BRUMAIRE_SOURCE_PACKET.json`
- `input_text/source_packets/18_brumaire_source_packet.txt`
- ignored `output/*/result.json` and `report.html` inventory, with one Brumaire pair inspected/hashes recorded

### Theory Forge

- `CLAUDE.md`, `AGENTS.md`, `SESSION_PROGRESS.md`, `Makefile`, `README.md`
- `docs/ROADMAP.md`, `docs/plans/CLAUDE.md`
- `docs/plans/107_phase1_bulk_compilation.md`
- `docs/plans/108_mixed_methods_operationalization_export.md`
- `docs/adr/0003-ac14-integration-deferred.md`
- `src/theory_forge/__init__.py`
- `src/theory_forge/schemas/meta_schema_v14.json`, `meta_schema_v15.json`
- selected bundled theory schemas and `tests/test_v15_schema.py`
- `evidence/phase1_batch/` inventory and automation-baseline inventory
- selected local manifests under `~/.theory-forge/compiled/`, especially Framing, Shannon, Agenda Building, Critical Discourse Analysis, Differential Association, and Scale-Free Network Theory

### Grounded Research

- `CLAUDE.md`, `AGENTS.md`, `Makefile`
- `docs/PLAN.md`, `docs/ROADMAP.md`, `docs/FEATURE_STATUS.md`, `docs/COMPETITIVE_ANALYSIS.md`
- `docs/plans/CLAUDE.md`, `docs/TYLER_SPEC_GAP_LEDGER.md` search results
- `src/grounded_research/models.py`, `tyler_v1_models.py`, `export.py`, `ingest.py`
- `tests/test_export.py`, `tests/test_tyler_v1_models.py`, fixture inventory
- ignored output inventory and `output/workbench_fba66f8df044_does_cash_transfer_programs_reduce_pover/handoff.json`

## Synthesis

### Root cause

The workbench is not blocked by a lack of internal producer capability. It is blocked by a lack of **durable public seams whose provenance and evidence license are at least as strong as their shape**. Internal models, ignored live outputs, synthetic fixtures, and compiled caches are abundant; producer-owned versioned projections with reproducible generation, negative controls, committed real fixtures, and independent methodological evidence are not.

### Impact

- Building adapters now would couple the workbench to unstable internals or incomplete artifacts.
- Calling QC+PT “mixed methods” would still be methodologically false because no quantitative strand exists.
- Theory Forge and Grounded Research can enrich later releases, but neither should delay the QC/PT walking skeleton.
- No inspected producer or fixture licenses a SOTA/beyond-SOTA claim; those claims require the long-term benchmark program and independent sign-off.

### Recommendation

Keep the immediate workbench lane documentation-only and provenance-first. Close T0's fixture-inventory invariant locally, then use this report to open bounded producer-owned documentation/planning slices in dependency order. The first implementation work should occur only after the named producer plan is authorized and its repo-local gates are repaired. The critical path remains: source governance → real QC export → real PT export → pinned fixtures → explicit release-0.1 authorization. Quantitative-text ownership is a separate human decision gate before release 0.4.

### Confidence and limits

**Overall confidence: High** for repository, plan, code, fixture, command-surface, Git, claims, and project-graph state at the freshness timestamp. **Medium** for conclusions derived from untracked/ignored runtime outputs and user-local Theory Forge compiled caches, because those artifacts are not portable or independently rerun here. This static investigation cannot establish current dependency solvability, actual full-suite pass/fail, live LLM behavior, deployed freshness, methodological validity, or benchmark superiority.
