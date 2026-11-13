# kgas-theory-context Specification

## Purpose
Preserve a KGAS example as inspectable, source-bound Workbench theory context, with explicit provenance limits and a bounded calculation under its declared rule.

## Requirements

### Requirement: Preserve pinned theory context

The consumer SHALL validate the captured KGAS artifact's digest and supported major version, retain original fields, confine file reads to the declared input root, and expose exact artifact references for the consumed constructs and procedures.

Source: Brian, 2026-11-12, "i approve", accepting the KGAS-to-Workbench theory-context proposal; plan 009.

#### Scenario: Review a preserved artifact
- **WHEN** the pinned supported artifact is read
- **THEN** definitions and procedures retain resolvable JSON Pointer references and original values

#### Scenario: Refuse incompatible or corrupted input
- **WHEN** the artifact version is unsupported, its digest differs, a required field is missing or its path escapes the root
- **THEN** the consumer fails explicitly before producing an accepted theory context

### Requirement: Preserve epistemic limits

The review SHALL distinguish artifact provenance from scholarly verification, theory context from empirical evidence, required observations from observed results, and declared operations from implemented operations.

Source: Brian, 2026-11-12, approval of the proposal to retain assumptions and limits on conclusions; unverified-source treatment inferred by agent from the preserved artifact's missing scholarly anchors.

#### Scenario: Display unverified operationalization
- **WHEN** the KGAS example is displayed
- **THEN** missing paper-level anchors and unverified rule/validation assertions remain visible and no empirical validity is implied

### Requirement: Calculate the declared rule with explicit inputs

The consumer SHALL calculate the declared geometric mean only from explicit finite inputs in the interval zero to one, retain the inputs and rule reference, and distinguish the arithmetic result from measured attributes or validated theory.

Source: Inferred by agent from the approved usable theory-to-method connection and the artifact's geometric-mean rule; deterministic calculation is a bounded implementation choice.

#### Scenario: Calculate a supplied example
- **WHEN** all three valid inputs are supplied
- **THEN** the result and receipt identify the supplied values and preserved rule

#### Scenario: Refuse invalid numeric inputs
- **WHEN** inputs are missing, nonfinite or outside the interval
- **THEN** calculation fails explicitly

### Requirement: Reuse the study review surface

The existing study builder SHALL expose matching machine and browser theory context, support a standalone review without fabricated corpus evidence, and preserve ordinary study behavior when context is absent.

Source: Inferred by agent from the approved Workbench integration and its existing study-page consumer seam.

#### Scenario: Build the review
- **WHEN** the standalone theory definition is built
- **THEN** JSON, HTML and a hash-bound build receipt expose the context and any requested calculation

#### Scenario: Preserve existing studies
- **WHEN** an existing study has no theory-context reference
- **THEN** its existing payload and review functions remain compatible
