# Decision Brief: First Quantitative-Text Strand

Date: 2026-07-12
Status: decision required; documentation only
Decision owner: Brian
Recommended disposition: approve a conditional task/owner pattern, not a
construct, model, or implementation

## Outcome

The first quantitative-text strand should estimate the prevalence or ordered
distribution of **one observable qualitative category supported by the selected
governed case**. Qualitative work must first define the construct, inclusion and
exclusion rules, boundary cases, and anchored examples. A quantitative
instrument may then measure the category over a frozen corpus and return
item-linked errors and uncertainty for an explicit joint display.

Use a transparent dictionary/count as the mandatory simple baseline. Use a
regularized supervised instrument only if the governed corpus has enough
independent labeled source/document groups for a leakage-safe held-out test.
Treat topic/embedding output as discovery or a stress test, not as the first
measure. A codebook-prompted LLM is a challenger subject to behavioral and
compliance tests, not ground truth.

The first adapter should be narrow, case-specific, and owned by
`mixed_methods_workbench`, wrapping established libraries. QC owns strict
category/codebook/anchor/human-label exports. PT owns within-case rival
inference. A generic shared quantitative-text engine is deferred until at least
a second real slice demonstrates a stable repeated seam.

## Decision in one table

| Candidate | Valid first use | Main evidence obligation | Disposition |
|---|---|---|---|
| Dictionary/count prevalence | Lexically explicit category in a stable language/edition | Frozen rules, grouped held-out context review, polysemy/negation/quotation/OCR/translation errors, prevalence error | Mandatory baseline; conditional primary |
| Supervised binary/multiclass prevalence | Contextual observable category with enough independent adjudicated groups | Grouped sealed split, dummy/dictionary/TF-IDF-linear comparisons, per-class and prevalence error, calibration, slices, item review | **Recommended default task form when feasible** |
| Supervised ordinal distribution | Substantively ordered levels with reproducible adjacent boundaries | Predeclared order/thresholds, assumption tests, per-level errors/calibration | Conditional subtype only |
| Topic/embedding discovery | Unknown recurring subjects or semantic neighborhoods | Multi-run stability, human interpretation, outliers, external and downstream-result validation | Discovery/negative comparator only; not first measure |

