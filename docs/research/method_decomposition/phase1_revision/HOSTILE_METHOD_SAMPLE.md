# Hostile six-method sample

Status: exploratory stress test; not a canonical method catalog or schema

## Purpose

This sample asks whether the revised three-level decomposition instrument still
works when applied beyond grounded theory, an RCT, and policy appraisal. The
methods were chosen because they stress different warrants and workflow shapes:

- systematic review: staged selection with conditional pooling and recursive
  correction;
- theory-testing Process Tracing: within-case rival discrimination with
  evidence-acquisition returns;
- time-series forecasting: repeated operational cycles containing protected
  evaluation boundaries;
- fuzzy-set Qualitative Comparative Analysis (fsQCA): cross-case set relations
  with repeated return to concepts and cases;
- agent-based policy simulation: generated evidence from an explicitly bounded
  model rather than observations of the policy world;
- legal-authority analysis plus institutional implementation mapping: two
  linked forms of analysis with different source authority and conclusions.

The sample is deliberately hostile to a universal pipeline. It does not imply
that every method is cyclic, that every move should be automated, or that
similar verbs have the same analytical meaning.

## How to read the tables

Each row is a Level 2 analytical move. Broad phases are Level 1. The
`Representative execution` column illustrates Level 3 without treating every
query, calculation, or interface action as a separate analytical capability.

Connection abbreviations are:

- `AF`: artifact flow;
- `RC`: retained context;
- `CG`: control gate;
- `FB`: feedback;
- `PT`: prohibited transition.

## 1. Cochrane-style systematic review of randomized intervention effects

### Frozen boundary

This is a review addressing a prespecified intervention-effect question. It may
include pairwise meta-analysis when included studies, estimands, and outcome
definitions are sufficiently compatible. PRISMA contributes reporting duties;
it does not replace the conduct method.

```text
question and protocol
  -> search and deduplicate
  -> title/abstract screening -> full-text eligibility
  -> extract study data and appraise risk of bias
  -> decide whether and how evidence may be synthesized
       -> narrative synthesis
       -> meta-analysis where defensible
       -> no pooled estimate where indefensible
  -> assess heterogeneity, certainty, and limits
  -> report
       -> correct extraction/search decisions when audit exposes an error
       -> update as a new review version when new evidence arrives
```

| Phase | Analytical move | Inspectable output | Method-owned rule / refusal | Representative execution | Connections |
| --- | --- | --- | --- | --- | --- |
| Frame | Specify the review question and eligibility | Review question, outcomes, eligible designs, populations, interventions, comparators | Eligibility must answer the question rather than follow convenient search results. | Human protocol authoring; structured protocol validation | `AF`, then `RC` throughout |
| Govern | Prespecify conduct and synthesis | Registered protocol, search plan, synthesis plan, deviation policy | Outcome-informed changes remain visible and justified. | Registry submission; version freeze; reviewer sign-off | `CG`; undisclosed outcome-informed rewrite is `PT` |
| Discover | Search comprehensively enough for the protocol | Search strategies, database runs, candidate records | Search adequacy is domain- and question-specific; one database is not automatically sufficient. | Database/API queries; citation chasing; human search review | `AF`; search audit may create `FB` |
| Select | Deduplicate and screen records | Unique record set and title/abstract decisions | Review-specific criteria determine inclusion; automation may prioritize but not silently change criteria. | Matching/deduplication; dual screening or adjudication | `AF`, `CG` |
| Select | Apply full-text eligibility | Included studies, excluded full texts, exclusion reasons | Missing reports, study/report multiplicity, and borderline eligibility require review-owned judgment. | Full-text retrieval; independent review; disagreement resolution | `AF`, `CG`; retrieval gaps produce `FB` |
| Extract | Construct study-level evidence records | Study identities, arms, outcomes, estimates, design features, provenance | Reports about one study must not be treated as independent studies; transformations remain explicit. | Structured extraction; cross-checks; calculations | `AF`; corrections are `FB` |
| Appraise | Judge risk of bias for each relevant result | Domain judgments, rationale, supporting passages | Risk of bias is not a generic source-quality score and is tied to a result/design. | Method-specific tool plus reviewer judgment | `AF`, `CG` into interpretation |
| Synthesize | Decide what can be combined | Synthesis groups and pooling disposition | Similar labels do not establish comparable estimands or measures. | Human/assisted grouping; compatibility checks | `CG`; inappropriate pooling is `PT` |
| Synthesize | Produce narrative and, conditionally, quantitative synthesis | Structured summary and optional pooled estimates | Statistical pooling cannot repair biased, incompatible, or selectively reported evidence. | Meta-analysis software; narrative synthesis; model diagnostics | Parallel `AF` branches |
| Stress | Assess heterogeneity, sensitivity, reporting bias, and certainty | Robustness results, certainty assessment, limitations | Each assessment uses review-specific criteria; absence of evidence is not evidence of no effect. | Sensitivity models; plots; structured certainty review | `AF`; anomaly can cause `FB` to extraction/grouping |
| Report | Publish an auditable review and flow account | Review report, flow diagram, data/code, deviations | Reporting transparency does not retroactively repair conduct. | Report generation; PRISMA checks; review | `AF`; later evidence begins versioned `FB` |

