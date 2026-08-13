# Evidence-to-Action Product Integration Map

**Status:** current cross-repository product assessment and recommended
implementation frontier

**Prepared:** 2026-08-13

**Decision supported:** how independently developed analytical engines become
one cohesive product without merging their methodologies

## 1. Decision

The program should stop treating method-catalog completion as the product
critical path. The cohesive product should be a Workbench-owned
**investigation spine** that preserves one question, evidence universe,
analytical plan, method runs, findings, unresolved questions, reviews, and
next actions while delegating substantive inference to method-owned engines.

The engines should not be merged:

- `qualitative_coding` remains the qualitative evidence, coding,
  interpretation, grounded-theory, and qualitative-review engine;
- `process_tracing` remains the within-case rival-explanation, diagnostic
  evidence, mechanism, and comparative-support engine;
- `theory-forge` remains the published-theory extraction,
  operationalization, compilation, and theory-application engine;
- `cybernetic_influence_v2` remains the governed simulation engine;
- future statistical, forecasting, optimization, and decision engines retain
  their own estimands and validity rules.

The Workbench should own the user-visible continuity among them. It should not
own their internal semantic judgments.

## 2. Synthesis boundary and authority

This assessment answers one question:

> What is the smallest architecture and implementation sequence that can turn
> the current repositories into one understandable Evidence-to-Action product?

Status was read from each repository's current canonical instructions and
status authority, then checked against the owning code and focused tests. The
current user direction to restore product cohesion controls prioritization;
existing method roadmaps remain authoritative only inside their repositories.

| Source | Role in this assessment |
| --- | --- |
| `mixed_methods_workbench/CLAUDE.md`, `PROJECT.md`, `docs/PLANNING_STATUS.md`, and current source | Integration ownership, current Workbench behavior, and authorization boundaries |
| `qualitative_coding/CLAUDE.md`, `docs/VISION_AND_ARCHITECTURE.md`, `docs/CURRENT_STATE_AND_ROADMAP.md`, and current source | Qualitative product boundary and the implemented QC-to-PT round trip |
| `process_tracing/CLAUDE.md`, `docs/INITIATIVE_ROADMAP.md`, `docs/CURRENT_STATUS.md`, and current source | Process Tracing boundary, exports, workbench, and current inference limits |
| `theory-forge/CLAUDE.md`, `docs/ROADMAP.md`, and current source | Theory producer boundary and implemented Entman/CPT seams |
| Project Meta `PROJECT_GRAPH.json` and `cybernetic_influence_v2` authorities | Canonical simulator identity and current simulation capability |
| `data-contracts/CLAUDE.md` | Existing shared-boundary mechanics and known limitations |

Historical plans, schema experiments, archived Cybernetic Influence versions,
and method-decomposition candidates were used only where a current authority
linked to them or where they supplied direct implementation evidence. They do
not define the product.

## 3. Repository-grounded current state

The inspected revisions were:

| Component | Inspected revision | Verified current role | Product integration state |
| --- | --- | --- | --- |
| Mixed Methods Workbench | `2a9365fb76b95f459fa7d248c89430b5b262d9d5` | Question-first method router, method catalog, synthetic QC/PT/GT assembly, Process Tracing topology view, Mist Trail decision fixture, and simulation-to-appraisal boundary | It is the declared integration authority, but it does not own a durable investigation or invoke current producer engines. Its visible examples are separate destinations rather than one evolving study. |
| Qualitative Coding / SQA | `4ea0ce6ca15a63ba91b1a3790e4737b411389902` | Mature qualitative project state, analysis pipeline, evidence step-down, grounded-theory development, theory views, and public demo | It is currently the strongest general researcher-facing host. It contains a real but P5-specific Process Tracing return consumer, so product integration exists inside a producer rather than in the Workbench. |
| Process Tracing | `ff3eb9ac6480881a727cc5b8770a982af03f477a` | Mature method-specific pipeline, source packets, case traces, comparisons, acquisition, exports, reports, and its own workbench | It exposes strong method-native product behavior and `pt_export_v2`, but its user journey and state remain PT-owned. Numerical validity is still under Plan 043 review. |
| Theory Forge | `9ec293f96b05a56115cfa4c1686ab7032fd79411` | Paper-to-schema-to-compile-to-run pipeline, Entman export, and deterministic CPT/Choices13k report | It has useful producer seams, but its active bulk-compilation roadmap is not on the cohesive-product critical path. It lacks a general stable executed-run export for the Workbench. |
| Cybernetic Influence v2 | `a7ebcfacc4c8c27aabaf0cc314a1dadb190f3c34` | Governed simulator with v2 default runtime and bounded v3 architecture proofs | It has a strong operator workbench and causal trace. The existing Workbench simulation appraisal consumed `cybernetic_influence_v3`, which Project Meta does not register as the canonical project. That seam must remain bounded until ownership is reconciled. |
| Data Contracts | `d845be0c5813ab26e9bf2f1eaf4473a262ac541b` | Shared Pydantic boundary primitives, compatibility checks, registry, and observability helpers | Useful as a future mechanics library, but not ready to own orchestration: input validation, multi-argument discovery, callable resolution, persistence, trace joining, and registry discovery have documented gaps. |

