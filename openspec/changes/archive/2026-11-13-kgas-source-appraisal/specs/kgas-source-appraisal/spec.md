## ADDED Requirements

### Requirement: Bind an attributable source appraisal

The consumer SHALL accept an optional versioned appraisal as a separate record, verify its digest and target artifact digest, and resolve each addressed artifact pointer to the recorded value. Claims SHALL retain reviewer attribution, disposition, source identity and printed-page references.

Source: Brian, 2026-11-13, "proceed", continuing the source-bound theory-to-Workbench integration; exact review-file contract inferred by agent.

#### Scenario: Display a source comparison
- **WHEN** a valid appraisal is supplied
- **THEN** source-linked judgments are displayed separately from original artifact assertions

#### Scenario: Refuse a broken review binding
- **WHEN** a declared review has an unsupported version, mismatched digest, invalid pointer/value, unsafe path or invalid source/page reference
- **THEN** context construction fails explicitly without silently discarding the appraisal

### Requirement: Preserve the distinction between review and validation

The review SHALL distinguish an attributable comparison with one scholarly source from empirical theory validation. The original KGAS rule and artifact SHALL remain available with their historical identity. Any comparison inputs SHALL be labelled illustrative rather than observed.

Source: Inferred by agent from the source gap, preserved artifact and user-approved requirement to retain limits on conclusions.

#### Scenario: Inspect a logical counterexample
- **WHEN** a reviewer supplies one- and two-attribute illustrative inputs
- **THEN** the KGAS arithmetic results and attributed paper-class distinction are visible without claiming a calibrated numerical interpretation of those classes

#### Scenario: Preserve unreviewed context
- **WHEN** a theory definition has no appraisal reference
- **THEN** the existing context and calculation remain usable with their original provenance limits
