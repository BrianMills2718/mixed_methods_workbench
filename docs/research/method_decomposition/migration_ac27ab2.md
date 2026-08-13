# Migration of frozen Codex Phase 0 candidate `ac27ab2` to rev 5.1

Status: `migration_record`; observational evidence preserved, not schema adoption

## Scope and rules

This artifact performs the field-by-field migration required by rev 5.1 §0.1 for all 77 rows in `codex_phase0/steps.yaml`. The source candidate remains frozen; this file does not rewrite it. Every record contains the exact legacy values, a complete rev-5 assignment, and explicit loss notes. `comparison_v0.md` remains the semantic synthesis and is neither replaced nor made canonical by this mechanical migration.

The migration uses the independently frozen sources in `claude_phase0/sources.md` only after both candidates were frozen. It preserves code references as implementation evidence and uses source+edition citations for `analytic` and `methodological_support` assignments. Exact source-code locations remain pinned to the repository revisions recorded by the two candidates; they are historical evidence, not current-HEAD claims.

## Global field crosswalk

| Legacy field | Rev-5 assignment | Treatment |
| --- | --- | --- |
| workflow key | `method_id` | Mapped to the independent candidate's frozen method identifier. |
| `step_id`, `verb`, `label`, `parameters`, `preconditions`, `method_owned_semantics`, `optional`, `repeatable` | same-named field | Preserved exactly. |
| `inputs`, `outputs` mapping | named slot lists | Slot names/types/optional flags preserved; legacy numeric ranges collapse to rev-5 cardinality vocabulary; input/output roles are synthesized. |
| `actor` | `actor_chain` | Ordered chain synthesized conservatively from the compound legacy label. |
| `implementation_status` | `execution_status` + `representation_status` | Assigned case by case from both the callable boundary and the actual performer. Legacy `executable` usually maps to `software_executable`, but a callable human-review boundary maps to `manually_performed`; `represented_manual→manually_performed`, `incomplete→incomplete_software`. Artifact representation is assigned from the cited implemented outputs. |
| `evidence_basis` + `source_refs` | `evidence_basis` + `implementation_ref` | Code/test evidence moves to implementation references; frozen method sources supply methodological evidence. |
| absent | `workflow_role`, `operation_kind`, `conclusion_supported`, `failure_output` | New assignments are marked as migration-derived. Missing failure artifacts remain explicitly unresolved. |
| `internal_method_phases`, `implementation_note` | no direct field | Preserved in `original_values` and called out as unexpressible without loss. |

## Coverage manifest

| Legacy workflow | Rows | Assigned rev-5 method |
| --- | ---: | --- |
| `qc_fixed_corpus_grounded_theory_v3` | 15 | `qc_grounded_theory` |
| `pt_single_case_rival_explanation_v2` | 23 | `pt_core_rival_explanation` |
| `pt_acquisition_companion` | 4 | `pt_source_acquisition` |
| `theory_forge_v14_compile_apply` | 19 | `theory_forge_compile_apply` |
| `theory_forge_cpt_choices13k_prediction` | 6 | `theory_forge_cpt_choices13k` |
| `mist_trail_deliberative_appraisal_mtd1` | 10 | `mist_trail_policy_appraisal` |
| **Total** | **77** | **77 unique legacy step IDs** |

## Row migrations

### `qc_gt.01` — Load and verify project state

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.01
  verb: retrieve
  label: Load and verify project state
  inputs:
    package_root:
      type: configuration
      cardinality: '1'
      optional: false
    public_manifest:
      type: configuration
      cardinality: '1'
      optional: false
    encoded_project_state:
      type: dataset
      cardinality: '1'
      optional: false
  outputs:
    manifest:
      type: configuration
      cardinality: '1'
      optional: false
    project_state:
      type: dataset
      cardinality: '1'
      optional: false
  parameters: &id001
  - state_encoding
  preconditions: &id002
  - manifest validates
  - state path remains inside package
  - digest and ProjectState validation succeed
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - qc_clean/core/public_demo.py:1026-1053
  - scripts/run_public_grounded_theory_full_corpus.py:1053-1059
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.01
  verb: retrieve
  label: Load and verify project state
  workflow_role: acquire
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: package_root
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  - slot: public_manifest
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  - slot: encoded_project_state
    type: dataset
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: manifest
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: project_state
    type: dataset
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `qc_gt.02` — Select ordered source units

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.02
  verb: retrieve
  label: Select ordered source units
  inputs:
    project_state:
      type: dataset
      cardinality: '1'
      optional: false
    document_ids:
      type: source_document
      cardinality: 2..25
      optional: false
  outputs:
    ordered_source_units:
      type: segment
      cardinality: 1..*
      optional: false
    source_units_digest:
      type: artifact_digest
      cardinality: '1'
      optional: false
  parameters: &id001
  - declared_document_order
  - seed_or_expansion_batch
  preconditions: &id002
  - document IDs are unique and present
  - at least one nonblank segment is selected
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - qc_clean/core/grounded_theory_development.py:3117-3151
  - scripts/run_public_grounded_theory_development.py:147-160
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.02
  verb: retrieve
  label: Select ordered source units
  workflow_role: acquire
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: project_state
    type: dataset
    role: subject
    cardinality: one
    optional: false
  - slot: document_ids
    type: source_document
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: ordered_source_units
    type: segment
    role: result
    cardinality: many
    optional: false
  - slot: source_units_digest
    type: artifact_digest
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `qc_gt.03` — Generate initial grounded-theory proposal

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.03
  verb: construct
  label: Generate initial grounded-theory proposal
  inputs:
    ordered_seed_units:
      type: segment
      cardinality: 1..*
      optional: false
    analytic_goal:
      type: claim
      cardinality: 0..1
      optional: true
  outputs:
    incidents:
      type: code
      cardinality: 8..24
      optional: false
    comparisons:
      type: finding
      cardinality: 4..12
      optional: false
    categories:
      type: construct
      cardinality: 3..8
      optional: false
    theoretical_memos:
      type: memo
      cardinality: 2..5
      optional: false
    core_process:
      type: theory
      cardinality: '1'
      optional: false
    category_relationships:
      type: relation
      cardinality: 3..12
      optional: false
    propositions:
      type: proposition
      cardinality: 2..8
      optional: false
  parameters: &id001
  - model
  - reasoning_effort
  - trace_id
  - budget
  - prompt_revision
  - fixed_seed_interviews
  preconditions: &id002
  - source aliases and prompt exist
  - structured model result validates
  method_owned_semantics: &id003
  - incident identification
  - constant comparison
  - category development
  - memo decisions
  - central-process selection
  - relationship formulation
  - proposition formulation
  internal_method_phases:
  - identify_incidents
  - compare_incidents
  - develop_categories
  - write_memos
  - select_core_process
  - formulate_relationships
  - formulate_propositions
  actor: llm_with_deterministic_orchestration
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_development.py:49-108
  - scripts/run_public_grounded_theory_development.py:164-212
  - qc_clean/core/grounded_theory_development.py:68-130
  - qc_clean/core/grounded_theory_development.py:244-296
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.03
  verb: construct
  label: Generate initial grounded-theory proposal
  workflow_role: conceptualize
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: ordered_seed_units
    type: segment
    role: subject
    cardinality: many
    optional: false
  - slot: analytic_goal
    type: claim
    role: context
    cardinality: optional_one
    optional: true
  outputs:
  - slot: incidents
    type: code
    role: result
    cardinality: many
    optional: false
  - slot: comparisons
    type: finding
    role: result
    cardinality: many
    optional: false
  - slot: categories
    type: construct
    role: result
    cardinality: many
    optional: false
  - slot: theoretical_memos
    type: memo
    role: result
    cardinality: many
    optional: false
  - slot: core_process
    type: theory
    role: result
    cardinality: one
    optional: false
  - slot: category_relationships
    type: relation
    role: result
    cardinality: many
    optional: false
  - slot: propositions
    type: proposition
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Generate initial grounded-theory proposal' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
- This executable boundary bundles multiple rev-5 ideal operations; one operation_kind cannot express the mixed internal semantics without splitting the observed boundary. The assignment follows the primary analytic act and is lossy.
```

### `qc_gt.04` — Bind and validate seed proposal

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.04
  verb: anchor
  label: Bind and validate seed proposal
  inputs:
    proposal_draft:
      type: theory
      cardinality: '1'
      optional: false
    source_alias_map:
      type: configuration
      cardinality: '1'
      optional: false
    project_state:
      type: dataset
      cardinality: '1'
      optional: false
    source_state_digest:
      type: artifact_digest
      cardinality: '1'
      optional: false
    source_units_digest:
      type: artifact_digest
      cardinality: '1'
      optional: false
  outputs:
    source_bound_seed_package:
      type: theory
      cardinality: '1'
      optional: false
    resolved_evidence_links:
      type: passage_anchor
      cardinality: 1..*
      optional: false
  parameters: &id001
  - schema_v1
  preconditions: &id002
  - aliases are known
  - array indexes and relation endpoints validate
  - state and unit custody match
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_development.py:111-135
  - scripts/run_public_grounded_theory_development.py:212-238
  - qc_clean/core/grounded_theory_development.py:257-296
  - qc_clean/core/grounded_theory_development.py:3183-3250
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.04
  verb: anchor
  label: Bind and validate seed proposal
  workflow_role: represent
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: proposal_draft
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: source_alias_map
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  - slot: project_state
    type: dataset
    role: context
    cardinality: one
    optional: false
  - slot: source_state_digest
    type: artifact_digest
    role: context
    cardinality: one
    optional: false
  - slot: source_units_digest
    type: artifact_digest
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: source_bound_seed_package
    type: theory
    role: result
    cardinality: one
    optional: false
  - slot: resolved_evidence_links
    type: passage_anchor
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `qc_gt.05` — Derive proposition evidence pools

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.05
  verb: derive
  label: Derive proposition evidence pools
  inputs:
    proposal:
      type: theory
      cardinality: '1'
      optional: false
    linked_categories:
      type: construct
      cardinality: 2..* per proposition
      optional: false
    linked_incidents:
      type: code
      cardinality: 2..* per category
      optional: false
  outputs:
    candidate_evidence_pool:
      type: evidence_item
      cardinality: 1..* per proposition
      optional: false
    candidate_pool_digest:
      type: artifact_digest
      cardinality: 1 per proposition
      optional: false
  parameters: &id001
  - proposition_index
  preconditions: &id002
  - category and incident indexes validate
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - qc_clean/core/grounded_theory_development.py:3154-3180
  - scripts/run_public_grounded_theory_appraisal.py:95-150
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.05
  verb: derive
  label: Derive proposition evidence pools
  workflow_role: analyze
  operation_kind: methodological_support
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: proposal
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: linked_categories
    type: construct
    role: context
    cardinality: many
    optional: false
  - slot: linked_incidents
    type: code
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: candidate_evidence_pool
    type: evidence_item
    role: result
    cardinality: many
    optional: false
  - slot: candidate_pool_digest
    type: artifact_digest
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `qc_gt.06` — Appraise seed propositions

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.06
  verb: review
  label: Appraise seed propositions
  inputs:
    propositions:
      type: proposition
      cardinality: 2..8
      optional: false
    candidate_evidence_pools:
      type: evidence_item
      cardinality: 1..* per proposition
      optional: false
  outputs:
    proposition_appraisal_draft:
      type: appraisal
      cardinality: 1 per proposition
      optional: false
  parameters: &id001
  - model
  - reasoning_effort
  - trace_id
  - budget
  - prompt_revision
  preconditions: &id002
  - every proposition has a bounded candidate pool
  method_owned_semantics: &id003
  - supporting versus qualifying evidence
  - fit
  - explanatory grammar
  - variation
  - retain-narrow-split-replace-or-more-evidence judgment
  internal_method_phases:
  - challenge_search
  - fit_appraisal
  - revision_judgment
  actor: llm_with_deterministic_orchestration
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_appraisal.py:151-180
  - scripts/run_public_grounded_theory_appraisal.py:275-323
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.06
  verb: review
  label: Appraise seed propositions
  workflow_role: appraise
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: propositions
    type: proposition
    role: subject
    cardinality: many
    optional: false
  - slot: candidate_evidence_pools
    type: evidence_item
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: proposition_appraisal_draft
    type: appraisal
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Appraise seed propositions' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `qc_gt.07` — Materialize accepted seed appraisal

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.07
  verb: project
  label: Materialize accepted seed appraisal
  inputs:
    appraisal_draft:
      type: appraisal
      cardinality: '1'
      optional: false
    seed_proposal:
      type: theory
      cardinality: '1'
      optional: false
    candidate_pools:
      type: evidence_item
      cardinality: 1..*
      optional: false
    source_alias_map:
      type: configuration
      cardinality: '1'
      optional: false
  outputs:
    appraised_seed_package:
      type: theory
      cardinality: '1'
      optional: false
    appraisal_records:
      type: appraisal
      cardinality: 1 per proposition
      optional: false
  parameters: &id001
  - schema_v2
  preconditions: &id002
  - complete proposition coverage
  - citations stay inside pools
  - revision rules pass
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_appraisal.py:183-245
  - scripts/run_public_grounded_theory_appraisal.py:324-353
  - qc_clean/core/grounded_theory_development.py:143-241
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.07
  verb: project
  label: Materialize accepted seed appraisal
  workflow_role: communicate
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: appraisal_draft
    type: appraisal
    role: subject
    cardinality: one
    optional: false
  - slot: seed_proposal
    type: theory
    role: context
    cardinality: one
    optional: false
  - slot: candidate_pools
    type: evidence_item
    role: context
    cardinality: many
    optional: false
  - slot: source_alias_map
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  outputs:
  - slot: appraised_seed_package
    type: theory
    role: result
    cardinality: one
    optional: false
  - slot: appraisal_records
    type: appraisal
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `qc_gt.08` — Initialize or resume corpus expansion

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.08
  verb: construct
  label: Initialize or resume corpus expansion
  inputs:
    appraised_seed_package:
      type: theory
      cardinality: '1'
      optional: false
    checkpoint:
      type: configuration
      cardinality: 0..1
      optional: true
    source_state_digest:
      type: artifact_digest
      cardinality: '1'
      optional: false
  outputs:
    current_proposal:
      type: theory
      cardinality: '1'
      optional: false
    covered_document_ids:
      type: source_document
      cardinality: 5..25
      optional: false
    iteration_history:
      type: review_event
      cardinality: 1..5
      optional: false
    completed_batch_count:
      type: measure
      cardinality: '1'
      optional: false
  parameters: &id001
  - four_fixed_expansion_batches
  preconditions: &id002
  - seed is schema v2 with appraisal and exact order
  - optional checkpoint matches source state
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_full_corpus.py:325-363
  - scripts/run_public_grounded_theory_full_corpus.py:1043-1078
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.08
  verb: construct
  label: Initialize or resume corpus expansion
  workflow_role: conceptualize
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: appraised_seed_package
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: checkpoint
    type: configuration
    role: config_data
    cardinality: optional_one
    optional: true
  - slot: source_state_digest
    type: artifact_digest
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: current_proposal
    type: theory
    role: result
    cardinality: one
    optional: false
  - slot: covered_document_ids
    type: source_document
    role: result
    cardinality: many
    optional: false
  - slot: iteration_history
    type: review_event
    role: result
    cardinality: many
    optional: false
  - slot: completed_batch_count
    type: measure
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `qc_gt.09` — Build one batch-comparison context

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.09
  verb: construct
  label: Build one batch-comparison context
  inputs:
    current_proposal:
      type: theory
      cardinality: '1'
      optional: false
    prior_incident_evidence:
      type: passage_anchor
      cardinality: 1..*
      optional: false
    new_batch_units:
      type: segment
      cardinality: 1..* across 5 documents
      optional: false
    prior_appraisal:
      type: appraisal
      cardinality: 0..1
      optional: true
    analytic_goal:
      type: claim
      cardinality: 0..1
      optional: true
  outputs:
    expansion_prompt:
      type: configuration
      cardinality: '1'
      optional: false
    source_alias_map:
      type: configuration
      cardinality: '1'
      optional: false
    preflight_metrics:
      type: measure
      cardinality: '1'
      optional: false
  parameters: &id001
  - current_document_ids
  - new_document_ids
  preconditions: &id002
  - new batch resolves
  - prior references remain resolvable
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_full_corpus.py:385-481
  - scripts/run_public_grounded_theory_full_corpus.py:1117-1127
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.09
  verb: construct
  label: Build one batch-comparison context
  workflow_role: conceptualize
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: current_proposal
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: prior_incident_evidence
    type: passage_anchor
    role: context
    cardinality: many
    optional: false
  - slot: new_batch_units
    type: segment
    role: context
    cardinality: many
    optional: false
  - slot: prior_appraisal
    type: appraisal
    role: context
    cardinality: optional_one
    optional: true
  - slot: analytic_goal
    type: claim
    role: context
    cardinality: optional_one
    optional: true
  outputs:
  - slot: expansion_prompt
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: source_alias_map
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: preflight_metrics
    type: measure
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `qc_gt.10` — Compare batch and revise proposal

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.10
  verb: revise
  label: Compare batch and revise proposal
  inputs:
    current_proposal:
      type: theory
      cardinality: '1'
      optional: false
    prior_evidence:
      type: passage_anchor
      cardinality: 1..*
      optional: false
    new_batch_units:
      type: segment
      cardinality: 1..*
      optional: false
  outputs:
    batch_incidents:
      type: code
      cardinality: 5..20
      optional: false
    complete_revised_proposal:
      type: theory
      cardinality: '1'
      optional: false
    category_changes:
      type: finding
      cardinality: 1..10
      optional: false
    incident_consolidation_memo:
      type: memo
      cardinality: '1'
      optional: false
    comparison_memo:
      type: memo
      cardinality: '1'
      optional: false
    remaining_uncertainty:
      type: uncertainty_note
      cardinality: '1'
      optional: false
  parameters: &id001
  - model
  - reasoning_effort
  - trace_id
  - budget
  - prompt_revision
  preconditions: &id002
  - expansion context exists
  method_owned_semantics: &id003
  - fresh incident development
  - constant comparison
  - consolidation
  - category refine-merge-split-replace decisions
  - novelty judgment
  - remaining uncertainty
  internal_method_phases:
  - develop_batch_incidents
  - constant_comparison
  - consolidate_incidents
  - revise_categories
  - revise_theory
  actor: llm_with_deterministic_orchestration
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_full_corpus.py:103-118
  - scripts/run_public_grounded_theory_full_corpus.py:428-467
  - scripts/run_public_grounded_theory_full_corpus.py:1128-1145
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.10
  verb: revise
  label: Compare batch and revise proposal
  workflow_role: revise
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: current_proposal
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: prior_evidence
    type: passage_anchor
    role: context
    cardinality: many
    optional: false
  - slot: new_batch_units
    type: segment
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: batch_incidents
    type: code
    role: result
    cardinality: many
    optional: false
  - slot: complete_revised_proposal
    type: theory
    role: result
    cardinality: one
    optional: false
  - slot: category_changes
    type: finding
    role: result
    cardinality: many
    optional: false
  - slot: incident_consolidation_memo
    type: memo
    role: result
    cardinality: one
    optional: false
  - slot: comparison_memo
    type: memo
    role: result
    cardinality: one
    optional: false
  - slot: remaining_uncertainty
    type: uncertainty_note
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Compare batch and revise proposal' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `qc_gt.11` — Validate and checkpoint iteration

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.11
  verb: project
  label: Validate and checkpoint iteration
  inputs:
    expansion_draft:
      type: theory
      cardinality: '1'
      optional: false
    source_alias_map:
      type: configuration
      cardinality: '1'
      optional: false
    new_batch_documents:
      type: source_document
      cardinality: '5'
      optional: false
    prior_iteration_history:
      type: review_event
      cardinality: 1..4
      optional: false
  outputs:
    validated_current_proposal:
      type: theory
      cardinality: '1'
      optional: false
    validated_batch_incidents:
      type: code
      cardinality: 5..20
      optional: false
    iteration_record:
      type: review_event
      cardinality: '1'
      optional: false
    checkpoint:
      type: configuration
      cardinality: '1'
      optional: false
    structural_repairs:
      type: uncertainty_note
      cardinality: 0..*
      optional: true
  parameters: &id001
  - iteration_number
  preconditions: &id002
  - batch incidents cover only and all new documents
  - category changes cite new evidence
  - proposal custody validates
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_full_corpus.py:536-623
  - scripts/run_public_grounded_theory_full_corpus.py:1152-1216
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.11
  verb: project
  label: Validate and checkpoint iteration
  workflow_role: communicate
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: expansion_draft
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: source_alias_map
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  - slot: new_batch_documents
    type: source_document
    role: context
    cardinality: many
    optional: false
  - slot: prior_iteration_history
    type: review_event
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: validated_current_proposal
    type: theory
    role: result
    cardinality: one
    optional: false
  - slot: validated_batch_incidents
    type: code
    role: result
    cardinality: many
    optional: false
  - slot: iteration_record
    type: review_event
    role: result
    cardinality: one
    optional: false
  - slot: checkpoint
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: structural_repairs
    type: uncertainty_note
    role: result
    cardinality: optional_many
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `qc_gt.12` — Build final appraisal universe

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.12
  verb: derive
  label: Build final appraisal universe
  inputs:
    final_proposal:
      type: theory
      cardinality: '1'
      optional: false
    all_corpus_units:
      type: segment
      cardinality: 1..*
      optional: false
  outputs:
    linked_candidate_pools:
      type: evidence_item
      cardinality: 1..* per proposition
      optional: false
    participant_challenge_pool:
      type: evidence_item
      cardinality: all participant units
      optional: false
    final_appraisal_prompt:
      type: configuration
      cardinality: '1'
      optional: false
    preflight_metrics:
      type: measure
      cardinality: '1'
      optional: false
  parameters: &id001
  - all_25_document_ids
  preconditions: &id002
  - four expansion batches completed
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_full_corpus.py:626-747
  - scripts/run_public_grounded_theory_full_corpus.py:1218-1230
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.12
  verb: derive
  label: Build final appraisal universe
  workflow_role: analyze
  operation_kind: methodological_support
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: final_proposal
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: all_corpus_units
    type: segment
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: linked_candidate_pools
    type: evidence_item
    role: result
    cardinality: many
    optional: false
  - slot: participant_challenge_pool
    type: evidence_item
    role: result
    cardinality: many
    optional: false
  - slot: final_appraisal_prompt
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: preflight_metrics
    type: measure
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `qc_gt.13` — Appraise final theory and corpus

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.13
  verb: review
  label: Appraise final theory and corpus
  inputs:
    final_propositions:
      type: proposition
      cardinality: 2..8
      optional: false
    linked_candidate_pools:
      type: evidence_item
      cardinality: 1..* per proposition
      optional: false
    participant_challenge_pool:
      type: evidence_item
      cardinality: 1..*
      optional: false
    final_categories:
      type: construct
      cardinality: 3..8
      optional: false
  outputs:
    proposition_appraisals:
      type: appraisal
      cardinality: 1 per proposition
      optional: false
    challenge_searches:
      type: appraisal
      cardinality: 1 per proposition
      optional: false
    category_adequacy:
      type: appraisal
      cardinality: 1 per category
      optional: false
    fixed_corpus_assessment:
      type: finding
      cardinality: '1'
      optional: false
    sampling_questions:
      type: gap
      cardinality: 2..6
      optional: false
    narrative_report:
      type: finding
      cardinality: '1'
      optional: false
  parameters: &id001
  - model
  - reasoning_effort
  - trace_id
  - budget
  - prompt_revision
  preconditions: &id002
  - final appraisal universe exists
  method_owned_semantics: &id003
  - evidence stance
  - counterexample search
  - fit-workability-revision judgment
  - category adequacy
  - fixed-corpus limitations
  - sampling value
  - narrative synthesis
  internal_method_phases:
  - challenge_search
  - proposition_appraisal
  - category_adequacy_appraisal
  - sampling_question_generation
  - narrative_synthesis
  actor: llm_with_deterministic_orchestration
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_full_corpus.py:120-178
  - scripts/run_public_grounded_theory_full_corpus.py:685-730
  - scripts/run_public_grounded_theory_full_corpus.py:1231-1248
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.13
  verb: review
  label: Appraise final theory and corpus
  workflow_role: appraise
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: final_propositions
    type: proposition
    role: subject
    cardinality: many
    optional: false
  - slot: linked_candidate_pools
    type: evidence_item
    role: context
    cardinality: many
    optional: false
  - slot: participant_challenge_pool
    type: evidence_item
    role: context
    cardinality: many
    optional: false
  - slot: final_categories
    type: construct
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: proposition_appraisals
    type: appraisal
    role: result
    cardinality: many
    optional: false
  - slot: challenge_searches
    type: appraisal
    role: result
    cardinality: many
    optional: false
  - slot: category_adequacy
    type: appraisal
    role: result
    cardinality: many
    optional: false
  - slot: fixed_corpus_assessment
    type: finding
    role: result
    cardinality: one
    optional: false
  - slot: sampling_questions
    type: gap
    role: result
    cardinality: many
    optional: false
  - slot: narrative_report
    type: finding
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Appraise final theory and corpus' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `qc_gt.14` — Materialize final appraisal outputs

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.14
  verb: project
  label: Materialize final appraisal outputs
  inputs:
    final_draft:
      type: appraisal
      cardinality: '1'
      optional: false
    proposal:
      type: theory
      cardinality: '1'
      optional: false
    source_alias_map:
      type: configuration
      cardinality: '1'
      optional: false
    candidate_pools:
      type: evidence_item
      cardinality: 1..* per proposition
      optional: false
  outputs:
    validated_appraisal:
      type: appraisal
      cardinality: '1'
      optional: false
    validated_category_adequacy:
      type: appraisal
      cardinality: 1 per category
      optional: false
    sampling_questions:
      type: gap
      cardinality: 2..6
      optional: false
    narrative_report:
      type: finding
      cardinality: '1'
      optional: false
    structural_repairs:
      type: uncertainty_note
      cardinality: 0..*
      optional: true
  parameters: &id001 []
  preconditions: &id002
  - exact proposition and category coverage
  - participant-only evidence
  - challenge classifications do not conflict
  - references validate
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - scripts/run_public_grounded_theory_full_corpus.py:782-1040
  - scripts/run_public_grounded_theory_appraisal.py:183-245
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.14
  verb: project
  label: Materialize final appraisal outputs
  workflow_role: communicate
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: final_draft
    type: appraisal
    role: subject
    cardinality: one
    optional: false
  - slot: proposal
    type: theory
    role: context
    cardinality: one
    optional: false
  - slot: source_alias_map
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  - slot: candidate_pools
    type: evidence_item
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: validated_appraisal
    type: appraisal
    role: result
    cardinality: one
    optional: false
  - slot: validated_category_adequacy
    type: appraisal
    role: result
    cardinality: many
    optional: false
  - slot: sampling_questions
    type: gap
    role: result
    cardinality: many
    optional: false
  - slot: narrative_report
    type: finding
    role: result
    cardinality: one
    optional: false
  - slot: structural_repairs
    type: uncertainty_note
    role: result
    cardinality: optional_many
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `qc_gt.15` — Project and persist full-corpus result

```yaml
legacy_workflow: qc_fixed_corpus_grounded_theory_v3
original_values:
  step_id: qc_gt.15
  verb: project
  label: Project and persist full-corpus result
  inputs:
    proposal:
      type: theory
      cardinality: '1'
      optional: false
    appraisal:
      type: appraisal
      cardinality: '1'
      optional: false
    iteration_history:
      type: review_event
      cardinality: '5'
      optional: false
    category_adequacy:
      type: appraisal
      cardinality: 1 per category
      optional: false
    sampling_questions:
      type: gap
      cardinality: 2..6
      optional: false
    narrative_report:
      type: finding
      cardinality: '1'
      optional: false
    project_state:
      type: dataset
      cardinality: '1'
      optional: false
  outputs:
    full_corpus_package:
      type: theory
      cardinality: '1'
      optional: false
    source_resolved_read_model:
      type: theory
      cardinality: '1'
      optional: false
    persisted_artifact:
      type: dataset
      cardinality: '1'
      optional: false
    artifact_digest:
      type: artifact_digest
      cardinality: '1'
      optional: false
  parameters: &id001
  - schema_v3
  - output_filename
  preconditions: &id002
  - v3 completeness
  - contiguous iteration lineage
  - full category coverage
  - custody and candidate hashes validate
  - every citation resolves
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - qc_clean/core/grounded_theory_development.py:316-407
  - qc_clean/core/grounded_theory_development.py:3183-3250
  - qc_clean/core/grounded_theory_development.py:3317-3605
  - scripts/run_public_grounded_theory_full_corpus.py:1263-1305
