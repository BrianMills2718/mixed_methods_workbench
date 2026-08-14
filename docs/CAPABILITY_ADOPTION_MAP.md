# Capability Adoption Map

Status: adopted initiative baseline; read-only census evidence, not capability
certification or implementation authority

Updated: 2026-08-13

## Purpose

This map answers a narrower question than the method-decomposition ledgers:
what useful machinery already exists, who owns it, whether a stable seam is
available, whether an authentic consumer has used it, and what the Mixed
Methods Workbench should do about it.

The map distinguishes four maturity states:

| State | Meaning |
| --- | --- |
| `implemented_internal` | Code exists and may be tested inside its repository. |
| `stable_seam` | A typed, versioned public boundary exists. |
| `adopted_consumer` | An intended external or product consumer actually uses the boundary. |
| `observed_runtime` | A relevant authentic execution or receipt exists. |

Passing an earlier state does not imply a later one. Synthetic fixtures prove
shape, not substantive behavior.

## Evidence snapshot

| Repository | Inspected revision | Role in this census |
| --- | --- | --- |
| `mixed_methods_workbench` | `e06b1cbe49cee1b1e6ef995b68308342646381a4` | Product/integration authority and current NYC example. |
| `data-contracts` | `d845be0c5813ab26e9bf2f1eaf4473a262ac541b` | Typed action, binding, guard, result, and transition grammar. |
| `llm_client` | `be189820d1412ec4d19ba148ed1cbdf79c387b3d` | Structured model execution and observability. |
| `open_web_retrieval` | `531a0937258320cccbaac0e868a7f05f399e2de7` | Search/fetch/extract transport and receipts. |
| `qualitative_coding` | `4ea0ce6ca15a63ba91b1a3790e4737b411389902` | Qualitative and grounded-theory protocol owner. |
| `process_tracing` | `8bada47d371303a0d66dab3aad96addc8f4fb47e` | Process Tracing protocol owner. |
| `grounded-research` | `0b46fc144b50360c6912e8ba0e2dfe15704f1d18` | Independent analysis and adjudication owner. |
| `theory-forge` | `9ec293f96b05a56115cfa4c1686ab7032fd79411` | Theory compile/application owner. |
| `onto-canon6` | `a271d37e07f827281070577eeb71c23589ecd4d0` | Governed assertion and semantic-projection owner. |
| `Digimon_for_KG_application` | `96a838ff8d9fd9c8bb40e6e23699974681c9be0c` | Graph/retrieval owner and adopted Data Contracts consumer. |
| `sb_ontologies` | `ec1aea3f199b4ca19615679c5428c9e603349129` | Donor/idea source only; not registered as a current platform authority. |

The Project Graph currently points to stale checkout locations for Data
Contracts, `llm_client`, and Open Web Retrieval; this census used the current
canonical work under `/home/brian/code/active/`. No separately governed
computational-social-science repository, including a Desktop checkout, was
discoverable from the current Project Graph or bounded workspace census.
Project Meta contains a tentative computational-social-science program, which
is not equivalent to an implemented repository.

Reverify revisions and Project Graph routing before implementation.

## Repository-level dispositions

