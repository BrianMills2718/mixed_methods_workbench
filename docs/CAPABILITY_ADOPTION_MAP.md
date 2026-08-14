# Capability Adoption Map

Status: adopted initiative baseline; read-only census evidence, not capability
certification or implementation authority

Updated: 2026-08-13

## Purpose

This map answers a narrower question than the method-decomposition ledgers:
what useful machinery already exists, who owns it, whether a stable seam is
available, whether an authentic consumer has used it, and what the Mixed
Methods Workbench should do about it.

Repository existence triggers consideration, not integration. This census is
allowed to borrow an idea or failure lesson without taking a runtime,
dependency, migration, or UI obligation.

The map distinguishes four maturity states:

| State | Meaning |
| --- | --- |
| `implemented_internal` | Code exists and may be tested inside its repository. |
| `stable_seam` | A typed, versioned public boundary exists. |
| `adopted_consumer` | An intended external or product consumer actually uses the boundary. |
| `observed_runtime` | A relevant authentic execution or receipt exists. |

Passing an earlier state does not imply a later one. Synthetic fixtures prove
shape, not substantive behavior.

Before an implementation disposition such as `reuse`, `wrap`, or `extend` can
enter the current critical path, assign a selection disposition:

| Selection disposition | Meaning |
| --- | --- |
| `adopt_now` | A named current need is best served through the authoritative seam and an intended consumer will prove it. |
| `adapt_later` | Promising, but a named trigger or contract gap prevents current adoption. |
| `donor_only` | Reuse ideas, fixtures, or lessons without a repository/runtime dependency. |
| `defer` | No current decision improves from integration or deeper comparison. |
| `reject` | The capability conflicts with the target boundary or costs more than the value it could add. |

`adopt_now` requires a named MVP need, an authoritative owner and stable seam,
lower total complexity than a bounded local path, preserved authority and
provenance, and a planned intended-consumer receipt. Otherwise the default is
`donor_only` or `defer`. Implementation tactics in the tables below do not by
themselves place a capability on the critical path.

## Evidence snapshot

| Repository | Inspected revision | Role in this census |
| --- | --- | --- |
| `mixed_methods_workbench` | `e36de3bcdbab021149a78631cc8ade72e1824261` | Product/integration authority, current NYC example, and adopted capability architecture. |
| `project-meta` | `origin/main@e2a2153a69c307c96f35b17e581a668cd2800c42` | Current ecosystem routing, shared architecture, CSS registration, and governed-graph adoption evidence. |
| `data-contracts` | `origin/master@33746efd75b309aeb2850666859e7b7102190385` | Current default-branch typed contract owner; the composition evidence below also cites exact consumer pins. |
| `llm_client` | `be189820d1412ec4d19ba148ed1cbdf79c387b3d` | Structured model execution and observability. |
| `open_web_retrieval` | `531a0937258320cccbaac0e868a7f05f399e2de7` | Search/fetch/extract transport and receipts. |
| `qualitative_coding` | `4ea0ce6ca15a63ba91b1a3790e4737b411389902` | Qualitative and grounded-theory protocol owner. |
| `process_tracing` | `8bada47d371303a0d66dab3aad96addc8f4fb47e` | Process Tracing protocol owner. |
| `grounded-research` | `0b46fc144b50360c6912e8ba0e2dfe15704f1d18` | Independent analysis and adjudication owner. |
| `theory-forge` | `9ec293f96b05a56115cfa4c1686ab7032fd79411` | Theory compile/application owner. |
| `onto-canon6` | `a271d37e07f827281070577eeb71c23589ecd4d0` | Governed assertion and semantic-projection owner. |
| `Digimon_for_KG_application` | `96a838ff8d9fd9c8bb40e6e23699974681c9be0c` | Graph/retrieval owner and adopted Data Contracts consumer. |
| `computational-social-science` | remote `main@33526009e13b8b93b6adcd52fef7408cf99ab7dc` | Study/application contracts, deterministic findings, reviewer decisions, and relational/graph composition. |
| `sb_ontologies` | `ec1aea3f199b4ca19615679c5428c9e603349129` | Donor/idea source only; not registered as a current platform authority. |

