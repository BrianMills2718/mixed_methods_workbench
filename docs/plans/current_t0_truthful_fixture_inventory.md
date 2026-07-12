# Completed Plan: T0-PROV Truthful Fixture Inventory

Status: completed and independently signed off
Date: 2026-07-12
Capability row: `T0` subcriterion `T0-PROV`
Coverage row: legacy ID `W2-fixture-inventory`

## Mission and Outcome

Make the existing hand-authored synthetic fixture inventory complete,
recoverable, and evidence-derived without implying that the fixtures came from
method engines or that all of T0/0.0 is complete.

One-sentence outcome: changing, omitting, inventing, or failing to inventory the
provenance evidence changes the W2 result and fails for the intended reason,
while every underlying fixture remains C-grade synthetic evidence.

## Closure Record

- Evaluated commit: `f26bc6ade93c475c7ebc4ca608e796a9b9fe2f1a`.
- Independent decision: **SIGNED-OFF**.
- Decision artifact: `docs/runs/2026-07-12-t0-prov-eval-signoff.md`.
- Final scaffold coverage: 1 A, 0 B, 2 C, 5 D, 0 F; overall D.
- Licensed scope: W2 synthetic inventory provenance only. Fixture contents
  remain C; broader T0/0.0 and the program score remain F; no later slice is
  authorized.

## Authorization Record

```yaml
authorized_slice:
  instruction: |-
    Handoff supplied by Brian: “close the T0 provenance-complete fixture inventory gap without starting engine integration.”
    Brian's direct instruction: “please inveistgae and set up clear long term plans then proceed until the mixed method work bench is sota or beyond in all areas”
  target_capability_row: "T0 subcriterion T0-PROV; coverage row W2-fixture-inventory"
  target_release_or_dependency: "0.0 truthful-evidence-baseline subslice only"
  in_scope:
    - mixed_methods_workbench fixture manifest and README
    - fixture provenance/inventory validation
    - invariant-specific negative controls
    - evidence-derived W2 coverage row
    - current planning, concern, and generated coverage documents
  out_of_scope:
    - qualitative_coding, process_tracing, theory-forge, grounded-research
    - real producer exports or a public research case
    - production Pydantic schemas or semantic engine validation
    - adapters, orchestration, API, UI, MCP, or evaluation harness
    - every other T0/0.0 subcriterion and all later capability rows
    - engine-readiness, methodological-validity, mixed-methods, or SOTA claims
  claim_to_license: "The current synthetic fixture directory has a complete, Git-recoverable, freshly validated provenance inventory whose W2 evidence changes when its proof changes."
  required_evidence_grade: "A for T0-PROV/W2 only (source plus discriminating tests); fixture shape remains C and T0 remains partial."
```

Interpretation: the handoff by itself is not authorization. Brian supplied it
as the named starting action and directly said “then proceed,” satisfying the
checklist's “asks to move ... into implementation” clause for this reversible
local subslice. The broader SOTA objective does not activate another row.

## Entry-Gate Readout

| Gate | Result | Evidence / consequence |
|---|---|---|
| Authorization | Pass for `T0-PROV` only | Exact text and interpretation above; canonical exception in `docs/PLANNING_STATUS.md`. |
| Repository state | Pass | Work began from clean synchronized `main` at `6be0a89` in in-repo worktree branch `goal-sota-program`; current dirt is this planned slice. No active claim named the repo. |
| Authority reconciliation | Pass when this doc increment is verified | ADR 0003, roadmap, capability graph, status, goal map, and scorecard resolve the material planning conflicts found in the investigation. |
| Dependencies | Pass | `AUTH` is documented. No producer, source case, or real fixture is a dependency for truthful provenance of hand-authored synthetic artifacts. |
| Upstream freshness | Not applicable, independently approved by scope | Producer repos are read-only and no engine behavior is claimed. Fresh read-only state is recorded in `.claude/tasks/research_producer_readiness.md`. |
| Evidence baseline | Pass | `make check` and `make coverage` reproduced 0 A, 0 B, 2 C, 5 D, 1 F before the slice. |
| Modality | Deductive | Inventory completeness, hash recovery, origin truth, and grade derivation have deterministic pass/fail behavior. |

