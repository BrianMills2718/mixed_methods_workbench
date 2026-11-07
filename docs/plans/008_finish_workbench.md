# Plan #8: finish the workbench (1.0) on a general, rights-clear study

Status: adopted 2026-11-06 on Brian's direction below; slice S1 in progress.

Planning package: docs/planning/planning-package.json

## Goal

Brian, 2026-11-06, answering open question Q1 ("what the workbench does next"), whose recommendation had been
upkeep only until a real study needed two methods' results joined:

> "on mixed mtheod work bench finsih that is not for a specific use case it is part of my broader vision"

So the workbench is finished to its 1.0, as a general tool in his broader evidence-to-action vision, not as
the back end of one study. A study is still needed to prove each slice works on real text; it is an
example, not the product's purpose.

**Broader vision, read from the repository** (open question Q18; Brian can overrule). The repository's
own product map, `docs/EVIDENCE_TO_ACTION_PRODUCT_INTEGRATION_MAP.md` (section 1), defines the workbench's
place in that vision: one workbench-owned investigation record that keeps the question, evidence, method
runs, findings, unresolved questions, reviews and next actions together, while each method stays in its
own repository; the same map names "separate destinations rather than one evolving study" as the defect
(section 3). So every slice below adds to one study record per corpus, built from a study definition file,
not a new page per feature; and S5 makes that record the general form of the existing PsychosisBank
investigation record (`investigation_spine.py`, today hard-coded to one investigation).

## What "finished" means here

The roadmap's 1.0 (`docs/ROADMAP.md`, "What 1.0 Means") is kept as the target, with the seven changes
marked in bold below. Each
change follows from evidence gathered on 2026-11-06 (`docs/planning/investigation.json`).

| 1.0 condition | Kept or changed | Why |
| --- | --- | --- |
| Governed study and corpus foundation | kept | Slice S1. |
| Method profiles that keep each tradition's validity rules | kept, reusing the method dashboard | `method_dashboard.py` already routes questions to method profiles; S7 marks which profiles the workbench actually runs. |
| At least one validated qualitative path | kept, **consumed, not rebuilt** | Qualitative Coding's grounded-theory export is the path; the workbench reads it. Its outside-researcher check (QC step 5) is still not done, so "validated" here means agreement with the corpus author's own coding, stated as such. |
| At least one computational or quantitative text path | kept, **workbench-owned** | No repository in `~/code2` measures text quantitatively (survey of capabilities.md and repo names, 2026-11-06); QC's quantitative follow-up can only say `conceptual_follow_up_only`. The workbench owns a narrow adapter around established libraries (roadmap 0.5 already says so). |
| Causal and theory work without category errors | **changed: within-case causal reasoning kept (Process Tracing); theory operationalization after 1.0** | PT's `pt_export_v2` already takes a QC handoff. Theory Forge has no consumer export and a stale roadmap; theory operationalization joins after 1.0. |
| One genuine qualitative–quantitative design with joint display and meta-inference | kept: exploratory sequential | The roadmap's recommended first design; a QC category becomes the measurement instrument under every condition of the repository's quantitative-strand brief (S2, open question Q16). |
| Human review, reflexivity, provenance, reporting, exports | kept | Slice S5; reflexivity is a researcher-positioning memo per study, kept with the review log and the bundle. |
| An observed benchmark | **changed** | From "multi-domain benchmark with expert review" to "two rights-clear corpora, each with its authors' own human coding as the reference, held-out interviews, and planted failures that must be caught". Whether 1.0 also needs an outside researcher's hour is open question Q12. |
| Roadmap phases B–E (shared-profile gate, shared extraction action, NYC refactor, QC/PT seam proof) as prerequisites | **cut** | Their premise was a shared capability across methods. The Plan #6 crosswalk adjudicated 36 groups: 29 different capability, 7 shared shell only, 0 same capability (`docs/research/method_decomposition/phase5/adjudication.yaml`). There is nothing shared to build first. Shared code is extracted only after two real slices use the same thing. |
| NYC Congestion Relief Zone as the stable example | **cut** | Paused by Brian 2026-10-04; he did not knowingly choose it. |
| Versions 0.2 (OntoCanon/DIGIMON), 0.3 (theory recommendation), 0.6–0.8 (more designs, QCA, method portfolio) | **after 1.0** | Not needed for any 1.0 condition; they are breadth, which the roadmap itself says comes after 1.0. |

