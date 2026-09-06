# State Assessment and Next-Agent Brief — 2026-09-06

Status: read-only assessment of canonical `main@739acf1` plus the producer
repositories it depends on, with a task brief for the next implementing agent.
Prepared by a Claude Code session on 2026-09-06. Everything under "Verified"
was executed in this session; everything under "Read" was read from a file and
not executed.

Audience: (1) Brian, to make one decision (section 5); (2) a less-capable
implementing agent, who should read sections 1, 2, 6 and 8 and can skip the
rest.

---

## 1. What this project is, in plain words

The Mixed Methods Workbench is meant to be the *front door* for a research
system built from several separate engines Brian already owns:

| Engine | What it does | Where |
| --- | --- | --- |
| `qualitative_coding` (QC) | codes text, finds themes, negative cases, grounded-theory objects, with exact quote anchors | `~/code/qualitative_coding` |
| `process_tracing` (PT) | tests rival causal explanations inside one case, Bayesian comparative support | `~/projects/process_tracing` |
| `theory-forge` | turns a published theory into an executable analysis | `~/projects/theory-forge` |
| `grounded-research` | independent analysis and adjudication of contested claims | `~/code/inside-success-mega/repos/grounded-research` |
| `llm_client` | the one shared model-call runtime (traces, cost, retries) | `~/code/inside-success-mega/repos/llm_client` |
| `data-contracts` | typed boundary models and a composition grammar | `~/code/data-contracts` |
| OntoCanon / DIGIMON | governed assertions and graph retrieval; **optional** here | `~/code/onto-canon6`, `~/code/Digimon_for_KG_application` |

The workbench's job is to let a researcher start from one policy question,
push evidence through those engines, and end with an auditable, bounded
finding — without merging the engines or flattening their methods into one
generic "analysis". The stable worked example since 2026-08-13 is the **NYC
Congestion Relief Zone** (congestion pricing): six frozen public-hearing
transcripts, two agency PDFs, and two frozen open-data snapshots.

The repository is deliberately *not* an implemented product. It is an
integration authority: contracts, plans, a small amount of real code, and a
lot of governance prose.

## 2. What actually exists (verified 2026-09-06)

### 2.1 Code and checks

| Item | Result | How verified |
| --- | --- | --- |
| Source | 16 modules, 5,555 lines under `src/mixed_methods_workbench/` | `find/wc` |
| Tests | **161 passed**, 0 failed, ~15 s | fresh venv: `pip install -e ~/code/data-contracts -e ".[dev]"`, then `python -m pytest -q` |
| `make check` | all fixture, negative-control, coverage, and DEMO-C1 gates pass; `typecheck-demo` was red only because the Makefile called bare `mypy` from `PATH` (system mypy cannot see `data_contracts`). Venv mypy: **0 issues in 16 files**. Fixed in this commit (`$(PYTHON) -m mypy`). | ran both |
| Dashboard | `PYTHONPATH=src python -m mixed_methods_workbench.method_dashboard_server --port 8765` serves `/` (74 KB HTML, title "Mixed Methods Workbench · Research Design") and `/api/catalog` (57 KB JSON) with HTTP 200 | started, curled, stopped |
| Dependency | `data_contracts==0.1.0` is **not** installed system-wide; the repo has no venv. A fresh agent will see `ModuleNotFoundError` until it installs from `~/code/data-contracts` (see 8.1). | reproduced |
| NYC extraction canary | `scripts/run_nyc_crz_extraction_canary.py` needs `llm_client` and `pypdf` in the same environment; not run today (it is a frozen, already-accepted trace — rerunning proves nothing and spends money) | read |

What the code actually implements (all bounded, all fixture- or receipt-backed):

