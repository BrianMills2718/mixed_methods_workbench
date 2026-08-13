# Capability-pressure readout from the hostile sample

Status: exploratory architecture evidence; no shared-capability adoption

## Bottom line

The broader sample supports a small reusable workflow substrate and several
reusable interaction/orchestration shells. It does **not** support a universal
analytical capability library.

The instrument is useful because it now exposes three different outcomes:

- stable mechanics that can preserve work across methods;
- repeatable shells whose analytical judgment must remain method-owned;
- operations that only look shared until their warrant, object, or permitted
  conclusion is inspected.

No global reuse percentage is calculated. The sample was selected to challenge
the instrument, not to estimate the frequency of policy-analysis work.

## Method-selection logic exercised by this sample

Selection is based on the conclusion sought and the available source of
inferential leverage, not on a single ladder of ambition. Several routes may be
needed in one investigation.

| Need | Route in this sample | Required leverage | Important non-claim |
| --- | --- | --- | --- |
| Synthesize what eligible intervention studies collectively establish | Systematic review, with meta-analysis only when defensible | Prespecified eligibility, systematic discovery, result-level appraisal, compatible synthesis | Publication counts or a pooled number do not repair biased/incompatible studies |
| Explain how a bounded outcome occurred and discriminate among causal processes | Theory-testing Process Tracing | Frozen rivals, within-case evidence opportunities, comparative diagnostic appraisal | Does not estimate a population average effect |
| Predict a named quantity at a future horizon | Operational time-series forecasting | Time-respecting data and held-out rolling-origin performance | Predictive accuracy does not establish causal explanation or intervention effects |
| Identify configurations that are necessary or sufficient across cases | fsQCA | Defensible set calibration, truth-table comparison, limited-diversity decisions, return to cases | Solution terms are not temporal mechanisms or average marginal effects |
| Explore what an explicit model generates under alternative configurations | Agent-based simulation experiment | Inspectable mechanisms, verified implementation, frozen experiments, replication and sensitivity | Model-generated behavior is not observed real-world confirmation |
| Determine what a policy option is legally allowed to do and whether institutions can implement it | Composed legal-authority and institutional-mapping route | Current controlling authority plus mandate, capacity, dependency, and practice evidence | Lawfulness, implementability, desirability, and accountable choice are distinct |

The router should allow multiple routes and preserve their handoffs. For
example, a systematic review may parameterize a simulation, simulation may
inform option appraisal, and legal/institutional analysis may eliminate or
redesign options. None of those handoffs makes the upstream and downstream
methods the same capability.

## Pressure matrix

`M` means a credible shared-mechanics candidate. `S` means a shared-shell
candidate with method-owned meaning. `L` means the capability remains local to
the method. Multiple values are intentional.

| Capability pressure | SR | PT | Forecast | fsQCA | Simulation | Legal + institutional | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Stable artifact identity and version | M | M | M | M | M | M | Strong mechanics candidate |
| Exact source/data/model/run custody | M | M | M | M | M | M | Shared custody mechanics; artifact types remain distinct |
| Applicability boundary | S/L | S/L | S/L | S/L | S/L | S/L | Common need, incompatible semantics; use typed method-owned boundary |
| Freeze a design before protected information | S | S | S | sometimes | S | sometimes | Shared shell where the variant requires it; each method defines what is protected and the consequence of exposure |
| Screen subjects against criteria | S | S | — | — | — | S | Shared review shell; criteria, subject, and exclusion meaning stay local |
| Appraise evidence or validity | S/L | S/L | S/L | S/L | S/L | S/L | Name collision at semantic level; share presentation/review mechanics only |
| Compare alternatives | L | L | L | L | L | L | Homonym: studies, rivals, forecasts, configurations, runs, and interpretations license different claims |
| Sensitivity / robustness branch | S/L | S/L | S/L | S/L | S/L | S/L | Reusable branching shell; perturbations and interpretations are method-owned |
| Return to earlier work | M/S | M/S | M/S | M/S | M/S | M/S | Shared feedback/version mechanics; method controls when return is allowed |
| Refuse or qualify | M/S | M/S | M/S | M/S | M/S | M/S | Shared result state and review shell; refusal conditions remain local |
| Human/expert review boundary | M/S | M/S | M/S | M/S | M/S | M/S | Shared accountability record; expertise and authority are not interchangeable |
| Project into table/graph/report | M | M | M | M | M | M | Shared projection mechanics where semantics are not rewritten |

