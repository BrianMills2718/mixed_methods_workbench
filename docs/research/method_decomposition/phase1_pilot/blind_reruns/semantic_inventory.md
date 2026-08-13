# Blind-rerun semantic inventory

Status: normalized audit evidence; not canonical method contracts

This compact record preserves the input/output and inferential distinction that
caused each operation to be separated. It complements the ordered IDs and
topology in `step_inventory.yaml`. “Refuse” describes the operation's bounded
failure result, not a runtime exception.

## Systematic review

| Step | Consumes | Produces | Method-owned boundary / refusal |
| --- | --- | --- | --- |
| SR01 | decision problem, PICO definitions | structured question, scope | Frame one randomized-effect question; refuse an incoherent scope. |
| SR02 | question, scope | protocol, eligibility, outcomes, analysis rules | Freeze decisions before results; disclose unresolved choices or amendments. |
| SR03 | question, eligibility | search strategies, source plan | Design sensitive reproducible searches independent of known results. |
| SR04 | strategies, source plan | deduplicated records, search log | Preserve source yields and record identity; expose inaccessible sources and uncertain duplicates. |
| SR05 | candidate records, eligibility | retrieval candidates, screening decisions | Apply criteria at title/abstract stage; uncertain records advance. |
| SR06 | full texts, eligibility | included studies, exclusions, report-study map | Link reports to studies and give exclusion reasons; do not erase unresolved linkage. |
| SR07 | search and screening logs | study-flow account, discrepancies | Reconcile records, reports, and studies; refuse normalized-away count gaps. |
| SR08 | included studies, protocol, outcomes | study table, outcome dataset, queries | Extract with source linkage; missing or inconsistent values remain queries. |
| SR09 | studies and outcome data | risk-of-bias judgments and rationale | Appraise result-level internal validity; missing reporting is not low risk. |
| SR10 | outcome data, analysis rules | typed effects, derivations | Respect outcome, unit, direction, and uncertainty; quarantine incompatible estimates. |
| SR11 | study characteristics and effects | synthesis groups, non-pooling decisions | Pool only defensibly comparable studies; non-pooling is valid. |
| SR12 | groups, effects, bias, rules | pooled effects or structured unpooled summaries | Run the declared model or refuse pooling without inventing an average. |
| SR13 | candidate/included evidence and synthesis | missing-results appraisal, sensitivities | Stress unavailable results and analytic alternatives; absence of a test is not reassurance. |
| SR14 | synthesis, heterogeneity, bias, robustness | bounded conclusion, limitations | Interpret within the protocol scope; issue inconclusive when evidence is inadequate. |
| SR15 | protocol through conclusion | auditable review report | PRISMA exposes conduct but cannot repair it; disclose missing items and deviations. |

## Constructivist grounded theory

| Step | Consumes | Produces | Method-owned boundary / refusal |
| --- | --- | --- | --- |
| GT01 | inquiry, researcher position | open question, reflexive frame | Orient without fixing categories or causal hypotheses. |
| GT02 | open question, access | initial sampling plan, richness criteria | Seek analytic richness, not statistical representation. |
| GT03 | sample plan, reflexive frame | corpus increment, field notes | Collect detailed actions, meanings, and contexts; mark thin data. |
| GT04 | source material and field notes | initial codes, analytic questions | Code provisionally near the data; flag forced prior categories. |
| GT05 | incidents, codes, prior comparisons | comparison record, variation map | Constant comparison generates patterns only with contrasts and negative cases. |
| GT06 | codes, comparisons, field notes | memos, sampling leads | Advance concepts and expose interpretive decisions; missing rationale is a gap. |
| GT07 | codes, memos, comparisons | focused codes, selection rationale | Select for analytic significance, not frequency alone. |
| GT08 | focused codes, memos, variation | categories, category gaps | Develop properties and relationships; topic labels alone are insufficient. |
| GT09 | categories and gaps | theoretical-sampling plan, expected tests | Target category development; fixed-corpus rereading is not new theoretical sampling. |
| GT10 | sampling plan, reflexive frame | targeted data and notes | Collect data for named gaps; record access-limited adequacy. |
| GT11 | targeted data, codes, categories | revised codes/categories, negative cases | Revise, split, relate, or reject categories when new data challenge them. |
| GT12 | categories, memos, negative cases, gaps | adequacy argument, residual gaps | Argue adequacy from development and variation; never use a mechanical count. |
| GT13 | categories, memos, adequacy | integrated category model, core process | Integrate rather than list themes; unsupported relations remain gaps. |
| GT14 | integrated model, adequacy, reflexivity | bounded theory and report | Produce situated interpretive theory or downgrade to descriptive analysis. |