Project Graph now assigns Data Contracts, `llm_client`, Open Web Retrieval, and
Computational Social Science to canonical `code-active` workspace slugs. Its
legacy `path` fields for the first three still name older locations, so agents
must resolve through `workspace_home` and `workspace_slug`. Computational
Social Science is registered as a governed active repository, but no local
checkout currently exists at either registered or legacy location; this census
therefore inspected its private GitHub remote at the exact revision above. The
repository is real and executable even though the broader Computational Social
Science program remains tentative and its recurrence, manual-baseline, value,
and complementary-method gates are open.

Reverify revisions and Project Graph routing before implementation.

## Repository-level dispositions

| Owner | What exists now | Seam/adoption truth | Selection disposition | Implementation tactic if selected |
| --- | --- | --- | --- | --- |
| Data Contracts | Strict producer/permissive consumer models; action descriptors and packs; typed inputs, outputs, resources, effects, and determinism; pure compilation; invocation and transition guards. | Stable typed substrate. DIGIMON genuinely consumes compiled manifests and guarded transitions. It intentionally does not load or dispatch implementations. | `adopt_now` | `reuse` composition grammar; `extend` only after two authentic consumers prove a missing neutral field. |
| `llm_client` | Arbitrary Pydantic structured output, prompt/model/route/budget identity, retries and disclosed fallbacks, traces, cost, and observed runs. | Stable shared runtime used by multiple repos. | `adopt_now` | `reuse`; it owns model-backed transform-step execution, not caller-owned instructions, schemas, validation, anchoring, method meaning, or evidence decisions. |
| Open Web Retrieval | Typed search, fetch, and extraction with source metadata, hashes, strict/partial modes, and tool receipts. | Shared retrieval implementation exists. Workbench still needs an adapter and must own query intent/admission policy. | `adapt_later` — activate when a selected workflow needs new source acquisition. | `wrap`; do not reimplement web transport. |
| Mixed Methods Workbench | Investigation Spine, UI/API, frozen NYC sources, authentic structured extraction trace, exact evidence bindings, deterministic quantitative audit, review gate, and bounded simulation appraisal. | Authentic examples exist, but current NYC extraction calls `llm_client` directly, returns a local receipt, hard-codes case semantics, and has no Data Contracts dependency. | `adopt_now` | `extend` as orchestrator; refactor one existing path through shared actions before adding another vertical. |
| Qualitative Coding | Generic internal structured extraction, pipeline stages, coding and grounded-theory state, constant comparison, anchors, review, memos, reflexivity, and strict project artifacts. | Strong method implementation; recurring execution-step patterns are internal rather than a neutral cross-repo ABI. | `adopt_now` for one exact incompatible method-profile proof. | `keep_method_owned`; `wrap` selected public operations and receipts. |
| Process Tracing | Generic internal LLM passes, deterministic Bayesian calculations, rival/partition/evidence/mechanism protocols, refinement transitions, source acquisition, and strict exports. | Strong method implementation and exports; no generic QC/PT operation ABI. | `adopt_now` for the second incompatible method-profile proof. | `keep_method_owned`; `wrap` selected public operations and receipts. |
| Theory Forge | Theory-schema compilation and theory-specific application machinery. | Useful strict method seam and deterministic CPT/Choices13k counterexample; general provenance-complete application-run export remains incomplete. | `donor_only` | Preserve method ownership and use relevant conformance patterns; no current dependency. |
| Grounded Research | Typed local `EvidenceBundle`, independent analysis, dispute/verification state, and adjudication. | Current outbound shared export writes plain JSONL dictionaries, while OntoCanon accepts typed `ClaimRecord`; the integration test constructs records directly. End-to-end adoption is not proven. | `defer` | `keep_method_owned`; reconsider a wrapper only after a real typed producer-consumer seam is observed. |
| OntoCanon | Ontology packs, candidate assertions, exact passages, validation/review/promotion, stable identity, Foundation IR 1.3, governed corpus compilation, and deterministic rule-owned semantic projection. | Strong producer boundary. Project Meta Plan 241 records an adopted two-domain public compile/query path into DIGIMON with typed insufficiency and exact support reopening. | `defer` — activate only for a named governed-assertion or semantic-projection need. | Conditional `reuse`; never the generic arbitrary-output primitive or mandatory MVP path. |
| DIGIMON | Graph materialization, typed graph/text/vector/structured-source actions, catalog compilation, guarded execution/commit, traversal, ranking, retrieval, and governed-model analysis. | Strongest current proof that Data Contracts can support a real composition runtime. Plan 241 proves two-domain OntoCanon/DIGIMON adoption; CSS separately consumes real DIGIMON graph analysis. Fully situational adaptive action-DAG value remains unproven, and a narrower direct-projection operator certification may remain open. | `defer` — activate only for a named graph/retrieval need. | Conditional `reuse` of its supported public boundaries; never its whole runtime as the Workbench. |
| Computational Social Science | Study questions/manifests, permissive producer readers, exact input cohorts, deterministic tables/findings, relational analysis, graph-projection composition, and reviewer decisions. | F1 authentically consumes reviewed QC/theory inputs into a 16-cell table, two cited licensed sentences, and an OCR custody non-result. A separate both-sign vertical composes Data Contracts and real DIGIMON analysis back to exact source rows. Recurrence, manual baseline, value, and fitness for the selected MVP remain open. | `donor_only` | Borrow exact-cohort, deterministic-derivation, reverse-binding, non-result, and scientific-review patterns. Take no CSS dependency unless a later named need passes the adoption gate. |
| SB Ontologies | Earlier ontology/theory experimentation. | Direct provider calls, loose dictionaries, and reported fidelity gaps; not a registered current owner. Theory Forge and OntoCanon have stronger relevant seams. | `donor_only` | Mine ideas only; no implementation dependency. |