No model family is universally best. Automated text analysis requires
application-specific validation and close reading; topic interpretability alone
does not establish a measure. [Grimmer and Stewart](https://doi.org/10.1093/pan/mps028),
[Ying, Montgomery, and Stewart](https://doi.org/10.1017/pan.2021.33),
[Zhang, Zhou, and Li](https://doi.org/10.1177/00811750241265336).

## Case-conditioned task contract

The recommended pattern is an exploratory-sequential **build** operation:

```text
governed corpus
-> QC category + anchored positive/negative/boundary cases
-> reviewed construct/use card and feasibility readout
-> frozen annotation + split manifests
-> dictionary and regularized supervised comparison
-> item-linked prevalence/distribution with uncertainty
-> joint display + convergence/divergence disposition
-> bounded meta-inference
```

The exact construct cannot be chosen before GOV/R01. If FRUS is selected, a
later feasibility study may test categories such as option framing or
escalation/risk language, but this brief does not approve those constructs. If
the category is not observable, labelable, or independently distributed across
enough source groups, choose a different category or case; do not substitute a
topic model, sentiment proxy, or segment-level pseudo-sample.

Intended use is a bounded category distribution within the frozen corpus or a
declared sampling frame. Prohibited uses include author motive, ideology,
causal effects, PT support, population generalization, and transfer to another
language, edition, domain, genre, period, or case without a new validation
study. Aggregate prevalence needs its own validation; high item accuracy can
still yield biased proportions. [Hopkins and King](https://doi.org/10.1111/j.1540-5907.2009.00428.x).

## Owner decision

| Boundary | Finding | Disposition |
|---|---|---|
| Workbench-owned narrow adapter | Owns the study measurement specification, compatible consumer, split/config manifests, predictions, uncertainty, evaluation, item links, and integration artifact; can replace libraries behind a stable research contract | **Recommended first owner** |
| Existing producer-owned adapter | QC would mix qualitative category creation with quantitative measurement; PT would mix population measurement with within-case causal comparison | Reject by default; producers supply strict inputs, not QT inference |
| New shared engine | No repeated real seam exists; a generic abstraction would encode unobserved units, constructs, and validity rules | Defer until at least a second materially similar slice |

The future operation must be importable and agent-invocable. Any CLI, API, UI,
or notebook must call the same typed core. This ownership recommendation is not
an authorization to create that core.

## Feasibility stop point before implementation

After GOV and R01 but before a QT implementation plan, run a documentation and
human-label feasibility readout that records:

- construct definition, unit, population/frame, intended/prohibited inference,
  and asymmetric error costs;
- lexical versus contextual character and edition/translation sensitivity;
- independent source/document/author/time groups and duplicate/near-duplicate
  structure;
- pilot prevalence/support, disagreement locations, difficult-case taxonomy,
  annotation/reviewer burden, and learning curve;
- allowed processing boundary and eligible incumbent models/libraries.

Brian must then approve the exact construct and separately authorize a named QT
slice. Metric margins, split sizes, power/noise rationale, and thresholds are
configured and preregistered from that readout, not hardcoded now.

## Acceptance evidence

| Gate | Evidence required | Claim licensed |
|---|---|---|
| GOV/use | Frozen denominator, source groups, language/edition, rights, anchors, processing/publication scope | Named corpus is eligible for the task |
| Construct/use | Literature/case-grounded definition, unit/frame, intended/prohibited uses, error costs, boundary/negative cases, accountable reviewer | Measurement may be attempted |
| Annotation | Versioned codebook, independently coded pilot and sealed set, retained disagreements/adjudication, prevalence/support and difficult cases | Human reference is reviewable, not automatically true |
| Split/contamination | Immutable train/development/sealed IDs; grouped documents/authors/editions/translations; duplicate audit; training-only preprocessing | Held-out evidence is not visibly contaminated |
| Baselines | Human-only, dummy, dictionary, TF-IDF regularized linear, and strongest eligible contextual incumbent; exact versions/config/licenses | Comparison is not comparator shopping |
| Measurement | Per-class metrics, prevalence error, calibration/proper scores when applicable, grouped uncertainty, source/language/time/error-cost slices, learning curve, item-level false-positive/negative review | Bounded observed performance for the named task |
| Integration | Every result resolves to governed source/anchor and category version; joint-display unit, denominator, construct, uncertainty, divergence, and meta-inference align | One reviewable qual–quant operation |
| Independent decision | Fresh reviewer inspects raw items, splits, codebook, errors, traces, and can reject promotion | Bounded QT decision only; no SOTA claim |

Accuracy alone is prohibited. If the corpus is a complete finite universe, the
observed corpus count has no sampling error for that universe but still has
measurement error. Do not manufacture segment-level confidence intervals from
dependent units.

## Required negative controls

- permuted labels and dummy/majority output collapse to the expected null;
- segments, duplicates, translations, editions, or source-lineage siblings
  crossing splits fail the split manifest;
- vocabulary, dictionary expansion, embeddings, calibration, or prompt tuning
  seeing sealed data fails the trace gate;
- dictionary polysemy, negation, quotation, attribution, historical spelling,
  OCR, and target reversal reach their expected error readouts;
- an off-construct proxy such as sentiment cannot license stance or another
  target even if its own metric is high;
- rare/negative-case erasure fails per-class recall and prevalence error;
- source/author/genre/edition shortcuts fail grouped and source-ablated tests;
- generic/swapped codebook labels, exclusion-rule triggers, codebook ablations,
  and invented/disallowed labels expose LLM shortcut or compliance failures;
- ordinal label shuffling or adjacent-level collapse removes any false ordinal
  advantage;
- topic solutions vary across seeds, preprocessing, topic counts, embeddings,
  outlier treatment, and model families, and cannot become the measure when
  semantically similar solutions change downstream conclusions;
- mismatched joint-display units or denominators, and missing source anchors,
  block aggregation and meta-inference.

The codebook-LLM challenger must pass codebook preparation, label-free
behavioral checks, labeled evaluation, systematic error analysis, and only then
any supervised tuning; fluent labels do not waive the gate.
[Halterman and Keith](https://doi.org/10.1017/pan.2025.10017).

## Failure modes and what to try next

| Failure | Required response |
|---|---|
| No useful observable category | Return to qualitative work or select another case; do not substitute sentiment/topics. |
| Too few independent groups | Use human-coded descriptive prevalence as an unpromoted pilot, broaden the governed corpus, or change case. |
| Boundary disagreement is concentrated | Refine/retain uncertainty/collapse with substantive justification, or abandon the construct. |
| Dictionary coverage is high but context precision is poor | Refine on development data; then use supervised measurement or change construct if sealed errors persist. |
| Supervised gain exists only on random segment splits | Treat as leakage; rerun grouped or retain the simpler honest measure. |
| Accuracy is high but prevalence/minority performance is poor | Evaluate the intended aggregate and error cost; change development thresholds/calibration or add labels. |
| Strongest model is ineligible under source governance | Use an eligible local model and record the comparison gap; never upload restricted text. |
| Topic labels are coherent but downstream results unstable | Keep as a sampling/discovery aid and validate any category from scratch. |
| No automation beats preregistered human/simple baselines | Publish the null and keep human coding for this case. |
| Second slice needs a different contract | Keep project-specific adapters; no shared engine boundary exists. |

## Exact decision requested

Brian may approve this planning sentence:

> After a governed case and R01 qualitative category exist, target the
> prevalence or ordered distribution of one observable QC-derived category.
> Use a narrow `mixed_methods_workbench`-owned adapter; require human, dummy,
> dictionary, and regularized supervised comparisons; choose the primary
> instrument only after a grouped leakage-safe feasibility readout; and prohibit
> topic/embedding output from serving as the first measure. The exact construct
> and implementation still require separate approval and named authorization.

If rejected, the replacement decision must name a quantitative inference and
its failure cost, not merely a preferred model.

## Synthesis provenance

The parent read every identified research/session artifact before writing this
brief. No identified research artifact was skipped:

- `.claude/tasks/session_context.md`
- `.claude/tasks/sota_program_progress.md`
- `.claude/tasks/research_artifact_authority.md`
- `.claude/tasks/research_producer_readiness.md`
- `.claude/tasks/research_sota_landscape.md`
- `.claude/tasks/decision_research_context.md`
- `.claude/tasks/research_gov_case_options.md`
- `.claude/tasks/research_qt_first_task_options.md`
- `~/projects/investigations/mixed_methods_workbench/2026-07-12-sota-program-baseline.md`
- `~/projects/investigations/cross-project/2026-06-26-mixed-methods-repo-assessment.md`
- `~/projects/investigations/cross-project/2026-06-26-theory-forge-ac-coupling.md`

Canonical sources reconciled were `docs/PLANNING_STATUS.md`, `docs/ROADMAP.md`,
`docs/MIXED_METHODS_CAPABILITY_MAP.md`, `docs/CAPABILITY_DEPENDENCY_GRAPH.md`,
`docs/SOTA_EVIDENCE_SCORECARD.md`, `docs/CONCERNS.md`, the long-term goal, and
handoff files. The complete primary/official bibliography, skipped sources,
null results, and freshness triggers are in
`.claude/tasks/research_qt_first_task_options.md`.
