# Row-schema findings from executable code

The pilot should not use the original row schema unchanged. These changes are
required by the four observed systems.

## 1. Represent topology outside the step row

`repeatable: true` cannot distinguish batch iteration, bounded repair,
conditional retry, analyst-directed feedback, or fan-out. Keep step signatures
in `steps.yaml` and express control flow in `edges.yaml` with:

```yaml
from_step:
to_step:
edge_kind: required | optional | branch | loop | feedback | failure
condition:
transfers:
```

This permits linear, DAG, branching, and cyclic workflows without treating any
one shape as the default.

## 2. Use named slots, not input/output type sets

Grouping on an unordered set of types loses cardinality, role, and identity.
For example, Process Tracing consumes one frozen rival set and one current
evidence inventory. Calling both `claim_set` is insufficient unless their slot
names remain visible.

Each slot therefore needs:

```yaml
slot_name:
  type:
  cardinality:
  optional:
```

Collision may begin with coarse types, but adjudication must inspect slot names,
cardinalities, preconditions, and transferred fields.

## 3. Separate evidence from implementation

The proposed `provenance: code | doc | inferred` field conflates two questions.
Use:

- `evidence_basis`: what supports the row (`code`, `test`, `fixture`, `doc`, or
  `inferred`);
- `implementation_status`: whether the operation is `executable`,
  `represented_manual`, `incomplete`, or `planned`;
- `actor`: deterministic software, LLM, human, or a declared combination.

Mist Trail proves why this matters: its consequence judgments and conditional
recommendation exist in code as typed data, but code does not perform those
analytical judgments.

## 4. Do not split prompt-internal reasoning into fictional capabilities

One structured QC call emits incidents, comparisons, categories, memos, a core
process, relationships, and propositions. The intellectual method describes a
sequence; the software exposes one operation. Phase 0 records the runnable
boundary and lists the bundled method semantics rather than manufacturing seven
steps.

The pilot should record both:

- `executable_granularity`: the real callable or handoff boundary;
- `internal_method_phases`: optional descriptive phases that are not separately
  executable.

Only executable granularity participates in code-reuse coverage.

## 5. Freeze the method variant

`process_tracing`, `policy appraisal`, and `systematic review` are families, not
single workflows. Each decomposition must declare a variant, scope, and
authoritative method sources. Otherwise differences between two analysts may be
variant drift rather than schema failure.

The Phase 0 variant identifiers are in `README.md`. The pilot needs equivalently
specific definitions before decomposition begins.

## 6. Record actor transitions

Actor is architecturally meaningful. These systems repeatedly separate:

- LLM semantic production;
- deterministic validation/projection;
- independent LLM audit;
- human judgment or admission;
- deterministic computation.

A shared shell may coordinate these transitions even when it cannot own the
analytical judgment.

## 7. Make refusal and qualified completion first-class

Refusal is sometimes a step and sometimes a terminal state reached from many
validators. Store terminal states in the workflow graph, including:

- invalid/custody-drift refusal;
- unresolved but useful completion;
- preflight-only stop;
- publication blocked;
- evidence-acquisition requested;
- completed with explicit limitations.

Do not force every refusal into a normal data-transformation row merely to make
it countable.

## 8. Separate method semantics from shell behavior

`method_owned_semantics` must remain mandatory. It should answer: what judgment
would become wrong or misleading if a generic implementation supplied it?

The shared shell, if one exists, belongs in a later adjudication field and must
state only what common code would do: iterate, validate, invoke a producer,
record revisions, gate, or project. It must not claim the delegated judgment.

## 9. Record execution evidence separately

Code presence is not a fresh runtime receipt. Add optional fields:

```yaml
execution_evidence:
  kind: focused_test | fixture | traced_run | none
  observed_at:
  reference:
```

For this phase, only Mist Trail was freshly executed: its 13 focused tests
passed. The LLM-heavy workflows were inspected, not rerun.

## 10. Do not compute one coverage percentage

A raw share of rows in Tier 1 or Tier 2 would reward over-decomposed methods and
treat a validation helper as equal to a substantive engine. Later reporting
should show at least:

1. raw step coverage;
2. required-step coverage;
3. equal-weighted method coverage;
4. implementation status coverage;
5. rough implementation effort and coverage per effort.

No weighting scheme should be frozen before the pilot exposes its sensitivity.

## Controlled-vocabulary observations

The original verbs were sufficient after normalization. `identify` was not
added: theory identification is an `extract` operation and compiled-module
identification is `retrieve`.

Two type additions are justified now:

- `artifact_ref` — a versioned/path-addressable artifact handle, not the
  artifact content;
- `artifact_digest` — a content identity used for custody and drift checks, not
  a general configuration value.
- `construct` — a developed analytical category or construct whose stable
  identity is consumed by later appraisal and theory-building operations.

Method-specific compound artifacts should first use existing coarse types plus
meaningful slot names. Only add a new type when downstream admissibility would
otherwise be lost.

## Pilot gate

Before the five-method pilot:

1. adopt the topology file and named slot format;
2. freeze one precise variant for every method;
3. replace `provenance` with evidence/implementation/actor fields;
4. add execution evidence and executable granularity;
5. keep coverage multidimensional;
6. use authoritative method sources for idealized rows and code references for
   implemented rows.

These are candidate schema revisions. Claude's independent Phase 0 may expose
additional failures; reconcile only after both outputs are frozen.
