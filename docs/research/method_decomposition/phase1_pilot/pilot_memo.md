# Phase 1 pilot memo

Status: audited but collision-blocked discovery pilot; stop before portfolio
selection and broader catalog decomposition

## Result

The original six transient reports were summarized as 90 source-derived
operations but were not preserved, so that claim cannot be independently
audited. A concise audit recovery produced 85 operations and a subsequent
detailed recovery produced 87. A compact
integration candidate contains 70 operations and 78 directed workflow edges
across five methods plus an agent-based-simulation stress test. The different
counts, rerun instability, and row-level losses are unresolved evidence, not something averaged
away. See `blind_reruns/`, `integration_findings.md`, and
`structural_gaps.yaml`.

| Method | Operations | Topology that must survive |
| --- | ---: | --- |
| Systematic review | 12 | planned path with conditional pooling and bounded search returns |
| Constructivist grounded theory | 12 | concurrent coding, comparison, memoing, and theoretical-sampling cycles |
| Theory-testing process tracing | 12 | rival-relative evidence appraisal with evidence-gap-driven returns |
| RCT causal-effect estimation | 12 | prespecified DAG with prohibited outcome-informed redesign |
| Policy option appraisal | 12 | branching appraisal plus later monitoring/evaluation feedback |
| Agent-based policy simulation | 10 | specification/verification and structural-sensitivity cycles |

The exercise supports the reconciled Phase 0 warning: repeated verbs are useful
candidate finders, but they do not demonstrate semantic equivalence. Most
analytically consequential operations contain a method-owned validity judgment.

## What genuinely appears reusable

The pilot leaves a narrow shared-mechanics hypothesis worth testing, but does
not strengthen it where the compact candidate lacks the claimed artifact:

- identity and typed input/output boundaries;
- source or artifact custody and exact references as a requirement; the compact
  process-tracing candidate does not yet produce an exact `passage_anchor`;
- declared parameters and prespecified plans;
- lineage, review state, uncertainty, and explicit information loss;
- branching, returns, refusal, and terminal unresolved states;
- projection of a method-owned result into another view.

These are not yet promoted shared infrastructure. The pilot did not demonstrate
two authentic compatible producer/consumer seams for any new implementation.

Several operations may support a shared shell with a method-owned interior:
search, acquire, screen, compare, appraise, synthesize, perturb, test, and
review. That is only a candidate classification. For example, eligibility
screening, source admissibility in process tracing, and simulation verification
all apply criteria, but the criteria license different conclusions and their
failure states are not interchangeable.

## Method-owned capabilities that must not be flattened

- Systematic review owns study eligibility, risk-of-bias judgments,
  synthesis comparability, and certainty of an effect body of evidence.
- Grounded theory owns theoretical significance, category development,
  theoretical sampling, adequacy, and reflexive integration.
- Process tracing owns rival construction, predicted evidence, source fitness,
  diagnostic likelihood judgments, and calibrated within-case conclusions.
- RCT analysis owns the estimand, randomization warrant, prespecification,
  missing-data and intercurrent-event handling, and causal interpretation.
- Policy appraisal owns intervention rationale, social value, distributional
  treatment, decision criteria and weights, and the boundary between analysis
  and accountable choice.
- Agent-based simulation owns model structure, behavioral rules, verification,
  calibration, experiment design, and the conditional scope of simulated
  results.

## Schema stresses found

### 1. Method variants have to be frozen

The method name alone is too broad. A realist review, a qualitative synthesis,
and a pairwise intervention-effect review would not share this review workflow.
Theory-building process tracing differs from the frozen theory-testing variant.
A quasi-experimental causal design replaces random assignment with a
design-specific identification argument; it is not an RCT parameter.

### 2. Topology is substantive, not display metadata

Grounded-theory cycles are required by the method. The RCT path instead has
prohibited returns: allowing primary results to silently redefine the estimand
or analysis plan changes the status of the claim. A representation limited to
an ordered checklist would therefore misrepresent both methods.

### 3. Actor, authority, and judgment ownership are not the same thing

The frozen methodology sources usually describe work by a human analyst. That
does not prove the operation cannot be partly automated, and an automated shell
does not transfer ownership of the analytical judgment. Policy appraisal also
showed that supplying evidence, making a judgment, authorizing objectives or
weights, recommending, and deciding are different roles. A later revision
should distinguish the actor performing an operation from the role authorized
to provide values, accept its method-owned judgment, or make the decision.

