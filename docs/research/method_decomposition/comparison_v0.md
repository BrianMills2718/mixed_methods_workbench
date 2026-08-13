# Phase 0 decomposition comparison

Status: `reconciliation_candidate`; no capability or schema adoption

Compared:

- code-derived candidate introduced at `ac27ab2`, with the reviewed correction
  merged at `c3d31aac`;
- independently produced candidate corrected at `7a9e40b` and reverified for
  the two Process Tracing workflows at `0747889`;
- Process Tracing evidence pinned to clean commit `4450d2e`.

## Decision

The candidates are complementary, not competing replacements. The code-derived
candidate is the stronger account of the software's actual control flow. The
independent candidate is the stronger account of method-meaningful operations,
manual judgment, and omissions. Neither should become a universal capability
schema.

The comparison supports three narrow architectural conclusions:

1. Reuse a small orchestration shell for source identity, typed input/output,
   validation, review state, lineage, refusal, and projection.
2. Keep coding judgments, diagnostic causal appraisal, theory compilation,
   prediction logic, and policy valuation method-owned.
3. Test proposed shared operations through real producer/consumer seams; labels
   such as `review`, `test`, `construct`, and `estimate` are not evidence of
   semantic equivalence.

## Adjudication table

Each row is a meaning-level comparison, not a row-count alignment. `A` refers
to the code-derived candidate and `B` to the independent candidate. Source
references point to step IDs in `codex_phase0/steps.yaml` and
`claude_phase0/step_ledger.yaml`.

For the rubric's remaining adjudication fields: `method_owner_review_needed`
is the owning methodologist for every `shared_operation`,
`shared_shell_method_refinement`, `signature_mismatch`, or `name_collision`
row (GT/QC, Process Tracing, Theory Forge plus a substantive theory owner, or
policy appraisal respectively). `provisional_disposition` is stated in each
row's final column. `unresolved_evidence` is empty except for the three
`evidence_mismatch` rows, whose missing replay is stated in that column.