- `method_dashboard.py` / `_server.py` — question-first method router and local browser page (`METHOD-DASH-C1/C2`).
- `investigation_spine.py` — one investigation page over the pinned Open Science / P5 QC→PT→QC round trip.
- `nyc_crz_evidence_slice.py` — verifies exact NYC PDF bytes, binds two model-extracted candidates to exact source units, presents a review packet (`NYC-EXTRACT-1`).
- `nyc_crz_quantitative.py` — recomputes the frozen 25,992-row vehicle-entry snapshot against the agency's No Action baseline (`NYC-QUANT-1`).
- `guarded_decision/` — "Plan 242" custody/replay seam: one QC and one PT native decision replayed through a common typed request/receipt, with positive and refusal bundles under `docs/research/plan242/evidence/`. Tested (550+554 lines of tests).
- `mist_trail_decision.py`, `simulation_policy_appraisal.py` — two bounded secondary examples.
- `models.py`, `assemble.py`, `io.py`, `cli.py` — the synthetic DEMO-C1 QC/PT/GT contract fixtures.

### 2.2 The NYC investigation — where it really stands

Plan #5 (`docs/plans/005_nyc_crz_mvp.md`) has six units:

| Unit | Status in graph | Reality |
| --- | --- | --- |
| `NYC-EXTRACT-1` | accepted | merged `6403fcf`; Brian accepted the two wordings 2026-08-14 |
| `NYC-QUANT-1` | accepted | merged `103be94`; Brian accepted the bounded comparison 2026-08-14 |
| `NYC-QC-1` | **ready** since 2026-08-14 | **Started in the QC repo the same day and abandoned unmerged** — see below |
| `NYC-INTEGRATE-1` | blocked on QC-1 | nothing |
| `NYC-MVP-REVIEW-1` | blocked | nothing |
| `NYC-CONTRACT-PROMOTION-1` | blocked / deferred | nothing |

**The undocumented QC-side work.** `qualitative_coding` branch
`nyc-crz-six-hearing-qc` (pushed to origin, worktree still present at
`~/code/qualitative_coding/worktrees/nyc-crz-six-hearing-qc`) has five commits
dated 2026-08-14 and ~2,700 added lines:

| Commit | What it adds |
| --- | --- |
| `663d8c92` Bind NYC QC execution unit locally | `docs/plans/5_nyc_crz_qc_work_graph.json` (local copy of `NYC-QC-1`) |
| `2ce05c46` Close NYC six-hearing corpus | `qc_clean/core/nyc_crz_corpus.py`, `scripts/prepare_nyc_crz_corpus.py`, a **corpus receipt** proving all six hearing PDFs were downloaded and byte-verified (359+261+267+317+… = 2,179 pages) |
| `79e6090b` Attest NYC printed-line universe | `nyc_crz_transcript.py`: 54,475 printed-line atoms with per-document manifests (`source_unit_receipt.json`) |
| `620ca7e8` Prepare NYC medical-access semantic canary | `nyc_crz_describe.py` (819 lines): a deductive one-code pass over every page with the frozen protocol `MEDICAL_ACCESS_COST_OR_BURDEN`; ~91 batched model calls; binds positives to exact printed-line atoms via QC's native narrow-evidence selector |
| `3553230d`, `1c6d924e` | model-justification binding; evidence-selection model separated |

Verified today: the branch's three test files **pass (22 tests)** when run as
`PYTHONPATH=. ../../.venv/bin/pytest tests/test_nyc_crz_*.py` from the
worktree. The branch is 5 ahead / **99 behind** QC `main`. The canary script
(`scripts/run_nyc_crz_medical_access_canary.py`) refuses to overwrite a
receipt and requires explicit `--max-budget`/`--budget-reservation`; **no
canary receipt exists on the branch**, so the model pass was never run (a
trace-DB check for `nyc*` trace IDs was still running when this document was
written; see appendix). The downloaded PDFs are not in either repository —
the QC script re-downloads them into `--cache-dir` and verifies SHA-256 and
byte count against the workbench manifest, so this is not a blocker.

Nothing in the workbench (`PLANNING_STATUS.md`, `005_nyc_crz_mvp.md`,
`CLAUDE.md`) mentions that this branch exists.

### 2.3 Producer repositories vs. the pins this repo cites

