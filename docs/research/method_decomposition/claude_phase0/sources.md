# Phase 0 — Frozen Authoritative Sources

Status: `independent_candidate` — produced without inspecting the frozen
Codex candidate (`ac27ab2`) per rev 5.1 §0.1. Frozen before the §8.2
ideal-to-code mapping was performed, per §8.3 Task 2 and §5.0a guard 1.

Each source below was independently verified to exist (web search against
publisher/DOI/journal records) and to actually specify method steps, not
merely discuss the method. All are used as evidence_basis citations in
`step_ledger.yaml`.

Source freezes are about the literature and are unaffected by repository
drift, but the *code* citations threaded through this document (e.g. the
in-repo citations found for grounded theory, process tracing, and CPT) were
read at the repository states recorded in `repository_snapshots.yaml`. See
that file for which repositories' states are confirmed vs. presumed vs.
confirmed-drifted since inspection — notably `process_tracing`.

---

## 1. QC fixed-corpus grounded theory (`qc_grounded_theory`)

**Primary:** Corbin, J. M., & Strauss, A. L. (2015). *Basics of Qualitative
Research: Techniques and Procedures for Developing Grounded Theory* (4th
ed.). Thousand Oaks, CA: Sage. — Verified to exist (SAGE, Amazon, Google
Books all list the 4th ed., 2015, ISBN 9781412997461). Specifies concrete
steps: open coding, categories with properties/dimensions, axial coding via
the conditions→actions/interactions→consequences paradigm, memo-writing
(chs. 5, 7-9), and theoretical sampling/adequacy (ch. 6, 12). This is the
edition-specific citation; step structure differs from the 3rd (1998) and
earlier Glaser & Strauss (1967) formulations, so edition is load-bearing.

**Corroborating:** Charmaz, K. (2014). *Constructing Grounded Theory: A
Practical Guide Through Qualitative Analysis* (2nd ed.). Los Angeles: Sage.
— Verified to exist (SAGE, Google Books, multiple citing works confirm 2nd
ed. 2014). Specifies constant comparison, memo-writing as a core analytic
technique (ch. 7), and explicitly distinguishes theoretical sampling/
saturation from convenience or fixed-corpus sampling (ch. 5) — the exact
distinction QC's own docs invoke ("fixed-corpus adequacy is not theoretical
saturation").

**Secondary, cited in-repo and used only for the negative-case-analysis
step:** Lincoln, Y. S., & Guba, E. G. (1985). *Naturalistic Inquiry*.
Beverly Hills, CA: Sage. — Not independently re-verified by web search
(pre-internet-era text of extremely high citation currency); accepted
because it is cited directly and specifically in-repo
(`qc_clean/core/pipeline/stages/negative_case.py:6-7,166`, prompt text
literally reads "(Lincoln & Guba, 1985)"), satisfying §7.2's preference for
verifiable, specific, non-composite citation.

**Not used, considered and rejected:** Glaser, B. G., & Strauss, A. L.
(1967). *The Discovery of Grounded Theory*. — the original text is
frequently invoked generically but the implemented pipeline explicitly
labels its axial-coding paradigm model as Strauss/Corbin's, not Glaser's
constant-comparison-only variant, so using Glaser 1967 as primary would
misattribute the paradigm-model steps.

---

## 2. Process Tracing core single-case rival-explanation workflow
(`pt_core_rival_explanation`)