## Theory-testing process tracing

| Step | Consumes | Produces | Method-owned boundary / refusal |
| --- | --- | --- | --- |
| PT01 | research question, candidate case | bounded case, outcome, interval | Refuse an unbounded case, outcome, or time period. |
| PT02 | case, outcome, candidate explanations | frozen rivals and scope | Rivals precede appraisal and cannot be silently rewritten afterward. |
| PT03 | rivals, case | causal mechanisms and sequences | A mechanism requires linked entities, activities, and intervening steps. |
| PT04 | mechanisms | predicted evidence, rival matrix | Predictions must discriminate rivals and connect to mechanism steps. |
| PT05 | predictions, rivals | likelihood expectations, test rules | Diagnosticity is comparative; refuse undefended likelihood judgments. |
| PT06 | rival matrix, expectations, case | evidence-collection plan, provenance needs | Target potentially discriminating within-case evidence. |
| PT07 | collection plan and provenance needs | authenticated observations, provenance, gaps | Evidence must be identifiable and temporally relevant; qualify weak provenance. |
| PT08 | observations and provenance | qualified evidence, dependence map, quality flags | Credibility and source dependence limit corroboration. |
| PT09 | qualified evidence, rival matrix, rules | rival-relative test results, mismatches | Compare every observation under every relevant rival; retain indeterminacy. |
| PT10 | test results, expectations, dependence | plausibility updates, likelihood record | Update relative support without claiming a population effect or false precision. |
| PT11 | updates, mismatches, gaps, quality flags | robustness and residual alternatives | Challenge likelihoods and dependence; flag rankings that reverse easily. |
| PT12 | mechanisms, test results, updates, robustness | mechanism-evidence account, rival comparison | Link evidence to sequence; narrative coherence alone is insufficient. |
| PT13 | account, rivals, alternatives, sensitivity | calibrated conclusion, limitations, refusal | Conclude within one bounded case or explicitly remain inconclusive. |

## Randomized causal-effect estimation

| Step | Consumes | Produces | Method-owned boundary / refusal |
| --- | --- | --- | --- |
| RCT-01 | policy question and contrast | superiority objective | Fix one confirmatory causal question. |
| RCT-02 | objective, population, treatments, outcome, intercurrent events | prespecified ITT estimand | Specify all estimand attributes; ITT is not a missing-data rule. |
| RCT-03 | estimand and design assumptions | design, sample size, SAP, missingness/sensitivity plans | Freeze analysis before assignment and outcome access. |
| RCT-04 | design and participant IDs | unpredictable sequence, concealment | Predictable or manipulated allocation destroys the ordinary randomized warrant. |
| RCT-05 | eligibility, candidates, sequence | randomized cohort, assignments, baseline | Eligibility precedes assignment; all assigned units enter ITT. |
| RCT-06 | assignment and treatment protocols | delivery, deviations, contamination, intercurrent events | Observe execution without redefining assignment by adherence. |
| RCT-07 | cohort, renewal records, time rule | outcomes, missingness | Apply one prespecified definition and clock across arms. |
| RCT-08 | baseline, delivery, outcomes, deviations | locked dataset, flow ledger | Retain and reconcile randomized units; expose post-lock alteration. |
| RCT-09 | allocation audit and conduct records | validity diagnostics | Audit compromise and attrition; baseline significance tests do not create randomization. |
| RCT-10 | locked data, estimand, SAP | primary effect and uncertainty | Estimate groups as randomized; reject post-hoc per-protocol primacy. |
| RCT-11 | primary result and sensitivity plans | assumption stress results | Stress declared missingness/intercurrent-event assumptions without replacing the primary result. |
| RCT-12 | secondary outcomes and multiplicity plan | adjusted or exploratory results | Keep auxiliary inference distinct from confirmation. |
| RCT-13 | estimate, validity, sensitivity, criterion | bounded causal conclusion | Lack of superiority is not equivalence; mechanism and population generalization are separate. |
| RCT-14 | protocol, SAP, flow, results, deviations | auditable trial report | CONSORT reports conduct but cannot repair design or analysis. |

