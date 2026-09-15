---
plan_id: "mixed_methods_workbench#current-simulation-to-policy-appraisal-probe"
dependencies: []
dependencies_reviewed: "2026-09-15"
---
# Authentic simulation-to-policy-appraisal boundary probe

Status: active bounded implementation plan

## Authorization and profile

```yaml
authorized_slice:
  instruction: >-
    Brian approved the recommended next stress test: take one real simulation
    comparison into policy appraisal while preserving that it is
    model-conditional generated evidence rather than an observed real-world
    effect.
  target_capability_row: SIM-APPRAISAL-PROBE (dependency-resolution slice;
    no existing release row claims this boundary)
  target_release_or_dependency: method-capability discovery
  in_scope:
    - mixed_methods_workbench consumer contract and adapter
    - pinned projection of three authentic Cybernetic Influence retained runs
    - one local JSON route and browser review surface
    - focused positive and negative tests
  out_of_scope:
    - Cybernetic Influence producer changes
    - shared schema or Data Contracts adoption
    - live simulation execution or model calls
    - policy recommendation, effect estimate, probability, or empirical validation
    - deployment
  claim_to_license: >-
    The Workbench can consume one pinned authentic simulation comparison as a
    explicitly model-conditional policy-appraisal input and can refuse to turn
    it into a real-world policy recommendation.
  required_evidence_grade: >-
    authentic/observed for the retained producer runs; A/test for the local
    consumer contract, corruption controls, API, and browser projection
```

- Design depth: Standard.
- Execution profile: private functional PoC.
- Overlays: exploratory boundary probe, runtime artifact, UI, repository
  governance.
- Landscape disposition: linked to the reconciled method-decomposition work
  and Cybernetic Influence's retained-run authority.

## Objective and visible result

An analyst opens one page and sees:

1. the policy-design question: whether a verified 48-hour allocation package
   deserves further investigation as part of a regional outbreak protocol;
2. three authentic retained simulation conditions and exact run identities;
3. what changed inside the model;
4. the narrow model-conditional consequence the comparison supports;
5. an explicit refusal to recommend real-world adoption from simulation alone;
6. the empirical, legal, operational, distributional, and cost evidence still
   required.

The stable example is the clean 12-role Cybernetic Influence outbreak triad:

| Condition | Run | Retained simulated outcome |
| --- | --- | --- |
| Baseline | `run_8924342b56ce` | 12 support; joint response approved |
| Capacity conflict without stabilization | `run_946a10a820fc` | 1 conditional, 11 defer; no joint response |
| Same conflict plus verified allocation package | `run_05acbaea1137` | 12 support; joint response approved |

## Current truth and authority boundary

- The three runs are authentic live LLM simulations retained by Cybernetic
  Influence and remain readable from its public comparison API.
- Cybernetic Influence commit `eaa49adf398df718249c7828061722d3285b619a`
  was clean when inspected on 2026-08-13.
- The public route is useful observational evidence but is not a declared
  strict producer export. This probe therefore freezes a compact projection
  plus the three complete source rows, with the source URL, inspected repository
  revision, retrieval time, exact run IDs, and SHA-256 of each canonicalized
  full source row. The rows do not embed the commit that produced them, so that
  revision remains explicitly unavailable.
- The Workbench owns the permissive typed consumer and all appraisal meaning.
  It does not import Cybernetic Influence internals or claim that the probe is
  an adopted cross-project contract.
- Project Meta currently lacks a current `cybernetic_influence_v3` graph record
  while the repository's own goal treats V3 as the active product line. The
  probe avoids mutating or assigning lifecycle authority to that repository;
  this governance drift remains visible rather than being resolved here.

## Domain rules

1. Every simulation input is labeled `model_generated`, never observed,
   experimental, or estimated real-world evidence.
2. Every run remains bound to its exact scenario, condition, model/runtime
   metadata, and complete source row. The later inspected repository revision
   is recorded separately from the unavailable run-producing commit.
3. The comparison may support only this statement:

   > In these retained simulated conditions, the modeled capacity conflict
   > coincided with loss of approval, and adding the modeled verified allocation
   > package coincided with restored approval.

4. The comparison does not isolate a real-world causal effect, establish an
   outcome probability, validate the model, estimate costs, establish legal
   authority, or resolve distributional and operational feasibility.
5. The appraisal result is `insufficient_for_recommendation`. Its permitted
   action is `investigate_design_candidate`.
6. A missing run, duplicate condition, wrong scenario, non-live execution,
   incomplete run, changed digest, incompatible model metadata, or invented
   observed-evidence label fails loudly.
7. The baseline is context, not a policy option. The capacity conflict and
   stabilization are modeled conditions, not automatically feasible choices.
