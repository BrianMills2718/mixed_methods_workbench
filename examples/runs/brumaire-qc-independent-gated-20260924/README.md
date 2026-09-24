# Fresh Brumaire QC trial from independently acquired sources

**Disposition: rejected before synthesis promotion; no QC handoff or PT run.**
This is the single native project run Brian approved up to $0.05. It used the
four committed, hash-verified texts in
[`examples/sources/brumaire-independent-20260923`](../../sources/brumaire-independent-20260923/README.md),
not the earlier Napoleon Series site-extracted packet. The project ran with the
opt-in independent synthesis entailment gate and its one allowed correction.

The first candidate had five material clauses: one supported, three partial,
and one unsupported. The corrected candidate had four: one supported and three
partial. The second independent verdict rejected the corrected candidate at
`finding:1:clause:0`, so the project persisted `pipeline_status=failed`,
`current_phase=synthesis`, and `synthesis=null`. The supported clause was **not**
promoted separately. No process-tracing inference was started.

The recurring failure was a claim that crossed beyond its selected passages.
The correction narrowed Bourrienne's account of Bonaparte's confused remarks,
but still said it contradicted unspecified later narratives of a coherent
speech. The selected memoir passages describe the remarks; they do not contain
those later narratives. A second corrected finding described execution as a
real possibility where the selected passage supplies a retrospective
conditional account. The corrected pattern also inferred a broader tension
between memoir and official narrative beyond what its selected passages
established. These are verifier dispositions, not accepted historical findings.

## Inspectable evidence

- `project_state_rejected.json` is the exact saved native project state. Its
  SHA-256 is `68c58f5f83b1370d221446925b622e21afa6a2ccce0db93ab61183d25898c991`.
  It embeds the four input texts, coding, and completed upstream stages.
- `initial_candidate.json` and `repaired_candidate.json` are normalized but
  **unpromoted** synthesis candidates reconstructed from the stored LLM
  responses using the exact QC runtime. They must not be presented as results.
- `initial_request.json` / `initial_verdict.json` and
  `repaired_request.json` / `repaired_verdict.json` bind every material clause
  to exact selected passages and the typed independent verdict. Rebuilt
  request digests matched the stored verifier response digests:
  `fd51794a0255319f7bd68aecfd32ebc2102edad27203289764a9b969d3f18e8b`
  and `610e03e8f8574833729410290b56107402852c29e03fc4d27ec72bdb442cb691`.
- `trace_receipt.json` lists seven semantic calls, model routes, tokens,
  retries, costs, exact revisions, and the terminal rejection. The local
  `llm_client` trace is
  `qualitative_coding/project/7de016ba-2295-40c1-bd8a-b977188762be`.
  All seven calls completed without retry or provider error; aggregate cost
  was **$0.0181869288**, below the authorized $0.05 ceiling.

The useful next experiment is a method-owned QC correction that prevents the
repair from retaining unsupported comparisons or stronger modal claims. It
requires its own verification on this saved state and a new spend approval
before any paid replay. PT must wait for a source-supported, typed QC handoff.