assigned_rev5_values:
  method_id: qc_grounded_theory
  step_id: qc_gt.15
  verb: project
  label: Project and persist full-corpus result
  workflow_role: communicate
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: proposal
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: appraisal
    type: appraisal
    role: context
    cardinality: one
    optional: false
  - slot: iteration_history
    type: review_event
    role: context
    cardinality: many
    optional: false
  - slot: category_adequacy
    type: appraisal
    role: context
    cardinality: many
    optional: false
  - slot: sampling_questions
    type: gap
    role: context
    cardinality: many
    optional: false
  - slot: narrative_report
    type: finding
    role: context
    cardinality: one
    optional: false
  - slot: project_state
    type: dataset
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: full_corpus_package
    type: theory
    role: result
    cardinality: one
    optional: false
  - slot: source_resolved_read_model
    type: theory
    role: result
    cardinality: one
    optional: false
  - slot: persisted_artifact
    type: dataset
    role: result
    cardinality: one
    optional: false
  - slot: artifact_digest
    type: artifact_digest
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Corbin & Strauss (2015), Basics of Qualitative Research, 4th ed.; Charmaz (2014), Constructing Grounded Theory, 2nd ed.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `pt.01` — Bind and validate run design

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.01
  verb: construct
  label: Bind and validate run design
  inputs:
    source_text:
      type: source_document
      cardinality: '1'
      optional: false
    source_packet:
      type: dataset
      cardinality: 0..1
      optional: true
    inference_design:
      type: configuration
      cardinality: 0..1
      optional: true
    theory_material:
      type: theory
      cardinality: 0..1
      optional: true
    segmented_source:
      type: dataset
      cardinality: 0..1
      optional: true
    cached_result:
      type: finding
      cardinality: 0..1
      optional: true
  outputs:
    bound_source_scope:
      type: configuration
      cardinality: '1'
      optional: false
    source_digest:
      type: artifact_digest
      cardinality: '1'
      optional: false
    validated_run_configuration:
      type: configuration
      cardinality: '1'
      optional: false
  parameters: &id001
  - research_question
  - models
  - review_and_refinement_switches
  - retry_budgets
  preconditions: &id002
  - fresh input has at least 300 words
  - options are compatible
  - packet question matches
  - segmented source reconstructs exactly
  - packet source IDs are unique
  method_owned_semantics: &id003
  - theory-first versus discovery-evaluation split versus exploratory design
  - theory-evidence independence
  internal_method_phases:
  - scope_case
  - choose_inference_design
  - bind_source_roles
  actor: researcher_and_deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pipeline.py:1653-1840
  - pt/schemas.py:663-723
  - pt/source_packet.py:389-425
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.01
  verb: construct
  label: Bind and validate run design
  workflow_role: conceptualize
  operation_kind: analytic
  actor_chain:
  - human_analyst
  - deterministic_validator
  inputs:
  - slot: source_text
    type: source_document
    role: subject
    cardinality: one
    optional: false
  - slot: source_packet
    type: dataset
    role: context
    cardinality: optional_one
    optional: true
  - slot: inference_design
    type: configuration
    role: config_data
    cardinality: optional_one
    optional: true
  - slot: theory_material
    type: theory
    role: context
    cardinality: optional_one
    optional: true
  - slot: segmented_source
    type: dataset
    role: context
    cardinality: optional_one
    optional: true
  - slot: cached_result
    type: finding
    role: context
    cardinality: optional_one
    optional: true
  outputs:
  - slot: bound_source_scope
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: source_digest
    type: artifact_digest
    role: result
    cardinality: one
    optional: false
  - slot: validated_run_configuration
    type: configuration
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Bind and validate run design' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.02` — Freeze pre-corpus hypotheses

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.02
  verb: construct
  label: Freeze pre-corpus hypotheses
  inputs:
    theory_material:
      type: theory
      cardinality: '1'
      optional: false
    research_question:
      type: claim
      cardinality: 0..1
      optional: true
    empty_extraction:
      type: finding
      cardinality: '1'
      optional: false
    generation_view:
      type: configuration
      cardinality: '1'
      optional: false
  outputs:
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
  parameters: &id001
  - analyst_model
  - optional_supplied_frozen_space
  preconditions: &id002
  - theory_first mode
  - theory material nonblank
  - corpus evidence hidden
  method_owned_semantics: &id003
  - causal mechanisms
  - complete rivals
  - observable predictions
  internal_method_phases:
  - formulate_mechanisms
  - enumerate_rivals
  - derive_observables
  actor: llm_or_researcher
  optional: true
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pipeline.py:1953-1982
  - pt/pass_hypothesize.py:242-273
  - pt/pass_hypothesize.py:295-383
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.02
  verb: construct
  label: Freeze pre-corpus hypotheses
  workflow_role: conceptualize
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - human_analyst
  inputs:
  - slot: theory_material
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: research_question
    type: claim
    role: context
    cardinality: optional_one
    optional: true
  - slot: empty_extraction
    type: finding
    role: context
    cardinality: one
    optional: false
  - slot: generation_view
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  outputs:
  - slot: hypothesis_space
    type: rival_explanation
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Freeze pre-corpus hypotheses' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.03` — Extract source-grounded causal inventory

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.03
  verb: extract
  label: Extract source-grounded causal inventory
  inputs:
    source_text:
      type: source_document
      cardinality: '1'
      optional: false
    analysis_focus_context:
      type: configuration
      cardinality: 0..1
      optional: true
    source_scope_context:
      type: configuration
      cardinality: 0..1
      optional: true
    segmented_source:
      type: dataset
      cardinality: 0..1
      optional: true
  outputs:
    evidence:
      type: evidence_item
      cardinality: 0..*
      optional: false
    actors:
      type: entity
      cardinality: 0..*
      optional: false
    events:
      type: finding
      cardinality: 0..*
      optional: false
    mechanisms:
      type: relation
      cardinality: 0..*
      optional: false
    causal_edges:
      type: relation
      cardinality: 0..*
      optional: false
    source_anchors:
      type: passage_anchor
      cardinality: 0..*
      optional: false
  parameters: &id001
  - extraction_model
  - grounding_repair_model
  preconditions: &id002
  - validated source
  - packet markers and source IDs validate when supplied
  method_owned_semantics: &id003
  - what counts as a causal-process observation relevant to the bounded outcome and rivals
  internal_method_phases:
  - extract_evidence
  - extract_actors_events_and_mechanisms
  - ground_spans
  actor: llm_with_deterministic_validation
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pipeline.py:1983-2006
  - pt/pass_extract.py:1152-1234
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.03
  verb: extract
  label: Extract source-grounded causal inventory
  workflow_role: analyze
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: source_text
    type: source_document
    role: subject
    cardinality: one
    optional: false
  - slot: analysis_focus_context
    type: configuration
    role: config_data
    cardinality: optional_one
    optional: true
  - slot: source_scope_context
    type: configuration
    role: config_data
    cardinality: optional_one
    optional: true
  - slot: segmented_source
    type: dataset
    role: context
    cardinality: optional_one
    optional: true
  outputs:
  - slot: evidence
    type: evidence_item
    role: result
    cardinality: many
    optional: false
  - slot: actors
    type: entity
    role: result
    cardinality: many
    optional: false
  - slot: events
    type: finding
    role: result
    cardinality: many
    optional: false
  - slot: mechanisms
    type: relation
    role: result
    cardinality: many
    optional: false
  - slot: causal_edges
    type: relation
    role: result
    cardinality: many
    optional: false
  - slot: source_anchors
    type: passage_anchor
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Extract source-grounded causal inventory' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.04` — Materialize evidence exposure lineage

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.04
  verb: project
  label: Materialize evidence exposure lineage
  inputs:
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    inference_design:
      type: configuration
      cardinality: '1'
      optional: false
  outputs:
    generation_view:
      type: configuration
      cardinality: '1'
      optional: false
    post_selection_evidence_ids:
      type: evidence_item
      cardinality: 0..*
      optional: false
  parameters: &id001 []
  preconditions: &id002
  - source roles cover packet sources for split designs
  - evidence-to-source lineage is complete
  method_owned_semantics: &id003
  - which evidence may formulate hypotheses and which remains update-eligible
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pipeline.py:609-690
  - pt/pipeline.py:2008-2017
  - pt/pass_hypothesize.py:242-273
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.04
  verb: project
  label: Materialize evidence exposure lineage
  workflow_role: communicate
  operation_kind: methodological_support
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: extraction
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: inference_design
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  outputs:
  - slot: generation_view
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: post_selection_evidence_ids
    type: evidence_item
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `pt.05` — Build hypotheses from exposed evidence

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.05
  verb: construct
  label: Build hypotheses from exposed evidence
  inputs:
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    generation_view:
      type: configuration
      cardinality: '1'
      optional: false
    theory_material:
      type: theory
      cardinality: 0..1
      optional: true
    source_scope_context:
      type: configuration
      cardinality: 0..1
      optional: true
  outputs:
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
  parameters: &id001
  - research_question
  - analyst_model
  preconditions: &id002
  - no frozen pre-corpus hypothesis space selected
  method_owned_semantics: &id003
  - rival causal configurations and observable predictions with anti-tautology and provenance constraints
  internal_method_phases:
  - formulate_mechanisms
  - enumerate_rivals
  - derive_observables
  actor: llm_with_deterministic_exposure_binding
  optional: true
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pipeline.py:2019-2044
  - pt/pass_hypothesize.py:295-383
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.05
  verb: construct
  label: Build hypotheses from exposed evidence
  workflow_role: conceptualize
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: extraction
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: generation_view
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  - slot: theory_material
    type: theory
    role: context
    cardinality: optional_one
    optional: true
  - slot: source_scope_context
    type: configuration
    role: config_data
    cardinality: optional_one
    optional: true
  outputs:
  - slot: hypothesis_space
    type: rival_explanation
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Build hypotheses from exposed evidence' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.06` — Review rival hypotheses

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.06
  verb: review
  label: Review rival hypotheses
  inputs:
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
  outputs:
    reviewed_hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
  parameters: &id001
  - custom_review_function_or_interactive_json
  preconditions: &id002
  - human review enabled
  method_owned_semantics: &id003
  - merge
  - split
  - revise
  - or accept rival explanations
  internal_method_phases: []
  actor: human
  optional: true
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pipeline.py:134-168
  - pt/pipeline.py:2046-2050
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.06
  verb: review
  label: Review rival hypotheses
  workflow_role: appraise
  operation_kind: methodological_support
  actor_chain:
  - human_reviewer
  inputs:
  - slot: hypothesis_space
    type: rival_explanation
    role: subject
    cardinality: many
    optional: false
  outputs:
  - slot: reviewed_hypothesis_space
    type: rival_explanation
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: manually_performed
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- Legacy executable means the human-review callback is callable, not that software performs the review judgment; rev 5 therefore assigns manually_performed.
```

### `pt.07` — Audit rival partition

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.07
  verb: review
  label: Audit rival partition
  inputs:
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    generation_view:
      type: configuration
      cardinality: '1'
      optional: false
  outputs:
    partition_audit:
      type: appraisal
      cardinality: '1'
      optional: false
    partition_resolution:
      type: finding
      cardinality: '1'
      optional: false
  parameters: &id001
  - audit_model
  - repair_budget
  - optional_manual_review
  preconditions: &id002
  - hypothesis and prediction IDs are unique
  - exposure lineage validates
  method_owned_semantics: &id003
  - whether every rival pair has an opposed prediction
  - whether overlap or complementarity blocks normalized comparison
  internal_method_phases:
  - pair_rivals
  - inspect_discriminators
  - judge_partition_adequacy
  actor: auditor_llm_with_deterministic_gate
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_partition.py:187-243
  - pt/pipeline.py:288-385
  - pt/pipeline.py:2052-2080
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.07
  verb: review
  label: Audit rival partition
  workflow_role: appraise
  operation_kind: methodological_support
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: hypothesis_space
    type: rival_explanation
    role: subject
    cardinality: many
    optional: false
  - slot: generation_view
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  outputs:
  - slot: partition_audit
    type: appraisal
    role: result
    cardinality: one
    optional: false
  - slot: partition_resolution
    type: finding
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.08` — Repair blocked rival partition

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.08
  verb: revise
  label: Repair blocked rival partition
  inputs:
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    partition_audit:
      type: appraisal
      cardinality: '1'
      optional: false
    generation_view:
      type: configuration
      cardinality: '1'
      optional: false
  outputs:
    revised_hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
  parameters: &id001
  - repair_model
  - automated_repair_count
  - optional_human_review
  preconditions: &id002
  - partition blocked
  - repair budget remains
  method_owned_semantics: &id003
  - revised rivals retain the outcome while resolving invalid pair structure
  internal_method_phases: []
  actor: repair_llm_or_human
  optional: true
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_partition_repair.py:27-63
  - pt/pipeline.py:340-377
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.08
  verb: revise
  label: Repair blocked rival partition
  workflow_role: revise
  operation_kind: methodological_support
  actor_chain:
  - llm_engine
  - human_reviewer
  inputs:
  - slot: extraction
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: hypothesis_space
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  - slot: partition_audit
    type: appraisal
    role: context
    cardinality: one
    optional: false
  - slot: generation_view
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  outputs:
  - slot: revised_hypothesis_space
    type: rival_explanation
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `pt.09` — Bind priors

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.09
  verb: construct
  label: Bind priors
  inputs:
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    prior_specification:
      type: parameter_set
      cardinality: 0..1
      optional: true
  outputs:
    validated_prior:
      type: parameter_set
      cardinality: '1'
      optional: false
  parameters: &id001
  - uniform_default_or_typed_prior
  preconditions: &id002
  - prior covers accepted hypotheses and declares evidence provenance
  method_owned_semantics: &id003
  - prior-construction rationale
  internal_method_phases: []
  actor: researcher_and_deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pipeline.py:588-606
  - pt/pipeline.py:2082-2086
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.09
  verb: construct
  label: Bind priors
  workflow_role: conceptualize
  operation_kind: analytic
  actor_chain:
  - human_analyst
  - deterministic_validator
  inputs:
  - slot: hypothesis_space
    type: rival_explanation
    role: subject
    cardinality: many
    optional: false
  - slot: extraction
    type: finding
    role: context
    cardinality: one
    optional: false
  - slot: prior_specification
    type: parameter_set
    role: context
    cardinality: optional_one
    optional: true
  outputs:
  - slot: validated_prior
    type: parameter_set
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Bind priors' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `pt.10` — Measure source coverage

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.10
  verb: measure
  label: Measure source coverage
  inputs:
    source_packet:
      type: dataset
      cardinality: 0..1
      optional: true
    source_text:
      type: source_document
      cardinality: '1'
      optional: false
    extraction:
      type: finding
      cardinality: '1'
      optional: false
  outputs:
    source_coverage:
      type: measure
      cardinality: 0..1
      optional: true
    source_opportunity_ids:
      type: source_document
      cardinality: 0..*
      optional: false
  parameters: &id001
  - packet_markers
  - source_ids
  preconditions: &id002
  - typed source packet supplied
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: true
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/source_coverage.py:22-103
  - pt/pipeline.py:2091-2097
  - pt/pipeline.py:2431-2438
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.10
  verb: measure
  label: Measure source coverage
  workflow_role: analyze
  operation_kind: methodological_support
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: source_packet
    type: dataset
    role: subject
    cardinality: optional_one
    optional: true
  - slot: source_text
    type: source_document
    role: context
    cardinality: one
    optional: false
  - slot: extraction
    type: finding
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: source_coverage
    type: measure
    role: result
    cardinality: optional_one
    optional: true
  - slot: source_opportunity_ids
    type: source_document
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `pt.11` — Elicit evidence-by-hypothesis likelihoods

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.11
  verb: test
  label: Elicit evidence-by-hypothesis likelihoods
  inputs:
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    partition_audit:
      type: appraisal
      cardinality: '1'
      optional: false
    prior_evidence_ids:
      type: evidence_item
      cardinality: 0..*
      optional: false
    post_selection_evidence_ids:
      type: evidence_item
      cardinality: 0..*
      optional: false
  outputs:
    raw_testing:
      type: appraisal
      cardinality: '1'
      optional: false
  parameters: &id001
  - analyst_model
  - batch_size_policy
  - repair_context
  preconditions: &id002
  - partition accepted
  - priors and evidence-exposure plan bound
  method_owned_semantics: &id003
  - rival-relative likelihood vectors
  - prediction links
  - diagnostic types
  - dependence structure
  internal_method_phases:
  - relate_evidence_to_predictions
  - elicit_relative_likelihoods
  - record_dependence
  actor: analyst_llm_with_deterministic_validation
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_test.py:1289-1416
  - pt/pipeline.py:1231-1245
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.11
  verb: test
  label: Elicit evidence-by-hypothesis likelihoods
  workflow_role: appraise
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: extraction
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: hypothesis_space
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  - slot: partition_audit
    type: appraisal
    role: context
    cardinality: one
    optional: false
  - slot: prior_evidence_ids
    type: evidence_item
    role: context
    cardinality: many
    optional: false
  - slot: post_selection_evidence_ids
    type: evidence_item
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: raw_testing
    type: appraisal
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Elicit evidence-by-hypothesis likelihoods' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.12` — Audit discriminator claims

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.12
  verb: review
  label: Audit discriminator claims
  inputs:
    raw_testing:
      type: appraisal
      cardinality: '1'
      optional: false
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    partition_audit:
      type: appraisal
      cardinality: '1'
      optional: false
  outputs:
    effective_testing:
      type: appraisal
      cardinality: '1'
      optional: false
    discriminator_resolution:
      type: finding
      cardinality: '1'
      optional: false
  parameters: &id001
  - independent_audit_model
  - re_elicitation_count
  preconditions: &id002
  - quotes and source lineage validate
  - prediction contrast was accepted
  method_owned_semantics: &id003
  - whether a non-equal likelihood comparison is warranted against the named rival
  internal_method_phases:
  - audit_each_discriminator
  - request_reelicitation_or_project_rejection
  actor: independent_auditor_llm_with_deterministic_projection
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_discriminator_audit.py:453-644
  - pt/pass_discriminator_audit.py:690-827
  - pt/pipeline.py:449-585
  - pt/pipeline.py:1247-1265
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.12
  verb: review
  label: Audit discriminator claims
  workflow_role: appraise
  operation_kind: methodological_support
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: raw_testing
    type: appraisal
    role: subject
    cardinality: one
    optional: false
  - slot: extraction
    type: finding
    role: context
    cardinality: one
    optional: false
  - slot: hypothesis_space
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  - slot: partition_audit
    type: appraisal
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: effective_testing
    type: appraisal
    role: result
    cardinality: one
    optional: false
  - slot: discriminator_resolution
    type: finding
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.13` — Evaluate missing predicted evidence

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.13
  verb: test
  label: Evaluate missing predicted evidence
  inputs:
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    effective_testing:
      type: appraisal
      cardinality: '1'
      optional: false
    source_scope_context:
      type: configuration
      cardinality: 0..1
      optional: true
  outputs:
    absence_result:
      type: diagnostic_item
      cardinality: '1'
      optional: false
  parameters: &id001
  - analyst_model
  preconditions: &id002
  - effective testing artifact exists
  method_owned_semantics: &id003
  - whether a trace should have been observable in the admitted corpus
  - severity under source limitations
  internal_method_phases:
  - derive_expected_traces
  - inspect_absence
  - judge_observability
  actor: analyst_llm_with_deterministic_severity_cap
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_absence.py:100-157
  - pt/pipeline.py:1267-1280
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.13
  verb: test
  label: Evaluate missing predicted evidence
  workflow_role: appraise
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: extraction
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: hypothesis_space
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  - slot: effective_testing
    type: appraisal
    role: context
    cardinality: one
    optional: false
  - slot: source_scope_context
    type: configuration
    role: config_data
    cardinality: optional_one
    optional: true
  outputs:
  - slot: absence_result
    type: diagnostic_item
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Evaluate missing predicted evidence' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.14` — Audit and admit source-silence evidence

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.14
  verb: review
  label: Audit and admit source-silence evidence
  inputs:
    absence_result:
      type: diagnostic_item
      cardinality: '1'
      optional: false
    testing:
      type: appraisal
      cardinality: '1'
      optional: false
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    source_scope_context:
      type: configuration
      cardinality: '1'
      optional: false
    source_ids:
      type: source_document
      cardinality: 1..*
      optional: false
  outputs:
    source_silence_resolution:
      type: finding
      cardinality: '1'
      optional: false
    absence_adjusted_testing:
      type: appraisal
      cardinality: '1'
      optional: false
  parameters: &id001
  - audit_model
  preconditions: &id002
  - theory-first or split design
  - no post-selection exposure
  - admitted sources cover proposed silence vectors
  method_owned_semantics: &id003
  - whether an admitted source was genuinely positioned to carry a missing trace
  internal_method_phases:
  - audit_source_position
  - admit_or_reject_silence_vector
  actor: independent_auditor_llm_with_deterministic_binding
  optional: true
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_absence_audit.py:166-230
  - pt/pass_absence_audit.py:233-305
  - pt/pipeline.py:1282-1328
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.14
  verb: review
  label: Audit and admit source-silence evidence
  workflow_role: appraise
  operation_kind: methodological_support
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: absence_result
    type: diagnostic_item
    role: subject
    cardinality: one
    optional: false
  - slot: testing
    type: appraisal
    role: context
    cardinality: one
    optional: false
  - slot: extraction
    type: finding
    role: context
    cardinality: one
    optional: false
  - slot: source_scope_context
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  - slot: source_ids
    type: source_document
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: source_silence_resolution
    type: finding
    role: result
    cardinality: one
    optional: false
  - slot: absence_adjusted_testing
    type: appraisal
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.15` — Compute comparative support and sensitivity

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.15
  verb: estimate
  label: Compute comparative support and sensitivity
  inputs:
    effective_testing:
      type: appraisal
      cardinality: '1'
      optional: false
    prior:
      type: parameter_set
      cardinality: '1'
      optional: false
    hypothesis_ids:
      type: rival_explanation
      cardinality: 1..*
      optional: false
  outputs:
    comparative_support:
      type: estimate
      cardinality: '1'
      optional: false
    no_silence_counterfactual:
      type: estimate
      cardinality: 0..1
      optional: true
  parameters: &id001
  - residual_inclusion
  - dependence_pooling
  - sensitivity_scenarios
  preconditions: &id002
  - audited semantic testing artifact exists
  method_owned_semantics: &id003
  - within-case comparative support
  - not historical-truth probability
  internal_method_phases:
  - pool_dependent_items
  - update_relative_support
  - run_sensitivity
  actor: deterministic_model
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/bayesian.py:668-758
  - pt/pipeline.py:1330-1356
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.15
  verb: estimate
  label: Compute comparative support and sensitivity
  workflow_role: analyze
  operation_kind: analytic
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: effective_testing
    type: appraisal
    role: subject
    cardinality: one
    optional: false
  - slot: prior
    type: parameter_set
    role: context
    cardinality: one
    optional: false
  - slot: hypothesis_ids
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: comparative_support
    type: estimate
    role: result
    cardinality: one
    optional: false
  - slot: no_silence_counterfactual
    type: estimate
    role: result
    cardinality: optional_one
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Compute comparative support and sensitivity' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.16` — Derive rival-pair diagnostic matrix

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.16
  verb: derive
  label: Derive rival-pair diagnostic matrix
  inputs:
    effective_testing:
      type: appraisal
      cardinality: '1'
      optional: false
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    partition_audit:
      type: appraisal
      cardinality: '1'
      optional: false
  outputs:
    diagnostic_matrix:
      type: diagnostic_item
      cardinality: '1'
      optional: false
  parameters: &id001
  - fixed_magnitude_descriptions
  preconditions: &id002
  - semantic audit completed
  method_owned_semantics: &id003
  - pairwise discriminator interpretation and grade caps
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_diagnostic.py:48-120
  - pt/pipeline.py:1358-1369
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.16
  verb: derive
  label: Derive rival-pair diagnostic matrix
  workflow_role: analyze
  operation_kind: analytic
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: effective_testing
    type: appraisal
    role: subject
    cardinality: one
    optional: false
  - slot: hypothesis_space
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  - slot: partition_audit
    type: appraisal
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: diagnostic_matrix
    type: diagnostic_item
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Derive rival-pair diagnostic matrix' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `pt.17` — Construct temporal mechanism graph

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.17
  verb: construct
  label: Construct temporal mechanism graph
  inputs:
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    partition_audit:
      type: appraisal
      cardinality: '1'
      optional: false
    effective_testing:
      type: appraisal
      cardinality: '1'
      optional: false
    discriminator_resolution:
      type: finding
      cardinality: '1'
      optional: false
  outputs:
    candidate_mechanism_trace:
      type: model
      cardinality: '1'
      optional: false
  parameters: &id001
  - analyst_model
  - source_scope
  - bounded_validation_repair
  preconditions: &id002
  - accepted discriminator audit bound to testing
  method_owned_semantics: &id003
  - stage definition and forward edge status as sequence
  - supported causation
  - contestation
  - or unresolved link
  internal_method_phases:
  - construct_stages
  - connect_forward_edges
  - label_edge_status
  actor: analyst_llm_with_deterministic_graph_validation
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_mechanism.py:433-531
  - pt/pipeline.py:1371-1382
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.17
  verb: construct
  label: Construct temporal mechanism graph
  workflow_role: conceptualize
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: extraction
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: hypothesis_space
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  - slot: partition_audit
    type: appraisal
    role: context
    cardinality: one
    optional: false
  - slot: effective_testing
    type: appraisal
    role: context
    cardinality: one
    optional: false
  - slot: discriminator_resolution
    type: finding
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: candidate_mechanism_trace
    type: model
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Construct temporal mechanism graph' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.18` — Audit and repair mechanism graph

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.18
  verb: review
  label: Audit and repair mechanism graph
  inputs:
    candidate_trace:
      type: model
      cardinality: '1'
      optional: false
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    hypothesis_space:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    effective_testing:
      type: appraisal
      cardinality: '1'
      optional: false
  outputs:
    final_trace:
      type: model
      cardinality: '1'
      optional: false
    mechanism_audit_resolution:
      type: finding
      cardinality: '1'
      optional: false
  parameters: &id001
  - audit_model
  - repair_budget
  - patch_or_replacement_mode
  preconditions: &id002
  - candidate is hash-bound and source grounded
  method_owned_semantics: &id003
  - whether each edge and mechanism-stage claim is source-supported; repair may weaken but not strengthen
  internal_method_phases:
  - audit_stages_and_edges
  - patch_or_replace
  - reaudit
  actor: independent_auditor_and_repair_llms_with_deterministic_checks
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pipeline.py:825-1182
  - pt/pipeline.py:1383-1398
  - pt/pass_mechanism_audit.py:979-1114
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.18
  verb: review
  label: Audit and repair mechanism graph
  workflow_role: appraise
  operation_kind: methodological_support
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: candidate_trace
    type: model
    role: subject
    cardinality: one
    optional: false
  - slot: extraction
    type: finding
    role: context
    cardinality: one
    optional: false
  - slot: hypothesis_space
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  - slot: effective_testing
    type: appraisal
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: final_trace
    type: model
    role: result
    cardinality: one
    optional: false
  - slot: mechanism_audit_resolution
    type: finding
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.19` — Synthesize process-tracing result

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.19
  verb: synthesize
  label: Synthesize process-tracing result
  inputs:
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    hypotheses:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    testing:
      type: appraisal
      cardinality: '1'
      optional: false
    comparative_support:
      type: estimate
      cardinality: '1'
      optional: false
    absence:
      type: diagnostic_item
      cardinality: '1'
      optional: false
    diagnostic_matrix:
      type: diagnostic_item
      cardinality: '1'
      optional: false
    mechanism_trace:
      type: model
      cardinality: '1'
      optional: false
  outputs:
    synthesis:
      type: finding
      cardinality: '1'
      optional: false
    evidence_development_agenda:
      type: gap
      cardinality: 0..*
      optional: false
  parameters: &id001
  - analyst_model
  - source_scope
  - terminal_repair_context
  preconditions: &id002
  - testing and mechanism artifacts accepted
  method_owned_semantics: &id003
  - verdicts
  - steelman cases
  - comparative narrative
  - limits
  - evidence-development agenda
  internal_method_phases:
  - state_rival_verdicts
  - steelman_alternatives
  - narrate_comparison
  - state_limits_and_gaps
  actor: analyst_llm_with_deterministic_verdict_calibration
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_synthesize.py:275-378
  - pt/pipeline.py:1470-1486
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.19
  verb: synthesize
  label: Synthesize process-tracing result
  workflow_role: integrate
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: extraction
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: hypotheses
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  - slot: testing
    type: appraisal
    role: context
    cardinality: one
    optional: false
  - slot: comparative_support
    type: estimate
    role: context
    cardinality: one
    optional: false
  - slot: absence
    type: diagnostic_item
    role: context
    cardinality: one
    optional: false
  - slot: diagnostic_matrix
    type: diagnostic_item
    role: context
    cardinality: one
    optional: false
  - slot: mechanism_trace
    type: model
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: synthesis
    type: finding
    role: result
    cardinality: one
    optional: false
  - slot: evidence_development_agenda
    type: gap
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Synthesize process-tracing result' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.20` — Run structural critic

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.20
  verb: review
  label: Run structural critic
  inputs:
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    hypotheses:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    testing:
      type: appraisal
      cardinality: '1'
      optional: false
    diagnostic_matrix:
      type: diagnostic_item
      cardinality: '1'
      optional: false
    absence:
      type: diagnostic_item
      cardinality: '1'
      optional: false
  outputs:
    critic_result:
      type: review_event
      cardinality: '1'
      optional: false
  parameters: &id001
  - critic_model
  preconditions: &id002
  - critic enabled
  - refinement disabled
  method_owned_semantics: &id003
  - structural and likelihood-claim problems; critic cannot change numbers directly
  internal_method_phases: []
  actor: critic_llm
  optional: true
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_critic.py:35-139
  - pt/pipeline.py:2118-2268
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.20
  verb: review
  label: Run structural critic
  workflow_role: appraise
  operation_kind: methodological_support
  actor_chain:
  - llm_engine
  inputs:
  - slot: extraction
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: hypotheses
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  - slot: testing
    type: appraisal
    role: context
    cardinality: one
    optional: false
  - slot: diagnostic_matrix
    type: diagnostic_item
    role: context
    cardinality: one
    optional: false
  - slot: absence
    type: diagnostic_item
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: critic_result
    type: review_event
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `pt.21` — Re-read revise and rerun

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.21
  verb: revise
  label: Re-read revise and rerun
  inputs:
    original_text:
      type: source_document
      cardinality: '1'
      optional: false
    extraction:
      type: finding
      cardinality: '1'
      optional: false
    hypotheses:
      type: rival_explanation
      cardinality: 1..*
      optional: false
    comparative_support:
      type: estimate
      cardinality: '1'
      optional: false
    absence:
      type: diagnostic_item
      cardinality: '1'
      optional: false
    synthesis:
      type: finding
      cardinality: '1'
      optional: false
  outputs:
    refinement:
      type: review_event
      cardinality: '1'
      optional: false
    revised_extraction:
      type: finding
      cardinality: 0..1
      optional: true
    revised_hypotheses:
      type: rival_explanation
      cardinality: 0..*
      optional: true
  parameters: &id001
  - analyst_model
  - grounding_repair_model
  - human_review_switch
  preconditions: &id002
  - refinement enabled
  - cached source and lineage integrity pass
  method_owned_semantics: &id003
  - missed evidence
  - reinterpretation
  - removals
  - causal-edge additions
  - hypothesis revision
  internal_method_phases:
  - reread
  - propose_delta
  - review_delta
  - rerun_affected_passes
  actor: analyst_llm_optional_human_and_deterministic_delta_application
  optional: true
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pass_refine.py:418-509
  - pt/apply_refinement.py:21-150
  - pt/pipeline.py:2305-2429
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.21
  verb: revise
  label: Re-read revise and rerun
  workflow_role: revise
  operation_kind: analytic
  actor_chain:
  - llm_engine
  - human_reviewer
  - deterministic_validator
  inputs:
  - slot: original_text
    type: source_document
    role: subject
    cardinality: one
    optional: false
  - slot: extraction
    type: finding
    role: context
    cardinality: one
    optional: false
  - slot: hypotheses
    type: rival_explanation
    role: context
    cardinality: many
    optional: false
  - slot: comparative_support
    type: estimate
    role: context
    cardinality: one
    optional: false
  - slot: absence
    type: diagnostic_item
    role: context
    cardinality: one
    optional: false
  - slot: synthesis
    type: finding
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: refinement
    type: review_event
    role: result
    cardinality: one
    optional: false
  - slot: revised_extraction
    type: finding
    role: result
    cardinality: optional_one
    optional: true
  - slot: revised_hypotheses
    type: rival_explanation
    role: result
    cardinality: optional_many
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Re-read revise and rerun' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.22` — Audit terminal claims and gate publication

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.22
  verb: review
  label: Audit terminal claims and gate publication
  inputs:
    final_artifacts:
      type: finding
      cardinality: 1..*
      optional: false
    terminal_prose_claims:
      type: claim
      cardinality: 1..*
      optional: false
  outputs:
    central_claim_review:
      type: review_event
      cardinality: '1'
      optional: false
    accepted_result:
      type: finding
      cardinality: 0..1
      optional: true
    blocked_prepublication_artifact:
      type: finding
      cardinality: 0..1
      optional: true
  parameters: &id001
  - review_model
  - worker_count
  preconditions: &id002
  - final mechanism and synthesis exist
  method_owned_semantics: &id003
  - whether each atomic final claim is entailed by exact evidence and analysis artifacts
  internal_method_phases:
  - atomize_claims
  - check_entailment
  - accept_or_block
  actor: independent_review_llms_with_deterministic_gate
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pipeline.py:2455-2528
  - pt/pass_central_claim_review.py:1081-1198
  - pt/report.py:54-79
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.22
  verb: review
  label: Audit terminal claims and gate publication
  workflow_role: appraise
  operation_kind: methodological_support
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: final_artifacts
    type: finding
    role: subject
    cardinality: many
    optional: false
  - slot: terminal_prose_claims
    type: claim
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: central_claim_review
    type: review_event
    role: result
    cardinality: one
    optional: false
  - slot: accepted_result
    type: finding
    role: result
    cardinality: optional_one
    optional: true
  - slot: blocked_prepublication_artifact
    type: finding
    role: result
    cardinality: optional_one
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt.23` — Persist result and publishable report

```yaml
legacy_workflow: pt_single_case_rival_explanation_v2
original_values:
  step_id: pt.23
  verb: project
  label: Persist result and publishable report
  inputs:
    accepted_final_artifacts:
      type: finding
      cardinality: 1..*
      optional: false
  outputs:
    result_json:
      type: artifact_ref
      cardinality: '1'
      optional: false
    report_html:
      type: artifact_ref
      cardinality: 0..1
      optional: true
  parameters: &id001
  - json_only
  preconditions: &id002
  - terminal review accepted for HTML
  method_owned_semantics: &id003
  - presentation preserves comparative-support and source-limit meanings
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/pipeline.py:2483-2513
  - pt/cli.py:510-560
