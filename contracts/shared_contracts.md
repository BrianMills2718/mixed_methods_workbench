# Shared Contract Sketch

This is a planning contract, not final implementation code. The canonical
domain and versioning decisions are in Plan 003. Producer models
should eventually be Pydantic models with `extra="forbid"`; consumer models
should tolerate compatible future extension with `extra="ignore"`.

## Executable Synthetic Fixture Contract

The first machine-readable contract target lives under
`examples/fixtures/workbench_contract_v1/`.

Files:

- `qc_handoff_stub.json` - synthetic placeholder for the future QC fixture.
- `pt_export_stub.json` - synthetic placeholder for the future PT export.
- `theory_operationalization_stub.json` - synthetic placeholder for the future
  Theory Forge artifact.
- `workbench_synthesis_stub.json` - synthetic integrated payload that exercises
  the shared contract shape.
- `manifest.json` - file hashes, evidence grade, claim limits, and replacement
  gates.

Validation:

```bash
make validate-fixtures
```

The validator enforces structural traceability, artifact hashes, synthetic
status, evidence grades, claim limits, and a shared forbidden-field list for
method-boundary mistakes such as generic confidence, posterior probability of
truth, likelihood vectors in the QC fixture, or unversioned support fields.
Negative controls live in `scripts/check_fixture_negative_controls.py` and run
as part of `make check`.

Evidence grade: `C-synthetic-contract-only`. These fixtures license only the
claim that the workbench has an executable target seam. They do not license any
claim about real engine readiness, research quality, methodological validity, or
mixed-methods synthesis quality.

Coverage report:

```bash
make coverage
```

This writes `docs/coverage_report.md` and `docs/coverage_report.json`.

## Core Types

### ResearchQuestion

Represents the focal question and the method context.

Fields:

- `id`: stable workbench identifier.
- `text`: research question.
- `method_context`: one of `qualitative_coding`, `grounded_theory`,
  `process_tracing`, `multi_method_qualitative_review`,
  `mixed_methods_synthesis`, `cross_case_causal`. The mixed-methods value
  requires an intentional qualitative-quantitative integration design.
- `outcome_or_phenomenon`: bounded outcome, phenomenon, or case focus.
- `scope_id`: links to `SourceScope`.
- `estimand_kind`: one of `descriptive_pattern`, `interpretive_claim`,
  `comparative_explanatory_support`, `population_causal_effect`,
  `generative_theory_model`, `not_applicable`.

### SourceScope

Normalizes `qualitative_coding.CorpusScope` and
`process_tracing.SourcePacket`/source-coverage metadata.

Fields:

- `id`
- `case_or_corpus_name`
- `population_or_case_universe`
- `source_selection_rule`
- `included_source_classes`
- `excluded_source_classes`
- `known_gaps`
- `gap_dispositions`
- `claim_limits`
- `source_hashes`

### SourceAnchor

A source-span reference shared across engines.

Fields:

- `id`
- `source_engine`: `qualitative_coding`, `process_tracing`, or `theory_forge`
- `source_artifact_path`
- `doc_id`
- `start_char`
- `end_char`
- `quote_text`
- `quote_hash`
- `segment_id`
- `source_marker`
- `anchor_resolution_status`: explicit state such as `exact_offset`,
  `source_marker_only`, or `unresolved`; never a generic confidence score.

### EvidenceRecord

Workbench-level evidence item. It may originate as a QC code application,
QC claim anchor, PT evidence item, PT absence finding, or future external
artifact.

Fields:

- `id`
- `source_anchor_ids`
- `description`
- `evidence_kind`: `coded_passage`, `claim_support`, `claim_contrary`,
  `process_trace_evidence`, `absence_finding`, `source_gap`, `quant_indicator`
- `semantic_tags`
- `code_ids`
- `entity_ids`
- `claim_ids`
- `hypothesis_ids`
- `provenance`
- `limitations`

### AnalyticAssertion

Shared empirical/analytic assertion type for claims, hypotheses, and findings.
Theory constructs and mechanisms remain in `TheoryOperationalizationArtifact`
and link to assertions through explicit `guides`, `operationalizes`, or
`challenged_by` relationships.

Fields:

- `id`
- `assertion_kind`: `qualitative_claim`, `theme`, `gt_category`,
  `causal_hypothesis`, `process_tracing_verdict`, `mixed_methods_finding`
