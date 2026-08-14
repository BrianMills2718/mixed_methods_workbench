# Plan #6 Candidate — Composable Research Capability Kernel

**Status:** unresolved design candidate; not adopted and not implementation authority

**Review revision:** `PACKET-MMW-CAPABILITY-KERNEL@1`

**Prepared:** 2026-08-13

**Route:** coordinated, Standard-depth design; pilot target profile with runtime,
LLM, and repository-governance overlays

**Landscape disposition:** linked to existing ecosystem owners and current
producer seams; no new platform or universal research ontology is proposed

## Current understanding

The target actor is a policy researcher who repeatedly needs to turn a governed
source universe into reviewable evidence, method-owned analyses, quantitative
results, and a bounded synthesis. The inspectable MVP result remains one
cohesive NYC Congestion Relief Zone investigation whose claims step down to
exact sources, transformations, reviews, method owners, and limitations.

The architecture question precedes further content approval: are the visible
NYC steps instances of reusable operations, or case-specific code that only
looks like a workflow? At current `mixed_methods_workbench` revision
`e06b1cbe49cee1b1e6ef995b68308342646381a4`, the answer is mostly the latter.
The NYC extraction runner hard-codes source units, locators, model, prompt, and
output schema, while the Workbench has no `data_contracts` dependency and no
runtime capability resolver. The existing P5 Investigation Spine is a useful
second seam, but its consumer models are also locally duplicated and
case-specific.

The desired delta is therefore:

```text
case-specific scripts and local duplicate envelopes
  -> shared typed composition grammar
  -> explicit Workbench runtime adapters
  -> method-owned engines and outputs
  -> workflows assembled from versioned operations
  -> one authentic, reviewable policy investigation
```

Reversible technical details within this boundary should follow the
recommendation below unless the contributor objects. Material architecture and
adoption choices remain attributable to the contributor.

## Recommendation and important alternative

### Recommendation

Adopt a deliberately small, three-layer capability architecture:

1. **Data Contracts owns composition semantics:** immutable action packs,
   payload declarations, artifact bindings, exact references, applicability,
   guarded invocations, execution results, and proposed state transitions.
2. **Workbench owns product runtime:** investigation state, explicit
   implementation resolution, adapter invocation, persistence, review and
   publication policy, projections, and cross-method integration.
3. **Domain repositories own research semantics:** QC, Process Tracing, Theory
   Forge, retrieval, and quantitative/simulation engines own their native
   inputs, judgments, validation, outputs, and claim limits. `llm_client` owns
   model execution and durable LLM observability.

Prototype only two provider-neutral contract families as Workbench-owned
extensions over Data Contracts' existing extension points:

- content-addressed source artifact, source-unit, and exact evidence-span
  references;
- candidate/field review dispositions and promotion receipts bound to exact
  candidate bytes.

Move either family into Data Contracts only after two authentic compatible
producer/consumer seams exercise that exact family. A family without that proof
remains an explicit Workbench-local exception; the MVP does not manufacture a
second consumer merely to earn shared status.

Keep the adapter registry explicit and Workbench-local. Do not use the legacy
Data Contracts `ContractRegistry` as a callable registry and do not introduce a
new orchestration repository for the MVP.

### Important alternative and tradeoff

The important alternative is to build a generic research-capabilities service
or universal evidence ontology before revisiting NYC. That could centralize
more behavior sooner, but it would require guessing stable semantics across
methods, duplicate current owners, and delay an authentic consumer-path test.
The recommended design instead shares only custody and composition mechanics;
it promotes a broader abstraction only after two authentic compatible seams.

**Contributor disposition required:** `accept | revise | reject | delegate`
for the recommendation, and for the exact review revision
`PACKET-MMW-CAPABILITY-KERNEL@1`.

## Outcome, success, and non-goals

### Outcome

A researcher can run or inspect this stable journey:

```text
frozen source artifact
  -> exact source units
  -> schema-driven structured extraction candidate
  -> deterministic evidence binding
  -> attributable review/promotion
  -> method-owned QC analysis
  -> deterministic quantitative transformation
  -> joint display and policy appraisal
```

Each arrow is a versioned action with typed inputs and outputs, an exact
implementation/configuration identity, a durable result or refusal, and a
lineage-preserving transition in one Workbench investigation.

### Material success criteria

