# System Goal and Capability Architecture

Status: adopted initiative direction; exact contracts and implementation remain
gated by the capability-adoption sequence below

Updated: 2026-08-13

## Purpose and authority

This is the context-independent description of the system the Mixed Methods
Workbench is intended to become. It is written for a contributor or external
agent who has not read the repository history.

This document is the Workbench initiative and application profile. Project
Meta remains authoritative for the ecosystem-wide artifact model, generalized
typed capability composition, and OntoCanon/DIGIMON boundary. Data Contracts
remains authoritative for the shared composition grammar. If this profile and
those authorities disagree, the shared authority controls its concern and this
profile must be reconciled; the Workbench must not establish a parallel
ecosystem architecture.

Brian approved the following direction on 2026-08-13:

1. reason from the full research-system goal before selecting another example;
2. inventory and disposition existing capabilities before building shared
   infrastructure;
3. distinguish a small generic execution substrate from reusable research
   primitives, method-owned protocols, and study workflows;
4. use an authentic policy investigation to prove the resulting composition,
   not to invent the architecture case by case; and
5. defer automated methodology recommendation until the lower layers work.

This direction changes initiative ordering. It does not accept the pending NYC
review statements, adopt a universal research schema, resume Phase 3 method
catalog expansion, or authorize product implementation by itself.

## North star

Build a general, agent-operable environment for rigorous policy and
mixed-methods research in which a researcher can move from a substantive
question and governed evidence universe to methodologically bounded findings,
cross-method integration, policy appraisal, and a reproducible investigation
bundle.

The system should make it possible to:

- reuse the same well-defined operation across different research workflows;
- preserve exact sources, transformations, review decisions, and limitations;
- invoke specialized research methods without moving their inference rules into
  a generic orchestrator;
- combine qualitative, quantitative, causal, theoretical, retrieval, and
  simulation outputs without flattening their meanings;
- keep human judgment, authority, values, and decision rights explicit; and
- show exactly which evidence and reasoning license each conclusion.

The eventual product begins with a research question and decision context. A
future methodology-guidance layer may recommend a study design, but method
selection is not on the MVP critical path. The present critical path begins
after a design or bounded workflow has been selected.

## First-principles model

Research work is a sequence or graph of governed state transitions over typed,
versioned artifacts. A transition is valid only when all of the following are
compatible:

- the input and output data contracts;
- the actual executable implementation;
- the operation's cost, determinism, effects, and failure behavior;
- the research method's preconditions, sequencing rules, and validity guards;
- the evidence and provenance obligations;
- the reviewer and decision authority; and
- the conclusions the result is allowed to support.

Schema compatibility is therefore necessary but not sufficient. Two operations
can exchange valid JSON and still form an invalid research workflow.

### Terms

| Term | Meaning |
| --- | --- |
| **Execution form** | A domain-neutral computational shape such as semantic transform, deterministic transform, validate, review, or apply transition. |
| **Research primitive** | A reusable research-facing capability such as fetch a source, extract structured candidates, bind a field to exact evidence, or compare records. It may use one or more execution forms. |
| **Analytical move** | A method-framed action such as initial coding, negative-case analysis, partition auditing, or diagnostic evidence assessment. |
| **Method protocol** | The method-owned state, ordering, guards, roles, iteration rules, and claim limits that make a set of analytical moves methodologically meaningful. |
| **Study workflow** | A research-design-specific composition of primitives and method protocols across one or more strands. |
| **Projection** | A graph, table, vector, or rendered view derived from an authoritative artifact. A projection is not automatically a new source of truth. |

This vocabulary prevents a common category error: a prompt is not a method, a
Pydantic model is not a capability, and a chain of type-compatible functions is
not necessarily a valid workflow.

## Layered capability architecture

```text
Future methodology guidance
  recommends a study design and explains alternatives
                         |
Study and integration workflows
  exploratory/explanatory/convergent/embedded/evidence-to-policy designs
                         |
Method modules and protocols
  qualitative coding, grounded theory, process tracing, theory application,
  statistical analysis, simulation, source criticism, policy appraisal
                         |
Reusable research primitives
  acquire, freeze, parse, segment, extract, anchor, compare, calculate,
  retrieve, review, visualize, synthesize, export
                         |
Generic execution forms
  semantic transform, deterministic transform, validate, bind, review,
  transition, retrieve, iterate/control
                         |
Typed composition, custody, execution, and observability substrate
  Data Contracts, artifact references, llm_client, tool runtimes, traces
```