assigned_rev5_values:
  method_id: pt_core_rival_explanation
  step_id: pt.23
  verb: project
  label: Persist result and publishable report
  workflow_role: communicate
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: accepted_final_artifacts
    type: finding
    role: subject
    cardinality: many
    optional: false
  outputs:
  - slot: result_json
    type: artifact_ref
    role: result
    cardinality: one
    optional: false
  - slot: report_html
    type: artifact_ref
    role: result
    cardinality: optional_one
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'not method-specified; engineering. Bennett & Checkel (2015), Process Tracing: From Metaphor to Analytic Tool; Fairfield & Charman (2017), Political Analysis 25(3).'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `pt_acq.01` — Freeze baseline and acquisition agenda

```yaml
legacy_workflow: pt_acquisition_companion
original_values:
  step_id: pt_acq.01
  verb: construct
  label: Freeze baseline and acquisition agenda
  inputs:
    baseline_result:
      type: finding
      cardinality: '1'
      optional: false
    source_packet:
      type: dataset
      cardinality: '1'
      optional: false
  outputs:
    acquisition_session:
      type: configuration
      cardinality: '1'
      optional: false
    acquisition_plan:
      type: gap
      cardinality: '1'
      optional: false
  parameters: &id001
  - max_targets
  preconditions: &id002
  - hypotheses and partition audit exist
  - packet question matches
  method_owned_semantics: &id003
  - source gaps
  - damaging absences
  - sensitive discriminators
  - driver corroboration needs
  internal_method_phases:
  - freeze_baseline
  - rank_source_needs
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/acquisition_session.py:555-626
  - pt/source_acquisition.py:226-266
assigned_rev5_values:
  method_id: pt_source_acquisition
  step_id: pt_acq.01
  verb: construct
  label: Freeze baseline and acquisition agenda
  workflow_role: conceptualize
  operation_kind: analytic
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: baseline_result
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: source_packet
    type: dataset
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: acquisition_session
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: acquisition_plan
    type: gap
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Freeze baseline and acquisition agenda' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Page et al. (2021), PRISMA 2020 statement; Howell & Prevenier (2001), From Reliable Sources.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt_acq.02` — Retrieve candidates for target

