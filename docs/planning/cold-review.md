# Cold reviews of this planning package

The latest review comes first. Each records the revision it read and its verdict; the package manifest's
`cold_review` field carries the latest.

## Plan #8, round 8 (read 9dd6009): revise

The reviewer found both round-7 blocking findings and notes a to d fixed, and reproduced the overlap
figures, the crosswalk counts, `make check`, the S4, S7 and Q12(c) costs and the stop search. It opened
Qualitative Coding's own code and its pinned Open Science state, and returned **revise** on one blocking
finding, with notes n1 to n11. What changed in answer:

| Finding | What it said | Fix |
| --- | --- | --- |
| B1 | QC's process-tracing handoff exports `state.claims` and never reads the grounded-theory export; QC builds `GT_PROPOSITION` claims only from a theoretical model the pinned state lacks (1,139 claims, none of that kind), so S4's causal route could not start as written | Option (a): the workbench writes a proposition case (the proposition, its supporting segment ids and texts, with the export's commit and sha256, provisionally `mmw_proposition_case_v1`) from the grounded-theory export S1 already pins, and Process Tracing's new input reads it; QC needs no change. Recorded as resolved agent question Q24 and investigation finding F20 (fails). Plan S4, S6, the finished table, `qc_pt_handoff`'s definition, Q21's precondition and the system model's S4 row now say so; `proposition_case` is a planned concept and `qc_pt_handoff` leaves "Relies on" |
| n1 | `qc_theory_export` read as planned though QC's export exists | Its definition now says the export exists in QC and only the workbench's reader is planned |
| n2 | S7's readiness record was in neither the domain graph nor "Relies on" | Added as planned concept `readiness_record` |
| n3 | S5 did not name the disposition of orange rows or G5's roles | S5's build now records a disposition for every orange row and the reviewer's role in every review entry |
| n4 | S6's cost entry left out the causal check | Its evidence now adds S4's measured upper figure, $0.0555 per run |
| n5 | The causal tab's plain-version comparison was not cited | S4 cites Process Tracing's own comparison (ADR 0004 :61-66: 7 and 7 against a plain-draft mean of 6.17, under its noise line); the workbench adds no stage |
| n6 | The Phase 3 lift was inferred from the crosswalk approval | The stop entry says so, and that Phase 3 is complete |
| n7 | The disproof tested no integration observation | The disproof now also fails if a joined claim cannot be followed to both its passage and its number, or Brian rejects most meta-inferences in review |
| n8 to n11 | Carried notes and the plugin's WAIT labelling | Unchanged, as answered in rounds 5 to 7 |

The reviewer's own report for round 8 is reproduced at the end of this file, ending with its verdict line.

## Plan #8, round 7 (read 58f644a): revise

The reviewer found round 6's B1 fixed (the two made-up test exports match Process Tracing's
`PublicationGateV2`, and A6 can be judged) and N1 to N3, N5 and N6 fixed. It reproduced the overlap
figures, the crosswalk counts, `make check` and the S2 and S4 costs. It returned **revise** with two
blocking findings and notes a to g. What changed in answer:

| Finding | What it said | Fix |
| --- | --- | --- |
| 1 | A12's end-to-end run includes a causal check that no slice builds on the second corpus; S7 claimed no AI step; "met" did not require Brian's judgement | S6 gains the causal check: S4's route on one second-corpus proposition (QC's handoff must carry it as a `GT_PROPOSITION` claim, added to Q21), costed at the measured upper $0.0555. S7's run is a fresh end-to-end run with a computed cost (about $0.15, new `cost_basis` entry). A row reads "met" only when its criterion is "judged pass" in Brian's recorded words; an agent-built, unjudged criterion reads "not yet: awaiting your judgement". A12's steps, expected result and failure example say so |
| 2 | The integration condition was labelled "kept" though 1.0 rows can only say "complements" or "silent", so the roadmap's G4 "contradiction disposition" never meets a real disagreement; the readiness page read only the eight bullets, not the G1–G6 gate | The finished table's row now reads "changed: ... verdicts limited to 'complements' or 'silent' in 1.0", with why. Q12 gains part (c) with a recommendation (complements only in 1.0: no second author code qualifies, so a second measured theme would have no human reference), a default, the cost of the other option (about $0.19 per S2 pass, worked out) and answer words "complements is enough" / "need agree or disagree"; Q22 points there. The plan states that S7's readiness page carries both the eight bullets and G1–G6's 1.0 conditions |
| a | Two Process Tracing stops were not lifted by ADR 0004; the freeze had approved words; the Phase 3 pause was not listed | "overbuilt" and "a patch ot an actual fix" now `holds`, honoured because S4 runs no pipeline. The freeze entry quotes Decision 1 as put to Brian and approved on 2026-11-05. The Phase 3 pause is listed, lifted 2026-10-07 |
| b | `qc_pt_handoff` is implemented in QC, not planned; missing from the plan's "Relies on"; the `GT_PROPOSITION` citation pointed at a use | Kind `elsewhere` in the graph, glossary and spectrum; added to "Relies on"; cited at `qc_clean/schemas/domain.py:179` |
| c | SYSTEM_MODEL had no S7 row or S7 pages | S7 row added (readiness record, end-to-end receipt, "runs / does not run" field) and the planned pages list the readiness, method-profile and crosswalk pages |
| d | The test exports' schema and reader were unnamed | The plan says they use the partial schema (`pt_draft_audit_export_v1` with the optional gate block in `PublicationGateV2`'s shape), read by the reader the real case uses |
| e, f, g | Coverage classes R3 as process; agent questions settleable now; page links 404 before merge | Unchanged, as answered in rounds 5 and 6: R3 stays mapped to A11; the questions are upkeep outside this plan's slices; the links resolve when this pull request merges |

The reviewer's own report for round 7 is reproduced near the end of this file, before round 8's.

## Plan #8, round 6 (read 9ad84d1): revise

The reviewer found round 5's S4 route fixed (the draft-audit prototype with a handoff input and Process
Tracing's Q20 adapter, F13 now "fails", the measured $0.0555 cost, the freeze in `stops`) and notes n1 to
n4 fixed. It reproduced the overlap figures, the crosswalk counts, `make check` and every computed cost. It
returned **revise** on one remaining part of B1, with notes N1 to N6. What changed in answer:

| Finding | What it said | Fix |
| --- | --- | --- |
| B1 (rest) | The fixture cited for A6's publishable case is a `pt_theory_test_return_v1` record with a blocked gate and no `publishable` field; no committed file shows a conclusion, so half of A6 could not be judged | Claim corrected in the plan's S4 build, A6 and Q23. S4 now commits two made-up test exports, labelled as test data (one publishable, one blocked), shown in a "how the gate behaves" panel; A6 gains a step that opens it and a second failure example ("the publishable test export still reads 'withheld'") |
| N1 | Plan lines 45 and 75 and the `pt_export` glossary entry described the old route; the adapter's schema was unnamed | Reworded; the plan says no 1.0 causal conclusion from the answer path shows as published; the adapter's schema is named (provisionally `pt_draft_audit_export_v1`) with a second, partial reader whose gate and conclusion fields are optional |
| N2 | `stops` missed Process Tracing's earlier stop signals; the freeze's words were an agent's paraphrase | Added "overbuilt" (2026-07-29), "archive ... start over" (2026-08-20) and "a patch ot an actual fix" (2026-09-24), each `lifted` with its reason; the freeze entry now says its words are a paraphrase |
| N3 | F18 held only for the frozen pipeline's export | Narrowed, and pointed to Q23 |
| N4 | The coverage record called "part of my broader vision" a process requirement | Re-judged with `--force`: the judge still classes it as process but now maps it to A11. The re-judge also found "finish" only partly covered (no criterion checked the whole bar), so acceptance A12 was added to S7: a 1.0 readiness page, one row per condition of the roadmap's 1.0 definition with its source, slice, status and evidence link, plus one end-to-end run on the second corpus; verdict covered |
| N5 | QC's Process Tracing handoff was missing from the domain model | Added as `qc_pt_handoff` (glossary, graph, spectrum, `relies_on`); S4 first checks the proposition is an anchored `GT_PROPOSITION` claim |
| N6, n5, n6 | Stale reviewed revision; agent questions settleable now; page links 404 before merge | N6 is replaced by this round's record. n5 and n6 stand as answered in round 5 |

## Plan #8, round 5 (read c79e70b): revise

The reviewer found round 4's F1, F2 and V fixed, and notes n1 to n7, n9 and n10 fixed. It reproduced the
overlap figures, the fitted prices and the crosswalk counts. It returned **revise** with one blocking
finding (B1) and notes n1 to n6. What changed in answer:

