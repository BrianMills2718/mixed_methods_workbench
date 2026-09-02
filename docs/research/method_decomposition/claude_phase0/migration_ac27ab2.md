# Migration of Codex's frozen Phase 0 candidate (`ac27ab2`) into rev-5.1 vocabulary

**Status:** `migration_of_frozen_candidate`. Produced after this candidate's own
`step_ledger.yaml`/`reality_check.md`/`prior_art.md`/`sources.md` were frozen
(rev 5.1 §0.1 sequencing). This document does not alter, re-derive, or
second-guess Codex's observations — it re-expresses them, row by row, in
rev-5.1's vocabulary, and states plainly everywhere that re-expression loses
information, is uncertain, or cannot be done at all.

**Source:** `mixed_methods_workbench` commit `ac27ab2b85d75acc492f9a58c40154ca2dbbdee4`,
files `docs/research/method_decomposition/codex_phase0/{README.md, steps.yaml,
edges.yaml, reality_check.md, schema_findings.md}`. `comparison_rubric.md` in
the same directory on the current branch tip is **not** part of the frozen
`ac27ab2` commit — it was added by a later reconciliation commit
(`ece88b8`) — and is treated in `candidate_comparison.md` as a jointly-agreed
comparison procedure, not as part of the frozen candidate being migrated here.

Codex's candidate has **77 steps across 6 workflow graphs** (verified by
direct count against `steps.yaml`, matching `reality_check.md`'s own summary
table exactly: 15 + 23 + 4 + 19 + 6 + 10 = 77, with 67 `executable`, 8
`represented_manual`, 2 `incomplete`).

---

## 1. What is directly, losslessly re-expressible

These Codex fields map onto rev-5.1 fields with no loss of information,
because the underlying concept is the same and Codex's controlled vocabulary
happens to be a (mostly overlapping) subset of rev-5.1's:

| Codex field | rev-5.1 field | Migration rule |
|---|---|---|
| `step_id` | `step_id` | Identical, copied verbatim. |
| `verb` | `verb` | Every verb Codex used (`retrieve, construct, anchor, derive, review, project, revise, extract, test, measure, screen, appraise_source, acquire, aggregate, value, recommend, perturb`) is already in rev-5.1's §6 controlled list. No verb additions needed on migration. |
| `label` | `label` | Identical in spirit; copied verbatim. |
| `preconditions` | `preconditions` | Same concept, same free-text form; copied verbatim. |
| `method_owned_semantics` | `method_owned_semantics` | Same concept; copied verbatim. Codex's is sometimes an empty list `[]` where rev-5.1 would still expect a value for an analytic step — flagged per-row in §2.4, not silently carried over as "confirmed empty." |
| `repeatable` | `repeatable` | Identical boolean. |
| `optional` | `optional` | Identical boolean. |
| `parameters` | `parameters` | Same concept (caller-configured, not consumed data); copied verbatim. |
| `source_refs` | `implementation_ref` | Codex's `source_refs` is a list of `file:line` citations; rev-5.1's `implementation_ref` is a single free-text field. Migration concatenates the list. No loss of citation content, but the list→scalar collapse loses the ability to say which specific citation supports which specific claim within a row — flagged where a row has 3+ refs (§2.5). |
| `internal_method_phases` | *(no direct field; closest is a note, not a schema field)* | Preserved verbatim as narrative annotation on the migrated row. Rev-5.1 has no field for "sub-phases bundled inside one executable operation" — see §2.6. |

---

## 2. Lossy, uncertain, and impossible mappings

### 2.1 `implementation_status` → `execution_status` × `representation_status` — the central structural mismatch