## Candidate shared mechanics

These recur without claiming analytical equivalence:

1. stable typed identity for source, dataset, case, model, run, result, and
   version;
2. content custody, provenance, and exact resolution;
3. derivation lineage and explicit input/output references;
4. immutable historical versions plus supersession links;
5. review state, reviewer identity, rationale, and accountable role;
6. explicit branches, gates, feedback, and prohibited transitions;
7. refusal and qualification as first-class outcomes;
8. projection to a UI, table, graph, export, or report without changing the
   producer-owned meaning;
9. declared information added, transformed, or lost at a handoff.

These are architecture hypotheses until two authentic, materially different
producer/consumer seams use the same boundary successfully.

## Candidate shared shells

The following shapes repeat, but the method module must supply criteria,
warrant, and permitted conclusions.

### Reviewed gate

```text
subjects + method-owned criteria + relevant evidence
  -> produce a proposed judgment and rationale
  -> accountable review
  -> continue | return | qualify | refuse
```

Examples: full-text eligibility, PT source admission, simulation verification,
legal-authority review, and option feasibility.

### Frozen design and protected evaluation

```text
freeze question/design/version
  -> restrict later information access
  -> execute or assess
  -> detect exposure/deviation
  -> preserve status | downgrade | refuse | create exploratory/new version
```

Examples: review protocols, PT rivals, RCT estimands, forecast folds, and
simulation experiments. Some QCA variants also distinguish calibration choices
made before versus after inspecting solution behavior, but that is not treated
as a universal QCA invalidity rule. What counts as exposure and what it
invalidates are method-owned.

### Alternative and sensitivity comparison

```text
freeze alternatives and comparison rule
  -> derive method-specific results
  -> perturb declared assumptions/inputs
  -> expose changes and failure boundaries
  -> retain | qualify | redesign | refuse
```

Examples: meta-analysis choices, rival likelihoods, forecast models, QCA
thresholds, simulation configurations, and legal interpretations. The shared
shell must never emit a generic winner or confidence score.

### Versioned feedback

```text
observe gap, anomaly, new evidence, outcome, or changed authority
  -> target an earlier artifact
  -> create a new version with lineage
  -> preserve the historical result
```

Examples: review updates, PT acquisition, forecast monitoring, return to QCA
cases, model revision, and legal/institutional updates.

## Capabilities that remain method-owned

- systematic-review eligibility, risk of bias, synthesis compatibility,
  meta-analysis, and certainty assessment;
- Process Tracing rivals, diagnostic likelihoods, mechanisms, comparative
  update, and verdict;
- forecast target/loss, time-respecting folds, predictive models, scoring,
  calibration, and drift response;
- QCA calibration, set relations, truth tables, remainders, minimization,
  consistency, and coverage;
- simulation abstraction, implementation correspondence, verification versus
  validation, experiment design, generated-evidence interpretation, and
  real-world extrapolation;
- legal hierarchy, interpretive method, application to facts, institutional
  mandate/capacity analysis, and the authority to issue legal advice.

## Instrument changes justified by the sample

### 1. Add a typed applicability boundary

Every analytical result should state where it applies, but there should not be
one universal `scope` object. The instrument should ask:

> Which method-owned boundary determines where this move or result is usable,
> and which change would require review or a new version?

Examples include review eligibility, PT case/outcome/period, forecast target and
information regime, QCA case population and calibration, simulation purpose and
model boundary, and legal jurisdiction/effective date.

### 2. Split information origin from source authority

`Observed`, `reported`, `interpreted`, `derived`, and `simulated` describe where
information came from. They do not say whether a source is legally controlling,
independently held out, eligible under a review protocol, or generated by the
model being assessed.

Add a plain-language prompt:

> What authority or inferential role does this input have here, and who or what
> establishes that role?

The answers remain method-owned; no universal evidence-strength scale follows.

### 3. Distinguish transfer from transformation

An artifact flow can be:

- **preserving:** the receiver consumes the producer artifact with its meaning
  unchanged;