**Primary:** Bennett, A., & Checkel, J. T. (Eds.). (2015). *Process
Tracing: From Metaphor to Analytic Tool*. Cambridge: Cambridge University
Press. — Verified (Cambridge Core, Amazon, ResearchGate; 342 pp.,
"Strategies for Social Inquiry" series). Cited directly in-repo
(`CLAUDE.md:33`, `docs/WHITEPAPER_optimal_automated_process_tracing.md`
bibliography, `docs/METHODOLOGY.md:40`). Specifies rival-explanation
identification, diagnostic-evidence testing, and causal-mechanism tracing
as distinct steps (ch. 1, editors' introduction).

**Corroborating:** Fairfield, T., & Charman, A. E. (2017). Explicit
Bayesian Analysis for Process Tracing: Guidelines, Opportunities, and
Caveats. *Political Analysis*, 25(3), 363-380. — Verified (Cambridge Core,
SSRN, LSE Research Online; won APSA's Sage Paper Award). Cited directly
in-repo (`docs/PROJECT_THEORY_AND_GOALS.md`, `docs/METHODOLOGY.md:40`,
`docs/WHITEPAPER...md`). Specifies explicit likelihood elicitation and
Bayesian updating steps — the source for the deterministic `pt/bayesian.py`
posterior computation.

**Named but not selected as primary/corroborating:** Van Evera, S. (1997).
*Guide to Methods for Students of Political Science*. Ithaca: Cornell
University Press. Well-established as the source of the four-test
diagnostic typology (hoop, smoking-gun, doubly-decisive, straw-in-the-wind)
referenced throughout the repo (`CLAUDE.md:33`, `docs/METHODOLOGY.md:40`).
Not independently re-verified by web search this pass (very high-currency,
frequently-reprinted text); treated as tertiary corroboration for the
diagnostic-typology vocabulary only, not as one of the two frozen sources.

**Explicitly not cited in-repo and not used:** Beach, D., & Pedersen, K. S.
— confirmed absent from the codebase and docs by direct grep (agent
finding). Not used as a source here to avoid attributing a variant the
implementation does not claim.

---

## 3. Process Tracing source-acquisition companion workflow
(`pt_source_acquisition`)

Per rev 5.1 §8, this workflow is expected to be "mixed; expect substantial
`methodological_support` and `runtime_delivery`." No methodology source is
cited in-repo for this workflow at all (confirmed by the inspecting agent's
grep across all acquisition-family files for historiography/archival/
source-criticism/systematic-review terms — zero hits). The sources below
are independently frozen from the discipline, not inherited from the repo.

**Primary:** Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I.,
Hoffmann, T. C., Mulrow, C. D., et al. (2021). The PRISMA 2020 statement:
An updated guideline for reporting systematic reviews. *BMJ*, 372, n71. —
Verified (BMJ, PRISMA statement site, Johns Hopkins repository). This is a
reporting *standard*, not a qualitative source-criticism text, but it is
the closest verifiable, step-specifying authority for "search → screen →
admit" as a governed sequence (items 6-9: information sources, search
strategy, selection process, data items), matching the acquire/screen/admit
shape actually implemented.

**Corroborating:** Howell, M. C., & Prevenier, W. (2001). *From Reliable
Sources: An Introduction to Historical Methods*. Ithaca: Cornell University
Press. — Verified (Cornell University Press, Amazon, JSTOR/Project MUSE
reviews). Specifies external/internal source criticism — authentication,
provenance, duplication/derivation checking — matching the
`provenance_fit`/`duplication_assessment`/`authenticity_notes` fields
actually present in the code's `ReviewCriteria` model.

**Finding to flag:** because neither source is cited in-repo, this
workflow's `evidence_basis` values rest on an externally-frozen judgment
that these are the closest applicable authorities, not on the
implementers' own stated intent. This is recorded honestly in
`reality_check.md` rather than treated as a verification failure of the
sources themselves (both sources independently verified to exist and to
specify steps).

---

## 4. Theory Forge generic compile/apply workflow (`theory_forge_compile_apply`)

**No methodology source frozen.** Per rev 5.1 §8 explicit instruction:
"expect largely `runtime_delivery`; do not force it against a methodology
source." Confirmed from code: this workflow (paper → schema → agent-driven
codegen → pytest-gated verification → run) has no external methodological
standard governing "how to compile a scientific theory into executable
code" that could be verified as authoritative and step-specifying. All
operations in this workflow are recorded in the ledger with
`operation_kind: runtime_delivery` (two borderline exceptions — theory
identification and formalization — are flagged in `reality_check.md` as
involving genuine interpretive judgment without an authoritative
methodological source, and are conservatively left `runtime_delivery`
rather than manufacturing a source to reclassify them `analytic`). This
workflow therefore contributes **zero** to the abort-gate numerator and
denominator, by design, not by exclusion-gaming (§5.0a guard 4 checked:
no authoritative source was found that specifies these steps, so none was
suppressed).