```yaml
legacy_workflow: pt_acquisition_companion
original_values:
  step_id: pt_acq.02
  verb: retrieve
  label: Retrieve candidates for target
  inputs:
    acquisition_session:
      type: configuration
      cardinality: '1'
      optional: false
    target_id:
      type: gap
      cardinality: '1'
      optional: false
    query_configuration:
      type: configuration
      cardinality: '1'
      optional: false
  outputs:
    retrieval_attempts:
      type: review_event
      cardinality: 1..*
      optional: false
    retrieved_candidates:
      type: source_document
      cardinality: 0..*
      optional: false
  parameters: &id001
  - providers
  - top_k
  - queries_per_action
  - timeout
  preconditions: &id002
  - frozen baseline unchanged
  - action known
  - session unevaluated
  method_owned_semantics: &id003 []
  internal_method_phases:
  - query
  - retrieve
  - record_failures_and_candidates
  actor: retrieval_service_and_deterministic_ledger
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/acquisition_session.py:637-758
  - pt/acquisition_session.py:761-887
  - pt/acquisition_session.py:890-1017
assigned_rev5_values:
  method_id: pt_source_acquisition
  step_id: pt_acq.02
  verb: retrieve
  label: Retrieve candidates for target
  workflow_role: acquire
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  - deterministic_validator
  inputs:
  - slot: acquisition_session
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  - slot: target_id
    type: gap
    role: context
    cardinality: one
    optional: false
  - slot: query_configuration
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  outputs:
  - slot: retrieval_attempts
    type: review_event
    role: result
    cardinality: many
    optional: false
  - slot: retrieved_candidates
    type: source_document
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Page et al. (2021), PRISMA 2020 statement; Howell & Prevenier (2001), From Reliable Sources.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `pt_acq.03` — Review and admit candidate source

```yaml
legacy_workflow: pt_acquisition_companion
original_values:
  step_id: pt_acq.03
  verb: appraise_source
  label: Review and admit candidate source
  inputs:
    candidate:
      type: source_document
      cardinality: '1'
      optional: false
    review_request:
      type: review_protocol
      cardinality: '1'
      optional: false
  outputs:
    candidate_review:
      type: review_event
      cardinality: '1'
      optional: false
    admitted_source:
      type: source_document
      cardinality: 0..1
      optional: true
  parameters: &id001
  - disposition
  - source_class
  - provenance_fit
  - duplication_assessment
  - optional_text_selection
  preconditions: &id002
  - candidate exists and is not admitted
  - reviewer acknowledges fit rather than favorable content
  method_owned_semantics: &id003
  - provenance relevance
  - novelty
  - usable source body
  - admission judgment
  internal_method_phases:
  - assess_fit
  - assess_novelty
  - admit_reject_or_defer
  actor: human_with_deterministic_validation
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - pt/acquisition_session.py:1055-1206
assigned_rev5_values:
  method_id: pt_source_acquisition
  step_id: pt_acq.03
  verb: appraise_source
  label: Review and admit candidate source
  workflow_role: appraise
  operation_kind: analytic
  actor_chain:
  - human_reviewer
  - deterministic_validator
  inputs:
  - slot: candidate
    type: source_document
    role: subject
    cardinality: one
    optional: false
  - slot: review_request
    type: review_protocol
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: candidate_review
    type: review_event
    role: result
    cardinality: one
    optional: false
  - slot: admitted_source
    type: source_document
    role: result
    cardinality: optional_one
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Review and admit candidate source' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Page et al. (2021), PRISMA 2020 statement; Howell & Prevenier (2001), From Reliable Sources.
  execution_status: manually_performed
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
- This executable boundary bundles multiple rev-5 ideal operations; one operation_kind cannot express the mixed internal semantics without splitting the observed boundary. The assignment follows the primary analytic act and is lossy.
- Legacy executable means the admission endpoint and validator are callable, not that software performs provenance-fit, duplication, or admission judgment; rev 5 therefore assigns manually_performed.
```

### `pt_acq.04` — Test frozen rivals on admitted evidence

```yaml
legacy_workflow: pt_acquisition_companion
original_values:
  step_id: pt_acq.04
  verb: test
  label: Test frozen rivals on admitted evidence
  inputs:
    acquisition_session:
      type: configuration
      cardinality: '1'
      optional: false
    admitted_sources:
      type: source_document
      cardinality: 1..*
      optional: false
  outputs:
    held_out_evaluation:
      type: finding
      cardinality: '1'
      optional: false
  parameters: &id001
  - model
  - discriminator_audit_model
  - retry_budget
  preconditions: &id002
  - baseline unchanged
  - all retained candidates dispositioned
  - at least one unique admitted source
  method_owned_semantics: &id003
  - targeted selection-reviewed reassessment of frozen rivals on newly admitted text
  internal_method_phases:
  - assemble_held_out_corpus
  - run_pt_testing_and_synthesis
  - compare_support
  actor: deterministic_orchestration_and_pt_llms
  optional: false
  repeatable: false
  implementation_status: incomplete
  evidence_basis:
  - code
  source_refs: &id004
  - pt/acquisition_session.py:1209-1378
  - pt/acquisition_session.py:1296-1319
  - pt/pipeline.py:1488-1498
  implementation_note: Current caller unpacks eight outputs from a function that returns nine.