| Criterion | Provenance | Acceptance evidence | Passing does not prove |
| --- | --- | --- | --- |
| NYC uses reusable operations rather than a case-owned execution path. | explicit contributor correction in this thread | the live NYC journey resolves and invokes registered action descriptors; a structural check rejects direct bypass of the selected path | that the operations generalize to every research method |
| `extract structured data from text` is a first-class reusable capability. | explicit contributor example | an arbitrary registered Pydantic output contract, prompt/config reference, and one or more content-addressed source units produce a candidate plus an exact `llm_client` trace; no NYC literals occur in the adapter | that generated content is accepted evidence or qualitative analysis |
| Shared composition does not absorb method semantics. | Workbench authority and current QC/PT boundaries | QC and PT public artifacts retain native schema, method owner, native limitations, and review payload; the Workbench stores opaque typed bindings and projections | that QC and PT methods are empirically valid |
| Every finding can step down to exact evidence and derivation. | active MVP goal and governing repository instructions | mutate a source byte, anchor, artifact digest, request, or output binding and require a loud refusal before promotion | that the source itself is truthful or representative |
| Review and decision rights are explicit and versioned. | Phase 1 structural finding and current NYC review gate | accept/edit/reject/withhold decisions bind reviewer, role, time, rationale, target digest, field/object refs, and any replacement; acceptance without authority fails | that a human made a substantively correct judgment |
| Shared abstractions have two real consumers before promotion. | current Workbench planning authority | each proposed family names two authentic compatible seams that exercised that exact family; NYC plus P5 may prove common custody, but P5 does not by itself prove structured extraction, exact binding, or candidate review | universal capability coverage or reuse of a different action |
| The final MVP remains one understandable policy investigation. | persistent user goal | exact browser/API/export journey shows source, extraction, review, QC, quantitative comparison, integration, limits, and next evidence needs | causal effect, prevalence, representativeness, or an objectively correct recommendation |

### Non-goals

- no universal research ontology, generic claim score, or canonical method enum;
- no migration of QC, PT, Theory Forge, retrieval, or simulation logic into the
  Workbench;
- no Data Contracts dispatch, scheduling, persistence, or workflow ownership;
- no dynamic plugin discovery for the first MVP;
- no Process Tracing, Theory Forge, ontology projection, or live web retrieval
  requirement for the NYC MVP unless the investigation question later requires
  it;
- no acceptance of the pending NYC prediction, concern, or quantitative
  statement as a side effect of adopting this architecture;
- no public deployment, universal schema promotion, or SOTA claim.

## Ownership and system boundaries

```text
                         semantic declarations and custody
              +----------------------------------------------+
              |               Data Contracts                 |
              | packs, bindings, guards, results, transitions|
              +-----------------------+----------------------+
                                      |
                                      v
+-------------+   explicit adapter   +------------------------+
| Researcher  | -------------------> | Mixed Methods Workbench|
| / reviewer  | <------------------- | state, dispatch, review|
+-------------+  projections/decisions| integration, export   |
                                      +---+----+----+----------+
                                          |    |    |
                  +-----------------------+    |    +------------------+
                  v                            v                       v
          +---------------+           +---------------+       +--------------+
          | QC / PT / TF  |           | llm_client    |       | Quant/retriev.|
          | method meaning|           | model runtime |       | engine meaning|
          +---------------+           +---------------+       +--------------+
```

| Owner | Must own | Must not own in this design |
| --- | --- | --- |
| Data Contracts | strict producer/permissive consumer models; `ActionPack`/`ActionDescriptor`; exact artifact bindings and references; compile/applicability/invocation guards; `ExecutionResult`; `ProposedTransition`; compatibility fixtures | callable discovery, dispatch, state persistence, retries, project workflows, research-method judgments, review UI/policy |
| Workbench | `Investigation`; explicit adapter resolver; invocation coordination; state publication; artifact resolver; review/promotion policy; projections; joint displays; integration and claim boundaries | QC coding/interpretation, PT rival/diagnostic logic, model runtime, retrieval ranking, statistical estimands |
| `llm_client` | provider/model execution, structured decoding, trace/cost/cache metadata, durable outer-run observability | source anchoring, evidence acceptance, method judgment, Workbench state |
| Qualitative Coding | corpus/project state, coding, comparison, negative cases, memos, reflexivity, adequacy, qualitative claims, strict public exports | generic orchestration or PT inference |
| Process Tracing | source design, rival explanations, predictions, diagnostic evidence, dependence/absence reasoning, within-case support, publication gate, `pt_export_v2` | generic qualitative interpretation or Workbench synthesis |
| Theory Forge | published-theory extraction, operationalization, compilation, theory application and native exports | empirical support or Workbench decision authority |
| Open Web Retrieval | retrieval/fetch behavior, source metadata, retrieval receipts and ranking limits | evidence admission, source criticism, or analytical inference |
| Quantitative/simulation owners | estimand/model/state, transformations, uncertainty, validation and native limits | cross-method synthesis or human value judgments |
| Ontology/graph systems | optional governed projection and navigation after review | native method authority or MVP critical path |

