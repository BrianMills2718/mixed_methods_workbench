# Revised method-decomposition instrument

Status: accepted Phase 2 discovery instrument; not a canonical production schema

Acceptance: Brian approved this narrow direction on 2026-08-13. Acceptance
covers the three levels, `operation_kind` at Levels 2 and 3, typed connections,
six authority roles, information origins, temporal/access/version guards, and
exact anchors. It does not accept the populated pilot records as a universal
model or close the provisional vocabularies.

- Request mode: write the approved design artifact.
- Design depth: Standard.
- Execution profile: exploratory documentation/research.
- Activated overlays: target outcome, exploratory readout, and cross-project
  authority boundaries.
- Landscape disposition: `linked`.

## What this is for

The objective is to discover which parts of policy analysis can be built once
and reused across many methods without erasing what makes each method valid.

The actor is the research-architecture reviewer. The recurring job is:

> Take a named method variant, describe how it actually works, and distinguish
> reusable workflow machinery from method-owned analytical judgment.

The inspectable result is a plain-language workflow that another reviewer can
trace from inputs to conclusions, including branches, returns, refusals, and
human decisions.

## Why the first format failed

The Phase 1 audit found 70, 85, 87, and historically claimed 90-step accounts
of the same six method variants. The problem was not simply inconsistent
analysts. One row was being asked to represent three different things:

1. a broad phase of a method;
2. a meaningful analytical move that changes what may be concluded;
3. an execution action performed by a person or software system.

For example, “screen studies” can be one phase, two analytical decisions
(initial screening and full-text eligibility), or many execution actions. All
three descriptions can be useful. Forcing them into one flat list makes the
number of rows arbitrary and creates false matches between methods.

## The revised three-level model

### Level 1 — Method phases

Phases are human-readable landmarks such as “design the study,” “collect
evidence,” or “appraise options.” They help someone understand the overall
journey.

Phases are allowed to be broad. Their number is not used to infer reuse. Each
phase records the set of `operation_kind` values present in its child moves so
aggregation cannot hide support or delivery work.

### Level 2 — Analytical moves

An analytical move is the main comparison unit. It is a bounded act that:

- consumes identifiable inputs;
- produces an independently inspectable artifact or decision;
- changes what the analysis may conclude, what must happen next, or whether the
  method must refuse to continue.

Examples include freezing an RCT estimand, deciding whether studies may be
pooled, or judging whether a grounded-theory category is sufficiently
developed.

Analytical moves remain method-owned unless evidence demonstrates otherwise.

### Level 3 — Execution actions

Execution actions describe how a move is currently carried out: database
queries, model calls, human coding, validation routines, API calls, interface
review, or file production.

These actions are essential for implementation audits, but they are not method
semantics. Different implementations may realize the same analytical move.

Every Level 2 move and Level 3 action retains exactly one rev-5.1
`operation_kind`: `analytic`, `methodological_support`, or `runtime_delivery`.
Level 1 records retain the exact set represented by their children. No kind is
dropped from collision discovery; rev-5.1 exclusions apply only to the abort
gate.

```text
METHOD PHASE
  └── ANALYTICAL MOVE
        ├── human or software execution actions
        ├── produced artifact
        ├── method-owned judgment
        └── allowed conclusion or refusal
```

## When to split an analytical move

Split a move when at least one of these is true:

- an intermediate artifact can be independently reviewed or handed off;
- the intermediate result changes the method's warrant or permitted claim;
- a different actor or authority becomes responsible;
- observed, elicited, derived, or simulated information crosses a boundary;
- a branch, refusal, or feedback loop can target the intermediate result;
- failure at the intermediate point requires a materially different response.

Keep actions together when the difference is only an implementation detail,
presentation choice, or convenient subdivision with no independently
meaningful output or decision.

This rule does not guarantee one universally correct step count. It makes
different decompositions comparable by requiring the reason for every split.

## What each analytical move records

The instrument records the following in plain language. A machine-readable
schema may follow only after this survives broader use.

