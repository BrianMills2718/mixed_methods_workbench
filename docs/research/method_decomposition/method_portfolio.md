# Phase 2b method portfolio proposal

Status: proposal for human approval; Phase 3 not authorized

Portfolio proposal version: `phase2b-proposal-0.2`

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
| `P04` | Theory-testing Process Tracing in one bounded case, with frozen rivals, observable implications, and qualitative-Bayesian diagnostic comparison | Theory-based within-case inference | Magenta A1.3; RAND-derived `case study` is split rather than treated as equivalent; [Bennett and Checkel](https://www.cambridge.org/core/books/process-tracing/4BCF053A25474F6B8A9EE5F46C20A7AE) | Discriminates rival causal processes and reconstructs a bounded mechanism; it does not estimate an average effect | `O,R,I,D` | Mechanism explanation | Magenta names it for government evaluation; Cambridge supplies the method authority |
| `P05` | Fuzzy-set QCA over a declared 10–50-case population, with substantive calibration, necessity/sufficiency analysis, explicit remainder policy, and return to cases | Configurational comparative inference | Magenta A1.1; RAND-derived `causal inference` is split; [Ragin's comparative method](https://www.ucpress.edu/book/9780520280038/the-comparative-method) | Identifies necessary or sufficient configurations and equifinality, not temporal mechanisms or marginal effects | `O,R,I,D` | Configurational explanation | Magenta describes policy use; an independent foundational method source defines its set-theoretic warrant |
| `P06` | Constructivist grounded theory with initial coding, constant comparison, memoing, theoretical sampling, category-adequacy appraisal, and reflexive integration | Qualitative interpretation and theory construction | RAND-derived `grounded theory`; government [quality guidance for qualitative policy evaluation](https://www.gov.uk/government/publications/the-magenta-book/quality-in-qualitative-evaluation-qqe-html); [Charmaz, 3rd ed.](https://uk.sagepub.com/en-gb/mst/constructing-grounded-theory/book255601) | Builds a bounded interpretive theory through iterative comparison and theoretically directed sampling | `O,R,I` | Theory construction | RAND seed plus a mature independent method guide; government guidance establishes the policy-evaluation use class |
| `P07` | Cross-sectional probability-sample survey estimating a named population prevalence, with a defined frame, design weights, nonresponse treatment, uncertainty, and error reporting | Population measurement | RAND-derived `survey analysis`/`sampling strategy`; Magenta A5.3; [OMB statistical-survey standards](https://nces.ed.gov/sites/default/files/nces/document/2024/10/standards_stat_surveys.pdf) | Estimates a population quantity with design-based uncertainty; it does not identify a policy effect | `O,R,D` | Description and measurement | Both catalogs; Magenta says surveys are widely used and OMB supplies official standards |
| `P08` | Supervised quantitative-text prevalence measurement using a human-coded target, document-grouped held-out evaluation, simple baselines, uncertainty, and item-level error analysis | Computational text measurement | RAND-derived `text-as-data`/`computational text analysis`; [Grimmer and Stewart](https://doi.org/10.1093/pan/mps028); [World Bank text analytics practice](https://www.worldbank.org/en/research/brief/text-and-data-analytics-at-the-world-bank) | Measures the prevalence of a declared textual construct at corpus level; classifier accuracy is not construct validity | `O,R,I,D` | Description and measurement | RAND seed, a field method review, and documented operational policy use at the World Bank |
| `P09` | Operational probabilistic time-series forecast for a named numerical target and horizon, evaluated by rolling origin against naive/seasonal baselines and monitored without rewriting historical forecasts | Forecasting | RAND-derived `forecasting`/`time series analysis`; Futures Toolkit forecasting family; [Hyndman and Athanasopoulos, 3rd ed.](https://otexts.com/fpp3/) | Predicts a future quantity under a time-respecting information set; prediction is not causal explanation | `O,D` | Prediction | Independent catalog/toolkit recognition plus a mature forecasting method source |
| `P10` | Agent-based policy simulation with an ODD-described model, explicit purpose and abstraction boundary, verified implementation, frozen stochastic experiment, replication, and sensitivity analysis | Simulation/model-based exploration | RAND-derived `agent-based modeling`; Magenta simulation family; [ODD 2020](https://www.jasss.org/23/2/7.html) | Establishes what the declared model generates under specified configurations; it does not confirm real-world effects | `D,S` | Model exploration | Both catalogs; ODD is a mature cross-domain description standard |
| `P11` | Robust Decision Making under deep uncertainty, using decision framing, many plausible futures, vulnerability/scenario discovery, trade-off analysis, and adaptive strategy revision | Decision under deep uncertainty and foresight | RAND-derived `robust decision making`; Futures Toolkit policy stress-testing; [RAND RDM methodology](https://www.rand.org/content/dam/rand/pubs/research_reports/RR3000/RR3017/RAND_RR3017.pdf) | Finds vulnerabilities and comparatively robust/adaptive strategies without pretending to predict one best future | `D,E,S` | Foresight and strategy design | RAND and UK-government classifications plus an official RAND method source |
| `P12` | Green Book 2026 policy-option appraisal composed of social cost-benefit analysis where defensible and bounded MCDA for material non-monetized dimensions, with distribution, uncertainty, feasibility, and accountable choice kept explicit | Option appraisal | RAND-derived `decision analysis`/`MCDA`; Magenta A3; [Green Book guidance](https://www.gov.uk/government/collections/the-green-book-and-accompanying-guidance-and-documents) and [MCA manual](https://www.gov.uk/government/publications/multi-criteria-analysis-manual-for-making-government-policy) | Compares options against public objectives and consequences; analytic appraisal informs but does not make the accountable policy choice | `O,R,I,D,E` | Option appraisal | Both catalogs and standing cross-government appraisal guidance |
| `P13` | Three-round anonymous policy Delphi with purposive expert-panel construction, controlled feedback, stability/disagreement analysis, and no rule that consensus equals truth | Structured expert elicitation | RAND-derived `Delphi method`; Futures Toolkit Delphi; [RAND Delphi guidance](https://www.rand.org/pubs/tools/TLA3082-1.html) | Elicits and stabilizes expert judgments or maps disagreement under incomplete information | `R,I,D,E` | Uncertainty characterization and prioritization | Both catalogs; official RAND guidance documents broad policy use |
| `P14` | Convergent mixed-methods policy evaluation with independently warranted qualitative and quantitative strands, explicit merge in a joint display, divergence disposition, and bounded meta-inference | Mixed-methods integration | Supplementary NIH classification; the RAND-derived inventory's separate qualitative and quantitative labels are not silently merged; [NIH best practices](https://obssr.od.nih.gov/research-resources/mixed-methods-research) | Produces a meta-inference from purposeful integration while preserving each strand's warrant and contradictions | `O,R,I,D` | Integration and meta-inference | NIH classifies convergent, sequential, embedded, and multiphase designs; this freezes only the convergent variant |

The recommendation is therefore **14 named variants across 13 families**. The
only two-member family is theory-based/configurational inference: `P04` asks
which causal process best explains one case, while `P05` asks which calibrated
condition configurations are necessary or sufficient across cases. Neither can
substitute for the other.

Eight variants overlap the accepted-format pilots or hostile stress sample.
That does not give them implementation credit: those artifacts established
that the discovery instrument can represent the variants, not that the
workbench implements them or that their Phase 3 decomposition is complete.

### Balance check

| Required spread | Portfolio coverage |
| --- | --- |
| Observed information | `P01`–`P09`, `P12`, `P14` |
| Reported information | `P01`, `P04`–`P08`, `P12`–`P14` |
| Interpreted information | `P01`, `P04`–`P06`, `P08`, `P12`–`P14` |
| Derived information | All except the central interpretive core of `P06`; even there, runtime actions may derive indexes without owning the interpretation |
| Elicited information | `P11`–`P13` |
| Simulated information | `P10`, `P11` |
| Description/measurement | `P07`, `P08` |
| Causal effect | `P02`, `P03` |
| Mechanism/configuration | `P04`, `P05` |
| Prediction | `P09` |
| Synthesis | `P01` |
| Appraisal/foresight | `P11`, `P12`, `P13` |
| Mixed-methods meta-inference | `P14` |

The set is deliberately not weighted toward current implementation. It includes
human-led interpretation and elicitation, deterministic estimation and
forecasting, generated model evidence, and genuine qualitative–quantitative
integration even though these have sharply different present software status.

## Exclusions and denominator consequences

Excluded labels are not declared unimportant. They are outside this proposed
denominator for the stated reason and may be proposed in a later, separately
versioned portfolio.

| Excluded family or labels | Disposition and reason | Effect of exclusion on later §11 claims |
| --- | --- | --- |
| `policy evaluation`, `program evaluation`, `impact assessment`, `outcome`, `process`, `formative`, `summative` | Purposes or umbrellas, not frozen methods. Their relevant roles are exercised by named designs above. | Prevents inflating method counts with labels that would decompose into overlapping component methods; narrows claims to the selected variants. |
| Generic `regression`, `causal inference`, `machine learning`, `NLP`, `validation`, `uncertainty analysis`, `sensitivity analysis` | Operations or technique families without a target estimand, evidence object, and warrant. | Makes all denominators smaller but more falsifiable; no coverage claim may extend to these umbrellas. |
| Propensity-score matching, instrumental variables, regression discontinuity, synthetic control, interrupted time series, staggered-adoption DiD | Eligible quasi-experimental variants, but `P03` is the one minimal representative. They are not aliases for `P03`. | Makes semantic and complete-method coverage easier within quasi-experimental work and prevents any claim of general quasi-experimental coverage. |
| Realist evaluation/synthesis and contribution analysis | Eligible theory-based variants, but excluded by the stop rule after `P04` and `P05` cover distinct mechanism and configurational leverage. | Makes theory-based coverage easier and leaves context–mechanism–outcome and contribution-claim interiors explicitly uncovered. |
| Ethnography, focus groups, interviews, observations, case study, generic content analysis | Some are data-collection modes and some are broad designs. `P06` freezes one full qualitative analytic method; these remain non-equivalent. | Makes qualitative coverage easier and bars a claim that serving grounded theory serves ethnography, case study, or generic qualitative analysis. |
| Rapid evidence assessment, literature review, knowledge synthesis, qualitative evidence synthesis, realist synthesis, network meta-analysis | `P01` freezes one high-integrity randomized-effect review variant. Faster, qualitative, realist, and network variants have different search, synthesis, and conclusion rules. | Makes synthesis coverage materially easier; future results apply only to `P01`. |
| Microsimulation, system dynamics, discrete-event simulation | `P10` is the single simulation representative; model ontology and inference differ across these variants. | Makes simulation coverage easier and prohibits generalizing ABM support to other simulation families. |
| Scenario planning, horizon scanning, trend analysis, backcasting, wargaming, tabletop exercises, serious games | `P11` and `P13` cover model-assisted deep uncertainty and elicitation. Participatory/non-model foresight and gaming are excluded by minimality, not merged. | Makes foresight and unattended-execution coverage easier, because facilitation-heavy workflows are absent. |
| Social-network analysis, GIS/spatial analysis | Eligible specialist relational/spatial families, but not required by the predeclared minimum decision-role spread. | Makes raw-shell, semantic, and complete-method coverage easier; no later claim may extend to relational or spatial inference. |
| Legal-authority analysis plus institutional implementation mapping | Important policy-analysis composition, but the source freeze does not yet have a cross-jurisdiction conduct authority sufficient for the candidate-level source gate. | Makes policy-appraisal coverage easier and leaves lawfulness and institutional mandate/capacity explicitly outside the denominator. |
| Stand-alone cost-benefit analysis | Included only as a named subprofile inside `P12`; it is not collapsed into MCDA. Phase 3 must preserve monetized welfare, non-monetized criteria, value judgments, and decision authority separately. | Avoids double-counting one composed appraisal while keeping both semantic interiors required for complete coverage of `P12`. |
| Sequential exploratory, sequential explanatory, embedded, and multiphase mixed-methods designs | NIH-recognized variants, but `P14` freezes only convergent integration. | Makes integration coverage substantially easier; coverage of `P14` cannot be generalized to other timing or priority structures. |

## Expected effect on §11 denominators

No Phase 6 numerator or percentage can be calculated until the approved
variants are decomposed and mapped. The directional effects are nevertheless
clear:

| §11 measure | Denominator under this proposal | Expected difficulty compared with an implementation-weighted portfolio |
| --- | --- | --- |
| `raw_shell_reuse` | All decomposed steps from these 14 variants, using the approved portfolio version beside the result | Harder: the set adds distinct evidence, simulation, elicitation, integration, and method-owned judgment shapes. Stable custody/version/review mechanics may recur, but broad verb similarity cannot count. |
| `semantic_implementation_coverage` | Required steps reported separately for each named variant | Harder: an existing shell earns no credit for a missing method-owned interior, and narrow variants prevent “supports surveys/ML/evaluation” overclaims. |
| `complete_method_coverage` | Fourteen equally weighted method variants | Materially harder: one missing required shell or semantic interior leaves that method uncovered, regardless of how many other methods are complete. |
| `unattended_execution_coverage` | Required operations across the same 14 variants, with any human in `actor_chain` treated as attended under §11 | Harder and more honest: grounded theory, PT, QCA calibration, appraisal, Delphi, systematic-review judgments, and mixed-methods reconciliation contain irreducible human authority; deterministic estimation, forecasting, and simulation do not offset them by method weight. |

The exclusions make all four measures easier than a universal policy-method
claim would be. The effect is largest for complete-method and unattended
coverage because facilitation-heavy foresight/gaming, legal judgment, other
mixed-methods timings, and specialist spatial/network workflows are outside the
set. Every Phase 6 result must therefore say
`portfolio=phase2b-proposal-0.2` (or its approved successor) and repeat these
scope limits.

## Important alternative and tradeoff

The strongest alternative is a **17-variant breadth-first portfolio** that adds:

- realist synthesis of complex interventions;
- policy stress-testing against qualitatively constructed scenarios; and
- social-network analysis of a bounded policy-actor network.

That alternative tests context–mechanism synthesis, facilitation-led foresight,
and relational evidence earlier. It is more representative of the whole RAND-
derived inventory, but it adds three source freezes and roughly 21% more
equally weighted methods before the current 14-family denominator has produced
any collision evidence. It also makes complete-method and unattended coverage
harder for reasons that are substantively legitimate but not required by the
predeclared minimum. The recommendation remains the 14-variant portfolio;
retain the three additions as the first expansion candidates after Phase 6.

## Human approval gate

**Recommendation:** approve exactly `phase2b-proposal-0.2`, the 14 variants
`P01`–`P14`, as the Phase 3 portfolio denominator.

Approval means Phase 3 may decompose these variants using the accepted
three-level discovery format and the cited methodology sources. Approval does
not accept any capability collision, implementation status, automation claim,
coverage result, schema, infrastructure design, product change, or promotion.

The important alternative is the 17-variant breadth-first set above. The human
decision is: **approve the 14-variant recommendation, revise to the 17-variant
alternative, or reject/defer portfolio selection.** Until that disposition is
recorded, Phase 3 remains blocked.

## Source verification note

Links above were checked on 2026-08-13 against the named publisher or issuing
institution. The sources serve different roles:

- the repository's RAND-derived inventory generates labels but supplies no
  methodological warrant;
- Magenta, GAO, the Futures Toolkit, and NIH establish policy/research-design
  families and real-use context;
- Cochrane, ICH, Bennett and Checkel, Ragin, Charmaz, OMB, Grimmer and Stewart,
  Hyndman and Athanasopoulos, ODD, RAND RDM/Delphi, the Green Book, and the MCA
  manual define or constrain the frozen variants.

Phase 3 must pin exact editions and sections in each method frame. This proposal
does not replace that source-freeze obligation.
