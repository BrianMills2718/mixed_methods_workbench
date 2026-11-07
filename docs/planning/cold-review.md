# Cold reviews of this planning package

The latest review comes first. Each records the revision it read and its verdict; the package manifest's
`cold_review` field carries the latest.

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
