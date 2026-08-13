# Phase 1 pilot work-unit graph

Profile: small, documentation/research only

Goal: independently stress the frozen method-decomposition format across five
materially different methods and one hostile counterexample, then integrate the
results without beginning capability selection or the broader portfolio.

Design input: frozen frames and sources at Git revision `4d25074`.

## Graph

```text
4d25074 frozen frames + sources
  ├─ P1-SR  systematic review ───────┐
  ├─ P1-GT  grounded theory ─────────┤
  ├─ P1-PT  process tracing ─────────┤
  ├─ P1-RCT randomized estimation ───┼─> P1-INTEGRATE
  ├─ P1-PA  policy appraisal ────────┤       │
  └─ P1-SIM hostile simulation ──────┘       └─> stop before Phase 2b/3
```

## Independent research units

All six units have execution class `independently_executable`, availability
`ready_for_execution`, class `research`, and no file-write surface. Each reads
only its frozen method frame and named sources and returns a report to the
integration owner. Each is accepted when it supplies 8–20 source-linked
operations, a directed topology, method-owned judgments, supported and refused
conclusions, and explicit schema stresses. Inspecting the integration draft,
colliding methods, selecting shared capabilities, or editing repository files
is excluded.

| Unit | Exclusive subject | Representative disproof/control |
| --- | --- | --- |
| `P1-SR` | systematic intervention-effect review | do not treat PRISMA reporting as the conduct method or force pooling |
| `P1-GT` | constructivist grounded theory | preserve concurrent cycles and do not claim fixed-corpus saturation |
| `P1-PT` | theory-testing process tracing | keep evidence rival-relative and permit an unresolved result |
| `P1-RCT` | two-arm randomized causal-effect estimation | make outcome-informed redesign a disclosed deviation, not a loop |
| `P1-PA` | Green Book policy option appraisal | keep value judgments visible and allow no robust preference |
| `P1-SIM` | ODD agent-based policy simulation | do not treat simulated output as observed policy-world evidence |

The original six reports were transient coordination outputs. That choice made
the historical 90-operation claim unauditable. Fresh independent audit reruns
are now durably normalized in `blind_reruns/step_inventory.yaml`; they are
explicitly labeled reruns rather than reconstructions of the unavailable
originals. The integration lane remains the sole repository writer.

## Integration unit

`P1-INTEGRATE` has execution class `coupled`, class `integration`, and is owned
by the current claimed session. Its hard evidence dependencies are the six
completed reports. Its exclusive write surface is
`docs/research/method_decomposition/phase1_pilot/` except the already frozen
`pilot_frame.md` and `sources.md`.

Acceptance requires:

1. every accepted independent finding is represented or its rejection is
   explained;
2. the combined ledger parses, uses unique step IDs and controlled verbs/types,
   and preserves named input/output roles;
3. every graph edge resolves and method topology preserves required and
   prohibited cycles;
4. the memo reports schema stresses and uncertainties without adjudicating
   collisions, calculating global reuse, or recommending shared infrastructure;
5. the branch is committed and pushed, then work stops before Phase 2b/3.

Failure rule: if the independent lanes materially disagree on the frozen method
or expose a representation that the pilot schema cannot express without loss,
retain the disagreement and mark the affected row unresolved. Do not repair it
by silently broadening a type or inventing a universal abstraction.