## Policy option appraisal

| Step | Consumes | Produces | Method-owned boundary / refusal |
| --- | --- | --- | --- |
| PA01 | problem evidence and current arrangements | intervention rationale | Demonstrate a problem and case for action before selecting a solution. |
| PA02 | rationale, jurisdiction, population, horizon | scope and business-as-usual counterfactual | Social value is incremental to an explicit baseline. |
| PA03 | rationale, commitments, needs | objectives, critical constraints | Objectives describe outcomes, not a preferred means. |
| PA04 | objectives and intervention dimensions | option longlist | Generate materially distinct options including BAU/do-minimum. |
| PA05 | longlist, criteria, feasibility evidence | shortlist and rejection log | Apply criteria consistently; failed options return for redesign. |
| PA06 | shortlist, BAU, delivery assumptions | comparable option models | Specify options at comparable maturity and expose dependencies. |
| PA07 | option models, scope, evidence | social impact register | Include material effects and bearers beyond fiscal flows. |
| PA08 | impacts, quantities, values, timing | valued and non-monetised impacts | Monetize defensibly; keep unmonetized effects visible. |
| PA09 | valued impacts, discounting, costs | social-value metrics | Aggregate incrementally without erasing composition or double counting. |
| PA10 | non-monetised impacts, criteria, scores, weights | structured assessment | Weights are value judgments; additive MCDA is not the sole decision rule. |
| PA11 | impacts and population segments | distributional profile | Show who gains and loses rather than relying on averages. |
| PA12 | options, metrics, distribution, uncertainty | risk cases, sensitivities, switching values | Test whether rankings survive plausible uncertainty. |
| PA13 | all appraisal strands and constraints | comparative option case | Integrate transparently; do not collapse conflicts into one opaque score. |
| PA14 | comparative case and adequacy | conditional advice or no preference | Advice is not approval; refusal is valid when evidence cannot distinguish options. |
| PA15 | advice, accountable decision, monitoring plan | decision pack, feedback requirements | Preserve analyst/decision-maker boundary and create a future learning loop. |

## Agent-based policy simulation

| Step | Consumes | Produces | Method-owned boundary / refusal |
| --- | --- | --- | --- |
| AB01 | policy question, alternatives, target patterns | bounded model purpose | Simulation claims remain conditional, not direct policy-world predictions. |
| AB02 | purpose and domain concepts | entity/state schema and scales | Interacting heterogeneous agents distinguish this ABM variant. |
| AB03 | entities and policy rules | ordered process schedule | Scheduler ordering is a substantive structural assumption. |
| AB04 | schema, schedule, behavioral assumptions | decision and interaction rules | Macro patterns must emerge from explicit micro-rules. |
| AB05 | schema, observed inputs, parameter definitions | initialization, mappings, submodels | Keep observed inputs separate from generated trajectories. |
| AB06 | ODD description and runtime | executable model, description-code map | Documentation is not implementation; expose semantic correspondence. |
| AB07 | executable model and behavioral oracles | verification result | Verification tests code against specification, not fitness to the world. |
| AB08 | verified model, observed patterns, criteria | empirical-fitness appraisal | Fit is bounded to named external patterns; self-generated output cannot validate structure. |
| AB09 | model, policies, outcomes, replications | experiment manifest | Freeze policy contrasts and controls so alternatives are not confounded. |
| AB10 | parameters, inputs, assumptions, ranges | uncertainty sampling design | Propagate plausible uncertainty rather than hide it behind a baseline. |
| AB11 | model, experiment, uncertainty, seeds | immutable run ensemble | Generated trajectories retain run identity; prohibit selective reruns. |
| AB12 | ensemble and outcome definitions | policy-pattern contrasts and uncertainty | Infer only within the executed model and declared design. |
| AB13 | ensemble, uncertainty design, contrasts | parameter/input sensitivity | Attribute variation within declared ranges and disclose interactions. |
| AB14 | model variants and matched experiments | structural sensitivity | Scheduler, behavior, network, and submodel alternatives are not mere parameters. |
| AB15 | verification, fitness, sensitivities, run evidence | pass/refuse decision and limitations | Refuse when decisive verification, fitness, provenance, or sensitivity gaps remain. |
| AB16 | passed gate, contrasts, limits, ODD | conditional conclusion and replication package | Report generated evidence as model-conditional, never as observed policy effect. |