| Area | Candidate A | Candidate B | Class | Shared invariants | Material difference / disposition |
| --- | --- | --- | --- | --- | --- |
| GT source units | `qc_gt.01-.02` | `qc_grounded_theory.01` | `signature_mismatch` | Stable corpus/source units enter analysis. | A loads and selects pre-existing units; B requires segmentation. Preserve segmentation as a producer-owned prerequisite. |
| GT initial analysis | `qc_gt.03-.04` | `.02`, `.04`, `.05`, `.07`, `.08` | `signature_mismatch` | Source-grounded theory objects are constructed and validated. | A emits a composite proposal; B separates open coding, categories, axial/selective integration, and propositions. Do not call the composite step a shared coding operation. |
| GT constant comparison | `qc_gt.09-.11` | `.03` | `shared_operation` | New incidents are compared with the evolving account and revisions are checkpointed. | A batches and checkpoints the loop; B names the method operation. Candidate for a method-owned GT contract, not a generic comparator. |
| GT memos | embedded in `qc_gt.03/.10` | `.06` | `signature_mismatch` | Analytic rationale is retained. | B treats memo writing as an operation; A embeds it in larger proposal/revision outputs. Keep memo identity explicit before claiming equivalence. |
| GT proposition appraisal | `qc_gt.05-.07`, `.12-.14` | `.09-.11` | `shared_shell_method_refinement` | Evidence pools, negative cases, and adequacy limits inform reviewed propositions. | B separates negative-case analysis, computed adequacy, and a human adequacy decision; A appraises a composite theory/corpus. Share targeting and review envelopes only. |
| GT theoretical sampling | no fixed-corpus counterpart | `.12` | `method_local` | — | The current A variant is deliberately fixed-corpus. B correctly records targeted next-data selection as incomplete. Do not manufacture a match. |
| GT cross-method handoff | no decomposition step | `.13`, `.15` | `method_local` | — | B includes QC→PT and PT→QC boundaries; A froze only the internal GT workflow. Retain as explicit integration boundaries. |
| PT run design, exposure, priors, coverage | `pt.01-.04`, `.09-.10` | no direct rows | `method_local` | — | A exposes critical inference-design controls that B's ideal operation list omits. Preserve them as PT-owned controls. |
| PT causal inventory | `pt.03` | `pt_core_rival_explanation.01` | `shared_operation` | Source-grounded actors, events, evidence, mechanisms, and edges are extracted. | Same method and role; keep PT's causal-evidence schema and provenance requirements. |
| PT rivals | `pt.02`, `.05-.06` | `.02` | `shared_shell_method_refinement` | Rival explanations and observable implications are made explicit and reviewed. | A distinguishes theory-first freezing from exposed-evidence construction; B collapses them. Share lifecycle shape, not inferential status. |
| PT partition gate | `pt.07-.08` | `.03` | `shared_shell_method_refinement` | Rival pairs require discriminating predictions and can block progress. | A makes repair topology explicit; B records the gate as one classification. Preserve PT-owned adequacy and repair rules. |
| PT diagnostic classification | `pt.16` | `.04` | `name_collision` | Both describe diagnostic evidence. | A derives a rival-pair matrix from likelihoods; B stores Van Evera labels that are currently numerically inert. Never merge these because both say “diagnostic.” |
| PT likelihood appraisal | `pt.11-.12` | `.05` | `shared_shell_method_refinement` | Evidence is appraised across all rivals and material splits are audited. | A separates elicitation and independent audit; B names the combined estimate. Keep elicitation/audit PT-owned. |
| PT source silence | `pt.13-.14` | `.06` | `shared_shell_method_refinement` | Missing predicted evidence is represented with source-opportunity limits. | A has a distinct admission audit; B's row is coarser. Share the reviewed finding envelope only. |
| PT comparative update | `pt.15` | `.07` | `shared_operation` | Audited likelihood vectors feed deterministic log-space comparative updating. | Same method-owned calculation; never generalize it into a cross-method confidence score. |
| PT structural critic | `pt.20` | `.08` | `shared_operation` | A critic identifies completeness gaps and may trigger further work. | A places the critic late; B permits re-elicitation. Preserve the PT topology. |
| PT mechanism graph | `pt.17-.18` | `.09` | `shared_shell_method_refinement` | A typed temporal mechanism graph is constructed and audited. | A separates producer and independent audit/repair; B names one operation. Share graph custody, not causal judgment. |
| PT synthesis and refusal | `pt.19`, `.22-.23` | `.10-.11` | `shared_shell_method_refinement` | A narrative result is calibrated and may refuse confident ranking. | A includes terminal audit/publication; B separates an explicit refusal operation. Preserve refusal as a first-class outcome. |
| PT refinement | `pt.21` | no direct row | `method_local` | — | A implements conditional re-reading and rerun lineage. B does not model it. |
| Acquisition agenda | `pt_acq.01` | `pt_source_acquisition.01` | `shared_shell_method_refinement` | A frozen baseline yields ranked evidence needs. | A binds a whole session/baseline; B emphasizes gap identification. Reuse agenda custody only. |
| Acquisition discovery/retrieval | `pt_acq.02` | `.02`, `.04` | `signature_mismatch` | Candidate sources are found and fetched. | A combines target retrieval through an external provider; B separates search from full-text retrieval. Preserve provider/result cardinality and failure states. |
| Acquisition review/admission | `pt_acq.03` | `.03`, `.05` | `shared_shell_method_refinement` | A reviewer records provenance/duplication judgments and hash-binds admitted text. | The analytic judgment is human in the scoped path. Share the review/custody shell, not a generic relevance score. |
| Acquisition reconciliation | no scoped counterpart | `.06` | `method_local` | — | B exposes an unimplemented same-case conflict-reconciliation need. The bulk comparative implementation is a different variant. |
| Held-out evaluation return | `pt_acq.04` | acquisition `.05` → core `.01` edge | `evidence_mismatch` | Newly admitted evidence should test frozen rivals. | A records the end-to-end step as incomplete; B calls the underlying evaluate path executable. Treat readiness as unresolved until the exact return contract is replayed. |
| Theory paper extraction | `tf.01-.03` | `theory_forge_compile_apply.01-.03` | `shared_operation` | Paper text is rendered, a theory selected, and a structured theory representation extracted. | B uses later schema language; pin schema version at the producer boundary. |
| Theory artifact validation | `tf.04-.05` | `.03` | `shared_shell_method_refinement` | Extracted theory artifacts are persisted and structurally validated. | A separates persistence/validation; B includes them in formalization. Share storage/validation mechanics only. |
| Theory compilation | `tf.06-.12` | `.04-.06` | `shared_shell_method_refinement` | A structured theory is projected into code, tested, repaired, and reviewed. | A exposes cache, prompt, computation, healing, and review stages; B compresses them. Compilation semantics stay Theory Forge-owned. |
| Compiled-theory execution | `tf.13-.19` | `.07` | `evidence_mismatch` | Parameters are extracted, transformations run, invariants checked, and interpretation produced. | A marks only invariant checking incomplete; B marks the combined run incomplete. Reconcile against one authentic compiled run before capability adoption. |
| Runtime-green manifest | no exact operation | `.08` | `evidence_mismatch` | A status artifact is expected to summarize runnable theories. | B found the manifest claim unsupported for most theories; A records report assembly, not fleet-wide runtime verification. Do not promote the manifest claim. |
| CPT model calculation | `tf_cpt.03-.04` | `theory_forge_cpt_choices13k.01-.04` | `signature_mismatch` | CPT transforms lead to a row-level predicted choice. | A treats the model calculation as a compact implementation call; B exposes value, weighting, cumulative weights, and prospect value. Preserve the theory-specific mathematical stages. |
| CPT baseline | part of `tf_cpt.04` | `.05` | `shared_operation` | Expected-value prediction is computed for the same eligible choice. | B exposes it separately; identity and eligible-row alignment must be retained. |
| CPT data acquisition | `tf_cpt.01` | `.06` | `shared_operation` | Dataset bytes are acquired and cryptographically pinned. | Suitable shared custody operation, with dataset-specific producer policy. |
| CPT eligibility | `tf_cpt.02` | `.07` | `shared_operation` | Declared row classes are screened before scoring. | The eligibility rule remains fixture/theory-owned. |
| CPT comparison/report | `tf_cpt.04-.06` | `.08` | `shared_shell_method_refinement` | CPT and EV predictions are compared with observed majority choices and reported. | A separates row computation, aggregation, and evidence report; B treats scoring as one operation. Share observation alignment/report envelope only. |
| Policy options | `mt.02` | `mist_trail_policy_appraisal.01` | `shared_operation` | Official alternatives are identified without inventing or merging options. | Both are reviewed manual operations. |
| Policy criteria/interests | `mt.02`, `.05` | `.02`, `.04` | `signature_mismatch` | Criteria, affected interests, and explicit judgments shape appraisal. | A separates framing from later value recording; B splits criterion identification from rendering judgment. Preserve the evidence/value boundary. |
| Policy consequence claims | `mt.03-.04` | `.03` | `shared_operation` | Source-bound consequences are reviewed per option × criterion. | A separates window anchoring and appraisal; both remain manual in this fixture. |
| Policy priority lenses | `mt.05-.06` | `.05` | `shared_operation` | Explicit alternative priorities can reverse or suspend a preference. | A calls the transformation perturbation; B calls it ranking. Do not infer numeric weights. |
| Policy recommendation/refusal | `mt.07` | `.06` | `shared_operation` | The result is conditional on priorities and may remain unresolved. | Same bounded manual outcome. |
| Policy packet/custody/UI | `mt.08-.10` | `.07-.09` | `shared_shell_method_refinement` | Typed packet integrity, source identity, API, and browser projection are preserved. | B splits validation, anchoring, and rendering; A distinguishes manual assembly from executable validation/projection. Reuse technical shell only. |