Codex's schema uses **one axis** (`implementation_status: executable |
represented_manual | incomplete | planned`). Rev-5.1 requires **two
independent axes** (`execution_status` × `representation_status`), because
rev-5.1's whole point (§5.0, "the trap this project is exposed to") is that a
typed, validated, served artifact can exist (`representation_status:
implemented_artifact`) while the analytical judgment behind it was
`manually_performed` — exactly the distinction Codex's `represented_manual`
status was independently invented to capture. Migration rule, applied
uniformly across all 77 rows:

| Codex `implementation_status` | rev-5.1 `execution_status` | rev-5.1 `representation_status` | Confidence |
|---|---|---|---|
| `executable` | `software_executable` | **cannot be migrated — see below** | execution_status: high; representation_status: none |
| `represented_manual` | `manually_performed` | `implemented_artifact` | high (Codex's own README defines `represented_manual` as "a typed, inspectable result... exists," which *is* rev-5.1's `implemented_artifact` by definition) |
| `incomplete` | `incomplete_software` | `implemented_artifact` (qualified) | medium — only where Codex's `implementation_note` independently describes partial, existing code (both occurrences do) |
| `planned` | *(does not occur in this candidate — 0 rows)* | — | n/a |

**Why `executable` → `representation_status` is impossible, not merely
uncertain, for all 67 rows carrying that status:** Codex's own interpretation
rule states `implementation_status: executable` "means a callable
implementation exists; it does not certify a fresh live LLM run" — it is
silent on whether that callable path leaves a durable, inspectable artifact
versus running and discarding its output. Rev-5.1's status-validity table
(§5.0) treats exactly this distinction as one of its four most informative
cells (`software_executable` × `missing` — "runs but leaves no durable
artifact, so the result is untraceable"). Assigning `implemented_artifact` to
all 67 by default would erase precisely the finding rev-5.1 is designed to
surface, and assigning it by guessing from the step's `outputs` types would
be new analysis invented after the fact — exactly what rev-5.1 §5.0a guard 2
and the general anti-fabrication guardrail (§14) prohibit. **This field is
therefore left unmigrated (not merely "uncertain") for all 67 `executable`
rows**; see the per-workflow tables in §3.

A minority of these 67 rows carry weak circumstantial evidence one way or the
other from their own `outputs` types or `source_refs`, worth naming as
illustration without treating it as a migrated value:
- `qc_gt.15` outputs `persisted_artifact` and `artifact_digest` — output
  typing suggests `implemented_artifact` is likely, but Codex did not assert
  this and no independent check was run for this migration.
- `tf_cpt.06` and `mt.10` both output `artifact_ref` types with named report/
  view files — same caveat.
- Most `pt.*` core-workflow rows output `finding`, `appraisal`, or
  `estimate` types with no artifact-typed output at all — for these, even
  circumstantial evidence is genuinely absent, and Claude's own independent
  `pt_core_rival_explanation` ledger (§8.2 mapping, produced without
  consulting `ac27ab2`) assigns `implemented_artifact` to every row on
  independent code-reading grounds. That independent agreement is evidence
  for the comparison in `candidate_comparison.md`, not license to backfill it
  into this migration as if Codex had stated it.

### 2.2 `operation_kind` — absent from Codex's schema entirely; the single most consequential impossible mapping

Codex's schema has **no field corresponding to rev-5.1's `operation_kind`**
(`analytic | methodological_support | runtime_delivery`), and Codex's own
`schema_findings.md` proposed schema revision (items 1-10) does not propose
adding one. This is not an oversight visible only in retrospect — Codex's
`reality_check.md` explicitly frames its purpose as recording "what... code
actually do[es]" prior to any methodological-ideal comparison, and states
outright: "Candidate reuse is deliberately not adjudicated here." Rev-5.1's
`operation_kind` is not a reuse-adjudication field, but it **is** the field
that determines abort-gate eligibility (§5.0a), which presupposes exactly
the source-anchored ideal-operations concept Codex's candidate deliberately
does not construct (no `sources.md`, no frozen authoritative citations, no
ideal-vs-code table — confirmed absent from all five `codex_phase0/` files).

**This field is not assigned in this migration for any of the 77 rows.**
Assigning it now, post-hoc, by inferring from each row's verb and prose
description, would constitute new analytic judgment produced *after* seeing
which classification would be convenient for any joint denominator — the
exact anti-gaming failure mode §5.0a guard 1 exists to prevent ("Assign
`operation_kind` to the **ideal** operations... *before* mapping them to
code, and freeze that assignment with the sources"). Codex's candidate has
no ideal operations frozen independently of code to assign it to. There is
no honest way to backfill this field without either (a) constructing a
methodology-sourced ideal for Codex's candidate that Codex never produced —
which is not migration, it is doing Codex's Phase 0 work for it — or (b)
guessing from code alone, which rev-5.1 explicitly forbids as the
denominator-defining field. **Escalated to `disagreements.md` as a
methodological disagreement bearing directly on whether any joint
abort-gate figure can ever be computed across the two candidates.**

### 2.3 `actor` → `actor_chain` — compound labels require decomposition rev-5.1 does not automate

Codex uses a single free-text compound `actor` string per row (e.g.
`independent_auditor_and_repair_llms_with_deterministic_checks`,
`analyst_llm_optional_human_and_deterministic_delta_application`). Rev-5.1's
`actor_chain` is an **ordered list** drawn from a small controlled vocabulary
(`human_analyst, human_reviewer, llm_engine, deterministic_engine,
deterministic_validator, browser_projection`, extendable only when none
fits), explicitly requiring producer/validator/auditor/reviewer to be
recorded as separate list entries rather than compressed into one label
(rev-5.1 §5: "do not compress producer, validator, auditor, and reviewer into
one actor label").

Mechanically splitting Codex's compound strings on `_and_`/`_with_` would
produce a list, but **the order in the resulting list would not reliably
reflect the true producer→validator→auditor sequence** — Codex's naming
convention does not guarantee first-mentioned-is-first-executed (e.g.
`repair_llm_or_human` for `pt.08` names an *alternative*, not a *sequence*;
`deterministic_orchestration_and_pt_llms` for `pt_acq.04` does not disambiguate
which deterministic step precedes which LLM step). Automated decomposition
would therefore fabricate an ordering Codex never asserted. **Every
`actor_chain` cell in §3's tables is marked uncertain and left as Codex's
original compound string rather than split into an ordered rev-5.1 list.**
A correct migration of this field requires re-reading the cited
`source_refs` per row to establish true call order — out of scope for a
migration pass whose purpose is re-expression, not re-verification (that
re-verification, where it bears on the `pt_source_acquisition` /
`revolution_source_development.py` scope, was performed separately and is
recorded in `reality_check_amendment.md`, not here).

### 2.4 `method_owned_semantics: []` on operations that are not obviously enabling-only

Rev-5.1 treats `method_owned_semantics` as load-bearing (§5.3: "a generic
signature plus heavy method-owned semantics is a Tier 2 capability, not
Tier 1"). Several Codex rows carry `method_owned_semantics: []` (empty) where
the row is not a pure enabling/plumbing step — for example `pt_acq.02`
(retrieve candidates for target) and `pt_acq.05`/`qc_gt.01`/`qc_gt.02`/many
`tf.*` rows. For rows Claude's own independent ledger also classified
`runtime_delivery`, an empty value is consistent (rev-5.1 also expects little
or no method-owned semantics there). But some empty-list Codex rows
correspond to rows Claude's independent ledger classified `analytic` with
non-trivial semantics recorded (e.g. Claude's
`theory_forge_cpt_choices13k.01`/`.02` record CPT-specific method-owned
semantics; Codex's `tf_cpt.01` records none because Codex placed that
semantic content instead in `tf_cpt.04`'s
`method_owned_semantics: [CPT and expected-value model equations and tie
handling]` — a genuine granularity difference, not a gap, see §3's CPT table
and `candidate_comparison.md` §granularity). **Not flagged as lossy per row
here** — each empty-list case is preserved exactly as Codex wrote it in §3;
readers comparing against Claude's ledger should expect apparent "gaps" that
are granularity differences, not migration errors.

### 2.5 `source_refs` (list) → `implementation_ref` (scalar) — citation-to-claim binding loosens

Where a Codex row cites 3+ `source_refs` (e.g. `pt.18`: three refs; `pt.12`:
four refs; `tf.07`: four refs), rev-5.1's single free-text
`implementation_ref` field, once populated by concatenating the list, no
longer indicates *which* specific claim in the row (e.g. "audit," "repair,"
or "re-audit" within `pt.18`) each specific citation supports. This is a
real but minor loss — full traceability is preserved (nothing is dropped),
only the fine-grained claim-to-citation binding present in the list
structure is flattened. Concatenation is applied uniformly in §3; the
original list order is preserved so the binding can be reconstructed by a
reader willing to re-cross-reference against `steps.yaml` at `ac27ab2`
directly.

### 2.6 Fields present in rev-5.1 with **no Codex equivalent at all**

These rev-5.1 step-ledger fields (§5) cannot be populated for any of the 77
rows because Codex's schema does not carry the underlying concept, and
inventing values would be fabrication, not migration:

- **`workflow_role`** (§5.4) — Codex has no coarse investigation-position
  label. Not migrated for any row.
- **`conclusion_supported`** (§5.5) — Codex has no field stating what a step
  licenses an analyst to assert. Not migrated for any row. This is a
  material gap for cross-candidate adjudication (§10's promotion rule treats
  divergent `conclusion_supported` as disqualifying for `same_capability`),
  addressed as a comparison-methodology point in `candidate_comparison.md`.
- **`failure_output`** (§5.6) — Codex represents failure only as terminal
  nodes and `failure`-kind edges in `edges.yaml` (e.g. `refuse_partition_blocked`,
  `refuse_mechanism_blocked`, `refuse_publication`, `refuse_invalid_schema`,
  `refuse_custody_mismatch`, `incomplete_evaluation`, `refuse_invalid_packet`,
  `stop_unresolved`, `stop_refused`), not as a per-step field. These are
  **partially reconstructable** (see `candidate_comparison.md` §workflow
  edges) but only for steps that are the source of a `failure`-kind edge —
  most steps have no such edge and therefore no reconstructable
  `failure_output` at all. Not migrated as a per-row field here to avoid
  implying completeness the reconstruction does not have.
- **Named-slot `role`** (`subject | criteria | context | prior |
  config_data`, §5.1) — Codex's `inputs`/`outputs` slots carry `type`,
  `cardinality`, `optional`, but no `role`. Rev-5.1's collision
  canonicalization (§5.1) explicitly runs on `(type, role, cardinality,
  optional)` — without `role`, Codex's slots cannot be projected onto
  rev-5.1's canonical signature at all. **This is impossible to migrate
  without fresh judgment call per slot** (deciding which input is "the
  subject" versus "context" versus "criteria" was not Codex's task and is
  not this migration's task either). Not attempted in §3's tables.
  `candidate_comparison.md` treats any signature-level collision comparison
  between the two candidates as correspondingly weakened by this gap.
- **`evidence_basis` as a methodology citation** (§5, rev-5.1's sense: "why
  the operation belongs to the method," pointing at `sources.md`) — Codex's
  `evidence_basis` is a different concept entirely (code/test/fixture/doc/
  inferred — i.e., rev-5.1's `evidence_basis` name collides with a field
  Codex uses for what rev-5.1 would call provenance-of-observation, closer to
  rev-5.1's `implementation_ref`/`execution_evidence` combined). **Migrated
  as `implementation_ref`-adjacent provenance tags in §3's tables** (labeled
  "evidence_basis (mapped)"), explicitly not as a rev-5.1 methodology
  citation, because Codex's candidate cites no methodology sources at all
  (confirmed: no `sources.md`-equivalent file exists anywhere in
  `codex_phase0/`).
- **Cardinality vocabulary** (§5.1: `one | many | optional_one |
  optional_many`) — Codex uses free-text range strings (`"1"`, `"0..1"`,
  `"2..25"`, `"8..24"`, `"1..* per proposition"`, `"5..25"`). A deterministic
  mapping is possible for the common cases (`"1"`→`one`, `"0..1"`→
  `optional_one`, any `"0.."`-prefixed range→`optional_many`, everything else
  with a lower bound ≥1→`many`) but **loses the exact bounds** rev-5.1's
  looser vocabulary doesn't carry (e.g. `"2..25"` and `"1..*"` both collapse
  to `many`, even though one is exactly bounded and the other open-ended —
  a real distinction for `qc_gt.02`'s document-count constraint). Not
  applied row-by-row in §3 to avoid manufacturing a false precision; noted
  here as a standing, uniform loss across every multi-slot row in the
  candidate.

---

## 3. Per-workflow migrated tables

Preserves Codex's original `implementation_status` and `actor` values
verbatim in the rightmost columns for audit against `steps.yaml` at
`ac27ab2`. Blank/impossible cells are marked, not guessed. Generated
programmatically from `ac27ab2:docs/research/method_decomposition/codex_phase0/steps.yaml`
against the migration rules in §1-2 (no hand-transcription) — 77/77 rows
accounted for, cross-checked against `reality_check.md`'s own summary table
(15+23+4+19+6+10=77; 67 executable / 8 represented_manual / 2 incomplete).

### `qc_fixed_corpus_grounded_theory_v3`

Repository: `/home/brian/code/qualitative_coding` @ `4ea0ce6ca15a63ba91b1a3790e4737b411389902`

| step_id | verb | rev-5.1 execution_status | rev-5.1 representation_status | actor_chain (Codex compound, unsplit — §2.3) | evidence_basis (mapped) | Codex implementation_status (preserved) |
|---|---|---|---|---|---|---|
| qc_gt.01 | retrieve | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| qc_gt.02 | retrieve | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| qc_gt.03 | construct | software_executable | impossible — §2.1 | llm_with_deterministic_orchestration | code | executable |
| qc_gt.04 | anchor | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| qc_gt.05 | derive | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| qc_gt.06 | review | software_executable | impossible — §2.1 | llm_with_deterministic_orchestration | code | executable |
| qc_gt.07 | project | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| qc_gt.08 | construct | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| qc_gt.09 | construct | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| qc_gt.10 | revise | software_executable | impossible — §2.1 | llm_with_deterministic_orchestration | code | executable |
| qc_gt.11 | project | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| qc_gt.12 | derive | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| qc_gt.13 | review | software_executable | impossible — §2.1 | llm_with_deterministic_orchestration | code | executable |
| qc_gt.14 | project | software_executable | impossible — §2.1 (circumstantial: `persisted_artifact`/`artifact_digest` outputs) | deterministic_software | code | executable |
| qc_gt.15 | project | software_executable | impossible — §2.1 | deterministic_software | code | executable |

### `pt_single_case_rival_explanation_v2`

Repository: `/home/brian/projects/process_tracing` @ `1bf255a605d0f6f83e26b6073206ccaa46805e21`

| step_id | verb | rev-5.1 execution_status | rev-5.1 representation_status | actor_chain (Codex compound, unsplit — §2.3) | evidence_basis (mapped) | Codex implementation_status (preserved) |
|---|---|---|---|---|---|---|
| pt.01 | construct | software_executable | impossible — §2.1 | researcher_and_deterministic_software | code | executable |
| pt.02 | construct | software_executable | impossible — §2.1 | llm_or_researcher | code | executable |
| pt.03 | extract | software_executable | impossible — §2.1 | llm_with_deterministic_validation | code | executable |
| pt.04 | project | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| pt.05 | construct | software_executable | impossible — §2.1 | llm_with_deterministic_exposure_binding | code | executable |
| pt.06 | review | software_executable | impossible — §2.1 | human | code | executable |
| pt.07 | review | software_executable | impossible — §2.1 | auditor_llm_with_deterministic_gate | code | executable |
| pt.08 | revise | software_executable | impossible — §2.1 | repair_llm_or_human | code | executable |
| pt.09 | construct | software_executable | impossible — §2.1 | researcher_and_deterministic_software | code | executable |
| pt.10 | measure | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| pt.11 | test | software_executable | impossible — §2.1 | analyst_llm_with_deterministic_validation | code | executable |
| pt.12 | review | software_executable | impossible — §2.1 | independent_auditor_llm_with_deterministic_projection | code | executable |
| pt.13 | test | software_executable | impossible — §2.1 | analyst_llm_with_deterministic_severity_cap | code | executable |
| pt.14 | review | software_executable | impossible — §2.1 | independent_auditor_llm_with_deterministic_binding | code | executable |
| pt.15 | estimate | software_executable | impossible — §2.1 | deterministic_model | code | executable |
| pt.16 | derive | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| pt.17 | construct | software_executable | impossible — §2.1 | analyst_llm_with_deterministic_graph_validation | code | executable |
| pt.18 | review | software_executable | impossible — §2.1 | independent_auditor_and_repair_llms_with_deterministic_checks | code | executable |
| pt.19 | synthesize | software_executable | impossible — §2.1 | analyst_llm_with_deterministic_verdict_calibration | code | executable |
| pt.20 | review | software_executable | impossible — §2.1 | critic_llm | code | executable |
| pt.21 | revise | software_executable | impossible — §2.1 | analyst_llm_optional_human_and_deterministic_delta_application | code | executable |
| pt.22 | review | software_executable | impossible — §2.1 | independent_review_llms_with_deterministic_gate | code | executable |
| pt.23 | project | software_executable | impossible — §2.1 | deterministic_software | code | executable |

**Cross-check against the reality_check_amendment.md re-verification:** all
23 rows' `source_refs` point at files confirmed byte-identical between
Codex's frozen revision (`1bf255a6...`) and current process_tracing HEAD
(`4450d2e...`) — see `reality_check_amendment.md` §1. No row in this table is
affected by the drift found there.

### `pt_acquisition_companion`

Repository: `/home/brian/projects/process_tracing` @ `1bf255a605d0f6f83e26b6073206ccaa46805e21`

| step_id | verb | rev-5.1 execution_status | rev-5.1 representation_status | actor_chain (Codex compound, unsplit — §2.3) | evidence_basis (mapped) | Codex implementation_status (preserved, incl. note) |
|---|---|---|---|---|---|---|
| pt_acq.01 | construct | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| pt_acq.02 | retrieve | software_executable | impossible — §2.1 | retrieval_service_and_deterministic_ledger | code | executable |
| pt_acq.03 | appraise_source | software_executable | impossible — §2.1 | human_with_deterministic_validation | code | executable |
| pt_acq.04 | test | **incomplete_software** | **implemented_artifact** (qualified — §2.1) | deterministic_orchestration_and_pt_llms | code | incomplete — "Current caller unpacks eight outputs from a function that returns nine." |

**Direct bearing on `reality_check_amendment.md`:** `pt_acq.03` is Codex's
counterpart to Claude's `pt_source_acquisition.03` (interactive
human-screening path) — Codex classifies it `executable`/`human_with_
deterministic_validation`; Claude's independent ledger classifies the same
underlying code `manually_performed`/`implemented_artifact`. This is a
genuine disagreement, not a migration artifact — resolved in
`candidate_comparison.md` / `disagreements.md` using the unchanged (per the
amendment) `acquisition_session.py` evidence. Codex's candidate has **no
row at all corresponding to Claude's `pt_source_acquisition.07`**
(the excluded bulk/comparative-case `revolution_source_development.py`
alternate) — Codex's `pt_acquisition_companion` workflow is scoped to the
interactive single-case path only, so there is nothing to migrate for that
row; this is a scope-boundary difference, addressed in
`candidate_comparison.md`.

### `theory_forge_v14_compile_apply`

Repository: `/home/brian/projects/theory-forge` @ `9ec293f96b05a56115cfa4c1686ab7032fd79411`

| step_id | verb | rev-5.1 execution_status | rev-5.1 representation_status | actor_chain (Codex compound, unsplit — §2.3) | evidence_basis (mapped) | Codex implementation_status (preserved, incl. note) |
|---|---|---|---|---|---|---|
| tf.01 | extract | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| tf.02 | extract | software_executable | impossible — §2.1 | llm_with_typed_validation | code | executable |
| tf.03 | extract | software_executable | impossible — §2.1 | llm_with_typed_validation | code | executable |
| tf.04 | construct | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| tf.05 | test | software_executable | impossible — §2.1 | deterministic_schema_validator | code | executable |
| tf.06 | retrieve | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| tf.07 | project | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| tf.08 | construct | software_executable | impossible — §2.1 | llm | code | executable |
| tf.09 | construct | software_executable | impossible — §2.1 | compilation_agent | code | executable |
| tf.10 | test | software_executable | impossible — §2.1 | deterministic_test_runner | code | executable |
| tf.11 | revise | software_executable | impossible — §2.1 | compilation_agent_and_diagnostic_llm | code | executable |
| tf.12 | review | software_executable | impossible — §2.1 | deterministic_software_and_optional_llm_or_agent_reviewer | code | executable |
| tf.13 | retrieve | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| tf.14 | extract | software_executable | impossible — §2.1 | runtime_llm_with_typed_validation | code | executable |
| tf.15 | derive | software_executable | impossible — §2.1 | deterministic_safe_executor | code | executable |
| tf.16 | test | **incomplete_software** | **implemented_artifact** (qualified — §2.1) | deterministic_software | code | incomplete — "Checker exists, but ordinary stage discovery does not copy schema invariants into StageSpec." |
| tf.17 | synthesize | software_executable | impossible — §2.1 | runtime_llm | code | executable |
| tf.18 | review | software_executable | impossible — §2.1 | llm_reviewer | code | executable |
| tf.19 | construct | software_executable | impossible — §2.1 | deterministic_software | code | executable |

Note the granularity contrast recorded here without resolving it: Claude's
independent ledger covers this workflow in **8** rows, all `operation_kind:
runtime_delivery` (contributing 0/0 to any abort-gate denominator, per
`sources.md` §4's explicit no-source finding), while Codex covers the same
workflow in **19** rows with no `operation_kind` field at all. `tf.16`
corresponds to part of what Claude's ledger folds into
`theory_forge_compile_apply.07`("run the compiled theory...invariant
check...") — a one-to-many granularity difference addressed in
`candidate_comparison.md`.

### `theory_forge_cpt_choices13k_prediction`

Repository: `/home/brian/projects/theory-forge` @ `9ec293f96b05a56115cfa4c1686ab7032fd79411`

| step_id | verb | rev-5.1 execution_status | rev-5.1 representation_status | actor_chain (Codex compound, unsplit — §2.3) | evidence_basis (mapped) | Codex implementation_status (preserved) |
|---|---|---|---|---|---|---|
| tf_cpt.01 | acquire | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| tf_cpt.02 | screen | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| tf_cpt.03 | construct | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| tf_cpt.04 | derive | software_executable | impossible — §2.1 | deterministic_model | code | executable |
| tf_cpt.05 | aggregate | software_executable | impossible — §2.1 | deterministic_software | code | executable |
| tf_cpt.06 | project | software_executable | impossible — §2.1 (circumstantial: `artifact_ref` outputs) | deterministic_software | code | executable |

### `mist_trail_deliberative_appraisal_mtd1`

Repository: `/home/brian/projects/mixed_methods_workbench` @ `eb1c5df4776fcf532a045b74e00b3e47a41c4a35`

| step_id | verb | rev-5.1 execution_status | rev-5.1 representation_status | actor_chain (Codex compound, unsplit — §2.3) | evidence_basis (mapped) | Codex implementation_status (preserved) |
|---|---|---|---|---|---|---|
| mt.01 | acquire | **manually_performed** | **implemented_artifact** (by definition — §2.1) | human | fixture, code | represented_manual |
| mt.02 | construct | **manually_performed** | **implemented_artifact** | human | fixture, code | represented_manual |
| mt.03 | anchor | **manually_performed** | **implemented_artifact** | human | fixture, code | represented_manual |
| mt.04 | appraise_source | **manually_performed** | **implemented_artifact** | human | fixture, code | represented_manual |
| mt.05 | value | **manually_performed** | **implemented_artifact** | human | fixture, code | represented_manual |
| mt.06 | perturb | **manually_performed** | **implemented_artifact** | human | fixture, code | represented_manual |
| mt.07 | recommend | **manually_performed** | **implemented_artifact** | human | fixture, code | represented_manual |
| mt.08 | construct | **manually_performed** | **implemented_artifact** | human_artifact_authoring | code, fixture | represented_manual |
| mt.09 | test | software_executable | impossible — §2.1 (circumstantial: this is the validator itself, strongly implies `implemented_artifact`; Claude's independent ledger agrees) | deterministic_software | code, test | executable |
| mt.10 | project | software_executable | impossible — §2.1 (circumstantial: `browser_view`/`json_payload` outputs) | deterministic_software | code, test | executable |

**This is the cleanest migration in the whole candidate.** Because Codex's
`represented_manual` status is *defined* to equal rev-5.1's
`manually_performed` × `implemented_artifact` combination, all 8 Mist Trail
analytic rows migrate with high confidence and no loss on the
execution/representation axis — and Claude's independent ledger
(`mist_trail_policy_appraisal.01-06`, produced without consulting `ac27ab2`)
reaches the identical classification for the same underlying artifact. This
agreement is carried into `candidate_comparison.md` as the strongest
cross-candidate concordance found anywhere in this exercise.

---

## 4. Preserved original observations (verbatim, for reference)

Codex's own bottom-line framing (`reality_check.md`, unedited):

> The four implementations already disprove a simple universal pipeline.
> - QC contains a real feedback loop: each new five-document batch revises
>   the whole proposal before the next batch is examined.
> - Process Tracing contains several bounded audit/repair loops, conditional
>   branches based on evidence exposure, and a terminal publication refusal.
> - Theory Forge is mostly sequential/DAG-shaped and explicitly rejects
>   circular computation dependencies.
> - Mist Trail is a completed, typed, source-bound appraisal, but the
>   analytical judgments were manually authored. Its code validates and
>   presents the appraisal; it does not calculate the recommendation.

Codex's own summary table (`reality_check.md`, unedited):

| Workflow | Rows | Executable | Represented manual | Incomplete |
| --- | ---: | ---: | ---: | ---: |
| QC grounded theory | 15 | 15 | 0 | 0 |
| Process Tracing core | 23 | 23 | 0 | 0 |
| PT acquisition companion | 4 | 3 | 0 | 1 |
| Theory Forge generic | 19 | 18 | 0 | 1 |
| Theory Forge CPT prediction | 6 | 6 | 0 | 0 |
| Mist Trail | 10 | 2 | 8 | 0 |
| **Total** | **77** | **67** | **8** | **2** |

Nothing in this migration document changes, rounds, or reinterprets these
numbers. They are Codex's, in Codex's vocabulary, and remain correct on
their own terms; §2 above explains only why they cannot be mechanically
folded into rev-5.1's differently-shaped denominator without additional
judgment this migration deliberately does not supply.
