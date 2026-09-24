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
but still said it contradicted later narratives of a *coherent* speech. One
selected memoir passage does discuss speeches later attributed to Bonaparte;
it does not say those accounts described a coherent speech. The verifier's
categorical rationale that the passages do not address later narratives at all
overstates the gap, although its `partial` disposition remains justified by
the added coherence qualifier. A second corrected finding described execution
as a real possibility where the selected passage supplies a retrospective
conditional account. The corrected pattern inferred a broader tension between
memoir and official narrative beyond what its selected passages established.
These are verifier dispositions and a source-bound review of them, not accepted
historical findings.

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

The method-owned next step is an unpaid review of why the repair retained
unsupported qualifiers and why one verifier rationale overstated the source
gap. The goal allows at most two reproduced attempts at the same blocker per
case. The earlier historical Brumaire QC trial and this independently sourced
trial both stopped at source support; do not treat a third paid Brumaire trial
as an automatic continuation. PT must wait for a source-supported, typed QC
handoff.