## Capability-level adoption map

| ID | Capability | Current owner and evidence | Current maturity | Selection disposition | Implementation tactic and MVP use |
| --- | --- | --- | --- | --- | --- |
| CAP-01 | Declare typed composable actions | Data Contracts action descriptors/packs and compiler. | `adopted_consumer` through DIGIMON. | `adopt_now` | `reuse` unchanged. |
| CAP-02 | Resolve applicability and guard invocation/transition | Data Contracts compiler and transition guards. | `adopted_consumer` through DIGIMON structured-source execution. | `adopt_now` | `reuse`; Workbench supplies its state and adapter resolver. |
| CAP-03 | Execute structured LLM transformations | `llm_client`; QC/PT/TF and Workbench use structured outputs. | `observed_runtime`. | `adopt_now` | `reuse` `llm_client` for the `model` backend. Record operation role (normally `transform`), semantic/programmatic/mixed correctness boundary, backend, and programmatic validation separately. Human or program-backed steps are different bindings, not `llm_client` modes. No Workbench model client. |
| CAP-04 | Search, fetch, and capture web sources | Open Web Retrieval. Grounded Research constructs its client and executes typed `SearchQuery` requests through a compatibility shim. | `adopted_consumer`; authentic runtime status remains separately bounded. | `adapt_later` — when the selected workflow needs new acquisition. | `wrap`; retain version-skew compatibility as visible debt, and keep evidence admission method/study-owned. |
| CAP-05 | Extract structured candidates against an arbitrary typed contract | Machinery exists in `llm_client` and internal QC/PT handlers; Workbench NYC proves a case-specific use. | `implemented_internal`; no adopted research-facing cross-repo action. | `adopt_now` | `extend` through a Workbench-owned research action pack that uses Data Contracts grammar and a Workbench adapter; first consumer is refactored NYC. Promote only proven neutral fields into Data Contracts after the two-consumer gate. |
| CAP-06 | Freeze source versions and identify exact units | Open Web Retrieval, QC, OntoCanon, and Workbench each implement parts. | Fragmented `implemented_internal`/local seams. | `adopt_now` | `wrap` existing custody; design only the smallest common reference required by authentic consumers. |
| CAP-07 | Bind candidate fields to exact evidence | QC, OntoCanon, and Workbench have anchor models and checks. | Authentic local evidence; no shared adopted contract. | `adopt_now` | Start Workbench-local over Data Contracts extension points; promote only after two compatible consumers. |
| CAP-08 | Validate structural output | Pydantic and owner-local validators. | `observed_runtime`. | `adopt_now` | `reuse`; keep separate from methodological validation. |
| CAP-09 | Validate methodological admissibility | QC/PT/TF/domain engines. | Strong owner-local behavior. | `adopt_now` | `keep_method_owned`; expose typed findings/receipts. |
| CAP-10 | Review, adjudicate, and promote candidates | OntoCanon, QC, PT, and Grounded Research have distinct implementations. | Strong owner-local behavior; no universal decision policy. | `adopt_now` | Share only neutral frozen-target/authority/recommendation envelopes after compatible seams; keep review rules and effective dispositions local. |
| CAP-11 | Apply lineage-preserving state transitions | Data Contracts supplies proposed-transition guards; PT has explicit immutable refinement application; QC has project-state updates. | Substrate adopted; method transitions owner-local. | `adopt_now` | `reuse` neutral guards and `wrap` method transitions. |
| CAP-12 | Iterate and control method protocols | QC pipeline and PT pipeline have explicit state/order/gates; DIGIMON has typed retrieval composition. | `implemented_internal` in multiple domains. | `adopt_now` for bounded profile execution, not a universal planner. | Standardize policy-bound receipts and applicability first. |
| CAP-13 | Qualitative coding and category development | Qualitative Coding. | Strong method implementation. | `adopt_now` | `keep_method_owned`; invoke through adapter. |
| CAP-14 | Grounded-theory development | Qualitative Coding. | Strong partial/full protocol machinery with method-specific adequacy limits. | `adopt_now` for the exact selected variant. | `keep_method_owned`; never reduce to one semantic transform. |
| CAP-15 | Rival-explanation Process Tracing | Process Tracing. | Strong method implementation and export. | `adopt_now` for the exact selected variant. | `keep_method_owned`; invoke through adapter. |
| CAP-16 | Theory operationalization and application | Theory Forge. | Bounded stable artifacts; complete general application export gap. | `donor_only` | Preserve method ownership and relevant conformance patterns; no current dependency. |
| CAP-17 | Independent claim adjudication | Grounded Research. | Strong local capability; current shared export mismatch. | `defer` | `keep_method_owned`; reconsider cross-repo adoption when a real typed seam exists. |
| CAP-18 | Governed semantic assertion lifecycle | OntoCanon. | `adopted_consumer` through the Plan 241 public governed-corpus path, with exact producer/review identities retained. | `defer` | Conditional `reuse` when cross-document semantic governance is needed. |
| CAP-19 | Semantic/evidence graph projection | OntoCanon plus DIGIMON. | Plan 241 proves a public two-domain compile/query/evidence round trip with exact support reopening. A narrower older direct `SemanticGraphProjectionV1` operator path may retain its own certification gap. | `defer` | Conditional `reuse` only when the question requires graph/semantic analysis; require method-artifact reverse binding in addition to source reopening. |
| CAP-20 | Graph/text/vector/structured retrieval | DIGIMON. | Substantial implementation, Plan 241 two-domain adoption, and a real CSS graph-analysis consumer; adaptive superiority remains unproven. | `defer` | Conditional `reuse` only for a named retrieval/analysis need; direct text/search may be sufficient. |
| CAP-21 | Deterministic descriptive measurement | Workbench NYC audit, Computational Social Science F1, and established method/statistical libraries. | Authentic bounded examples exist; CSS owns study-specific source-to-table/finding derivation, not a general inference engine. | `adopt_now` for the named Workbench quantitative artifact; CSS remains `donor_only`. | Use the cheapest authoritative implementation after the measure is named; reconsider CSS only if a concrete study need passes the adoption gate. |
| CAP-22 | Statistical, predictive, or causal analysis | Established engines and future adapters; owner unresolved for portfolio. | Mixed; not censused as one stable seam. | `adapt_later` — when the accepted study design names an estimand/model. | `keep_method_owned`/`missing`; decide per study design, never create one generic inference engine. |
| CAP-23 | Simulation and scenario comparison | External simulation owners; Workbench has a bounded Cybernetic Influence projection. | Bounded authentic projection, not a canonical general seam. | `defer` | `keep_method_owned`; adapter only when required. |
| CAP-24 | Policy-option appraisal | Workbench plus explicit human/value authority; Mist Trail content is manually performed. | Product projection exists; no executing general appraisal engine. | `adopt_now` for the bounded policy MVP. | `extend` from a real decision case; do not treat typed artifacts as computed analysis. |
| CAP-25 | Joint display and mixed-methods meta-inference | Workbench. | `missing` authentically. | `adopt_now` for the cohesive mixed-methods MVP. | `extend` after qualitative and quantitative artifacts are accepted. |
| CAP-26 | Investigation continuity and orchestration | Workbench Investigation Spine. | Authentic bounded UI/API; limited action runtime. | `adopt_now` | `extend` over Data Contracts; retain one investigation state without absorbing method state. |
| CAP-27 | Reproducible investigation bundle | Workbench and method-native exports have pieces. | Partial local evidence. | `adopt_now` for MVP export. | `extend` after action/artifact/derivation identities stabilize. |
| CAP-28 | Methodology recommendation | No adopted owner. | `missing`. | `defer` | Future planner compiles accepted designs after lower layers work; never choose by schema match. |
| CAP-29 | Study-level application composition and scientific review | Computational Social Science is one observed implementation; Workbench or another study owner may supply the selected seam. | `observed_runtime` in CSS: F1 exact cohort -> 16-cell table -> cited finding/non-result -> named scientific license; recurrence/manual baseline/value remain open. | `adopt_now` as a capability; CSS remains `donor_only`. | Select the cheapest reviewed artifact that proves the Workbench boundary; any external integration requires its own fresh `adopt_now` disposition. |

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

