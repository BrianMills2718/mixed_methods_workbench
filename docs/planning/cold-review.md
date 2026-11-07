# Cold reviews of this planning package

The latest review comes first. Each records the revision it read and its verdict; the package manifest's
`cold_review` field carries the latest.

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
