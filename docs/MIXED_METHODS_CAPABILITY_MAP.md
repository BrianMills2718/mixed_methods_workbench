# Text-Centered Mixed-Methods Capability Map

Status: canonical future scope inventory; documentation only
Updated: 2026-08-13

This map records eventual coverage and planning gaps. It does not activate or
authorize implementation; see `docs/PLANNING_STATUS.md`.

## Purpose

This map defines the breadth of the north star without pretending the breadth is
implemented. It is both a completeness checklist and a guard against category
errors: different methods require different workflows, evidence, uncertainty,
and quality criteria.

The first code-derived capability evidence is frozen under
[`docs/research/method_decomposition/codex_phase0/`](research/method_decomposition/codex_phase0/README.md).
The independent candidate and the meaning-level reconciliation are recorded in
[`docs/research/method_decomposition/claude_phase0/`](research/method_decomposition/claude_phase0/reality_check.md)
and
[`docs/research/method_decomposition/comparison_v0.md`](research/method_decomposition/comparison_v0.md).
They describe inspected implementations and method obligations; they do not
replace this future-scope map or adopt a universal capability schema.

Status grades describe workbench-level evidence:

- **A**: source-backed implementation plus tests and observed validation;
- **B**: observed live behavior without durable test coverage;
- **C**: fixture-backed or schema-shaped only;
- **D**: documented/planned only;
- **F**: absent, wrong, or missing a necessary owner.

Upstream engine maturity is noted separately and does not automatically raise a
workbench grade.

## Reconciled Phase 0 Evidence Crosswalk

This crosswalk locates the reconciled Phase 0 findings in the future inventory
without turning either candidate's steps into canonical capabilities. It does
not change the grades below: the decompositions provide bounded evidence about
inspected implementations, while the grades describe workbench-level evidence.

| Inspected workflow | Inventory families informed | Observed evidence | Limit retained by this map |
|---|---|---|---|
| Fixed-corpus grounded theory in `qualitative_coding` | Qualitative analysis; review and reflexivity; causal handoff boundaries | Constant comparison, proposal/revision checkpoints, negative-case appraisal, and typed QC/PT handoffs have executable support; method-meaningful coding and memo operations are coarser in software than in the independent decomposition. | Theoretical sampling remains incomplete, and executable control flow is not evidence of grounded-theory fidelity or saturation validity. |
| Process Tracing rival-explanation core | Causal and comparative inference; source governance; review and refusal | Rival construction, partition repair, likelihood appraisal/audit, absence handling, deterministic comparative updating, mechanism graphs, critic/refinement loops, and calibrated refusal are represented in the observed control flow. | These are PT-owned inference operations. Van Evera labels are computed but do not drive the numeric discrimination grade; no generic diagnostic or confidence capability follows. |
| Process Tracing source acquisition | Source governance; corpus construction; iterative feedback | The scoped interactive path preserves an acquisition agenda, external retrieval, human review, provenance, duplicate handling, and hash-bound admission. A separate bulk/comparative path automates pair review. | The two paths are different variants, not interchangeable evidence. The exact held-out return from newly admitted evidence to frozen rivals remains an evidence mismatch. |
| Theory Forge compile/apply | Theory construction and operationalization; evaluation; reproducible execution | Extraction, structural validation, compilation, repair, review, staged execution, and reporting mechanics are visible in the inspected implementation. | No authoritative methodology source establishes “compile a theory into code.” Authentic compiled execution and fleet-wide runtime-green status remain unresolved evidence, so representation must not be promoted to executed-theory capability. |
| Theory Forge CPT/Choices13k | Quantitative/computational analysis; theory application; evaluation | Dataset pinning, eligibility, CPT transformations, expected-value baseline, row-level prediction, aggregation, and reporting are deterministic and executable in the inspected workflow. | One theory-specific benchmark is not a generic quantitative-text strand, fitting loop, or empirical validation of Theory Forge as a whole. |
| Mist Trail policy appraisal | Research design; human/agent governance; reporting and projection | Typed, validated, hash-bound option, consequence, criterion, priority-lens, recommendation, API, and UI artifacts are present. | The analytic judgments are manually performed and the pipeline makes no model call. Artifact quality and projection must remain separate from analytic execution. |

Across these workflows, the credible reuse hypothesis is a small shell for
identity, custody, typed boundaries, validation, review state, lineage,
refusal, and projection. Coding judgments, causal diagnostics, theory
compilation, prediction mathematics, policy valuation, and required workflow
topology remain method-owned. A shared capability still requires two authentic
compatible producer/consumer seams before infrastructure adoption.