## Domain rules

1. A source is immutable for one artifact version; a changed byte creates a new
   version rather than silently updating an existing reference.
2. A source unit is an exact, content-addressed window inside one source
   artifact. Its locator and selected/context hashes are part of identity.
3. Model output is always a candidate. Schema validity and exact anchoring do
   not constitute analytical or human acceptance.
4. Evidence binding is deterministic. Missing, duplicate, or mismatched text
   refuses promotion; it never silently repairs or substitutes text.
5. A review decision binds the exact candidate version. An edit produces a new
   artifact and lineage; it never mutates the candidate in place.
6. An action descriptor describes semantic I/O and execution constraints. An
   implementation resolver separately selects an exact callable. Neither one
   proves the other's identity.
7. A failed, refused, or indeterminate action cannot mutate semantic
   investigation state. Valid upstream artifacts remain inspectable and
   resumable.
8. Method-native payloads remain authoritative. A Workbench projection must
   retain a round trip to the exact native artifact and may not reinterpret a
   native score as generic confidence.
9. Information origin is a lineage chain, not one lossy label: source carrier,
   content kind, derivation action, method owner, and review decision remain
   separately addressable. Observed, elicited, derived, generated, and
   simulated material must not be collapsed into one evidence status.
10. Prespecification is digest-bound: request, input universe, method config,
    prompt/schema/model route, and decision policy are frozen before result
    publication. Feedback creates a versioned successor.
11. Human authority is role-specific. Candidate review, method acceptance,
    integration acceptance, value judgment, and publication are distinct
    decisions even if one person holds several roles.
12. Exact evidence anchors and reflexive/methodological records travel beside
    the method artifact. They are never reduced to a generic provenance string.

## Minimal capability kernel

The kernel distinguishes **substrate operations** from **method operations**.
Substrate operations are reusable mechanics. Method operations may be invoked
through the same grammar but keep their native semantics.

Capability claims use three separate maturity levels:

- **case-neutral local primitive:** the implementation has no case literals,
  accepts registered typed contracts/configuration, and has one authentic
  consumer-path execution;
- **reused Workbench capability:** two distinct authentic Workbench workflows
  execute the exact same implementation contract;
- **shared ecosystem capability:** two authentic compatible cross-repository
  producer/consumer seams use the exact promoted contract and one intended
  consumer receipt proves adoption.

Passing a lower level never licenses the higher label.

| Versioned action | Kind | Input | Output | Initial implementation owner | MVP posture |
| --- | --- | --- | --- | --- | --- |
| `research.source.segment/1` | substrate | content-addressed source artifact + locator specification | exact source-unit bindings | Workbench adapter using format-specific parsers | required |
| `research.text.extract_structured/1` | substrate | source-unit bindings + registered output contract + prompt/config/model identities | generated candidate artifact + LLM receipt | Workbench adapter over `llm_client` | required local primitive; reuse claim waits for K2x |
| `research.evidence.bind_exact/1` | substrate | candidate fields + declared source-unit references | exact evidence-span attachments or typed refusal | Workbench deterministic adapter | required |
| `research.candidate.review/1` | control | exact candidate + anchors + authority/review policy | disposition and optional promoted successor artifact | Workbench review policy/UI | required |
| `research.transform.deterministic/1` | substrate | typed input artifacts + transform/config/environment identities | derived artifact + replay receipt | Workbench-local or named quantitative adapter | required |
| `research.method.invoke/1` | method bridge | source/artifact bindings + method-specific request/config | native method artifact refs + invocation receipt | Workbench adapter; method engine executes | required for QC |
| `research.findings.integrate/1` | product analysis | reviewed method artifacts + quantitative artifacts + explicit value inputs | joint display, bounded meta-inference, open questions | Workbench | required last |
| `research.source.acquire/1` | substrate | source need/query + acquisition policy | fetched source artifacts + retrieval receipts | Open Web Retrieval adapter | required capability seam; NYC may reuse frozen bytes but must prove one authentic acquisition path |
| `research.theory.apply/1` | method bridge | reviewed question/findings + selected theory artifact | native Theory Forge application artifact | Theory Forge adapter | later unless the study requires it |
| `research.projection.publish/1` | optional control | reviewed artifact bindings | governed ontology/graph projection | Ontology/graph adapter | later and non-authoritative |

The action IDs are candidate names, not adopted shared vocabulary. The first
implementation may namespace them to the Workbench pack while their reuse is
being proven.

## Contract model

### Reuse unchanged from `data_contracts.composition`

- `ArtifactVersionRef` and `VersionIdentityRef` for exact artifact,
  implementation, configuration, model, and environment identity;
