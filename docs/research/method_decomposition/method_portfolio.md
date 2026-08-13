# Phase 2b method portfolio

Status: 14-method alternative adopted by Brian on 2026-08-13; Phase 3
decomposition authorized

Portfolio proposal version: `phase2b-proposal-0.3`

Adopted denominator: `phase2b-proposal-0.3` (`P01`–`P13`) plus `P14`, the
theory-testing Process Tracing alternative defined below. The proposal's
13-method recommendation and stop-rule analysis are retained as decision
history; Brian deliberately selected the non-substitutable 14-method
alternative. This approval authorizes Phase 3 decomposition only. It does not
authorize collisions, adjudication, coverage claims, shared infrastructure,
schema adoption, or product implementation.

## Decision boundary

This document will propose the denominator for Phase 3 decomposition and the
four later coverage measures in §11 of
`METHOD_DECOMPOSITION_HANDOFF.md` rev 5.1. It is a research proposal, not an
adopted portfolio. It does not begin Phase 3, run collisions, promote a
capability, adopt a production schema, change product code, or recommend shared
infrastructure.

The approved discovery format remains method phase → analytical move →
execution action. A portfolio decision selects named method variants to study;
it does not make their similarly named moves equivalent.

## Candidate sources and source limits

Candidate names will be generated from two independent classification
surfaces before individual methodology sources are frozen:

1. The repository's 73-label, 13-category
   [RAND-derived policy-research inventory](../../reference/RAND_POLICY_METHODS_TAXONOMY.md).
   Its provenance is a pinned historical project file whose underlying email
   is not preserved. It is therefore a discovery vocabulary, **not an official
   RAND taxonomy or methodological authority**. Official RAND method
   publications will be used separately where relevant.
