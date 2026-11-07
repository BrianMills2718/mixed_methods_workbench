# Plan #8: finish the workbench (1.0) on a general, rights-clear study

Status: adopted 2026-11-06 on Brian's direction below; slice S1 in progress.

Planning package: docs/planning/planning-package.json

## Goal

Brian, 2026-11-06, answering open question Q1 ("what the workbench does next"), whose recommendation had been
upkeep only until a real study needed two methods' results joined (source: docs/planning/open-questions.json:27):

> "on mixed mtheod work bench finsih that is not for a specific use case it is part of my broader vision" (source: docs/planning/open-questions.json:27)

For Brian and any researcher who joins qualitative and quantitative evidence, change today's hand-joining of separate
method pages, done afresh for each study, into one general workbench finished to its 1.0, part of his broader evidence-to-action
vision; a study proves each slice on real text and is an example, not the product's purpose (agent judgment, unconfirmed).

**Broader vision, read from the repository** (open question Q18; Brian decides between two readings). The
repository's own product map, `docs/EVIDENCE_TO_ACTION_PRODUCT_INTEGRATION_MAP.md`, supports two readings.
Section 1 defines the workbench's place: one workbench-owned investigation record that keeps the question,
evidence, analytical plan, method runs, findings, unresolved questions, reviews and next actions together, while each
method stays in its own repository; section 3 names "separate destinations rather than one evolving study"
as the defect. Sections 5, 7 and 9 go further: the product runs from a policy question to a reviewed
recommendation, Open Science is "too weak to organize the general policy-analysis product", and the next
step is a completed public policy decision case. This plan follows the first reading, which fits "not for
a specific use case": every slice adds to one study record per corpus, built from a study definition file,
not a new page per feature, and S5 makes that record the general form of the existing PsychosisBank
investigation record (`investigation_spine.py`, today hard-coded to one investigation). Open Science is
used to prove the methods on real text, not as the policy flagship. If Brian picks the second reading, S6's
second study becomes a completed public policy decision and the record runs to a reviewed recommendation
(Q18 says what that costs) (source: docs/EVIDENCE_TO_ACTION_PRODUCT_INTEGRATION_MAP.md:15-17). Which reading he meant is agent judgment, unconfirmed.

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
| Causal and theory work without category errors | **changed: within-case causal reasoning kept (Process Tracing); theory operationalization after 1.0** | Process Tracing's frozen pipeline takes a QC handoff and writes `pt_export_v2`; its answer path, the draft-audit prototype, does neither yet, so S4 adds a handoff input and a partial export (open question Q23). That answer path carries no publication gate, so in 1.0 no causal conclusion from it is shown as published: the line reads "withheld". Theory Forge has no consumer export and a stale roadmap; theory operationalization joins after 1.0. This narrows what 1.0 promises, so it is Brian's call with the benchmark change (open question Q12). |
| One genuine qualitative–quantitative design with joint display and meta-inference | kept: exploratory sequential | The roadmap's recommended first design; one of the author's codes, picked by how much of a QC category's evidence it holds, becomes the measurement instrument under the conditions of the repository's quantitative-strand brief, with the two it cannot meet named (S2, open question Q16). |
| Human review, reflexivity, provenance, reporting, exports | kept | Slice S5; reflexivity is a researcher-positioning memo per study, kept with the review log and the bundle. |
| An observed benchmark | **changed** | From "multi-domain benchmark with expert review" to "two rights-clear corpora, each with its authors' own human coding as the reference, held-out interviews, and planted failures that must be caught". Whether 1.0 also needs an outside researcher's hour is open question Q12. |
| Roadmap phases B–E (shared-profile gate, shared extraction action, NYC refactor, QC/PT seam proof) as prerequisites | **cut** | Their premise was a shared capability across methods. The Plan #6 crosswalk adjudicated 36 groups: 29 different capability, 7 shared shell only, 0 same capability (`docs/research/method_decomposition/phase5/adjudication.yaml`). There is nothing shared to build first. Shared code is extracted only after two real slices use the same thing. |
| NYC Congestion Relief Zone as the stable example | **cut** | Paused by Brian 2026-10-04; he did not knowingly choose it. |
| Versions 0.2 (OntoCanon/DIGIMON), 0.3 (theory recommendation), 0.6–0.8 (more designs, QCA, method portfolio) | **after 1.0** | Not needed for any 1.0 condition; they are breadth, which the roadmap itself says comes after 1.0. |

