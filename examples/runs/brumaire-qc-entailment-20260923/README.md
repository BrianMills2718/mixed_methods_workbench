# Brumaire QC semantic-verifier replay

**Disposition: rejected; no PT inference or publishable finding.** On
2026-09-23, an internal, opt-in Qualitative Coding verifier reviewed the six
synthesis claims from a fresh native QC run against only their 16 selected
source applications. The request and typed model response are retained here.
The four exact QC inputs are in the [frozen Brumaire source packet](../../sources/brumaire-20260923/README.md).

This was a **posthoc replay** against an already-completed QC project state.
It demonstrates that QC's method-owned semantic validator rejects the handoff
when invoked; it does **not** show that the ordinary QC project run enabled the
gate before promotion. PT's structural loader accepted the unverified handoff,
so that handoff was deliberately withheld from PT inference.

## Evidence

- `synthesis_entailment_request.json` contains the exact six clauses and 16
  source applications, bound by candidate digest
  `fd29829e8beab861ff53b8674f39a92c47e3696cf3c5286779395db5dc8d094d`.
- `synthesis_entailment_response.json` contains one typed verdict per clause
  and one evidence verdict per selected application. QC identity validation
  passed; semantic validation rejected the first unsupported clause.
- `synthesis_entailment_trace_receipt.json` records the runtime revisions,
  source-state and prompt hashes, model route, trace ID, one successful native
  schema call, zero retries, 4,674 prompt tokens, 1,020 completion tokens, and
  **$0.00239235** recorded cost. The response classified two clauses
  `unsupported`, one `non_atomic`, and three `partial`; none passed.

The first rejected finding purported to describe how the decree and
proclamation framed the coup, but all three selected excerpts were from the
later memoir. The second purported to describe the Constitution while citing
only a memoir passage about troops. The verifier identified both mismatches.

## Limit

The original full QC project state and raw provider trace are in local runtime
storage and are not reproduced here. These retained request/response files make
the exact verifier decision inspectable, but they do not make the full native
QC generation reproducible byte for byte. A connected QC-to-PT proof still
requires a fresh synthesis that passes semantic review before export, followed
by a new PT rival test and independent challenge.
