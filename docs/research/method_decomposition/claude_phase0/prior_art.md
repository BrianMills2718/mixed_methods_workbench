# Phase 0 Prior Art (§8.1)

**Status:** `independent_candidate`. Inspected in Phase 0, written up
separately here, and **not** consulted while producing the ideal
decompositions in `step_ledger.yaml`/`sources.md` — per rev 5.1's
sequencing guard, to avoid the collision exercise simply rediscovering the
current design and reporting it back as a "finding." Everything below is
evidence about what already composes and a candidate implementation
substrate — not a schema any future decomposition must conform to.

**Repository provenance:** see `repository_snapshots.yaml`. The
`process_tracing` findings below (§3) were reverified for the two frozen
workflows at clean commit `4450d2e`; their implementation classifications did
not change. The Data Contracts and Theory Forge
findings (§1-2) rest on presumed-unchanged, not contemporaneously
captured, commits.

## 1. Data Contracts (`/home/brian/code/active/data-contracts`)

A shared Pydantic-based library, explicitly scoped by its own ADR as a
"boundary-contract substrate," bundling several largely independent
sub-systems:

- **Core boundary layer** (`models.py`, `decorator.py`, `registry.py`,
  `checker.py`): `BoundaryModel` (strict `extra="forbid"` base with a
  `.permissive()` classmethod producing an `extra="ignore"` consumer
  subclass), `@boundary` decorator, `ContractRegistry`, and purely
  **structural** (property-name + JSON-type) compatibility/breaking-change
  checking. No semver parsing here — `ContractInfo.version` is a free
  string, never compared.
- **`data_contracts.composition`** (2741 lines): a real, generic,
  dependency-light DSL for versioned "action packs" — typed payload/
  reference/resource/refinement/semantic contracts, cross-pack imports,
  cycle detection, and a pure compiler emitting an immutable
  `CompiledManifest`. This layer has genuine PEP 440
  (`packaging.specifiers.SpecifierSet`) version-constraint resolution and
  major-version-in-ID enforcement — the most mature version-compatibility
  mechanism found anywhere in this survey. It is domain-agnostic: it has
  no notion of "qualitative coding," "process tracing," or "theory."
- **`data_contracts.runtime_seams`**: portable wire contracts built
  specifically for a *different* ecosystem (DIGIMON / Team-Brains / Inside
  Success). Implements the same strict-producer/permissive-consumer
  pattern as the core layer, independently, using a fixed-literal
  `SCHEMA_VERSION_V1` (exact match or reject — no minor/patch tolerance).
- **`governed_graph.py`, `governed_lifecycle.py`, `governed_ambiguity.py`,
  `improvement.py`, `review.py`**: all built for the onto-canon6/DIGIMON/
  Inside Success cluster; not relevant to QC/PT/theory-forge/workbench.

**Consumption reality, verified by grep across all four target repos and
by building a clean test venv:**

| Consumer | Status |
|---|---|
| qualitative_coding | Not imported anywhere. |
| process_tracing | Not imported anywhere. |
| mixed_methods_workbench | Not imported anywhere (documentation-only repo). |
| theory-forge | Imported via a **soft, optional** try/except fallback in two files (`contracts/schema_compile.py`, `codegen/runner.py`), **not** declared in `pyproject.toml`. Confirmed by building a clean venv without `data_contracts`: `tests/test_schema_compile_contracts.py`'s boundary-metadata test fails, because the fallback no-op decorator doesn't set the attribute the test expects. Installing the real package fixes it. `data_contracts`'s own "known consumers" docs do not list theory-forge at all — the maintainers' bookkeeping has not caught up to even this fragile integration. |

Test suite: 474 tests pass (verified by installation and direct run), but
they verify internal consistency and architectural purity of subsystems
built for the onto-canon6/DIGIMON/Inside-Success cluster — not integration
with any repository in this project's cluster.