### What is genuinely connected now

1. Theory Forge Entman claims enter QC deductive coding through one bounded,
   hash-bound adapter.
2. QC's frozen P5 proposition enters Process Tracing through a bounded,
   P5-specific theory input.
3. Process Tracing returns a publication-aware P5 appraisal to QC; QC renders
   `retain_unconfirmed` and preserves the publication block.
4. The Workbench consumes one pinned Cybernetic Influence comparison and turns
   it into a deliberately non-recommending policy appraisal.
5. The Workbench can assemble synthetic QC/PT/GT-shaped artifacts, but this is
   contract demonstration rather than producer integration.

### What is not connected

- There is no Workbench-owned investigation record spanning producer artifacts.
- A user cannot begin with one policy question and watch the study state evolve
  across QC, PT, theory application, quantitative analysis, simulation, and
  appraisal.
- The Workbench does not launch or resume producer runs.
- QC and PT each provide their own workbench and navigation model.
- Existing cross-repository adapters are case-specific and located in producer
  repositories.
- There is no stable Theory Forge application-run export consumed by the
  Workbench.
- No authentic qualitative-to-quantitative mixed-method design is integrated.
- No one case currently exercises description, explanation, prediction, and
  intervention appraisal with appropriate evidence.

## 4. Diagnosis: where the program drifted

The independent development of QC and Process Tracing is not the primary
problem. Method engines should be independently coherent. The drift occurred
at the product layer:

1. **The integration authority remained mostly a planning surface.** The
   Workbench accumulated catalogs, fixtures, and separate examples without
   acquiring an investigation state or a real cross-engine journey.
2. **Producer repositories became product hosts.** QC and Process Tracing each
   built substantial UIs and workflow orchestration because no higher product
   layer was ready.
3. **Examples became architecture.** Open Science/P5 usefully proved a
   theory-test return, but its anonymized interviews and niche disclosure case
   are too weak to organize the general policy-analysis product.
4. **Method coverage became an end in itself.** The 14-method decomposition can
   still reveal reusable operations, but completing it does not make the
   current systems one product.
5. **Shared-schema debate displaced user continuity.** The first product need
   is not a universal claim or theory ontology. It is the ability to follow one
   investigation across method-owned artifacts without losing identity,
   evidence, status, or next action.

## 5. Cohesive product model

The user should experience one evolving investigation:

```text
Policy question and decision context
  -> governed evidence universe
  -> initial description and interpretation
  -> candidate explanations and alternatives
  -> analytical plan and evidence requirements
  -> one or more method-owned runs
  -> method-specific findings and unresolved questions
  -> prediction, scenario, or intervention appraisal where warranted
  -> reviewed synthesis or recommendation
  -> reusable investigation record and next-evidence agenda
```

The workflow may be linear, a DAG, or cyclic. A result may send the user back
to source acquisition, recoding, construct revision, rival specification,
measurement, or a different method.

### Product-owned mechanics

The Workbench should initially own only:

- `Investigation`: title, policy question, decision context, current status;
- `Scope`: cases/population, time, evidence universe, known exclusions;
- `ArtifactRef`: producer, artifact type and version, object identity,
  content digest, resolver information;
- `RunRef`: method, producer run, configuration/model references, execution
  and review status;
- `Derivation`: exact input references, operation identity, output reference,
  information added or lost;
- `ReviewState`: who or what reviewed an artifact and the disposition;
- `OpenQuestion` and `EvidenceNeed`: unresolved issue, why it matters, what
  could change;