## Capability Families

### 1. Research Design and Epistemic Frame

| Capability | Why it belongs | Likely owner | Current grade | Target version |
|---|---|---|---:|---|
| Study protocol and research-question registry | Methods cannot be selected or judged without the purpose, units, cases, population, time, and intended inference. | Workbench | D | 0.1 |
| Qualitative, multi-method qualitative, and mixed-methods distinction | Prevents false product and inference claims. | Workbench method profiles | D | 0.0 |
| Convergent, explanatory sequential, exploratory sequential, embedded, multiphase, transformative designs | Defines timing, priority, dependency, and integration points. | Workbench | D | 0.4–0.5 |
| Philosophical/epistemic stance and reflexive assumptions | Interpretivist, critical, realist, pragmatic, and post-positivist designs do not share one validity regime. | Workbench + researcher | F | 0.4 |
| Sampling, case selection, linkage, and strand timing | Determines what can be generalized or integrated. | Workbench + engines | F | 0.4–0.6 |
| Protocol/preregistration and deviations | Separates planned analysis from adaptive discovery. | Workbench | F | 0.5 |

### 2. Data Governance, Corpus Construction, and Source Identity

| Capability | Required scope | Likely owner | Current grade | Target version |
|---|---|---|---:|---|
| Ingestion | Interviews, focus groups, open-ended surveys, documents, archives, web/social text, OCR, transcripts, structured metadata. | QC plus source adapters | D workbench; upstream partial/implemented | 0.1–0.7 |
| Corpus provenance and denominator | Inclusion/exclusion, deduplication, missingness, coverage, version, source identity. | QC + workbench registry | D | 0.1 |
| Consent, IRB/ethics, licensing, and permitted use | Research legality and participant obligations cannot be inferred after analysis. | Workbench governance | F | 0.7, metadata starts 0.1 |
| PII/de-identification and sensitive-source policy | Needed before fixtures, collaboration, model calls, or publication. | Source sanitizer + workbench | D | 0.1 |
| Access, residency, retention, deletion, and audit | Real teams require governed data operations. | Workbench platform | F | 0.7 |
| Multilingual text and translation provenance | Translation is an analytic transformation, not clerical preprocessing. | Adapter/profile layer | F | 0.7 |
| Audio/image/OCR traceability | Text derived from media must retain time/page/region anchors and transformation history. | Source adapters | F | 0.7+ |

### 3. Qualitative Analysis Traditions

The workbench must use versioned method profiles. A profile declares valid
objects, workflow obligations, quality criteria, forbidden claims, and reporting
requirements. For example, intercoder agreement can be relevant to structured
codebook analysis but is not a universal validity test for reflexive thematic
analysis.

| Method profile | Essential workflow | Current grade | Target |
|---|---|---:|---|
| Codebook thematic/content analysis | Codebook, exhaustive or declared partial denominator, coding, reconciliation, claims, negative cases. | D workbench; upstream strong | 0.1 |
| Reflexive thematic analysis | Researcher subjectivity, recursive theme development, reflexive memos; no mechanical consensus requirement. | F | 0.7 |
| Grounded theory | Constant comparison, theoretical coding, memoing, theoretical sampling, category development, negative cases, and an adequacy/saturation argument. This is not the `grounded-research` adjudication project. | Owner unresolved; D planning evidence | 0.1 demo, 0.4 validation |
| Framework analysis | Matrix indexed by cases and analytic categories with within/cross-case review. | F | 0.5–0.7 |
| Narrative analysis | Plot, temporality, voice, positioning, and case-level coherence. | F | 0.7+ |
| Discourse/critical discourse analysis | Language, power, ideology, intertextuality, and contextual interpretation. | F | 0.7+ |
| Conversation analysis | Turn-taking, sequence, repair, transcription detail, and interactional context. | F | 0.7+ |
| Phenomenology/IPA | Lived experience, idiography, interpretive engagement, and case depth. | F | 0.7+ |
| Ethnography | Field context, observation, positionality, thick description, and prolonged engagement. | F | 0.7+ |
| Case/document analysis | Source criticism, within-case context, comparison, and documentary silences. | D | 0.1–0.7 |
| Qualitative evidence synthesis | Search/screening, appraisal, extraction, translation, synthesis, confidence. | F | 0.7+ |

The `qualitative_coding` engine is the near-term qualitative substrate, but it
still needs observed grounded-theory fidelity evidence, expert labels, populated
theoretical-sampling runs, and a workbench-safe export.