- `PayloadContract`, `ReferenceContract`, `SemanticContract`, and `ActionPack`;
- `ActionDescriptor`, typed input/output slots, derivation, extent, effect, and
  determinism declarations;
- immutable row/value/vector bindings, reference attachments, lineage, and
  `CompositionState`;
- manifest compilation, static compatibility, applicability, eligibility, and
  guarded invocation;
- `ExecutionResult`, output validation facts, `ProposedTransition`, and
  transition validation.

### Provisional Workbench extensions and conditional Data Contracts promotion

These types carry provider-neutral custody only. Locator payloads and method
payloads remain domain-owned typed contracts. K0 defines them in the Workbench
pack first. They are proposals for Data Contracts only after the family-specific
two-seam gate passes.

```text
SourceArtifactRef
  artifact_version: ArtifactVersionRef
  producer_identity: VersionIdentityRef
  payload_contract_id: VersionedId
  media_type: string
  content_digest: Digest
  resolver_ref: VersionIdentityRef

SourceUnitRef
  source_artifact_binding: exact immutable ValueBinding
  source_unit_id: non-empty opaque ID scoped to the artifact version
  descriptor_binding: exact immutable ValueBinding whose registered payload
    contains the typed locator, context value/ref, normalization rules, and
    their digests
  source_window_reference: ReferenceAttachment bound to the exact source
    artifact version and descriptor payload path

EvidenceSpanRef
  source_unit: SourceUnitRef
  evidence_span_id: non-empty opaque ID scoped to the source unit
  selection_binding: exact immutable ValueBinding whose registered payload
    contains selected value/ref, offsets or occurrence rule, normalization
    rule, and selected/context digests
  candidate_reference: ReferenceAttachment bound to the exact candidate
    artifact version and field/object JsonPointer
  source_window_reference: ReferenceAttachment bound to the same exact source
    artifact version as SourceUnitRef

CandidateReviewDecision
  decision_id: string
  candidate_artifact: ArtifactVersionRef
  reviewer_identity: VersionIdentityRef
  review_policy_identity: VersionIdentityRef
  authority_grant_binding: exact immutable binding naming principal, role,
    scope, validity interval, and granting authority/policy
  target_dispositions: non-empty list of exact field/object reference plus
    accept | edit | reject | withhold, rationale, and replacement ref when edited
  aggregate_disposition: promote | partially_promote | reject | withhold
  rationale: string
  decided_at: timezone-aware datetime

PromotionReceipt
  decision: exact decision identity and digest
  promoted_artifact: ArtifactVersionRef
  supersedes: ArtifactVersionRef | null
  published_transition: exact proposed-transition identity and digest
```

The final field names must be reconciled against current Data Contracts naming
and fixtures. The design requirement is the invariant, not this illustrative
spelling.

`content_digest` means SHA-256 of the exact raw source bytes. The
`ArtifactVersionRef.version_digest` means SHA-256 of the canonical source-
artifact manifest that includes the content digest, media type, producer,
resolver, and payload contract. They are intentionally distinct, and the local
contract must recompute and validate the manifest digest. For a binding whose
payload is exactly the raw source bytes, its payload digest must equal
`content_digest`; otherwise the binding's registered payload contract states
the deterministic relationship. Every descriptor/selection binding must be
resolvable through the declared artifact resolver and revalidated from bytes;
a digest without a resolvable bound payload is invalid.

An authority role is never self-asserted by the decision. The authority grant
is a separately versioned artifact issued under the exact review policy. The
review validator checks principal, role, target scope, decision time, and
allowed dispositions. Aggregate promotion is derived from per-target
dispositions and the policy's required target set; one aggregate action cannot
erase mixed accepted, edited, rejected, or withheld fields.

### Workbench-owned runtime contracts

```text
AdapterRegistration
  action_id + descriptor version
  implementation identity
  request and response model identities
  injected callable
  supported model/environment/resource contracts

AuthorityAssignment
  performer: actor ref | none
  judgment_owner: actor ref | none
  acceptance_authority: actor ref | none
  recommender: actor ref | none
  value_or_goal_authority: actor ref | none
  decision_authority: actor ref | none

MethodInvocationEnvelope
  investigation and invocation IDs
  method owner + method action ID
  exact input bindings
  source-unit/evidence refs
  method request/config artifact
  requested review mode

MethodInvocationReceipt
  normalized/validated invocation fingerprint
  status: succeeded | refused | unresolved | failed
  engine repository and revision
  trace/run identity
  native output artifact refs and public projection ref
  method limitation and claim-bound refs
  typed reason on non-success

InvestigationTransitionReceipt
  prior state fingerprint
  proposed transition
  publication/review decision
  resulting state fingerprint when committed
```