**Example corpus.** "Semi-structured interviews with linguists about Open Science" by Elen Le Foll (Zenodo
record 17630137, CC BY-SA 4.0, anonymised, participants consented to open publication). It suits a general
tool: 26 interview transcripts on a non-policy topic, the author's own coding of 837 passages under 39
codes, exported from OpenQDA (a human reference for every strand), and Qualitative Coding's grounded-theory
result on 25 of the interviews already exists. The product map keeps it for exactly this (a real QC
round trip) and warns against using it as the policy-analysis flagship (section 7); here it is a method
proof, not the flagship (Q18). Nothing is sent to the author (Qualitative Coding's outreach
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
| S2 | Quantitative strand: one coded theme measured across every interviewee turn | The same page gains a measurement tab: the feasibility readout, the instrument (rule, included and excluded examples), each candidate measure beside its baselines, which interviews tuned and which tested it, prevalence error and agreement on held-out interviews, a shuffled-label control, and every disagreement listed and openable |
| S3 | Joint display and meta-inference | A joint-display tab: one row per proposition, the qualitative claim beside the measured distribution, a "complements" or "silent: not measured" verdict with the passages behind it (a prevalence cannot confirm or contradict a when-then claim, Q22), and a bounded meta-inference that stays "pending review" |
| S4 | Process Tracing on one proposition | A causal tab: QC handoff → Process Tracing's draft-audit answer path → its partial export, for one proposition in one interview; within-case verdicts shown apart from the measured prevalence, the conclusion "withheld" while no gate allows it, and a "how the gate behaves" panel opening two made-up test exports (one publishable, one blocked) |
| S5 | Review, provenance and export, on one investigation record | The study page becomes the general investigation record (question, evidence, analytical plan, method runs, findings, unresolved questions, reviews, next actions), the PsychosisBank investigation rebuilt as one instance of it; accept, reject or annotate each meta-inference and see it saved; write a reflexivity memo; download one research bundle (corpus manifest, strand exports, joint display, decisions, traces, a GRAMMS reporting checklist). Served where open question Q11 says |
| S6 | Second corpus and benchmark | A benchmark page: both corpora, each strand's agreement with the authors' coding, every planted failure and whether it was caught, cost and time per run, and for each corpus the files its addition changed ("data only" or the code paths, in orange) |
| S7 | 1.0 release | The method-profile page marks what the workbench runs and what it does not; the crosswalk page (acceptance A2) shows the Plan #6 verdicts; the release bundle lists unsupported methods as prominently as supported ones |

### S1 — Governed corpus and qualitative strand

- **Build:** a study definition file (`examples/studies/open_science/study.json`: source record, file
  pattern, the author's coding columns, the producer export paths) drives everything; nothing about this
  corpus is written into `src/`. `scripts/freeze_study_inputs.py` downloads the Zenodo files, checks each
  against the record's md5, and writes the texts and a typed `CorpusManifest` (DOI, licence, consent
  statement, per-file sha256, retrieval date) under `examples/studies/open_science/`. A permissive consumer view of QC's
  grounded-theory package (schema 3, pinned by QC commit and sha256) and of QC's segments; each segment's
  offsets are checked against the frozen text (after the recorded CRLF-to-LF normalisation). The author's
  OpenQDA offsets do not point at the published text (12 of 837 match), so her passages are located by
  their own words: exact, whitespace-only difference, text differs, or not found, each counted, and the
  ones whose text differs or is not found listed on the page (open question Q14).
  `src/mixed_methods_workbench/study_workbench.py` builds the payload; a static page renders it.
- **Checks:** md5 of every file equals Zenodo's; every QC segment the theory cites resolves and its text
  equals the frozen source at its offsets (counted, mismatches listed, never silently dropped); an
  unsupported QC schema major version is refused; the committed page equals what the builder produces.
- **Trace:** `examples/studies/open_science/build_receipt.json`: input hashes, each step with its counts,
  output hashes. Read by the building agent before reporting; no model calls.
- **Cost:** none (no AI step).

### S2 — Quantitative strand

S2 takes its method from the repository's quantitative-strand brief
(`docs/decisions/2026-07-12-first-quantitative-text-strand.md`). The brief was never approved (its status
line reads "decision required; documentation only"); open question Q16 adopts its conditions as S2's
method, and the table below says how each is met or, where it is not, why. The brief's two calls for
Brian are kept as his: the exact construct (Q15) and authorising the slice (his 2026-11-06 direction to
finish).

| Brief condition (line) | In S2 |
| --- | --- |
| A narrow, case-specific adapter owned by the workbench (`:25`) | **overridden** by Brian's 2026-11-06 "not for a specific use case": the adapter is general (it reads any study definition), and S6's second corpus tests that |
| One typed core behind every interface (`:83-85`) | kept: `study_workbench.py` is the core; the page builder and the command line call it, never their own copy |
| Word-list count baseline mandatory; always-majority and TF-IDF baselines (`:18`, `:113`) | kept |
| Human-only baseline (`:113`) | **not met**: there is one human coder and no second human labelling, so no human-only figure exists; the page says so beside the baselines |
| Strongest eligible contextual incumbent (`:113`) | the codebook-prompted language model is the contextual comparator; **no fine-tuned encoder**, because 25 interviews give too few groups for a grouped held-out fine-tune |
| Language model is a challenger with behavioural and compliance tests (`:22-23`, `:136-137`, `:146-148`) | kept: label-free checks before any labelled evaluation (same answer when the turn is repeated, and when the instrument's order of examples changes), then a swapped-label control (another category's definition under this category's name), a codebook ablation (the instrument's rule removed) and an invented-label check (an answer outside yes/no is refused and counted) |
| Topic or embedding output not the first measure (`:21-22`) | kept; no topic model is run, so the topic-stability controls (`:140-142`) do not arise |
| Feasibility readout before choosing the instrument (`:87-99`) | kept |
| Metric margins, split sizes and thresholds preregistered from the readout, not hard-coded (`:102-103`) | kept: after the readout and before any measure is scored on held-out interviews, the agreement bar and the split sizes are written into the split manifest with the readout's figures behind them, and the receipt shows they were not changed afterwards; the construct-matching rule (Construct, below) was fixed in this plan from S1's data, before any measure exists |
| Learning curve and slices (`:114`) | kept: agreement on tuning folds at increasing numbers of tuning interviews, and every figure sliced by interview |
| Error costs and an accountable reviewer (`:110`) | kept: a false positive counts a turn that is not about the theme and inflates its prevalence; a false negative hides the interviews where it is rare; both are listed by interview and neither is traded for the other. Brian is the accountable reviewer (he can reject the result on the page), after the fresh reviewer below |
| Independently coded pilot and sealed set, with adjudication; a versioned codebook (`:111`) | **partly met**: the instrument is written for the author's own code, so the measure and its human reference name the same construct; but the reference is her existing single-coder coding with no adjudication, and her code has no written definition, so the instrument's definition is drafted from her tuning-interview passages, in one llm_client call (task `mixed_methods_workbench.open_science.define`, traced and costed below) that the building agent reads and edits, and versioned in the split manifest. The page says "one coder, no adjudication, definition drafted from her passages" beside every agreement figure |
| Immutable splits; nothing tuned sees sealed data (`:112`, `:126-129`) | kept: the split manifest fixes tuning and held-out interviews first; the receipt records which interviews each fitting step (word list, TF-IDF vocabulary, prompt edits) saw, and a check fails if any held-out interview appears there |
| Per-class metrics, prevalence error, calibration, grouped uncertainty; accuracy alone prohibited; no turn-level intervals (`:114`, `:118-121`) | kept |
| A count over a complete corpus has measurement error but no sampling error (`:118-121`) | kept: the 25 interviews are the whole corpus the count speaks for, so its interval is measurement error only (the instrument's held-out error rates, resampled by interview, applied to the count) and the page says it is not an estimate for linguists in general; agreement figures keep their by-interview interval, because those do generalise from tuning to held-out interviews |
| Dictionary polysemy, negation, quotation and attribution reach their error readouts (`:130-131`) | kept: the word list's false positives and false negatives on tuning interviews are listed with their words, so these errors can be read |
| Off-construct proxy, rare-case erasure, grouped shortcuts (`:132-135`) | kept as per-class recall and prevalence error by interview; there is one source, so source ablation does not arise |
| Ordinal label shuffling (`:138-139`) | does not arise: the label is yes or no |
| Fresh reviewer can reject promotion (`:116`) | kept: a fresh Claude Code session (no API cost) reads raw turns, splits, errors and traces before the result is called measured; Brian can reject it on the page |

- **Unit of analysis** (open question Q17): one interviewee turn, as Qualitative Coding segmented it (630
  interviewee turns in the 25 analysed interviews; interviewer turns are not measured). A turn is a
  positive reference case for the construct when any of the author's passages coded with the matching code
  overlaps it. Her passages vary in length and overlap one another; each maps to the turns it overlaps, and
  passages that fall only on interviewer turns are counted and listed, not dropped. The interview, not the
  turn, is the independent group: splits, intervals and the prevalence estimate are by interview, and no
  turn-level confidence interval is reported.
- **Construct** (open question Q15, Brian's call with a default): one of the author's codes, measured with
  its own human reference, chosen by how much of a QC category's evidence it holds, so the measure speaks to
  QC's theory and is checked against coding of the same construct. The rule, fixed now from S1's data
  (computed from S1's committed data: QC's segments and theory export, and the author's passages as S1
  locates them; S2's first test recomputes it and fails if it differs): leave out the author's 11 numbered interview-question
  codes (their names begin with the question's number, such as "1. subdisciplines"; they mark which
  question a passage answers, not a theme), listed on the page; for each QC category and each remaining
  code, count the interviewee turns QC cites for the category that the code also marks; a code qualifies for
  a category when it marks at least half of them and a one-sided chance test over the 630 turns
  (hypergeometric) gives below 0.001; take the code that qualifies with the largest share; if none does,
  S2 stops and says so. On S1's data (8 categories × 28 codes, 224 pairs) one code qualifies: "open data"
  marks 14 of the 22 turns QC cites for "Conditional and claim-adequate disclosure" (0.64, chance
  3 × 10⁻⁹) and 14 of the 21 for "Labour, governance, priority, credit, and scrutiny negotiation" (0.67,
  chance 1 × 10⁻⁹); the next best share is 0.48 ("resistance/reasons not to do OS"). "Open data" marks 72
  of the 630 turns (11%) in 23 of the 25 interviews, so a grouped held-out test is possible. A two-way
  overlap (turns both mark ÷ turns either marks) is shown but does not gate: QC marks only the turns it
  cites as examples (18–24 per category), so the highest two-way overlap among the 224 pairs is 0.18 and a
  0.3 floor could never be met. The page shows both counts, the share, the chance figure and the two-way
  overlap, such as "QC cites 22 turns; the code marks 14 of them and 72 in all", never a clean match.
  The page also says that QC's 8 categories rest on 6 distinct sets of cited turns: two pairs
  ("Traceable, linked, discoverable, and interpretable" with "Corrective, replicative, and reflexive
  reviewability"; "Terminological and audience boundary work" with "Attributed reuse, translation, and
  collaborative extension") cite exactly the same two incidents. The two categories "open data" qualified
  for are distinct, so the construct choice is unaffected.
- **Feasibility readout first:** before any instrument is chosen, the page shows the construct, unit,
  frame, intended and prohibited uses, its prevalence among the turns, how many interviews carry positive
  cases, whether it is lexical or contextual, and the disagreement locations in the author's own coding.
  If too few interviews carry positive cases for a grouped held-out test, S2 stops there and says so
  ("open data" has positive turns in 23 of the 25 interviews).
- **Measures, all compared on the same grouped splits:** the always-majority (dummy) baseline; the
  mandatory word-list count (dictionary) baseline, its word list frozen from tuning interviews only; a
  word-weighting (TF-IDF) regularised logistic regression; and a codebook-prompted language model through
  `llm_client` applying the instrument to each turn (structured output: yes or no, the quoted words it
  rests on). The language model is a challenger, not ground truth; the primary instrument is chosen from the
  readout and the tuning folds, never from the held-out interviews. Embedding or topic output is not a
  candidate for the first measure.
- **Results:** per-class agreement, prevalence error per interview and overall (accuracy alone is never
  shown), calibration where a measure gives probabilities, a bootstrap interval by interview, and which
  interviews tuned and which tested each figure. Negative controls: shuffled labels must fall to chance,
  the dummy must show its null, and a split that puts one interview on both sides must fail the split
  check, and a held-out interview found in any fitting step's inputs must fail the trace check. The
  language model's behavioural and compliance controls are in the table above.
- **No second model in S2.** A second model is added only after the traces show a gap it would close, and
  then the cases it re-judges are chosen without the author's codes (for example, where the language model
  and the regression disagree); the author's coding never selects or changes a prediction.
- **Known limit, stated on the page:** QC built its theory from all 25 interviews, and the code was chosen
  by its overlap with QC's cited turns across all of them, so the construct was not chosen on separate
  text. The choice used no measure's output, and the instrument's definition is drafted from tuning
  interviews only, so held-out agreement is not inflated by it; S2 reports measurement agreement, not an
  out-of-sample construct test. S6's second corpus is the held-out test.
- **Trace:** every model call through `llm_client` with task `mixed_methods_workbench.open_science.measure`
  and a trace id; a run receipt with inputs, the split manifest, each call's id, tokens and cost, and
  outputs. The agent reads every disagreement's full trace and a sample of 20 agreements before reporting.
- **Plain version first** (the comparison every AI answer path gets): the language model starts as the
  plain version, the same model given the whole source in two calls: one call with the instrument and every
  interviewee turn of the tuning interviews, and one with the instrument and every turn of the held-out
  interviews, each returning one label per turn (turn id, yes or no, the quoted words it rests on, capped by
  the output schema at about 40 tokens, so about 60 output tokens per label). The calls are split by
  tuning and held-out so nothing held out is in the call the prompt is tuned on. The whole corpus is
  108,452 tokens (all 1,277 turns, o200k tokenizer) and about 315 labels need about 19,000 output tokens,
  inside gpt-5.6-luna's 922,000-token input and 128,000-token output limits (LiteLLM's model information).
  Two stages are added only if the plain version shows a gap on the tuning interviews (turns left
  unlabelled, labels that repeat a neighbour's, or agreement below the word-list count): one call per
  interview, then one call per turn. Each is compared with the plain version on the tuning interviews
  only, kept only if its agreement there is better, and the held-out interviews are scored once, with the
  design chosen.
- **Cost (computed, not measured):** the plain version is 2 calls of about 58,000 input tokens (the
  instrument, 3,924 tokens, measured from QC's comparable instrument, plus half the corpus) and about
  19,000 output tokens, at gpt-5.6-luna's per-token rates fitted to the 708 recorded calls of QC's
  `qualitative_coding.gt_constant_comparison.application` (input $0.2168, output $1.4057 per million
  tokens; `llm-cost estimate`, 2026-11-05): about $0.04 a call, $0.08 for both. The stages, if a gap
  shows, on the tuning interviews only: one call per interview, 13 calls, about $0.15; one call per turn,
  315 calls at that task's median 4,052 input and 268 output tokens, about $0.40. The four language-model
  controls (repeat, reordered examples, swapped label, codebook ablation) each rerun the chosen design on
  the tuning interviews: with the plain version, 4 calls, about $0.16. Drafting the instrument's definition is one call over
  at most all 81 of her "open data" passages (55,001 characters, about 13,750 tokens at 4 characters a
  token, plus about 1,000 of instructions) with about 800 output tokens: about $0.004. The dictionary, dummy and regression
  run locally at no model cost.
- **Cheapest design that still does the job:** the plain version, two calls, about $0.08 per pass. It is
  also the starting design, so nothing more expensive is built unless the tuning interviews show the plain
  version falls short; quality decides, not cost, and every design here is under a dollar per pass.

### S3 — Joint display and meta-inference

- **Which rows can be compared** (open question Q22, resolved by a written rule): QC's six propositions
  are conditional statements ("when X, then Y") that each name two or three categories, and S2 measures one
  theme's prevalence. A prevalence cannot confirm or contradict a conditional, so each proposition is
  mapped, before any verdict is drafted, either to the measure (it names a QC category the measured code
  qualified for, Construct above) or to "silent: not measured". A mapped row may say only
  "complements" (the measure shows how widely the theme is talked about, beside the qualitative claim);
  the number and passage check refuses "converges" or "diverges" on a row matched by prevalence alone,
  and the page says why. A silent row shows the qualitative claim and the word "silent" in grey, with the
  reason. A row whose units differ (a turn-level claim against an interview-level figure) blocks
  aggregation and meta-inference, as the brief requires (`:143-144`), and says so in orange. The page
  states how many of the six rows are mapped. Measuring a proposition's condition and outcome together, so
  a row could converge or diverge, is a later slice's choice, not 1.0's.
- **Build:** for each mapped row, a draft integration verdict and bounded meta-inference through
  `llm_client` (the plain version below), citing passage ids and the measured numbers. A deterministic
  check (the number and passage check) then verifies that every number the draft cites equals the measured
  result, every passage id resolves, and no prevalence-only row says "converges" or "diverges"; a draft
  that fails is shown in orange with the failing number, id or verdict, never silently corrected. No second model
  challenges the drafts: the PsychosisBank challenge (`verification_challenge`) returned "bounded
  support" on all three of its findings and changed no answer, so a challenger is added only when S3's
  traces show a gap it would close. Drafts stay "pending review" until S5's review.
- **Plain version first:** S3 starts with one call given all six propositions, the mapping, the measured
  result and the passages, returning every row's verdict and bounded meta-inference. One draft per mapped
  proposition is a stage added only if the plain call shows a gap on the number and passage check (a
  number not in the measured result, a passage id that does not resolve, a verdict the rule refuses) or on
  Brian's review; the two are then shown side by side.
- **Trace:** task `mixed_methods_workbench.open_science.integrate`; receipt as in S2. The agent reads every
  draft in full.
- **Cost (computed):** the plain version is one call over all six propositions: at most 6 × the closest
  measured task's median input, QC's `qualitative_coding.grounded_theory_verdict` (`llm-cost estimate`, 55
  calls: median 15,196 input and 807 output tokens), so about 91,000 input and 4,800 output tokens, at
  gpt-6-luna's per-token rates fitted to its recorded calls (input $0.1354, output $0.2895 per million
  tokens): about $0.014 per run, an upper figure because the shared passages are counted six times. The
  per-proposition stage, if a gap shows, is at most 6 calls at the same total. Redone from S3's receipt.

### S4 — Process Tracing on one proposition

- **Route** (open question Q23): Process Tracing's answer path is its draft-audit prototype (its ADR
  0004, approved by Brian on 2026-11-05 and confirmed on a fresh case on 2026-11-06), which writes no
  `pt_export_v2` (ADR 0004, "Bad: the prototype writes no `pt_export_v2.json` for
  `mixed_methods_workbench` (Q20)"), and its pipeline (`pt/`, which does accept a QC handoff and write the
  gated export) has been frozen since 2026-09-30. So S4 starts with producer work in `process_tracing`,
  under that repository's own rules: (1) a qualitative-handoff input to the prototype, so QC's
  `export-process-tracing-handoff` output for the chosen proposition becomes a draft-audit case; (2) the
  small export adapter Process Tracing's own open question Q20 recommends once a consumer resumes, which
  writes only the fields the merged answer supports and marks the rest absent, never a full V2 claim. No
  `pt/` code changes and the frozen pipeline is not run.
- **Schema:** the adapter's file declares its own schema, provisionally `pt_draft_audit_export_v1` (Process
  Tracing names it when it builds the adapter), never `pt_export_v2`. The workbench's reader
  `ProcessTracingExport` (`investigation_run.py:101-113`) requires `schema_version` "pt_export_v2" and every
  section, so S4 adds a second, partial reader in which the comparative conclusion, the publication gate
  and any section the merged answer does not support are optional and shown as "absent". QC's
  `export-process-tracing-handoff` exports the project's claims (`state.claims`,
  `qualitative_coding/qc_clean/core/process_tracing_handoff.py:221`), so S4 first checks that the Open
  Science project state carries the chosen proposition as an anchored claim of QC's `GT_PROPOSITION` kind
  (`qc_clean/core/claims.py:33`).
- **Build:** the workbench reads only that export. Its existing reader (`investigation_run.py`) reads
  `comparative_conclusion.public_headline_eligible`; S4 extends it to read `publication_gate.publishable`
  (`process_tracing/pt/export.py`, `PublicationGateV2`) and shows a causal conclusion only when both allow
  it. A field the adapter marks absent counts as not allowing it: the causal tab shows the prototype's
  hypotheses, tests and verdicts in their own panel and the conclusion line reads "withheld: Process
  Tracing's answer path carries no publication gate". No committed file carries a publishable
  Process Tracing gate: the investigation-spine fixture
  (`examples/fixtures/investigation_spine/process_tracing_return.json`) is a `pt_theory_test_return_v1`
  record whose gate is blocked, and the PsychosisBank `pt_export_v2` has no gate at all. So S4 commits two
  small made-up export files, each labelled as test data that supports only a claim about its shape: one
  with a publishable gate (status accepted, integrity verified, `publishable` true) and one with a blocked
  gate. The causal tab's "how the gate behaves" panel opens both: the publishable one shows its
  conclusion, the blocked one reads "withheld" and why. Unit tests cover these two and the absent gate.
- **Trace:** PT's own trace ids recorded in a connected-run receipt. The existing receipt
  (`investigation_run.py`) is fixed to the PsychosisBank run (its ids and paths are constants), so S4
  generalises it to take the study, the proposition and the export paths from the study definition, and
  the PsychosisBank receipt must still build byte-identical.
- **Cost (measured):** one full prototype run, drafts plus merge, on Process Tracing's large FOMC case
  cost $0.0555 over 7 calls (`process_tracing/docs/evaluations/efficiency_20261105/README.md:161-163`,
  trace `draft-audit/fomc_v4`, 277,101 of 352,770 input tokens cached); one proposition's case is smaller, so this is an upper figure. The handoff input and the
  adapter are code and make no model call. Replaced by S4's own run receipt total.

### S5 — Review, provenance and export

- **Build:** the study record becomes the general investigation record of the product map: the eight parts
  the map names (`EVIDENCE_TO_ACTION_PRODUCT_INTEGRATION_MAP.md:15-17`): the question, evidence, analytical
  plan, method runs, findings, unresolved questions, reviews and next actions of one study, read from the
  study definition. The analytical plan is the study's design (which strands run, the integration design,
  the evidence each strand needs), taken from the study definition and the method dashboard's route plan
  (`route_plan`), and a record without it is refused; `investigation_spine.py`'s PsychosisBank investigation is rebuilt as one instance of it
  and its public page must still pass `tests/test_psychosisbank_public_review.py`. A local server in the
  `method_dashboard_server.py` pattern writes review decisions and the reflexivity memo to typed JSON files
  in the study folder, committed. On the served page, where no server runs (open question Q20), each
  accept, reject, annotation or memo opens a pre-filled GitHub issue in this repository that Brian submits
  from his phone; `make import-reviews` turns labelled issues into the same typed files, and the page shows
  "recorded, waiting to be imported" until the next build. The bundle is a zip of committed files plus a
  manifest of hashes; the page itself recomputes each file's hash and shows any mismatch in orange. QDPX
  exchange is reused from QC's export, not rebuilt.