**Example corpus.** "Semi-structured interviews with linguists about Open Science" by Elen Le Foll (Zenodo
record 17630137, CC BY-SA 4.0, anonymised, participants consented to open publication). It suits a general
tool: 26 interview transcripts on a non-policy topic, the author's own coding of 837 passages under 39
codes, exported from OpenQDA (a human reference for every strand), and Qualitative Coding's grounded-theory
result on 25 of the interviews already exists. Nothing is sent to the author (Qualitative Coding's outreach
to her is parked). A second corpus for the benchmark is chosen by the agent in S6 under the same rules
(open licence, consent, the authors' own coding published) and must differ from the first in subject, in
research team and in the coding tool or export format (open question Q19).

## Slices, in order

Each slice ends with something a person can open and try. Every slice: tests first, `make check` and
`pytest` exit 0, merged through `ship`, page rendered and looked at before it is reported.

| # | Slice | What a person can open and try at the end |
| --- | --- | --- |
| S0 | Plan 007 upkeep: deploy the current public page, stale-page test (done 2026-11-06, PR #59); then the remaining Plan 007 steps (deploy rule, NYC relabel, repo.yaml, wiki, architecture pointer) alongside S1–S2 | The public PsychosisBank page serves the committed bytes; `pytest` fails on a stale `deploy/` page |
| S1 | Governed corpus and qualitative strand | The study page (`make study-page`): the 26 frozen interviews with licence and hash status, QC's categories and propositions, each supporting passage opening the interview at that place with its speaker, the author's codes beside them, and the quantitative and integration strands shown as "not built" |
| S2 | Quantitative strand: one QC category measured across every interviewee turn | The same page gains a measurement tab: the feasibility readout, the instrument (rule, included and excluded examples), each candidate measure beside its baselines, which interviews tuned and which tested it, prevalence error and agreement on held-out interviews, a shuffled-label control, and every disagreement listed and openable |
| S3 | Joint display and meta-inference | A joint-display tab: one row per proposition, the qualitative claim beside the measured distribution, a convergence / complementarity / divergence / silence verdict with the passages behind it, and a bounded meta-inference that stays "pending review" |
| S4 | Process Tracing on one proposition | A causal tab: QC handoff → PT `pt_export_v2` for one proposition in one interview; within-case verdicts shown apart from the measured prevalence, and the publication gate respected |
| S5 | Review, provenance and export, on one investigation record | The study page becomes the general investigation record (question, evidence, method runs, findings, unresolved questions, reviews, next actions), the PsychosisBank investigation rebuilt as one instance of it; accept, reject or annotate each meta-inference and see it saved; write a reflexivity memo; download one research bundle (corpus manifest, strand exports, joint display, decisions, traces, a GRAMMS reporting checklist). Served where open question Q11 says |
| S6 | Second corpus and benchmark | A benchmark page: both corpora, each strand's agreement with the authors' coding, every planted failure and whether it was caught, cost and time per run, and for each corpus the files its addition changed ("data only" or the code paths, in orange) |
| S7 | 1.0 release | The method-profile page marks what the workbench runs and what it does not; the crosswalk page (acceptance A2) shows the Plan #6 verdicts; the release bundle lists unsupported methods as prominently as supported ones |

### S1 — Governed corpus and qualitative strand

- **Build:** a study definition file (`examples/studies/open_science/study.json`: source record, file
  pattern, the author's coding columns, the producer export paths) drives everything; nothing about this
  corpus is written into `src/`. `scripts/freeze_study_inputs.py` downloads the Zenodo files, checks each
  against the record's md5, and writes the texts and a typed `CorpusManifest` (DOI, licence, consent
  statement, per-file sha256, retrieval date) under `examples/studies/open_science/`. A permissive consumer view of QC's
  grounded-theory package (schema 3, pinned by QC commit and sha256) and of QC's segments; each segment's
  offsets are checked against the frozen text. The author's coded passages are checked the same way.
  `src/mixed_methods_workbench/study_workbench.py` builds the payload; a static page renders it.
- **Checks:** md5 of every file equals Zenodo's; every QC segment the theory cites resolves and its text
  equals the frozen source at its offsets (counted, mismatches listed, never silently dropped); an
  unsupported QC schema major version is refused; the committed page equals what the builder produces.
- **Trace:** `examples/studies/open_science/build_receipt.json`: input hashes, each step with its counts,
  output hashes. Read by the building agent before reporting; no model calls.
- **Cost:** none (no AI step).

### S2 — Quantitative strand

S2 follows every condition of the repository's quantitative-strand brief
(`docs/decisions/2026-07-12-first-quantitative-text-strand.md`), adopted in open question Q16; the plan
does not relax any of them.

- **Unit of analysis** (open question Q17): one interviewee turn, as Qualitative Coding segmented it (630
  interviewee turns in the 25 analysed interviews; interviewer turns are not measured). A turn is a
  positive reference case for the construct when any of the author's passages coded with the matching code
  overlaps it. Her passages vary in length and overlap one another; each maps to the turns it overlaps, and
  passages that fall only on interviewer turns are counted and listed, not dropped. The interview, not the
  turn, is the independent group: splits, intervals and the prevalence estimate are by interview, and no
  turn-level confidence interval is reported.
- **Construct** (open question Q15): the QC category with the most supporting passages that also has a
  matching author code, picked by that written rule and shown on the page with the rule.
- **Feasibility readout first:** before any instrument is chosen, the page shows the construct, unit,
  frame, intended and prohibited uses, its prevalence among the turns, how many interviews carry positive
  cases, whether it is lexical or contextual, and the disagreement locations in the author's own coding.
  If too few interviews carry positive cases for a grouped held-out test, S2 stops there and says so,
  choosing the next category by the same rule.
- **Measures, all compared on the same grouped splits:** the always-majority (dummy) baseline; the
  mandatory word-list count (dictionary) baseline, its word list frozen from tuning interviews only; a
  word-weighting (TF-IDF) regularised logistic regression; and a codebook-prompted language model through
  `llm_client` applying QC's instrument to each turn (structured output: yes or no, the quoted words it
  rests on). The language model is a challenger, not ground truth; the primary instrument is chosen from the
  readout and the tuning folds, never from the held-out interviews. Embedding or topic output is not a
  candidate for the first measure.
- **Results:** per-class agreement, prevalence error per interview and overall (accuracy alone is never
  shown), calibration where a measure gives probabilities, a bootstrap interval by interview, and which
  interviews tuned and which tested each figure. Negative controls: shuffled labels must fall to chance,
  the dummy must show its null, and a split that puts one interview on both sides must fail the split
  check.
- **No second model in S2.** A second model is added only after the traces show a gap it would close, and
  then the cases it re-judges are chosen without the author's codes (for example, where the language model
  and the regression disagree); the author's coding never selects or changes a prediction.