The layers are not separate services by default. They are ownership and
reasoning boundaries. One repository may implement more than one layer, but a
lower layer must not silently acquire the semantics or authority of a higher
one.

### Layer 0 — custody, identity, execution, and composition

This layer answers:

- What exact artifact or source version was used?
- What implementation, schema, prompt, configuration, model, and policy ran?
- What was produced, refused, or left unresolved?
- What state transition is proposed?
- Can the consumer accept this output and are the operation's guards satisfied?

Data Contracts already supplies much of the typed composition grammar. It does
not load or dispatch implementations. `llm_client` already supplies structured
model execution and durable outer-run observability. The Workbench should use
these owners rather than create another dispatcher or model client.

The logical artifact and derivation ledger does not require one physical
database. Source bytes, method artifacts, graph projections, tables, vectors,
and review records may remain in their appropriate stores as long as their
identities and derivations round-trip exactly.

Application/investigation state, composition state, artifact-lifecycle state,
method state, governed-assertion state, retrieval-request state, and
review/authority state remain distinct. They may refer to each other through
typed identities; none is the universal state store.

### Layer 1 — generic execution forms

The smallest recurring forms observed across current method engines are:

| Form | Abstract behavior | Required result |
| --- | --- | --- |
| `semantic_transform[I, O]` | Typed inputs and source context plus a versioned instruction/prompt and output contract produce a candidate typed output. | Candidate artifact plus exact execution receipt; never implicit acceptance. |
| `deterministic_transform[I, O]` | Versioned code applies a deterministic calculation or mapping. | Output, implementation/configuration identity, input/output hashes, and failure. |
| `validate[T]` | Structural or method-owned rules inspect a candidate. | Typed findings and `pass`, `fail`, or `unresolved`; validation does not rewrite the candidate. |
| `bind/anchor` | A candidate field or record is connected to exact source units. | Resolvable evidence references or a loud refusal. |
| `review/adjudicate[T, D]` | An authorized reviewer considers a frozen candidate and context. | Attributable disposition, rationale, target digest, authority, and any explicit replacement. |
| `apply_transition[S, D, S2]` | An accepted delta is applied to a particular prior state. | New immutable state identity and lineage, or refusal on stale/incompatible input. |
| `retrieve/select` | A query and declared universe select source units or artifacts. | Results plus universe, ranking, coverage, and retrieval receipt. |
| `iterate/control` | A typed state machine chooses and sequences the other forms. | Checkpoints, guards, bounded attempts, stop/block outcome, and state lineage. |

These are execution forms, not a new universal method ontology. Their exact
portable contracts remain to be designed from adopted consumers.

Exact binding is primarily a validation or attestation fact over frozen
candidate and source versions. It becomes a separate action when it also
materializes an attachment artifact; that does not transfer evidence-admission
authority to the generic layer.

### Layer 2 — reusable research primitives

The first capability inventory should test, rather than assume, reuse for:

- discover and acquire sources;
- freeze exact source bytes and custody metadata;
- parse, segment, and identify exact source units;
- extract structured candidates from text against a versioned output contract;
- bind records or fields to exact evidence;
- classify, code, annotate, compare, aggregate, and summarize;
- calculate deterministic measures;
- run statistical, predictive, or simulation models through method-owned
  adapters;
- invoke a method-owned analysis;
- review, edit, reject, withhold, or promote candidates;
- construct graph, table, vector, text, and joint-display projections;
- synthesize bounded conclusions and appraise policy options; and
- export a reproducible investigation bundle.

Each capability must name its owner, callable seam, typed inputs and outputs,
execution mode, guards, effects, provenance, failure behavior, authentic
consumers, portability, limitations, and adoption disposition. "Code exists"
is weaker than "stable boundary exists," which is weaker than "an intended
consumer actually used it."