### Reuse result

- Mechanics: source identity, deduplication lineage, decisions with reasons,
  version freezing, review state, and correction history.
- Shell: present candidates against criteria, record independent judgments and
  adjudication, then continue, request evidence, or exclude.
- Method-owned: eligibility meaning, study/report linkage, risk of bias,
  synthesis compatibility, meta-analysis, certainty, and review conclusions.

## 2. Theory-testing Process Tracing in one bounded case

### Frozen boundary

This variant asks which of several frozen rival causal processes best explains
a bounded outcome in one case. It uses qualitative Bayesian likelihood
reasoning to compare diagnostic evidence. It does not estimate a population
average treatment effect.

```text
bound case and outcome
  -> freeze rivals, mechanisms, and observable implications
  -> assess evidence exposure and source opportunities
  -> acquire and admit case evidence
  -> appraise each item under every relevant rival
  -> compare rival support and reconstruct temporal mechanism
  -> critic and publication gate
       -> qualified result or refusal
       -> seek missing evidence, repair a rival, or rerun as a new version
```

| Phase | Analytical move | Inspectable output | Method-owned rule / refusal | Representative execution | Connections |
| --- | --- | --- | --- | --- | --- |
| Bound | Define case, outcome, period, and process boundary | Case specification | The case must make the outcome and evidence opportunities determinate enough to test. | Analyst definition; validation | `AF`, `RC` |
| Design | Freeze rivals, mechanisms, and discriminating implications | Rival set, mechanism sketches, evidence predictions | Rivals must be meaningfully distinguishable; seeing case evidence before freezing changes inferential status. | Theory/source review; structured authoring | `CG`; undisclosed post-exposure rewrite is `PT` |
| Govern | Assess exposure, priors, coverage, and source opportunities | Design audit and source-fitness disposition | Reused theory-generating evidence may warn or downgrade; a method-owned invalidity condition decides whether it blocks. | Metadata checks; analyst review | `CG` |
| Acquire | Build and review a case source packet | Admitted sources, hashes, provenance, rejected candidates | Authenticity, relevance, temporal opportunity, and independence remain explicit. | Search/retrieval; custody checks; human admission | `AF`; gaps create `FB` |
| Appraise | Extract case events and evidence items | Typed events, actors, sources, passages, absences | Extraction is not yet diagnostic support. | Structured extraction; anchoring; review | `AF` |
| Appraise | Judge likelihood of each item under each rival | Comparative likelihood judgments and rationales | Diagnostic force is relational across rivals, not an intrinsic evidence score. | Human/model elicitation with independent audit | `AF`, `CG` |
| Compare | Update comparative support without erasing uncertainty | Rival comparison and sensitivity | The calculation cannot rescue bad likelihood judgments or missing rivals. | Deterministic log-space update; audit | `AF` |
| Reconstruct | Build and audit the temporal mechanism account | Mechanism graph and gap list | Temporal sequence and causal linkage must be supported separately from rival ranking. | Graph construction; contradiction checks | `AF`; gaps may create `FB` |
| Conclude | Synthesize, criticize, qualify, or refuse | Bounded verdict and missing-evidence agenda | “Retain unconfirmed” and “cannot distinguish” are valid results. | Narrative synthesis; critic; publication gate | `CG`; failure produces refusal or `FB` |
| Revise | Acquire new evidence or create a reviewed new run | New packet/run with lineage | Later evidence must not silently rewrite the frozen baseline or historical result. | Versioned rerun and derivation record | `FB`; overwriting old result is `PT` |

