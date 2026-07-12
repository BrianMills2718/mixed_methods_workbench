# Mixed Methods Workbench Handoff

## What This Project Is

`mixed_methods_workbench` is the integration and planning authority for a future
text-centered research workbench. Producer repos retain their own methodology
and implementation. This repo owns study framing, cross-method boundaries,
consumer contracts, compatibility policy, integration sequencing, and eventual
bounded meta-inferences. It is currently in **documentation-only mode**; no
implementation slice is active.

## What Was Completed

- `98b5310`: added executable synthetic contract fixtures.
- `d00f02d`: added coverage visibility and initial negative controls.
- `bc22b90`: made controls invariant-specific and corrected overclaimed grades.
- `efde0a5`: mapped the full product north star and version ladder.
- `60b72f2`: made planning versus implementation authority explicit.
- `ad5de78`: added the capability and claim-licensing dependency graph.
- `fce654e`: added the pre-implementation entry checklist.
- Upstream planning already exists: Qualitative Coding Plan 242, Process Tracing
  Plan 7, and Theory Forge Plan 108. These are plans, not current authorization.

## Current Truth

- Branch: `main`, synchronized with `origin/main` before this handoff.
- Evidence baseline: **0 A, 0 B, 2 C, 5 D, 1 F; overall F**.
- The synthetic fixture seam demonstrates candidate shapes only.
- AC15 is not coupled to Theory Forge or the workbench at runtime. It inherited
  benchmark lineage through AC14 and is, at most, an optional future backend
  experiment after Theory Forge has a stable export.
- There are no critical untracked or ephemeral source files.

## Required Reading Order

1. `docs/PLANNING_STATUS.md` - current authorization boundary.
2. `docs/CAPABILITY_DEPENDENCY_GRAPH.md` - dependency and claim gates.
3. `docs/PRE_IMPLEMENTATION_CHECKLIST.md` - mandatory entry process after a
   named implementation authorization.
4. `docs/ROADMAP.md` - future release sequence.
5. `docs/CONCERNS.md` - unresolved risks.
6. `docs/coverage_report.md` - evidence baseline.
7. `docs/plans/002_engine_stability_and_integration_readiness.md` - historical
   cross-repo findings, not current repo state.
8. `docs/IMPLEMENTING_AGENT_NOTES.md` - concise repo-local guidance.

## Remaining Work, In Dependency Order

### 1. Finish the 0.0 truthful baseline

The immediate safe work is capability `T0`, specifically coverage row
`W2-fixture-inventory`. Define a provenance-complete fixture manifest and an
invariant-specific negative control. It must record source commands, producer
commits, validation results, hashes, caveats, and evidence grades while keeping
all current fixtures explicitly synthetic. Do not promote engine readiness.

### 2. Establish study and source governance

Confirm the first public case. The roadmap recommends the 18 Brumaire packet,
but this remains a proposal. Record corpus denominator, source identities and
hashes, licensing, sensitivity/publication constraints, anchor recovery, and
claim limits before creating real producer fixtures.

### 3. Stabilize the QC export in `qualitative_coding`

Freshly inspect active claims, agent memory, Plans 239/241/242, git state, and
verification commands. Select and validate one canonical export containing
source scope, anchors, codes/categories, claims, patterns or candidate
explanations, review state, provenance, and caveats. Keep likelihoods,
posteriors, verdicts, and comparative support out of QC.

### 4. Stabilize `pt_export_v1` in `process_tracing`

Freshly inspect Plan 7, repo-local checks, and any dirty/untracked workbench
state. Implement the export in that repo with source packet identity, rival
hypotheses, evidence and absence findings, comparative support, sensitivity,
verdict language, caveats, run metadata, schema version, and provenance. The
workbench must not parse `result.json` or import `pt.schemas`.

### 5. Pin real QC/PT fixtures here

After both producer exports pass engine-local tests, import immutable fixture
copies and record producer commits, source hashes, validation commands/results,
supported schema majors, governance, caveats, and licensed claims. Add targeted
negative controls before making any requirement a hard gate.

### 6. Request authorization for release 0.1

Real fixtures do not themselves authorize implementation. Brian must name the
slice or ask to enter implementation. Then run every step in
`docs/PRE_IMPLEMENTATION_CHECKLIST.md` and create a current implementation plan
for typed producer/consumer contracts, compatibility checks, synthesis payload,
and a static reviewer packet. Release 0.1 may claim one auditable
**multi-method qualitative** case, not mixed methods.

### 7. Later, independent tracks

- Release 0.2: evaluate Grounded Research as a contested-claim adjudicator.
- Release 0.3: execute Theory Forge Plan 108 after reconciling v14/v15 and
  identifying one known-green theory export. Theory is analysis context, not
  empirical evidence.
- AC15: optional post-export pilot only. It blocks no workbench release.
- Release 0.4: choose a quantitative-text task and owner, validate it on held-out
  material, then build a joint display and bounded meta-inference. This is the
  first release eligible to claim genuine mixed methods.
- Later releases: additional integration designs, causal/comparative bridges,
  method profiles, governance hardening, interoperability, and independent SOTA
  evaluation follow the capability graph.

## Explicit Uncertainties

### First case and governance

The proposed 18 Brumaire case is not confirmed. Verify source licensing,
complete corpus scope, stable anchors, and publication constraints. This blocks
real QC/PT fixtures and release 0.1.

### Qualitative Coding export

It is unresolved whether the strict QC-to-PT handoff is the right canonical
workbench export or whether a separate consumer-safe QC artifact is needed.

### Process Tracing export

`pt_export_v1` is planned but unproven. Exact numeric-versus-banded comparative
support and source-marker-versus-offset behavior must be decided from real
engine capabilities, not guessed here.

### Theory Forge

Current health, v14/v15 authority, and the first green theory remain uncertain.
Resolve these in Theory Forge before hardening a workbench theory schema.

### Quantitative text

There is no owner, task, instrument, or evaluation design. This is the largest
known gap before the project can honestly become mixed methods.

### Grounded Research and `research_v3`

Grounded Research's internal benchmark does not establish workbench validity.
`research_v3` has conflicting active/archive signals and remains off the
critical path pending an ADR.

## Files That Must Not Be Edited Directly

- `docs/coverage_report.md` and `docs/coverage_report.json` are generated by
  `scripts/check_coverage.py`; change the script's requirement data, then run
  `make coverage`.
- Do not turn Plans 001, 002, or 003 into a current implementation plan. Create
  `docs/plans/current_<slice>.md` only after named authorization.
- Do not edit producer repos from a workbench slice unless Brian explicitly
  includes the owning repo and the active-claim checks are clean.

## Build and Verification

There is no deployed application. This is a planning and fixture scaffold.

```bash
make help
make check
make coverage
git status --short
```

Expected current state: fixture validation and six targeted negative controls
pass; coverage reports `0 A, 0 B, 2 C, 5 D, 1 F`; git status is clean after the
handoff commit.

## Takeover Rule

Start with the `next_action` in `.claude/handoff.yml`. If Brian has not named an
implementation slice, remain documentation-only. Every status inherited from
the June investigation must be rechecked against the current producer repo
before it is used as evidence.