assigned_rev5_values:
  method_id: pt_source_acquisition
  step_id: pt_acq.04
  verb: test
  label: Test frozen rivals on admitted evidence
  workflow_role: appraise
  operation_kind: analytic
  actor_chain:
  - deterministic_engine
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: acquisition_session
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  - slot: admitted_sources
    type: source_document
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: held_out_evaluation
    type: finding
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Test frozen rivals on admitted evidence' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Page et al. (2021), PRISMA 2020 statement; Howell & Prevenier (2001), From Reliable Sources.
  execution_status: incomplete_software
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
- implementation_note has no rev-5 field; preserved only in original_values.
```

### `tf.01` — Render paper into text

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.01
  verb: extract
  label: Render paper into text
  inputs:
    paper_pdf:
      type: source_document
      cardinality: '1'
      optional: false
  outputs:
    paper_text:
      type: source_document
      cardinality: '1'
      optional: false
    fulltext_file:
      type: artifact_ref
      cardinality: 0..1
      optional: true
  parameters: &id001
  - save_fulltext
  - output_dir
  preconditions: &id002
  - readable PDF
  - pypdf or system pdftotext available
  method_owned_semantics: &id003 []
  internal_method_phases:
  - extract_page_text
  - preserve_page_boundaries
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/extraction/extractor_single.py:329-379
  - src/theory_forge/extraction/extractor_single.py:473-503
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.01
  verb: extract
  label: Render paper into text
  workflow_role: analyze
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: paper_pdf
    type: source_document
    role: subject
    cardinality: one
    optional: false
  outputs:
  - slot: paper_text
    type: source_document
    role: result
    cardinality: one
    optional: false
  - slot: fulltext_file
    type: artifact_ref
    role: result
    cardinality: optional_one
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf.02` — Identify theories in paper

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.02
  verb: extract
  label: Identify theories in paper
  inputs:
    paper_text:
      type: source_document
      cardinality: '1'
      optional: false
    paper_title:
      type: configuration
      cardinality: '1'
      optional: false
  outputs:
    theory_identification:
      type: theory
      cardinality: 1..*
      optional: false
  parameters: &id001
  - extraction_model
  - single_or_multi_mode
  preconditions: &id002
  - paper text is nonempty
  method_owned_semantics: &id003
  - what counts as the primary theory or a distinct theory
  internal_method_phases:
  - identify_primary_or_multiple_theories
  actor: llm_with_typed_validation
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/extraction/extractor_single.py:382-406
  - src/theory_forge/extraction/extractor_multi.py:42-66
  - src/theory_forge/extraction/extractor_multi.py:127-149
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.02
  verb: extract
  label: Identify theories in paper
  workflow_role: analyze
  operation_kind: runtime_delivery
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: paper_text
    type: source_document
    role: subject
    cardinality: one
    optional: false
  - slot: paper_title
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  outputs:
  - slot: theory_identification
    type: theory
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
- The step contains interpretive judgment, but rev 5.1 directs the unsourced compile/apply workflow to runtime_delivery; no frozen methodology source licenses an analytic classification.
```

### `tf.03` — Extract structured theory schema

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.03
  verb: extract
  label: Extract structured theory schema
  inputs:
    paper_text:
      type: source_document
      cardinality: '1'
      optional: false
    theory_identification:
      type: theory
      cardinality: 1..*
      optional: false
  outputs:
    theory_schema:
      type: theory
      cardinality: 1..*
      optional: false
  parameters: &id001
  - prompt
  - extraction_model
  - schema_mode
  preconditions: &id002
  - theory identification validates
  method_owned_semantics: &id003
  - mechanisms
  - constructs
  - categories
  - operations
  - uncertainty
  - validation interpretation
  internal_method_phases:
  - extract_constructs
  - extract_mechanisms
  - extract_operations
  - record_uncertainty_and_validation
  actor: llm_with_typed_validation
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/extraction/extractor_single.py:409-470
  - src/theory_forge/extraction/extractor_multi.py:69-104
  - src/theory_forge/extraction/extractor_multi.py:151-171
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.03
  verb: extract
  label: Extract structured theory schema
  workflow_role: analyze
  operation_kind: runtime_delivery
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: paper_text
    type: source_document
    role: subject
    cardinality: one
    optional: false
  - slot: theory_identification
    type: theory
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: theory_schema
    type: theory
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
- The step contains interpretive judgment, but rev 5.1 directs the unsourced compile/apply workflow to runtime_delivery; no frozen methodology source licenses an analytic classification.
```