---

## 5. Theory Forge CPT/Choices13k prediction workflow
(`theory_forge_cpt_choices13k`)

**Primary:** Tversky, A., & Kahneman, D. (1992). Advances in prospect
theory: Cumulative representation of uncertainty. *Journal of Risk and
Uncertainty*, 5, 297-323. DOI: 10.1007/BF00122574. — Verified (Springer
Link, SciRP, EconPapers; ~15,000+ citations). Specifies the rank-dependent
value function, one-parameter probability-weighting transform, and
cumulative decision-weight construction implemented verbatim in
`cumulative_prospect.py`, including population parameter values (α=0.88,
β=0.88, λ=2.25, γ_gains=0.61, γ_losses=0.69) directly attributable to this
paper's reported estimates.

**Corroborating:** Peterson, J. C., Bourgin, D. D., Agrawal, M., Reichman,
D., & Griffiths, T. L. (2021). Using large-scale experiments and machine
learning to discover theories of human decision-making. *Science*, 372,
1209-1214. — Verified (Science/AAAS DOI 10.1126/science.abe2629,
Semantic Scholar, Princeton CoCoSci). This is the paper that produced the
Choices13k dataset the workflow evaluates against, and specifies the
majority-choice / classification-accuracy comparison paradigm for
benchmarking psychological theories that `choices13k.py`'s scoring
(`_paired_summary`) implements.

**Finding to flag:** the repository correctly and repeatedly cites
Tversky & Kahneman (1992) — including embedding the DOI in every output
artifact — but **never cites Peterson et al. (2021)** anywhere in code,
schemas, or docs (confirmed by the inspecting agent via exhaustive grep for
author names and the DOI prefix). It references only the dataset's GitHub
repository and a pinned commit hash, treating Choices13k as pinned *data*
rather than citing the *paper* that produced it. This is recorded as a
citation-completeness finding in `reality_check.md`, not as a failure to
verify Peterson et al. (2021) itself, which independently verified as
existing and specifying exactly this benchmarking approach.

---

## 6. Mist Trail policy-appraisal vertical (`mist_trail_policy_appraisal`)

**Primary:** Dodgson, J. S., Spackman, M., Pearman, A., & Phillips, L. D.
(2009). *Multi-Criteria Analysis: A Manual*. London: Department for
Communities and Local Government. — Verified (LSE Research Online
eprint 12761, ResearchGate, UK government publication index). Specifies
the concrete option-appraisal sequence Mist Trail's own plan document says
it borrows from: establish decision context → identify options → identify
objectives/criteria → score options against criteria → assign relative
weights → combine/examine results → sensitivity analysis → conclusion.

**Corroborating:** Moberg, J., Oxman, A. D., Rosenbaum, S., Schünemann,
H. J., Guyatt, G., Flottorp, S., et al. (2018). The GRADE Evidence to
Decision (EtD) framework for health system and public health decisions.
*Health Research Policy and Systems*, 16, 45. — Verified (BioMed Central /
Springer, DOI 10.1186/s12961-018-0320-2). Chosen over the clinical-guideline
EtD variant (Alonso-Coello et al., 2016, *BMJ*) because it targets
system/public-health *policy* decisions rather than individual clinical
recommendations, closer to Mist Trail's NPS-policy context. Specifies
separating the problem, evidence on effects/values/resources, and judgment
from the final decision — matching the plan document's explicit intent to
keep evidence, values, and conclusion inspectably separate.

**Explicitly not implemented, per the vertical's own design intent (not a
gap):** full MCDA additive weighted scoring, formal GRADE certainty
rating, and Robust Decision Making — the plan document states this
directly (`docs/plans/mist_trail_policy_decision_vertical.md:31-34`).