- **Known limit, stated on the page:** QC built its theory from all 25 interviews, so the construct was not
  discovered on separate text; S2 reports measurement agreement, not an out-of-sample construct test. S6's
  second corpus is the held-out test.
- **Trace:** every model call through `llm_client` with task `mixed_methods_workbench.open_science.measure`
  and a trace id; a run receipt with inputs, the split manifest, each call's id, tokens and cost, and
  outputs. The agent reads every disagreement's full trace and a sample of 20 agreements before reporting.
- **Cost (computed, not measured):** 630 turns × 1 call × a measured per-call figure from the closest
  existing task, QC's `qualitative_coding.gt_constant_comparison.application` (one inclusion rule applied to
  one passage: median $0.0011, p90 $0.0019 per call, 4,052 input tokens, 0% cached; `llm-cost estimate`,
  708 calls, 2026-11-05). About $0.69 per full pass (p90 $1.20). The dictionary, dummy and regression run
  locally at no model cost.
- **Cheapest design that still does the job:** one call per turn with the instrument as a cached prefix.
  The cheaper alternative, one call per interview labelling all its turns at once (26 calls; about 0.27M
  instead of 2.6M input tokens, by the reviewer's estimate of 300 tokens per turn), is run on the tuning
  interviews in the feasibility readout and adopted if its agreement is no worse; per-turn calls are the
  default because labels from one long call can influence one another and long-context labelling can lose
  accuracy. Quality decides, not cost: both options cost under a dollar per pass.

### S3 — Joint display and meta-inference

- **Build:** for each QC proposition, a draft integration verdict and bounded meta-inference through
  `llm_client`, citing passage ids and the measured numbers; a second, different model challenges each draft
  (as the PsychosisBank independent challenge did, the existing `verification_challenge`). Both stay
  "pending review" until S5's review.
- **Trace:** task `mixed_methods_workbench.open_science.integrate`; receipt as in S2. The agent reads every
  draft and challenge in full.
- **Cost (computed):** 6 propositions × 2 calls × the measured per-call figure of QC's
  `qualitative_coding.grounded_theory_verdict` (median $0.0038, p90 $0.0111 per call, 15,196 input tokens;
  `llm-cost estimate`, 55 calls). About $0.05 per run (p90 $0.13).

### S4 — Process Tracing on one proposition

- **Build:** QC `export-process-tracing-handoff` → PT draft-audit route → `pt_export_v2`; the workbench reads
  only `pt_export_v2`. Its existing reader (`investigation_run.py`) reads
  `comparative_conclusion.public_headline_eligible`; S4 extends it to read PT's
  `publication_gate.publishable` (`process_tracing/pt/export.py`, `PublicationGateV2`) and shows a causal
  conclusion only when both allow it.
- **Trace:** PT's own trace ids recorded in a connected-run receipt (the existing `investigation_run.py`
  shape).