### `tf.04` — Persist extraction artifacts

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.04
  verb: construct
  label: Persist extraction artifacts
  inputs:
    theory_schema:
      type: theory
      cardinality: 1..*
      optional: false
    extraction_metadata:
      type: configuration
      cardinality: '1'
      optional: false
  outputs:
    theory_artifacts:
      type: artifact_ref
      cardinality: 1..*
      optional: false
    identification_artifact:
      type: artifact_ref
      cardinality: '1'
      optional: false
    summary_artifact:
      type: artifact_ref
      cardinality: '1'
      optional: false
  parameters: &id001
  - output_directory
  - fulltext_retention
  preconditions: &id002
  - extraction completed
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/extraction/extractor_single.py:514-556
  - src/theory_forge/extraction/extractor_multi.py:146-207
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.04
  verb: construct
  label: Persist extraction artifacts
  workflow_role: conceptualize
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: theory_schema
    type: theory
    role: subject
    cardinality: many
    optional: false
  - slot: extraction_metadata
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  outputs:
  - slot: theory_artifacts
    type: artifact_ref
    role: result
    cardinality: many
    optional: false
  - slot: identification_artifact
    type: artifact_ref
    role: result
    cardinality: one
    optional: false
  - slot: summary_artifact
    type: artifact_ref
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `tf.05` — Validate theory schema

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.05
  verb: test
  label: Validate theory schema
  inputs:
    theory_schema:
      type: theory
      cardinality: '1'
      optional: false
    meta_schema:
      type: configuration
      cardinality: '1'
      optional: false
  outputs:
    validated_theory_schema:
      type: theory
      cardinality: '1'
      optional: false
  parameters: &id001
  - default_meta_schema_v14
  preconditions: &id002
  - schema artifact exists
  method_owned_semantics: &id003
  - v14 structural validity
  - not theoretical correctness
  internal_method_phases: []
  actor: deterministic_schema_validator
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/automation.py:330-357
  - src/theory_forge/cli.py:145-180
  - src/theory_forge/__init__.py:28-33
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.05
  verb: test
  label: Validate theory schema
  workflow_role: appraise
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_validator
  inputs:
  - slot: theory_schema
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: meta_schema
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  outputs:
  - slot: validated_theory_schema
    type: theory
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `tf.06` — Reuse or request compiled module

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.06
  verb: retrieve
  label: Reuse or request compiled module
  inputs:
    validated_theory_schema:
      type: theory
      cardinality: '1'
      optional: false
    compiled_modules:
      type: artifact_ref
      cardinality: 0..*
      optional: false
  outputs:
    compiled_module:
      type: artifact_ref
      cardinality: 0..1
      optional: true
    compile_request:
      type: configuration
      cardinality: 0..1
      optional: true
  parameters: &id001
  - force_recompile
  - compiled_directory
  preconditions: &id002
  - theory identity exists
  method_owned_semantics: &id003
  - whether a prior compiled operationalization represents the same theory
  internal_method_phases:
  - match_identity_and_hash
  - choose_reuse_or_compile
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/automation.py:211-302
  - src/theory_forge/automation.py:359-380
  - src/theory_forge/codegen/compiler.py:253-272
  - src/theory_forge/codegen/compiler.py:565-578
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.06
  verb: retrieve
  label: Reuse or request compiled module
  workflow_role: acquire
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: validated_theory_schema
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: compiled_modules
    type: artifact_ref
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: compiled_module
    type: artifact_ref
    role: result
    cardinality: optional_one
    optional: true
  - slot: compile_request
    type: configuration
    role: result
    cardinality: optional_one
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf.07` — Project theory into compiler artifacts

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.07
  verb: project
  label: Project theory into compiler artifacts
  inputs:
    theory_schema:
      type: theory
      cardinality: '1'
      optional: false
    pipeline_spec:
      type: configuration
      cardinality: 0..1
      optional: true
  outputs:
    extraction_model:
      type: model
      cardinality: '1'
      optional: false
    orchestration:
      type: configuration
      cardinality: '1'
      optional: false
    defaults:
      type: parameter_set
      cardinality: '1'
      optional: false
    prompts:
      type: configuration
      cardinality: 0..*
      optional: false
    computation_stubs:
      type: model
      cardinality: 0..*
      optional: false
    property_tests:
      type: review_protocol
      cardinality: 0..*
      optional: false
  parameters: &id001
  - handwritten_spec
  - auto_spec
  - direct_function_path
  preconditions: &id002
  - compilation not reused
  method_owned_semantics: &id003
  - mapping theory operations
  - constructs
  - algorithms
  - dependencies
  - and uncertainty into stages
  internal_method_phases:
  - derive_stage_plan
  - generate_models_and_stubs
  - generate_orchestration_and_tests
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/compiler.py:281-423
  - src/theory_forge/codegen/compiler.py:852-948
  - src/theory_forge/codegen/schema_to_spec.py:132-251
  - src/theory_forge/codegen/pipeline_spec.py:24-317
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.07
  verb: project
  label: Project theory into compiler artifacts
  workflow_role: communicate
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: theory_schema
    type: theory
    role: subject
    cardinality: one
    optional: false
  - slot: pipeline_spec
    type: configuration
    role: config_data
    cardinality: optional_one
    optional: true
  outputs:
  - slot: extraction_model
    type: model
    role: result
    cardinality: one
    optional: false
  - slot: orchestration
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: defaults
    type: parameter_set
    role: result
    cardinality: one
    optional: false
  - slot: prompts
    type: configuration
    role: result
    cardinality: many
    optional: false
  - slot: computation_stubs
    type: model
    role: result
    cardinality: many
    optional: false
  - slot: property_tests
    type: review_protocol
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf.08` — Enrich qualitative prompts

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.08
  verb: construct
  label: Enrich qualitative prompts
  inputs:
    generated_prompts:
      type: configuration
      cardinality: 1..*
      optional: false
    theory_mechanisms_and_operations:
      type: theory
      cardinality: '1'
      optional: false
  outputs:
    enriched_prompts:
      type: configuration
      cardinality: 0..*
      optional: false
  parameters: &id001
  - review_model
  preconditions: &id002
  - generated qualitative prompt files exist
  method_owned_semantics: &id003
  - mechanism-specific sections
  - counterinterpretations
  - observed-inferred distinctions
  internal_method_phases: []
  actor: llm
  optional: true
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/compiler.py:950-1138
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.08
  verb: construct
  label: Enrich qualitative prompts
  workflow_role: conceptualize
  operation_kind: runtime_delivery
  actor_chain:
  - llm_engine
  inputs:
  - slot: generated_prompts
    type: configuration
    role: config_data
    cardinality: many
    optional: false
  - slot: theory_mechanisms_and_operations
    type: theory
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: enriched_prompts
    type: configuration
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `tf.09` — Implement computation functions

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.09
  verb: construct
  label: Implement computation functions
  inputs:
    theory_algorithms:
      type: theory
      cardinality: 0..*
      optional: false
    computation_stubs:
      type: model
      cardinality: 0..*
      optional: false
    tests:
      type: review_protocol
      cardinality: 0..*
      optional: false
    existing_compute_source:
      type: model
      cardinality: 0..1
      optional: true
  outputs:
    implemented_compute_source:
      type: model
      cardinality: 0..1
      optional: true
  parameters: &id001
  - agent_model
  - max_turns
  - direct_legacy_or_ac8_path
  preconditions: &id002
  - compile support artifacts exist
  method_owned_semantics: &id003
  - translate formulas and procedures without changing theoretical meaning
  internal_method_phases:
  - implement_each_function
  actor: compilation_agent
  optional: true
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/compiler.py:1228-1384
  - src/theory_forge/codegen/compiler.py:1452-1483
  - src/theory_forge/codegen/compiler.py:1546-1799
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.09
  verb: construct
  label: Implement computation functions
  workflow_role: conceptualize
  operation_kind: runtime_delivery
  actor_chain:
  - llm_engine
  inputs:
  - slot: theory_algorithms
    type: theory
    role: subject
    cardinality: many
    optional: false
  - slot: computation_stubs
    type: model
    role: context
    cardinality: many
    optional: false
  - slot: tests
    type: review_protocol
    role: context
    cardinality: many
    optional: false
  - slot: existing_compute_source
    type: model
    role: context
    cardinality: optional_one
    optional: true
  outputs:
  - slot: implemented_compute_source
    type: model
    role: result
    cardinality: optional_one
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf.10` — Verify compiled module

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.10
  verb: test
  label: Verify compiled module
  inputs:
    compiled_files:
      type: model
      cardinality: 1..*
      optional: false
    property_tests:
      type: review_protocol
      cardinality: 0..*
      optional: false
    golden_tests:
      type: review_protocol
      cardinality: 0..*
      optional: false
    reviewer_probes:
      type: review_protocol
      cardinality: 0..*
      optional: false
  outputs:
    verification_result:
      type: appraisal
      cardinality: '1'
      optional: false
  parameters: &id001
  - probe_inclusion
  - pytest_timeout
  preconditions: &id002
  - required generated files and tests exist
  method_owned_semantics: &id003
  - narrowly coded executable and semantic conformance
  internal_method_phases:
  - run_tests
  - run_probes
  - classify_failure
  actor: deterministic_test_runner
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/compiler.py:2360-2471
  - src/theory_forge/codegen/golden_tests.py:62-200
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.10
  verb: test
  label: Verify compiled module
  workflow_role: appraise
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_validator
  inputs:
  - slot: compiled_files
    type: model
    role: subject
    cardinality: many
    optional: false
  - slot: property_tests
    type: review_protocol
    role: context
    cardinality: many
    optional: false
  - slot: golden_tests
    type: review_protocol
    role: context
    cardinality: many
    optional: false
  - slot: reviewer_probes
    type: review_protocol
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: verification_result
    type: appraisal
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf.11` — Heal failed compilation

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.11
  verb: revise
  label: Heal failed compilation
  inputs:
    failed_verification:
      type: appraisal
      cardinality: '1'
      optional: false
    compute_source:
      type: model
      cardinality: '1'
      optional: false
    theory_algorithm_context:
      type: theory
      cardinality: '1'
      optional: false
  outputs:
    revised_compiled_files:
      type: model
      cardinality: 1..*
      optional: false
  parameters: &id001
  - max_fix_attempts
  - per_function_or_monolithic_repair
  preconditions: &id002
  - verification failed
  - repair budget remains
  method_owned_semantics: &id003
  - classify implementation versus contract versus theory-operation failure
  internal_method_phases:
  - diagnose
  - revise
  actor: compilation_agent_and_diagnostic_llm
  optional: true
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/compiler.py:1341-1450
  - src/theory_forge/codegen/compiler.py:1464-1544
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.11
  verb: revise
  label: Heal failed compilation
  workflow_role: revise
  operation_kind: runtime_delivery
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: failed_verification
    type: appraisal
    role: subject
    cardinality: one
    optional: false
  - slot: compute_source
    type: model
    role: context
    cardinality: one
    optional: false
  - slot: theory_algorithm_context
    type: theory
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: revised_compiled_files
    type: model
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf.12` — Review and finalize compiled module

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.12
  verb: review
  label: Review and finalize compiled module
  inputs:
    verified_compiled_artifacts:
      type: model
      cardinality: 1..*
      optional: false
    theory_schema:
      type: theory
      cardinality: '1'
      optional: false
    verification_result:
      type: appraisal
      cardinality: '1'
      optional: false
  outputs:
    manifest:
      type: configuration
      cardinality: '1'
      optional: false
    compilation_review:
      type: review_event
      cardinality: 0..1
      optional: true
    compiled_module:
      type: artifact_ref
      cardinality: '1'
      optional: false
  parameters: &id001
  - review
  - agent_review
  - reviewer_model
  preconditions: &id002
  - compile route returned verification result
  method_owned_semantics: &id003
  - theoretical fidelity
  - defaults
  - edge cases
  - configurable completeness
  internal_method_phases:
  - build_manifest
  - optional_review
  actor: deterministic_software_and_optional_llm_or_agent_reviewer
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/compiler.py:467-563
  - src/theory_forge/codegen/compiler.py:2207-2358
  - src/theory_forge/codegen/manifest.py:280-377
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.12
  verb: review
  label: Review and finalize compiled module
  workflow_role: appraise
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  - llm_engine
  - human_reviewer
  inputs:
  - slot: verified_compiled_artifacts
    type: model
    role: subject
    cardinality: many
    optional: false
  - slot: theory_schema
    type: theory
    role: context
    cardinality: one
    optional: false
  - slot: verification_result
    type: appraisal
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: manifest
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: compilation_review
    type: review_event
    role: result
    cardinality: optional_one
    optional: true
  - slot: compiled_module
    type: artifact_ref
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf.13` — Load compiled theory

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.13
  verb: retrieve
  label: Load compiled theory
  inputs:
    compiled_module:
      type: artifact_ref
      cardinality: '1'
      optional: false
  outputs:
    loaded_pipeline:
      type: model
      cardinality: '1'
      optional: false
  parameters: &id001
  - compiled_directory
  preconditions: &id002
  - manifest exists
  - referenced modules and contracts load
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/runner.py:211-277
  - src/theory_forge/codegen/runner.py:954-1133
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.13
  verb: retrieve
  label: Load compiled theory
  workflow_role: acquire
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: compiled_module
    type: artifact_ref
    role: subject
    cardinality: one
    optional: false
  outputs:
  - slot: loaded_pipeline
    type: model
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `tf.14` — Extract theory parameters from new text

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.14
  verb: extract
  label: Extract theory parameters from new text
  inputs:
    analysis_text:
      type: source_document
      cardinality: '1'
      optional: false
    compiled_extraction_model:
      type: model
      cardinality: '1'
      optional: false
  outputs:
    extracted_parameters:
      type: evidence_item
      cardinality: '1'
      optional: false
  parameters: &id001
  - extraction_model
  - structured_output_fallback_model
  preconditions: &id002
  - compiled extraction model loaded
  method_owned_semantics: &id003
  - what in the new text instantiates the theory constructs
  internal_method_phases:
  - extract_and_validate_construct_instantiations
  actor: runtime_llm_with_typed_validation
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/runner.py:434-596
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.14
  verb: extract
  label: Extract theory parameters from new text
  workflow_role: analyze
  operation_kind: runtime_delivery
  actor_chain:
  - llm_engine
  - deterministic_validator
  inputs:
  - slot: analysis_text
    type: source_document
    role: subject
    cardinality: one
    optional: false
  - slot: compiled_extraction_model
    type: model
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: extracted_parameters
    type: evidence_item
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf.15` — Execute deterministic theory transformations

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.15
  verb: derive
  label: Execute deterministic theory transformations
  inputs:
    extracted_parameters:
      type: evidence_item
      cardinality: '1'
      optional: false
    prior_stage_results:
      type: finding
      cardinality: 0..*
      optional: false
    defaults:
      type: parameter_set
      cardinality: '1'
      optional: false
    computation_function:
      type: model
      cardinality: '1'
      optional: false
  outputs:
    computed_result:
      type: finding
      cardinality: 0..*
      optional: false
  parameters: &id001
  - orchestration_spec
  - dotpaths
  - defaults
  - per_item_or_group_mode
  preconditions: &id002
  - computation stage exists
  - inputs resolve
  method_owned_semantics: &id003
  - theory-specific formula or procedure
  internal_method_phases:
  - resolve_inputs
  - execute_function
  actor: deterministic_safe_executor
  optional: true
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/runner.py:605-785
  - src/theory_forge/codegen/runner.py:1352-1444
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.15
  verb: derive
  label: Execute deterministic theory transformations
  workflow_role: analyze
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  - deterministic_validator
  inputs:
  - slot: extracted_parameters
    type: evidence_item
    role: subject
    cardinality: one
    optional: false
  - slot: prior_stage_results
    type: finding
    role: context
    cardinality: many
    optional: false
  - slot: defaults
    type: parameter_set
    role: context
    cardinality: one
    optional: false
  - slot: computation_function
    type: model
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: computed_result
    type: finding
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf.16` — Check runtime invariants

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.16
  verb: test
  label: Check runtime invariants
  inputs:
    computed_result:
      type: finding
      cardinality: '1'
      optional: false
    stage_invariants:
      type: criterion
      cardinality: 1..*
      optional: false
  outputs:
    invariant_violations:
      type: uncertainty_note
      cardinality: 0..*
      optional: false
    updated_manifest_health:
      type: review_event
      cardinality: '1'
      optional: false
  parameters: &id001
  - invariant_expressions
  preconditions: &id002
  - stage manifest contains invariants
  method_owned_semantics: &id003
  - acceptable range
  - type
  - or state for the theory operation
  internal_method_phases: []
  actor: deterministic_software
  optional: true
  repeatable: true
  implementation_status: incomplete
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/runner.py:354-371
  - src/theory_forge/codegen/runner.py:1255-1312
  - src/theory_forge/codegen/compiler.py:2473-2567
  implementation_note: Checker exists, but ordinary stage discovery does not copy schema invariants into StageSpec.
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.16
  verb: test
  label: Check runtime invariants
  workflow_role: appraise
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: computed_result
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: stage_invariants
    type: criterion
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: invariant_violations
    type: uncertainty_note
    role: result
    cardinality: many
    optional: false
  - slot: updated_manifest_health
    type: review_event
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: incomplete_software
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- implementation_note has no rev-5 field; preserved only in original_values.
```

### `tf.17` — Produce qualitative theory interpretation

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.17
  verb: synthesize
  label: Produce qualitative theory interpretation
  inputs:
    source_text:
      type: source_document
      cardinality: '1'
      optional: false
    extracted_parameters:
      type: evidence_item
      cardinality: '1'
      optional: false
    computed_results:
      type: finding
      cardinality: 0..*
      optional: false
    prior_qualitative_outputs:
      type: finding
      cardinality: 0..*
      optional: false
    theory_anchor:
      type: theory
      cardinality: '1'
      optional: false
  outputs:
    qualitative_analysis:
      type: finding
      cardinality: 0..*
      optional: false
  parameters: &id001
  - model
  - temperature
  - rigor_profile
  - compiled_prompt
  preconditions: &id002
  - qualitative stage and prompt exist
  method_owned_semantics: &id003
  - theory-grounded interpretation
  - counterinterpretations
  - uncertainty
  - falsifiable checks
  internal_method_phases:
  - interpret_with_theory
  - consider_alternatives
  - state_uncertainty_and_checks
  actor: runtime_llm
  optional: true
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/runner.py:787-929
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.17
  verb: synthesize
  label: Produce qualitative theory interpretation
  workflow_role: integrate
  operation_kind: runtime_delivery
  actor_chain:
  - llm_engine
  inputs:
  - slot: source_text
    type: source_document
    role: subject
    cardinality: one
    optional: false
  - slot: extracted_parameters
    type: evidence_item
    role: context
    cardinality: one
    optional: false
  - slot: computed_results
    type: finding
    role: context
    cardinality: many
    optional: false
  - slot: prior_qualitative_outputs
    type: finding
    role: context
    cardinality: many
    optional: false
  - slot: theory_anchor
    type: theory
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: qualitative_analysis
    type: finding
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf.18` — Review runtime analysis quality

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.18
  verb: review
  label: Review runtime analysis quality
  inputs:
    input_text:
      type: source_document
      cardinality: '1'
      optional: false
    analysis_outputs:
      type: finding
      cardinality: 1..*
      optional: false
    theory_summary:
      type: theory
      cardinality: '1'
      optional: false
  outputs:
    quality_assessment:
      type: review_event
      cardinality: 0..1
      optional: true
  parameters: &id001
  - review_output
  - review_model
  preconditions: &id002
  - analysis result assembled
  method_owned_semantics: &id003
  - evidence grounding
  - construct operationalization
  - theoretical depth
  - epistemic rigor
  internal_method_phases: []
  actor: llm_reviewer
  optional: true
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/runner.py:414-420
  - src/theory_forge/codegen/runner.py:1150-1248
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.18
  verb: review
  label: Review runtime analysis quality
  workflow_role: appraise
  operation_kind: runtime_delivery
  actor_chain:
  - llm_engine
  inputs:
  - slot: input_text
    type: source_document
    role: subject
    cardinality: one
    optional: false
  - slot: analysis_outputs
    type: finding
    role: context
    cardinality: many
    optional: false
  - slot: theory_summary
    type: theory
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: quality_assessment
    type: review_event
    role: result
    cardinality: optional_one
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: true
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `tf.19` — Assemble and persist analysis report