## Counts and consequences

Counts are by the 40 meaning-level rows above, not by either candidate's raw
step count:

| Class | Count | Architectural consequence |
| --- | ---: | --- |
| `shared_operation` | 12 | Reuse remains a hypothesis; require a concrete seam and preserve method ownership. |
| `shared_shell_method_refinement` | 13 | Strongest shared-layer candidates are custody, validation, review, lineage, refusal, and projection shells. |
| `method_local` | 5 | Keep within the owning method or expose a typed boundary only when consumed. |
| `signature_mismatch` | 6 | Do not merge without an explicit adapter and loss account. |
| `name_collision` | 1 | Namespace the two diagnostic operations. |
| `evidence_mismatch` | 3 | Re-run the exact behavior before using it for architecture or readiness claims. |

No percentage or global reuse score should be derived from these counts.

## Immediate reconciliation decisions

Adopt as planning guidance, not as a schema:

- The smallest credible neutral layer is typed identity and custody plus
  method-declared inputs, outputs, review state, lineage, refusal, and loss.
- Analytical judgments remain in method profiles/engines.
- Workflow topology is part of method meaning; it cannot be reconstructed from
  a flat capability list.
- Execution evidence must remain separate from representation quality.

Do not adopt yet:

- a universal verb vocabulary;
- one cross-method evidence-strength or confidence scale;
- a generic `review`, `test`, `estimate`, or `diagnostic` capability inferred
  from labels;
- the independent candidate's proposed type/verb additions as canonical;
- either candidate's raw step granularity as the catalog normal form.

## Next gate

The comparison is sufficient to resume method-capability catalog work only as
a discovery exercise. Before a shared capability becomes infrastructure, test
it through two authentic compatible seams. The three evidence mismatches
(held-out acquisition return, compiled-theory execution, and runtime-green
manifest) should be resolved only if a near-term architectural decision depends
on them.