2. HM Treasury's 2026
   [Magenta Book Annex A](https://www.gov.uk/government/publications/the-magenta-book/magenta-book-annex-a-analytical-methods-for-use-within-an-evaluation-html),
   which classifies theory-based, experimental and quasi-experimental,
   value-for-money, evidence-synthesis, and generic research methods used in
   government evaluation.

The [UK Government Futures Toolkit](https://www.gov.uk/government/publications/futures-toolkit-for-policy-makers-and-analysts/the-futures-toolkit-html),
the [U.S. GAO guide to designing evaluations](https://www.gao.gov/products/gao-12-208g),
the UK [Government Analysis Function techniques guide](https://analysisfunction.civilservice.gov.uk/policy-store/guide-to-gss-statistical-techniques-and-tools/),
the Palgrave [public-policy research-method classification](https://link.springer.com/chapter/10.1007/978-3-030-99724-3_4),
and the [NIH mixed-methods guide](https://obssr.od.nih.gov/research-resources/mixed-methods-research)
will be used as supplementary established classifications where the two seed
lists are thin. No catalog label will be treated as a sufficiently specified
method variant.

## Predeclared inclusion criteria

These criteria are frozen before the candidate list is scored. A later change
must be dated, justified, and applied again to every candidate rather than used
to rescue a favored method.

### Candidate-level gates

A candidate is eligible only if it passes all five gates:

1. **Catalog traceability.** A label or explicit synonym appears in at least
   one named classification above. The proposal records the exact label and
   any split, merge, or normalization.
2. **Distinct inferential leverage.** The frozen variant supports a conclusion
   that no already-selected variant supports under the same warrant. Merely
   using different software, data, or vocabulary does not count.
3. **Methodological source sufficiency.** At least one primary method source,
   consensus standard, or authoritative government methodology guide is
   available for Phase 3. A detector vocabulary, product documentation, or
   example application alone is insufficient.
4. **Real-policy prevalence proxy.** The method is either named by two
   independent established classifications/guides, or one cross-government
   guide describes its policy use and an independent method authority defines
   its conduct. This is a checkable proxy, not an invented frequency estimate.
5. **Decomposable frozen variant.** Population or case scope, evidence object,
   target conclusion, decisive design choices, and important exclusions can be
   stated now. A broad umbrella such as “machine learning,” “evaluation,” or
   “participatory methods” fails until split into a method variant.

### Portfolio-level balance tests

The eligible set is then minimized while satisfying all four tests:

1. **Evidence-form spread.** The portfolio must include methods whose central
   inputs or outputs exercise observed, reported, interpreted, derived,
   elicited, and simulated information. These origins describe provenance,
   not an evidence-strength ladder.
2. **Decision-role spread.** Collectively the methods must exercise population
   description or measurement, causal-effect estimation, mechanism or
   configurational explanation, prediction, evidence synthesis, option
   appraisal, uncertainty/foresight, and mixed-methods meta-inference.
3. **Family balance.** The portfolio must cover the following predeclared
   families: evidence synthesis; experimental causal estimation;
   quasi-experimental causal estimation; theory-based within-case or
   configurational inference; qualitative interpretation/theory construction;
   population measurement; computational text measurement; forecasting;
   simulation; decision under deep uncertainty/foresight; option appraisal;
   structured expert elicitation; and mixed-methods integration. Normally one
   variant represents a family. A second is allowed only when its inferential
   leverage is demonstrably non-substitutable.
4. **Implementation neutrality.** Existing repository support gives a candidate
   zero inclusion credit, and missing implementation gives it zero penalty.
   Selection happens before code mapping. This prevents the §11 denominator
   from being weighted toward workflows already built.

### Stop rule

Choose the smallest eligible set that covers every predeclared family and
decision role. Do not add a second near-duplicate merely to increase likely
reuse, and do not remove a hard-to-automate method to improve future coverage.

## Candidate application

The application below was made after the criteria were committed separately at
`a0038b8`. Evidence-form codes are `O` observed, `R` reported, `I`
interpreted, `D` derived, `E` elicited, and `S` simulated. They identify the
central information forms exercised by the method, not every possible input.

### Recommended compact portfolio

| ID | Frozen method variant | Family | Catalog trace and source basis | Inferential leverage | Evidence form | Decision role | Prevalence proxy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `P01` | Cochrane-style systematic review of randomized intervention effects, with pairwise meta-analysis only where estimands and measures are compatible | Evidence synthesis | RAND-derived `systematic review`/`meta-analysis`; Magenta A4; [Cochrane Handbook 6.5](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current) | A bounded synthesis of all eligible intervention studies; pooling remains conditional | `O,R,I,D` | Evidence synthesis | Named in both catalogs; Cochrane supplies a cross-domain conduct standard |
| `P02` | Individually randomized, two-arm, parallel superiority policy trial with a prespecified treatment-policy/ITT estimand | Experimental causal estimation | RAND-derived `RCT`; Magenta A2.1; [ICH E9/E9(R1)](https://www.ema.europa.eu/en/ich-e9-statistical-principles-clinical-trials-scientific-guideline) | Estimates the effect of randomized assignment for the frozen estimand | `O,D` | Causal-effect estimation | Both catalogs; Magenta documents policy-area use and ICH defines conduct |
| `P03` | Two-group, multi-period difference-in-differences evaluation with one adoption date, no staggered treatment, and an explicit parallel-trends/sensitivity design | Quasi-experimental causal estimation | RAND-derived `difference-in-differences`; Magenta A2.7; [2026 AEA practitioner's guide](https://www.aeaweb.org/articles?id=10.1257%2Fjel.20251650) | Estimates a policy effect from comparative trends without random assignment | `O,D` | Causal-effect estimation | Both catalogs; UK government guidance describes operational policy use |
| `P04` | Fuzzy-set QCA over a declared 10–50-case population, with substantive calibration, necessity/sufficiency analysis, explicit remainder policy, and return to cases | Configurational comparative inference | Magenta A1.1; RAND-derived `causal inference` is split; [Schneider and Wagemann](https://www.cambridge.org/core/books/settheoretic-methods-for-the-social-sciences/236C162386C1188966FE269D625CA289) covers calibration, truth tables, fit, limited diversity, and logical remainders | Identifies necessary or sufficient configurations and equifinality, not temporal mechanisms or marginal effects | `O,R,I,D` | Configurational explanation | Magenta describes government-evaluation use; an independent comprehensive method source defines the frozen conduct |
| `P05` | Constructivist grounded theory with initial coding, constant comparison, memoing, theoretical sampling, category-adequacy appraisal, and reflexive integration | Qualitative interpretation and theory construction | RAND-derived `grounded theory`; [public-policy research-method classification](https://link.springer.com/chapter/10.1007/978-3-030-99724-3_4); [Charmaz, 3rd ed.](https://uk.sagepub.com/en-gb/mst/constructing-grounded-theory/book255601) | Builds a bounded interpretive theory through iterative comparison and theoretically directed sampling | `O,R,I` | Theory construction | The independent public-policy methods chapter names grounded theory; Charmaz defines the selected constructivist variant |
| `P06` | Cross-sectional probability-sample survey estimating a named population prevalence, with a defined frame, design weights, nonresponse treatment, uncertainty, and error reporting | Population measurement | RAND-derived `survey analysis`/`sampling strategy`; Magenta A5.3; [OMB statistical-survey standards](https://nces.ed.gov/sites/default/files/nces/document/2024/10/standards_stat_surveys.pdf) | Estimates a population quantity with design-based uncertainty; it does not identify a policy effect | `O,R,D` | Description and measurement | Both catalogs; Magenta says surveys are widely used and OMB supplies official standards |
| `P07` | Supervised quantitative-text prevalence measurement using a human-coded target, document-grouped held-out evaluation, simple baselines, uncertainty, and item-level error analysis | Computational text measurement | RAND-derived `text-as-data`/`computational text analysis`; UK Government Analysis Function [text-analysis/classification guide](https://analysisfunction.civilservice.gov.uk/policy-store/guide-to-gss-statistical-techniques-and-tools/); [Grimmer and Stewart](https://doi.org/10.1093/pan/mps028) | Measures the prevalence of a declared textual construct at corpus level; classifier accuracy is not construct validity | `O,R,I,D` | Description and measurement | A cross-government analysis guide names the technique family; an independent field review constrains conduct and validation |
| `P08` | Operational probabilistic time-series forecast for a named numerical target and horizon, evaluated by rolling origin against naive/seasonal baselines and monitored without rewriting historical forecasts | Forecasting | RAND-derived `forecasting`/`time series analysis`; Futures Toolkit forecasting family; [Hyndman and Athanasopoulos, 3rd ed.](https://otexts.com/fpp3/) | Predicts a future quantity under a time-respecting information set; prediction is not causal explanation | `O,D` | Prediction | Independent catalog/toolkit recognition plus a mature forecasting method source |
| `P09` | Agent-based policy simulation with an ODD-described model, explicit purpose and abstraction boundary, verified implementation, frozen stochastic experiment, replication, and sensitivity analysis | Simulation/model-based exploration | RAND-derived `agent-based modeling`; Magenta simulation family; [ODD 2020](https://www.jasss.org/23/2/7.html) | Establishes what the declared model generates under specified configurations; it does not confirm real-world effects | `D,S` | Model exploration | Both catalogs; ODD is a mature cross-domain description standard |
| `P10` | Robust Decision Making under deep uncertainty, using decision framing, many plausible futures, vulnerability/scenario discovery, trade-off analysis, and adaptive strategy revision | Decision under deep uncertainty and foresight | RAND-derived `robust decision making`; Futures Toolkit policy stress-testing; [RAND RDM methodology](https://www.rand.org/content/dam/rand/pubs/research_reports/RR3000/RR3017/RAND_RR3017.pdf) | Finds vulnerabilities and comparatively robust/adaptive strategies without pretending to predict one best future | `D,E,S` | Foresight and strategy design | RAND and UK-government classifications plus an official RAND method source |
| `P11` | Green Book 2026 staged policy-option appraisal: objectives and critical success factors; standard Options Framework Filter longlisting; expert-facilitated MCDA only if the standard route does not resolve complex technical trade-offs; shortlist appraisal by CBA or CEA with unmonetized impacts explicit; accountable recommendation and decision | Option appraisal | RAND-derived `decision analysis`/`MCDA`; Magenta A3; [Green Book 2026](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026) and [2024 MCDA supplement](https://www.gov.uk/government/publications/green-book-supplementary-guidance-use-of-multi-criteria-decision-analysis) | Filters viable options, compares shortlisted social costs, benefits, risks, and unmonetized impacts, then advises an accountable decision-maker; MCDA does not replace shortlist CBA/CEA and simple MCA weighting/scoring is excluded | `O,R,I,D,E` | Option appraisal | Both catalogs and current cross-government appraisal guidance |
| `P12` | Three-round anonymous policy Delphi with purposive expert-panel construction, controlled feedback, stability/disagreement analysis, and no rule that consensus equals truth | Structured expert elicitation | RAND-derived `Delphi method`; Futures Toolkit Delphi; [RAND Delphi guidance](https://www.rand.org/pubs/tools/TLA3082-1.html) | Elicits and stabilizes expert judgments or maps disagreement under incomplete information | `R,I,D,E` | Uncertainty characterization and prioritization | Both catalogs; official RAND guidance documents broad policy use |
| `P13` | Convergent mixed-methods policy evaluation with independently warranted qualitative and quantitative strands, explicit merge in a joint display, divergence disposition, and bounded meta-inference | Mixed-methods integration | The 2026 [Magenta Book](https://www.gov.uk/government/publications/the-magenta-book/magenta-book-central-government-guidance-on-evaluation-html) says most evaluation designs combine qualitative and quantitative methods; [NIH best practices](https://obssr.od.nih.gov/research-resources/mixed-methods-research) classify and define convergent integration | Produces a meta-inference from purposeful integration while preserving each strand's warrant and contradictions | `O,R,I,D` | Integration and meta-inference | A cross-government guide describes routine mixed-method evaluation use; the independent NIH authority defines the convergent variant |

The proposal recommendation was therefore **13 named variants across 13
families**. The original 14-member draft also selected theory-testing Process
Tracing. That exceeded the frozen minimum stop rule: its decision-role and family tests said
“mechanism or configurational,” so `P04` already satisfied both. Process
Tracing remained an eligible, non-substitutable method. Brian's later approval
selected that explicit alternative despite its one-method denominator cost.

### Adopted fourteenth variant

| ID | Frozen method variant | Family | Source basis to freeze in Phase 3 | Inferential leverage | Evidence form | Decision role |
| --- | --- | --- | --- | --- | --- | --- |
| `P14` | Theory-testing Process Tracing in one bounded case, with frozen rival explanations, observable implications, explicit searches for present and absent evidence, and qualitative-Bayesian diagnostic comparison | Theory-based within-case causal inference | Bennett and Checkel (2015), *Process Tracing: From Metaphor to Analytic Tool*; Phase 3 must pin chapters/sections and corroborating conduct guidance | Discriminates among rival within-case causal explanations and assesses mechanism evidence; it does not estimate an average effect or identify cross-case necessity/sufficiency | `O,R,I,D` | Mechanism explanation |

Seven variants overlap the accepted-format pilots or hostile stress sample.
That does not give them implementation credit: those artifacts established
that the discovery instrument can represent the variants, not that the
workbench implements them or that their Phase 3 decomposition is complete.

### Balance check

| Required spread | Portfolio coverage |
| --- | --- |
| Observed information | `P01`–`P09`, `P11`, `P13`, `P14` |
| Reported information | `P01`, `P04`–`P07`, `P11`–`P14` |
| Interpreted information | `P01`, `P04`, `P05`, `P07`, `P11`–`P14` |
| Derived information | All except the central interpretive core of `P05`; even there, runtime actions may derive indexes without owning the interpretation |
| Elicited information | `P10`–`P12` |
| Simulated information | `P09`, `P10` |
| Description/measurement | `P06`, `P07` |
| Causal effect | `P02`, `P03` |
| Mechanism/configuration | `P04`, `P14` |
| Prediction | `P08` |
| Synthesis | `P01` |
| Appraisal/foresight | `P10`–`P12` |
| Mixed-methods meta-inference | `P13` |

The set is deliberately not weighted toward current implementation. It includes
human-led interpretation and elicitation, deterministic estimation and
forecasting, generated model evidence, and genuine qualitative–quantitative
integration even though these have sharply different present software status.

### Candidate gate matrix

`G1`–`G5` correspond exactly to the five frozen candidate-level gates above.
Every selected row passes every gate; the evidence cell names the check rather
than replacing the detailed variant table.

| ID | G1 catalog trace | G2 distinct leverage | G3 method authority | G4 prevalence proxy | G5 frozen variant |
| --- | --- | --- | --- | --- | --- |
| `P01` | Pass — RAND + Magenta A4 | Pass — eligible-study synthesis | Pass — Cochrane 6.5 | Pass — two classifications | Pass — randomized-effect review; conditional pairwise pooling |
| `P02` | Pass — RAND + Magenta A2.1 | Pass — randomized assignment effect | Pass — ICH E9/E9(R1) | Pass — two classifications | Pass — individual two-arm superiority; treatment-policy/ITT estimand |
| `P03` | Pass — RAND + Magenta A2.7 | Pass — comparative-trend effect | Pass — AEA guide | Pass — two classifications | Pass — one adoption date; no staggered treatment |
| `P04` | Pass — Magenta A1.1 + RAND `causal inference` split | Pass — necessary/sufficient configurations | Pass — Schneider and Wagemann | Pass — government guide + independent authority | Pass — fuzzy sets; 10–50 cases; explicit remainder policy |
| `P05` | Pass — RAND `grounded theory` + public-policy methods chapter | Pass — iteratively constructed interpretive theory | Pass — Charmaz 3rd ed. | Pass — two independent classifications/guides | Pass — constructivist variant with theoretical sampling |
| `P06` | Pass — RAND + Magenta A5.3 | Pass — design-based population prevalence | Pass — OMB standards | Pass — two classifications | Pass — cross-sectional probability sample |
| `P07` | Pass — RAND + Government Analysis Function | Pass — corpus-level textual-construct prevalence | Pass — Grimmer and Stewart | Pass — cross-government guide + independent authority | Pass — supervised, grouped holdout, human-coded target |
| `P08` | Pass — RAND + Futures Toolkit | Pass — future quantity prediction | Pass — Hyndman and Athanasopoulos | Pass — two classifications/guides | Pass — named target/horizon; rolling origin |
| `P09` | Pass — RAND + Magenta simulation | Pass — generated model behavior | Pass — ODD 2020 | Pass — two classifications | Pass — ABM; frozen stochastic experiment |
| `P10` | Pass — RAND + Futures Toolkit | Pass — vulnerability/robust strategy | Pass — RAND RDM | Pass — two classifications | Pass — many plausible futures; adaptive strategy |
| `P11` | Pass — RAND + Magenta A3 | Pass — staged public option appraisal | Pass — Green Book 2026 + 2024 supplement | Pass — two classifications | Pass — MCDA longlist only; CBA/CEA shortlist |
| `P12` | Pass — RAND + Futures Toolkit | Pass — structured expert judgment/disagreement | Pass — RAND Delphi | Pass — two classifications | Pass — anonymous three-round policy Delphi |
| `P13` | Pass — Magenta + NIH | Pass — integrated meta-inference | Pass — NIH best practices | Pass — cross-government guide + independent authority | Pass — convergent design; independent strands and explicit merge |
| `P14` | Pass — accepted mechanism-inclusive expansion | Pass — within-case rival discrimination is non-substitutable for fsQCA | Pass — Bennett and Checkel 2015 | Pass — retained eligible alternative from the reviewed proposal | Pass — one bounded case; frozen rivals and qualitative-Bayesian diagnostic comparison |

## Exclusions and denominator consequences

Excluded labels are not declared unimportant. They are outside this proposed
denominator for the stated reason and may be proposed in a later, separately
versioned portfolio.

| Excluded family or labels | Disposition and reason | Effect of exclusion on later §11 claims |
| --- | --- | --- |
| `policy evaluation`, `program evaluation`, `impact assessment`, `outcome`, `process`, `formative`, `summative` | Purposes or umbrellas, not frozen methods. Their relevant roles are exercised by named designs above. | Prevents inflating method counts with labels that would decompose into overlapping component methods; narrows claims to the selected variants. |
| Generic `regression`, `causal inference`, `machine learning`, `NLP`, `validation`, `uncertainty analysis`, `sensitivity analysis` | Operations or technique families without a target estimand, evidence object, and warrant. | Makes all denominators smaller but more falsifiable; no coverage claim may extend to these umbrellas. |
| Propensity-score matching, instrumental variables, regression discontinuity, synthetic control, interrupted time series, staggered-adoption DiD | Eligible quasi-experimental variants, but `P03` is the one minimal representative. They are not aliases for `P03`. | Makes semantic and complete-method coverage easier within quasi-experimental work and prevents any claim of general quasi-experimental coverage. |
| Realist evaluation/synthesis, contribution analysis | Eligible theory-based variants outside the adopted denominator. Theory-testing Process Tracing is now `P14`; the other variants remain non-equivalent exclusions. | Leaves context–mechanism–outcome synthesis and contribution-claim interiors explicitly uncovered. |
| Ethnography, focus groups, interviews, observations, case study, generic content analysis | Some are data-collection modes and some are broad designs. `P05` freezes one full qualitative analytic method; these remain non-equivalent. | Makes qualitative coverage easier and bars a claim that serving grounded theory serves ethnography, case study, or generic qualitative analysis. |
| Rapid evidence assessment, literature review, knowledge synthesis, qualitative evidence synthesis, realist synthesis, network meta-analysis | `P01` freezes one high-integrity randomized-effect review variant. Faster, qualitative, realist, and network variants have different search, synthesis, and conclusion rules. | Makes synthesis coverage materially easier; future results apply only to `P01`. |
| Microsimulation, system dynamics, discrete-event simulation | `P09` is the single simulation representative; model ontology and inference differ across these variants. | Makes simulation coverage easier and prohibits generalizing ABM support to other simulation families. |
| Scenario planning, horizon scanning, trend analysis, backcasting, wargaming, tabletop exercises, serious games | `P10` and `P12` cover model-assisted deep uncertainty and elicitation. Participatory/non-model foresight and gaming are excluded by minimality, not merged. | Makes foresight and unattended-execution coverage easier, because facilitation-heavy workflows are absent. |
| Social-network analysis, GIS/spatial analysis | Eligible specialist relational/spatial families, but not required by the predeclared minimum decision-role spread. | Makes raw-shell, semantic, and complete-method coverage easier; no later claim may extend to relational or spatial inference. |
| Legal-authority analysis plus institutional implementation mapping | Important policy-analysis composition, but the source freeze does not yet have a cross-jurisdiction conduct authority sufficient for the candidate-level source gate. | Makes policy-appraisal coverage easier and leaves lawfulness and institutional mandate/capacity explicitly outside the denominator. |
| Stand-alone cost-benefit or cost-effectiveness analysis | Included as the shortlist-analysis stage inside `P11`; optional MCDA is a distinct longlist stage, not a substitute. Phase 3 must keep monetized welfare, unmonetized impacts, uncertainty, recommendation, and accountable decision separate. | Avoids double-counting one staged appraisal while keeping its required semantic interiors in the complete-coverage test. |
| Sequential exploratory, sequential explanatory, embedded, and multiphase mixed-methods designs | NIH-recognized variants, but `P13` freezes only convergent integration. | Makes integration coverage substantially easier; coverage of `P13` cannot be generalized to other timing or priority structures. |

## Expected effect on §11 denominators

No Phase 6 numerator or percentage can be calculated until the approved
variants are decomposed and mapped. The directional effects are nevertheless
clear:

| §11 measure | Denominator under this proposal | Expected difficulty compared with an implementation-weighted portfolio |
| --- | --- | --- |
| `raw_shell_reuse` | All decomposed steps from these 14 variants, using the approved portfolio version beside the result | Harder: the set adds distinct evidence, simulation, elicitation, integration, and method-owned judgment shapes. Stable custody/version/review mechanics may recur, but broad verb similarity cannot count. |
| `semantic_implementation_coverage` | Required steps reported separately for each named variant | Harder: an existing shell earns no credit for a missing method-owned interior, and narrow variants prevent “supports surveys/ML/evaluation” overclaims. |
| `complete_method_coverage` | Fourteen equally weighted method variants | Materially harder: one missing required shell or semantic interior leaves that method uncovered, regardless of how many other methods are complete. |
| `unattended_execution_coverage` | Required operations across the same 14 variants, with any human in `actor_chain` treated as attended under §11 | Harder and more honest: grounded theory, QCA calibration, Process Tracing diagnostic judgments, appraisal, Delphi, systematic-review judgments, and mixed-methods reconciliation contain irreducible human authority; deterministic estimation, forecasting, and simulation do not offset them by method weight. |

The exclusions make all four measures easier than a universal policy-method
claim would be. The effect is largest for complete-method and unattended
coverage because facilitation-heavy foresight/gaming, legal judgment, other
mixed-methods timings, and specialist spatial/network workflows are outside the
set. Every Phase 6 result must therefore say
`portfolio=phase2b-proposal-0.3+P14` and repeat these
scope limits.

## Important alternative and tradeoff

Brian selected the **14-variant mechanism-inclusive
portfolio** that adds theory-testing Process Tracing in one bounded case, with
frozen rivals, observable implications, and qualitative-Bayesian diagnostic
comparison ([Bennett and Checkel](https://www.cambridge.org/core/books/process-tracing/4BCF053A25474F6B8A9EE5F46C20A7AE)). It would preserve both within-case
mechanism discrimination and cross-case configurational inference. The tradeoff
is that it knowingly relaxes the frozen minimum stop rule to buy a second,
non-substitutable theory-based warrant before any Phase 3 collision result
shows that the added decomposition changes a decision. That tradeoff is now an
accepted denominator property, not an unresolved alternative.

A later **17-variant breadth-first portfolio** would add Process Tracing plus:

- realist synthesis of complex interventions;
- policy stress-testing against qualitatively constructed scenarios; and
- social-network analysis of a bounded policy-actor network.

The 17-member set tests within-case mechanism discrimination,
context–mechanism synthesis, facilitation-led foresight, and relational evidence
earlier. It is more representative of the whole RAND-derived inventory, but it
adds four source freezes—about 31% more equally weighted methods—before the
current 13-family denominator has produced any collision evidence. It makes
complete-method and unattended coverage harder for substantively legitimate
reasons that the predeclared minimum does not require. Before Brian's decision,
the proposal recommended 13 variants and presented 14 as the important human
alternative. The remaining three are still later breadth candidates.

## Human approval disposition

Brian approved the 14-method alternative on 2026-08-13: exactly
`phase2b-proposal-0.3` (`P01`–`P13`) plus `P14` theory-testing Process Tracing.

Approval means Phase 3 may decompose these variants using the accepted
three-level discovery format and the cited methodology sources. Approval does
not accept any capability collision, implementation status, automation claim,
coverage result, schema, infrastructure design, product change, or promotion.

The 13-method recommendation and 17-member breadth set remain decision history.
Neither is the active denominator. Phase 3 may proceed under the coordination
graph; Phases 4–6 and implementation remain separately unauthorized.

## Source verification note

Links above were checked on 2026-08-13 against the named publisher or issuing
institution. The sources serve different roles:

- the repository's RAND-derived inventory generates labels but supplies no
  methodological warrant;
- Magenta, GAO, the Futures Toolkit, the Government Analysis Function,
  Palgrave's public-policy methods classification, and NIH establish
  policy/research-design families and real-use context;
- Cochrane, ICH, Schneider and Wagemann, Charmaz, OMB, Grimmer and Stewart,
  Hyndman and Athanasopoulos, ODD, RAND RDM/Delphi, the Green Book 2026, and the
  2024 MCDA supplement define or constrain the frozen variants.

Phase 3 must pin exact editions and sections in each method frame. This proposal
does not replace that source-freeze obligation. In particular, the frames must
resolve four scope cautions retained from review: do not treat placeholder
records as operations; distinguish reported/observed inputs from the derived
synthesis in `P01`; add an experiment-design authority beyond ODD's model-
description role for `P09`; and justify which ICH clinical-trial rules transfer
to the policy-trial scope in `P02`.
