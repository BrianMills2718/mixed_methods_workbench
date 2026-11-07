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

## What "finished" means here

The roadmap's 1.0 (`docs/ROADMAP.md`, "What 1.0 Means") is kept as the target, with five changes. Each
change follows from evidence gathered on 2026-11-06 (`docs/planning/investigation.json`).

| 1.0 condition | Kept or changed | Why |
| --- | --- | --- |
| Governed study and corpus foundation | kept | Slice S1. |
| Method profiles that keep each tradition's validity rules | kept, reusing the method dashboard | `method_dashboard.py` already routes questions to method profiles; S7 marks which profiles the workbench actually runs. |
| At least one validated qualitative path | kept, **consumed, not rebuilt** | Qualitative Coding's grounded-theory export is the path; the workbench reads it. Its outside-researcher check (QC step 5) is still not done, so "validated" here means agreement with the corpus author's own coding, stated as such. |
| At least one computational or quantitative text path | kept, **workbench-owned** | No repository in `~/code2` measures text quantitatively (survey of capabilities.md and repo names, 2026-11-06); QC's quantitative follow-up can only say `conceptual_follow_up_only`. The workbench owns a narrow adapter around established libraries (roadmap 0.5 already says so). |
| Causal and theory work without category errors | kept, **Process Tracing only on the critical path** | PT's `pt_export_v2` already takes a QC handoff. Theory Forge has no consumer export and a stale roadmap; it joins after 1.0. |
| One genuine qualitative–quantitative design with joint display and meta-inference | kept: exploratory sequential | The roadmap's recommended first design; QC categories become the measurement instrument. |
| Review, provenance, reporting, exports | kept | Slice S5. |
| An observed benchmark | **changed** | From "multi-domain benchmark with expert review" to "two rights-clear corpora, each with its authors' own human coding as the reference, held-out interviews, and planted failures that must be caught". Whether 1.0 also needs an outside researcher's hour is open question Q12. |
| Roadmap phases B–E (shared-profile gate, shared extraction action, NYC refactor, QC/PT seam proof) as prerequisites | **cut** | Their premise was a shared capability across methods. The Plan #6 crosswalk adjudicated 36 groups: 29 different capability, 7 shared shell only, 0 same capability (`docs/research/method_decomposition/phase5/adjudication.yaml`). There is nothing shared to build first. Shared code is extracted only after two real slices use the same thing. |
| NYC Congestion Relief Zone as the stable example | **cut** | Paused by Brian 2026-10-04; he did not knowingly choose it. |
| Versions 0.2 (OntoCanon/DIGIMON), 0.3 (theory recommendation), 0.6–0.8 (more designs, QCA, method portfolio) | **after 1.0** | Not needed for any 1.0 condition; they are breadth, which the roadmap itself says comes after 1.0. |