| Field | Question answered |
| --- | --- |
| Method variant | Exactly which form of the method is this? |
| Parent phase | Where does this move sit in the understandable journey? |
| Move | What meaningful analytical act occurs? |
| Inputs | What existing evidence, artifact, assumption, or decision does it use? |
| Output | What inspectable artifact, judgment, or state does it create? |
| Information origin | Is the information observed, reported, elicited, interpreted, derived, or simulated? |
| Source authority or inferential role | Why may this input play this role here, and who or what establishes that status? |
| Applicability boundary | Where is the move or result usable, and which change requires review or a new version? |
| Method-owned rule | What can only this method legitimately judge? |
| Permitted conclusion | What can now be said that could not be said before? |
| Refusal or qualification | What result is returned when the move cannot support that conclusion? |
| Performer | Who or what carries out the work? |
| Authority | Who may set goals or values, accept the judgment, recommend, or decide? |
| Incoming/outgoing connections | Does the connection carry an artifact, retained context, permission, control, or feedback? |
| Implementation evidence | Is it manual, executable software, an implemented artifact, incomplete software, or design only? |
| Source basis and exact anchors | Which frozen source locator and which compact/rerun records ground this move? |
| Temporal/access/version guards | What must precede what, who may inspect protected information, and which immutable version is in force? |

## Five connection types

The old graph assumed that most arrows transferred the output of one row into
the next. Twenty required arrows did not. The revised graph distinguishes:

1. **Artifact flow** — an output becomes a downstream input.
2. **Retained context** — both moves use the same earlier artifact; it is not
   recreated by the intervening move.
3. **Control gate** — a judgment permits or blocks the next move without
   becoming its analytical input.
4. **Feedback** — a later result requests revision, more evidence, or a new
   version of earlier work.
5. **Prohibited transition** — taking this route would invalidate or downgrade
   the analysis, such as rewriting an RCT estimand after seeing outcomes.

Every connection names its type. A graph is invalid if an apparent artifact
flow has no compatible output and input.

An artifact-flow connection also states whether it is **preserving**,
**transforming**, or **lossy**. A transforming or lossy handoff names the
method responsible for the transformation and the information added, changed,
or unavailable to the receiver.

One inventory label may contain multiple methods. In that case, the instrument
uses named subprofiles and an explicit reconciliation move rather than forcing
the label into one artificial workflow.

## Six authority roles

“Human in the loop” is too vague. The instrument distinguishes:

- **performer** — carries out the operation;
- **judgment owner** — is accountable for the method-specific assessment;
- **acceptance authority** — accepts or rejects that assessment for the
  workflow without thereby making the policy decision;
- **recommender** — owns advice presented to a decision-maker;
- **value or goal authority** — supplies objectives, criteria, weights, or
  priorities;
- **decision authority** — accepts, rejects, or acts on advice.

One person can occupy several roles. They remain separate because automation of
the performer does not automatically transfer judgment, acceptance,
recommendation, value-setting, or decision authority. Use `none` where a role
does not exist; do not infer it from the performer.

## Temporal, access, and version guards

Each move records `temporal`, `access`, and `run_version` guards. They capture
ordering/freeze rules, protected-information access, and immutable artifact or
run identity plus successor-version behavior. If a future method cannot
express a guard, the field is `blocked` with a reason; absence never implies
that the issue is solved.

## How reuse is classified

The instrument does not collide rows merely because their verbs match. It asks
what can actually be reused.

### Shared mechanics candidate

The reusable part is method-neutral machinery such as stable identity,
versioning, custody, validation, lineage, review state, branching, feedback,
refusal, and projection into a table, graph, or report.

### Shared shell candidate

The workflow shape can be reused, but the judgment remains supplied by a method
module. For example:

```text
take subjects + criteria
→ present the relevant evidence
→ obtain a method-owned judgment
→ record rationale and reviewer
→ continue, qualify, return, or refuse
```