**Bottom line for future promotion decisions:** `data_contracts` is a
mature, well-tested, real composition/versioning substrate — but it is
currently substrate for a *different* product cluster, and would need to
be extended or its patterns re-implemented, not simply imported, to serve
as shared infrastructure for QC/PT/theory-forge/workbench. Any Tier 1/2
crosswalk claim (§11.3) that assumes `data_contracts` "already covers"
cross-method composition in *this* cluster would be false on current
evidence — it is `expressible_with_extension` at best for the
runtime-seam pattern, and `requires_new_machinery` for anything that needs
awareness of this cluster's actual types.

## 2. Theory Forge `PipelineSpec` and v15 algorithm fields

`PipelineSpec` (`theory_forge/codegen/pipeline_spec.py`) is the
intermediate representation between a theory schema and generated code
("Theory Schema -> Operationalize -> Pipeline Spec -> Compile -> Code"),
with real referential-integrity validation beyond Pydantic (orchestration
reference checks, cycle detection). "v15 algorithm fields"
(`AlgorithmV15` in `extraction/models.py`) add four **optional** fields
(`typed_inputs`, `output_type`, `invariants`, `golden_cases`) to any v14
algorithm entry. Fully implemented and heavily tested (1385 tests passing
across `test_v15_schema.py` + `test_schema_to_spec.py`), and functions
correctly as backward-compatible additive schema evolution — independent
of `data_contracts` entirely. This is a real, working pattern for
"producer schema versioning with additive fields" that a future shared
capability could crosswalk against, separate from the `data_contracts`
composition machinery.

**Caveat surfaced by inspection, not by design:** the shipped CLI still
validates against v14 (`META_SCHEMA_PATH` points at `meta_schema_v14.json`),
and v14's algorithm definitions have no `additionalProperties: false`, so
v15 fields silently pass through the "v14" validator without it ever
switching schema versions. The v14/v15 behavioral split lives entirely in
application-code field-presence checks (`if stage.invariants: ...`), not
in schema-version branching. Functionally sound, but worth naming
precisely: this is not "the system now validates against v15" — it is "v15
fields are additive and happen to slip through the v14 gate unchanged."

## 3. Producer export interfaces — general survey

Three distinct cross-repo contract pairs were found, at three different
levels of actual integration:

- **QC -> Process Tracing handoff** (`qc_clean/core/process_tracing_handoff.py`):
  producer-complete, self-tested (own CLI validator + 7 passing tests), with
  a hard-enforced denylist (`FORBIDDEN_PT_INFERENCE_FIELDS`) preventing QC
  from smuggling in PT-owned concepts. **Zero references to this contract
  exist anywhere in the process_tracing repository** — it is
  producer-complete with no real consumer.
- **Process Tracing -> QC "theory test return"** (`pt/theory_test_return.py`
  <-> `qc_clean/core/process_tracing_theory_test_return.py`): **the one
  genuinely two-sided, exercised cross-repo contract found in this whole
  survey.** Both sides implemented and tested independently (25 + 10 tests
  passing across both repos), field-for-field structurally identical, but
  hand-written independently on each side with **no shared library or
  codegen** keeping them in sync — and the QC-side consumer only ever sees
  a static fixture (`p5_theory_test_return_v1.json`), not a live
  process-tracing run in the same pass. A real integration, sustained by
  manual/reviewed duplication rather than a shared contract.
- **Process Tracing's `pt_export_v2`** (`pt/export.py`): producer-complete
  and thoroughly tested (dedicated v2 tests for policy-scenario replay,
  source-silence sensitivity, methodology-integrity controls, same-case
  reuse). Its intended consumer, mixed_methods_workbench, has only a
  **synthetic, schema-mismatched stub** (`pt_export_stub.json`, explicitly
  labeled `"artifact_status": "synthetic_contract_fixture"`, whose own
  manifest notes it still targets the *older* v1 concept). The workbench's
  own docs are explicit that this is "preliminary future architecture;
  documentation only" — the "strict producer / permissive consumer" pattern
  is a stated design intent here, not a built mechanism.

**Bottom line:** the single strongest piece of real, non-`data_contracts`,
cross-repo prior art is the PT<->QC `theory_test_return` seam. Any future
shared-capability design for cross-method handoffs should study that seam's
actual (hand-synchronized, fixture-consumed) shape rather than assume the
more aspirational QC->PT handoff or PT->workbench `pt_export_v2` seams
represent working integration today.