- `Projection`: a user-facing table, graph, text, or vector view tied back to
  its owning artifact;
- navigation, orchestration, compatibility, and the unified browser/API
  experience.

These are product mechanics, not a universal ontology of analytical meaning.

### Method-owned semantics

The Workbench must not normalize the following into generic scores or claims:

- qualitative coding and interpretation decisions;
- grounded-theory adequacy and theoretical-sampling judgments;
- Process Tracing rivals, diagnosticity, likelihood semantics, mechanisms,
  comparative support, and source-coverage limits;
- statistical estimands, identification assumptions, measurements, estimates,
  and uncertainty;
- configurational calibration and solution semantics;
- forecasting leakage, calibration, and backtesting;
- simulation state, mechanisms, scenarios, trajectories, and fidelity;
- policy criteria, value judgments, weights, and recommendation rules.

Adapters may produce readable projections of these objects. The method-native
artifact remains authoritative.

## 6. Target ownership map

| Product responsibility | Owner | Current gap |
| --- | --- | --- |
| Investigation, question, decision context, and overall state | Mixed Methods Workbench | No durable implementation |
| Source/corpus identity and qualitative evidence workspace | QC, referenced by Workbench | Workbench has no real QC export consumer |
| Coding, comparison, grounded theory, and qualitative appraisal | QC | Strong implementation; needs a narrow producer export selected from current `ProjectState` rather than a duplicate schema |
| Published theory extraction and application | Theory Forge | Bounded exports exist; general run export absent |
| Within-case causal testing and evidence acquisition | Process Tracing | Strong implementation and export; Workbench adapter absent |
| Statistical, predictive, and configurational analysis | Method-specific adapters/engines | Ownership unresolved for several families |
| Simulation and scenario comparison | Cybernetic Influence v2 | Canonical export and Workbench adapter unresolved; current V3 projection is bounded only |
| Policy appraisal and decision synthesis | Workbench, with explicit human/value inputs | Mist Trail is manually authored; no executing general appraisal path |
| Cross-method synthesis and joint displays | Workbench | Not implemented authentically |
| Portable boundary mechanics | Native Pydantic now; Data Contracts after demonstrated reuse | Data Contracts limitations prevent adopting its registry/runtime as the product spine now |

## 7. Stable product example strategy

No current example should be asked to prove everything.

| Example | Keep it for | Do not use it as |
| --- | --- | --- |
| Open Science/P5 | Existing authentic QC -> PT -> QC round trip and an honestly inconclusive theory test | The general policy-analysis flagship or proof of broad evidence acquisition |
| Entman | Published-theory -> deductive-codebook seam and constitutive theory preservation | A general theory ontology or causal test |
| Romanian Revolution / 8888 Uprising | Deep Process Tracing case, comparison, source asymmetry, and exact evidence step-down | A complete policy-decision or mixed-methods workflow |
| CPT/Choices13k | Bounded quantitative prediction/application result | A general Theory Forge run contract or integrated prediction product |
| Simulation outbreak appraisal | Model-generated consequence input and truthful refusal to recommend | Real-world intervention evidence |
| Mist Trail | Understandable bounded policy decision, options, consequences, criteria, and a current Workbench page | An executing appraisal engine today; its analytical judgments are hand-authored and exact source bytes are incomplete |

### Recommended flagship candidate

Use **Mist Trail visitor-use management** as the candidate first cohesive
policy-analysis flagship, subject to a short source-availability gate.

It is preferable to Open Science because it is an understandable policy
decision with explicit options and consequences, and it already has a
Workbench surface. It could naturally connect:

- document and public-comment description through QC;
- concepts, stakeholder positions, tradeoffs, and negative cases;
- a theory or logic model of crowding, access, safety, experience, and
  environmental effects;
- within-case Process Tracing of how the decision and implementation occurred;
- visitor-use measurements and before/after or comparative analysis;
- crowd-flow or management simulation;
- criteria- and value-explicit policy appraisal.

This is a recommendation, not a claim that the needed evidence is already
available. Before implementation, verify the official decision documents,
source-use rights, public-comment availability, visitor/use measurements,
decision chronology, and whether any contemporaneous records can support a
real Process Tracing question. If that gate fails, select another bounded
public policy decision using the same criteria rather than returning to P5 by
default.

## 8. Smallest next implementation slice