Schema-specific extraction records, QC records, PT records, theory schemas,
quantitative results, and simulation results are explicitly absent from this
shared model.

## Runtime flow and failure behavior

```text
compile action packs
  -> resolve static compatibility and applicability
  -> select an explicit registered adapter
  -> normalize and guard the exact invocation
  -> execute the adapter
  -> validate output payload and references
  -> create ExecutionResult and ProposedTransition
  -> review/promotion policy
  -> atomically publish or preserve prior state
```

| Failure | Required behavior | Retained evidence / recovery |
| --- | --- | --- |
| unknown action, implementation, contract, or major version | refuse before execution | typed incompatibility/refusal; no state change |
| artifact/source digest mismatch | refuse before parsing or model call | exact mismatched identity and source; obtain/freeze a new version |
| missing or ambiguous evidence span | quarantine candidate; no promotion | candidate, source unit, and binding refusal remain inspectable |
| prompt/schema/model route incompatibility | fail before paid call where detectable | rendered prompt/schema/config identities; correct and retry as a new invocation |
| model call or structured decode fails | produce failed receipt; no fabricated fallback | `llm_client` trace and bounded explicit retry state; never substitute hand-authored output as model output |
| adapter raises or returns wrong type | produce failed receipt; no transition | exact invocation and adapter identity; repair and resume that action |
| review absent or unauthorized | keep pending/withheld | candidate and review request; await attributable decision |
| method export incompatible or native publication-blocked | quarantine native output; do not project as accepted finding | native method artifact and refusal/limitation payload |
| downstream integration fails | retain all accepted upstream artifacts | resume integration only; do not rerun expensive upstream stages |

No retries, route switches, repairs, or fallbacks are invisible. The current
single-call NYC extraction remains bounded by its existing explicit model,
trace, and cost configuration; a material multi-call graph must receive a
separate call budget before execution.

## Positive fixtures and negative controls

The same portable fixture set must run on producer and consumer sides where a
contract crosses repositories.

1. **NYC extraction fixture:** two exact frozen source units, an arbitrary
   registered prediction/concern schema, candidate output, exact anchors, and
   the retained authentic trace.
2. **P5 QC/PT seam fixture:** existing QC input, source artifacts, PT return,
   and native review/publication states represented as opaque typed bindings.
3. **Digest mutation:** change one source, candidate, request, or native output
   byte and require pre-publication refusal.
4. **Ambiguous span:** duplicate selected text inside the source unit and
   require `bind_exact` refusal.
5. **Unauthorized or mixed promotion:** accept without an exact policy/grant,
   use an expired or out-of-scope grant, or aggregate mixed field dispositions
   incorrectly; require refusal.
6. **Method flattening:** attempt to map PT comparative support or QC support
   status into generic confidence; the consumer contract must have no such
   field/path.
7. **Native block preservation:** a publication-blocked PT artifact must remain
   blocked after Workbench projection.
8. **QC anchor revalidation:** validate exported QC spans against the separately
   bound source bytes because the current QC handoff validates referential
   integrity but does not re-verify quote hashes/offsets during export.

Portable contract fixtures prove custody and compatibility. They do not prove
runtime adoption. Each slice also needs one consumer-path execution receipt.

## Risk-ordered planning horizon

### Slice K0 — Freeze the shared seam and current owners

**Epistemic state:** `fully_specifiable_now`

**Class:** dependency-resolution enabler, not the visible MVP

- Reconcile stale Project Meta paths for Data Contracts and QC through their
  owning authority; pin current canonical revisions.
- Encode the Workbench action pack, provisional Workbench-owned source/evidence
  refs, review and runtime adapter interfaces, and both-sign portable fixtures
  using current Data Contracts extension points. Do not change Data Contracts
  public types in K0.
- Do not change producer methods or accept NYC content.
- **Success:** both current Data Contracts composition validators and
  Workbench consumer models accept the positive fixtures and reject digest,
  ambiguity, unauthorized-promotion, and generic-confidence controls.
- **Return path:** immediately execute K1; K0 alone is not product progress.

### Slice K1 — Run NYC through the primitive path

**Epistemic state:** `fully_specifiable_now`

**Class:** authentic vertical and first visible architecture proof

- Replace the NYC runner's case-owned execution flow with registered
  `source.segment -> text.extract_structured -> evidence.bind_exact` actions.
- Keep NYC-specific source definitions, prompt asset, and output schema as
  configuration/domain payloads, not adapter logic.
- Use the retained authentic `llm_client` call only as evidence if the exact
  implementation/configuration and output can be bound truthfully; otherwise
  run one new non-cached canary after local preflight.
- **Success:** the existing NYC review packet is reproduced through the
  registered action path; a test proves bypassing or mutating that path fails;
  browser/API content remains pending human review.