| Finding | What it said | Fix |
| --- | --- | --- |
| B1 | S4 named a Process Tracing route (draft-audit → `pt_export_v2`) that, by Process Tracing's own ADR 0004 and its Q20, writes no such export; F13 held only by citing the frozen pipeline; the cost left out the merge step; A6 needed a gate field the route never writes; `stops.searched` did not look at Process Tracing | New question Q23 (agent, resolved by argument): S4 adds, in `process_tracing`, a qualitative-handoff input to the draft-audit prototype and the partial export adapter Process Tracing's Q20 recommends; no `pt/` work and the frozen pipeline is not run. The workbench treats an absent gate as withheld, and tests the publishable branch with the committed fixture that carries a gate. S4's cost is now the measured full prototype run, $0.0555 over 7 calls (fomc_v4). F13's verdict is now "fails" with Q23; SYSTEM_MODEL's S4 row and A6's expected result say the same; `stops.searched` and `stops.found` add the `pt/` freeze (2026-09-30) and ADR 0004 |
| n1 | Stale "convergence / complementarity / divergence" wording; A5 said "read whether they agree"; the goal said "a qualitative category" | The slice table, DOMAIN.md, the `joint_display` node and the questions map say "complements" or "silent: not measured" in 1.0; A5 reads "see which ones the measure speaks to and how"; the review page's goal says S2 measures one of the authors' own codes |
| n2 | LiteLLM does list a price for gpt-5.6-luna | Each cost entry now cites LiteLLM's list price ($0.20 input, $1.20 output per million tokens) beside the fit, which is higher, so the figures are conservative |
| n3 | Two pairs of QC categories cite exactly the same turns: 8 categories rest on 6 distinct evidence sets | Confirmed from S1's data; new finding F19, and plan S2 has the study page say so. "Open data"'s two categories are distinct, so the construct choice is unaffected |
| n4 | Who drafts the instrument's definition was unnamed | One llm_client call (`mixed_methods_workbench.open_science.define`), traced, read and edited by the building agent, versioned in the split manifest; costed at about $0.004 in plan S2 and the manifest |
| n5 | Agent-owned Q2, Q3, Q4, Q10 and Q21 could be settled now | Kept open, not settled in this round: Q2–Q4 and Q10 are upkeep fixes outside this plan's slices (a missing `.agentic/repo.yaml`, the wiki cap, the architecture pointer, a label on the paused NYC lane), each with its fix written in the question; Q21 waits on S6's corpus choice (Q19) |
| n6 | The page's GitHub links 404 until the branch is merged | Unchanged by design; they resolve once this pull request merges |

The reviewer's own report for round 5 is reproduced at the end of this file, ending with its verdict line.

## Plan #8, round 4 (read bdf06d7): revise

The reviewer found B1 and B3 fixed, B2 and B4 fixed only in part, and returned **revise** with three
blocking findings (F1, F2, V) and notes n1 to n10. What changed in answer:

| Finding | What it said | Fix |
| --- | --- | --- |
| F1 | The S2 "plain" version was 25 per-interview calls, not the same model given the whole source in one or two calls; per-turn S2 calls and per-proposition S3 drafts were built first | Plan S2 and S3 and the manifest: the plain version is the starting design. S2 labels every interviewee turn of one split in one call (two calls: tuning, held-out; about 58,000 input and 19,000 output tokens each, inside gpt-5.6-luna's 922,000 input and 128,000 output limits from LiteLLM's model information), about $0.08 per pass. Per-interview and per-turn calls, and S3's per-proposition drafts, are stages added only if the plain version shows a gap; `cheapest_design` no longer calls per-turn the cheapest |
| F2 | A prevalence cannot confirm or contradict QC's conditional propositions, yet a row could say "converges" or "diverges"; the co-occurrence branch had nothing to compare | Q22, plan S3 and A5: a row matched by prevalence alone may only say "complements", and the number and passage check refuses any other verdict; the co-occurrence branch is dropped; A5's failure example is a prevalence-only row marked "converges" |
| V | The validator's record showed the plain-version and stage-effects checks failing | Those two lines show `WAIT`, not a failure: the package contract makes `plain_baseline.kind: planned` and each `stage_effects` entry with status `untested` show `WAIT` until the comparison runs, "even after the field is due, never a pass". They stay `WAIT` until S2 and S3 run their plain versions; the validator still exits 0 with them pending |
| n1 | Edge e38 (a second model challenges each meta-inference) remained; the number and passage check and the proposition-to-measure map were not concepts | e38 dropped; `proposition_measure_map` and `integration_check` added to the domain graph, DOMAIN.md, the spectrum file and `relies_on`; the planted overclaim added to `planted_failure` |
| n2 | QC marks only its cited turns, so a two-way overlap floor of 0.3 might be unreachable; compute the table now | Computed from S1's data over 8 categories × 28 codes: the highest two-way overlap is 0.18, so the floor could never be met. The construct is redesigned (Q15, plan S2): S2 measures one of the author's codes, so the measure and its reference name the same construct, chosen as the code holding at least half of a QC category's cited turns with a chance test below 0.001. Only "open data" qualifies (14 of 22 and 14 of 21 cited turns of two categories; chance 3e-9 and 1e-9); it marks 72 turns in 23 of 25 interviews |
| n3 | S2's table left out brief :110 and :118-121 | Two rows added: error costs and Brian as accountable reviewer; a count over the complete corpus has measurement error only, so its interval is the instrument's held-out error resampled by interview, while agreement keeps its by-interview interval |
| n4 | PLANNING_STATUS.md:208-218 forbids rerunning QC or PT "merely to populate the Workbench" | Plan "Not in this plan" and `stops.searched`: the limit was written by an agent under Brian's approval of the 2026-08-13 assessment; its rerun limit still holds as written (S4 and S6 run producers in their own repositories to test a 1.0 condition, never to fill the page); its limit on authorising implementation is superseded by Brian's 2026-11-06 direction |
| n5 | Router records A5, A7 and A11 predated later changes | A4, A5, A7 and A11 use cases updated and rerun through the Representation Router; each still recommends the view its entry names |
| n6 | Stale citations (Q19 to S4; investigation.json said S3 is measured) | Every plan citation in the package remapped to the edited plan; Q19 cites S6; the investigation note says S3 is computed |
| n7 | The GitHub-issue review route and `make import-reviews` missing from the system model and context diagram | Added to SYSTEM_MODEL.md's S5 row and as a `github_issues` source in the context graph |
| n8 | The page does not show the cost table, plain-version record, stage effects or stops | Not fixed here: the shared review-page builder does not render those fields; the plan text and the checklist carry them |
| n9 | A4 and A10 wording was technical | Reworded in plain terms |
| n10 | The fresh reviewer is a model step mentioned only in prose | It is a Claude Code session on the subscription, named in the S2 controls step's evidence and in `cheapest_design` |

The reviewer's own report for round 4 is reproduced at the end of this file, ending with its verdict line.

## Plan #8, round 3 (read 3957779): revise

The reviewer confirmed all five round-2 findings fixed and returned **revise** with four new blocking
findings (B1 to B4) and notes N1 to N11. What changed in answer:

| Finding | What it said | Fix |
| --- | --- | --- |
| B1 | S2's construct match was a one-way share against a different codebook, with no minimum, so broad numbered interview-question codes could win | Plan S2 and Q15: the match is two-way (turns both mark ÷ turns either marks, over the 630 interviewee turns); the author's 11 numbered interview-question codes are left out by their label format and listed; a minimum overlap (0.3 unless the readout gives a reason) is preregistered from the feasibility readout, else the next category, else S2 stops; the brief's :111 row and A4 name the different codebook |
| B2 | No question said which proposition the single measure speaks to; mismatched units must block aggregation | New Q22 (resolved by a written rule): each proposition maps to the measure (prevalence or co-occurrence by interview) or to "silent: not measured"; differing units block aggregation (brief :143-144); A5 states how many rows are comparable |
| B3 | The product map names eight parts; the analytical plan was dropped | The analytical plan added to A11 ("eight parts"), `investigation_record` (glossary and graph, with an edge to `route_plan`), plan S5, the vision paragraph, the S5 slice row and Q18 |
| B4 | No `plain_baseline`, `stage_effects` or `stops`; S3's challenger had no shown effect | Manifest adds all three (plain baseline planned for S2 and S3; two untested stages; stops: the NYC pause holds). S3's second-model challenger is dropped: a deterministic check verifies every cited number and passage id, S6 plants an overclaimed meta-inference for it to catch, and S3 is 6 calls (computed, $0.014) plus one plain-version call |

Notes: N1, the plan checklist moved to the end of the plan, so every citation into the plan is back at
the line it was set against and later checklist rewrites cannot shift them; N2, the four language-model
controls are a computed step ($1.58 once per corpus) and the fresh reviewer is a Claude Code session; N3,
S3 relabelled computed with fitted gpt-6-luna prices, the $0.0038 measured median kept as the upper
figure; N4, brief rows :25 (overridden by "not for a specific use case"), :83-85, :102-103, :113 and :114
added to S2's table; N5, Q16 records the task/owner pattern as an agent working default; N6, coverage
rerun after B3; N7, the instrument is applied to every interviewee turn; N8, links resolve once merged; N9,
the test command reads `PYTHONPATH=src:.`; N10, A4 prints the chance level beside the shuffled-label row;
N11, `split_manifest` and `feasibility_readout` are planned domain concepts and in relies_on.

## Plan #8, round 2 (read 47475ef): revise

The reviewer returned **revise** with five blocking findings and notes a to q. What changed in answer:

| Finding | What it said | Fix |
| --- | --- | --- |
| 1 | S2 did not keep every condition of the quantitative-strand brief, and Q16 called the unapproved brief "reviewed" | Plan S2 now has a table of every brief condition with its line and how S2 meets it; two are named as not met with reasons (no fine-tuned encoder; no independent adjudicated pilot); the language model's behavioural and compliance controls and the held-out trace check are added; Q16 rewritten (brief never approved, adopted condition by condition); the construct is Brian's call again (Q15, with a default) |
| 2 | Q18 showed only half the product map; R3 uncovered | Q18 gives both readings (map sections 1 and 3 against 5, 7 and 9) with a third answer, "policy flagship"; the plan says Open Science is the method proof, not the flagship; A11 and the outcome tie the record to the evidence-to-action vision; coverage rerun: verdict covered, R3 judged a statement about the planning process |
| 3 | A7 needed a server that Q11's static hosting does not give; reflexivity memo had no criterion | New Q20 (resolved): served-page actions open pre-filled GitHub issues and `make import-reviews` imports them; A7 adds the memo, the import state and the page's own hash check (mismatch in orange) |
| 4 | S6 needs Qualitative Coding to run on corpus 2; no question or cost | New Q21 (open, agent); S6 schedules it; measured cost $4.94 over 2,075 calls added to the cost basis; the thesis says QC runs in its own repository |
| 5 | Q14 answered by the S1 receipt but still open | Q14 resolved with the receipt's counts; plan S1 says the author's passages are located by their words (12 of 837 stated offsets match) and lists the 36 that differ and 7 not found |