### Reuse result

- Mechanics: source custody, frozen baselines, derivation lineage, review,
  qualification, refusal, and rerun versioning.
- Shell: expose alternatives and evidence to a method-owned reviewer, retain
  rationale, and permit continue/repair/refuse.
- Method-owned: case/process bounding, diagnostic predictions, comparative
  likelihood appraisal, mechanism inference, and the final PT warrant.

## 3. Operational time-series forecasting

### Frozen boundary

This variant produces a probabilistic forecast for a named numerical target and
horizon using time-indexed historical data. It compares candidate models using
rolling-origin evaluation and monitors later performance. It excludes causal
effect estimation, scenario planning, and judgment-only forecasting.

```text
define target, horizon, use, and information cutoff
  -> acquire and time-index data
  -> establish naive/seasonal baselines
  -> create rolling-origin evaluation folds
  -> fit candidate models inside each fold
  -> compare point and distributional performance
  -> diagnose residuals, calibration, subgroup/regime failure
  -> select or combine and refit at the deployment origin
  -> issue forecast with uncertainty and limits
  -> observe outcomes and monitor
       -> continue
       -> investigate shift
       -> version data/model and retrain
```

| Phase | Analytical move | Inspectable output | Method-owned rule / refusal | Representative execution | Connections |
| --- | --- | --- | --- | --- | --- |
| Target | Define forecast object, horizon, origin, use, and loss | Forecast specification | A useful target and evaluation loss depend on the decision context; prediction is not causal explanation. | Analyst/stakeholder specification | `AF`, `RC` |
| Govern | Freeze the information set available at each origin | Data-availability contract and cutoff policy | Future information and revised data may not leak into historical folds. | Timestamp/as-of joins; access controls | `CG`; leakage is `PT` |
| Prepare | Build time-respecting observations and features | Versioned modeling dataset | Missingness, revisions, frequency, and transformations must preserve what was knowable then. | ETL, temporal joins, validation | `AF` |
| Benchmark | Define simple meaningful baselines | Baseline forecasts | Complexity is justified by out-of-sample gain, not in-sample fit. | Naive/seasonal models | `AF` |
| Evaluate | Construct rolling-origin folds | Frozen train/test origins and horizons | Test observations occur after their training information; horizon matches the use case. | Time-series cross-validation | `CG`; training on test data is `PT` |
| Fit | Estimate candidate models within each fold | Fold-specific fitted models and forecasts | Model assumptions and tuning remain inside the evaluation design. | Statistical/ML fitting | `AF` |
| Score | Compare predictive distributions and point forecasts | Horizon-specific scores, calibration, interval coverage | Metric choice is use-dependent; one aggregate score may hide consequential failures. | Proper scores, errors, calibration plots | `AF`, `CG` |
| Diagnose | Inspect residual structure, instability, and regime/subgroup failures | Diagnostic and shift-risk record | Good historical averages do not guarantee stability at the deployment origin. | Residual tests; slice/regime analysis | `AF`; failure triggers `FB` |
| Produce | Select/combine, refit, and issue the forecast | Versioned forecast distribution and assumptions | The deployment model must follow the evaluated procedure; unsupported horizon extrapolation is qualified/refused. | Fit on available data; forecast generation | `CG`, `AF` |
| Monitor | Join realized outcomes and assess performance | Monitoring series and drift findings | Newly observed outcomes evaluate an earlier forecast; they must not alter that historical forecast. | Outcome ingestion; score updates | `FB`; historical overwrite is `PT` |
| Revise | Retrain or redesign under a new version | New model/data/run lineage | Regime change may require a new method, target, or refusal rather than automatic retraining. | Pipeline rerun plus review | `FB` |

