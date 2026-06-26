# Mixed Methods Workbench Concern Register

Each concern must be dispositioned at slice boundaries: `open`, `resolved`,
`mitigated`, `accepted`, `deferred`, or `escalated`.

| ID | Status | Concern | Why It Matters | Disposition |
|---|---|---|---|---|
| C001 | open | Shared evidence contract may be too weak to represent both QC anchors and PT evidence likelihoods. | A bad seam would force lossy adapters or premature schema churn. | Resolve in Slice 1 by building a fixture-backed contract mockup and adapter readout. |
| C002 | open | The workbench could blur estimands: qualitative claim support, process-tracing comparative support, and cross-case causal effects are different. | False precision would damage the product's methodology claims. | Require method-specific `estimand_kind` and report caveats in every synthesis payload. |
| C003 | open | UI shell could become a superficial dashboard over unrelated artifacts. | The product goal is a research workflow, not a portfolio index. | First mockup must show a concrete data-to-claim-to-hypothesis-to-report path. |
| C004 | open | Cross-repo imports can create dependency cycles or brittle local path coupling. | The workbench needs durable module boundaries. | Use file/artifact adapters first; defer direct library imports until contracts stabilize. |
| C005 | open | "PhD-level research output" is an ambition, not a single deterministic acceptance test. | The plan must not fake a universal quality threshold. | Treat quality as a ladder: structural gates now, expert/frozen-case validation later. |
| C006 | open | The engine repos are not all stable enough to build the workbench against yet. | A workbench slice would either depend on dirty/untracked state or undocumented export gaps. | Execute Plan 002 readiness gates before Plan 001. |
| C007 | open | Theory Forge is not represented in the original QC/PT architecture. | Bolting it on later could confuse generated theory, theory operationalization, and compiled analysis code. | Treat Theory Forge as a dependency subplan and add only a `TheoryOperationalizationArtifact` after a real fixture. |
| C008 | open | AC14/AC15 Theory Forge benchmark evidence could be misused as mixed-methods evidence. | Those benchmarks measure coding-agent/codegen behavior, not qualitative/process-tracing integration utility. | Keep AC15 optional and out of the workbench critical path. |
| C009 | open | `process_tracing` needs a stable export seam before the workbench consumes it. | Parsing `result.json` or importing `pt.schemas` would couple the workbench to internal PT artifacts. | Require `pt_export_v1` before PT adapters. |
| C010 | open | `process_tracing/workbench/` is untracked. | Plans that depend on it would depend on non-durable local state. | Commit, ignore, or archive the directory before using it as evidence. |
| C011 | open | Current `qualitative_coding` worktree dirt may make readiness claims stale. | The prior green check may not describe the current checkout. | Re-check after the dirty files are understood or committed. |
| C012 | open | Theory Forge current health and v14/v15 status are uncertain. | A theory export contract built on stale schema assumptions would churn quickly. | Run a dedicated Theory Forge readiness investigation before adding a workbench theory contract. |
| C013 | mitigated | Synthetic workbench fixtures could be mistaken for engine readiness evidence. | Placeholder JSON can look like a real integrated payload if status, grade, and claim limits are not enforced. | `make check` validates `artifact_status=synthetic_contract_fixture`, `C-synthetic-contract-only`, hashes, and claim limits; real fixtures still require engine-local validation. |
