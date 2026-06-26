# Plan 001: Fixture-Backed Walking Skeleton

Status: blocked by engine readiness
Created: 2026-06-25
Blocked By: `docs/plans/002_engine_stability_and_integration_readiness.md`

Do not execute this walking skeleton until the readiness gates in Plan 002 pass
for the engines included in the slice. The minimum gate for the original QC/PT
scope is a canonical QC export fixture and a versioned PT export fixture. Theory
Forge is not required for the original QC/PT walking skeleton unless the slice is
explicitly expanded into a theory-enhanced workbench payload.

## Outcome

Create the first vertical, end-to-end workbench slice without moving engine code:
load one completed `qualitative_coding` artifact and one completed
`process_tracing` artifact, normalize them into shared contracts, and render a
static demo/review payload that shows the integrated research path.

## Advances

Turns the integration vision into a testable seam:

```text
engine artifacts -> shared contracts -> workbench synthesis -> review/export mockup
```

## Vertical Scope

- fixture selection from both engine repos;
- artifact hash capture;
- adapter sketch or notebook/script that emits the shared payload;
- static Markdown or HTML demo payload using real fixture data;
- adversarial review against method-boundary failures.

## De-Risks

- Whether QC and PT can share evidence/source/claim contracts without loss.
- Whether the workbench can show an actual research workflow rather than a
  superficial dashboard.
- Whether method caveats survive integration.

## Success Readout

Because this is hybrid, success is partly deterministic and partly exploratory:

- deterministic: payload validates against the shared contract sketch and every
  input artifact hash is recorded;
- exploratory readout: a reviewer can trace one integrated finding from
  research question to source scope, evidence, qualitative claim/pattern,
  process-tracing hypothesis/support, and caveat.

## Acceptance Criteria

- Uses real local fixture data, not invented example values.
- Includes at least:
  - one QC source anchor;
  - one QC analytic claim;
  - one QC pattern or relationship;
  - one PT evidence record;
  - one PT causal hypothesis;
  - one PT comparative-support reference;
  - one source-scope or source-gap caveat from each engine where available.
- Blocks or visibly flags any assertion without evidence.
- Explicitly labels estimands.
- Does not import engine internals directly unless artifact loading proves
  impossible.
- Updates `contracts/shared_contracts.md` with mapping rules learned from the
  fixtures.
- Updates `docs/CONCERNS.md` with all audit findings and dispositions.

## Adversarial Audit

Try to break the slice by checking:

- Can the payload make a causal claim from a descriptive code co-occurrence?
- Can a process-tracing support ranking be mistaken for truth probability?
- Can a QC claim appear without source anchors or a `needs_anchor` limitation?
- Can a source gap disappear in the synthesis?
- Can the review artifact hide which engine produced a claim?

Findings must be fixed, accepted with rationale, or deferred to a named future
slice.

## Cleanup

- Remove invented placeholder payloads or clearly quarantine them as examples.
- Keep generated fixture output in a deterministic `examples/fixtures/` or
  equivalent path only after the source command and caveats are recorded.
- No direct source edits to engine repos unless a separate engine-local plan is
  created.

## Done When

Readout observed, adapter/mapping notes updated, static review payload exists,
adversarial findings dispositioned, concern register triaged, and all scaffold
files are committed in whichever repo owns the scaffold.

## Next Slice Candidates

1. Demo-mode review shell: convert the static payload into a local HTML review
   shell with tabs for scope, evidence, claims, hypotheses, patterns, caveats,
   and export manifest.
2. QC adapter hardening: implement a typed package in this scaffold or a shared
   library that maps one QC project state into shared contracts.
3. PT adapter hardening: implement a typed package that maps one PT result into
   shared contracts.