### Reuse result

- Mechanics: versioned data/model/run identity, temporal cutoffs, lineage,
  monitoring, review, and explicit refusal.
- Shell: freeze a design, execute candidates, compare against a baseline,
  diagnose failures, and gate deployment.
- Method-owned: target and loss definition, fold construction, forecast models,
  scoring/calibration interpretation, shift diagnosis, and deployment validity.

## 4. Fuzzy-set Qualitative Comparative Analysis

### Frozen boundary

This variant evaluates necessary and sufficient set relations among calibrated
conditions and an outcome across a defined case population. It includes truth
table analysis, Boolean minimization, limited-diversity decisions, robustness,
and return to cases. It does not claim a temporal within-case mechanism or an
average marginal effect.

```text
define case population, outcome, and conditions
  -> develop set meanings and calibration anchors
  -> calibrate case memberships
  -> inspect necessity
  -> construct truth table for sufficiency
  -> resolve contradictory rows and limited diversity
  -> minimize under explicit counterfactual assumptions
  -> assess consistency, coverage, robustness, and asymmetry
  -> return to typical, deviant, and contradictory cases
       -> revise concepts/calibration with a recorded new version
       -> qualify or refuse the solution
```

| Phase | Analytical move | Inspectable output | Method-owned rule / refusal | Representative execution | Connections |
| --- | --- | --- | --- | --- | --- |
| Bound | Define the case population, outcome, and candidate conditions | Case universe and conceptual model | Cases must belong to a defensible population; conditions are not selected solely for convenient data. | Theoretical/case review | `AF`, `RC` |
| Calibrate | Define set meanings and qualitative anchors | Calibration rationale and thresholds/functions | Calibration is a substantive claim about set membership, not rescaling by habit. | External anchors, case knowledge, analyst judgment | `CG` |
| Calibrate | Assign and inspect membership scores | Calibrated data matrix and ambiguous cases | Scores must preserve conceptual meaning; doubtful cases remain inspectable. | Calibration functions; case review | `AF`; anomalies create `FB` |
| Analyze | Evaluate candidate necessary conditions | Necessity results, consistency/coverage, relevance checks | Necessity and sufficiency are distinct claims; high consistency alone can mislead. | Set-relation calculations | `AF` |
| Configure | Construct the truth table | Configurations, cases, frequencies, consistency | Threshold choices and contradictory configurations remain explicit. | QCA software plus review | `AF`, `CG` |
| Resolve | Investigate contradictions and limited diversity | Resolution log and remainder policy | Contradictions may require return to cases or concepts; logical remainders are not observed cases. | Case inspection; sensitivity; theoretical review | `FB`, `CG` |
| Minimize | Derive solution terms under declared assumptions | Complex, parsimonious, or intermediate solution | Counterfactual assumptions determine permissible simplification and remain visible. | Boolean minimization | `AF` |
| Stress | Assess robustness, asymmetry, consistency, and coverage | Robustness envelope and claim limits | Results for the presence of an outcome do not automatically invert for its absence. | Threshold/specification tests | `AF`; instability creates `FB` |
| Return | Examine typical, deviant, and contradictory cases | Case-level interpretation and new questions | Cross-case set relations do not establish temporal mechanisms; case analysis may explain anomalies. | Case selection and qualitative analysis | `AF`, `FB` |
| Conclude | State bounded necessity/sufficiency findings or refuse | Solution account, scope, unresolved contradictions | A mechanically produced solution is not enough when calibration or contradictions are indefensible. | Synthesis and expert review | `CG` |