- **Trace:** each review action appended to one review log per day; the bundle's manifest lists every trace.
- **Cost:** none (no AI step).

### S6 — Second corpus and benchmark

- **Qualitative Coding runs first** (open question Q21): S1 reads QC's existing export, and that export
  exists only for Open Science. Either S6 picks a corpus QC has already analysed, or QC runs its
  grounded-theory pipeline on the second corpus in its own repository before S6 starts; the workbench never
  runs it. Cost (measured): every `qualitative_coding` call on the Open Science corpus from 2026-11-05 to
  06 totals $4.94 over 2,075 calls (llm_client's log), including partial reruns and four grounded-theory
  school variants, so one pass on a corpus of similar size costs at most about that.
- **Build:** the whole S1–S3 path on a second rights-clear corpus with its authors' coding, differing from
  the first in subject, research team and coding tool or export format (Q19); planted failures (a quote
  altered by one word, a passage from the wrong interview, a swapped label, a fabricated segment id, and
  the overclaim below) that
  the checks must catch. The second corpus is added by one study definition file plus its frozen data; a
  test, not the builder that reads the corpus, lists the files that commit changed (`git diff --name-only`)
  and the page shows "data only" or, in orange, any code path (the test of "not for a specific use case"). If the second corpus's export format needs a new reader, that
  reader is general (named by format, not by corpus) and the page says so.
- **Trace:** one receipt per run; the benchmark page links each.
- **Planted failures include an overclaim:** a meta-inference citing a number that is not in the measured
  result, which S3's number check must catch.
- **Cost (computed):** S2's plain version + S3 on a corpus of similar size from the same figures, about
  $0.10 per run; three repeat runs to show variation, about $0.28, plus the S2 language-model controls once
  (about $0.16), plus Qualitative Coding's own pass if Q21 needs one. Redone with `llm-cost estimate` on S2's own
  task once S2 has run.

### S7 — 1.0 release

- **Build:** method-profile page states supported and unsupported paths; release notes; version tag.
- **Cost:** none (no AI step).

## Relies on

`study_definition`, `study_corpus`, `qc_theory_export`, `qualitative_strand`, `source_segment`,
`evidence_anchor`, `author_coding`, `workbench_view`, `measurement_instrument`, `measured_result`,
`joint_display`, `meta_inference`, `verification_challenge`, `pt_export`, `publication_gate`,
`connected_run_receipt`, `investigation_record`, `review_decision`, `research_bundle`, `planted_failure`,
`benchmark`, `method_profile`, `public_review`, `capability_verdict`, `reflexivity_memo`, `split_manifest`,
`feasibility_readout`, `route_plan`, `proposition_measure_map`, `integration_check` (see
`docs/planning/DOMAIN.md`).

## Not in this plan

Running a qualitative method inside the workbench; a universal schema or method planner; OntoCanon, DIGIMON
or Theory Forge on the critical path; contacting any corpus author; publishing anything beyond the existing
PsychosisBank Worker without Brian's answer to open question Q11. Brian's NYC pause (2026-10-04) still
holds: NYC is not used as an example and its vertical is not extended. The 2026-08-13 integration
assessment's limits (`docs/PLANNING_STATUS.md:208-218`, written by an agent under Brian's approval of
that assessment) said work must not "rerun QC, Process Tracing, Theory Forge, or simulation analyses
merely to populate the Workbench" nor infer authorization beyond the Investigation Spine. Brian's
2026-11-06 direction to finish authorises this plan's slices; the rerun limit still holds in this sense:
S4 runs Process Tracing's answer path (adding only a handoff input and an export adapter, never `pt/` work during its freeze) and S6 may run Qualitative Coding in their own repositories to test a 1.0
condition (a causal path; a second corpus for the benchmark), never to fill the page, and the workbench
never runs either.