### Layers 3 and 4 — method protocols and study workflows

Method repositories own the analytical meaning that cannot be inferred from a
generic operation descriptor. Examples include:

- qualitative code identity, constant comparison, negative-case handling,
  memoing, reflexivity, category adequacy, sampling, and saturation limits;
- Process Tracing rivals, predictions, evidence exposure, partition adequacy,
  diagnosticity, likelihood semantics, dependence, absence reasoning,
  mechanism integrity, and publication gates;
- statistical estimands, measurement assumptions, identification, uncertainty,
  leakage, calibration, and robustness;
- theory constructs, mechanisms, scope conditions, predictions, and validation
  obligations;
- simulation state, mechanisms, fidelity, scenarios, and trajectories; and
- policy criteria, value judgments, weights, trade-offs, and recommendation
  authority.

Study workflows select and connect these protocols according to a research
design. A workflow is therefore compiled from lower-level capabilities under
method- and design-owned rules; it is not an arbitrary user-authored pipe.

### Layer 5 — future methodology guidance

Later, a planner may:

- elicit the research question, decision context, constraints, evidence, and
  desired inference;
- propose appropriate study designs and explain rejected alternatives;
- expose assumptions, feasibility, and authority decisions; and
- compile an accepted design into method protocols and research primitives.

That planner must not decide methodology merely because two component schemas
connect. The analyst or named methodology authority accepts the design.

## The structured-candidate primitive

Brian's example identifies the most important first reusable semantic
capability:

```text
ExtractStructuredCandidates(
  source_units,
  output_contract_ref,
  instruction_or_method_policy_ref,
  execution_policy,
  trace_and_budget
)
  -> CandidateSet(
       typed_payloads,
       exact_evidence_anchors,
       execution_receipt,
       provenance,
       review_state
     )
```

This is deliberately broader than "qualitative coding" and narrower than
"perform a research method."

The implementation may accept an in-process Pydantic type, but a durable
cross-process invocation should carry a versioned contract reference rather
than serialize a Python class. The instruction, schema, implementation, model,
configuration, inputs, and candidate outputs must all have stable identities.

`llm_client` owns the model call. A method repository owns its schema,
instructions, validators, interpretation, and authoritative method review. The
Workbench owns invocation, application-level review orchestration and
references, integration acceptance, value/publication decisions, and the
investigation journey. OntoCanon separately owns assertion-candidate review and
promotion. Data Contracts owns the neutral action and transition grammar. No
component may treat a generated candidate as accepted evidence merely because
it validated structurally.

### Why qualitative coding is more than prompt plus schema

A single coding proposal can compile onto the generic primitive:

```text
frozen segment
  -> semantic_transform[segment, CodeCandidate]
  -> exact-anchor validation
  -> method-owned comparison and admissibility checks
  -> reviewer disposition
  -> codebook/project-state transition
```

Category development is a protocol over many such operations:

```text
code candidates + evolving codebook + prior comparisons
  -> constant comparison
  -> merge/split/retain proposals
  -> negative-case search
  -> memo/reflexive record
  -> category adequacy and sampling questions
  -> review and state transition
  -> continue, block, or stop under method-owned rules
```

The generic machinery is valuable precisely because it is reusable. The
method-owned loop is indispensable because it determines what the operations
mean, what evidence they must see, when they may run, and what claims they may
support.

## System ownership