Notes: a, theory operationalization added to Q12; b, the overlap match defined (Q15, plan S2); c,
`capability_verdict` and `reflexivity_memo` in relies_on; d, `reflexivity_memo` is a planned domain
concept; e, `workbench_view` says it reads the synthetic DEMO-C1 shape; f, `pt_export` cites
`investigation_run.py:101`; g, S4 generalises the PsychosisBank receipt and keeps it byte-identical; h,
`scripts/type_inventory.py` now keys classes by module and resolves imports; i, per-interview cost stated
as about $0.28 against $0.79, S3 measured per call ($0.05), S2 feasibility tokens counted from QC's segments;
j, counts 204 and the cost note reworded; k, round-1 notes listed below; l, the review page has no served
URL until Q11 is answered, and its GitHub links resolve once this branch merges; m, the duplicate
`adr-2026` ids come from the shared builder (date-named decision files), filed as
BrianMills2718/company-planning#264; n, disproof reads "agrees no better than", and the thesis now claims
the measure's agreement, which A4 tests; o, A7 hash check on the page, A9 links the slice and test, A10's
"data only" computed by a test from `git diff`; p, context diagram: Cybernetic Influence added and the
case slices connected; q, F10 says 90 cited passages.

Round-1 notes not listed before: N5, planned concepts have their own "Planned (Plan #8)" kind and "passage"
is in the spectrum's ambiguous list; N12, the standing publish rule does not settle Q11 because serving
from hive.brianmills.dev needs a change to another repository and Brian's direction limits deploys to the
existing Worker, so Q11 stays his; N13, see note l.

## Plan #8, round 1 (read a295230): revise

The reviewer (`company-planning:planning-compliance-reviewer`, run cold with `claude -p`) returned
**revise** with ten blocking findings and thirteen notes. What changed in a95a519 in answer:

| Finding | What it said | Fix |
| --- | --- | --- |
| B1 | S2 dropped the repository's quantitative-strand brief (word-list count baseline, dummy and TF-IDF baselines, language model as challenger, feasibility readout, prevalence error) | S2 rewritten to keep every condition; Q16 resolved by argument |
| B2 | "Disagreements" undefined; re-judging only misses inflates agreement | No second model in S2; if added later, the cases are chosen without the author's codes (Q16) |
| B3 | Unit of analysis and the 650 count unsourced; author passages vary and overlap | Unit = interviewee turn, 630 counted; author passages mapped by overlap (Q17) |
| B4 | "Part of my broader vision" had no criterion | Read from the evidence-to-action map: one investigation record per study (Q18, Brian's call with that default); acceptance A11; S5 builds it |
| B5 | Domain definitions did not match code; relies_on missed concepts | evidence_anchor, producer_export, publication_gate redefined; ten concepts added; planned concepts have their own kind |
| B6 | System model listed no types | Generated type inventory (195 classes, stale-check test); planned types per slice; context diagram shows the inside |
| B7 | A3, A7, A10 needed a command line or a git commit | Each opens an address (Q11 decides where); the benchmark page states the files each corpus changed |
| B8 | The package carried an older review's pass | This record; manifest verdict set to revise until the next round passes |
| B9 | No cheapest-design comparison | Per-interview calls measured against per-turn calls on tuning interviews; quality decides |
| B10 | Second corpus had no difference rule | Must differ in subject, team and coding tool or export format (Q19) |

Notes: costs relabelled computed or guess (N6); A2 scheduled in S7 (N7); A4 shows tuned and tested
interviews and a shuffled-label control (N8); goal fields rewritten as direction, claim and disproof (N9);
the "five changes" count corrected and reflexivity kept in S5 (N10); Q7 count 203 (N11); citations fixed
(N1, N3, N4); the generator gap behind the hand-added wiki line filed as BrianMills2718/project-meta#2716 (N2).

## Earlier: Plan #7 package, round 2 (read 794be795): pass

The package now passes. Both blocking findings from round 1 are fixed, and nothing new would change a reader's conclusion. A few small notes remain.

**Validator:** exit 1. 9 of 10 parts pass. The only failure is the cold review, marked missing, which this review supplies. 7 of 8 substance checks pass, none fail, and 1 is pending (no route declared, which only a new or `full_method` repository needs). All 4 spectrum-tier checks pass. Goal coverage shows WAIT because `asked_by` is empty. Freshness passes: the package was built from 2c3c13f and 2 commits of work have landed since.

**Check rerun:** I reran the crosswalk check (`scripts/crosswalk_phase4.py --check`) read-only. It gave 171 steps, 36 groups and 0 errors, exit 0, which matches the new line in `checks.txt`. The tree stayed clean.

## Previous findings

- **B1 (plan relied on the wrong concept): fixed.** The new `public_review` concept points at `investigation_spine.py:278`, which is the `InvestigationSpine` class. Its definition cites `build_psychosisbank_public_review.py:16`, and `build()` at that line writes the deploy page and payload. The plan's `relies_on` list has `public_review` instead of `review_packet`, and so do Q5 and Q6. Both graphs and the page show it.
- **B2 (nothing kept the public page in step with the renderer): fixed.** New question Q9 is resolved by an argument, with no test proposed, which suits the question. Plan step 2 adds a test that fails when the committed `deploy/` page differs from what `build()` produces. Step 3 records a rule: every merge that touches `deploy/` is followed by a deploy and a comparison of the served page's hash. "Done when" now includes "`pytest` fails on a stale `deploy/` page".
- **N1 (NYC findings labelled "Human-approved"): fixed.** It is now open question Q10 and plan step 4. Both cited lines in `investigation_spine.html` do say "Human-approved" and "human approved".
- **N2 (Q3 hand-edited a generated file): fixed.** Q3 now reruns the generator, and `wiki/index.md:24` is the "Generated by…" line.
- **N3, N4 (A1 pointed at the wrong section; table versus cards): fixed.** A1 now names the "Independent challenge" section, and a note records why the existing cards stand in for the table the router chose.
- **N5 (acceptance gaps): partly fixed, by choice.** The outcome line no longer overclaims: it says the crosswalk view is planned but not scheduled. A2 now names a location. `asked_by` is still empty, with the reason recorded; this is acceptable because the package does not set `full_method`.
- **N6 (system model lists no types): not fixed, by choice.** This stays a note for a package that does not set `full_method`.
- **N7 (`producer_export` read as the real export): fixed.** Its definition now says "synthetic mirror".
- **N8 (checks ran on an older revision): fixed.** The checks were rerun on d1e013d, and the crosswalk check was added.
- **N9 (north star and disproof): fixed.** The north star now reads as a direction you could not pass or fail. The disproof is now a single observation that would trigger it: a real study that cannot be answered without re-running method logic inside the workbench.
- **N10 (issue #27 and page URL): partly fixed.** Issue #27 is recorded as closed. The review page still has no `url` in the manifest.
- **N11 (Q2, Q4, Q6 already settled by argument): not fixed, by choice.** They stay open as plan steps. This is a note only.

## Remaining notes

- **Open questions**, `open-questions.json` Q3 cites `wiki/index.md:21`, but that line is blank. The "no declared roadmap" text is on line 22. Fix: cite line 22.
- **Open questions**, Q10 `touches` lists `quantitative_audit`, but the "Human-approved" labels are on the NYC *qualitative* findings. Fix: remove that entry or point it at the qualitative concept.
- **Open questions**, Q10 is marked open even though its `resolves_with` already settles it by argument. This is the same pattern as N11.
- **Manifest**, `planning-package.json`: `subject_revision` is still 2c3c13f, older than the revision reviewed here. The validator's freshness check accepts it. Fix: update it when the package is rebuilt.
- **Review page**: still no `url` recorded (N10). Record the served URL after merge.
- **System model**: N6 still stands.

## Judgments I was unsure about

- I accepted the claim that `worker.js:4` "routes only PsychosisBank". Strictly, the Worker rewrites only the PsychosisBank API path and passes every other request to the static files. The NYC payload is not among those files, because `build()` writes only the PsychosisBank payload. So the claim holds in effect, but it is not literally what line 4 says.
- I did not render the page in a browser this round. I checked the page source for each new item instead: `public_review`, Q9, Q10, `tmp_path`, "blanket-approved", "hash comparison", "Independent challenge", "synthetic mirror" and the new north star are all present.

Reviewed revision: 794be795fc69eb2a813300280539180266920d0a

Verdict: pass

## Plan #8, round 4 reviewer's report (verbatim)

I've finished the round 4 review, and the verdict is **revise**. Of round 3's four blocking findings, two are fixed. The other two were answered in a way that is only partly right, so they stay blocking. One more thing blocks too: the validator's own record shows two checks failing on the plan's plain-version comparison.

Two limits on this review. First, this session could not read the plugin's contract or validator, or run any Python, so I could not rerun the validator or any recorded check. I reproduced counts by hand instead (below). Second, I did not render the page in a browser.

### Validator

I could not run it. Its last recorded result is the checklist it writes into the plan (`008_finish_workbench.md:308-348`, revision `bdf06d7310b1`): "not compliant", exit status not shown.

- **Parts:** 9 of 10 ok; the cold review part fails, and this report supplies it.
- **Substance:** 9 of 13 ok. Two of the four failures are the cold review's and clear with this report. The other two will not clear on their own: "plan compares its AI answer path with the plain version" and "plan shows what each stage adds over the plain version".
- **Other lines:** the 3 tier checks, initiative, goal coverage, goal provenance and freshness are all ok.

### Checks

No recorded command could be rerun here. What I reproduced by hand:

- `grep "^class "` over `src` and `scripts` finds 195 classes, matching `TYPES.md:7`.
- The S1 receipt (`s1-open-science-study`, `examples/studies/open_science/build_receipt.json`) matches Q14, Q17 and F10: 28 of 28 md5 matches, 1,277 of 1,277 segments, 90 of 90 cited passages, and the author's passages located as 681 exact, 113 whitespace-only, 36 text differs, 7 not found, with 12 stated offsets correct.
- QC's export says 630 interviewee units, 8 categories and 6 propositions.
- The author's CSV has exactly 11 numbered interview-question codes.

### Round 3 findings

- **B1** (two-way construct match): **fixed**. Plan :136-148, Q15, the brief's :111 row and A4 all carry it.
- **B2** (which proposition the measure speaks to): **fix wrong in part**, stays blocking (F2 below).
- **B3** (analytical plan in the record): **fixed** in A11, the graph (e150), S5, the vision paragraph and Q18. Router record A11 is stale (note n5).
- **B4** (plain version, stage effects, stops; S3 challenger dropped): **fix wrong in part**, stays blocking (F1 below). The challenger is gone from the plan, but the domain graph still shows it (note n1).
- **N1–N7, N9–N11:** fixed. **N8** (GitHub links resolve once merged) is not fixed, by choice: the plan is still not on `origin/main` and the branch is not on GitHub (note n8).

### Blocking findings

- **F1. Plan / plain version.** `planning-package.json:330-350`, plan `:184-191` and `:211-214`.
  - The S2 "plain" comparison is 25 calls, one per interview. Brian's rule says the plain version is the same model given the whole source in one or two calls.
  - The whole corpus is 108,452 tokens (plan :187), so it fits in one window; nothing in the package rules that version out.
  - The design also builds the staged versions first: one call per turn in S2, one per proposition in S3. Both stages are marked "untested", and the validator fails both checks.
  - **Fix:** make the plain version the starting design in S2 and S3. For S2 that is one or two calls over the whole corpus; split the calls tuning/held-out, and state the model's output limit, since 630 labels × 268 ≈ 169k output tokens. If that limit really forces more calls, record the proof from construction and per-interview calls become the plain version. List per-turn and per-proposition calls as stages added only after the plain version shows a gap. Reword `cheapest_design`: per-turn is not the cheapest (about $0.31 even with a cached prefix, against about $0.28 per interview). Then rerun the validator.
- **F2. Open questions / S3 join (Q22).** `open-questions.json:415`, plan `:195-203`.
  - All six of QC's propositions are conditionals that each name 2–3 categories (export `grounded_theory.json:3218-3345`). The prevalence of one category cannot confirm or contradict "when X, then Y".
  - Yet the rule lets such a row carry "converges" or "diverges", and the number-and-passage check would not catch that.
  - The "co-occurrence with another category" branch has nothing to compare against: S2 labels one category, and QC's segments carry no category codes.
  - **Fix:**
    - A row matched by prevalence alone may only say "complements", and the check refuses any other verdict.
    - Either have S2 measure both categories of one chosen proposition (cost computed), or drop the co-occurrence branch.
    - Add "a prevalence-only row marked converges" to A5's failure example.
- **V. Validator.** `008_finish_workbench.md:335-336`: the two plain-version and stage-effects checks fail. A failing validator is a revise finding. F1's fix should clear it; if the validator rejects every not-yet-run comparison by design, record that reason in the package.

### Notes (do not block)

- **n1.** Domain model `domain.graph.json:489-494`: edge e38 still says a second model challenges each meta-inference. The S3 number-and-passage check and the proposition-to-measure mapping (planned types in `SYSTEM_MODEL.md:50`) are not concepts and not in `relies_on`. `DOMAIN.md:47` leaves out the planted overclaim. **Fix:** drop e38, add the check as a planned concept.
- **n2.** Q15 / S2 (plan :139-146):
  - QC's side of the overlap is only its cited examples: 8 incidents, 88 turns, about 22 per category. Its two-incident categories mark at most about 22 turns, while the author's broad codes are large ("open data" 81 passages, "open/closed access publishing" 57).
  - So a two-way overlap is capped at roughly 22 divided by the author code's turns, and a real match to a broad code can fall below 0.3.
  - The S1 data can produce the 8 × 28 overlap table now, settling whether the 0.3 floor is reachable before S2 is built around it.
- **n3.** S2's table of brief conditions leaves out brief `:110` (error costs, accountable reviewer) and `:118-121`. The second says the count over a complete corpus has measurement error but no sampling error. It does not fit cleanly with the plan's by-interview interval on prevalence.
- **n4.** Stops: `PLANNING_STATUS.md:208-218` (2026-08-13) says work "must not rerun QC, Process Tracing ... merely to populate the Workbench". S4 and S6/Q21 do that. `stops.searched` read the file but did not record whether Brian's 2026-11-06 direction lifts this. I'm unsure it still applies; its section is headed "Completed Phase".
- **n5.** Acceptance router inputs predate later changes: `router/A11.usecase.json:18-27` has no analytical plan, A7 has no memo, A5 has no comparable count. Each still chose the view named in its entry. Rerun them.
- **n6.** Stale citations: Q19 evidence cites plan ":232", which is now S4 (should be :265-266). `investigation.json:319` still says S3 is measured; it is now computed.
- **n7.** The context diagram and `SYSTEM_MODEL.md:52` leave out the GitHub-issue review route and `make import-reviews` (Q20).
- **n8.** Page:
  - The diagrams are drawn on the page and every part is shown.
  - The page does not show the manifest's cost table, plain-version record, stage effects or stops; only the plan text and the checklist carry them.
  - The page is not served anywhere (Q11), and its Plan #8 GitHub links 404 until the branch is pushed and merged. The repository is personal, so the company-organization rule does not apply.
- **n9.** Acceptance wording: A4's expected result (`:69`) uses "per-class agreement", "prevalence error" and "shows its null", and A10's (`:176`) names `git diff --name-only`. The orange failure flags are judgeable by a non-expert; the wording could be plainer.
- **n10.** Cost basis `:256`: the fresh reviewer (a Claude Code session) is a model step mentioned only in prose. Q21 is nearly settled by the plan's own S6 text (`:259-261`). S4's measured $0.03 and QC's $4.94 could not be checked against llm_client's log here.

### Judgments I was unsure about

- Whether F1 and F2 are blocking rather than notes. The cost at stake is cents; the joint display's validity and Brian's plain-version rule are what tipped them.
- Why the validator fails the two checks; I couldn't read it.
- Whether n4's 2026-08-13 constraint still holds.
- The output limit of gpt-5.6-luna, which decides whether two calls suffice for F1.

---

- **Verification:** every count above came from `grep`, `git show` and file reads at a251ee2; the validator, `pytest` and the crosswalk check were denied by this session's permissions.
- **Feedback:** the cold reviewer ran without permission to read the plugin or run Python, so required steps 1–2 could not be done. Grant read and run access to the plugin path and `.venv/bin/python` for review sessions.
- **Need anything from human:** No.

Reviewed revision: bdf06d7310b1df76dd35c1334a02eec53ccd160a

Verdict: revise

## Plan #8, round 5 reviewer's report (verbatim)

I've finished the round-5 review. The verdict is **revise**, because of one new blocking finding.

All three of round 4's blocking findings (F1, F2, V) are fixed, and so are nine of its ten notes. The new problem is in slice S4. The plan says it will take Process Tracing's results from a route that, according to Process Tracing's own records, does not produce the file the workbench reads.

#### Validator

I ran it at revision `2092693` and it exited 1.

- **Parts:** 9 of 10 are ok. The only failure is the cold review, whose recorded verdict is still `revise`.
- **Substance checks:** 10 of 12 are ok, none fail, and 2 show WAIT. The two WAIT lines are the plain-version comparison (still planned) and the three untested extra stages. The contract makes those WAIT by design.
- **Other lines:** initiative and spectrum tiers are 4 of 4. Goal coverage (3 requirements), goal provenance and freshness all pass. Freshness counts 1 commit of work since the package revision.
- **Odd output:** the validator's JSON output labels those two WAIT lines as "failing". The plan's generated checklist copies that word at lines 369-370, and `plan_checklist.py --check` says it matches, exit 0. This is a fault in the plugin, not the package.

#### Recorded checks rerun

- **Crosswalk check:** `scripts/crosswalk_phase4.py --check` gave 171 steps, 36 groups, 0 errors, exit 0. That matches the manifest, and the tree stayed clean.
- **Overlap scripts:** `overlap.py` and `overlap2.py` on the S1 branch (`faf5399`) reproduce every figure the package quotes:
  - 630 interviewee turns, 224 code-and-category pairs, and 11 numbered interview-question codes left out.
  - "Open data" marks 14 of 22 turns (0.64, chance 3.0e-9) and 14 of 21 turns (0.67, chance 1.2e-9).
  - The next-best share is 0.48, and the highest two-way overlap is 0.18.
  - "Open data" marks 72 turns in 23 of the 25 interviews (I counted this separately).
- **Prices and token counts:** refitting the call log gives exactly what the package uses:
  - 708 calls priced at $0.2168 input and $1.4057 output per million tokens, with medians of 4,052 input and 268 output tokens.
  - $0.1354 and $0.2895 per million for gpt-6-luna, with medians of 15,196 and 807 across 55 calls.
  - The S2 figure recomputes to $0.0783.
- **Measured costs:** the five S4 stage averages sum to $0.030. Qualitative Coding's calls over 5-6 November now total 2,088 calls and $5.01, against the recorded 2,075 and $4.94; the gap is later calls, under 2%.
- **Not rerun:** this session was not allowed to run the full test suite.

#### Round 4 findings

- **F1 (plain version first): fixed.**
  - S2 now labels every turn in two calls (tuning interviews, then held-out interviews), at plan lines 186-198.
  - S3 drafts every row in one call, at lines 235-239.
  - Per-interview calls, per-turn calls and per-proposition drafts are now stages added only if the plain version shows a gap.
  - The 922,000-token input and 128,000-token output limits are confirmed in LiteLLM's model data.
- **F2 (what a prevalence can say about a when-then claim): fixed.**
  - A row matched by prevalence alone may only say "complements", in Q22 and plan lines 215-226.
  - A5's failure example is a prevalence-only row marked "converges".
  - The co-occurrence branch is gone.
  - With "open data", 3 of the 6 rows are mapped (propositions P2, P4 and P5).
- **V (validator showed the two checks failing): fixed.** The text output shows WAIT, and `cold-review.md` records why.
- **Notes n1 to n7, n9 and n10: fixed.**
  - The challenge edge e38 is gone, and the two new concepts are in the domain graph.
  - The brief's lines :110 and :118-121 now have rows (plan lines 121 and 125).
  - The `PLANNING_STATUS.md:208-218` limits are quoted and handled.
  - The A4, A5, A7 and A11 router records each choose the view their entry names.
  - Q19 now cites :292, and the investigation file says S3 is computed.
  - The context graph has a `github_issues` node.
- **Note n8 (page links): not fixed, by choice.** It stays a note.

#### Blocking finding

**B1. S4: the Process Tracing route it names does not produce the export the workbench reads. Where:** plan lines 251-255 and 260-262; `planning-package.json:313-320`; `investigation.json:231-238` (F13); `SYSTEM_MODEL.md:51`; `acceptance-criteria.json:97-112` (A6).

- **What is wrong:** S4 runs "QC handoff → PT draft-audit route → `pt_export_v2`" and prices the draft-audit route. Process Tracing's own records say otherwise:
  - Its accepted ADR 0004, which Brian approved on 2026-11-05 ("i approve those."), says the draft-audit prototype "writes no `pt_export_v2.json` for `mixed_methods_workbench` (Q20)" (`process_tracing/docs/adr/0004_…md:79`).
  - Its open question Q20 (`process_tracing/docs/planning/open-questions.json:404-412`) proposes only a small adapter that is "never a full V2 claim" and marks the missing fields absent.
  - The prototype folder has no qualitative-handoff input at all (no match for `qualitative_handoff` under `proposals/pt-draft-audit`).
  - The pipeline that does accept the handoff and write the gated export (`pt/cli.py:72`, `pt/export.py:634`) "stays frozen" and is kept as the comparison (ADR 0004:67-70). On its last two hard cases it stopped without an answer, after 122 calls and $0.94 on one of them.
- **Why it blocks:**
  - Investigation finding F13 says "holds" only because it cites the frozen pipeline.
  - The $0.03 cost leaves out the merge step: Process Tracing records $0.0555 over 7 calls per run.
  - A6's gate test needs a `publication_gate.publishable` field that the named route never writes.
  - No question in this package's ledger raises any of this.
  - `stops.searched` (`planning-package.json:376-381`) looked only for stops on the workbench, not on the Process Tracing work S4 runs.
- **Fix:**
  - Add a ledger question citing Process Tracing's ADR 0004 and its Q20. It should choose between (a) adding the Q20 adapter in Process Tracing, plus a handoff input, as costed producer work, with the gate shown as "withheld" when the field is absent, or (b) running the frozen pipeline on a small case as the "full provenance chain" reference that ADR 0004 allows.
  - Correct S4's route and cost, F13's verdict, the system model's S4 row and A6.
  - Extend `stops.searched` to Process Tracing's freeze and its 2026-11-05 decision.
  - **Weight:** blocking.

#### Notes (do not block)

- **n1. Stale wording after the design change.**
  - Plan line 74 (the S3 row of the slice table), `DOMAIN.md:35` and the `joint_display` node still offer "convergence / complementarity / divergence" verdicts.
  - A5's criterion says "read whether they agree", but no row can now say that.
  - The goal statement (`review-page.json`) says S2 measures "a qualitative category"; it now measures one of the author's codes.
  - **Fix:** reword all four to "complements or silent in 1.0" and "one of the authors' codes".
- **n2. Wrong claim about LiteLLM.** The cost evidence (`planning-package.json:224,241,258,275`) says LiteLLM "carries no price" for gpt-5.6-luna. llm_client's copy of LiteLLM lists $0.20 input and $1.20 output per million tokens (its price file, lines 33826/33839 and 65989-65990). The fitted prices are higher, so the figures are conservative. **Fix:** cite the list price beside the fit.
- **n3. A question the ledger misses about the qualitative side.** Two pairs of QC's categories cite exactly the same turns: "Traceable…" with "Corrective…", and "Terminological…" with "Attributed reuse…". So QC's 8 categories rest on only 6 distinct sets of evidence. A3 will show 8. "Open data"'s two categories are distinct, so S2 and S3 are not affected. **Fix:** add a finding or question so the study page says so.
- **n4. Unnamed step.** Plan line 122 does not say who drafts the instrument's definition from the author's passages. If a model drafts it, that call belongs in the cost table.
- **n5. Agent-owned questions still open.** Q2, Q3, Q4, Q10 and Q21 could be settled now by checking (an old pattern).
- **n6. Page links (carried from n8).** The branch is on no remote (`git branch -r --contains 2092693` is empty), so the page's `/blob/main/` links to the plan return 404 until it is pushed and merged. The repository belongs to Brian's own account, so the company-organization rule does not apply.

#### What I was unsure about

- **Whether B1 should block.** S4 is a later slice. But the package's claim that S4's route works is wrong, and it changes S4's design, its cost and how A6 is judged, so I counted it as blocking.
- **Whether running the frozen pipeline would break a standing stop.** ADR 0004 keeps the pipeline as "the reference where a reader must step through a full provenance chain", which may allow option (b).
- **Two limits on this review.** I did not render the page because no browser tool was available. I also could not run the test suite.

---

- **Verification:**
  - Validator: exit 1, with the counts above.
  - `plan_checklist.py --check`: exit 0.
  - Crosswalk check: exit 0, 171/36/0.
  - Overlap scripts and an open-data spread check: figures as above.
  - Price refit from a read-only query of `llm_observability.db`: matches.
  - The Process Tracing ADR, ledger and autopsy were read directly.
- **Feedback:** The validator's `--json` checklist labels planned or untested lines "failing" while its text output prints WAIT, so plans carry "failing" lines for a state the contract defines as pending. The fix belongs in `validate_planning_package.py`. This session also could not run the test suite (it needed approval) or list folders in sibling repositories.
- **Need anything from human:** No.

Reviewed revision: c79e70bc7704557221b028ebf168f910b843c68e

Verdict: revise

## Plan #8, round 6 reviewer's report (verbatim)

The verdict is **revise**. One blocking problem is left, and it is the part of the round-5 fix that changed acceptance check A6. That fix leans on a test file that does not exist in the form the plan describes. The rest of the round-5 fix holds, and so do the overlap figures, the crosswalk counts and the S4 cost.

#### Validator

I ran it on the current branch (revision 0782bbf); it exited **1**.

- **Parts:** 9 of 10 ok. The only failure is the cold review, whose recorded verdict is still `revise`. That was expected.
- **Substance checks:** 10 of 12 ok, 0 failing, 2 pending (WAIT). The two pending lines are the planned plain-version comparison and the 3 untested extra stages; the contract makes both WAIT on purpose.
- **Other lines:** initiative and spectrum tiers 4 of 4. Goal coverage passes (2 requirements covered, 1 marked as being about process). Goal provenance passes. Freshness passes, counting 1 commit of work since 9ad84d1.
- **Plan checklist:** `plan_checklist.py --check` matches, 0 differing lines, exit 0.

#### Recorded checks I reran

- **Overlap scripts** (`overlap.py` and `overlap2.py` on the S1 branch at faf5399): every figure matches the package. There are 630 interviewee turns, 224 pairs of a QC category and an author code, and 11 numbered question codes. "Open data" marks 14 of 22 turns (0.64, chance 3.0e-9) and 14 of 21 (0.67, chance 1.2e-9). The next-best share is 0.48 and the highest two-way overlap is 0.18. The two pairs of QC categories that cite identical turns show up as stated.
- **Crosswalk check:** 171 steps, 36 groups, 0 errors, exit 0. Matches the manifest, and the tree stayed clean.
- **`make check`:** exit 0, with 41 pytest tests passing (11 + 30). Matches the manifest.
- **S4 cost:** Process Tracing's efficiency readout (lines 161-163) gives `fomc_v4` as 7 calls, 352,770 input tokens (277,101 cached), 26,828 output, $0.0555, with no audits. That matches the cost entry and the default setup ADR 0004 chose.
- **Computed costs:** the S2 plain version ($0.0783), the definition call ($0.0043) and the S3 plain version ($0.0137) all recompute.
- **A1 (marked built):** the live page returned 200. Its `index.html` hash (eae2c256…) equals the committed `deploy/psychosisbank-review/public/index.html`. It contains the "Independent challenge" section, "withheld" and "Controlled access", so the demonstration can be followed there.

#### Round-5 findings

- **B1 (S4's Process Tracing route): partly fixed; the A6 part is fixed wrongly, so B1 stays blocking.**
  - **Fixed:** S4 now names the draft-audit prototype plus a handoff input and the export adapter that Process Tracing's own Q20 recommends. That matches ADR 0004 (line 79: the prototype "writes no `pt_export_v2.json`"; line 67: `pt/` stays frozen) and Q20 (open-questions.json, line 410: "never a full V2 claim").
  - **Also fixed:** finding F13 now says "fails" and points to Q23. The S4 row in SYSTEM_MODEL.md (line 51) is corrected, the cost is the measured $0.0555, and `stops` now records the freeze.
  - **Fixed wrongly:** the claim that "the publishable branch is tested with the committed fixture that carries a gate" (detail under the blocking finding below).
- **n1 (stale verdict wording): fixed.** No "convergence / complementarity / divergence" wording is left. A5 reads "which ones the measure speaks to and how". The goal fields name "one of the corpus authors' own codes".
- **n2 (LiteLLM price): fixed.** The list price ($0.20 input, $1.20 output per million tokens) is cited beside the higher fitted price.
- **n3 (QC categories citing the same turns): fixed.** Finding F19 and plan lines 157-161 cover it, and my overlap run confirms it.
- **n4 (who drafts the instrument's definition): fixed.** One traced llm_client call, costed at $0.0043 in the plan (line 212) and the manifest.
- **n5 (agent questions that could be settled now): not fixed, by choice.** Still a note.
- **n6 (page links): not fixed, by design.** Still a note: the branch is still on no remote.

#### Blocking finding

- **B1 (remaining part): acceptance and plan.** Where: `docs/plans/008_finish_workbench.md:272-274`, `docs/planning/acceptance-criteria.json:104` (A6 expected result) and `docs/planning/open-questions.json:436` (Q23 `resolves_with`).
  - **What is wrong:** the fixture cited for the "publishable" case, `examples/fixtures/investigation_spine/process_tracing_return.json`, does not support that claim:
    - It is a `pt_theory_test_return_v1` record, not a `pt_export_v2`.
    - Its gate says `"status": "blocked"` and `"public_conclusion_status": "withheld_pending_repair"`, which is the withheld case.
    - It has no `publishable` field at all.
    - The only real `pt_export_v2` in the repository (`examples/runs/psychosisbank-synthesis-20260923/pt-generated/pt_export_v2.json`) has no `publication_gate` either, and its `public_headline_eligible` is false.
  - **Why it matters:** no committed file exercises the "conclusion shows" case. A6's demonstration has no step that reaches one. On the only real case, the Open Science proposition, a working page and a broken page that never shows any conclusion both read "withheld". So Brian cannot judge the half of A6 that says "unless the gate allows it".
  - **Fix:**
    - Correct the claim in all three places.
    - Then do one of two things:
      - (i) Commit a small `pt_export_v2` test file with a publishable gate (status accepted, integrity verified, `publishable` true), and one with a blocked gate. Label them as made-up test data, which supports only a claim about their shape. Show both in a "how the gate behaves" panel on the Causal tab, with an A6 step that opens it.
      - (ii) Run the frozen pipeline once on the same small one-interview case. ADR 0004 (lines 67-69) keeps it "as the reference where a reader must step through a full provenance chain (… report and workbench)", so this gives a real gated export.
    - Add a second failure example: "the publishable example still reads 'withheld'".
  - **Weight:** blocking.

#### Notes (do not block)

- **N1 (plan wording).** `008_finish_workbench.md:45`, `:75` and `DOMAIN.md:42` still describe the old route:
  - Line 45 says "PT's `pt_export_v2` already takes a QC handoff". Only the frozen pipeline's command does.
  - Line 75 says "QC handoff → PT `pt_export_v2` … publication gate respected".
  - DOMAIN.md:42 still says the export's own `publication_gate.publishable` field is read from S4, but S4's export will carry no gate.
  - Also missing: in 1.0, no causal conclusion from Process Tracing's answer path is ever shown, because that path carries no gate.
  - Also unnamed: the schema the adapter's partial export declares. Process Tracing's Q20 says "never a full V2 claim", yet `ProcessTracingExport` (`investigation_run.py:101-113`) requires `schema_version` to be "pt_export_v2" and a full set of required sections.
  - **Fix:** reword lines 45 and 75 and the glossary entry, and name the adapter's schema and which reader fields become optional. Weight: note.
- **N2 (`stops`).** `planning-package.json:398` and `:410`:
  - The search line says Process Tracing's stops were read, but the stops its autopsy lists are not recorded: "overbuilt" (2026-07-29), "archive … start over" (2026-08-20) and "a patch, not an actual fix" (2026-09-24). See `process_tracing/docs/analysis/autopsy_20261106.md:142-143`.
  - None of them holds against S4's work on the prototype. Brian's 2026-09-24 decision to archive the restart and his 2026-11-05 "i approve those." lift them, so they should be recorded as `lifted`.
  - The freeze entry's `words`, "pt/ stays frozen (Brian, 2026-09-30)", is the ADR's paraphrase. The autopsy (line 75) says Brian's own words for the freeze were not found.
  - Weight: note.
- **N3 (investigation).** `investigation.json:288`: F18 says "holds" and points to Q1. That is true of the frozen pipeline's schema, not of the export S4 will read. **Fix:** narrow the claim and point it to Q23. Weight: note.
- **N4 (acceptance coverage record).** `acceptance-criteria.json:251-254`: the stored record calls "part of broader vision" a process requirement and leaves it uncovered.
  - I split Brian's words myself into three requirements:
    - "finish" is covered by A2-A9;
    - "not for a specific use case" is covered by A10 and A3;
    - "part of my broader vision" is covered by A11, and the outcome line keeps it.
  - So nothing is lost today. But if A11 were later dropped, no coverage check would notice. **Fix:** re-judge once with `--force` so the third requirement becomes a constraint mapped to A11. Weight: note.
- **N5 (domain model).** S4 builds an input for QC's `export-process-tracing-handoff` package (`qc/qc_clean/core/process_tracing_handoff.py:202`, which exports `state.claims`). That concept is in neither the domain graph nor `relies_on`. S4 should also confirm that the Open Science project state carries the chosen proposition as an anchored claim (QC has a `GT_PROPOSITION` claim kind). Weight: note.
- **N6 (cold-review record).** `planning-package.json:430` and the page still give bdf06d7 (round 4) as the reviewed revision, though round 5 read c79e70b. This round replaces it. Weight: note.
- **n5 (carried, ledger).** Q2, Q3, Q4, Q10 and Q21 are agent questions that could be settled by checking now. Weight: note.
- **n6 (carried, page).** `git branch -r --contains 9ad84d1` is empty, so the page's `/blob/main/` links return 404 until the branch is pushed and merged. The repository is in Brian's own account, so the company-organization rule does not apply. Weight: note.

#### What I was unsure about

- **Whether the A6 problem should block.** It is narrow and S4 is a later slice. But it is a false claim inside a blocking fix, and it leaves half of a user outcome impossible for Brian to judge, so I kept it blocking.
- **Whether option (b) is the better route.** Running the frozen pipeline once on the small one-interview case changes no `pt/` code, ADR 0004 names the workbench as a reason to keep it, and it would give A6 a real gate. Choosing between (a) and (b) is the agent's technical call; Q23's reasoning for (a) is defensible.
- **What I could not do.** No browser tool was available (Playwright is not installed), so the page was read as HTML, not rendered. I ran the 41 tests inside `make check`, not the full 204-test suite.

---

- **Verification:**
  - Validator: exit 1. Parts 9/10, substance 10/12 ok with 2 pending, tiers 4/4; coverage, provenance and freshness ok.
  - `plan_checklist.py --check`: exit 0.
  - Crosswalk check: exit 0 (171 / 36 / 0).
  - `make check`: exit 0.
  - Overlap scripts: figures as above.
  - Fixture and real-export gate fields: read directly.
  - Process Tracing's ADR 0004, its Q20, the efficiency readout lines 161-163 and the autopsy: read directly.
  - A1's live page: fetched; its hash equals the committed copy.
- **Feedback:** the validator's JSON checklist labels the pending lines "failing" (plan lines 389-390) while its text output prints WAIT. This is a plugin fault, carried from round 5.
- **Need anything from human:** No.

Reviewed revision: 9ad84d1a935515f616067d98c77a58aecf2a0084

Verdict: revise

## Plan #8, round 7 reviewer's report (verbatim)

The verdict is **revise**. Round 6's one remaining blocker is fixed: Process Tracing's gate code supports the two made-up test exports, and A6 can now be judged. But two new problems block:

- **The new A12 check promises something no slice builds.** A12 is the "is it finished" check. Its end-to-end run on the second corpus includes a causal check, but no slice runs Process Tracing on that corpus, and S7 still says it makes no model calls.
- **The plan quietly narrows mixed-methods integration and labels it "kept".** The roadmap's 1.0 gate requires "contradiction disposition". Under the plan, the 1.0 joint display can only ever say "complements" or "silent", so the two strands can never agree or disagree. Brian has not been asked about this.

#### Validator

I ran it on the branch head, 09ff61e. Since the subject revision 58f644a, that commit changed only package files. It **exited 1**, which was expected.

- **Parts:** 9 of 10 ok. The only failure is the cold review, whose recorded verdict is `revise`.
- **Substance checks:** 10 of 12 ok, 0 failing, 2 pending (WAIT). The two pending lines are the planned plain-version comparison and the 3 untested stages; the contract makes both WAIT on purpose.
- **Initiative and spectrum checks:** 4 of 4 ok.
- **Goal coverage:** ok. It found 3 requirements in Brian's words: 2 covered (R1 by A12, R2 by A10) and 1 classed as about process (R3, mapped to A11).
- **Goal provenance and freshness:** both ok, with 0 commits of work since 58f644a.
- **Plan checklist** (`plan_checklist.py --check`): matches, 0 differing lines, exit 0.

#### Recorded checks I reran

All match the manifest.

- **Overlap scripts** (`overlap.py` and `overlap2.py` on the S1 checkout, faf5399, clean tree):
  - 630 interviewee turns, 224 pairs, 11 numbered question codes.
  - "Open data" marks 14 of 22 turns (0.64, chance 3.0e-9) and 14 of 21 (0.67, chance 1.2e-9). The next-best share is 0.48, and the highest two-way overlap is 0.18.
  - The two pairs of identical categories (F19) show up as stated.
- **Crosswalk check** (`crosswalk_phase4.py --check`): 171 steps, 36 groups, 0 errors, exit 0.
- **`make check`:** exit 0, 41 tests passing (11 + 30).
- **S4 cost:** Process Tracing's efficiency readout (`README.md:161-163`) gives `fomc_v4` as 7 calls, 352,770 input tokens (277,101 cached), 26,828 output, $0.0555. That matches the cost entry.
- **S2 plain-version cost:** 2 × (58,150 × $0.2168 + 18,900 × $1.4057) per million tokens = $0.0783. That matches.

#### Round-6 findings

- **B1 (A6's publishable case): fixed.**
  - The plan (lines 283-289), A6 (`acceptance-criteria.json:103-106`) and Q23 now say that no committed file carries a publishable gate.
  - S4 commits two labelled test exports. The gate fields named ("status accepted, integrity verified, `publishable` true") match `PublicationGateV2` in `process_tracing/pt/export.py:597-626`.
  - Process Tracing's own export says "consumers must treat a missing gate as not publication-ready", which supports showing "withheld" when the gate is absent.
  - A6 has a step that opens the panel, and a second failure example.
- **N1 (old route wording): fixed.** Plan lines 45 and 75 and `DOMAIN.md:43` are reworded. The partial schema `pt_draft_audit_export_v1` and its optional fields are named (plan lines 268-272).
- **N2 (`stops`): fixed.** The three stops are recorded and the freeze's wording is marked as a paraphrase. Two of the new labels are questionable (note a).
- **N3 (F18): fixed.** It is narrowed and points to Q23.
- **N4 (coverage record for R3): not fixed in substance.** The judge still classes R3 as process; it is mapped to A11 but still needs no criterion. A12 was added for R1. Still a note (note f).
- **N5 (QC's handoff missing): fixed.** `qc_pt_handoff` is now in the glossary, graph, spectrum and `relies_on`, and the claims citation `process_tracing_handoff.py:221` is right. Its kind is wrong (note b).
- **N6 (stale reviewed revision): fixed.** The manifest now gives 9ad84d1.
- **n5 and n6 (carried):** still notes.

#### Blocking findings

**1. Acceptance and plan: A12's end-to-end run asks for a causal check that no slice builds or costs.**

- **Where:** `acceptance-criteria.json:211` and `:214`; `008_finish_workbench.md:326`, `:337-340` and `:344-352`.
- **What is wrong:**
  - A12 step 4 runs "the second corpus … through qualitative strand, measurement, joint display, causal check, review and bundle".
  - S6 builds only "the whole S1–S3 path" on the second corpus. S4 is one Open Science proposition.
  - So nothing builds the causal check on the second corpus. It would need QC's handoff with a `GT_PROPOSITION` claim on that corpus, a run of Process Tracing's prototype, and the export adapter.
  - S7 still reads "Cost: none (no AI step)", and no `cost_basis` entry covers this run.
  - A12 also never says that "met" requires Brian's "judged pass". Its failure example catches only "not built", so 1.0 could be tagged on criteria an agent marked "built".
- **Fix:**
  - Either add S4's route on one second-corpus proposition to S6, with its cost: measured, at most $0.0555, plus QC's precondition under Q21.
  - Or narrow A12's end-to-end run to the steps S6 runs, and point the causal row at S4's Open Science run.
  - Change S7's cost line to the run's real calls, or say it reuses S6's receipts.
  - State that a row reads "met" only when its criterion is "judged pass" in Brian's recorded words.
- **Weight:** blocking. A12 is the only criterion covering "finish", and as written it cannot pass by following the plan.

**2. Plan and open questions: the integration condition is marked "kept" but is narrowed by an agent, and no question asks Brian.**

- **Where:** `008_finish_workbench.md:46` and `:222-233`; Q22 (`open-questions.json:411`); `ROADMAP.md:83` and `:437`; Q12 (`open-questions.json:201`).
- **What is wrong:**
  - The roadmap's 1.0 gate is "G1–G6 meet their 1.0 conditions" (`ROADMAP.md:437`). For G4 that condition is "One observed design, joint display, contradiction disposition, and integration-quality review" (`:83`).
  - Under Q22's rule, every 1.0 row can only say "complements" or "silent: not measured". So 1.0 can never show the strands agreeing or disagreeing, and never deals with a contradiction.
  - The plan and ledger never mention "contradiction disposition", and the "finished" table says the condition is "kept".
  - Q12 already sends two similar narrowings of what 1.0 promises to Brian. This third one was settled by agent argument.
  - A12's own rule says a changed condition must show Brian's approving answer. Yet S7 and A12 build their rows from the eight "What 1.0 Means" bullets, not from the G1–G6 gate the roadmap's 1.0 section uses.
- **Fix:**
  - Mark the row "changed: complements only in 1.0".
  - Add it to Q12 as part (c), with a recommendation and a default. One option to name: in S2, measure a proposition's condition and outcome, or a salience claim QC makes, so that a row could agree or disagree.
  - Have the readiness page carry G1–G6's 1.0 conditions too, or state in the plan that the eight bullets replace that gate.
- **Weight:** blocking. A material question is missing, and it changes what 1.0 claims about the integration, which is the core purpose of a mixed-methods workbench.

#### Notes (do not block)

- **a. `stops` labels** (`planning-package.json:417-425` and `:437-445`).
  - "overbuilt" and "a patch ot an actual fix" are marked `lifted` by "i approve those." (ADR 0004 line 10).
  - Those words approve freezing the pipeline and making the prototype the answer path. That acts on "overbuilt" rather than lifting it, and does not address the round cap at all.
  - **Fix:** mark both `holds`, honoured because S4 runs no pipeline. For the freeze entry, Brian's own approved words exist and could replace the paraphrase: ADR 0004's Decision 1, "the full pipeline is frozen …", answered "i approve those." on 2026-11-05.
  - Also: `stops.searched` (line 396) found the Phase 3 pause lifted on 2026-10-08, but `found` does not list it.
- **b. `qc_pt_handoff`'s kind** (`domain.graph.json:278`, `DOMAIN.md:38`).
  - It is marked "planned", but QC already implements it (`process_tracing_handoff.py:202`), so its kind should be "elsewhere".
  - The plan's own "Relies on" list (lines 356-362) leaves it out.
  - `claims.py:33` points at a use of `GT_PROPOSITION`, not where it is defined.
- **c. System model** (`SYSTEM_MODEL.md:44-53` and `:71-72`): there is no S7 row. The readiness page, the "runs / does not run" field and the crosswalk page are missing from both the planned types and the planned list of pages.
- **d. S4's test exports** (plan lines 283-289): the plan does not say which schema the two made-up exports use, or which reader opens them. The panel should test the reader the real case uses.
- **e. Coverage record** (`acceptance-criteria.json:270-276`): R3 is still classed as process (round-6 N4). If A11 were dropped, the coverage check would not notice.
- **f. Carried n5:** Q2, Q3, Q4, Q10 and Q21 are agent questions that could be settled by checking now.
- **g. Carried n6:** the branch is on no remote (`origin/plan-008-finish` does not exist). So the page's `/blob/main/` links to Plan #8's files return 404 until merge, and the page has no served address (Q11). The repository is in Brian's own account, so the company-organization rule does not apply.

#### What I was unsure about

- **Weight of blocking finding 2.** The plan states the narrowing openly (line 232), so a careful reader is not misled about what S3 does. I kept it blocking because the plan labels the condition "kept", "contradiction disposition" appears nowhere in the plan or the ledger, and Q12 sets the precedent that narrowing what 1.0 promises is Brian's call.
- **Whether the A12 fix should widen S6 or narrow A12.** Either is defensible; it is the author's call.
- **What I could not do:**
  - No browser tool was available, so I read the page as HTML. The diagrams are drawn on the page by `GraphViewer.mount` from embedded data, and every local link resolves.
  - Fetching A1's live page needed approval this session lacks. `deploy/` is unchanged since round 6, which matched the live page against the committed copy.
  - I ran the 41 tests inside `make check`, not the 204-test suite.

---

- **Verification:**
  - Validator: exit 1. Parts 9/10, substance 10/12 ok with 0 failing and 2 pending, tiers 4/4; coverage, provenance and freshness ok.
  - `plan_checklist.py --check`: exit 0.
  - Crosswalk check: exit 0 (171 / 36 / 0).
  - `make check`: exit 0.
  - Overlap scripts: the figures above.
  - `git diff 9ad84d1 09ff61e -- deploy/ src/ tests/ scripts/ examples/`: empty.
  - Read directly: Process Tracing's ADR 0004, its Q20, the autopsy (lines 65-80 and 135-150), the efficiency readout (lines 155-170) and `pt/export.py:590-660`; QC's `process_tracing_handoff.py:195-235` and `claims.py:20-45`.
- **Feedback:** the validator's JSON checklist still labels WAIT lines "failing" (plan lines 411-412). This is a plugin fault, carried from rounds 5 and 6.
- **Need anything from human:** No.

Reviewed revision: 58f644a7e99565b103940b7c884c3b5cb7ab7a25

Verdict: revise

## Plan #8, round 8 reviewer's report (verbatim)

**Round 8 cold review: revise.** Both round-7 blocking findings are fixed. One new problem blocks, and the round-7 fix for A12 now leans on it: the causal check in S4 and S6 needs Qualitative Coding's handoff to Process Tracing to carry a proposition, and QC's own code and its pinned Open Science data show it carries none.

#### Validator

I ran it on the branch head, 2757565. Since the subject revision 9dd6009, that commit changed only package files. It **exited 1**, which was expected.

- **Parts:** 9 of 10 ok. The only failure is the cold review, whose recorded verdict is `revise`.
- **Substance checks:** 10 of 12 ok, 0 failing, 2 pending (WAIT). The two pending lines are the planned plain-version comparison and the 3 untested stages; the contract makes both WAIT on purpose.
- **Other figures:**
  - Cost basis: 13 AI steps, 3 measured and 10 computed.
  - Stops: 6 found, 4 hold and 2 lifted.
  - Citations: 79 checked.
- **Initiative and spectrum checks:** 4 of 4 ok.
- **Goal coverage:** ok. It found 3 requirements in Brian's words: R1 is covered by A12 and A9, R2 by A10, and R3 is classed as about process (mapped to A11).
- **Goal provenance and freshness:** both ok.
- **Plan checklist** (`plan_checklist.py --check`): matches, 0 differing lines, exit 0.

#### Recorded checks I reran

All match the manifest.

- **Overlap scripts** (`overlap.py` and `overlap2.py` on the S1 checkout, faf5399, clean tree):
  - 630 interviewee turns, 224 pairs, 11 numbered question codes.
  - "Open data" marks 14 of 22 turns (0.64, chance 3.0e-9) and 14 of 21 (0.67, chance 1.2e-9). The next-best share is 0.48, and the highest two-way overlap is 0.18.
- **Crosswalk check:** 171 steps, 36 groups, 0 errors, exit 0.
- **`make check`:** exit 0, 41 tests passing (11 + 30).
- **S4 cost:** Process Tracing's efficiency readout (`README.md:161-163`) gives 7 calls, 352,770 input tokens (277,101 cached), 26,828 output, $0.0555. That matches.
- **S7 cost:** $0.0783 + $0.0137 + $0.0555 = $0.1475 over 10 calls, which matches "about $0.15".
- **Q12(c)'s cost:** 2 × (58,150 × $0.2168 + 56,700 × $1.4057) per million tokens, plus 2 × $0.0043, is $0.193. That matches "about $0.19".
- **Stop search:** `git log -i --grep 'pause|archive|overbuilt|start over'` finds the NYC pause (91a69a5) and the Phase 3 pause (e37fd80) and its lift (680c4d5). It found no stop the manifest missed.

#### Round-7 findings

- **1. A12's causal check had no slice: fixed as asked.**
  - S6 now runs S4's route on one second-corpus proposition (plan `:343-347`).
  - S7's run is costed, with three `cost_basis` entries.
  - A row reads "met" only when its criterion is "judged pass" in Brian's recorded words (plan `:362-364`; A12's expected result and failure example).
  - However, the route it adds depends on the same QC precondition as S4, which fails (new finding B1).
- **2. Integration narrowed but labelled "kept": fixed.**
  - The row now reads "changed: … 'complements' or 'silent' in 1.0" (plan `:46`) and cites G4's "contradiction disposition" (`ROADMAP.md:83`).
  - Q12 has a part (c) with a recommendation, a default, the worked-out cost of the other option and answer words. Q22 points there.
  - S7 and A12 now carry both the eight bullets and the G1–G6 1.0 conditions (plan `:53-56`, `:359-361`; `ROADMAP.md:79-84`, `:437`).
- **a. `stops` labels: fixed.**
  - "overbuilt" and "a patch ot an actual fix" are now `holds`.
  - The freeze entry quotes Decision 1, matching ADR 0004 lines 10-15.
  - The Phase 3 pause is listed (see note n6).
- **b. `qc_pt_handoff`: fixed in kind, citation and "Relies on".** `domain.py:179` is where the claim kind is defined. Its definition is now wrong (B1).
- **c. System model had no S7 row: fixed** (`SYSTEM_MODEL.md:54`, `:73-74`).
- **d. Test exports' schema and reader unnamed: fixed** (plan `:293-295`).
- **e, f, g: not fixed, by choice.** They remain notes n8 to n10.

#### Blocking finding

**B1. Plan, domain model and open questions: QC's handoff to Process Tracing carries no proposition, so S4's causal route cannot start as written.**

- **Where:**
  - `docs/plans/008_finish_workbench.md:270-271` and `:280-283` (S4)
  - `:343-347` (S6)
  - `docs/planning/DOMAIN.md:38` (`qc_pt_handoff`)
  - Q21's `resolves_with`
- **What is wrong:**
  - The plan says that QC's `export-process-tracing-handoff` output for the chosen proposition becomes a draft-audit case. It also says that S4 "first checks" that the Open Science project state carries the proposition as an anchored claim of QC's `GT_PROPOSITION` kind.
  - QC's code already answers that check, and the answer is no:
    - `qc_clean/core/claims.py:999-1013` builds that kind of claim as an "unanchored grounded-theory proposition-like claim".
    - It is called only from `claims_for_gt_theory` (`:433-461`), which reads `state.theoretical_model`.
  - The pinned Open Science state (`public_demo_assets/open_science/project_state.json.gz`, sha256 a16375a1…, matching S1's pin) has 1,139 claims, none of them of the proposition kind, and no `theoretical_model`.
  - The six propositions and their supporting segment ids exist only in the grounded-theory export (`proposal.propositions[].supporting_source_unit_ids`). `process_tracing_handoff.py` never reads that export: the words "proposition", "theor" and "grounded" do not appear in it.
  - So the handoff would hand Process Tracing no proposition at all. That breaks S4, A6, S6's causal check and the causal step of A12's end-to-end run.
  - The investigation never checked the QC side of this route; F13 looks only at Process Tracing.
- **Fix:**
  - Record an agent question, resolved by this reading.
  - Choose one of:
    - (a) S4's handoff input reads the chosen proposition and its supporting segments from the grounded-theory export S1 already pins. Name that reader and its schema; QC needs no change.
    - (b) QC adds anchored proposition claims to `state.claims`, done in QC's repository under its own rules and with its cost.
  - Correct the `qc_pt_handoff` definition and Q21's precondition to match.
- **Weight:** blocking. A reader would conclude S4 is ready to build, but the only causal route in 1.0 cannot start as written.

#### Notes (do not block)

- **n1. Domain model** (`DOMAIN.md:37`): `qc_theory_export` is marked planned, but QC's export already exists; only the workbench's reader of it is planned. This is the same issue round-7 note b found for the handoff. **Fix:** mark it "elsewhere", or say that only the reader is planned.
- **n2. "Relies on" and domain graph:** S7's 1.0 readiness record (`SYSTEM_MODEL.md:54`) is something the plan creates, but it is in neither the domain graph nor `relies_on`. **Fix:** add a planned concept for it.
- **n3. Plan `:46` against S5 `:310-323`:**
  - Line 46 says S5 "records a disposition for every row the number and passage check marks orange", but S5's build text says only "accept, reject or annotate each meta-inference".
  - G5's "roles" (`ROADMAP.md:84`) is not named in any slice.
  - **Fix:** one clause in S5 for each.
- **n4. Cost basis:** S6's own causal-check run and its S3 call have no entries of their own. The S4 and S3 "per run" entries cover them, but the S6 entry's evidence leaves out the $0.0555 that plan `:353` adds.
- **n5. Plain version:** the causal tab shows Process Tracing's prototype output, but `plain_baseline` covers only S2 and S3. Process Tracing's own records show the prototype beat a plain draft by 0.83, under its 1-point noise line (ADR 0004 `:61-66`). **Fix:** cite that comparison, or say the answer path is Process Tracing's.
- **n6. `stops`, the Phase 3 entry:**
  - Its `words` are an agent's record of the pause, not Brian's words.
  - The lift words "i approve." (`ROADMAP_AGENT_MODEL.md:19`) approved the crosswalk. The lift itself was inferred from that approval (row 5a, and `GOAL_FINISH_DECOMPOSITIONS.md:14-16`).
  - It has no effect on this plan, because Phase 3 is complete.
- **n7. Goal fields:**
  - The thesis's headline, "Integration is the workbench's own value", is not tested by any observation in the disproof. The disproof tests only measurement agreement, planted faults and code changes.
  - **Fix:** add one integration observation to the disproof, or narrow the thesis.
- **n8. Carried e:** the coverage record classes R3 as process.
- **n9. Carried f:** Q2, Q3, Q4, Q10 and Q21 are agent questions that could be settled by checking now. Q21 could be answered today by listing QC's run records.
- **n10. Carried g:**
  - The branch is not on the remote, so the page's 147 `/blob/main/` links return 404 until this pull request merges.
  - The page has no served address (Q11).
  - The repository is in Brian's own account, so the company-organization rule does not apply. Every local link on the page resolves.
- **n11. Plugin fault:** the plan checklist labels the WAIT lines "failing" (plan `:431-432`). This is carried from earlier rounds.

#### Checked and found sound

- **Domain model:**
  - The eight implemented locations I opened (`models.py:268` and `:438`, `investigation_spine.py:127`, `:160` and `:278`, `investigation_run.py:101` and `:124`, `method_dashboard.py:190`) are the classes named.
  - `executes_typed_rules: false` holds: the guarded-decision module calls a policy function passed in, and evaluates no rules itself.
- **Router records:** A6, A11 and A12 choose the views their entries name.
- **No code changed since round 7:** `git diff 58f644a HEAD -- deploy/ src/ tests/ scripts/ examples/` is empty.
- **Review page:**
  - It draws all three diagrams on the page (`GraphViewer.mount`).
  - It carries round 7's changes: Q12(c), "awaiting your judgement", and the causal check on the second corpus.
- **Goal fields:** the north star, disproof and outcome fit their definitions.

#### Judgments I was unsure about

- **B1's weight.** Option (a) is a small redesign, so it could look like a note. I kept it blocking because the plan states a precondition the pinned data already contradicts, on the only causal route in 1.0.
- **Q12(c)'s recommendation.** It says a second measured theme would have no human reference. The argument holds for any category other than the one "open data" already qualifies for. I did not test other options, such as co-occurrence of two author codes by interview; it is Brian's call.
- **What I could not do:**
  - No browser tool was available, so I read the page as HTML.
  - I did not fetch A1's live page.
  - I ran the 41 tests inside `make check`, not the 204-test suite.

---

- **Verification:**
  - Validator: exit 1. Parts 9/10, substance 10/12 ok with 0 failing and 2 pending, tiers 4/4; coverage, provenance and freshness ok.
  - `plan_checklist.py --check`: exit 0.
  - Overlap scripts: the figures above.
  - Crosswalk check: exit 0 (171 / 36 / 0).
  - `make check`: exit 0.
  - QC state read with `python3 -I` after a sha256 check: 1,139 claims, 0 of the proposition kind.
- **Feedback:** the investigation part records no check of the producer's own export path, so a route that is broken on QC's side passed seven rounds of review. The reviewer contract could ask the reviewer to open the producer data a route depends on, not only its documentation.
- **Need anything from human:** No.

Reviewed revision: 9dd600945f7dbbdcf3803486ff1d14981331c5f8

Verdict: revise