## Done when

S7 is merged: on two rights-clear corpora a person can open one investigation record per study, follow
every claim to its passage, see the quantitative strand's agreement with the authors' coding, read each meta-inference with its
review state, download the bundle, and read on the benchmark page what works, what fails and what it cost.

<!-- planning-compliance-checklist:v1 -->
## Compliance checklist

Written by `plan_checklist.py --write`, not by hand. `--check` re-runs the validator and fails
if any line below differs from what it says now. Unticked pending items are not passes.

Manifest: `docs/planning/planning-package.json`
Package revision: `9ad84d1a9355`
Verdict: not compliant

- [x] part investigation: ok
- [x] part checks: ok
- [x] part open_questions: ok
- [x] part system_model: ok
- [x] part domain_model: ok
- [x] part diagrams: ok
- [x] part plan: ok
- [x] part acceptance: ok
- [x] part review_page: ok
- [ ] part cold_review: failing
- [x] substance route follows from its path decision: ok
- [x] substance citations resolve: ok
- [x] substance domain model has a glossary: ok
- [x] substance project layer checks against the planning layer: ok
- [x] substance concepts point at their code: ok
- [x] substance plan names the concepts it relies on: ok
- [x] substance plan records the cost basis of each AI step: ok
- [ ] substance plan compares its AI answer path with the plain version: failing
- [ ] substance plan shows what each stage adds over the plain version: failing
- [x] substance plan records Brian's stops on this work: ok
- [x] substance type-level model of executable rules: ok
- [x] substance cold review read this revision: ok
- [x] initiative initiative names its home: ok
- [x] tiers spectrum rungs 1-11 are cited: ok
- [x] tiers production rungs 12-14 are cited when it runs in production: ok
- [x] tiers thesaurus separates near-identical names (rung 4): ok
- [x] coverage goal coverage: ok
- [x] goal_provenance goal provenance: ok
- [x] freshness package is current: ok
<!-- /planning-compliance-checklist -->