| Owner | Owns in this system | Must not silently own |
| --- | --- | --- |
| Mixed Methods Workbench | Investigation continuity, accepted study plan, adapter resolution, orchestration, application-review references and queues, integration acceptance, value/publication decisions, cross-method linkage, joint displays, synthesis, UI/API, and reproducible export. | Authoritative method review, assertion promotion, method-specific inference, generic model runtime, retrieval ranking, or a universal ontology. |
| Data Contracts | Typed action declarations, bindings, resources/effects, applicability, invocation guards, execution-result and proposed-transition grammar. | Implementation loading/dispatch, workflow selection, persistence, or research-method meaning. |
| `llm_client` | Structured model execution, route/model/config identity, budgets, retries/fallback disclosure, traces, cost, and outer-run observation. | Evidence acceptance, source anchoring, or methodological validity. |
| Open Web Retrieval | Search/fetch/extract transport, source metadata, exact retrieval receipts, and strict/partial retrieval behavior. | Source admission, source criticism, or analytical inference. |
| Qualitative Coding | Corpus/project state, coding, comparison, qualitative claims, grounded-theory development, memos, reflexivity, review, and strict native exports. | Process Tracing, quantitative inference, or cross-method synthesis. |
| Process Tracing | Rival explanations, predictions, source design, evidence exposure, diagnostic assessment, dependence/absence logic, within-case support, and publication gates. | Generic qualitative coding, population effects, or policy choice. |
| Theory Forge | Theory extraction, operationalization, compilation, application stages, and theory-native limits. | Empirical support, method selection, or policy authority. |
| Grounded Research | Independent analysis, disputed-claim verification, and adjudication workflows. | Universal truth, Workbench state, or replacement of source- and method-owned review. |
| Computational Social Science | Study questions/manifests, application-local adapters, exact input cohorts, derived tables/findings/relational analyses, and scientific-review records. | Producer method/theory semantics, generic graph or assertion ownership, or cross-study Workbench orchestration. |
| OntoCanon | Vocabulary packs, candidate assertions, semantic identity, evidence review, promotion, governed assertion exports, and deterministic semantic projections. | Method-native findings, Workbench investigation state, or graph retrieval. |
| DIGIMON | Graph materialization, named projection surfaces, traversal, ranking, retrieval, analytics, and typed operator composition in its domain. | Canonical assertion storage, promotion authority, or method-native inference. |
| Quantitative and simulation engines | Estimands or model state, calculations, uncertainty, validation, and native artifacts. | Workbench integration or human value judgments. |
| Human/authorized roles | Method/design acceptance, evidence admission where required, value judgments, recommendation approval, and final decisions. | Execution receipts or software evidence that did not occur. |

Six authority roles remain distinguishable even if one person fills several:
performer, judgment owner, acceptance authority, recommender, value/goal
authority, and decision authority.

## OntoCanon and DIGIMON

OntoCanon and DIGIMON are important, but neither should become an obligatory
detour for every research artifact.

### OntoCanon's role

OntoCanon is governed-assertion middleware, not a generic synonym for
structured output. Its useful reusable path is:

```text
source text or external producer
  -> ontology-pack-constrained candidate assertion
  -> validation and evidence review
  -> promotion with stable assertion identity
  -> versioned Foundation assertion export
  -> optional deterministic semantic projection
```

Use it when the investigation needs cross-document semantic identity,
governed assertions, ontology-pack constraints, or reusable graph projection.
Do not force method-native findings, raw observations, statistical objects, or
simulations through its semantic kernel merely to participate in the
Workbench.

A method-native artifact may be mapped into an explicitly labeled OntoCanon
semantic assertion candidate. Method acceptance and assertion review are
separate decisions: the method artifact remains authoritative for the finding,
while OntoCanon may promote the mapped semantic interpretation after its own
review. The assertion candidate and any promoted assertion must preserve the
method artifact, method-review decision, mapping execution, and exact
supporting-evidence references. An unreviewed method candidate cannot be
presented as a reviewed method finding merely because OntoCanon stores its
mapped assertion candidate.

### DIGIMON's role

DIGIMON owns graph and retrieval capabilities. It already demonstrates real
typed action composition over Data Contracts. Its graph boundary distinguishes:

- semantic relations for meaning-bearing traversal;
- assertion/evidence links for returning to exact support; and
- weak associations such as co-occurrence, which cannot silently act as
  semantic evidence.

Project Meta Plan 241 now proves the public OntoCanon `compile_corpus` ->
DIGIMON `ask_governed_model` path across nanoGPT and DoDAF, including typed
insufficiency, cited answers, and exact assertion/source-passage reopening. The
general governed-corpus product round trip is therefore adopted and observed.

A narrower direct `SemanticGraphProjectionV1` operator path may retain its own
certification gate. For method-native use, the remaining architectural seam is
different: a projected answer must return not only to exact source evidence but
also to the authoritative method artifact and method-review decision from which
the mapped assertion was derived.