Eligibility screening, source-fitness appraisal, and option shortlisting may
use such a shell while retaining incompatible criteria and conclusions.

### Method-owned capability

The move's warrant and output are specific to the method: random assignment,
theoretical sampling, diagnostic likelihood appraisal, social valuation, QCA
calibration, or forecast backtesting.

## Collision test

Two moves are candidates for reuse only when all of these agree:

- they are described at the same level;
- their inputs and outputs have compatible roles;
- they license the same kind of downstream action;
- failure or refusal has the same operational meaning;
- actor and authority boundaries are compatible;
- information origin is preserved;
- workflow connections can be reused without changing method validity.

If only the surrounding workflow agrees, classify a shared shell. If the
warrant or conclusion differs, keep the capability method-owned.

Collision participation is level-specific. Level 1 phases never collide.
Level 2 analytical moves collide only with Level 2 moves. Level 3 execution
actions participate, including analytic, methodological-support, and
runtime-delivery actions, but only against Level 3 actions. A Level 3 match
cannot prove that its parent moves are the same. Cross-level matches are
invalid.

No capability is promoted from this instrument alone. Rev-5.1's threshold is
unchanged: the capability must appear in **three materially different methods**
and survive a deliberate attempt to break it with a **fourth**, chosen as a
hostile case. Two authentic compatible producer/consumer seams are an
additional workbench adoption requirement, not a replacement for that test.

## Exploratory readout

This format succeeds at the pilot stage if:

- a reviewer can understand the workflow without reading YAML;
- disagreements about step count can be localized to phase grouping or
  execution detail;
- meaningful split decisions are justified by artifacts, warrants, authority,
  origins, or topology;
- every arrow has an explicit connection type;
- missing capabilities and refusals remain visible;
- apparent reuse separates mechanics, shells, and method-owned interiors.

It fails if reviewers still disagree about the identity of analytical moves,
if the same move changes meaning across methods, or if important distinctions
must again be hidden to make operations collide.

## Material uncertainties

- Whether analytical-move identity remains stable when applied to a broader
  portfolio is unknown; this is the main question the instrument measures.
- Method phases may ultimately be presentation metadata rather than a durable
  contract field.
- The five connection types survived the six-method hostile sample, but they
  remain untested for deliberation, negotiation, participatory methods,
  wargaming, and multi-stage mixed-method integration.
- Applicability is a recurrent field, but review eligibility, a PT case,
  forecast horizon, simulation boundary, and legal jurisdiction must not be
  collapsed into one method-neutral scope semantics.
- Information origin does not establish source authority or inferential role;
  those remain separately declared and method-owned.
- The information-origin categories are useful distinctions, not an adopted
  closed vocabulary.
- Shared shells may prove reusable in user experience and orchestration without
  justifying one shared analytical implementation.
- A later method portfolio still needs a defensible selection rule before any
  coverage statement is meaningful.

## Boundaries and non-claims

- This is not a universal ontology of policy analysis.
- It does not establish a correct number of steps per method.
- It does not prove that candidate shells should share production code.
- It does not select the broader RAND-derived method portfolio.
- It does not measure percentage coverage.
- It does not alter producer-owned contracts or analytical engines.
- It does not select the Phase 2b/Phase 3 portfolio, run Phase 4 collisions, or
  issue Phase 5 adjudication verdicts.
- It does not promote any capability or authorize infrastructure, analytical,
  or product implementation.

## Consulted authority and evidence

- `docs/research/method_decomposition/comparison_v0.md`
- `docs/research/method_decomposition/phase1_pilot/pilot_memo.md`
- `docs/research/method_decomposition/phase1_pilot/integration_findings.md`
- `docs/research/method_decomposition/phase1_pilot/structural_gaps.yaml`
- `docs/research/method_decomposition/phase1_pilot/blind_reruns/`
- `docs/MIXED_METHODS_CAPABILITY_MAP.md`
- `docs/ROADMAP.md`

This instrument extends those authorities and evidence records rather than
replacing them.
