# Reality-check amendment — bounded re-verification of affected Process Tracing evidence

**Status:** post-freeze amendment. This document does not rewrite
`reality_check.md`, `step_ledger.yaml`, `workflow_edges.yaml`, or
`prior_art.md` — those remain the original independent observations, frozen
before `ac27ab2` was inspected. This amendment records what changed in
`process_tracing` since the SHA Codex's frozen candidate cites, and
re-verifies only the two narrative claims that scope covers. Everything else
in the original candidate is unaffected and is not re-examined here.

## 0. Revisions used

- **`FROM` (baseline):** `1bf255a605d0f6f83e26b6073206ccaa46805e21` — this is
  the exact commit Codex's `ac27ab2` candidate records as its inspected
  `process_tracing` revision for both `pt_single_case_rival_explanation_v2`
  and `pt_acquisition_companion` (`codex_phase0/README.md`'s frozen-evidence
  table and `codex_phase0/steps.yaml`'s per-workflow `revision:` field both
  cite it).
- **`TO` (current Process Tracing HEAD, captured now):**
  `4450d2ec7fc898672d5b3b23a3669ea5dbddb881` — `git rev-parse HEAD` on
  `process_tracing`'s clean `master` at the time of this amendment (`git
  status --short` empty; confirmed clean).
- `FROM` is a confirmed ancestor of `TO` (`git merge-base --is-ancestor`
  passed). 11 merge commits separate them (PR #76 through PR #87 by commit
  count on `master`'s first-parent chain).

## 1. Path diff: in-scope core rival-explanation and single-case acquisition — unchanged

`git diff --stat` from `FROM` to `TO`, restricted to every file cited in
`implementation_ref` for `pt_core_rival_explanation.*` (11 rows) and for the
in-scope rows of `pt_source_acquisition.*` (`.01`-`.06`, i.e. everything
except the explicitly-excluded-alternate `.07`):

- **Core rival-explanation files** (`pass_extract.py`, `pass_hypothesize.py`,
  `pass_partition.py`, `pass_test.py`, `pass_discriminator_audit.py`,
  `pass_absence.py`, `pass_absence_audit.py`, `bayesian.py`, `pass_critic.py`,
  `pass_mechanism_trace.py`, `pass_mechanism_audit.py`, `pass_synthesize.py`,
  `verdict_calibration.py`): **zero diff.** Byte-identical at `FROM` and `TO`.
- **In-scope acquisition files** (`source_acquisition.py`,
  `acquisition_session.py`, `source_lineage.py`): **zero diff.**
  Byte-identical at `FROM` and `TO`. In particular, `acquisition_session.py`
  (1,742 lines at both revisions) is unchanged, so the `pt_source_acquisition.03`
  finding it grounds — "confirmed zero `call_llm` occurrences in this file";
  `CandidateReviewRequest` at lines 335-343; `review_candidate()` at lines
  1055-1206 checking only internal consistency — **is reconfirmed at current
  HEAD without qualification.**
- **`revolution_reconciliation.py`, `revolution_adjudication.py`** (cited only
  as the out-of-scope analog for `.06`'s `not_implemented` finding): **zero
  diff.**

**Conclusion for this section: the abort-gate-relevant claims for
`pt_core_rival_explanation` (100%, PASS) and for `pt_source_acquisition`'s
in-scope rows `.01`-`.06` (2 executable / 1 manually_performed / 1
not_implemented of the 4 denominator-eligible rows) are unaffected by any
change between `FROM` and `TO`.** All relevant test suites were re-run at
`TO` in a clean venv and pass: 341 tests across the core-workflow test
families (`test_pass_hypothesize.py`, `test_pass_partition.py`,
`test_pass_absence.py`, `test_pass_critic.py`, `test_pass_diagnostic.py`,
`test_pt_bayesian.py`, `test_verdict_calibration.py`, `test_pt_schemas.py`,
`test_mechanism_audit.py`, `test_mechanism_trace.py`,
`test_methodology_integrity.py`) and 108 tests across the acquisition/
revolution families (`test_source_acquisition.py`, `test_source_coverage.py`,
`test_source_packet.py`, `test_segmented_source.py`,
`test_acquisition_session.py`, `test_p5_acquisition_view.py`,
`test_cli_source_packet.py`, `test_revolution_source_development.py`,
`test_revolution_reconciliation.py`, `test_revolution_adjudication.py`).

One supporting (non-denominator-affecting) citation drifted and is corrected
here: `step_ledger.yaml`'s `pt_source_acquisition.03` row cites
`pt/workbench.py:2654-2664` as secondary evidence that admission is "validated
directly off an HTTP POST body." `workbench.py` grew from 2,194 lines at
`FROM` to 3,231 lines at `TO` (+1,037 net). Line 2654-2664 does not exist at
`FROM` (file too short) and at `TO` now contains unrelated
`revolution-study case-traces` handler code, not the `review_candidate`
call site (which is at `workbench.py:3045-3047` at `TO`). **This citation was
never resolvable at either the nominal baseline or current HEAD as written —
it reflects some unrecorded intermediate commit's line numbering.** The
row's *substantive* classification (`manually_performed`,
`implemented_artifact`) does not depend on this citation — it rests on
`acquisition_session.py`, confirmed unchanged above — so no ledger value
changes; this is a citation-accuracy note, not a reclassification.

## 2. Re-verified narrative claim: the excluded alternate `revolution_source_development.py` (`pt_source_acquisition.07`)

**The claim under review** (`reality_check.md` §3, item 3, quoted verbatim,
unedited by this amendment): "`pt_source_acquisition` screen/admit (.03) has
two structurally different implementations with opposite execution status
... the interactive single-case companion path (`acquisition_session.py`,
`manually_performed`) and the separate bulk/comparative-case 'revolution'
pipeline (`revolution_source_development.py`, `software_executable`, with a
genuinely independent second-LLM pair-review) ... Counting the bulk-pipeline
realization instead would flip `pt_source_acquisition`'s share from 50%
(FAIL) to 75% (PASS)."

This area changed materially between `FROM` and `TO`:

- `revolution_source_development.py` grew from 702 to 1,231 lines (+529, 0
  deletions) across two commits (`5bdf331` "Add complete revolution source
  packet runner," `5dadda6` "Preserve reviewer corrections and exact
  resume"), both landing strictly after `FROM`.
- **The two functions the ledger's `pt_source_acquisition.07` row cites by
  line number — `run_source_assessment` and `run_pair_review` — are
  byte-identical in body between `FROM` and `TO`.** Their *line numbers*,
  however, moved: at `FROM` they sit at lines 512 and 607; at `TO` (and
  already at the very first of the two post-`FROM` commits) they sit at
  lines 656 and 751 — which is exactly what the frozen ledger row cites
  (`pt/revolution_source_development.py:656-685` and `:751-777`). **This
  means the ledger's line-number citation for this row reflects the file's
  state *after* both Plan #41 commits landed, not the state at `FROM` —
  i.e., the original Phase 0 inspection of this specific file happened at
  some commit no earlier than `5bdf331`, not at the nominal `FROM` baseline.**
  The underlying claim (two independent LLM calls, genuinely separate
  pair-review) is unaffected by this — the function bodies are unchanged —
  but the citation's implied baseline was already inconsistent with `FROM`
  before this amendment, for reasons independent of ordinary code drift.
- **A new, third LLM-calling function was added in this same window and is
  not reflected anywhere in the original narrative claim:**
  `run_packet_completeness_review` (current line 966, calling `call_llm` at
  line 985), backing new `CasePacketCompletenessReview` /
  `CompleteCaseSourcePacket` schema types and a new
  `freeze_source_packet_design_and_plans` function. This is additional
  automated capability in the excluded alternate path beyond what the
  original claim described — it does not change the claim's truth value
  (the path was already `software_executable` with independent second-LLM
  review; it now has a third independent LLM-backed operation on top), but
  it means the original claim's description of this path is now
  incomplete, not merely stale.

**Verdict: the narrative claim remains true, with one addition.** At current
HEAD, `revolution_source_development.py` is still `software_executable` with
a genuinely independent second-LLM pair-review (`run_source_assessment` /
`run_pair_review`, unchanged), so the 50%→75% scoping-sensitivity finding
still holds exactly as stated — the hypothetical swap being illustrated does
not depend on the new function. The path now additionally contains a third
independent LLM-backed operation (packet completeness review) not present
when the original claim was written. This is recorded as an addition to,
not a correction of, the original observation. 108 tests re-run at `TO`
across the acquisition and revolution test families, all passing (§1 lists
the exact suites; includes `test_revolution_source_development.py`).

## 3. What this amendment does not do

- It does not change any value in `step_ledger.yaml`, `workflow_edges.yaml`,
  `reality_check.md`, or `prior_art.md`. The abort-gate table in
  `reality_check.md` §1 (`pt_core_rival_explanation`: 100% PASS;
  `pt_source_acquisition`: 50% FAIL, exact-half) stands unchanged and is
  reconfirmed current as of `4450d2ec7fc898672d5b3b23a3669ea5dbddb881`.
- It does not re-verify `qualitative_coding`, `theory-forge`, or
  `data-contracts` — those repositories' claims remain "presumed unchanged,
  not proven," per `repository_snapshots.yaml`, and were out of scope for
  this bounded amendment (the amendment's mandate was Process Tracing only,
  triggered by confirmed drift in that one repository).
- It does not touch `codex_phase0/` or Codex's frozen candidate in any way.