| Repo | Pinned in `CAPABILITY_ADOPTION_MAP.md` (2026-08-13) | HEAD today | Drift |
| --- | --- | --- | --- |
| `qualitative_coding` | `4ea0ce6` | `1ead13ad` 2026-09-02 | 102 commits |
| `process_tracing` | `8bada47` (amendment re-verified at `4450d2e`) | `a422fb7` 2026-09-01 | 293 commits past `4450d2e`; core rival-explanation files were byte-identical at the amendment |
| `theory-forge` | `9ec293f` | `52dc442` 2026-09-01 | 9 |
| `llm_client` | `be18982` | `028e129` 2026-08-25 | 1 |
| `grounded-research` | `0b46fc1` | `a9edeca` 2026-09-04 | pin not an ancestor of the inspected checkout (different fork lineage) |
| `open_web_retrieval` | `531a093` | `f4621bd` 2026-09-03 | pin not found in the inspected checkout |
| `data-contracts` | `33746ef` / Plan-242 pin `d845be0` | `bfd59aa` 2026-08-28 | canonical checkout is commit-blocked (`6287766`) |

All producer checkouts were clean except `onto-canon6` (7 dirty files,
unrelated). No coordination claim exists on `mixed_methods_workbench` or on the
QC NYC lane (`check_coordination_claims.py --list`: zero matches).

### 2.4 Governance surfaces in this repo

- 145 documentation files (4.6 MB) vs. 5.5 k lines of code and 3.1 k lines of
  tests.