- `text`
- `scope_id`
- `supporting_evidence_ids`
- `contrary_evidence_ids`
- `status`: `draft`, `needs_anchor`, `needs_review`, `supported_within_scope`,
  `challenged`, `revised`, `withdrawn`
- `method_payload_ref`

### PatternFinding

Represents co-occurrence, temporal sequence, clustering, or cross-case matrix
findings without pretending they are causal proof.

Fields:

- `id`
- `pattern_kind`: `co_occurrence`, `temporal_sequence`, `case_contrast`,
  `network_relation`, `latent_cluster`, `matrix_association`
- `variables`
- `cases_or_documents`
- `summary`
- `strength_description`
- `source_evidence_ids`
- `causal_interpretation_status`: `descriptive_only`,
  `candidate_explanation_generated`, `tested_by_process_tracing`,
  `eligible_for_cross_case_model`

### CausalHypothesisSet

Workbench bridge into process tracing or future causal engines.

Fields:

- `id`
- `research_question_id`
- `hypotheses`
- `residual_hypothesis_id`
- `observable_predictions`
- `source_scope_id`
- `partition_caveats`
- `origin_pattern_ids`
- `origin_claim_ids`

### WorkbenchSynthesis

Final review/report payload for one workbench run.

Fields:

- `id`
- `research_question_id`
- `source_scope_id`
- `evidence_records`
- `analytic_assertions`
- `pattern_findings`
- `causal_hypothesis_sets`
- `theory_operationalizations`
- `theory_links`
- `method_outputs`
- `review_state`
- `export_manifest`
- `claim_limits`

### TheoryOperationalizationArtifact

Future workbench-safe view of a `theory-forge` theory artifact. This is a broad
stub until a real Theory Forge fixture exists.

Fields:

- `id`
- `schema_version`
- `theory_id`
- `producer_commit`
- `source_schema_ref`
- `compiled_manifest_ref`
- `constructs`
- `mechanisms`
- `hypotheses`
- `observables`
- `measures`
- `assumptions`
- `scope_conditions`
- `uncertainties`
- `validation_obligations`
- `compiled_function_refs`
- `limitations`
- `provenance`

## Adapter Stubs

### QC to Workbench

Input: `qualitative_coding` project state JSON.

Output:

- `SourceScope` from `ProjectState.corpus_scope`.
- `SourceAnchor` from `ClaimAnchor` and anchored `CodeApplication`.
- `EvidenceRecord` from code applications, claim support, contrary anchors,
  and negative-case rows.
- `AnalyticAssertion` from `ProjectState.claims`, codes, core categories,
  synthesis findings, and GT propositions.
- `PatternFinding` from code relationships, entity relationships, cross-case
  memos, and future co-occurrence matrices.

Allowed failures:

- missing source file;
- malformed project state;
- unanchored claim that cannot become source-backed evidence;
- unsupported schema version.

### Process Tracing to Workbench

Input: `process_tracing` `result.json` plus optional source packet.

Output:

- `SourceScope` from source packet and source coverage.
- `SourceAnchor` from evidence `source_text` when offsets or source markers can
  be resolved.
- `EvidenceRecord` from extracted evidence and absence findings.
- `AnalyticAssertion` from hypotheses and synthesis verdicts.
- `CausalHypothesisSet` from hypothesis space and observable predictions.
- method output reference to Bayesian comparative support and sensitivity.

Allowed failures:

- missing result/report pair;
- source hash mismatch;
- no source packet where one is required by the workbench mode;
- unresolved evidence quote that cannot be mapped to a source anchor.

### Theory Forge to Workbench

Input: future `theory-forge` `TheoryOperationalizationArtifact` export.

Output:

- `TheoryOperationalizationArtifact` with constructs, mechanisms, hypotheses,
  observables, measures, assumptions, scope, and validation obligations.
- typed links from theory objects to empirical hypotheses, measures, or claims;
  these links guide or record challenges and never supply empirical support.
- `MethodOutputRef` to schema, compiled manifest, compiled functions, and
  validation artifacts.
- optional links to `CausalHypothesisSet` candidates when the theory artifact
  explicitly defines rival hypotheses or observable implications.

Allowed failures:

- missing schema or manifest provenance;
- stale or non-green compiled artifact;
- ambiguous v14/v15 schema version;
- theory artifact presented as empirical evidence rather than
  operationalization context;
- dependency on AC runtime or untracked compiled output.