DIGIMON is optional for the first MVP unless graph or multi-hop retrieval is
needed to answer the selected investigation question. It should never decide a
method's inference or become the canonical review state.

### Combined optional flow

```text
reviewed method-native artifact + method-review decision
  -> Workbench adapter and exact native artifact/version reference
  -> optional mapped OntoCanon semantic assertion candidate
  -> separate OntoCanon assertion review/promotion decision
  -> OntoCanon evidence and semantic projections
  -> optional DIGIMON materialization/retrieval
  -> exact supporting assertion and source occurrence
  -> revalidated source window/view, immutable artifact bytes, and custody
  -> exact method-native artifact and method-review decision
```

No graph answer is supportable if it cannot make the return trip.

## Evidence and artifact authority

The system must distinguish at least:

- source resource;
- acquisition event, distinct from the captured transport response;
- transport capture, distinct from the intellectual source boundary;
- logical source-artifact identity, distinct from each immutable artifact
  version;
- derived source-view version, distinct from the bounded source window or unit
  selected from that view;
- custody binding;
- observed or reported content;
- elicited human input;
- generated candidate;
- assertion submission or extraction-run version, distinct from a deduplicated
  assertion-candidate identity;
- source-bound claim occurrence, distinct from semantic-content identity;
- interpreted or governed assertion;
- deterministic derived measurement;
- estimated result;
- simulated result;
- analytical finding;
- human value judgment and decision;
- projection artifact and its local row, node, edge, or chunk identities,
  distinct from the governed source identities they project; and
- derivation and execution records.

Provenance proves where something came from and what transformed it. It does
not prove that the source is truthful, that a sample is representative, or that
an interpretation is correct.

Every derived artifact must identify exact input versions and the execution
that produced it. Following the derivation chain must reach immutable source
versions, explicit human inputs, or another declared root observation.

## Adoption rule for existing capabilities

Before adding an implementation, record one of these dispositions against its
current owner and authentic evidence:

- `reuse` — use the existing seam unchanged;
- `wrap` — keep the owner and add a Workbench adapter;
- `extend` — add a capability at its existing owner;
- `supersede` — replace an accepted owner through an explicit migration;
- `keep_method_owned` — compose the native artifact without generalizing its
  semantics;
- `defer` — valuable, but not needed for the current outcome;
- `explicit_exception` — a bounded local implementation is necessary and its
  non-reuse is visible; or
- `missing` — no adequate implementation or owner exists.

Two authentic compatible consumers are required before a Workbench-local
research extension is promoted to shared Data Contracts infrastructure. The
second consumer must arise from a real need; it must not be manufactured to
justify promotion.

## Roadmap to an authentic MVP

### Phase A — capability and adoption baseline

Inventory current implementations at exact revisions. Distinguish internal
code, stable public seams, and authentic consumer adoption. Resolve repository
authority drift. Preserve conflicts instead of declaring a canonical
capability model prematurely.

Exit evidence:

- every MVP-relevant capability has an owner and disposition;
- important false-positive seams are recorded;
- OntoCanon, DIGIMON, computational-social-science, and SB Ontologies are
  explicitly included or deferred; and
- the flat method-operation inventories are mapped to the layered model without
  erasing their 70-versus-90 operation disagreement.

### Phase B — minimal shared execution seam

First freeze a Project Meta-owned method-operation composition and evidence
round-trip profile subordinate to its existing generalized composition and
governed-knowledge authorities. It must crosswalk source/custody, composition,
method, assertion, application, retrieval, and decision-rights states without
inventing another universal schema.

Then design the smallest Workbench `ExtractStructuredCandidates` consumer
action and its artifact, anchor, receipt, review, and transition bindings by
reusing Data Contracts and `llm_client`. No universal method schema or dynamic
plugin platform is added.

Exit evidence:

- a context-independent contract names implementation, input, output, prompt
  or policy, execution, evidence, review, and failure identities;
- method-owned payloads remain opaque to the generic composition layer; and
- case-specific literals are prohibited from the primitive.

### Phase C — refactor an existing authentic consumer