| Owner | What exists now | Seam/adoption truth | Disposition |
| --- | --- | --- | --- |
| Data Contracts | Strict producer/permissive consumer models; action descriptors and packs; typed inputs, outputs, resources, effects, and determinism; pure compilation; invocation and transition guards. | Stable typed substrate. DIGIMON genuinely consumes compiled manifests and guarded transitions. It intentionally does not load or dispatch implementations. | `reuse` for composition grammar; `extend` only after two authentic consumers prove a missing neutral field. |
| `llm_client` | Arbitrary Pydantic structured output, prompt/model/route/budget identity, retries and disclosed fallbacks, traces, cost, and observed runs. | Stable shared runtime used by multiple repos. | `reuse`; it owns structured model-call execution used within `semantic_transform`, not caller-owned instructions, schemas, validation, anchoring, method meaning, or evidence decisions. |
| Open Web Retrieval | Typed search, fetch, and extraction with source metadata, hashes, strict/partial modes, and tool receipts. | Shared retrieval implementation exists. Workbench still needs an adapter and must own query intent/admission policy. | `wrap`; do not reimplement web transport. |
| Mixed Methods Workbench | Investigation Spine, UI/API, frozen NYC sources, authentic structured extraction trace, exact evidence bindings, deterministic quantitative audit, review gate, and bounded simulation appraisal. | Authentic examples exist, but current NYC extraction calls `llm_client` directly, returns a local receipt, hard-codes case semantics, and has no Data Contracts dependency. | `extend` as orchestrator; refactor one existing path through shared actions before adding another vertical. |
| Qualitative Coding | Generic internal structured extraction, pipeline stages, coding and grounded-theory state, constant comparison, anchors, review, memos, reflexivity, and strict project artifacts. | Strong method implementation; reusable execution forms are internal rather than a neutral cross-repo ABI. | `keep_method_owned`; `wrap` selected public operations and receipts. |
| Process Tracing | Generic internal LLM passes, deterministic Bayesian calculations, rival/partition/evidence/mechanism protocols, refinement transitions, source acquisition, and strict exports. | Strong method implementation and exports; no generic QC/PT operation ABI. | `keep_method_owned`; `wrap` selected public operations and receipts. |
| Theory Forge | Theory-schema compilation and theory-specific application machinery. | Useful strict method seam and deterministic CPT/Choices13k counterexample; general provenance-complete application-run export remains incomplete. | `keep_method_owned`; use as a conformance example, not the universal extraction kernel. |
| Grounded Research | Typed local `EvidenceBundle`, independent analysis, dispute/verification state, and adjudication. | Current outbound shared export writes plain JSONL dictionaries, while OntoCanon accepts typed `ClaimRecord`; the integration test constructs records directly. End-to-end adoption is not proven. | `keep_method_owned`; `wrap` only after a real typed producer-consumer seam is observed. |
| OntoCanon | Ontology packs, candidate assertions, exact passages, validation/review/promotion, stable identity, Foundation IR 1.3, and deterministic rule-owned semantic projection. | Strong producer boundary. Current graph evidence path exists; projection consumers and claims must remain exact and versioned. | `reuse` conditionally for governed assertions/projections; not the generic arbitrary-output primitive or mandatory MVP path. |
| DIGIMON | Graph materialization, typed graph/text/vector/structured-source actions, catalog compilation, guarded execution/commit, traversal, ranking, and retrieval. | Strongest current proof that Data Contracts can support a real composition runtime. Fully situational adaptive action-DAG value remains unproven. Semantic projection SP-03 evidence re-entry remains open. | `reuse` as retrieval/graph owner when needed; reuse its composition lessons, not its whole runtime as the Workbench. |
| SB Ontologies | Earlier ontology/theory experimentation. | Direct provider calls, loose dictionaries, and reported fidelity gaps; not a registered current owner. Theory Forge and OntoCanon have stronger relevant seams. | `defer`; mine ideas only. |
| Computational social science | Project Meta program language, but no governed standalone repository located. | No callable seam, exact revision, or consumer evidence to adopt. | `missing` as a repository-level owner; locate/register it before relying on it. |

## Capability-level adoption map