Build one Workbench-owned **Investigation Spine** using the already completed
P5 round trip as integration test data, while keeping Mist Trail as the
flagship candidate.

### Visible result

One page and matching JSON endpoint show, in plain language:

1. the investigation question and bounded case;
2. the accepted QC proposition that entered testing;
3. the exact Process Tracing run and evidence packet used;
4. the returned method-owned result;
5. why the result is unresolved and publication-blocked;
6. the QC theory disposition (`retain_unconfirmed`);
7. the evidence needed next;
8. the exact producer artifacts, versions, digests, and native views.

The page must look like one investigation, not links to several demos.

### Implementation boundary

- Add a small Workbench-owned `Investigation`/artifact-lineage model.
- Read the existing pinned QC and PT artifacts through narrow adapters.
- Keep the P5 mapping case-specific; do not call it a generic theory-testing
  schema.
- Keep PT judgments in the PT payload and QC theory disposition in the QC
  payload.
- Make JSON and browser views agree.
- Fail on unsupported schema version, digest mismatch, missing source
  reference, or contradictory workflow state.
- Do not invoke an LLM, rerun QC/PT, import producer internals, adopt Data
  Contracts, or create a universal claim/evidence/theory model.

### Pass criteria

- A newcomer can answer: What question was investigated? What did QC produce?
  What did Process Tracing add? What remains unresolved? What evidence is
  needed next?
- Every displayed transition resolves to exact immutable input and output
  artifacts.
- A PT result cannot silently change the QC theory state.
- A publication-blocked PT result cannot appear as a validated explanation.
- Removing or mutating one artifact/digest fails loudly.
- The Workbench becomes the entry point; native QC/PT pages remain available
  as progressive detail rather than competing product home pages.

### What this slice decides

It tests whether the proposed product spine is enough to make two independently
developed engines feel like one workflow. It does not prove that P5 is the
right flagship or that the spine generalizes. The next vertical should apply
the same spine to the selected policy case and reveal which additional
mechanics are actually needed.

## 9. Sequencing after the spine

1. **Investigation Spine:** assemble the existing P5 round trip in the
   Workbench without rerunning analysis.
2. **Flagship source gate:** verify Mist Trail evidence availability and freeze
   the exact policy question, options, time scope, and initial evidence
   universe; select a replacement only if it fails.
3. **Describe:** run or import an authentic QC analysis for the flagship and
   preserve exact passages, stakeholder positions, findings, and open gaps.
4. **Explain:** represent candidate explanations and route one bounded question
   to Process Tracing only if the source design is adequate.
5. **Measure or predict:** add one appropriate quantitative/forecasting strand
   with its own measurement and validation contract.
6. **Evaluate interventions:** consume a real simulation, causal estimate, or
   scenario comparison as one consequence input; keep value judgments explicit.
7. **Synthesize:** create a joint display and bounded recommendation or
   unresolved decision, with every dependency visible.
8. **Generalize selectively:** resume method-decomposition collision analysis
   only for operations and handoffs that the product vertical actually needs.

## 10. Deferred decisions and explicit uncertainties

- Whether the Workbench should eventually launch producer jobs or initially
  remain a read-only artifact orchestrator.
- Whether QC's `ProjectState` needs a new producer export or already contains a
  sufficiently narrow stable projection.
- Whether `pt_export_v2` is sufficient for the flagship or needs a separate
  theory-test/application view.
- Whether Theory Forge needs one generic executed-run export or several
  application-specific exports.
- Whether Mist Trail has enough contemporaneous decision evidence for real
  Process Tracing.
- Which quantitative method and engine best answer the first flagship
  measurement/prediction question.
- Whether Data Contracts should own any mechanics after a second authentic
  seam, and which documented limitations must be fixed first.
- How Project Meta should reconcile canonical `cybernetic_influence_v2` with
  the V3 repository previously consumed by the Workbench.
- When the product requires ethics, privacy, consent, legal, and operational
  governance beyond the current development boundary.

These uncertainties are not blockers to the read-only Investigation Spine.
They are decisions to resolve from the first and second cohesive verticals,
not through another universal schema exercise.

## 11. Superseded critical-path assumption

The current Phase 3 method decomposition remains useful research and should be
preserved. It no longer controls the immediate product critical path. No
collision, capability-promotion, shared-schema, or broad method-coverage claim
should proceed until the Investigation Spine is visible and the flagship
source gate has selected a credible policy case.