- Four ADRs, seventeen plan documents, two machine-consumed work graphs, four
  phases of method-decomposition research (`docs/research/method_decomposition/`,
  three parallel Codex lanes' output retained at pushed refs), a concern
  register (43 rows), a SOTA scorecard, a coverage report generator, and a
  capability census of thirteen repositories.
- One stale worktree: `worktrees/claude-method-decomposition-phase0` at
  `7a9e40b`, 100 commits behind `main`; its only untracked files are
  byte-identical to files already committed on `main` in `739acf1`. Removed
  in this commit (branch retained locally and on origin).
- `.claude/HANDOFF.md` and `.claude/handoff.yml` date from 2026-07-12 and
  describe a world (ADR 0004 "demo-first", "documentation-only mode") that four
  later Brian decisions have superseded. Marked superseded in this commit.

## 3. Findings

Severity: **H** = will send a fresh agent the wrong way; **M** = costs time or
credibility; **L** = hygiene.

| # | Sev | Finding | Evidence |
| --- | --- | --- | --- |
| F1 | **H** | **Two Brian-approved documents one day apart disagree about the next step.** 2026-08-13: the architecture reset (`SYSTEM_GOAL_AND_CAPABILITY_ARCHITECTURE.md`, `ROADMAP.md` §"Adopted execution roadmap") says the next work is Phase A→B→C→D (capability census → Project-Meta profile → `ExtractStructuredCandidates` action → refactor NYC through it) and that "this sequence supersedes a direct jump … to another case-specific `NYC-QC-1`". 2026-08-14: Brian said "accept all 3" in the coordinating Codex session, Plan #5 was updated to "`NYC-QC-1` is now ready for an exact claimed Qualitative Coding execution", and the QC-side lane was actually started. Neither document acknowledges the other. A fresh agent reading `CLAUDE.md` + `PLANNING_STATUS.md` will conclude NYC is paused; one reading `005_nyc_crz_mvp.md` will start QC-1. | `docs/ROADMAP.md:176-179`; `docs/plans/005_nyc_crz_mvp.md` "Current execution checkpoint"; `docs/research/nyc_crz_human_disposition.json` |
| F2 | **H** | `CLAUDE.md`, `PLANNING_STATUS.md` and `SYSTEM_GOAL_AND_CAPABILITY_ARCHITECTURE.md` still state the three NYC statements are "unaccepted `completion_review` artifacts". They were accepted 2026-08-14 (`c95488c`, `6f73dbe`). Corrected in `CLAUDE.md` and `PLANNING_STATUS.md` in this commit; the architecture doc's line 33 is left as a dated statement of what that direction did *not* do at the time. | commits `c95488c`, `6f73dbe` |
| F3 | **H** | ~2,700 lines of QC-side `NYC-QC-1` work exist unmerged and undocumented (section 2.2). No claim, no receipt, no mention in the workbench. Three weeks of silence since. | `git log main..nyc-crz-six-hearing-qc` in QC |
| F4 | **H** | The infrastructure-first path (Phase B) depends on a Project Meta "method-operation composition and evidence round-trip profile" that does not exist. The nearest owner, Project Meta **Plan #226** ("Shared typed capability composition core", Critical, In Progress), records its own shared core as *unmerged* on a `data_contracts` branch and DIGIMON's cutover as incomplete. Phase B therefore has an external blocker with no date. Nothing in this repo says so. | `~/code/project-meta/docs/plans/226_…md` "Gap" section |
| F5 | M | The 2026-08-13 product-integration map correctly diagnosed "the integration authority remained mostly a planning surface … examples became architecture … shared-schema debate displaced user continuity" — and the same day's reset added six more planning phases (A–F) before the user-visible journey. The repo's own diagnosis was not applied to the repo's own remedy. | `EVIDENCE_TO_ACTION_PRODUCT_INTEGRATION_MAP.md` §4 vs `ROADMAP.md` §"Adopted execution roadmap" |
| F6 | M | The Plan 242 guarded-decision seam (one QC move + one PT move through a common typed invocation and receipt, with refusal controls) already exists, is tested, and is essentially the Phase E "method-protocol seam proof" — but `PLANNING_STATUS.md` never mentions it, so its existence cannot shorten the roadmap. | `src/mixed_methods_workbench/guarded_decision/`, `docs/research/plan242/evidence/README.md` |
| F7 | M | `.claude/HANDOFF.md` / `handoff.yml` (2026-07-12) contradict every later authority ("documentation-only mode", "blocked on producer export slices", ADR 0004 order). An agent that reads handoffs first is misdirected. Marked superseded in this commit. | file dates |
| F8 | M | `CONCERNS.md` was last refreshed 2026-07-12; it predates NYC, the reset, Plan 242 and the QC branch; IDs `C037` and `C038` are each used twice. | `docs/CONCERNS.md` |
| F9 | M | `CAPABILITY_ADOPTION_MAP.md` pins are three weeks stale (section 2.3). Two pins (`grounded-research`, `open_web_retrieval`) do not resolve in the checkouts `~/workspace` routes to, which means the census inspected different clones than the ones an agent will find. | `git rev-list` / `cat-file` |
| F10 | L | `project-meta/PROJECT_GRAPH.json` says `has_remote: false` (there is a remote: `github.com-personal:BrianMills2718/projects-backup-mixed_methods_workbench-cdfee35f`) and lists `depends_on` without `data_contracts`, which `pyproject.toml` hard-requires. Owned by Project Meta; not changed here. | `PROJECT_GRAPH.json` |
| F11 | L | No venv, no `requirements` lock, and the Makefile assumed `mypy` on `PATH`; `README.md` does not say how to install. Fixed the Makefile; install steps are in 8.1. | reproduced |
| F12 | L | The long-term goal file (`plan/goals/2026-07-12-sota-or-beyond.md`) and `SOTA_EVIDENCE_SCORECARD.md` still frame the program as "SOTA or beyond in all areas", overall grade F, while the 2026-08-13 reset re-scoped the goal to one authentic policy MVP. Two north stars are in force. | both files |

## 4. Critique and open questions

1. **The repo optimises for not being wrong rather than for being useful.**
   Every artifact is careful to say what it does *not* license. That
   discipline is real and valuable (nothing here overclaims), but after
   eleven weeks the only thing a researcher can *see* is a method-chooser
   page and a P5 spine page built from other repos' fixtures. The
   product-integration map (F5) already said this.

2. **Three planning vocabularies coexist**: version ladder 0.0–2.x
   (`ROADMAP.md` §"Version Ladder"), phases A–G (same file), and Plan #5's
   unit graph. Plus Phase 0–3 of method decomposition, plus the T0/DEMO
   slices. Each has its own authorization language. A less capable agent
   cannot tell which one is live without this document.

3. **"Method-owned" is doing a lot of work.** The architecture says QC owns
   qualitative meaning and the workbench only orchestrates — yet the only
   authentic model run in the workbench (`NYC-EXTRACT-1`) is a
   workbench-local prompt+schema, and the QC-side `NYC-QC-1` canary is a
   *deductive single-code* pass, not the "Describe" the acceptance criteria
   demand (variation, contradictions, negative cases, reflexivity). The
   canary is a sensible first observation, but the brief must not let it be
   reported as `NYC-QC-1` complete.

4. **Is the `ExtractStructuredCandidates` refactor worth doing before the
   MVP is visible?** The reset's rationale is sound (don't grow a second
   case-specific vertical). But the refactor's own exit test is "the NYC path
   resolves and executes the generic action" — i.e. the NYC path is the proof.
   Finishing NYC-QC-1 and NYC-INTEGRATE-1 first does not create a second
   vertical; it completes the first, and gives the refactor a *second*
   consumer (QC's Describe export) instead of one. That is exactly the
   two-consumer rule the repo itself imposes on Data Contracts promotion.

5. **Questions only Brian can answer**
   - Is the 2026-08-14 acceptance the operative intent (finish NYC), or does
     the 08-13 reset still control (architecture first)? (Section 5.)
   - Should QC's `NYC-QC-1` deliver a real Describe over six hearings (the
     acceptance criteria), or is the one-code canary an acceptable first
     accepted artifact? Recommendation: canary first as a cheap gate, then a
     real Describe run in the same lane.
   - Does the "SOTA or beyond" goal file still govern, or is it archived by
     the reset? Recommendation: archive it as historical; one north star.