### 4. Quantitative and Computational Text Analysis

| Capability | Minimum validity obligation | Owner | Current grade | Target |
|---|---|---|---:|---|
| Descriptive counts and case/code matrices | Declared denominator, missingness, weighting, and uncertainty where sampled. | Decision pending; recommended narrow workbench adapter | F | 0.5 |
| Dictionary/lexicon measurement | Construct validity, context/polysemy checks, language/domain transfer. | Decision pending; recommended narrow workbench adapter | F | 0.5 |
| Supervised classification/annotation | Label protocol, grouped train/held-out split, class balance, error analysis, calibration, measurement error. | Decision pending; recommended narrow workbench adapter | F | 0.5 |
| Embeddings, clustering, and topic models | Stability, sensitivity, interpretability, held-out/generalization checks; no topic-as-truth shortcut. | Unresolved adapter | F | 0.5–0.7 |
| Semantic scaling/positioning | Construct anchors, identification, uncertainty, robustness. | Unresolved adapter | F | 0.6+ |
| Event, sequence, temporal, network, and relational text analysis | Extraction validity, temporal/source uncertainty, dependence, coverage. | PT/shared adapters | F workbench | 0.6 |
| Multilingual computational text | Cross-language measurement invariance and translation/model effects. | Unresolved adapter | F | 0.7+ |

Strategic decision: do not create a generic quantitative-text engine in advance.
For 0.5, the current decision brief recommends measuring the prevalence or
ordered distribution of one observable, case-supported QC category through
established libraries behind a narrow workbench adapter. It requires a
dictionary/count and regularized supervised comparison and treats
topic/embedding output as discovery rather than the first measure. Extract
shared infrastructure only after a second slice demonstrates a stable boundary.
Brian must still approve the task/owner pattern and later the exact construct;
the owner remains a formal F-grade gap until then. See
`docs/decisions/2026-07-12-first-quantitative-text-strand.md`.

### 5. Causal and Comparative Inference

| Capability | Distinct inference | Owner | Current grade | Target |
|---|---|---|---:|---|
| Within-case process tracing | Comparative support for rival explanations under a bounded source packet. | `process_tracing` | D workbench; upstream substantial | 0.1 |
| Absence/negative evidence and source coverage | Whether missing observations are diagnostic depends on observability and source design. | `process_tracing` | D | 0.1–0.6 |
| Nested analysis and case selection | Cross-case result selects or is explained by within-case evidence. | Workbench + PT + quant adapter | F | 0.6 |
| QCA/fsQCA | Set calibration, necessity/sufficiency, limited diversity, contradictory configurations. | Future adapter | F | 0.6+ |
| Causal inference with text | Text as treatment, mediator, confounder, or outcome with identification assumptions. | Future adapter | F | 0.6+ |
| Experimental/survey/regression/Bayesian models | Population/sample estimands, assignment/selection, model assumptions, uncertainty. | Established engines via adapters | F | 0.6+ |
| Within-to-cross-case bridge | Prevents PT support from becoming an effect estimate or vice versa. | Workbench integration policy | D | 0.6 |

`process_tracing` still needs a stable export, a clean deterministic check
surface, stronger source-design/partition/production-provenance guards, and a
formal validation benchmark. These are engine obligations behind a stable seam,
not reasons to duplicate PT logic in the workbench.

### 6. Theory Construction, Operationalization, and Revision

| Capability | Required distinction | Owner | Current grade | Target |
|---|---|---|---:|---|
| Theory candidate discovery and recommendation | Search a governed library and academic sources; use LLM knowledge only for candidate/query leads; retain citations, inclusion/rejection rationale, and human approval. | Workbench + research services + researcher | F | 0.3 |
| Theory extraction/representation | What a selected source theory claims, with provenance. | Theory Forge | D workbench | 0.3 |
| Constructs, mechanisms, hypotheses, observables, measures | Formal schema plus operationalization context and test obligations. | Theory Forge | D | 0.3 |
| Scope conditions and assumptions | Bounds where a theory may apply. | Theory Forge + researcher | D | 0.3 |
| Empirical linkage | Evidence challenges/supports a prediction under a method; theory is not evidence. | Workbench | F | 0.3 |
| Theory building and revision | Patterns, negative cases, rival mechanisms, and failed predictions alter the theory graph transparently. | Workbench + QC/PT/TF | F | 0.3–0.6 |
| Compiled theory-specific pipeline | Schema-derived extraction, deterministic transformations, orchestration, qualitative stages, mechanisms, uncertainty, and validation. Compilation is not validation. | Theory Forge | D external implementation evidence | 0.3 |
| Executed theory application | Versioned staged run with inputs, anchors, stage outputs/errors, model/prompt/schema/manifest versions, uncertainty, and claim limits. | Theory Forge producer export + workbench consumer | F; stable export absent | 0.3 |

