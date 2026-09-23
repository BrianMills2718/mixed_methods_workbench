# Fresh native Brumaire QC source-gate run

**Disposition: rejected before synthesis promotion; no PT inference.** This
2026-09-23 Qualitative Coding project ran from the four committed public texts
in [`examples/sources/brumaire-20260923`](../../sources/brumaire-20260923/README.md).
Unlike the earlier posthoc verifier replay, this native project run enabled
`--verify-synthesis-entailment` before synthesis could enter project state.

The generator proposed five findings and four patterns. Their nine selected
passage sets received six `partial` and three `unsupported` verdicts. The first
finding claimed that the Constitution established a broad framework for a
change of authority, but selected only a sentence on temporary replacement of
the First Consul. Another finding about personal interactions and secret
negotiations selected a constitutional sentence on Senate seats. The gate
rejected the first clause and saved `pipeline_status=failed` with no synthesis.

## Inspectable evidence

- `project_state_rejected.json` is the exact saved native state, SHA-256
  `6a95ae3fe4a5c69f8a02932a2cef26ba723e9ace06a7f5ad4d5581f44d584844`.
  It retains the four source texts, coding, and upstream phase results needed
  for a native failed-run resume.
- `candidate_synthesis.json` is the generated but **unpromoted** candidate.
  Its content must not be read as a QC finding.
- `synthesis_entailment_request.json` binds all nine candidate clauses to
  their exact selected applications; candidate digest
  `ddc03e0ea394fd2881f8c3388747010170d3fdcab18eafeb55421d4581683019`.
- `synthesis_entailment_response.json` is the typed independent verdict.
  Identity validation passed; semantic validation rejected the candidate.
- `trace_receipt.json` lists all five calls, model routes, token use, retries,
  costs, revisions, and the rejection. Recorded cost was **$0.00963133**;
  each call had zero retries.

The first CLI attempt lacked a model-route justification and failed before
provider dispatch. The corrected run made the five recorded calls. The local
observability database retains the full raw LLM trace under
`qualitative_coding/project/e9736999-2a6c-49a6-b676-37729c758633`; this
package preserves a source-safe receipt and the exact state needed to inspect
the rejection, not the raw provider transcript.

The method-owned QC correction merged later at `31a9e1f6b2bd958f1266cdd624c9125f1de34207`.
That change allows one source-bound correction and a second independent check
on opt-in runs. It was **not** present in this rejected run. A separately
authorized resume or fresh run must verify whether it produces a supported
handoff before PT starts.