8. A human decision authority remains outside this fixture.
9. The page shows one selected run per condition. It is not a random sample or
   an estimate of frequencies, probabilities, or effects within the simulator.

## Typed boundary

```text
pinned Cybernetic Influence source projection
  -> strict fixture integrity and semantic validation
  -> workbench-owned model-conditional consequence
  -> policy-appraisal boundary check
  -> investigate design candidate | insufficient for recommendation
  -> JSON and browser projections of the same typed artifact
```

The fixture-local consumer models require:

- source API URL, retrieval timestamp, producer repository, later inspected
  repository revision, unavailable embedded producer revision, and projection
  digest;
- three exact run records with source-row digests;
- three complete pinned source rows from which every compact field is derived;
- scenario, condition, execution, model metadata, final simulated decisions,
  outcome, requests, risks, and stabilization event;
- applicability boundary and prohibited inferences;
- one derived model-conditional consequence;
- appraisal status, permitted use, evidence gaps, and non-claims.

No field is promoted to a shared schema.

## Failure behavior

| Failure | Behavior |
| --- | --- |
| Fixture bytes do not match packet digest | Refuse to serve the artifact |
| Required run/condition is missing or duplicated | Pydantic validation failure |
| A run is not completed, live, regional-outbreak, or 12-agent | Pydantic validation failure |
| Retained outcomes do not match the narrow comparison | Pydantic validation failure |
| Any projected field differs from its complete hashed source row | Refuse to serve the artifact |
| Appraisal recommends adoption or calls the evidence observed | Pydantic validation failure |
| Browser/API drift | Focused parity test fails |
| Public producer later changes | Historical fixture remains readable; a new capture requires a new version and review |

## Acceptance and disproof

The slice passes when:

- the fixture validates, retains the three complete source rows, recomputes
  their exact hashes, and derives every compact projected field from them;
- the model derives only the frozen model-conditional consequence;
- the conclusion is visibly `insufficient_for_recommendation` with concrete
  next evidence;
- mutation tests reject an observed-evidence label, a swapped outcome, a
  duplicate condition, and a changed fixture digest;
- one local route and one browser page use the same typed artifact;
- an authentic re-fetch confirms the three pinned source rows still match or
  records drift without rewriting the fixture;
- no Cybernetic Influence files, shared schemas, deployments, or model calls
  are changed.

The slice is disproved if a useful appraisal cannot be represented without
either treating model output as real-world evidence or inventing a generic
cross-method result schema.

Passing proves one bounded transforming handoff. It does not prove the
simulation is valid, the intervention works, the policy should be adopted, or
the boundary is ready for shared infrastructure.

## Thin implementation slice

This is one vertical slice, fully specifiable now:

1. freeze the compact authentic comparison fixture, its three complete source
   rows, and truthful custody metadata;
2. implement the fixture-local Pydantic consumer and derived refusal result;
3. expose matching JSON and plain-language browser views in the existing
   Method Dashboard service;
4. run focused positive, corruption, API/UI-parity, and live source-drift
   checks;
5. record the bounded result and return the repository to a clean pushed state.

No producer integration is activated. A future producer-owned export is
conditional on a second consumer need and resolution of V3 repository
governance.

## Concern dispositions

- Existing C004 (cross-repo coupling): mitigated here through a frozen file
  projection and no producer import.
- Existing C006/C025 (no strict producer export / typed validation): remains
  open; this consumer probe must not be described as producer readiness.
- New bounded concern: Project Meta lacks a current V3 lifecycle record. Defer
  lifecycle correction to Project Meta; do not change it inside this slice.
- New bounded concern: simulation-only consequence evidence is insufficient for
  recommendation. Resolved in this slice by a typed refusal state.

## Consulted sources

- `CLAUDE.md`, `docs/PLANNING_STATUS.md`, `docs/ROADMAP.md`,
  `docs/CAPABILITY_DEPENDENCY_GRAPH.md`,
  `docs/PRE_IMPLEMENTATION_CHECKLIST.md`,
  `docs/MIXED_METHODS_CAPABILITY_MAP.md`, and `docs/CONCERNS.md`;
- `docs/research/method_decomposition/phase1_revision/`;
- Cybernetic Influence `README.md`, `docs/GOAL.md`, `docs/ROADMAP.md`, the
  public `/api/regional-outbreak-comparison` response, and repository revision
  `eaa49adf398df718249c7828061722d3285b619a`.

## Next-skill handoff

```yaml
next_skill: work-unit-graph
reason: adopted cross-project boundary probe is ready for implementation-unit analysis
required_inputs:
  - this plan revision
  - Cybernetic Influence inspected repository revision eaa49adf398df718249c7828061722d3285b619a; run-producing commit unavailable
  - exact three-run source projection and hashes
```