### 7. Mixed-Methods Integration

This family is the product's core differentiator and its largest current gap.

| Capability | Meaning | Current grade | Target |
|---|---|---:|---|
| Connecting | One strand's results determine sampling or cases for another. | F | 0.5–0.6 |
| Building | One strand creates an instrument, variables, prompts, or hypotheses for another. | F | 0.5 |
| Merging | Independently analyzed strands are compared or combined. | F | 0.5–0.6 |
| Embedding | A secondary strand answers a bounded question inside a primary design. | F | 0.5 |
| Quantitizing/qualitizing | Transformations preserve assumptions, provenance, and information loss. | F | 0.5–0.6 |
| Joint displays | Cases/categories/estimates/evidence align in an inspectable analytic display. | F | 0.5 |
| Convergence, complementarity, divergence, silence | Strand relationships are classified rather than averaged away. | F | 0.5 |
| Meta-inference | Integrated conclusion states evidence, logic, scope, uncertainty, and unresolved contradictions. | F | 0.5 |
| Integration fit/legitimation | Review whether the integration design and inference are warranted. | F | 0.5–0.9 |
| Iterative feedback | Later results can revise sampling, coding, measurement, source design, or theory. | F | 0.5–2.x |

### 8. Review, Reflexivity, and Human/Agent Governance

| Capability | Required behavior | Current grade | Target |
|---|---|---:|---|
| Roles and authority | Record who may propose, accept, revise, withdraw, or publish. | F | 0.2 |
| Analytic and reflexive memos | Capture interpretive decisions, positionality, model influence, and changes over time. | D upstream | 0.2–0.7 |
| Disagreement/adjudication | Preserve competing analyses, verify disputed claims, and record human disposition. | D; Grounded Research implemented | 0.2 |
| Human review queues | Prioritize by risk, ambiguity, novelty, contradiction, and sampling value. | D upstream | 0.2–0.5 |
| Model/prompt/version provenance | Every generated transformation is attributable and rerunnable. | D | 0.1 |
| Nonstationarity/drift | Re-evaluate outputs after model, prompt, corpus, or method-profile changes. | F | 0.8 |
| Agent API parity | Every researcher-visible operation has an inspectable programmatic interface. | D | all versions |

### 9. Evaluation, Reporting, and Interoperability

| Capability | Minimum surface | Current grade | Target |
|---|---|---:|---|
| Software verification | Unit/schema/integration checks, real seams, failure observability. | C/F scaffold | 0.0 onward |
| Methodological evaluation | Method-specific rubrics, experts, held-out cases, planted failures, sensitivity. | F workbench | 0.1 onward |
| Trace evaluation | Evaluate recorded stages and context, not only final prose. | F | 0.1 onward |
| Reporting profiles | JARS mixed/qual, COREQ, SRQR, MMAT; PRISMA/ENTREQ for synthesis. | F | 0.5–0.7 |
| REFI-QDA exchange | Import/export projects and codebooks without locking users in. | F | 0.5 |
| Reproducible research bundle | Protocol, data manifest, transforms, artifacts, decisions, environment, report. | D | 0.5–1.0 |
| Reviewer/replication packet | Minimal inspectable evidence for a claim or publication. | D | 0.1–0.8 |
| Comparative product benchmark | Quality, fidelity, time, labor, cost, reproducibility, and failure detection. | F | 0.8 |

### 10. Product Workspaces

The eventual product needs these coherent workspaces, each backed by JSON APIs:

1. study and method-design registry;
2. source/corpus governance and provenance;
3. method-specific analysis workspaces;
4. evidence, claim, pattern, hypothesis, theory, and estimate ledger;
5. integration/joint-display studio;
6. disagreement, adjudication, and human review;
7. reporting, interoperability, and reproducible export;
8. run traces, evaluation, cost, and drift monitoring.

The UI should not be built as eight empty shells. Each workspace appears only
when a vertical slice has real fixture and API evidence.

## Architecture Ownership

