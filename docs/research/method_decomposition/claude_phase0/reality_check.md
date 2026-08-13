# Phase 0 Reality Check — Independent Candidate (rev 5.1)

**Status:** `independent_candidate`. Produced without inspecting `ac27ab2`'s
rows, edges, or findings (rev 5.1 §0.1). Not yet migrated or compared.

**Repository provenance:** see `repository_snapshots.yaml` for the exact
commit SHA, branch, and clean/dirty status recorded for every inspected
repository, and for which claims are revision-uncertain. Read that file
before treating any citation below as current. In particular:
**`process_tracing` has confirmed-drifted since inspection** — a new merge
(PR #83) landed after the sub-agent that produced
`pt_core_rival_explanation` and `pt_source_acquisition` finished its read.
No exact inspected SHA was captured contemporaneously for
`qualitative_coding`, `process_tracing`, `theory-forge`, or `data-contracts`
(only `mixed_methods_workbench`'s SHA was captured at the time); those four
repos' findings are therefore "presumed unchanged, not proven" except
`process_tracing`, which is "confirmed changed." No claim in this document
should be read as asserting current-moment truth about `process_tracing`'s
present state.

> **Interpretation note.** The 74.4% result measures callable software
> implementation across this selected Phase 0 workflow set. It does not
> estimate automation coverage of policy analysis generally, methodological
> validity, result quality, or unattended execution.

## Branch taken, in one paragraph

**Aggregate branch: PASS** — 29 of 39 eligible denominator operations
(74.4%) are `software_executable`, a strict majority. **But two of the five
analytic methods fail individually while the aggregate passes**:
`pt_source_acquisition` lands at exactly 50% (the exact-half case, which
rev 5.1 defines as FAIL, not a rounding tie) and `mist_trail_policy_appraisal`
lands at 0% — every one of its six analytic operations is manually
performed behind a well-built, typed, validated, hash-bound, API-and-UI-served
artifact. Per §8.4, both failing methods are excluded from any promotion
claim even though the aggregate branch is PASS, and Mist Trail's failure is
reported first because it is the starkest instance of the exact trap this
exercise exists to catch: representation quality with zero automated
execution behind it.

---

## 1. Abort gate — per-method table

Denominator = required `analytic` ideal operations for the frozen variant,
plus `methodological_support` operations an authoritative source actually
requires (cited per-row in `step_ledger.yaml`). `runtime_delivery`
operations are excluded from the denominator entirely (recorded in the
ledger, not here). The denominator is the count of **distinct ideal
operations**, not ledger rows — where one ideal operation has more than one
code realization (e.g. `pt_source_acquisition` screen/admit), it is counted
once, using the realization actually in scope for the named Phase-0
workflow (see §3 below for the full accounting of why).

| method | analytic ideal ops (denominator) | software_executable | manually_performed | incomplete_software | not_implemented | share | branch |
|---|---:|---:|---:|---:|---:|---:|---|
| `qc_grounded_theory` | 11 | 9 | 1 | 1 | 0 | 81.8% | PASS |
| `pt_core_rival_explanation` | 11 | 11 | 0 | 0 | 0 | 100.0% | PASS |
| `pt_source_acquisition` | 4 | 2 | 1 | 0 | 1 | 50.0% | **FAIL (exact half)** |
| `theory_forge_cpt_choices13k` | 7 | 7 | 0 | 0 | 0 | 100.0% | PASS |
| `mist_trail_policy_appraisal` | 6 | 0 | 6 | 0 | 0 | 0.0% | **FAIL** |
| **Aggregate** | **39** | **29** | **8** | **1** | **1** | **74.4%** | **PASS** |

`theory_forge_compile_apply` is **not a row in this table** — it has zero
denominator-eligible ideal operations by design (see `sources.md` §4 and
`step_ledger.yaml` header comment); it contributes `0/0`, not `0/N`, and is
excluded from the table rather than reported as a failing method, per the
distinction the spec draws between "no ideal exists" and "ideal exists but
unimplemented."

**With vs. without post-mapping `operation_kind` reclassifications
(§5.0a guard 3):** identical. `operation_kind` was frozen from the sources
before code inspection for every method that has a source, and no
reclassification was made after seeing the code. The share is 74.4% in
both cases. This itself is a finding worth stating plainly: the absence of
any reclassification is not because none was tempting — `qc_grounded_theory`
steps .10/.11 (adequacy diagnostic vs. adequacy determination) and
`pt_source_acquisition` step .01 (gap-scoring) were the closest calls, and
both were resolved by checking what the source actually specifies, not by
what would move the denominator.

---

## 2. Status validity table (§5.0), full ledger (58 rows, all `operation_kind`)

| execution ↓ / representation → | implemented_artifact | designed_only | methodology_reference_only | missing |
|---|---:|---:|---:|---:|
| **software_executable** | 45 | 0 | 0 | 1 |
| **manually_performed** | 8 | 0 | 0 | 1 |
| **incomplete_software** | 2 | 0 | 0 | 0 |
| **not_implemented** | 0 | 0 | 0 | 1 |

Total = 58, matching the full ledger row count. No invalid combinations
were assigned.

**The four occupied cells that matter most:**

- **`manually_performed` × `implemented_artifact` (8 rows) — the trap this
  project is watching for.** All 6 Mist Trail analytic rows
  (`mist_trail_policy_appraisal.01-06`) plus QC's manual-coding alternate
  path (`qc_grounded_theory.14`) plus PT's interactive-companion source
  screening (`pt_source_acquisition.03`). Every one of these is a typed,
  validated, often hash-bound, sometimes API/UI-served artifact whose
  actual analytical content was authored by a person, not derived by
  software. Mist Trail is the cleanest and most complete instance: nine
  rows of genuinely excellent engineering (Pydantic cross-validation, SHA-256
  binding, dual API+UI serving) sit on top of six rows of purely
  human-authored judgment, and the project's own planning document says so
  explicitly ("no model call or automated source interpretation").
- **`manually_performed` × `missing` (1 row) — performed and not
  recorded.** `qc_grounded_theory.11`, the theoretical-adequacy
  determination. There is no durable artifact anywhere recording that a
  human decided the categories were adequate; it is a pure off-system
  judgment gate, exactly matching the docs' own honesty about this
  ("fixed-corpus adequacy is not theoretical saturation").
- **`software_executable` × `missing` (1 row) — runs but leaves no
  durable, traceable artifact.** `theory_forge_compile_apply.08`, the
  compiled-theory manifest-verification gate. The gate is real, tested
  code (confirmed executing via a live pytest-subprocess trace for at
  least one theory), but 37 of the 39 theories `CLAUDE.md` describes as
  "runtime-green" have no durable evidence checked into this repository —
  their compiled-module cache (`~/.theory-forge/compiled/`) does not exist
  on the inspecting machine. Only 2/39 (`plan12_cognitive_dissonance`,
  the Shannon automation-baseline case) have a committed manifest
  snapshot. The mechanism is sound; the claim's current
  machine-independent traceability is not.
- **`not_implemented` × `missing` (1 row) — empty scaffolding, honestly
  absent.** `pt_source_acquisition.06`, reconciling conflicting source
  assessments on the single-case companion path. No code exists for this
  on that path at all — not a stub, not a schema, nothing. (An analogous
  operation does exist in PT's separate bulk/comparative pipeline,
  demonstrating the operation is buildable, but it is a structurally
  different pipeline out of this workflow's scope.)

---

## 3. One-to-many / many-to-one mappings and divergent-execution alternates

Reported honestly per rev 5.1's explicit instruction, rather than
collapsed to keep the denominator simple:

1. **`qc_grounded_theory` open coding + constant comparison (.02/.03) are
   bundled into one code path.** The per-segment LLM call in
   `gt_constant_comparison.py` performs both the open-coding judgment and
   the comparison-against-existing-codebook judgment in a single call; the
   deterministic `_merge_segment_results` that follows is bookkeeping, not
   the comparison itself. Two ideal operations map to one code
   realization (many-to-one at the code level, though both remain
   analytic and `software_executable`, so this does not change the
   denominator outcome — it changes what "software_executable" is actually
   crediting).
2. **`qc_grounded_theory` open coding has two code realizations with
   divergent execution status**: the default LLM pipeline path (.02,
   `software_executable`) and a human-authored manual-coding path (.14,
   `manually_performed`). Both are legitimate, shipped code paths for the
   same ideal operation. The denominator counts this ideal operation once,
   using the default/primary pipeline path (.02), and records the manual
   alternative separately in the ledger rather than silently dropping it.
3. **`pt_source_acquisition` screen/admit (.03) has two structurally
   different implementations with opposite execution status**, and this is
   the most consequential one-to-many finding in the whole exercise: the
   interactive single-case companion path (`acquisition_session.py`,
   `manually_performed` — confirmed zero `call_llm` calls in that file)
   and the separate bulk/comparative-case "revolution" pipeline
   (`revolution_source_development.py`, `software_executable`, with a
   genuinely independent second-LLM pair-review). **The same repository
   proves the operation is automatable and chooses not to automate it on
   the path that actually companions the in-scope single-case core
   workflow.** The denominator counts the in-scope (interactive) path.
   Counting the bulk-pipeline realization instead would flip
   `pt_source_acquisition`'s share from 50% (FAIL) to 75% (PASS) — which is
   exactly why rev 5.1 requires reporting this kind of divergence rather
   than picking whichever realization is convenient.
4. **`pt_core_rival_explanation` diagnostic-type classification (.04) is
   executed but functionally inert downstream.** PT's own docs
   (`docs/PROJECT_THEORY_AND_GOALS.md:141-142`) claim the Van Evera
   diagnostic-type field is "not yet repopulated by the new pass" — this is
   **stale and refuted** by current code: the field is populated by a
   genuinely separate, validated LLM call and deterministically enforced
   for completeness. However, the numeric discriminator-strength grading
   that actually governs evidence weighting is computed purely from
   `abs(log_lr)` thresholds in `pass_diagnostic.py` and never reads the Van
   Evera label at all. The classification is real and stored
   (`software_executable`, correctly counted in the denominator as such),
   but the Van Evera *typology*'s causal role in the method's actual
   discrimination grading is cosmetic. This is a one-to-one mapping with a
   functional caveat, not a one-to-many mapping, and is recorded here
   rather than in the ledger to keep the ledger's execution_status field
   honest about what genuinely executes versus what genuinely matters
   downstream — two different questions.

---

## 4. Mist Trail — representation and execution, kept separate (§8.3 Task 1)

| element | representation_status | execution_status | evidence |
|---|---|---|---|
| options | implemented_artifact | manually_performed | `decision_packet.json:142-169`, literal authored strings |
| consequences | implemented_artifact | manually_performed | `decision_packet.json:186-204`, 18 hand-written entries; plan doc: "no model call or automated source interpretation" |
| criterion_judgments | implemented_artifact | manually_performed | `decision_packet.json:206-212`, `author_role: "Workbench reviewer"` |
| priority_weights (lenses) | implemented_artifact | manually_performed | `decision_packet.json:214-217`; test asserts fixed literal lens winners `["C","B",None]` |
| recommendation | implemented_artifact | manually_performed | `decision_packet.json:222-233`; validator checks only structural mutual-consistency |

**No LLM call exists anywhere in the Mist Trail pipeline** (confirmed by
repo-wide grep for provider/API/prompt terms across `src/`, `scripts/`,
`tests/`, and by the absence of any LLM dependency in `pyproject.toml`).
Separately, the **artifact/validation/API/UI layer is genuinely well
built**: Pydantic models with `extra="forbid", frozen=True`, real
cross-reference validation (unique IDs, A/B/C identity, common-action
coverage, one-judgment-per-criterion completeness), SHA-256 hash-binding to
a source manifest, a working API route, and a working browser view that
renders the served JSON with no client-side aggregation logic. 13/13
tests pass (`tests/test_mist_trail_decision.py`). Representation and
execution are correctly kept as two separate axes here: this is
`implemented_artifact` across the board and `manually_performed` across
the board, simultaneously and without contradiction — exactly the
combination the status validity table (§5.0) calls "the trap this project
is exposed to."

---

## 5. Theory Forge compile/apply — why it is not compared against a source

Confirmed from code, not assumed: this workflow (paper -> schema -> agent-
driven codegen -> pytest-gated verification -> staged run) has no
authoritative external methodology governing "how to compile a scientific
theory into executable code." Per rev 5.1's explicit steer and
`sources.md` §4, every operation is recorded `runtime_delivery` and
contributes nothing to either the numerator or denominator. Two operations
(theory identification, schema formalization) involve genuine LLM
interpretive judgment and were the closest candidates for `analytic`
classification, but no authoritative source specifying them was found —
this is recorded as an explicit borderline case in the ledger (§5.0a guard
4 checked: nothing was suppressed that a source actually requires) rather
than silently defaulted.

**Independent findings surfaced along the way, beyond what was asked:**

- `CLAUDE.md` describes an MCP server (`tf_mcp_server.py`) as a current,
  working tool surface; the file was deleted from the repository over five
  months before the doc's current revision date, and its stated
  replacement location does not exist on this machine. The relevant test
  gracefully skips rather than failing, so this is a known, tolerated gap
  — but the documentation was never corrected.
- The dedicated reliability tests for the runtime-invariant-checking
  feature (`tests/test_runtime_invariants.py`) currently fail at the
  inspected snapshot (`theory-forge` commit `9ec293f`, see
  `repository_snapshots.yaml`; corroborated but not independently
  SHA-confirmed as the exact inspected state) due
  to a genuine signature/shape drift between the test and
  `runner.py`'s `_check_invariants()` return type. The underlying
  behavior (invariant logging) is real, executing code — but its own
  verification suite is currently broken, which is itself informative
  about how reliable "reliability infrastructure" claims are in this repo
  without independently re-running the tests.
- Of the 39 theories `CLAUDE.md` lists as "runtime-green," only 2 have a
  durable, git-committed evidence/manifest snapshot; the other 37 rest
  entirely on an ephemeral, non-version-controlled cache directory that
  does not exist on the inspecting machine. The verification mechanism
  itself (pytest run via subprocess, not a self-report) is confirmed real
  and sound for the cases that could be checked; the claim's
  reproducibility for the other 37 could not be independently confirmed in
  this pass.

---

## 6. Theory Forge CPT/Choices13k — a genuine counterexample worth naming

This is the one workflow in the whole Phase 0 set that is fully
deterministic, end-to-end tested, and 100% `software_executable`, with no
LLM, no agent, and no fitting loop anywhere in it — a useful counterweight
to the Mist Trail/source-acquisition findings, since it shows the
repositories are capable of genuinely automated analytic execution when
the method itself is a fixed, literature-specified formula rather than an
open-ended interpretive judgment. One citation-completeness finding:
the repository correctly and repeatedly cites Tversky & Kahneman (1992,
DOI embedded in every output artifact) but never cites Peterson et al.
(2021), the paper that produced the Choices13k dataset it benchmarks
against — it treats the dataset as pinned data (GitHub commit + SHA-256),
not as a cited scientific claim.

---

## 7. Guardrail compliance notes

- **Multi-subject exception usage: 0 of 58 rows (0%).** Every row was
  decomposable with a single `role: subject` input; no step required the
  multi-subject exception.
- **Verb additions: 0.** All verbs used are in rev 5.1's controlled list
  (see `verb_additions.md`).
- **Type additions: 0.** All types used are in rev 5.1's controlled list
  (see `type_additions.md`).
- **Steps I was unsure how to type (reported per §14):** 3.
  (a) `pt_core_rival_explanation.09` (mechanism-DAG construction) — evidence
  is a passing-test citation and a docs description, not an
  independently-narrated file:line read; flagged for deeper Phase-1
  verification. (b) `theory_forge_compile_apply.08` (manifest verify-gate)
  — the execution/representation split between the 2 durably-evidenced and
  37 unverifiable theories was collapsed to one row rather than two,
  noted narratively instead. (c) `qc_grounded_theory.04` (category
  development) — its LLM-populating code lives in a one-off script outside
  the default pipeline invocation, which weakens confidence that this
  executes on every default run versus only when that script is
  separately invoked.
- **No invented steps, no merges to inflate collision counts, no unsure
  type assignments forced to match a signature** — none of these
  guardrail violations were needed or used.

---

## 8. Material uncertainties carried into any future comparison

1. **Incidental exposure to Codex-candidate aggregate numbers.** While
   reading `mixed_methods_workbench/docs/PLANNING_STATUS.md` for the
   required repository-orientation pass (not the sealed
   `codex_phase0/` directory itself), I incidentally saw a summary
   sentence quantifying `ac27ab2`'s results ("77 source-linked steps: 67
   executable, eight represented manual, two incomplete"). This ledger's
   counts (58 rows; 39-operation denominator; 29 executable) were derived
   independently from source-first ideal decomposition and code inspection
   before and regardless of that exposure, and no number here was reverse-
   engineered to match or diverge from it — but full disclosure requires
   recording the exposure rather than omitting it.
2. **PT core workflow's case identity was not independently confirmed** —
   the inspecting agent verified the pipeline code and passing tests
   extensively but did not confirm which specific case/corpus is the
   "shipped" example referenced in `pt_core_rival_explanation`'s use_case.
3. **Environment could not reproduce Theory Forge's compiled-theory cache**
   (`~/.theory-forge/compiled/` does not exist on this machine), bounding
   confidence in the 39-theory "runtime-green" claim to the 2 theories with
   committed evidence.
4. **`pt_source_acquisition`'s frozen sources (PRISMA 2020, Howell &
   Prevenier 2001) are not cited anywhere in the repository** — they were
   independently frozen from the discipline per §7.2, not inherited from
   implementer intent, because no in-repo citation exists for this
   workflow at all. This is recorded as a citation-completeness finding
   about the repository, not a defect in the sources themselves (both
   independently verified to exist and specify steps).
5. **The abort-gate share is sensitive to a scoping choice** (§3 item 3
   above): had `pt_source_acquisition`'s screen/admit operation been
   scored using the bulk/comparative pipeline's implementation instead of
   the interactive single-case companion's, that method's share would be
   75% (PASS) instead of 50% (FAIL), and the aggregate would shift from
   29/39 (74.4%) to 30/39 (76.9%) — the branch would not change, but the
   per-method PASS/FAIL would. This scoping choice is defended in §3 and
   should be an explicit point of scrutiny in any future migration/
   comparison against `ac27ab2`.
6. **`process_tracing` has confirmed-drifted since inspection** (added in
   the `repository_snapshots.yaml` corrective pass): a new merge (PR #83)
   landed on `process_tracing`'s `master` after the sub-agent that produced
   `pt_core_rival_explanation` and `pt_source_acquisition` read the
   repository. No `git rev-parse HEAD` was captured contemporaneously by
   that sub-agent, so the exact commit it actually inspected cannot be
   reconstructed — only that it precedes commit `44556a0` (2026-08-12
   18:44:57-04:00). Every `pt_core_rival_explanation` and
   `pt_source_acquisition` row, and their 100%/50% shares, describes that
   earlier, unrecorded state. This is the single most consequential
   uncertainty introduced by this corrective pass, since it bears directly
   on one of the two individually-failing methods
   (`pt_source_acquisition`). Re-verification against current
   `process_tracing` HEAD is recommended before this candidate is used to
   support any promotion or build decision, independent of the eventual
   comparison against `ac27ab2`.
7. **Four of five repositories' claims rest on presumed, not proven,
   revision stability** (`qualitative_coding`, `theory-forge`,
   `data-contracts`, and — with confirmed-negative status —
   `process_tracing`). Only `mixed_methods_workbench`'s inspected commit
   (`10bc11f`) was captured contemporaneously. See
   `repository_snapshots.yaml` for the full per-repository accounting and
   the reasoning behind each "presumed unchanged" judgment.
