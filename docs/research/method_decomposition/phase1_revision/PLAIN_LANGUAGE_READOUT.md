# What the revised decomposition tells us

## The short version

We are not trying to build one giant “policy-analysis method.” We are trying to
build a system with:

1. common workflow machinery;
2. reusable patterns for organizing work and review;
3. specialized method modules that retain their own rules.

That is the likely route to broad coverage without flattening analytical
methods into generic verbs.

## What can probably be built once

These capabilities recur without requiring the system to pretend that two
analytical judgments mean the same thing:

- give evidence and artifacts stable identities and versions;
- preserve exact sources, provenance, and transformations;
- pass an artifact from one operation to another;
- retain earlier context across several later operations;
- freeze a plan or decision before protected information becomes available;
- branch, join, loop, and prohibit invalid workflow transitions;
- present evidence and criteria for human or method-owned review;
- record uncertainty, disagreement, qualifications, and refusal;
- distinguish an analyst's work from a value setter, reviewer, recommender, or
  accountable decision-maker;
- project the same underlying artifact into text, tables, graphs, or reports.

This is meaningful shared infrastructure, but it is mostly the machinery that
makes analysis composable and traceable—not the analytical reasoning itself.

## What may share a shell

Several recurring patterns could use common software around a method-specific
interior:

- **Screen:** show subjects and criteria, record a decision and rationale, then
  include, exclude, return, or escalate.
- **Appraise:** assemble relevant evidence, obtain a method-owned judgment,
  record its basis, and qualify or refuse when support is inadequate.
- **Compare:** align alternatives on declared dimensions, preserve conflicts,
  and return a structured comparison without assuming one universal scoring
  rule.
- **Stress:** vary declared assumptions, show what changes, and record whether
  a conclusion is robust, conditional, fragile, or indeterminate.
- **Review and accept:** present a versioned artifact with evidence and limits,
  record reviewer action, and preserve the superseded version.

The shell handles presentation, identity, review, and workflow. The method
module decides what counts as eligibility, adequacy, diagnostic force,
identification, social value, or robustness.

## What should remain specialized

Examples from the three-method pilot include:

- grounded-theory constant comparison, theoretical sampling, category
  adequacy, and reflexive integration;
- RCT estimands, concealed randomization, intention-to-treat estimation, and
  causal interpretation;
- policy-appraisal intervention rationale, social valuation, distributional
  treatment, weighting, and recommendation logic.

Specialized does not mean isolated. Each module can still consume and produce
traceable artifacts through common boundaries.

## How this fits the larger Evidence-to-Action vision

```text
Messy policy question
  → choose and configure appropriate method modules
  → run them through shared workflow machinery
  → preserve evidence, artifacts, judgments, uncertainty, and alternatives
  → connect outputs into later methods when the handoff is legitimate
  → produce advice while retaining the boundary to accountable decisions
  → reuse the accumulated knowledge in the next investigation
```

The eventual product can let a user begin with a question and assemble or
recommend a workflow without assuming the workflow is linear. A method may be
a sequence, DAG, cycle, or combination. The common system executes and exposes
the topology; each method module owns why its moves are valid.

## A better way to assess coverage

We should not calculate coverage by counting how many row labels are shared.
Instead, for each selected method, ask:

- Are all required analytical moves represented?
- Can the shared machinery execute its topology and preserve its artifacts?
- Which moves use a reusable shell plus method-owned judgment?
- Which method-owned moves have an actual implementation?
- Where must the system refuse because evidence, authority, or capability is
  missing?

This produces a method-by-capability coverage matrix. Later, once a defensible
portfolio is frozen, it can reveal the highest-leverage missing modules. Until
then, a global “80 percent covered” number would be selection-sensitive and
misleading.

## How the revised format addresses the audit findings

| Audit finding | Revised treatment |
| --- | --- |
| The same methods produced 70, 85, 87, and historically 90 steps. | Separate broad phases, analytical moves, and execution actions; do not use raw row count as capability evidence. |
| Twenty required arrows did not transfer compatible data. | Every arrow is typed as artifact flow, retained context, control gate, feedback, or prohibited transition. |
| Important intermediate artifacts disappeared during compression. | Split when an artifact can be reviewed, handed off, targeted by feedback, or changes the warrant. |
| Exact anchored observations disappeared from the compact process-tracing path. | Every move names its inspectable output and information origin; missing required artifacts remain visible failures. |
| Performer, reviewer, value setter, recommender, and decision-maker were conflated. | Record performer, judgment owner, acceptance/review authority, recommender, value/goal authority, and decision authority separately. |
| Simulated output risked looking like observed evidence. | Preserve information origin across every move and handoff. |
| Prespecification was represented as ordinary forward ordering. | Allow temporal/access barriers and prohibited transitions, not only directed edges. |
| The compact systematic-review row exceeded the frozen source scope. | Every method move retains its source basis; source-scope mismatches block promotion. |

## What the wider stress test added

The recommended six-method sample is now complete. It found four changes worth
retaining:

- state each result's method-owned applicability boundary without inventing one
  universal `scope`;
- record source authority or inferential role separately from information
  origin;
- distinguish preserving, transforming, and lossy artifact handoffs; and
- allow one catalog label to compose several methods rather than forcing it
  into one workflow.

The legal/institutional label was the clearest example of the fourth point:
legal-authority analysis and institutional implementation mapping answer
different questions and reconcile only at a later policy-feasibility move.

## Accepted Phase 2 disposition

Brian accepted the revised instrument as the Phase 2 discovery format on
2026-08-13. Preserve the 70-row flat candidate as a failed instrument rather
than repairing it into a universal schema. The accepted format does not make
the populated pilot records or their provisional vocabularies canonical.

The completed hostile sample is a stress test, not selection of the Phase 2b
portfolio. Existing verbs remain a coarse discovery input. `analysis_plan`
remains provisional for further testing rather than a closed shared enum.
Phase 2b must still propose a portfolio for Brian's approval.

Do not yet build a shared schema or broad capability service. Promotion still
requires three materially different methods plus a deliberate fourth hostile
case; the two-authentic-seam rule is a separate workbench adoption gate. After
those decisions, an authentic simulation-to-policy-appraisal handoff is the
strongest currently proposed seam test. It must preserve model-conditional
generated evidence and would not by itself justify shared infrastructure. No
collision scoring, capability promotion, infrastructure, or product
implementation is authorized by the format decision.