### Slice K2 — Prove a second authentic seam

**Epistemic state:** `fully_specifiable_now` after K0 contracts freeze

**Class:** integration/conformance vertical

- Represent the existing QC-to-PT-to-QC P5 round trip through the same artifact,
  source, invocation, receipt, review-lineage, and transition contracts.
- Keep the native QC and PT payloads opaque and authoritative; do not rerun the
  engines merely to populate the Workbench.
- **Success:** one Workbench investigation state traverses both native artifacts,
  detects source/artifact/review mutations, and preserves the PT publication
  block and QC `retain_unconfirmed` disposition.
- **Evidence limit:** K2 can prove common artifact/source custody, native review
  lineage, invocation receipts, and transition mechanics. Because it does not
  execute `text.extract_structured`, `evidence.bind_exact`, or
  `candidate.review`, it supplies no reuse evidence for those action
  implementations.
- **Promotion:** only the exact common contract families exercised by both K1
  and K2 become candidates for shared adoption.

### Slice K2b — Bind authentic source acquisition

**Epistemic state:** `fully_specifiable_now` after K0 contracts freeze

**Class:** parallel authentic boundary probe with an immediate return path

- Register an Open Web Retrieval adapter for `research.source.acquire/1` and
  retrieve one official NYC source through its current strict fetch/extract
  seam, using search only when discovery is part of the declared request.
- Compare the fetched bytes and provenance with the frozen source identity. A
  match demonstrates replayable acquisition; a mismatch is retained as a new
  source version and must not silently replace the evidence freeze.
- **Success:** a joined Workbench/OWR tool receipt produces a content-addressed
  source artifact consumed by the same source-reference contract as K1.
- **Return path:** either bind the matching artifact into K1 replay or preserve
  the drift receipt and continue K1 from the already frozen bytes.

### Dependency subplan K2x — Find a second structured-extraction consumer

**Epistemic state:** `exploration_required`

- **Question:** can a non-NYC workflow use the exact same
  `research.text.extract_structured/1` implementation and source/evidence/review
  families without moving its method semantics into the Workbench?
- **Why it is not derivable now:** current QC/PT seams use structured model calls
  internally but do not consume the proposed Workbench action; Theory Forge has
  an arbitrary-schema extraction stage but owns its compiled method runtime.
- **Cheapest representative probe:** test one existing, rights-clear,
  non-NYC source/schema pair through the adapter as a candidate-producing
  operation, with the owning method or product treating it as input rather than
  silently replacing its native inference. Candidate sources include a pinned
  Theory Forge operationalization input or another frozen policy document.
- **Controls:** no NYC literals in the implementation; different Pydantic
  output contract; exact evidence binding and mixed field review; no bypass of
  a method-owned inference stage.
- **Readout:** `compatible_second_consumer | case_local_only |
  would_move_method_semantics` with exact invocation/consumer receipts.
- **Stopping rule:** one representative candidate and one method-ownership
  check; do not start a broad use-case search or method migration.
- **Promotion:** call `text.extract_structured`, `bind_exact`, or candidate
  review reusable only for the exact actions/families the second consumer
  exercised. Otherwise retain them as clear, case-neutral Workbench-local
  primitives and state that ecosystem reuse is unproven.

### Slice K2c — Promote only proven contract families

**Epistemic state:** `conditional`

- Condition: two authentic compatible seams have exercised the same exact
  provisional family and the owning Data Contracts checkout/path is reconciled.
- Add that family, its positive/negative portable fixtures, and compatibility
  behavior to Data Contracts; pin the accepted revision in the Workbench and
  replace the provisional local definition.
- A family that fails the gate remains local and visible; it does not block the
  NYC MVP unless the MVP itself needs cross-repository use of that family.
- **Success:** both producer and consumer fixtures plus an authentic Workbench
  invocation use the pinned Data Contracts definition; no duplicate local
  authority remains.

### Slice K3 — Contributor evidence disposition

**Epistemic state:** `human_decision_required`

- Present the three existing NYC statements only after K1 proves their
  architecture and provenance path.
- The contributor may accept, edit, reject, or withhold each exact candidate.
- **Invariant:** architecture adoption does not predetermine content acceptance.

### Slice K4 — Method-owned QC over the frozen hearings

**Epistemic state:** `conditional`

- Condition: the exact source/evidence/review contract used by K1 is accepted
  and the six-hearing corpus still verifies.
- Invoke QC through a Workbench adapter using content-bound source artifacts;
  QC retains method semantics, review, reflexivity, negative cases, and no-
  prevalence limits.
- **Success:** authentic traced QC output validates natively, crosses the shared
  envelope, and appears in the same investigation without copying QC internals.

