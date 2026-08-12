# Independent decomposition comparison rubric

Status: frozen comparison procedure; no capability adoption

Updated: 2026-08-12

## Decision this supports

When the separately produced decomposition is frozen, compare it with the Codex
Phase 0 candidate without treating either vocabulary or graph shape as the
answer. The comparison decides which apparent similarities are credible reuse
hypotheses and which remain method-owned or unresolved. It does not select a
universal schema or authorize implementation.

## Comparison unit

Compare the smallest meaning-preserving operation available in both candidates.
Each comparison must inspect:

- precise method and workflow variant;
- operation and named input/output roles, types, and cardinalities;
- preconditions, refusal behavior, and terminal outcomes;
- actor transition: human, LLM, deterministic software, or combination;
- required topology: sequence, branch, loop, feedback, or fan-out;
- method-owned judgment and forbidden generic substitutions;
- implementation status and supporting code, test, fixture, or document;
- information preserved, transformed, or lost at the boundary.

Labels alone are never enough to establish equivalence.

## Classification

Assign exactly one provisional class to each compared operation:

| Class | Meaning | Permitted next disposition |
| --- | --- | --- |
| `shared_operation` | Inputs, outputs, control behavior, actor boundary, and semantic obligations materially agree. | Candidate for reuse behind one contract. |
| `shared_shell_method_refinement` | Generic orchestration or validation agrees, but the analytic judgment and validity rules remain method-owned. | Reuse the shell; keep separate method profiles or owners. |
| `method_local` | The operation is constitutive of one method or has no meaningful counterpart. | Keep local; expose only a typed boundary if another consumer needs it. |
| `name_collision` | Similar labels conceal different operations or inferential force. | Rename or namespace; never merge. |
| `signature_mismatch` | The operation is related, but roles, cardinality, state, scope, or loss behavior differ materially. | Split or define an explicit adapter only after a real seam requires it. |
| `topology_mismatch` | Similar steps occupy materially different branch, loop, sequence, or feedback roles. | Preserve separate workflow semantics. |
| `evidence_mismatch` | One candidate claims executable behavior that the other records as manual, planned, or unsupported. | Recheck source evidence before architecture discussion. |
| `unresolved` | Available evidence cannot distinguish the above classes. | Defer; record the exact missing evidence or method-owner decision. |

## Adjudication record

For every proposed match, retain:

```yaml
candidate_a_ref:
candidate_b_ref:
classification:
shared_invariants: []
material_differences: []
source_refs: []
method_owner_review_needed:
provisional_disposition: reuse | refine | keep_local | rename | split | defer
unresolved_evidence: []
```

Do not calculate a single similarity or coverage score. Report counts by class,
by method, and by implementation status so over-decomposed workflows do not
appear more reusable merely because they contain more rows.

## Acceptance rules

A shared capability may be recommended only when:

1. both candidate operations have pinned source evidence;
2. named roles, cardinalities, actor boundaries, topology, refusal behavior,
   and preserved information agree or have an explicit compatible refinement;
3. no method-owned judgment is moved into the shared layer;
4. the recommendation states what remains method-specific;
5. a concrete producer/consumer seam would benefit from the shared boundary.

Otherwise retain the operation as method-local, split it, or mark it unresolved.
Disagreement between decompositions is evidence to inspect, not an error to
average away.

## Next gate

Begin reconciliation only after the independent candidate identifies its source
revision, variants, artifacts, and completion state. The next artifact should be
one comparison table using this rubric. RAND catalog expansion, generalized
contracts, capability implementation, and additional method fixtures remain
outside this gate.
