# DEMO-C1 Independent Audit

Date: 2026-07-12  
Evaluated commit: `6a8e0b5338221c29ddf9f7ad92bd92a98b06ec29`  
Verdict: **PASS**

## Bounded Decision

Accept DEMO-C1 as A/test evidence for the eight declared **synthetic structural
contract-behavior** rows. Fixture content remains C. This decision does not
promote QC/PT/GT-I producer readiness, open-prose meaning, methodological
validity, mixed-methods integration, or SOTA evidence.

## Independent Execution

- `pytest`: 41/41 passed.
- `mypy --strict`: passed.
- Ruff: passed.
- `make check`: all legacy and DEMO-C1 controls passed.
- Review assembly: passed.
- `make demo-coverage`: passed in a detached disposable clone and regenerated
  Markdown/JSON coverage byte-identically; overall coverage remained D.
- Held-out adversarial matrix: 37/37 invalid mutations rejected, covering
  hashes, exact offsets, packet binding, closed claim envelopes, QC/PT/GT
  identities/cardinalities/reference uniqueness, residual/ranking rules,
  comparison iteration order, link method/object-kind compatibility, manifest
  inventory, and CLI failure behavior.
- Deliberately arbitrary QC/PT/GT/link prose was accepted only while every
  containing surface retained
  `synthetic_non_authoritative_human_review_required`.

## Audit History and Correction

The initial implementation commit `3c048fc` was rejected. Its controls
overstated semantic closure and missed same-length offset shifts, duplicate
cardinalities, incomplete native-object identity, open claim envelopes, and
the real CLI failure path. The remediation:

- bound offsets to exact document content;
- closed every authoritative claim-limit surface;
- added method + native object kind to link identity;
- enforced uniqueness before set aggregation;
- narrowed A/test claims to structural behavior;
- marked all open analytic prose non-authoritative and human-review-required;
- exercised positive and invalid CLI subprocess paths;
- added held-out regression controls for the failure families.

The verification-gap entry is staged in
`.claude/tasks/verification_gap_pending_demo_c1.md` because an active
project-meta claim currently owns the shared append-only log.

## Repository Boundaries

No producer repository was changed. `qualitative_coding`, `grounded-research`,
and `theory-forge` were clean. `process_tracing` retained only its known
pre-existing untracked `workbench/frontend/node_modules/`, already tracked as
concern C010.