### Reuse result

- Mechanics: case/data identity, versioned calibration and solutions, lineage,
  review, sensitivity branches, and refusal.
- Shell: apply a method-owned transformation, expose threshold-sensitive
  cases, stress alternatives, and return to source cases.
- Method-owned: set conceptualization, calibration, necessity/sufficiency,
  truth-table thresholds, remainders, minimization, and QCA interpretation.

## 5. Agent-based policy simulation experiment

### Frozen boundary

This variant uses an agent-based model to compare policy configurations under
explicit mechanisms, initial conditions, schedules, and stochastic variation.
ODD structures the model description; purpose-specific verification,
calibration/validation, experiment design, uncertainty, and sensitivity are
required separately. Simulated events are generated evidence about the model,
not observations of the policy world.

```text
define policy question, model purpose, and system boundary
  -> specify entities, state, processes, schedule, initialization, and inputs
  -> implement and verify correspondence with the specification
  -> calibrate or justify uncertain inputs and compare relevant patterns
  -> freeze scenarios and experimental contrasts
  -> execute replicated runs with retained seeds/configurations
  -> compare distributions, traces, failures, and mechanisms
  -> sensitivity and uncertainty analysis
       -> revise model or experiment as a new version
       -> issue a model-conditional finding or refuse real-world extrapolation
```

| Phase | Analytical move | Inspectable output | Method-owned rule / refusal | Representative execution | Connections |
| --- | --- | --- | --- | --- | --- |
| Bound | Define purpose, question, system boundary, and intended inference | Model-purpose statement and excluded phenomena | Appropriate abstraction is purpose-specific; omitted processes bound the conclusion. | Domain/modeler review | `AF`, `RC` |
| Specify | Define entities, state, processes, timing, initialization, inputs, and stochasticity | ODD-style model specification | The specification must make model behavior and assumptions inspectable. | Structured authoring and review | `AF` |
| Implement | Realize the specification in executable code | Versioned model build | Implementation choices must not silently change the conceptual model. | Programming; compilation; unit/invariant checks | `AF`; mismatch creates `FB` |
| Verify | Test whether implementation behaves as specified | Verification results and defects | Verification asks whether the model was built as specified, not whether the model is true. | Tests, traces, invariants, extreme-case checks | `CG`, `FB` |
| Ground | Calibrate parameters or justify assumptions and assess relevant empirical patterns | Calibration/validation record | Fit to selected patterns does not validate every mechanism or use. | Data comparison; parameter fitting; expert elicitation | `CG`, `AF` |
| Design | Freeze scenarios, contrasts, factors, replications, and estimands of model behavior | Simulation experiment plan | Post-result scenario selection changes status; stochastic precision requires adequate replication. | Experiment design; power/precision checks | `CG`; undisclosed rewrite is `PT` |
| Execute | Run and retain the experiment | Runs, seeds, event/state traces, failures | Every result remains bound to exact model, configuration, seed, and environment. | Scheduler/runtime; artifact retention | `AF` |
| Compare | Estimate model-conditional contrasts and inspect mechanisms/failures | Distributions, matched comparisons, trace explanations | Generated contrasts describe this model under these configurations. | Aggregation; visualization; trace queries | `AF` |
| Stress | Perform uncertainty and sensitivity analysis | Influential assumptions, robustness regions, failure boundaries | Input uncertainty and structural uncertainty must not collapse into Monte Carlo noise. | Global/local sensitivity; alternative structures | Parallel `AF`; failures create `FB` |
| Conclude | State model-conditional implications and limits | Finding, applicability boundary, next empirical needs | The simulation cannot confirm its own real-world mechanisms or intervention effects. | Synthesis and review | `CG`; unsupported extrapolation is refused |
| Revise | Change model/specification/experiment with explicit lineage | New model and experiment version | Historical runs remain attached to the exact prior version. | Versioned rebuild and rerun | `FB`; overwriting is `PT` |