| Component | Owns | Must not own |
|---|---|---|
| `mixed_methods_workbench` | Study protocols, method profiles, orchestration, consumer adapters, linkage, integration, review, reports, compatibility. | Engine-specific inference or generic LLM/retrieval clients. |
| `qualitative_coding` | Corpus/segment/coding/claim/GT state, method-specific review, strict QC exports. | PT likelihoods, quantitative effects, generic integration policy. |
| `process_tracing` | Rival-hypothesis PT inference, source scope/coverage, absence analysis, strict PT exports. | Qualitative coding or population causal effects. |
| `grounded-research` | Independent analyst/adjudication workflow, claim/dispute ledger, verification results. | Universal truth oracle or generic workbench state. |
| `theory-forge` | Theory extraction, operationalization, validation obligations, optional compiled metadata. | Empirical evidence or causal verdicts. |
| OntoCanon | Governed assertion/ontology-pack lifecycle, identity, provenance, review/promotion, source-bound exports. | QC/PT/GT inference or replacement of native method artifacts. |
| DIGIMON | Graph/index projection, retrieval, ranking, traversal, analytics, evidence navigation. | Method-native inference or authority over source claims. |
| Quantitative text adapter, owner unresolved | First design's measurement/classification/estimate artifacts. | Universal text-method abstraction before real slices. |
| Shared infra | `llm_client`, `open_web_retrieval`, `trace_eval`, `prompt_eval`, narrow `data_contracts`. | Project-specific workflows. |

## Common Domain Vocabulary

The workbench domain model should distinguish at least:

- `StudyProtocol`, `ResearchQuestion`, `MethodProfile`, `MethodStrand`,
  `IntegrationPlan`, `SamplingPlan`;
- `Corpus`, `Source`, `Case`, `Participant`, `SourceAnchor`, `Transformation`;
- `EmpiricalEvidence`, `Code`, `Theme`, `Category`, `AnalyticMemo`, `Claim`,
  `Pattern`;
- `TheorySpecification`, `Construct`, `Mechanism`, `Hypothesis`, `Observable`,
  `Measure`, `ScopeCondition`;
- `ProcessTracingAssessment`, `QuantitativeMeasure`, `Estimate`,
  `IdentificationAssumption`;
- `JointDisplay`, `StrandRelationship`, `MetaInference`;
- `ReviewDecision`, `AdjudicationResult`, `RunTrace`, `ExportPackage`.

These are vocabulary and boundary candidates, not permission to create one
universal schema. Real slices determine which relationships become durable
contracts.

## Beyond-SOTA Thesis

The strongest opportunity is not that an LLM can code text. Bounded annotation
tasks are increasingly commoditized. The defensible frontier is an integrated
epistemic control system that:

- uses programmatic checks for exhaustive coverage and invariant enforcement;
- uses agents for interpretation, competing hypotheses, relevance, ambiguity,
  and contradiction-seeking;
- reserves human direction for research purpose, method choice, values,
  positionality, and consequential adjudication;
- chooses the next source, case, code review, or measurement task by expected
  information value;
- preserves every transformation across methods so a meta-inference can be
  audited and revised.

## External Methodological Anchors

- Mixed-methods design/integration: NIH Best Practices,
  <https://obssr.od.nih.gov/sites/g/files/mnhszr296/files/Best_Practices_for_Mixed_Methods_Research.pdf>.
- Joint displays/meta-inference: <https://pmc.ncbi.nlm.nih.gov/articles/PMC4639381/>,
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC10173938/>.
- Text-as-data validation: <https://unstats.un.org/unsd/trade/events/2014/Beijing/documents/socialmedia/Grimmer%20and%20Stuart%20-%202013.pdf>.
- Causal inference with text: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9581481/>.
- Computational grounded theory: <https://csuned.github.io/resources/nelson-computational-grounded-theory-rotated.pdf>.
- REFI-QDA exchange: <https://www.qdasoftware.org/>.
- Qualitative/mixed reporting: <https://www.equator-network.org/reporting-guidelines/journal-article-reporting-standards-for-qualitative-primary-qualitative-meta-analytic-and-mixed-methods-research-in-psychology-the-apa-publications-and-communications-board-task-force-report/>,
  <https://www.equator-network.org/reporting-guidelines/coreq/>, and
  <https://www.equator-network.org/reporting-guidelines/srqr/>.
- Mixed Methods Appraisal Tool:
  <https://mixedmethodsappraisaltoolpublic.pbworks.com/w/file/fetch/127916259/MMAT_2018_criteria.pdf>.
- Responsible research use of generative AI:
  <https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research?hub=67098>.
- Qualitative data sharing/de-identification:
  <https://wpvip.icpsr.umich.edu/icpsr/wp-content/uploads/sites/11/2025/06/Guide-for-Sharing-Qualitative-Data-at-ICPSR-V2.pdf>.
