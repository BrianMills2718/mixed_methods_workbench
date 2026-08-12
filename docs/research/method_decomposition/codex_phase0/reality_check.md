# Phase 0 reality check

## Bottom line

The four implementations already disprove a simple universal pipeline.

- QC contains a real feedback loop: each new five-document batch revises the
  whole proposal before the next batch is examined.
- Process Tracing contains several bounded audit/repair loops, conditional
  branches based on evidence exposure, and a terminal publication refusal.
- Theory Forge is mostly sequential/DAG-shaped and explicitly rejects circular
  computation dependencies.
- Mist Trail is a completed, typed, source-bound appraisal, but the analytical
  judgments were manually authored. Its code validates and presents the
  appraisal; it does not calculate the recommendation.

This supports configurable topology and typed handoffs. It does not support a
single mandatory workflow shape or a claim that similarly named operations
share analytical meaning.

## Implementation truth by workflow

### QC fixed-corpus grounded theory

The real path is 15 code-observed operations. The important analytical unit is
coarser than the intellectual description: incident identification, constant
comparison, category construction, memoing, core-process selection, and
proposition formulation are returned by one structured model call during seed
development. They are not separately callable capabilities.

The implemented expansion loop is:

```text
current proposal + next five interviews
  -> structured comparison and complete revised proposal
  -> deterministic validation and checkpoint
  -> next five interviews
```

After four fixed batches, the system runs a full-corpus appraisal and emits
sampling questions. It does not acquire new samples, branch on saturation, or
pause for human approval.

The installed v3 artifact covers 25 documents, five iterations, eight
categories, six propositions, six appraisals, five sampling questions, and five
narrative findings. Its observed SHA-256 was
`538a26465bb91cfe79bb62a2f16b6e0ea8b0017412f8fe1874fef4045ea66e3b`.

### Process Tracing

The real core path contains 23 operations because its review and repair gates
are executable parts of the method rather than presentation detail. It
branches among theory-first, discovery/evaluation split, and exploratory
evidence-exposure designs; audits the rival partition; may repair and re-audit
it; tests evidence against rivals; independently audits discriminating claims;
evaluates meaningful absences; computes within-case comparative support;
constructs and audits a temporal mechanism graph; synthesizes; optionally
criticizes or refines; and reviews every terminal prose claim before
publication.

The acquisition companion workflow separately implements planning, retrieval,
human source-fit admission, and intended held-out testing. Its successful
evaluation path is currently incomplete: `AcquisitionSession.evaluate()`
unpacks eight values from `_run_passes_3_plus()`, while that function returns
nine. Existing tests cover gates and wiring but not a successful end-to-end
evaluation. This row must not count as executable coverage.

Process Tracing uses Bayesian calculations, but its problem is still a
qualitative within-case causal-inference problem: the quantitative update
summarizes source-bounded comparative support and is explicitly not a
population effect estimate or a probability that a historical hypothesis is
true.

### Theory Forge

The current end-to-end workflow remains centered on
`meta_schema_v14.json`. v15 adds optional typed inputs, output types,
invariants, and golden cases. Typed stubs and golden-test generation consume
some of those fields, and the runtime can check invariants. However, normal
compiler stage discovery does not copy schema invariants into the generated
stage manifest. v15 is therefore an implemented reliability surface, not the
default fully wired schema version.

The generic path extracts a theory, validates it, compiles it into extraction,
computation, and qualitative stages, verifies and repairs compilation, applies
the result to new text, optionally reviews it, and persists a report. Stage
failures are generally recorded while later stages continue. The generic
runtime does not implement a theory-to-new-case research-design artifact or a
feedback cycle that revises earlier analytical stages.

Two authentic but separate verticals matter:

- Entman operationalization creates a strict, source-bound, non-empirical
  artifact. It is not the generic compiler.
- CPT/Choices13k performs a real, pinned prediction comparison. It is a direct
  deterministic vertical, not a reusable stage in the generic runner.

They should inform later collisions, but must not be used to overstate the
generic pipeline.

### Mist Trail policy appraisal

MT-D1 is done as an implementation slice: its typed packet, browser view, JSON
route, validation rules, and 13 focused tests are present on main. Stakeholder
comprehension review remains pending, but that does not make implementation
unfinished.

The packet records official options, source anchors, empirical consequence
summaries, affected interests, explicit criterion judgments, priority lenses,
tradeoffs, a conditional recommendation, evidence gaps, non-claims, and a
review event. The conclusion changes from C to B under a different declared
priority lens and stays unresolved under an operations-first lens.

The application does not execute source interpretation, consequence
assessment, priority selection, or recommendation logic. Those are completed
human-authored analytical operations represented in a validated fixture. The
executable capabilities are strict loading, custody checks, referential/domain
validation, refusal on corruption, and one shared API/browser projection.

## Provenance and implementation counts

Every row in this Phase 0 inventory is grounded in current code, tests, or a
typed fixture; there are no literature-inferred rows. That does **not** mean
every operation is automated.

| Workflow | Rows | Executable | Represented manual | Incomplete |
| --- | ---: | ---: | ---: | ---: |
| QC grounded theory | 15 | 15 | 0 | 0 |
| Process Tracing core | 23 | 23 | 0 | 0 |
| PT acquisition companion | 4 | 3 | 0 | 1 |
| Theory Forge generic | 19 | 18 | 0 | 1 |
| Theory Forge CPT prediction | 6 | 6 | 0 | 0 |
| Mist Trail | 10 | 2 | 8 | 0 |
| **Total** | **77** | **67** | **8** | **2** |

`Executable` means the code path exists, not that this review reran an
authenticated LLM workflow. Mist Trail's focused non-LLM suite passed locally:
13 tests.

## What the code does not justify

- A universal `compare`, `test`, `review`, or `synthesize` implementation.
- Treating prompt-internal intellectual stages as independently runnable
  capabilities.
- Treating a typed representation of human work as automation of that work.
- Treating PT's within-case comparative support as SEM, RCT, or population
  causal-effect estimation.
- Treating Theory Forge v15 as the default complete end-to-end schema.
- Treating a source anchor as proof of source quality or analytical validity.
- Promoting Data Contracts fields merely because similar names appear here.

## Candidate mechanics to test later

The following recurred in the code and deserve collision testing, not immediate
promotion:

- typed input validation and fail-loud preconditions;
- content/digest-bound artifacts;
- exact source anchoring and custody validation;
- structured model calls separated from deterministic validation;
- audit -> bounded repair -> re-audit control flow;
- checkpoint/resume and revision lineage;
- human review over typed artifacts;
- unresolved/refused terminal states;
- publication or presentation gates;
- explicit evidence gaps and next-evidence agendas;
- projections that preserve a method-native source of truth.

Their signatures and delegated semantics still need to collide across the
five-method pilot before any shared implementation decision.