### Reuse result

- Mechanics: specification/build/run identity, configuration custody, seeds,
  lineage, review, branching, and refusal.
- Shell: freeze an experiment, execute replications, compare alternatives,
  expose uncertainty, and gate a bounded conclusion.
- Method-owned: model abstraction, mechanisms, calibration/validation,
  simulation experiment design, sensitivity interpretation, and extrapolation.

## 6. Legal authority and institutional implementation constraints

### Why this is a composed route, not one method

The RAND-derived inventory label `legal/institutional analysis` hides two
different questions:

1. **Legal-authority analysis:** What does controlling law permit, require, or
   prohibit for this policy option in this jurisdiction and period?
2. **Institutional implementation mapping:** Which organizations have the
   mandate, capacity, dependencies, and coordination relationships needed to
   implement the option?

The first relies on jurisdiction-specific authority and interpretive practice.
The second combines formal mandates with empirical information about actual
organizations and implementation. They may exchange artifacts, but neither
substitutes for the other.

```text
named policy option and factual assumptions
  -> legal track: jurisdiction/time -> controlling authorities -> interpretation
                   -> application -> permission/duty/prohibition/discretion
  -> institutional track: actors/mandates -> resources/dependencies/practices
                   -> coordination and implementation constraints
  -> reconcile legal powers with institutional feasibility
       -> feasible within constraints
       -> redesign option
       -> unresolved legal question / counsel review
       -> legally available but institutionally infeasible, or vice versa
  -> monitor legal and institutional change as a new version
```

| Phase | Analytical move | Inspectable output | Method-owned rule / refusal | Representative execution | Connections |
| --- | --- | --- | --- | --- | --- |
| Frame | Specify the legal question, policy option, facts, jurisdiction, date, and decision-maker | Issue statement and factual assumptions | A conclusion outside the named jurisdiction/time or on uncertain facts is qualified. | Analyst/client framing; validation | `AF`, `RC` |
| Research law | Retrieve and validate controlling authorities | Statutes, regulations, precedent, orders, authority hierarchy, currency record | Primary authority, hierarchy, amendment, effective date, and precedent control are jurisdiction-specific. | Legal databases; citation and currency checking | `AF`, `CG` |
| Interpret law | Interpret relevant text in context | Competing interpretations and rationale | Ordinary meaning, statutory context, canons, precedent, history, purpose, and implementation receive jurisdiction- and question-specific weight. | Legal reasoning; expert review | `AF` |
| Apply law | Apply interpretations to the stated facts and option | Permissions, duties, prohibitions, discretion, ambiguity, litigation risk | Changing facts may change the result; policy desirability does not determine legal authority. | Issue/rule/application reasoning | `AF`, `CG` |
| Map institutions | Identify responsible bodies, mandates, oversight, and coordination | Actor/mandate/responsibility map | Formal responsibility does not establish practical capacity or informal operation. | Document review; interviews; organizational mapping | `AF` |
| Appraise implementation | Assess resources, capacity, incentives, dependencies, and actual practices | Implementation constraint and dependency record | Legal authority, administrative capacity, political support, and operational feasibility are distinct. | Administrative data; interviews; workflow analysis | `AF` |
| Reconcile | Compare the option against both tracks | Feasibility matrix, conflicts, redesign needs | A policy can be lawful but infeasible, feasible but unauthorized, or uncertain on either dimension. | Cross-track review and option redesign | Convergent `AF`, then `CG` |
| Challenge | Develop counterarguments and obtain appropriate review | Adversarial issues, unresolved questions, review disposition | Material ambiguity or high-stakes advice may require qualified counsel or other accountable expertise. | Red-team; legal/expert review | `FB`, `CG` |
| Conclude | State bounded constraints and available routes | Constraint memo, qualified options, unresolved issues | This analysis does not itself choose the policy or guarantee a court/agency outcome. | Synthesis and decision support | `AF`; unresolved issue can refuse |
| Update | Recheck authorities and institutions after material change | New version and supersession lineage | Changed law, precedent, mandates, leadership, resources, or practice can invalidate prior applicability. | Alerts, re-research, versioning | `FB`; silent historical rewrite is `PT` |