- **transforming:** the receiver creates a new artifact or evidential role;
- **lossy:** the receiver cannot preserve some relevant source distinction.

This is metadata on an artifact-flow connection, not a sixth analytical
connection type. A transformation names the producing method and information
added/lost.

### 4. Permit composed method profiles

One inventory label may contain multiple methods or workstreams. A profile may
therefore contain named subprofiles with an explicit reconciliation move. The
legal/institutional case demonstrates this need. The same allowance may later
help with mixed-method reviews, evaluation-plus-economic-appraisal, or
simulation-plus-deliberation.

### 5. Make protected boundaries explicit

The existing `prohibited transition` type is adequate, but each method must
name:

- the protected artifact or information;
- when access becomes consequential;
- what transition is prohibited;
- whether violation invalidates, downgrades, or merely warns;
- whether a separately labeled new version is allowed.

This avoids treating circularity as a universal blocker. The method determines
whether it is a warning, qualification, downgrade, or invalidity condition.

## What did not need to change

- The phase / analytical-move / execution-action distinction survived.
- The original five connection types were enough after artifact flow gained
  preserving/transforming/lossy metadata.
- The four authority roles remain useful. Legal review reinforces, rather than
  replaces, the distinction between performer, judgment owner, goal/value
  authority, and decision authority.
- Nonlinear topology remained permissive rather than mandatory. Systematic
  review can be predominantly staged; forecasting operationally cycles; QCA and
  simulation return iteratively; legal and institutional tracks converge.

## Collisions and contract gaps exposed

| Apparent collision or gap | Finding | Required treatment |
| --- | --- | --- |
| `appraise` | Risk of bias, diagnostic force, forecast adequacy, QCA robustness, simulation validity, and legal authority differ | Share review mechanics only; namespace analytical result |
| `compare` | Objects and warranted conclusions differ across all six methods | No generic comparison result or winner |
| `case` | PT bounded case, QCA population member, review study, and legal factual situation differ | Typed references; no universal case semantics |
| `validation` | Software verification, empirical validation, predictive evaluation, legal currency checks, and review appraisal differ | Typed validation activities and result bodies |
| `update` | New evidence, realized outcomes, changed law, and model revision have different triggers | Share version/lineage mechanics; method owns trigger and consequences |
| `scope` | Eligibility, population, horizon, model boundary, and jurisdiction differ | Typed applicability boundary |
| legal/institutional inventory label | It composes authority interpretation and empirical implementation analysis | Split into subprofiles and reconcile explicitly |
| artifact flow | Current type hides semantic transformation and information loss | Add preserving/transforming/lossy metadata |

## Smallest next stress test

The strongest next challenge is not a seventh paper profile. It is one authentic
cross-method seam:

> Take a versioned simulation comparison and feed it into a policy-option
> appraisal as one explicitly model-conditional consequence estimate, while
> retaining the model boundary, configurations, uncertainty/sensitivity, and
> the fact that simulated output is not observed policy evidence.

Why this seam:

- it tests preserving versus transforming handoffs;
- it crosses generated evidence into a decision workflow without merging their
  warrants;
- it forces applicability, uncertainty, values, and decision authority to
  remain separate;
- it can use an existing Cybernetic Influence/Concordia-family artifact only if
  current repository evidence shows a suitable retained comparison; otherwise
  the result should be a precise missing-contract finding, not a fixture passed
  off as adoption.

Success would not justify a universal schema. It would supply one of the two
authentic seams required before proposing shared infrastructure for this
boundary.

## Explicit uncertainties

- Six deliberately diverse profiles are enough to find breakage, not enough to
  estimate the prevalence of capabilities across policy work.
- Legal analysis is jurisdiction-specific; the U.S. federal statutory example
  must not control other jurisdictions or forms of law.
- Institutional mapping spans formal and informal evidence and may need its own
  family of profiles.
- QCA schools and software practices differ; this sample covers one fsQCA
  theory-oriented variant.
- Forecasting beyond historical time-series patterns, including expert
  elicitation and structural or scenario forecasts, will stress different
  capabilities.
- Agent-based modeling does not cover system dynamics, discrete-event
  simulation, wargaming, or participatory simulation.
- Shared shells may be reusable as UI/orchestration patterns without deserving
  one shared analytical implementation.
