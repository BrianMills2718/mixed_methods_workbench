# Independent Codex review — Phase 0 rev-5.1 compliance

reviewed_commit: `c106de230d6ba2761eacd03727c0bed1bc1eef84`

independent_reviewer: OpenAI Codex (GPT-5), read-only subagent

review_scope: frozen authoring commit only; later uncommitted state was not inspected

Disposition: `accept_with_corrections`

## Independence and checks

The reviewer was started only after the authoring pass was frozen at the commit
above. It received the rev 5.1 §0.1-0.2 acceptance questions and read the frozen
artifacts directly. It made no edits.

The review confirmed:

- 77/77 unique migration records, with an exact ID-set match to
  `codex_phase0/steps.yaml`;
- every `original_values` mapping equals the frozen legacy row field for field;
- all 20 rev-5 fields are present in every assigned row and every row carries
  an explicit loss note;
- 40/40 comparison entries map exactly and in order to D01-D40: 25 factual,
  11 methodological, and 4 unsettled;
- D22, D24, D28, and D29 are explicitly escalated;
- `comparison_v0.md` is byte-identical to the parent version, blob
  `c6bf31274a8a0bf851fd2139403f40ed57184921`.

## Findings and correction disposition

### Major — human judgments mislabeled as software execution

`pt.06` and `pt_acq.03` inherited `software_executable` from the legacy
candidate even though their legacy actors are `human` and
`human_with_deterministic_validation`. This also contradicted D22's explicit
finding for interactive source admission.

Correction applied after review:

- both rows now assign `execution_status: manually_performed`;
- `pt.06` now uses `actor_chain: [human_reviewer]`;
- the global crosswalk now states that migration is semantic and case-specific,
  because a callable human-review boundary is not software execution;
- focused validation asserts both statuses.

A read-only correction verification then caught an accidental neighboring-row
regression: `qc_gt.02`, a deterministic source-unit selection step, had changed
to `manually_performed` while editing the large migration artifact. It was
restored to `software_executable`; validation now pins that status and the
`pt.06` reviewer actor explicitly.

### Minor — incomplete repository pins

D01, D02, D35, and D37-D40 included shorthand factual references after an
initial pinned reference.

Correction applied after review: every factual code reference in those rows now
uses `repository@revision:file:line`.

### Minor — permissive validator

The frozen validator checked first-word area overlap and only the existence of
some `file:line` text.

Correction applied after review: validation now requires exact ordered area
identity and checks every backticked factual reference for a repository,
7-40-character revision, path, and line.

## Reviewer conclusion

The reviewer did not reject the migration or comparison. Its exact disposition
was `accept_with_corrections`: the 77-row and 40-row structures were complete,
the semantic synthesis was preserved, and the bounded defects above had to be
corrected before merge. The correction checks are durable in
`scripts/validate_phase0_compliance.py` and `tests/test_phase0_compliance.py`.