## Contract

### Current supported origin

Every current fixture entry declares:

```text
path
sha256
evidence_grade = C-synthetic-contract-only
origin_kind = workbench_synthetic
authoring_repository
last_content_commit
authoring_path
recovery_command
creation_method
intended_invariant
claim_limits
```

`last_content_commit` is the exact most recent Git commit that changed the
fixture bytes, not arbitrary current `HEAD`. The validator must confirm:

```text
git log -1 --format=%H -- <authoring_path> == last_content_commit
sha256(git show <last_content_commit>:<authoring_path>) == sha256(current bytes)
recovery_command == git show <last_content_commit>:<authoring_path>
```

The code supports only `workbench_synthetic` in this slice and fails loudly on
another origin kind. A future real-export slice may add a discriminated
`engine_export` variant with producer repository/commit, generation command,
package hash, and engine-local validation. Implementing that unused path now
would be hypothetical scope expansion.

### Validation observation

The manifest also records one observation bound to the same bytes:

```text
command
control_commands
control_sha256
control_result = pass
evidence_deriver_path
evidence_deriver_sha256
validator_path
validator_sha256
observed_at
result = pass
validated_file_hashes[path] = entry.sha256
```

This stored assertion cannot license itself. `make coverage` must first execute
the validator and inventory negative controls, and the coverage program must
derive W2 from the current manifest, current fixture bytes, current validator
bytes, current control and evidence-deriver bytes, and Git history. A stale
recorded observation fails.

Freshness is licensed by that live re-execution, not by the age of the stored
timestamp. `observed_at` is historical provenance: it must be timezone-aware,
must not predate manifest creation, and must not be in the future. There is no
arbitrary maximum-age threshold because every coverage derivation reruns the
current validator over current bytes.

### Inventory boundary

The inventory is exhaustive, at any depth and with case-insensitive `.json`
extension matching, over every JSON-like artifact in
`examples/fixtures/workbench_contract_v1/` except `manifest.json` itself. An
unlisted extra JSON file and a listed missing file both fail. The manifest is
excluded to avoid self-hash recursion. Symlinks are rejected so traversal has
one unambiguous boundary; malformed JSON and duplicate object keys also fail
with normalized diagnostics.

## Acceptance Criteria and Evidence

| ID | Pass condition | Final evidence | Closure | Verification |
|---|---|---:|---:|---|
| T0P-1 | Canonical status records the exact authorization and limits it to this repo/subcriterion. | D/current and reviewed | Achieved | Documentation audit and exact-text comparison. |
| T0P-2 | Every current JSON artifact except the manifest is listed exactly once; no extra/missing/unlisted artifact passes. | A/test | Achieved | Real directory scan plus missing-entry and unlisted-extra controls asserting exact diagnostics. |
| T0P-3 | Every entry truthfully declares synthetic origin, invariant, file-specific claim limits, and C grade. | A/test | Achieved | Validator plus missing-origin, unsupported-origin, missing-limit, and grade-escalation controls. |
| T0P-4 | Each current byte sequence is recoverable from its exact last-content Git commit and path. | A/test | Achieved | Live `git log`/`git show` checks plus wrong-commit and changed-byte controls. |
| T0P-5 | Validation metadata is bound to the same file, validator, control, and evidence-deriver hashes and is re-executed before coverage generation. | A/test | Achieved | Fresh positive run plus stale file, validator, control, and evidence-deriver hash controls. |
| T0P-6 | W2 grade and notes are computed from evidence rather than a fixed grade declaration. | A/test | Achieved | Evidence-present readout is A; temporary missing-evidence and malformed-JSON lanes both render a complete report with W2/overall F and the intended diagnostic. |
| T0P-7 | Promotion remains bounded: fixtures stay C, T0 remains partial, overall report has unresolved D rows, and no producer/SOTA wording appears. | A/test for containment | Achieved | Assertions over generated JSON/Markdown plus adversarial documentation review. |