| ID | Capability | Current owner and evidence | Current maturity | Disposition and MVP use |
| --- | --- | --- | --- | --- |
| CAP-01 | Declare typed composable actions | Data Contracts action descriptors/packs and compiler. | `adopted_consumer` through DIGIMON. | `reuse` unchanged. |
| CAP-02 | Resolve applicability and guard invocation/transition | Data Contracts compiler and transition guards. | `adopted_consumer` through DIGIMON structured-source execution. | `reuse`; Workbench supplies its state and adapter resolver. |
| CAP-03 | Execute structured LLM transformations | `llm_client`; QC/PT/TF and Workbench use structured outputs. | `observed_runtime`. | `reuse` model-backed execution; semantic transforms may also have human, deterministic, or other domain implementations. No Workbench model client. |
| CAP-04 | Search, fetch, and capture web sources | Open Web Retrieval. Grounded Research constructs its client and executes typed `SearchQuery` requests through a compatibility shim. | `adopted_consumer`; authentic runtime status remains separately bounded. | `wrap`; retain version-skew compatibility as visible debt, and keep evidence admission method/study-owned. |
| CAP-05 | Extract structured candidates against an arbitrary typed contract | Machinery exists in `llm_client` and internal QC/PT handlers; Workbench NYC proves a case-specific use. | `implemented_internal`; no adopted research-facing cross-repo action. | `extend` through a Workbench-owned research action pack that uses Data Contracts grammar and a Workbench adapter; first consumer is refactored NYC. Promote only proven neutral fields into Data Contracts after the two-consumer gate. |
| CAP-06 | Freeze source versions and identify exact units | Open Web Retrieval, QC, OntoCanon, and Workbench each implement parts. | Fragmented `implemented_internal`/local seams. | `wrap` existing custody; design only the smallest common reference required by authentic consumers. |
| CAP-07 | Bind candidate fields to exact evidence | QC, OntoCanon, and Workbench have anchor models and checks. | Authentic local evidence; no shared adopted contract. | Start Workbench-local over Data Contracts extension points; promote only after two compatible consumers. |
| CAP-08 | Validate structural output | Pydantic and owner-local validators. | `observed_runtime`. | `reuse`; keep separate from methodological validation. |
| CAP-09 | Validate methodological admissibility | QC/PT/TF/domain engines. | Strong owner-local behavior. | `keep_method_owned`; expose typed findings/receipts. |
| CAP-10 | Review, adjudicate, and promote candidates | OntoCanon, QC, PT, and Grounded Research have distinct implementations. | Strong owner-local behavior; no universal decision policy. | Share only neutral frozen-target/authority/disposition envelopes after compatible seams; keep review rules local. |
| CAP-11 | Apply lineage-preserving state transitions | Data Contracts supplies proposed-transition guards; PT has explicit immutable refinement application; QC has project-state updates. | Substrate adopted; method transitions owner-local. | `reuse` neutral guards and `wrap` method transitions. |
| CAP-12 | Iterate and control method protocols | QC pipeline and PT pipeline have explicit state/order/gates; DIGIMON has typed retrieval composition. | `implemented_internal` in multiple domains. | Do not build a universal planner yet. Standardize receipts and applicability first. |
| CAP-13 | Qualitative coding and category development | Qualitative Coding. | Strong method implementation. | `keep_method_owned`; invoke through adapter. |
| CAP-14 | Grounded-theory development | Qualitative Coding. | Strong partial/full protocol machinery with method-specific adequacy limits. | `keep_method_owned`; never reduce to one semantic transform. |
| CAP-15 | Rival-explanation Process Tracing | Process Tracing. | Strong method implementation and export. | `keep_method_owned`; invoke through adapter. |
| CAP-16 | Theory operationalization and application | Theory Forge. | Bounded stable artifacts; complete general application export gap. | `keep_method_owned`; conditional MVP dependency only if study design requires it. |
| CAP-17 | Independent claim adjudication | Grounded Research. | Strong local capability; current shared export mismatch. | `keep_method_owned`; defer cross-repo adoption until typed seam is real. |
| CAP-18 | Governed semantic assertion lifecycle | OntoCanon. | `stable_seam` with authentic bounded producer evidence. | `reuse` when cross-document semantic governance is needed. |
| CAP-19 | Semantic/evidence graph projection | OntoCanon producer plus DIGIMON consumer work. | Evidence projection adopted; direct semantic dual-surface path not fully proven. | `defer` from MVP critical path unless question requires graph; require exact evidence re-entry. |
| CAP-20 | Graph/text/vector/structured retrieval | DIGIMON. | Substantial implementation and bounded runtime evidence; adaptive superiority unproven. | `reuse` only for named retrieval need; direct text/search may be sufficient. |
| CAP-21 | Deterministic descriptive measurement | Workbench NYC audit and method/statistical libraries. | Authentic bounded example; no general quantitative adapter owner. | `wrap` established libraries through a narrow Workbench adapter after the target measure is named. |
| CAP-22 | Statistical, predictive, or causal analysis | Established engines and future adapters; owner unresolved for portfolio. | Mixed; not censused as one stable seam. | `keep_method_owned`/`missing`; decide per study design, never create one generic inference engine. |
| CAP-23 | Simulation and scenario comparison | External simulation owners; Workbench has a bounded Cybernetic Influence projection. | Bounded authentic projection, not a canonical general seam. | `keep_method_owned`; adapter only when required. |
| CAP-24 | Policy-option appraisal | Workbench plus explicit human/value authority; Mist Trail content is manually performed. | Product projection exists; no executing general appraisal engine. | `extend` later from a real decision case; do not treat typed artifacts as computed analysis. |
| CAP-25 | Joint display and mixed-methods meta-inference | Workbench. | `missing` authentically. | `extend` after qualitative and quantitative artifacts are accepted. |
| CAP-26 | Investigation continuity and orchestration | Workbench Investigation Spine. | Authentic bounded UI/API; limited action runtime. | `extend` over Data Contracts; retain one investigation state without absorbing method state. |
| CAP-27 | Reproducible investigation bundle | Workbench and method-native exports have pieces. | Partial local evidence. | `extend` after action/artifact/derivation identities stabilize. |
| CAP-28 | Methodology recommendation | No adopted owner. | `missing`. | `defer` until lower layers work; future planner compiles accepted designs rather than choosing by schema match. |