```yaml
legacy_workflow: theory_forge_v14_compile_apply
original_values:
  step_id: tf.19
  verb: construct
  label: Assemble and persist analysis report
  inputs:
    stage_results:
      type: finding
      cardinality: 1..*
      optional: false
    confidence_estimate:
      type: uncertainty_note
      cardinality: '1'
      optional: false
    quality_review:
      type: review_event
      cardinality: 0..1
      optional: true
  outputs:
    analysis_result:
      type: finding
      cardinality: '1'
      optional: false
    analysis_artifact:
      type: artifact_ref
      cardinality: '1'
      optional: false
    automation_report:
      type: artifact_ref
      cardinality: '1'
      optional: false
  parameters: &id001
  - output_directory
  preconditions: &id002
  - analysis attempt reached result assembly
  method_owned_semantics: &id003
  - stage success remains visible rather than becoming a global substantive conclusion
  internal_method_phases: []
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/codegen/runner.py:403-430
  - src/theory_forge/automation.py:411-445
assigned_rev5_values:
  method_id: theory_forge_compile_apply
  step_id: tf.19
  verb: construct
  label: Assemble and persist analysis report
  workflow_role: conceptualize
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: stage_results
    type: finding
    role: subject
    cardinality: many
    optional: false
  - slot: confidence_estimate
    type: uncertainty_note
    role: context
    cardinality: one
    optional: false
  - slot: quality_review
    type: review_event
    role: context
    cardinality: optional_one
    optional: true
  outputs:
  - slot: analysis_result
    type: finding
    role: result
    cardinality: one
    optional: false
  - slot: analysis_artifact
    type: artifact_ref
    role: result
    cardinality: one
    optional: false
  - slot: automation_report
    type: artifact_ref
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. No frozen authoritative methodology source; engineering workflow by rev 5.1 instruction.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `tf_cpt.01` — Fetch or verify pinned dataset

```yaml
legacy_workflow: theory_forge_cpt_choices13k_prediction
original_values:
  step_id: tf_cpt.01
  verb: acquire
  label: Fetch or verify pinned dataset
  inputs:
    dataset_spec:
      type: configuration
      cardinality: '1'
      optional: false
    local_dataset_files:
      type: source_document
      cardinality: 0..2
      optional: true
  outputs:
    verified_dataset_files:
      type: source_document
      cardinality: '2'
      optional: false
    dataset_digests:
      type: artifact_digest
      cardinality: '2'
      optional: false
  parameters: &id001
  - fetch_missing
  preconditions: &id002
  - repository commit and file digests are pinned
  method_owned_semantics: &id003 []
  internal_method_phases:
  - fetch_missing_without_overwrite
  - verify_digests
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/choices13k.py:31-148
  - scripts/run_choices13k_cpt.py:80-88
assigned_rev5_values:
  method_id: theory_forge_cpt_choices13k
  step_id: tf_cpt.01
  verb: acquire
  label: Fetch or verify pinned dataset
  workflow_role: acquire
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: dataset_spec
    type: configuration
    role: config_data
    cardinality: one
    optional: false
  - slot: local_dataset_files
    type: source_document
    role: context
    cardinality: optional_many
    optional: true
  outputs:
  - slot: verified_dataset_files
    type: source_document
    role: result
    cardinality: many
    optional: false
  - slot: dataset_digests
    type: artifact_digest
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Tversky & Kahneman (1992), Journal of Risk and Uncertainty 5; Peterson et al. (2021), Science 372.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf_cpt.02` — Screen declared eligible rows

```yaml
legacy_workflow: theory_forge_cpt_choices13k_prediction
original_values:
  step_id: tf_cpt.02
  verb: screen
  label: Screen declared eligible rows
  inputs:
    verified_dataset_files:
      type: source_document
      cardinality: '2'
      optional: false
    eligibility_criteria:
      type: criterion
      cardinality: 1..*
      optional: false
  outputs:
    eligible_rows:
      type: dataset
      cardinality: 0..*
      optional: false
    exclusions:
      type: screening_decision
      cardinality: 0..*
      optional: false
  parameters: &id001
  - no_feedback
  - no_ambiguity
  - maximum_two_outcomes
  - valid_probability_mass
  preconditions: &id002
  - CSV and JSON row counts reconcile
  - required columns and A/B options validate
  method_owned_semantics: &id003
  - eligibility of a choice problem for this source-correct CPT comparison
  internal_method_phases:
  - parse_inputs
  - apply_criteria
  - preserve_exclusion_reasons
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/choices13k.py:242-325
assigned_rev5_values:
  method_id: theory_forge_cpt_choices13k
  step_id: tf_cpt.02
  verb: screen
  label: Screen declared eligible rows
  workflow_role: acquire
  operation_kind: methodological_support
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: verified_dataset_files
    type: source_document
    role: subject
    cardinality: many
    optional: false
  - slot: eligibility_criteria
    type: criterion
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: eligible_rows
    type: dataset
    role: result
    cardinality: many
    optional: false
  - slot: exclusions
    type: screening_decision
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Tversky & Kahneman (1992), Journal of Risk and Uncertainty 5; Peterson et al. (2021), Science 372.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf_cpt.03` — Normalize eligible choice row

```yaml
legacy_workflow: theory_forge_cpt_choices13k_prediction
original_values:
  step_id: tf_cpt.03
  verb: construct
  label: Normalize eligible choice row
  inputs:
    eligible_row:
      type: dataset
      cardinality: '1'
      optional: false
  outputs:
    normalized_choice_row:
      type: dataset
      cardinality: '1'
      optional: false
    observed_majority:
      type: finding
      cardinality: '1'
      optional: false
  parameters: &id001
  - reference_point
  preconditions: &id002
  - options and observed B rate are valid
  method_owned_semantics: &id003
  - lottery normalization and observed majority rule
  internal_method_phases:
  - normalize_lotteries
  - derive_observed_majority
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/choices13k.py:307-340
assigned_rev5_values:
  method_id: theory_forge_cpt_choices13k
  step_id: tf_cpt.03
  verb: construct
  label: Normalize eligible choice row
  workflow_role: conceptualize
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: eligible_row
    type: dataset
    role: subject
    cardinality: one
    optional: false
  outputs:
  - slot: normalized_choice_row
    type: dataset
    role: result
    cardinality: one
    optional: false
  - slot: observed_majority
    type: finding
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Tversky & Kahneman (1992), Journal of Risk and Uncertainty 5; Peterson et al. (2021), Science 372.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf_cpt.04` — Compute and compare row predictions

```yaml
legacy_workflow: theory_forge_cpt_choices13k_prediction
original_values:
  step_id: tf_cpt.04
  verb: derive
  label: Compute and compare row predictions
  inputs:
    normalized_choice_row:
      type: dataset
      cardinality: '1'
      optional: false
    cpt_parameters:
      type: parameter_set
      cardinality: '1'
      optional: false
  outputs:
    cpt_prediction:
      type: forecast
      cardinality: '1'
      optional: false
    expected_value_prediction:
      type: forecast
      cardinality: '1'
      optional: false
    row_comparison_category:
      type: finding
      cardinality: '1'
      optional: false
  parameters: &id001
  - cpt_value_function
  - weighting_function
  - choice_rule
  preconditions: &id002
  - row eligible and normalized
  method_owned_semantics: &id003
  - CPT and expected-value model equations and tie handling
  internal_method_phases:
  - compute_cpt_values
  - compute_expected_values
  - choose_predictions
  - compare_with_observation
  actor: deterministic_model
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/choices13k.py:326-358
  - src/theory_forge/cumulative_prospect.py:26-239
assigned_rev5_values:
  method_id: theory_forge_cpt_choices13k
  step_id: tf_cpt.04
  verb: derive
  label: Compute and compare row predictions
  workflow_role: analyze
  operation_kind: analytic
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: normalized_choice_row
    type: dataset
    role: subject
    cardinality: one
    optional: false
  - slot: cpt_parameters
    type: parameter_set
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: cpt_prediction
    type: forecast
    role: result
    cardinality: one
    optional: false
  - slot: expected_value_prediction
    type: forecast
    role: result
    cardinality: one
    optional: false
  - slot: row_comparison_category
    type: finding
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Compute and compare row predictions' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Tversky & Kahneman (1992), Journal of Risk and Uncertainty 5; Peterson et al. (2021), Science 372.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
- This executable boundary bundles multiple rev-5 ideal operations; one operation_kind cannot express the mixed internal semantics without splitting the observed boundary. The assignment follows the primary analytic act and is lossy.
```

### `tf_cpt.05` — Aggregate model comparison

```yaml
legacy_workflow: theory_forge_cpt_choices13k_prediction
original_values:
  step_id: tf_cpt.05
  verb: aggregate
  label: Aggregate model comparison
  inputs:
    scored_rows:
      type: dataset
      cardinality: 0..*
      optional: false
    exclusions:
      type: screening_decision
      cardinality: 0..*
      optional: false
  outputs:
    prediction_summary:
      type: estimate
      cardinality: '1'
      optional: false
    category_counts:
      type: measure
      cardinality: '1'
      optional: false
    representative_cases:
      type: case_set
      cardinality: '1'
      optional: false
  parameters: &id001
  - paired_common_scored_rows
  - representative_case_rules
  preconditions: &id002
  - eligible and excluded rows reconcile to source rows
  method_owned_semantics: &id003
  - accuracy denominator
  - tie exclusion
  - representative disagreement categories
  internal_method_phases:
  - summarize_each_model
  - create_paired_comparison
  - select_representatives
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/choices13k.py:159-239
  - src/theory_forge/choices13k.py:360-414
assigned_rev5_values:
  method_id: theory_forge_cpt_choices13k
  step_id: tf_cpt.05
  verb: aggregate
  label: Aggregate model comparison
  workflow_role: analyze
  operation_kind: analytic
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: scored_rows
    type: dataset
    role: subject
    cardinality: many
    optional: false
  - slot: exclusions
    type: screening_decision
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: prediction_summary
    type: estimate
    role: result
    cardinality: one
    optional: false
  - slot: category_counts
    type: measure
    role: result
    cardinality: one
    optional: false
  - slot: representative_cases
    type: case_set
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Aggregate model comparison' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: Tversky & Kahneman (1992), Journal of Risk and Uncertainty 5; Peterson et al. (2021), Science 372.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `tf_cpt.06` — Write prediction evidence reports

```yaml
legacy_workflow: theory_forge_cpt_choices13k_prediction
original_values:
  step_id: tf_cpt.06
  verb: project
  label: Write prediction evidence reports
  inputs:
    prediction_analysis:
      type: finding
      cardinality: '1'
      optional: false
    producer_revision:
      type: artifact_ref
      cardinality: '1'
      optional: false
    theory_schema_digest:
      type: artifact_digest
      cardinality: '1'
      optional: false
  outputs:
    full_report:
      type: artifact_ref
      cardinality: '2'
      optional: false
    compact_evidence_report:
      type: artifact_ref
      cardinality: 0..2
      optional: true
  parameters: &id001
  - output_directory
  - optional_evidence_directory
  preconditions: &id002
  - compact export requires producer revision and theory-schema digest
  method_owned_semantics: &id003
  - reports preserve selection denominator
  - comparison limits
  - and nonclaims
  internal_method_phases:
  - render_markdown
  - write_full_private_output
  - optionally_write_compact_evidence
  actor: deterministic_software
  optional: false
  repeatable: false
  implementation_status: executable
  evidence_basis:
  - code
  source_refs: &id004
  - src/theory_forge/choices13k.py:417-574
  - scripts/run_choices13k_cpt.py:89-113
assigned_rev5_values:
  method_id: theory_forge_cpt_choices13k
  step_id: tf_cpt.06
  verb: project
  label: Write prediction evidence reports
  workflow_role: communicate
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: prediction_analysis
    type: finding
    role: subject
    cardinality: one
    optional: false
  - slot: producer_revision
    type: artifact_ref
    role: context
    cardinality: one
    optional: false
  - slot: theory_schema_digest
    type: artifact_digest
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: full_report
    type: artifact_ref
    role: result
    cardinality: many
    optional: false
  - slot: compact_evidence_report
    type: artifact_ref
    role: result
    cardinality: optional_many
    optional: true
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: not method-specified; engineering. Tversky & Kahneman (1992), Journal of Risk and Uncertainty 5; Peterson et al. (2021), Science 372.
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `mt.01` — Freeze official source identities

```yaml
legacy_workflow: mist_trail_deliberative_appraisal_mtd1
original_values:
  step_id: mt.01
  verb: acquire
  label: Freeze official source identities
  inputs:
    official_public_sources:
      type: source_document
      cardinality: '3'
      optional: false
  outputs:
    source_manifest:
      type: dataset
      cardinality: '1'
      optional: false
    source_digests_and_custody:
      type: artifact_digest
      cardinality: 1..*
      optional: false
  parameters: &id001
  - bounded_source_list
  - retrieval_date
  preconditions: &id002
  - official project page
  - document record
  - and Draft EA identified
  method_owned_semantics: &id003
  - which official materials bound the appraisal
  internal_method_phases:
  - select_source_packet
  - record_identity_and_use_limits
  actor: human
  optional: false
  repeatable: false
  implementation_status: represented_manual
  evidence_basis:
  - fixture
  - code
  source_refs: &id004
  - docs/plans/mist_trail_policy_decision_vertical.md:80-113
  - examples/fixtures/mist_trail_decision/source_manifest.json:1
assigned_rev5_values:
  method_id: mist_trail_policy_appraisal
  step_id: mt.01
  verb: acquire
  label: Freeze official source identities
  workflow_role: acquire
  operation_kind: runtime_delivery
  actor_chain:
  - human_analyst
  inputs:
  - slot: official_public_sources
    type: source_document
    role: subject
    cardinality: many
    optional: false
  outputs:
  - slot: source_manifest
    type: dataset
    role: result
    cardinality: one
    optional: false
  - slot: source_digests_and_custody
    type: artifact_digest
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'not method-specified; engineering. Dodgson et al. (2009), Multi-Criteria Analysis: A Manual; Moberg et al. (2018), GRADE Evidence to Decision framework.'
  execution_status: manually_performed
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `mt.02` — Frame decision and official options

```yaml
legacy_workflow: mist_trail_deliberative_appraisal_mtd1
original_values:
  step_id: mt.02
  verb: construct
  label: Frame decision and official options
  inputs:
    source_manifest:
      type: dataset
      cardinality: '1'
      optional: false
    project_purpose_and_alternatives:
      type: source_document
      cardinality: 1..*
      optional: false
  outputs:
    decision_frame:
      type: configuration
      cardinality: '1'
      optional: false
    options:
      type: option
      cardinality: '3'
      optional: false
    common_actions:
      type: finding
      cardinality: 0..*
      optional: false
    criteria:
      type: criterion
      cardinality: '6'
      optional: false
    affected_interests:
      type: entity
      cardinality: 1..*
      optional: false
  parameters: &id001
  - development_only_nonclaims
  preconditions: &id002
  - official alternatives A B and C retained without invention or merger
  method_owned_semantics: &id003
  - decision framing
  - criterion selection
  - affected-interest identification
  internal_method_phases:
  - state_question_and_authority
  - identify_options_and_common_actions
  - define_criteria_and_interests
  actor: human
  optional: false
  repeatable: false
  implementation_status: represented_manual
  evidence_basis:
  - fixture
  - code
  source_refs: &id004
  - docs/plans/mist_trail_policy_decision_vertical.md:54-63
  - docs/plans/mist_trail_policy_decision_vertical.md:115-134
  - src/mixed_methods_workbench/mist_trail_decision.py:145-196
assigned_rev5_values:
  method_id: mist_trail_policy_appraisal
  step_id: mt.02
  verb: construct
  label: Frame decision and official options
  workflow_role: conceptualize
  operation_kind: analytic
  actor_chain:
  - human_analyst
  inputs:
  - slot: source_manifest
    type: dataset
    role: subject
    cardinality: one
    optional: false
  - slot: project_purpose_and_alternatives
    type: source_document
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: decision_frame
    type: configuration
    role: result
    cardinality: one
    optional: false
  - slot: options
    type: option
    role: result
    cardinality: many
    optional: false
  - slot: common_actions
    type: finding
    role: result
    cardinality: many
    optional: false
  - slot: criteria
    type: criterion
    role: result
    cardinality: many
    optional: false
  - slot: affected_interests
    type: entity
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Frame decision and official options' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Dodgson et al. (2009), Multi-Criteria Analysis: A Manual; Moberg et al. (2018), GRADE Evidence to Decision framework.'
  execution_status: manually_performed
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `mt.03` — Review and anchor source windows

```yaml
legacy_workflow: mist_trail_deliberative_appraisal_mtd1
original_values:
  step_id: mt.03
  verb: anchor
  label: Review and anchor source windows
  inputs:
    official_sources:
      type: source_document
      cardinality: 1..*
      optional: false
  outputs:
    source_anchors:
      type: passage_anchor
      cardinality: 1..*
      optional: false
  parameters: &id001
  - page_section_locator
  - passage_custody_policy
  preconditions: &id002
  - source window reviewed
  - exact text rendered only from matching bytes
  method_owned_semantics: &id003
  - faithful source summary and relevant source window
  internal_method_phases:
  - read_source_window
  - summarize
  - attach_locator
  actor: human
  optional: false
  repeatable: true
  implementation_status: represented_manual
  evidence_basis:
  - fixture
  - code
  source_refs: &id004
  - src/mixed_methods_workbench/mist_trail_decision.py:103-143
  - examples/fixtures/mist_trail_decision/decision_packet.json:1