### Slice K5 — Integrate and review the cohesive MVP

**Epistemic state:** `conditional`

- Condition: reviewed extraction, accepted QC output, and accepted quantitative
  receipt exist at exact versions.
- Compose the joint display, explicit value inputs, bounded policy appraisal,
  open questions, and inspectable export.
- **Success:** fresh browser/API/export walkthrough at one immutable revision;
  a researcher can explain what was observed, elicited, generated, derived,
  reviewed, and still unknown; methodological/human review is recorded.

### Later capability portfolio

Theory Forge application, Process Tracing for a suitable causal question,
simulation, ontology projection, and a broader computational-social-science
adapter remain typed extension points. They enter the critical path only when
the policy question needs them and their current native seam is verified.
Open Web Retrieval is different: acquisition is a core operation and its
current seam is reusable, so K2b proves its adoption without making live web
state replace the frozen NYC evidence. Repository existence alone is never an
MVP dependency.

## Compatibility, rollout, and reset boundary

- Producers remain strict; Workbench consumers accept additive fields and fail
  unsupported major versions.
- Existing case-specific NYC and P5 artifacts are retained as comparison inputs,
  then superseded only after the primitive path reproduces their supported
  behavior at an exact revision.
- There is no bulk migration. Each adapter is adopted one consumer path at a
  time.
- Failure before publication leaves prior `CompositionState` unchanged.
- Every expensive or model-backed stage checkpoints exact inputs,
  configuration, trace, and outputs so later failures resume locally.
- Course-check tripwires are the workspace defaults: roughly 45 minutes without
  a visible capability, two supporting-only increments, or three failures at
  the same boundary. A tripwire triggers comparison of the current path with
  the best next 30–60 minute outcome; it does not roll back or shrink scope.

## Evidence and non-claims

### Current evidence used

| Source | Revision / location | What it establishes |
| --- | --- | --- |
| Workbench | `e06b1cbe49cee1b1e6ef995b68308342646381a4`; `pyproject.toml`, `investigation_spine.py`, `nyc_crz_evidence_slice.py`, `run_nyc_crz_extraction_canary.py` | no Data Contracts adoption or runtime resolver; typed but case-specific NYC/P5 paths |
| Data Contracts | local `d845be0c5813ab26e9bf2f1eaf4473a262ac541b`, known remote `33746efd75b309aeb2850666859e7b7102190385`; `composition/contracts.py`, `compiler.py`, `transitions.py`, `conformance.py` | reusable semantic composition substrate; intentional absence of dispatch/persistence; neutral source-unit and evidence-review gaps |
| Qualitative Coding | local `4ea0ce6ca15a63ba91b1a3790e4737b411389902`, known remote `7dbbf91d07fa6e78b712dbe2ee9c8378ad7b8340`; `domain.py`, `pipeline_engine.py`, `process_tracing_handoff.py` | real typed method engine and QC-to-PT handoff; native review/anchor semantics; no Data Contracts dependency |
| Process Tracing | inspected current origin `b9dfe6cf6ff0c40c872bd6d3dc686d6c3fb01db9`; `pipeline.py`, `source_packet.py`, `export.py`, `theory_test_return.py`, `evidence_anchor_view.py` | real method runtime, `pt_export_v2`, native publication controls, and an experimental shared-anchor shape; no generic QC handoff consumer |
| Open Web Retrieval | canonical checkout `/home/brian/code/active/open_web_retrieval` at `531a0937258320cccbaac0e868a7f05f399e2de7`; `models.py`, `client.py` | current strict search/fetch/extract seam with content hashes, extraction provenance, explicit partial mode, and joined tool traces; requires a Workbench adapter because Data Contracts is optional/no-op in the producer |
| `llm_client` | canonical checkout `/home/brian/code/active/llm_client` at `be189820d1412ec4d19ba148ed1cbdf79c387b3d`; `core/client.py`, `execution/call_wrappers.py`, `observability/observed_runs.py` | current arbitrary-Pydantic structured execution, route/budget/trace metadata, and durable outer-run custody; boundary registry metadata alone is not enforcement |
| Theory Forge | `9ec293f96b05a56115cfa4c1686ab7032fd79411`; `schema_compile.py`, `runner.py`, `operationalization.py` | real method-owned compile/run behavior and a bounded Entman export, but no provenance-complete generic executed-run export; conditional after the kernel |
| SB Ontologies | `/home/brian/code/sb_ontologies` at `ec1aea3f199b4ca19615679c5428c9e603349129` | historical/prototype representation ideas with direct SDK calls and loose outputs; not a current runtime or ontology/projection owner for the MVP |
| Existing product assessment | `docs/EVIDENCE_TO_ACTION_PRODUCT_INTEGRATION_MAP.md` | Workbench integration ownership and method-engine separation |
| Phase 1 pilot | `docs/research/method_decomposition/phase1_pilot/` at merged Workbench history | authority, information-origin, prespecification, feedback, reflexivity, and exact-anchor concerns that the kernel must preserve without declaring the compact operation model canonical |