- **Cost (guess, from a measured total):** PT's `process_tracing.draft_audit.*` tasks total $0.233
  (`llm-cost cost --group-by task`, 2026-11-06); the number of runs behind it, about 6, is a guess, so about
  $0.04 per run is a guess. Replaced by the run receipt's own total after S4's first run.

### S5 — Review, provenance and export

- **Build:** the study record becomes the general investigation record of the product map: the question,
  evidence, method runs, findings, unresolved questions, reviews and next actions of one study, read from the
  study definition; `investigation_spine.py`'s PsychosisBank investigation is rebuilt as one instance of it
  and its public page must still pass `tests/test_psychosisbank_public_review.py`. A local server in the
  `method_dashboard_server.py` pattern; review decisions and the reflexivity memo written to typed JSON files
  in the study folder and committed; the bundle is a zip of committed files plus a manifest of hashes. QDPX
  exchange is reused from QC's export, not rebuilt.
- **Trace:** each review action appended to one review log per day; the bundle's manifest lists every trace.
- **Cost:** none (no AI step).

### S6 — Second corpus and benchmark

- **Build:** the whole S1–S3 path on a second rights-clear corpus with its authors' coding, differing from
  the first in subject, research team and coding tool or export format (Q19); planted failures (a quote
  altered by one word, a passage from the wrong interview, a swapped label, a fabricated segment id) that
  the checks must catch. The second corpus is added by one study definition file plus its frozen data; the
  benchmark builder lists the files that commit changed and shows "data only" or, in orange, any code path
  (the test of "not for a specific use case"). If the second corpus's export format needs a new reader, that
  reader is general (named by format, not by corpus) and the page says so.
- **Trace:** one receipt per run; the benchmark page links each.
- **Cost (computed):** S2 + S3 on a corpus of similar size from the same per-call figures, about 642 calls
  and $0.74 per run; three repeat runs to show variation, about $2.21. Redone with `llm-cost estimate` on
  S2's own task once S2 has run.

### S7 — 1.0 release

- **Build:** method-profile page states supported and unsupported paths; release notes; version tag.
- **Cost:** none (no AI step).

## Relies on

`study_definition`, `study_corpus`, `qc_theory_export`, `qualitative_strand`, `source_segment`,
`evidence_anchor`, `author_coding`, `workbench_view`, `measurement_instrument`, `measured_result`,
`joint_display`, `meta_inference`, `verification_challenge`, `pt_export`, `publication_gate`,
`connected_run_receipt`, `investigation_record`, `review_decision`, `research_bundle`, `planted_failure`,
`benchmark`, `method_profile`, `public_review` (see `docs/planning/DOMAIN.md`).

## Not in this plan

Running a qualitative method inside the workbench; a universal schema or method planner; OntoCanon, DIGIMON
or Theory Forge on the critical path; contacting any corpus author; publishing anything beyond the existing
PsychosisBank Worker without Brian's answer to open question Q11.

## Done when

S7 is merged: on two rights-clear corpora a person can open one investigation record per study, follow
every claim to its passage, see the quantitative strand's agreement with the authors' coding, read each meta-inference with its
review state, download the bundle, and read on the benchmark page what works, what fails and what it cost.
