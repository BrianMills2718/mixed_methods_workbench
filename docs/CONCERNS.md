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