Move the already observed NYC structured extraction through the adopted action
instead of adding a new showcase. Preserve its frozen sources, authentic model
trace, rejected attempts, exact anchors, and pending human review state.

Exit evidence:

- the NYC path resolves and executes the generic action;
- a focused check fails if the case bypasses the selected action;
- the old direct case-specific invocation is removed or retained as an
  explicit bounded exception; and
- no substantive NYC statement is accepted as a side effect.

### Phase D — prove method composition without flattening

Adapt one qualitative and one Process Tracing move that share an execution
form but retain incompatible method guards. Strong seam probes are QC
negative-case review and PT partition audit: both can use semantic transform
plus deterministic validation, but their admissibility and claim rules remain
method-owned.

Exit evidence:

- both use the common invocation and receipt shape;
- neither can consume the other's method state or validator accidentally;
- exact candidate universes and evidence exposure are retained; and
- accepted deltas produce lineage-preserving method-state transitions.

### Phase E — compose the cohesive policy MVP

Complete one understandable policy investigation through governed sources,
reviewed extraction, method-owned qualitative analysis, deterministic
quantitative description or analysis, integration, value-explicit appraisal,
limitations, and reproducible export. Add Process Tracing, Theory Forge,
OntoCanon, DIGIMON, simulation, or another engine only when the study question
requires it.

The NYC Congestion Relief Zone remains the stable example unless the capability
work exposes a fatal fit problem. Existing NYC evidence is retained; work does
not restart from source acquisition.

Exit evidence:

- one browser/API/export journey follows the investigation end to end;
- every material statement steps down through method-native artifacts and
  exact evidence;
- qualitative and quantitative strands have an explicit integration design;
- contradictions, uncertainty, and missing evidence remain visible;
- recommendations identify criteria, value inputs, and decision authority; and
- the system refuses causal, representative, or policy-effect claims the
  design cannot support.

### Phase F — later guidance and portfolio growth

After the MVP, add methodology guidance, additional study designs, method
profiles, optional graph navigation, broader quantitative methods,
interoperability, and comparative evaluation. Expansion is driven by real
workflows and evidence, not catalog completeness.

## Architecture acceptance tests

The architecture is working only when all of these are true:

1. an existing authentic example consumes a reusable action rather than a
   case-local duplicate;
2. mutating a source byte, contract, prompt/policy, implementation, candidate,
   anchor, review target, or prior-state hash causes a visible refusal or new
   artifact identity;
3. a type-compatible but method-invalid composition is rejected;
4. a generated candidate cannot promote itself;
5. deterministic, LLM, human, hybrid, and represented-only operations are
   distinguishable;
6. method-owned artifacts retain their native meaning and claim limits;
7. optional OntoCanon/DIGIMON projections round-trip to evidence and native
   authority before supporting an answer; and
8. an external agent can identify the owner, current evidence, and next valid
   action without reading the entire repository history.

## Current evidence and known gaps

The evidence baseline is maintained in
[`CAPABILITY_ADOPTION_MAP.md`](CAPABILITY_ADOPTION_MAP.md). The most important
current findings are:

- Data Contracts has a real composition grammar and DIGIMON is an authentic
  consumer;
- the current NYC extraction is authentic but case-specific and does not use
  Data Contracts;
- QC and Process Tracing contain recurring generic execution forms but no
  neutral cross-repository method-operation ABI;
- OntoCanon has a strong governed-assertion and semantic-projection producer,
  and Project Meta Plan 241 proves the public two-domain OntoCanon/DIGIMON
  compile/query/evidence round trip; a narrower direct-projection certification
  and method-artifact reverse binding remain separate gates;
- Grounded Research and OntoCanon have adjacent adapters but no proven current
  producer-to-consumer export path;
- Computational Social Science is an active governed study/application
  repository at remote
  `main@33526009e13b8b93b6adcd52fef7408cf99ab7dc`; F1 has a real reviewed
  source-to-table/finding path and a separate Data Contracts/DIGIMON vertical,
  while recurrence, manual baseline, value, and complementary-method gates
  remain open; and
- SB Ontologies is useful donor history, not a current platform owner.

These gaps determine the next planning and implementation sequence. They are
not reasons to create a new universal platform.
