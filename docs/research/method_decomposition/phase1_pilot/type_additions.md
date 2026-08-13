# Pilot type additions

## `analysis_plan`

**Status:** added for this discovery pilot; not promoted to a shared contract.

**Definition:** A prespecified plan for an analysis, evaluation, or empirical
design, including the decisions that must be frozen before relevant results are
inspected.

**Why the existing list did not fit:** `review_protocol` is specific to an
evidence review. Reusing it for an RCT statistical-analysis plan or a policy
evaluation plan would manufacture a false type collision. `configuration` is
too weak because it does not carry prespecification, deviation, or review
semantics.

**Rows using it:** `rct.02`, `pa.12`.

The systematic-review protocol remains `review_protocol`: its review-specific
meaning is real and should not be erased merely to increase collisions.