### Reuse result

- Mechanics: authoritative-source identity, effective-date and jurisdiction
  metadata, citation lineage, review, versioning, supersession, and refusal.
- Shell: apply explicit criteria/authority to a bounded option, expose competing
  interpretations and assumptions, require accountable review, and return a
  constrained result.
- Method-owned: legal hierarchy and interpretation, application to facts,
  mandate analysis, capacity/coordination appraisal, and the authority to issue
  or rely on legal advice.

## Source ledger

The systematic-review, Process Tracing, and simulation variants reuse the
sources frozen before the earlier Phase 1 pilot in
[`../phase1_pilot/sources.md`](../phase1_pilot/sources.md).

Additional sources frozen for this hostile sample:

| Variant | Primary source | Supporting source and boundary |
| --- | --- | --- |
| Operational time-series forecasting | Hyndman and Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed., especially [forecasting data and methods](https://otexts.com/fpp3/data-methods.html), [time-series cross-validation](https://otexts.com/fpp3/tscv.html), [distributional accuracy](https://otexts.com/fpp3/distaccuracy.html), and [prediction intervals](https://otexts.com/fpp3/prediction-intervals.html) | This is a bounded time-series profile, not a general machine-learning, causal-forecasting, judgmental-forecasting, or strategic-foresight standard. |
| fsQCA | Ragin, *Redesigning Social Inquiry: Fuzzy Sets and Beyond* ([publisher page](https://press.uchicago.edu/ucp/books/book/chicago/R/bo5973952.html)) | Schneider and Wagemann, *Set-Theoretic Methods for the Social Sciences* ([publisher page](https://www.cambridge.org/core/books/settheoretic-methods-for-the-social-sciences/236C162386C1188966FE269D625CA289)); crisp-set and multi-value variants remain outside this frozen profile. |
| Legal authority | Congressional Research Service, [*Statutory Interpretation: Theories, Tools, and Trends*](https://www.congress.gov/crs-product/R45153) | U.S. federal statutory interpretation is an example variant, not a universal legal method; jurisdiction-specific law and current authority control actual work. |
| Institutional implementation mapping | OECD, [*Policy Framework on Sound Public Governance*](https://www.oecd.org/en/publications/2020/12/policy-framework-on-sound-public-governance_931b05fc.html) | The framework establishes roles, coordination, capacities, implementation, monitoring, and feedback as relevant dimensions; it is not evidence that one generic institutional score is valid. |

## Sample-level result

The three-level instrument remains understandable across all six routes. It
also needs revision before a broader catalog can rely on it:

1. applicability boundaries such as forecast horizon/information regime,
   simulation purpose/model boundary, and legal jurisdiction/effective date
   recur, but their semantics remain typed and method-owned;
2. legal/institutional analysis proves that one inventory label may represent a
   composition of methods rather than one method variant;
3. current `artifact flow` does not distinguish a lossless handoff from a
   transformation that changes the artifact's meaning or evidential status;
4. source authority is not captured by information origin alone;
5. protected information boundaries and historical immutability recur in RCT,
   forecasting, Process Tracing, simulation, and systematic review;
6. the five existing connection types are otherwise sufficient for this
   sample when accompanied by typed artifacts and explicit authority.

These findings are developed in
[`CAPABILITY_PRESSURE_READOUT.md`](CAPABILITY_PRESSURE_READOUT.md).