assigned_rev5_values:
  method_id: mist_trail_policy_appraisal
  step_id: mt.03
  verb: anchor
  label: Review and anchor source windows
  workflow_role: represent
  operation_kind: runtime_delivery
  actor_chain:
  - human_analyst
  inputs:
  - slot: official_sources
    type: source_document
    role: subject
    cardinality: many
    optional: false
  outputs:
  - slot: source_anchors
    type: passage_anchor
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'not method-specified; engineering. Dodgson et al. (2009), Multi-Criteria Analysis: A Manual; Moberg et al. (2018), GRADE Evidence to Decision framework.'
  execution_status: manually_performed
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `mt.04` — Assess option consequences by criterion

```yaml
legacy_workflow: mist_trail_deliberative_appraisal_mtd1
original_values:
  step_id: mt.04
  verb: appraise_source
  label: Assess option consequences by criterion
  inputs:
    options:
      type: option
      cardinality: '3'
      optional: false
    criteria:
      type: criterion
      cardinality: '6'
      optional: false
    affected_interests:
      type: entity
      cardinality: 1..*
      optional: false
    source_anchors:
      type: passage_anchor
      cardinality: 1..*
      optional: false
  outputs:
    consequence_assessments:
      type: consequence
      cardinality: '18'
      optional: false
  parameters: &id001
  - direction_vocabulary
  - time_horizon_vocabulary
  - mitigation_flag
  preconditions: &id002
  - exactly one assessment for every option-criterion pair
  - every assessment source-bound
  method_owned_semantics: &id003
  - consequence interpretation
  - direction
  - affected interests
  - uncertainty
  - mitigation assumptions
  internal_method_phases:
  - interpret_consequence
  - classify_direction_and_time
  - state_uncertainty
  actor: human
  optional: false
  repeatable: true
  implementation_status: represented_manual
  evidence_basis:
  - fixture
  - code
  source_refs: &id004
  - docs/plans/mist_trail_policy_decision_vertical.md:135-161
  - src/mixed_methods_workbench/mist_trail_decision.py:198-213
assigned_rev5_values:
  method_id: mist_trail_policy_appraisal
  step_id: mt.04
  verb: appraise_source
  label: Assess option consequences by criterion
  workflow_role: appraise
  operation_kind: analytic
  actor_chain:
  - human_analyst
  inputs:
  - slot: options
    type: option
    role: subject
    cardinality: many
    optional: false
  - slot: criteria
    type: criterion
    role: context
    cardinality: many
    optional: false
  - slot: affected_interests
    type: entity
    role: context
    cardinality: many
    optional: false
  - slot: source_anchors
    type: passage_anchor
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: consequence_assessments
    type: consequence
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Assess option consequences by criterion' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Dodgson et al. (2009), Multi-Criteria Analysis: A Manual; Moberg et al. (2018), GRADE Evidence to Decision framework.'
  execution_status: manually_performed
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `mt.05` — Record explicit criterion judgments

```yaml
legacy_workflow: mist_trail_deliberative_appraisal_mtd1
original_values:
  step_id: mt.05
  verb: value
  label: Record explicit criterion judgments
  inputs:
    criteria:
      type: criterion
      cardinality: '6'
      optional: false
    consequence_assessments:
      type: consequence
      cardinality: '18'
      optional: false
  outputs:
    criterion_judgments:
      type: value_judgment
      cardinality: '6'
      optional: false
  parameters: &id001
  - importance_vocabulary
  - judgment_kind_vocabulary
  preconditions: &id002
  - every criterion receives one visible judgment
  method_owned_semantics: &id003
  - importance
  - factual-normative-mixed status
  - rationale
  - dissent
  - change condition
  internal_method_phases:
  - set_priority
  - explain_rationale
  - record_alternative_and_change_condition
  actor: human
  optional: false
  repeatable: true
  implementation_status: represented_manual
  evidence_basis:
  - fixture
  - code
  source_refs: &id004
  - docs/plans/mist_trail_policy_decision_vertical.md:150-156
  - src/mixed_methods_workbench/mist_trail_decision.py:215-226
assigned_rev5_values:
  method_id: mist_trail_policy_appraisal
  step_id: mt.05
  verb: value
  label: Record explicit criterion judgments
  workflow_role: appraise
  operation_kind: analytic
  actor_chain:
  - human_analyst
  inputs:
  - slot: criteria
    type: criterion
    role: subject
    cardinality: many
    optional: false
  - slot: consequence_assessments
    type: consequence
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: criterion_judgments
    type: value_judgment
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Record explicit criterion judgments' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Dodgson et al. (2009), Multi-Criteria Analysis: A Manual; Moberg et al. (2018), GRADE Evidence to Decision framework.'
  execution_status: manually_performed
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `mt.06` — Apply alternative priority lenses

```yaml
legacy_workflow: mist_trail_deliberative_appraisal_mtd1
original_values:
  step_id: mt.06
  verb: perturb
  label: Apply alternative priority lenses
  inputs:
    criterion_judgments:
      type: value_judgment
      cardinality: '6'
      optional: false
    consequence_assessments:
      type: consequence
      cardinality: '18'
      optional: false
  outputs:
    priority_lenses:
      type: appraisal
      cardinality: '3'
      optional: false
    tradeoff_findings:
      type: finding
      cardinality: 1..*
      optional: false
  parameters: &id001
  - safety_flow_lens
  - minimum_disturbance_lens
  - operations_first_lens
  preconditions: &id002
  - each lens declares decisive criteria and names a conditional result or unresolved state
  method_owned_semantics: &id003
  - how changed priorities alter the preferred option
  - which tradeoffs remain value-dependent
  internal_method_phases:
  - apply_lens
  - inspect_reversal_or_unresolved_result
  - identify_tradeoff
  actor: human
  optional: false
  repeatable: true
  implementation_status: represented_manual
  evidence_basis:
  - fixture
  - code
  source_refs: &id004
  - docs/plans/mist_trail_policy_decision_vertical.md:163-175
  - src/mixed_methods_workbench/mist_trail_decision.py:228-254
assigned_rev5_values:
  method_id: mist_trail_policy_appraisal
  step_id: mt.06
  verb: perturb
  label: Apply alternative priority lenses
  workflow_role: analyze
  operation_kind: analytic
  actor_chain:
  - human_analyst
  inputs:
  - slot: criterion_judgments
    type: value_judgment
    role: subject
    cardinality: many
    optional: false
  - slot: consequence_assessments
    type: consequence
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: priority_lenses
    type: appraisal
    role: result
    cardinality: many
    optional: false
  - slot: tradeoff_findings
    type: finding
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Apply alternative priority lenses' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Dodgson et al. (2009), Multi-Criteria Analysis: A Manual; Moberg et al. (2018), GRADE Evidence to Decision framework.'
  execution_status: manually_performed
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `mt.07` — Form conditional conclusion

```yaml
legacy_workflow: mist_trail_deliberative_appraisal_mtd1
original_values:
  step_id: mt.07
  verb: recommend
  label: Form conditional conclusion
  inputs:
    consequence_assessments:
      type: consequence
      cardinality: '18'
      optional: false
    criterion_judgments:
      type: value_judgment
      cardinality: '6'
      optional: false
    priority_lenses:
      type: appraisal
      cardinality: '3'
      optional: false
    tradeoff_findings:
      type: finding
      cardinality: 1..*
      optional: false
  outputs:
    decision_conclusion:
      type: recommendation
      cardinality: '1'
      optional: false
    evidence_gaps:
      type: gap
      cardinality: 0..*
      optional: false
    next_actions:
      type: recommendation
      cardinality: 1..*
      optional: false
  parameters: &id001
  - conditional_unresolved_or_refused_state
  preconditions: &id002
  - conclusion names decisive assessments and judgments
  - sensitivity and nonclaims remain explicit
  method_owned_semantics: &id003
  - whether a recommendation is licensed
  - decisive reasons
  - sensitivity
  - next action
  internal_method_phases:
  - integrate_evidence_and_values
  - choose_terminal_state
  - state_dependencies_and_limits
  actor: human
  optional: false
  repeatable: false
  implementation_status: represented_manual
  evidence_basis:
  - fixture
  - code
  source_refs: &id004
  - src/mixed_methods_workbench/mist_trail_decision.py:256-276
  - examples/fixtures/mist_trail_decision/decision_packet.json:1
assigned_rev5_values:
  method_id: mist_trail_policy_appraisal
  step_id: mt.07
  verb: recommend
  label: Form conditional conclusion
  workflow_role: decide
  operation_kind: analytic
  actor_chain:
  - human_analyst
  inputs:
  - slot: consequence_assessments
    type: consequence
    role: subject
    cardinality: many
    optional: false
  - slot: criterion_judgments
    type: value_judgment
    role: context
    cardinality: many
    optional: false
  - slot: priority_lenses
    type: appraisal
    role: context
    cardinality: many
    optional: false
  - slot: tradeoff_findings
    type: finding
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: decision_conclusion
    type: recommendation
    role: result
    cardinality: one
    optional: false
  - slot: evidence_gaps
    type: gap
    role: result
    cardinality: many
    optional: false
  - slot: next_actions
    type: recommendation
    role: result
    cardinality: many
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: The method may rely on the completed 'Form conditional conclusion' result, subject to its method-owned semantics; the legacy row did not state a narrower licensed claim.
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'Dodgson et al. (2009), Multi-Criteria Analysis: A Manual; Moberg et al. (2018), GRADE Evidence to Decision framework.'
  execution_status: manually_performed
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `mt.08` — Assemble typed decision packet

```yaml
legacy_workflow: mist_trail_deliberative_appraisal_mtd1
original_values:
  step_id: mt.08
  verb: construct
  label: Assemble typed decision packet
  inputs:
    decision_components:
      type: appraisal
      cardinality: 1..*
      optional: false
    source_manifest_digest:
      type: artifact_digest
      cardinality: '1'
      optional: false
    review_events:
      type: review_event
      cardinality: 1..*
      optional: false
  outputs:
    decision_packet:
      type: dataset
      cardinality: '1'
      optional: false
  parameters: &id001
  - schema_version_0_1_0
  - packet_id
  preconditions: &id002
  - all manually authored components exist
  method_owned_semantics: &id003 []
  internal_method_phases: []
  actor: human_artifact_authoring
  optional: false
  repeatable: false
  implementation_status: represented_manual
  evidence_basis:
  - code
  - fixture
  source_refs: &id004
  - src/mixed_methods_workbench/mist_trail_decision.py:279-308
  - examples/fixtures/mist_trail_decision/decision_packet.json:1
assigned_rev5_values:
  method_id: mist_trail_policy_appraisal
  step_id: mt.08
  verb: construct
  label: Assemble typed decision packet
  workflow_role: conceptualize
  operation_kind: runtime_delivery
  actor_chain:
  - human_analyst
  inputs:
  - slot: decision_components
    type: appraisal
    role: subject
    cardinality: many
    optional: false
  - slot: source_manifest_digest
    type: artifact_digest
    role: context
    cardinality: one
    optional: false
  - slot: review_events
    type: review_event
    role: context
    cardinality: many
    optional: false
  outputs:
  - slot: decision_packet
    type: dataset
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'not method-specified; engineering. Dodgson et al. (2009), Multi-Criteria Analysis: A Manual; Moberg et al. (2018), GRADE Evidence to Decision framework.'
  execution_status: manually_performed
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: false
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
```

### `mt.09` — Validate custody and decision invariants

```yaml
legacy_workflow: mist_trail_deliberative_appraisal_mtd1
original_values:
  step_id: mt.09
  verb: test
  label: Validate custody and decision invariants
  inputs:
    source_manifest:
      type: dataset
      cardinality: '1'
      optional: false
    decision_packet:
      type: dataset
      cardinality: '1'
      optional: false
  outputs:
    validated_decision_artifact:
      type: appraisal
      cardinality: '1'
      optional: false
  parameters: &id001
  - expected_source_set
  - expected_draft_ea_hash_and_size
  preconditions: &id002
  - manifest and packet parse under strict frozen models
  method_owned_semantics: &id003
  - fixture-specific invariants only; not policy appraisal validity
  internal_method_phases:
  - validate_uniqueness_and_references
  - validate_option_criterion_completeness
  - validate_source_identity_and_passage_custody
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  - test
  source_refs: &id004
  - src/mixed_methods_workbench/mist_trail_decision.py:24-130
  - src/mixed_methods_workbench/mist_trail_decision.py:289-389
  - src/mixed_methods_workbench/mist_trail_decision.py:399-425
  - tests/test_mist_trail_decision.py:33-121
assigned_rev5_values:
  method_id: mist_trail_policy_appraisal
  step_id: mt.09
  verb: test
  label: Validate custody and decision invariants
  workflow_role: appraise
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: source_manifest
    type: dataset
    role: subject
    cardinality: one
    optional: false
  - slot: decision_packet
    type: dataset
    role: context
    cardinality: one
    optional: false
  outputs:
  - slot: validated_decision_artifact
    type: appraisal
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'not method-specified; engineering. Dodgson et al. (2009), Multi-Criteria Analysis: A Manual; Moberg et al. (2018), GRADE Evidence to Decision framework.'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

### `mt.10` — Serve shared API and browser artifact

```yaml
legacy_workflow: mist_trail_deliberative_appraisal_mtd1
original_values:
  step_id: mt.10
  verb: project
  label: Serve shared API and browser artifact
  inputs:
    validated_decision_artifact:
      type: appraisal
      cardinality: '1'
      optional: false
  outputs:
    json_payload:
      type: dataset
      cardinality: '1'
      optional: false
    browser_view:
      type: artifact_ref
      cardinality: '1'
      optional: false
  parameters: &id001
  - existing_dashboard_routes
  preconditions: &id002
  - full packet validates; browser contains no embedded conclusion that can drift
  method_owned_semantics: &id003
  - plain-language presentation preserves source
  - evidence
  - value
  - uncertainty
  - and nonclaim distinctions
  internal_method_phases:
  - serialize_once
  - render_browser_from_same_payload
  actor: deterministic_software
  optional: false
  repeatable: true
  implementation_status: executable
  evidence_basis:
  - code
  - test
  source_refs: &id004
  - src/mixed_methods_workbench/mist_trail_decision.py:428-430
  - src/mixed_methods_workbench/method_dashboard_server.py:61-75
  - tests/test_mist_trail_decision.py:124-152
assigned_rev5_values:
  method_id: mist_trail_policy_appraisal
  step_id: mt.10
  verb: project
  label: Serve shared API and browser artifact
  workflow_role: communicate
  operation_kind: runtime_delivery
  actor_chain:
  - deterministic_engine
  inputs:
  - slot: validated_decision_artifact
    type: appraisal
    role: subject
    cardinality: one
    optional: false
  outputs:
  - slot: json_payload
    type: dataset
    role: result
    cardinality: one
    optional: false
  - slot: browser_view
    type: artifact_ref
    role: result
    cardinality: one
    optional: false
  parameters: *id001
  preconditions: *id002
  conclusion_supported: none — enabling or delivery step only
  failure_output: migration_unresolved — the legacy row specified preconditions but no explicit failure artifact or terminal state
  method_owned_semantics: *id003
  evidence_basis: 'not method-specified; engineering. Dodgson et al. (2009), Multi-Criteria Analysis: A Manual; Moberg et al. (2018), GRADE Evidence to Decision framework.'
  execution_status: software_executable
  representation_status: implemented_artifact
  implementation_ref: *id004
  optional: false
  repeatable: true
unexpressible_or_loss_notes:
- workflow_role, operation_kind, conclusion_supported, failure_output, slot roles, and actor_chain were absent from the legacy schema and are explicit migration assignments, not original observations.
- Legacy cardinalities are ranges/strings; rev 5 permits only one/many/optional_one/optional_many, so exact numeric bounds are preserved only in original_values and collapsed in assigned_rev5_values.
- internal_method_phases has no rev-5 field; preserved only in original_values. The bundled callable cannot be split into separately executable rows without changing the observation.
```

## Migration disposition

- All 77 legacy IDs occur exactly once above.
- The migration does not assert that the 77 executable boundaries are the correct rev-5 ideal granularity. Bundled operations remain bundled and carry loss notes.
- `failure_output` remains unresolved for every legacy row because the frozen candidate did not record a failure artifact; inventing one would change the observation.
- Consequential classification or scoping differences are adjudicated or escalated in `disagreements.md`; this file alone cannot settle them.