**Example corpus.** "Semi-structured interviews with linguists about Open Science" by Elen Le Foll (Zenodo
record 17630137, CC BY-SA 4.0, anonymised, participants consented to open publication). It suits a general
tool: 26 interview transcripts on a non-policy topic, the author's own MAXQDA coding of 837 passages under
26 codes (a human reference for every strand), and Qualitative Coding's grounded-theory result on 25 of the
interviews already exists. Nothing is sent to the author (Qualitative Coding's outreach to her is parked).
A second corpus for the benchmark is chosen by the agent in S6 under the same rules (open licence, consent,
the authors' own coding published).

## Slices, in order

Each slice ends with something a person can open and try. Every slice: tests first, `make check` and
`pytest` exit 0, merged through `ship`, page rendered and looked at before it is reported.

| # | Slice | What a person can open and try at the end |
| --- | --- | --- |
| S0 | Plan 007 upkeep: deploy the current public page, stale-page test (done 2026-11-06, PR #59); then the remaining Plan 007 steps (deploy rule, NYC relabel, repo.yaml, wiki, architecture pointer) alongside S1–S2 | The public PsychosisBank page serves the committed bytes; `pytest` fails on a stale `deploy/` page |
| S1 | Governed corpus and qualitative strand | The study page (`make study-page`): the 26 frozen interviews with licence and hash status, QC's categories and propositions, each supporting passage opening the interview at that place with its speaker, the author's codes beside them, and the quantitative and integration strands shown as "not built" |
| S2 | Quantitative strand: one QC category measured across every interviewee passage | The same page gains a measurement tab: the instrument (rule, included and excluded examples), the measure per interview, and its agreement with the author's coding on held-out interviews, with every disagreement listed and openable |
| S3 | Joint display and meta-inference | A joint-display tab: one row per proposition, the qualitative claim beside the measured distribution, a convergence / complementarity / divergence / silence verdict with the passages behind it, and a bounded meta-inference that stays "pending review" |
| S4 | Process Tracing on one proposition | A causal tab: QC handoff → PT `pt_export_v2` for one proposition in one interview; within-case verdicts shown apart from the measured prevalence, and the publication gate respected |
| S5 | Review, provenance and export | A local workbench server (`make study-workbench`): accept, reject or annotate each meta-inference and see it saved; download one research bundle (corpus manifest, strand exports, joint display, decisions, traces, a GRAMMS reporting checklist) |
| S6 | Second corpus and benchmark | A benchmark page: both corpora, each strand's agreement with the authors' coding, every planted failure and whether it was caught, cost and time per run |
| S7 | 1.0 release | The method-profile page marks what the workbench runs and what it does not; the release bundle lists unsupported methods as prominently as supported ones |

### S1 — Governed corpus and qualitative strand

- **Build:** `scripts/freeze_open_science_corpus.py` downloads the Zenodo files, checks each against the
  record's md5, and writes the texts and a typed `CorpusManifest` (DOI, licence, consent statement, per-file
  sha256, retrieval date) under `examples/studies/open_science/`. A permissive consumer view of QC's
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

- **Build:** the agent picks the construct by a written rule: the QC category with the most supporting
  passages that also has a matching author code (so a human reference exists). The instrument is QC's own
  category definition with its included and excluded passages. Two measures, compared: (a) an LLM annotation
  of each interviewee passage through `llm_client` applying the instrument (structured output: yes/no, the
  quoted words it rests on); (b) a regularised logistic regression on sentence embeddings trained on the
  author's labels. Agreement with the author's coding is computed on interviews held out by group
  (leave-interviews-out folds), with bootstrap intervals by interview.
- **Known limit, stated on the page:** QC built its theory from all 25 interviews, so the construct was not
  discovered on separate text; S2 reports measurement agreement, not an out-of-sample construct test. S6's
  second corpus is the held-out test.
- **Trace:** every model call through `llm_client` with task `mixed_methods_workbench.open_science.measure`
  and a trace id; a run receipt with inputs, each call's id, tokens and cost, and outputs. The agent reads
  every disagreement's full trace and a sample of 20 agreements before reporting.
- **Cost:** about 650 interviewee passages × 1 call. Measured analogue: QC's
  `qualitative_coding.gt_constant_comparison.application` (applying one inclusion rule to one passage),
  median $0.0011, p90 $0.0019 per call, 4,052 input tokens, 0% cached (`llm-cost estimate`, 708 calls,
  2026-11-05). So about $0.72 per full pass (p90 $1.24); a second model on every disagreement adds under
  $0.30. The embedding classifier runs locally at no model cost. Cheapest design that still does the job:
  one pass with one model plus the second model only on disagreements, not two full passes.

### S3 — Joint display and meta-inference

- **Build:** for each QC proposition, a draft integration verdict and bounded meta-inference through
  `llm_client`, citing passage ids and the measured numbers; a second, different model challenges each draft
  (as the PsychosisBank independent challenge did). Both stay "pending review" until S5's review.
- **Trace:** task `mixed_methods_workbench.open_science.integrate`; receipt as in S2. The agent reads every
  draft and challenge in full.
- **Cost:** 6 propositions × 2 calls. Measured analogue: QC's `qualitative_coding.grounded_theory_verdict`,
  median $0.0038, p90 $0.0111 per call, 15,196 input tokens (`llm-cost estimate`, 55 calls). About $0.05 per
  run (p90 $0.13).

### S4 — Process Tracing on one proposition

- **Build:** QC `export-process-tracing-handoff` → PT draft-audit route → `pt_export_v2`; the workbench reads
  only `pt_export_v2` and requires `publication_gate.publishable` before showing a causal conclusion.
- **Trace:** PT's own trace ids recorded in a connected-run receipt (the existing `investigation_run.py`
  shape).
- **Cost:** measured: PT's `process_tracing.draft_audit.*` tasks total $0.233 over about 6 runs
  (`llm-cost cost --group-by task`, 2026-11-06), about $0.04 per run.

### S5 — Review, provenance and export

- **Build:** a local server in the `method_dashboard_server.py` pattern; review decisions written to a typed
  JSON file in the study folder and committed; the bundle is a zip of committed files plus a manifest of
  hashes. QDPX exchange is reused from QC's export, not rebuilt.
- **Trace:** each review action appended to one review log per day; the bundle's manifest lists every trace.
- **Cost:** none (no AI step).

### S6 — Second corpus and benchmark

- **Build:** the whole S1–S3 path on a second rights-clear corpus with its authors' coding; planted failures
  (a quote altered by one word, a passage from the wrong interview, a swapped label, a fabricated segment id)
  that the checks must catch. The second corpus is added by one study definition file plus its frozen
  data; the commit that adds it changes nothing under `src/` (the test of "not for a specific use case").
- **Trace:** one receipt per run; the benchmark page links each.
- **Cost:** from the same measured per-call figures: S2 + S3 on a corpus of similar size, 662 calls, about
  $0.77 per run; three repeat runs to show variation, about $2.31. The figure is redone with `llm-cost estimate` on S2's own task once S2 has run.

### S7 — 1.0 release

- **Build:** method-profile page states supported and unsupported paths; release notes; version tag.
- **Cost:** none (no AI step).

## Relies on

`study_corpus`, `qualitative_strand`, `source_segment`, `evidence_anchor`, `producer_export`,
`workbench_view`, `measurement_instrument`, `joint_display`, `meta_inference`, `publication_gate`,
`public_review` (see `docs/planning/DOMAIN.md`).

## Not in this plan

Running a qualitative method inside the workbench; a universal schema or method planner; OntoCanon, DIGIMON
or Theory Forge on the critical path; contacting any corpus author; publishing anything beyond the existing
PsychosisBank Worker without Brian's answer to open question Q11.

## Done when

S7 is merged: on two rights-clear corpora a person can open the study page, follow every claim to its
passage, see the quantitative strand's agreement with the authors' coding, read each meta-inference with its
review state, download the bundle, and read on the benchmark page what works, what fails and what it cost.