Project Meta Plan 241 is complete and records one public OntoCanon
`compile_corpus` -> DIGIMON `ask_governed_model` product path over both nanoGPT
and DoDAF. It includes typed insufficiency and cited answers that reopen exact
assertions and source passages. This is an adopted platform round trip, not a
future hypothesis.

A narrower older direct `SemanticGraphProjectionV1` operator path and its SP-03
certification may remain incomplete. That local gate must not be broadened into
a claim that the overall OntoCanon/DIGIMON product boundary lacks an authentic
consumer. For method use, an additional binding is still required from the
semantic assertion/projection back to the authoritative method artifact and
its method-review decision.

### Repository routing

Project Graph's `workspace_home`/`workspace_slug` routing now names the current
canonical workspaces for Data Contracts, `llm_client`, Open Web Retrieval, and
Computational Social Science. Some legacy `path` fields still lag, and the
registered CSS local checkout is absent. This does not invalidate exact remote
evidence, but Project Meta still owns path-field cleanup and checkout
realization.

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
  and `src/onto_canon6/adapters/semantic_graph_projection.py:1`;
- Project Meta Plan 241 and
  `docs/runs/plan241_gpa06_two_domain_adoption.md` for the completed public
  OntoCanon/DIGIMON two-domain round trip;
- DIGIMON Plan 186 for the narrower direct-projection certification boundary;
  and
- Computational Social Science remote `main@33526009e13b8b93b6adcd52fef7408cf99ab7dc`:
  `src/computational_social_science/f1_table.py`, `f1_finding.py`,
  `f1_review.py`, `linked_analysis_composition.py`,
  `linked_analysis_vertical.py`, and
  `integration_tests/test_linked_analysis_vertical.py`.

These are inspection anchors, not permanent line-stable API references. Exact
revisions above control this snapshot.