### 4. Ideal-method and implementation statuses should remain separate

`execution_status` and `representation_status` are informative when checking
existing code, but nearly constant in a source-derived ideal decomposition.
They should remain available for reality checks without being treated as
method semantics or collision keys.

### 5. One controlled type was missing

`analysis_plan` is needed for a prespecified empirical or evaluation design.
Using `review_protocol` for RCT and policy evaluation would create a false
collision; using `configuration` would discard prespecification and deviation
semantics. The addition and its two uses are documented in
`type_additions.md`.

### 6. Generated evidence needs an explicit epistemic origin

Simulation stressed a distinction not safely carried by the current type list:
a `model_run` is produced evidence about a model under assumptions, not an
observation of the policy world. Before a broader catalog, test a field such as
`epistemic_origin` with at least `observed`, `elicited`, `derived`, and
`simulated`. Do not adopt that vocabulary from this single example.

### 7. Temporal and version barriers are load-bearing

An RCT's prespecification boundary depends on when a change occurred and who had
access to outcome-by-arm information. A policy evaluation result must create a
new appraisal version rather than overwrite its predecessor. Process tracing
must distinguish predictions and priors recorded before evidence appraisal from
posterior judgments. Edge direction alone cannot carry these constraints.

### 8. Failure outputs and supported conclusions are load-bearing

The same nominal output can license different claims. Recording what a step may
conclude, and what it returns when it cannot, prevented pooling refusal,
unresolved rivals, exposed deviations, non-robust policy rankings, and
model-conditional simulation results from becoming generic “findings.”

## Granularity and typing findings

- The handoff-based granularity rule was workable at 10–12 operations per
  method, but some rows still contain tightly coupled subjudgments. Splitting
  them further would aid method implementation while reducing useful
  cross-method collision.
- The compact integration candidate uses no multi-primary-subject exceptions:
  0 of 70 operations. The blind lanes nevertheless found genuine compound
  subjects and additional authority/evidence/control roles. The zero count may
  therefore reflect compression rather than a successful schema property.
- No new verbs were required. This is evidence that the verbs are adequate
  discovery buckets, not evidence of shared analytical implementations.
- `operation_kind` helped prevent runtime delivery from inflating analytic
  coverage. Boundaries remain contestable for search, data collection, protocol
  construction, and monitoring plans; each classification therefore retains a
  source and stated conclusion.
- Literature review is not merely a universal first step. The frozen
  systematic review is a complete effect-synthesis method. Other reviews can
  orient a study, map a field, synthesize mechanisms, or produce an evidentiary
  conclusion, and must be decomposed as distinct variants later.

## Source and uncertainty limits

- PRISMA and CONSORT constrain reporting; they do not replace the conduct and
  inferential sources used here.
- Chapter-level book references identify the controlling method sections but
  do not encode every judgment as a deterministic rule.
- The policy-appraisal workflow follows the current Green Book variant and does
  not claim to cover legal analysis, political authorization, implementation,
  or ex-post impact evaluation.
- The simulation result is a hostile stress test, not a sixth portfolio member
  and not evidence that all methods begin with source-document acquisition.
- This phase deliberately did not calculate global reuse coverage or
  adjudicate collisions. A percentage over these six deliberately selected
  methods would be selection-sensitive and premature.

## Proposed revision before the broader portfolio

Retain the structured rows and graph edges, but make only these candidate
changes for human approval:

1. Add `analysis_plan` to the pilot type vocabulary.
2. Test, rather than adopt, an `epistemic_origin` field on outputs.
3. Separate operation performer, value/goal authority, judgment acceptance,
   recommendation, and decision rights.
4. Test a temporal/version barrier for prespecification and cross-run feedback.
5. Treat execution and representation status as implementation-evidence fields,
   not collision semantics.
6. Keep `conclusion_supported`, `failure_output`, method-owned semantics, and
   prohibited topology explicit.

No collision grouping, broader portfolio, or RAND-method normalization should
start while `structural_gaps.yaml` or a `compressed_with_loss`/`missing`
reconciliation remains unresolved.