An A for T0P/W2 is possible because its bounded claim has direct Git source
evidence and discriminating runtime tests. It says nothing about the truth of
synthetic research content. Passing W2 removes the single F row in the current
eight-row scaffold report, but it does not close T0 or 0.0; the expected overall
grade becomes D while the two fixture-shape rows remain C.

## Implemented Slices

1. **Manifest truth:** add the current synthetic-origin and validation metadata
   without changing fixture payloads.
2. **Fail-loud validation:** enforce exhaustiveness, per-entry provenance, exact
   Git recovery, byte/hash binding, and current-validator binding.
3. **Discriminating controls:** add one control per promoted invariant and keep
   unrelated integrity/provenance gates neutral for semantic controls.
4. **Derived coverage:** calculate only the W2 row from evidence; make coverage
   execute its prerequisite positive/negative checks.
5. **Readback and audit:** regenerate both reports, inspect exact grades/claims,
   run an independent adversarial review, disposition findings, and update the
   concern/progress/handoff surfaces.

Each verified slice is a separate commit and normal push. Do not batch a later
capability into these commits.

## Failure Modes and What to Try Next

| Failure | Diagnosis | Next action |
|---|---|---|
| Git recovery fails for unchanged fixture | Wrong commit/path or dirty fixture bytes. | Use `git log -1 -- <path>` and compare `git show` bytes; never substitute current HEAD. |
| Semantic control fails at provenance first | Test mutation changed bytes without neutralizing the source-only gate. | Explicitly disable repository-provenance verification only in that semantic test helper; retain hash and validation binding and test provenance separately. |
| Unlisted artifact passes | Directory boundary is based on a fixed required set or case-sensitive glob. | Compare every recursively discovered case-variant `.json` artifact except `manifest.json` with the manifest set in both directions. |
| W2 remains A after evidence removal | Grade is still declarative or stale. | Move the predicate into one evidence-assessment function and have the control call the same function. |
| Coverage aborts on malformed evidence | Parser failures bypass the evidence-grade surface. | Normalize parse failures and assert the complete report renders W2/overall F. |
| Stored `result=pass` is sufficient by itself | Self-attestation is being trusted. | Bind every evidence program by hash, execute the controls inside live derivation, and derive from current bytes/history. |
| Existing fixture grade rises above C | Inventory proof is being confused with real-content proof. | Fail loudly and restore `C-synthetic-contract-only`. |
| Change requires engine semantics or real producer data | Slice crossed into W1/QCX/PTX/TFX. | Stop that change and author a separately authorized plan. |

## Commands and Expected Readout

```bash
make help
make check
make coverage
make coverage-json
git diff --check
git status --short --branch
```

Final readout:

- fixture validation passes;
- every negative control reports its full count and passes only by catching the
  intended diagnostic;
- coverage distribution is 1 A, 0 B, 2 C, 5 D, 0 F; overall D;
- `W2-fixture-inventory` is A/test and explicitly bounded to synthetic inventory
  provenance;
- no fixture or method capability is promoted above its existing grade.

## Adversarial Audit

The reviewer must try at least:

- unlisted extra JSON;
- nested case-variant/dotfile JSON, symlinks, malformed JSON, and duplicate keys;
- duplicate and missing manifest entry;
- missing and unsupported `origin_kind`;
- current HEAD substituted for exact last-content commit;
- a commit/path whose recovered bytes differ;
- stale validation file hash and stale validator hash;
- stale control and evidence-deriver hashes;
- alternate or unknown claim-bearing fields;
- `result=pass` with a broken fixture;
- evidence grade changed to A;
- direct call to coverage after evidence removal;
- wording that implies engine, method, mixed-methods, or full-T0 readiness.

The audit must inspect the raw generated reports and temporary-control errors,
not only `make check`'s exit code. Findings update `docs/CONCERNS.md` before
closure.

## Stop Conditions

Stop and request direction only if the slice requires:

- changing a producer repository or fixture payload semantics;
- selecting a real source case or quantitative-text owner;
- adding production schemas, an adapter, API, UI, or benchmark machinery;
- changing the claim from inventory provenance to engine/method readiness;
- an irreversible shared-state operation.

Ordinary test failures, documentation drift, and a failed negative control are
not stop conditions; diagnose, record, and repair within this slice.