### Known authority/state concerns

- Project Meta points to missing `~/projects/data_contracts`; the inspected
  checkout is `/home/brian/code/active/data-contracts`.
- Project Meta points to missing `/home/brian/projects/qualitative_coding`; the
  inspected checkout is `/home/brian/code/qualitative_coding`.
- The Data Contracts checkout has pre-existing untracked `build/` and is three
  commits behind its remote; the remote delta is documentation/ignore-only.
- QC is one documentation-only commit behind its remote.
- Project Meta points to stale project checkouts for Open Web Retrieval and
  `llm_client`; their current canonical `code/active` checkouts are the ones
  cited above.
- One active Process Tracing claim owns broad `pt`, `scripts`, `tests`, and
  `docs` surfaces. K0/K2 must remain read-only there until that lane closes or
  a non-overlapping exact path is agreed.
- The exact-session mailbox for this Workbench design lane contained no active
  messages when inspected.
- A separate computational-social-science repository described as being on the
  Desktop was not discoverable from this host. It is not silently equated with
  SB Ontologies and is not required to settle the kernel; its exact path is
  needed before claiming portfolio coverage.

### Non-claims

This packet does not claim that the candidate action names are canonical, that
Data Contracts is currently adopted by the Workbench, that a runtime adapter
exists, that NYC evidence is accepted, that QC/PT interoperate generically, or
that the MVP is complete. It is a facilitator recommendation pending exact
contributor disposition.

## Planning-method feedback

```yaml
planning_method_feedback:
  status: candidate
  plugin_version: 0.2.0+codex.20260813162256
  skills: [initiative-roadmap, bounded-design, work-unit-graph]
  context: Mixed Methods Workbench Plan #5 at e06b1cbe49cee1b1e6ef995b68308342646381a4
  observed_behavior: >-
    The coordinated plan made case-specific extraction and quantitative lanes
    ready, then presented content-acceptance decisions before proving that the
    visible vertical was composed through reusable capability seams. The
    contributor had to interrupt and restate that reusable primitives—such as
    structured extraction from text—were the intended architecture unit.
  expected_behavior: >-
    Before making a vertical implementation-ready, planning should explicitly
    classify every operation as existing shared capability, method-owned
    capability, case-local adapter, or unresolved seam; it should require a
    consumer-path adoption proof for every claimed reusable capability.
  impact: >-
    Two useful but case-shaped implementation lanes completed before the
    architecture question was resolved, causing review confusion and rework in
    sequencing.
  evidence:
    - contributor correction in this coordination thread
    - docs/plans/005_nyc_crz_mvp.md
    - scripts/run_nyc_crz_extraction_canary.py
    - src/mixed_methods_workbench/nyc_crz_evidence_slice.py
  proposed_change: >-
    Add a pre-decomposition capability-adoption checkpoint to bounded-design
    and work-unit-graph: name the canonical seam and owner, select reuse,
    extend, supersede, or explicit exception, and require an authentic intended
    consumer receipt before marking a reusable capability implemented.
  canonical_target: >-
    Inside-Success/company-planning docs/PLANNING_METHOD_FEEDBACK.md; reconcile
    with draft PR #108 rather than creating a duplicate record.
```

This feedback does not alter the Workbench outcome or adopt this packet.

## Packet review

If accepted, this packet should replace Plan #5's current content-review-first
sequence with K0–K5 while retaining all authentic NYC artifacts as pending
inputs. The canonical `PLANNING_STATUS.md`, Plan #5 graph, and capability graph
must then be revised together; a coordinated work-unit graph may be generated
only from the accepted packet revision.

Before adoption, the unresolved material choices are:

1. whether to accept the three-owner architecture (Data Contracts semantics,
   Workbench runtime, method-repository inference);
2. whether the two proposed neutral contract families are the correct
   Workbench-local provisional extensions and should be promoted family by
   family only after the stated evidence gate; and
3. whether K1 NYC plus K2 P5 QC/PT is sufficient only for their common custody
   families, with K2x required before any structured-extraction/binding/review
   reuse claim.

The recommended disposition is to **accept** all three. The important
alternative is to keep even proven families Workbench-local through the entire
MVP and decide Data Contracts promotion afterward. That avoids a mid-MVP
cross-repository change but leaves duplicate custody semantics in an explicit
temporary exception and delays proof that the intended shared owner is actually
usable.