## 5. Recommendation (decision for Brian)

**Recommended: Path A — finish the NYC vertical now; do the shared-action
refactor after the journey is visible.**

Concretely: merge-up and run the existing QC branch (`NYC-QC-1`), consume its
strict export in the workbench, build `NYC-INTEGRATE-1` (joint display +
value-explicit appraisal), then re-enter the roadmap at Phase C/D with two
real consumers.

- Confidence: ~80 %. Brian's most recent concrete actions (accepting all
  three NYC items, and the QC lane being started the same day) point this
  way; the workspace-level rule "vertical work owns the critical path until
  the stable example is observed" points this way; and the alternative's key
  dependency (F4) is blocked outside this repo.
- Cost: the QC canary is ~91 calls of ~35 k chars on DeepSeek V4 Flash; QC's
  own 25-interview / 534 k-character pilot cost **$0.185** (its ledger). A
  full Describe over ~2,179 pages is plausibly $1–5. Set `--max-budget 10`.
- Risk: it contradicts the literal text of the 08-13 roadmap ("supersedes a
  direct jump … to NYC-QC-1"). If Brian confirms Path A, `ROADMAP.md`
  §"Adopted execution roadmap" must be edited to say Phase C/D follows, not
  precedes, the NYC MVP (one paragraph; task 8.4).

**Alternative: Path B — architecture first, as the 08-13 reset says.**
Design the `ExtractStructuredCandidates` action over Data Contracts +
`llm_client`, refactor `NYC-EXTRACT-1` through it, then resume QC-1.
Honest cost: Phase B's Project Meta profile does not exist (F4); an agent
would either wait on Plan #226 or write a "Workbench-subordinate" profile the
architecture doc explicitly forbids. Expect design-only output for weeks.
Choose B only if Brian believes a second case-specific extraction (QC's) will
be harder to unwind later than the current one — I do not think it will, and
the guarded-decision seam (F6) already shows QC and PT can share an
invocation shape without a shared schema.

Either way, the housekeeping in section 8 needs no decision.

## 6. Task brief for the next agent — Path A

Do these in order. Each step has a pass/fail check. Stop and report if a
check fails; do not "repair silently". Never present a model output as an
accepted finding; acceptance is Brian's, recorded like
`docs/research/nyc_crz_human_disposition.json`.

### A0. Environment (both repos)

```bash
# Workbench
cd ~/projects/mixed_methods_workbench
python3 -m venv .venv && .venv/bin/pip install -e ~/code/data-contracts -e ".[dev]"
.venv/bin/python -m pytest -q          # expect 161 passed
make check PYTHON=.venv/bin/python     # expect all gates green

# Qualitative Coding (has its own venv)
cd ~/code/qualitative_coding && .venv/bin/python -c "import pypdf, qc_clean; print('ok')"
```

Pass: both commands print the expected result. If `data_contracts` fails to
import, the install line above was skipped.

### A1. Claim the QC lane and bring the branch up to date

```bash
cd ~/code/qualitative_coding
# use the repo's own worktree/claim entry point (see its Makefile: make help)
git fetch origin
git worktree list                      # nyc-crz-six-hearing-qc should be present
cd worktrees/nyc-crz-six-hearing-qc
git rebase origin/main                 # 99 commits behind; resolve conflicts, keep NYC files
PYTHONPATH=. ../../.venv/bin/pytest tests/test_nyc_crz_corpus.py tests/test_nyc_crz_transcript.py tests/test_nyc_crz_describe.py -q
```

Pass: 22 tests pass after rebase. If rebase conflicts touch
`qc_clean/core/narrow_evidence.py` or `qc_clean/core/llm/`, stop and report —
the canary depends on those.

### A2. Re-materialise the frozen corpus (no model calls)

```bash
CACHE=~/projects/data/nyc_crz_pdf_cache      # any dir; PDFs are ~9 MB
W=~/projects/mixed_methods_workbench
PYTHONPATH=. ../../.venv/bin/python scripts/prepare_nyc_crz_corpus.py \
  --cache-dir $CACHE --workbench-repo $W --workbench-revision 739acf1 \
  --source-manifest-ref docs/research/evidence/nyc_crz_mvp_v1/source_manifest.json \
  --source-manifest-sha256 63dd0ec70180800e4678572570f97514849633eaa16284b706ea66615b0e63dc \
  --human-disposition-ref docs/research/nyc_crz_human_disposition.json \
  --human-disposition-sha256 847e57e94eabbb0fc57a6416cabfd6e9b6712f424cd992862e7f45902651c067 \
  --accepted-anchor-ref examples/fixtures/nyc_crz_evidence_slice/source_units.json \
  --accepted-anchor-sha256 974a95ec812e730c1cf74da03926eecd87674167e3f0137ae91ca1099fad881b \
  --output /tmp/corpus_receipt.json
PYTHONPATH=. ../../.venv/bin/python scripts/prepare_nyc_crz_units.py --cache-dir $CACHE --output /tmp/source_unit_receipt.json
```

Pass: the regenerated receipts are byte-identical to
`docs/benchmarks/nyc_crz_describe_v1_2026_08_14/{corpus_receipt,source_unit_receipt}.json`
(`cmp`). If a hearing PDF's SHA-256 no longer matches the manifest, the MTA
changed the file — **stop**; Plan #5's stop rule applies ("Stop if exact
source bytes … no longer verify").

### A3. Run the medical-access canary (first model spend)

```bash
PYTHONPATH=. ../../.venv/bin/python scripts/run_nyc_crz_medical_access_canary.py \
  --cache-dir $CACHE \
  --protocol docs/benchmarks/nyc_crz_describe_v1_2026_08_14/medical_access_protocol.json \
  --corpus-receipt docs/benchmarks/nyc_crz_describe_v1_2026_08_14/corpus_receipt.json \
  --source-unit-receipt docs/benchmarks/nyc_crz_describe_v1_2026_08_14/source_unit_receipt.json \
  --receipt-output docs/benchmarks/nyc_crz_describe_v1_2026_08_14/medical_access_canary_receipt.json \
  --coverage-checkpoint /tmp/nyc_cov.json --narrow-checkpoint /tmp/nyc_narrow.json \
  --model openrouter/deepseek/deepseek-v4-flash \
  --model-justification "default QC route; same family as NYC-EXTRACT-1" \
  --trace-id nyc-crz-qc1-medical-access-$(date -u +%Y%m%dT%H%M%SZ) \
  --max-budget 10 --budget-reservation 0.25
```

Pass: exit 0; the printed JSON has `status` not equal to an error state,
`page_unit_count == 2179`, and `positive_page_count >= 1` (the accepted
hearing-2022-08-25 page 82 passage must be among the positives — the receipt's
`accepted_anchor` block says whether it was recovered). Record the trace ID,
cost (query `~/projects/data/llm_observability.db`, never estimate), and
receipt SHA-256 in the QC commit message. This is an *observation*, not
`NYC-QC-1` complete.

### A4. Run the real QC Describe over the six hearings

This is the part the branch does not yet contain. Use QC's normal project
path rather than another bespoke module:

```bash
cd ~/code/qualitative_coding/worktrees/nyc-crz-six-hearing-qc
../../.venv/bin/python qc_cli.py project create --name "NYC CRZ six-hearing Describe" --methodology thematic
../../.venv/bin/python qc_cli.py project add-docs <project_id> $CACHE/hearing_2022_08_2*.pdf $CACHE/hearing_2022_08_3*.pdf
../../.venv/bin/python qc_cli.py project scope <project_id>      # set: six hearings, no prevalence, no causal claims
../../.venv/bin/python qc_cli.py project run <project_id> --exhaustive --max-budget 10 --budget-reservation 0.25 --review
```

Then satisfy `NYC-QC-1`'s three acceptance criteria from
`docs/plans/5_nyc_crz_qc_work_graph.json`:

- **AC1** every reported finding carries document / page / printed-line /
  quote / hash lineage — reuse `nyc_crz_transcript.py` atoms as the anchor
  universe; add one negative control that removes one hearing and shows the
  denominator receipt fails.
- **AC2** the reviewed artifact contains variation, contradictions or
  negative cases, reflexive decisions, and an explicit no-prevalence limit;
  add one negative control that a theme count cannot be promoted to
  prevalence (there is already a `_PROHIBITED_CLAIM_PATTERNS` gate in
  `nyc_crz_describe.py` to reuse).
- **AC3** a strict typed producer export the workbench can load with
  `StrictQCExport` (`src/mixed_methods_workbench/models.py:268`) — or, if that
  DEMO-C1 shape is too narrow, a new `qc_export_v1` model in QC plus a
  permissive `CompatibleQCView` in the workbench. Do not import `qc_clean`
  from the workbench.

Pass: QC focused tests green; export validates in the workbench venv with
`python -c "from mixed_methods_workbench.models import StrictQCExport; ..."`;
commit + push on the QC branch; open a PR (do not merge yet).

### A5. Hand the artifact to Brian for acceptance

Write the review packet the way `nyc_crz_human_disposition.json` was written:
exact commit, artifact SHA-256, the candidate findings with anchors, the
limits. Put it in the workbench under `docs/research/` and paste the
findings list into the chat — Brian does not open files. Update
`docs/plans/5_nyc_crz_mvp_work_graph.json` `NYC-QC-1.status` to
`completion_review`. **Stop here for Brian.**

### A6. After acceptance: `NYC-INTEGRATE-1`

Workbench-only. One page and one JSON route
(`/api/investigation/nyc-congestion-relief-zone` already exists — extend it,
do not add a parallel one) showing: question → frozen sources → accepted
prediction and concern → QC description → quantitative comparison → an
explicit integration statement (which strands agree, disagree, or are silent)
→ a value-explicit appraisal with human-owned weights → limits. Reuse the
`mist_trail_decision.py` appraisal shape. Pass criteria are the "MVP
acceptance boundary" list in `docs/plans/005_nyc_crz_mvp.md`. Then
`NYC-MVP-REVIEW-1` (Brian).

### Rules for this brief

- Work in a claimed linked worktree in each repo (`<repo>/worktrees/<branch>/`).
- Every model call goes through `llm_client` with `task=`, `trace_id=`,
  `max_budget=`; report real cost from the DB.
- Do not touch `process_tracing`, `theory-forge`, OntoCanon, DIGIMON, or Data
  Contracts. Plan #5 says they are not required for the MVP.
- Do not resume Phase 3 method decomposition, collision scoring, or the
  `ExtractStructuredCandidates` design. Those wait for Path A to finish.
- Do not delete or rewrite frozen receipts; a mismatch is a stop, not a fix.
- End every report with what a researcher can now *see* that they could not
  before.

## 7. Task brief — Path B (only if Brian chooses it)

1. Read `SYSTEM_GOAL_AND_CAPABILITY_ARCHITECTURE.md` §"The structured-candidate
   primitive" and `CAPABILITY_ADOPTION_MAP.md` §"Immediate decision".
2. Check Project Meta Plan #226 status; if the shared core is still unmerged,
   write the Phase B profile as a *Workbench-local candidate* explicitly
   labelled "to be superseded by Project Meta", and say so in
   `PLANNING_STATUS.md` — the alternative is indefinite waiting.
3. Design `ExtractStructuredCandidates` as a Data Contracts action descriptor
   + a workbench adapter over `llm_client`; settle only the seven items in
   `CAPABILITY_ADOPTION_MAP.md` §"Immediate decision".
4. Refactor `scripts/run_nyc_crz_extraction_canary.py` +
   `nyc_crz_evidence_slice.py` through it; add the "bypass is rejected" test.
   Prove the frozen receipt digests in `EXPECTED_FIXTURE_DIGESTS` are
   unchanged (no new model call).
5. Only then return to section 6.

## 8. Housekeeping (no decision needed; do in any order)

| # | Task | Done? |
| --- | --- | --- |
| 8.1 | Add install instructions to `README.md` (venv + `pip install -e ~/code/data-contracts -e ".[dev]"`) | done in this commit |
| 8.2 | `Makefile` `typecheck-demo` → `$(PYTHON) -m mypy` | done in this commit |
| 8.3 | Correct the "unaccepted" NYC statement in `CLAUDE.md` and `PLANNING_STATUS.md`; record the QC branch's existence | done in this commit |
| 8.4 | After Brian's decision: edit `ROADMAP.md` §"Adopted execution roadmap" so the phase order matches the decision | **open — needs section 5** |
| 8.5 | Mark `.claude/HANDOFF.md` and `handoff.yml` superseded | done in this commit |
| 8.6 | Remove stale worktree `worktrees/claude-method-decomposition-phase0` (branch kept) | done in this commit |
| 8.7 | Refresh `CONCERNS.md`: close/rewrite stale rows, fix duplicate `C037`/`C038` IDs, add rows for F1/F3/F4 | open |
| 8.8 | Re-pin `CAPABILITY_ADOPTION_MAP.md` "Evidence snapshot" to current HEADs, and resolve the two non-resolving pins | open |
| 8.9 | Ask Project Meta to set `has_remote: true` and add `data_contracts` to `depends_on` in `PROJECT_GRAPH.json` (owned there) | open |
| 8.10 | Archive `plan/goals/2026-07-12-sota-or-beyond.md` and `SOTA_EVIDENCE_SCORECARD.md` as historical, or re-scope them to the MVP — one north star | open (small decision; recommend archive) |
| 8.11 | Add a `PLANNING_STATUS.md` line acknowledging the Plan 242 guarded-decision seam as Phase E evidence | open |

## Appendix — verification log (2026-09-06)

- Workbench: `git log` (147 commits, 2026-06-25 → 2026-09-01); `git status`
  clean; `main == origin/main`.
- Fresh venv at `/tmp/…/mmw-venv`: `pip install -e ~/code/data-contracts -e ".[dev]"`
  ok; `pytest -q` → 161 passed; `make check PYTHON=<venv>` → all gates pass
  except `typecheck-demo` (bare `mypy`); `<venv>/bin/mypy --strict src/…` →
  0 issues; four focused `make test-*` targets pass (12 + 7 + 8 + 13).
- Dashboard: served on 127.0.0.1:8765; `/` 200 (73,831 B), `/api/catalog`
  200 (56,755 B); unknown routes 404.
- QC branch `nyc-crz-six-hearing-qc`: 5 ahead / 99 behind `main`; worktree
  clean; 22 tests pass with `PYTHONPATH=.`; no `*canary*receipt*` file exists
  in QC; workbench's own `canary_run_receipt.json` is the NYC-EXTRACT-1 trace.
- Hearing PDFs: a size-based `find` over `~/projects`, `~/code`, `~/.cache`,
  `/tmp` **timed out** (exit 124) — absence is *not* established; the QC
  script re-downloads and verifies, so it does not matter.
- `llm_observability.db` (31 GB): a `trace_id LIKE 'nyc%'` query was still
  running at write time. If it later shows calls, the canary ran without
  writing a receipt; the brief's A3 still applies (the script refuses to
  overwrite a receipt, so a missing receipt means re-run is safe).
- Coordination claims: none on this repo or the QC NYC lane.
- Producer HEADs and pin distances: section 2.3.