## False-positive seams and drift

### Workbench NYC extraction

The existing extraction canary directly calls `llm_client` with a
case-specific output type and prompt, then returns a local dictionary receipt.
The durable evidence models include NYC-specific literals and candidate IDs.
It is an authentic observed vertical and a valuable requirements probe, but it
does not prove reusable primitive composition.

### Grounded Research to OntoCanon

Grounded Research's local evidence models are typed, but its current shared
export explicitly writes untyped JSONL dictionaries. OntoCanon's adapter
accepts `epistemic_contracts.ClaimRecord`, and the integration test constructs
that object directly instead of consuming Grounded Research's output. Both
sides have code; the claimed producer-to-consumer path is not demonstrated.

### OntoCanon to DIGIMON

The assertion/evidence import path is real. OntoCanon also produces a typed
deterministic semantic projection, and DIGIMON has accepted two consumer
slices. The remaining promotion evidence is a real query that traverses a
direct semantic edge and re-enters its exact supporting assertion and source
evidence. Until then, do not describe the full dual-surface path as complete.

### Repository routing

Project Graph paths for several shared repositories lag the current canonical
checkouts. This does not invalidate the inspected code, but it can cause future
agents to inspect or modify the wrong clone. Project Meta owns the routing
repair; this Workbench map records the dependency and does not edit cross-repo
authority.

## Immediate decision

The next implementation should not be another policy vertical. It should be a
bounded refactor of the current NYC structured extraction through one generic
action composed from existing Data Contracts and `llm_client` capabilities.

The next design packet must settle only:

- versioned source-unit and output-contract references;
- instruction/method-policy identity;
- execution policy and `llm_client` receipt binding;
- candidate and field-level exact evidence anchors;
- frozen candidate review state and authority;
- invocation failure and transition behavior; and
- how a method-owned schema/validator attaches without moving into the
  Workbench or Data Contracts.

It must not design dynamic plugin discovery, a universal evidence ontology, a
generic method planner, a graph requirement, or the full MVP workflow.

## Evidence locations

Key source locations used for this snapshot include:

- Workbench: `pyproject.toml:5`,
  `scripts/run_nyc_crz_extraction_canary.py:162`, and
  `src/mixed_methods_workbench/nyc_crz_evidence_slice.py:20`;
- Data Contracts: `src/data_contracts/models.py:15`,
  `src/data_contracts/composition/contracts.py:739`,
  `src/data_contracts/composition/compiler.py:1`, and
  `src/data_contracts/composition/transitions.py:241`;
- DIGIMON: `digimon/catalog.py:1` and
  `digimon/composition/structured_source_public.py:429`;
- Qualitative Coding: `qc_clean/core/llm/llm_handler.py:59`,
  `qc_clean/core/pipeline/pipeline_engine.py:449`,
  `qc_clean/core/pipeline/stages/gt_constant_comparison.py:225`, and
  `qc_clean/core/grounded_theory_development.py:23`;
- Process Tracing: `pt/llm.py:338`, `pt/pass_partition.py:33`,
  `pt/apply_refinement.py:21`, and `pt/pipeline.py:1904`;
- Grounded Research: `src/grounded_research/models.py:340` and
  `src/grounded_research/shared_export.py:1`;
- OntoCanon: `src/onto_canon6/adapters/foundation_assertion_export.py:69`
  and `src/onto_canon6/adapters/semantic_graph_projection.py:1`; and
- DIGIMON Plan 186 for the remaining semantic-projection consumer gate.

These are inspection anchors, not permanent line-stable API references. Exact
revisions above control this snapshot.
