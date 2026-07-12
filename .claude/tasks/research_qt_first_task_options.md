# Lane B Research: First Quantitative-Text Task and Owner Options

Date: 2026-07-12
Access date for every external source: 2026-07-12
Status: documentation-only research; no task, construct, owner, or implementation is authorized

> **Sources:** frozen lane context; current workbench roadmap, capability map,
> dependency graph, concern register, goal, project thesis, and repository
> instructions; Fetters, Curry, and Creswell (2013); Grimmer and Stewart (2013);
> Hopkins and King (2010); Birkenmaier, Lechner, and Wagner (2024); Bestvater
> and Monroe (2023); Ying, Montgomery, and Stewart (2022); Zhang, Zhou, and Li
> (2025); Halterman and Keith (2026); the `stm` package paper; and current
> official documentation for quanteda, scikit-learn, statsmodels, and BERTopic.
> Complete URLs and source limits appear in
> [Sources consulted](#sources-consulted).

## 1. Executive Finding

### Recommended task family, conditional on the governed case

The strongest default is **not a named construct or model**. It is this bounded
task family:

> Estimate the prevalence or ordered distribution of one observable,
> case-supported qualitative category across a frozen governed corpus, using
> adjudicated item labels as the reference, a transparent dictionary/count as
> the mandatory simple baseline, and a supervised instrument only if the corpus
> contains enough independent labeled units for a leakage-safe held-out test.

This is a faithful exploratory-sequential **build** operation: qualitative work
defines the construct, inclusion/exclusion rules, difficult boundary cases, and
anchored examples; the quantitative strand turns that reviewed specification
into a measurement instrument, estimates its error and distribution, and
returns item-linked results for a joint display. Fetters, Curry, and Creswell
define building as one strand informing the data collection or analysis of the
next strand, while warning that sequential phases must actually integrate
rather than merely follow one another.

The governed case decides which instrument is viable:

- If the selected category is lexically explicit, stable across the approved
  language/edition, and recoverable with reviewed phrases and context rules, a
  dictionary/count can be the primary instrument.
- If the category is contextual, target-dependent, relational, or ordinal and
  there are enough independent labeled source/document groups, use a
  regularized supervised classifier or ordinal model, with the dictionary as
  the simple baseline.
- If the corpus is too small, too homogeneous, too dependent, or too
  translation-sensitive to support a sealed group-held-out evaluation, do not
  manufacture an automated quantitative strand. Use human-coded descriptive
  prevalence as a pilot or choose a better governed case; neither option by
  itself promotes `QT`.
- Topic or embedding models may be used for discovery, robustness probing, or
  as a negative comparator. They should not supply the first construct measure:
  topic labels and coherence do not establish construct validity, and
  semantically similar topic solutions can support conflicting downstream
  inferences.

### Recommended owner boundary

The first adapter should be a **narrow, project-specific adapter owned by
`mixed_methods_workbench`**, wrapping established libraries selected after the
case and construct are fixed. Qualitative Coding should own the strict export
of codebook/category definitions, anchors, human labels, and review state;
the workbench should own the measurement protocol, split manifest, library
configuration, predictions/uncertainty, item linkage, integration, and review
packet. Process Tracing should not own a population/prevalence text measure.

Do not create a generic shared quantitative-text engine now. Extract shared
infrastructure only after at least a second real slice demonstrates a repeated,
method-independent contract. This follows the repository's current ownership
policy and avoids making an unobserved abstraction the dependency for the first
mixed-methods case.

### Confidence

- **High** that construct/use must precede method choice; that a held-out,
  item-linked, error-analyzed measure is required; that an unsupervised topic
  model cannot be the default measure; and that a narrow workbench adapter is
  the least boundary-violating first owner.
- **Medium** that supervised prevalence measurement will be the best primary
  instrument, because the selected case, construct, label prevalence,
  independent-group count, language/edition, and error costs are not yet known.
- **Low** confidence in any specific library, model family, split proportion,
  sample-size threshold, or construct until GOV freezes the corpus and a pilot
  measures feasibility.

## 2. Search and Provenance Method

### Questions

1. Which first quantitative-text task fits an exploratory-sequential build from
   qualitative categories without treating counts as self-validating?
2. What evidence distinguishes a dictionary, supervised measure, and
   unsupervised topic/embedding discovery surface?
3. What train/test, leakage, uncertainty, and item-linkage obligations apply to
   a single governed text case?
4. Which repository should own the first adapter without flattening QC, PT, or
   workbench responsibilities?

### Collection

- Read the frozen lane context completely before collection.
- Read the current local roadmap/capability/ownership statements that govern QT.
- Preferred primary methods papers and peer-reviewed validation research over
  tutorials or vendor claims.
- Used official current library documentation only to establish available
  operations, not methodological validity.
- Searched dictionary/prevalence, supervised/ordinal, topic/embedding,
  mixed-method integration, validation, leakage, calibration, and grouped split
  surfaces.

### Stopping rule

Collection stopped after obtaining:

- a primary mixed-methods basis for exploratory-sequential building;
- cross-method validation principles and a contemporary validation review;
- one primary aggregate-prevalence method warning;
- one observed construct-mismatch example comparing dictionaries and supervised
  models;
- two primary topic-model measurement/stability critiques;
- one current primary framework testing whether LLMs follow real social-science
  codebooks rather than merely emit plausible labels;
- official operations for transparent dictionary lookup/context inspection,
  supervised grouped evaluation/calibration, ordinal modeling, and two current
  topic-model families; and
- enough local authority to resolve the owner boundary.

Additional searches repeated the same result: no method is universally best,
and no case-free benchmark can choose the first construct or instrument.

## 3. Candidate Comparison Matrix

All candidates assume a frozen `ResearchBundle` with stable item, source,
document, segment, actor/time (when applicable), language/edition, and anchor
identities. “Population” means the explicitly governed corpus or a declared
sampling frame—not an undefined population of texts.

| Candidate | Case-dependent construct and unit | Qual-to-quant build | Validation and leakage design | Baselines/incumbents | Metrics and uncertainty | Burden/failure cost | Disposition |
|---|---|---|---|---|---|---|---|
| **A. Dictionary/count prevalence** | One observable category whose reviewed definition is substantially lexical; segment or document is the coding unit, but source/document is the minimum independence group. Population is the frozen corpus or declared frame. | QC codebook + anchored positive/negative/boundary examples -> versioned phrase/term rules -> context review -> item scores -> prevalence by a predeclared grouping -> joint display with qualitative explanations and exceptions. | Freeze the dictionary before sealed evaluation. Develop only on training/development sources. Hold out whole source/document/edition groups. Review every false positive/negative type, polysemy, negation, quotation/attribution, historical spelling, OCR, and translation effects. | Human-coded prevalence; literal count/empty or irrelevant dictionary; a validated domain lexicon only if construct, language, genre, and license actually match; supervised task-specific measure as stronger contextual comparator. | Per-class precision/recall/F1 and confusion matrix; prevalence absolute error/bias against adjudicated labels; coverage/unmatched rate; source/genre/time/language slices. If census: measurement-error interval/sensitivity, not fictitious sampling error. If sampled: design-appropriate or group bootstrap interval. | Lowest implementation burden and highest inspectability. High false-positive/negative cost when words are context-dependent; a plausible count can silently become a wrong construct. | **Conditional primary or mandatory simple baseline.** Primary only for lexically explicit constructs that pass held-out context/error tests. |
| **B. Supervised binary/multiclass prevalence measure** | One explicitly observable, case-supported category; item unit can be segment/document, but labels and splits retain source/document groups. Intended quantity is item classification plus aggregate prevalence, not author intention or causal effect. | QC category specification + independently coded/adjudicated training items -> frozen feature/model pipeline -> sealed predictions/probabilities -> error-corrected or sensitivity-bounded prevalence -> item-linked joint display and qualitative error review. | Split before preprocessing; group by source/document/author/edition and use time-aware grouping where relevant. Keep duplicate/near-duplicate and translated versions in one split. Tune on training/development only; sealed test remains untouched. Preserve label disagreements and difficult cases. Any codebook-prompted LLM must also pass definition recall, instruction/compliance, exclusion, generic/swapped-label, ablation, and manual-output tests before its accuracy is decision-relevant. | Human-only coding; majority/stratified dummy; dictionary/count baseline; TF-IDF regularized logistic regression or linear SVM as transparent strong baseline; task-specific contextual transformer/embedding/LLM classifier only as the strongest relevant incumbent after construct/domain and behavioral review. | Class prevalence/support; per-class precision, recall, F1, balanced accuracy, confusion; probability calibration/reliability and proper scores; aggregate prevalence error; group/source/language/time/error-cost slices; clustered bootstrap or design-based uncertainty; learning curve and repeated split variability. Accuracy alone is prohibited. | Higher annotation/adjudication and evaluation burden. False negatives can erase rare/negative cases; false positives can fabricate prevalence. Context models may hide source/edition artifacts and appear strong through leakage. Codebook-prompted LLMs can ignore exclusions, use lexical/label shortcuts, hallucinate labels, and vary sharply by class despite plausible aggregate output. | **Recommended default task form when feasible.** Instrument choice remains conditional on independent groups, label quality, prevalence, and error costs. Advanced models cannot displace the dictionary and TF-IDF/linear baselines. |
| **C. Supervised ordinal measurement** | A category with a defensible order whose levels have stable substantive meaning; levels are ordered but not assumed equally spaced. | QC defines ordered levels, thresholds, counterexamples, and adjacent-boundary cases -> adjudicated labels -> ordinal model or constrained classifier -> level probabilities/distribution -> joint display that preserves threshold uncertainty and qualitative cases. | Same grouped/sealed design as B. Pre-register ordering and thresholds before test inspection. Test proportional-odds or alternative assumptions when using an ordered regression; never convert labels to an interval scale by convenience. | Human ordered coding; median/majority dummy; collapsed binary/multiclass model; ordered logit/probit or task-specific ordinal classifier; nominal classifier as an assumption check. | Per-level precision/recall; weighted kappa as a descriptive agreement statistic, not a validity verdict; absolute/adjacent-level error; threshold confusion; per-level calibration; prevalence/distribution error and uncertainty. | Highest codebook burden because adjacent levels must be distinguishable. Severe levels may be rare; disagreement may reveal a non-ordinal construct. | **Conditional subtype, not the default.** Use only if qualitative analysis establishes a real order and a pilot shows reproducible adjacent distinctions. |
| **D. Unsupervised topic/embedding discovery** | Unknown recurring subject matter or semantic neighborhoods, not a predeclared social construct. Unit and corpus size must fit the selected model; small/dependent historical packets are especially risky. | Corpus -> multiple seeded/preprocessing/model solutions -> representative words/items -> independent human interpretation -> candidate categories returned to qualitative analysis. Any later measure requires a separate supervised/dictionary validation cycle. | Run multiple seeds, preprocessing choices, topic counts/cluster settings, embeddings, and model families; hold out or temporally test assignment where supported; compare stability, topic/word intrusion, representative-document judgments, external-event hypotheses, and downstream-result stability. Preserve outliers rather than forcing them into attractive topics. | Human qualitative discovery/codebook; simple term/document-frequency and co-occurrence summaries; LDA/STM; embedding clustering such as BERTopic. The relevant incumbent is corpus- and discovery-goal-specific. | Stability/alignment across runs; held-out assignment where meaningful; coherence only as one diagnostic; topic/word intrusion; coverage/outlier rate; expert interpretability; external/convergent tests; downstream coefficient/sign sensitivity across semantically similar solutions. | High analyst degrees of freedom and interpretation burden. Topic labels can look persuasive while assignments or downstream estimates are unstable. Embedding/model versions add drift and opaque training-corpus effects. | **Negative/conditional comparator only for the first QT measure.** Useful for discovery or stress testing, not construct prevalence or meta-inference by itself. |

### Intended and prohibited use common to A-C

**Intended:** describe a bounded category distribution within a frozen corpus or
declared sampling frame; compare predeclared source/time/actor strata only when
the design supports them; return uncertain item-level results for review and
integration with qualitative findings.

**Prohibited:** infer author motives, stance, ideology, population prevalence,
causal effects, PT hypothesis support, or generalize to another language,
edition, domain, genre, period, or case without a new validity study. Bestvater
and Monroe show why an apparently adjacent construct is unsafe: sentiment
measures—including sophisticated models—can be poor proxies for target-specific
stance and can distort downstream estimates.

## 4. Owner Boundary Comparison

| Boundary | What it would own | Advantages | Risks / disqualifiers | Decision |
|---|---|---|---|---|
| **Narrow workbench adapter around established libraries** | Study-specific measurement spec, input consumer, split manifest, exact library/config, predictions/probabilities, uncertainty, item links, evaluation, and integration artifact. QC remains source of strict codebook/label exports. | Aligns ownership with integration and compatibility policy; avoids changing producers; supports one thin slice; makes replacement of the library possible without changing the research contract. | Must not grow into a generic text engine, invent its own qualitative labels, or hide an R/Python/subprocess boundary. Exact versions, seeds, resources, and failures must be visible. | **Recommended first owner.** |
| **Existing producer owns adapter** | QC or another producer would perform quantitative measurement in addition to its method export. | Could colocate codebook/annotations and reduce data movement. | QC's current boundary is qualitative coding/claims, not population text measurement; PT is within-case rival inference. Ownership would blur estimands, introduce producer coupling, and make integration policy leak upstream. Only producer-owned descriptive counts that are intrinsic to a strict export are plausible; they do not settle QT ownership. | **Reject as default.** Producer supplies strict inputs/evidence, not the workbench quantitative strand. Reconsider only with a named producer decision and method rationale. |
| **New shared quantitative-text engine** | Generic corpus, dictionary, classifier, topic, evaluation, and artifact APIs for multiple projects. | Potential reuse after repeated needs; could centralize evaluation and versioning. | No second slice or stable seam exists; a universal abstraction would be hypothetical, broad, and likely to encode the wrong unit/construct/validity rules. It creates a new owner before the task is known. | **Defer.** Extract only after at least a second real slice demonstrates repeated contracts and independent ownership value. |

The recommended adapter should expose a typed, method-specific artifact rather
than raw library objects. At minimum it needs: construct/use version, corpus and
unit IDs, grouping/split manifest, library/model/config identity, label and
prediction records, uncertainty, validation results, caveats/prohibited uses,
and exact item/source anchors. The core operation must be importable and
agent-invocable; any CLI/API/UI should call the same implementation.

## 5. Facts, Inferences, and Recommendations

### Observed facts

1. **Mixed-method integration:** exploratory sequential work is integrated when
   the qualitative phase builds the quantitative instrument or data collection,
   not merely when two outputs are shown side by side. **Confidence: high.**
2. **Application-specific validity:** automated text methods are imperfect
   language models, no method is universally best, and both supervised and
   unsupervised applications require substantive validation. **High.**
3. **Construct-first design:** the contemporary validation review recommends an
   explicit literature-grounded construct definition and tracing its
   consequences for data, method, and preprocessing choices. **High.**
4. **Aggregate quantity differs from item accuracy:** Hopkins and King show that
   high individual classification accuracy can still yield biased category
   proportions; the intended prevalence quantity needs its own validation.
   **High.**
5. **Construct mismatch can dominate model sophistication:** Bestvater and
   Monroe found sentiment-to-stance transfer degraded task performance and
   downstream estimates; a model accurate for the wrong label is still an
   invalid instrument. **High for the demonstrated domains; medium for transfer
   to the future governed case.**
6. **Topic quality is not measurement validity:** Zhang, Zhou, and Li show that
   semantically similar topic solutions can support conflicting downstream
   results. Ying, Montgomery, and Stewart provide human topic-validation
   procedures, which are useful but do not eliminate the downstream-measurement
   problem. **High.**
7. **Current library capabilities:** quanteda supports dictionaries, fixed/glob/
   regex matching, multiword patterns, counts, and keyword-in-context inspection;
   scikit-learn supports grouped/stratified-group splits, pipelines, per-class
   metrics, and calibration; statsmodels supplies an experimental ordered
   logit/probit model; STM supplies metadata-aware topic estimation and
   uncertainty; BERTopic exposes modular embeddings/clustering, representative
   documents, topic mappings, probabilities/approximations, and outlier
   handling. These are operations, not evidence that a use is valid. **High.**
8. **Local owner null:** current project authority records no QT task or owner
   and explicitly recommends a narrow adapter around established libraries for
   the first slice, with shared extraction only after repeated evidence.
   **High; refresh if the project graph or an ADR changes.**
9. **Codebook compliance is empirically testable and cannot be assumed from an
   LLM's fluency:** Halterman and Keith's five-stage framework requires
   human/machine-readable codebook preparation, label-free behavioral tests,
   labeled zero-shot evaluation, systematic error analysis, and only then
   supervised instruction tuning. Across three real political-science
   codebooks, zero-shot performance and per-class F1 varied substantially; one
   sampled Manifesto condition had extensive output non-compliance, and manual
   analysis exposed exclusion-rule and lexical-label shortcuts. Supervised
   tuning improved some tasks but did not create a universal best model.
   **High for the studied English political corpora; medium for transfer to the
   future case.**

### Inferences

1. A prevalence/distribution task is the smallest quantitative output that can
   connect directly to a case-derived qualitative category and produce an
   inspectable joint display. **High.**
2. Supervised measurement is the best *default task form*, but not always the
   best instrument. A transparent dictionary can be superior for a truly
   lexical construct or a small corpus because its failure surface is easier to
   enumerate; contextual supervised models are preferable only when label and
   split evidence support them. **Medium-high.**
3. Segment count is not sample size. Segments from the same source, author,
   edition, or translated document are dependent and must stay in one split;
   otherwise a large-looking corpus can produce leakage and pseudo-replication.
   **High.**
4. If the governed case is a complete finite corpus, the observed corpus count
   has no sampling error with respect to that corpus, but it still has
   measurement error. Reporting a naive segment-level confidence interval would
   misstate uncertainty. **High.**
5. Assigning the first adapter to QC would make qualitative code construction
   and quantitative measurement one producer concern, weakening the explicit
   method boundary. **High given current repository contracts.**

### Recommendation

Approve only the **conditional task/owner pattern**, not a construct or model:

1. GOV freezes the case, corpus denominator, language/edition, source groups,
   and allowed processing.
2. QC/R01 produces one reviewed category specification with anchored positive,
   negative, difficult, and absent cases.
3. A documentation-only feasibility readout determines lexicality,
   labelability, prevalence, group count, reviewer burden, and error costs.
4. Brian then confirms the exact construct and authorizes a narrow QT slice.
5. The workbench-owned adapter compares human-only, dummy, dictionary, and
   regularized supervised baselines on a sealed group-held-out set. A contextual
   model is included only if it is the strongest relevant current incumbent and
   the governed processing boundary permits it. A codebook-prompted LLM must
   additionally pass codebook-specific behavioral and compliance tests; fluent
   output or aggregate F1 cannot waive this gate.
6. The released measure is the simplest candidate that meets the preregistered
   construct/error/uncertainty criteria; unsupervised results cannot substitute
   for a failed measure.

## 6. Required Acceptance Evidence and Negative Controls

No fixed metric threshold or sample size is defensible before the construct,
prevalence, independent-group structure, decision costs, and baseline noise are
observed. The implementation plan must preregister margins and power/learning-
curve rationale after that readout and before sealed results.

### Acceptance evidence before implementation/promotion

| Gate | Required evidence | Claim licensed if it passes |
|---|---|---|
| GOV and use | Frozen corpus/source manifest; denominator and exclusions; language/edition/translation; rights/access; stable anchors; permitted processing/publication. | The selected corpus can be used for the named research task. |
| Construct/use card | Literature/case-grounded definition; unit; population/frame; intended and prohibited inferences; error costs; known boundary/negative cases; responsible reviewer. | The category is specified well enough to attempt measurement. |
| Annotation instrument | Versioned codebook; independently coded pilot and sealed set; disagreements and adjudication retained; per-class prevalence/support; difficult-case taxonomy. Agreement is descriptive, not the sole validity gate. | Human reference labels are reviewable for this task. |
| Split/contamination manifest | Immutable train/development/sealed IDs; source/document/author/edition/translation groups; duplicate/near-duplicate audit; preprocessing fit on training only; no prompt/dictionary/model tuning on sealed items. | Held-out results are not visibly contaminated by known dependencies. |
| Baseline registry | Human-only workflow, dummy, transparent dictionary/count, regularized TF-IDF linear model, and strongest task-relevant contextual incumbent with exact version/config/license. If that incumbent is an LLM, record the complete codebook/prompt/output contract and behavioral-test results. | Model comparisons are not comparator shopping. |
| Measurement result | Per-class and aggregate metrics; calibration when probabilities are used; prevalence error; uncertainty; group/language/genre/time slices; learning curve; qualitative false-positive/negative review; all item outputs retained. | The instrument has bounded observed performance on the named case/split. |
| Integration artifact | Every quantitative item resolves to a governed source/anchor and qualitative category version; joint display aligns unit, denominator, construct, evidence, uncertainty, divergence, and meta-inference. | One explicit qualitative-quantitative build/merge operation can be reviewed. |
| Independent decision | Fresh reviewer inspects raw items, splits, codebook, errors, and traces and can reject the promotion. | A bounded QT decision may be used; no global SOTA claim follows. |

### Required negative and boundary controls

| Control | Expected failure/readout |
|---|---|
| Label permutation and majority/dummy baseline | Supervised performance collapses to the expected null; a model that still appears strong exposes leakage or a broken evaluator. |
| Same-document/source segments split across train and test | Split validator rejects the manifest before fitting. |
| Duplicate, near-duplicate, original/translation, or multiple-edition pair crosses splits | Contamination check rejects or groups the pair; no silent deduplication. |
| Feature selection, tokenization vocabulary, dictionary expansion, embedding fitting, or calibration sees sealed data | Pipeline/trace check fails. |
| Dictionary polysemy, negation, quotation, attribution, historical spelling, OCR corruption, and target reversal | Context fixture must reach the intended false-positive/negative diagnostic. |
| Off-construct proxy (for example sentiment used as stance) | Construct validator or held-out comparison shows the proxy cannot license the target claim even if its own metric is high. |
| Codebook labels replaced by generic IDs or swapped among definitions | A codebook-following model tracks the definitions rather than label familiarity; shortcut-driven behavior fails. |
| Codebook exclusion added/removed while its trigger is present/absent | Prediction changes only in the logically applicable condition; ignored exclusions or trigger-word shortcuts fail. |
| LLM emits multiple, invented, or otherwise disallowed labels | Structured output/compliance gate fails before accuracy or downstream use is considered. |
| Codebook definition, clarification, or examples are ablated | Performance and error changes are recorded by component; no prompt/codebook form is assumed universally best. |
| Rare/negative-case erasure | Per-class recall and prevalence error expose the failure; aggregate accuracy cannot pass it. |
| Source/author/genre/edition shortcut | Group-held-out and source-ablated results reveal the dependency; the item trace shows the shortcut features. |
| Ordered labels shuffled or adjacent levels collapsed | Ordinal advantage disappears or threshold checks fail; do not retain ordinal semantics. |
| Topic/embedding rerun across seeds, preprocessing, topic counts, and model families | Instability and unmatched topics are reported; an attractive single run cannot become the measure. |
| Semantically similar topic solutions yield divergent downstream signs/ranks | Topic model is barred from measurement use pending a separate validity design. |
| BERTopic outliers forcibly reassigned | Sensitivity report shows how reassignment changes prevalence/interpretation; original outlier state remains visible. |
| Mismatched joint-display denominators or units | Integration validator rejects the cell; no meta-inference is emitted. |
| Item anchor/source removed | Quantitative output and every aggregate depending on it fail provenance validation. |

## 7. Failure Modes and What to Try Next

| Failure | Meaning | What to try next |
|---|---|---|
| No category is both substantively useful and observable in text | The case does not support the proposed QT construct. | Return to qualitative analysis or choose another governed case; do not substitute sentiment or topics. |
| Too few independent source/document groups for a sealed split | Segment volume is pseudo-replication, not generalization evidence. | Use human-coded descriptive prevalence as a pilot, obtain a broader governed corpus, or select a different case. |
| Label disagreements cluster at category boundaries | Construct/codebook may be ambiguous or non-ordinal. | Refine inclusion/exclusion rules, preserve an uncertain class, collapse only with substantive justification, or abandon the construct. |
| Dictionary has high coverage but poor contextual precision | Lexical presence is not the construct. | Add reviewed phrases/context exclusions on development data, then retest sealed data; if still poor, use supervised measurement or change construct. |
| Supervised model beats dictionary only on random segment splits | Gain is leakage or source memorization. | Group by source/document/author/edition and rerun; if the gain disappears, keep the simpler honest measure or stop. |
| Accuracy is high but prevalence error or minority recall is poor | The metric is misaligned with the intended aggregate/error cost. | Optimize/evaluate the named prevalence quantity and rare-class cost; consider direct quantification methods, threshold/calibration changes on development data, or more labels. |
| Contextual model is strongest but cannot run within the governed processing boundary | The incumbent is operationally ineligible for this corpus. | Use an eligible local model/library and record the comparison gap; do not upload restricted text or claim strongest-model parity. |
| Ordinal proportional-odds/threshold assumptions fail | Ordered levels do not share one stable latent scale/model. | Use a nominal classifier, partial/alternative ordinal model, or report separate categories; do not impose interval meaning. |
| Topic labels are coherent but runs/downstream results are unstable | Discovery surface is not a valid measure. | Retain it as a qualitative sampling aid; validate a resulting category through A-C from scratch. |
| No candidate beats human-only/simple baselines within preregistered margins | Automation is not licensed. | Publish the null, keep human coding for this case, and use errors to select the next experiment. |
| A second real slice needs a materially different contract | No shared engine boundary exists yet. | Keep project-specific adapters; extract only genuinely repeated low-level utilities. |

## 8. Exact Decision Requested from Brian

After Lane A selects or narrows the governed case, Brian must decide:

> **Should the first QT slice target the prevalence/ordered distribution of one
> observable QC-derived category in that frozen corpus, with a narrow
> `mixed_methods_workbench`-owned adapter; require human/dummy/dictionary and
> regularized supervised comparisons; select dictionary versus supervised
> primary instrumentation only after a leakage-safe feasibility readout; and
> prohibit topic/embedding output from serving as the first measure?**

If yes, Brian must additionally name or approve the exact case-supported
construct and separately authorize the QT implementation slice after the
feasibility protocol is written. If no, Brian must choose a different intended
quantitative inference (not merely a model family) and its failure cost.

Still blocked after this report:

- the governed case, corpus denominator, rights, language/edition, and source
  grouping;
- the exact construct, item unit, population/frame, and intended use;
- observed label prevalence, independent-group count, annotation burden, and
  achievable noise floor;
- the exact library/model, metrics, margins, split sizes, power rationale, and
  strongest relevant incumbent;
- the typed `QuantitativeTextMeasurement` contract and adapter implementation;
- any `QT`, `MM`, product, or SOTA evidence promotion.

This report is research, not approval or implementation authority.

## 9. Sources Consulted

### Local authority and context

All accessed from the decision worktree on 2026-07-12:

- `.claude/tasks/decision_research_context.md` — complete frozen lane mission,
  facts, boundaries, required candidates, and report shape.
- `docs/ROADMAP.md`, especially 0.4 — exploratory-sequential build and default
  narrow adapter around established libraries.
- `docs/MIXED_METHODS_CAPABILITY_MAP.md`, quantitative-text and ownership
  sections — current F owner gap, validity obligations, and prohibition on a
  premature generic engine.
- `docs/CAPABILITY_DEPENDENCY_GRAPH.md` — QT dependencies, evidence, and claim
  license.
- `docs/CONCERNS.md` C018 — unresolved owner/task decision.
- `plan/goals/2026-07-12-sota-or-beyond.md`, `PROJECT.md`, and `CLAUDE.md` —
  long-term claim limits and producer/workbench method boundaries.

### Primary methods and validation research

- Michael D. Fetters, Leslie A. Curry, and John W. Creswell, “Achieving
  Integration in Mixed Methods Designs—Principles and Practices” (2013),
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4097839/> — design/method/reporting
  integration and connecting/building/merging/embedding. Open primary article.
- Justin Grimmer and Brandon M. Stewart, “Text as Data: The Promise and
  Pitfalls of Automatic Content Analysis Methods for Political Texts” (2013),
  DOI <https://doi.org/10.1093/pan/mps028>; author page
  <https://brandonstewart.org/publication/text-data-promise-and-pitfalls-automatic-content-analysis-methods-political/>
  — no universal best method, close reading, and application-specific
  validation for supervised and unsupervised methods.
- Lukas Birkenmaier, Clemens M. Lechner, and Claudia Wagner, “The Search for
  Solid Ground in Text as Data” (2024),
  <https://doi.org/10.1080/19312458.2023.2285765> — systematic validation review
  and construct-first measurement recommendations. Review evidence, not a
  universal benchmark.
- Daniel J. Hopkins and Gary King, “A Method of Automated Nonparametric Content
  Analysis for Social Science” (2010),
  <https://doi.org/10.1111/j.1540-5907.2009.00428.x>; Harvard manuscript
  <https://gking.harvard.edu/files/gking/files/words.pdf> — individual
  classification accuracy can misestimate aggregate category prevalence; direct
  quantification is a relevant later comparator. The method is not assumed to
  fit the unknown case.
- Samuel E. Bestvater and Burt L. Monroe, “Sentiment is Not Stance” (2023),
  <https://doi.org/10.1017/pan.2022.10> — construct mismatch across dictionary,
  SVM, and contextual models can degrade both classification and downstream
  inference. Demonstrated on political survey/social data; transfer to the
  future case is an inference.
- Luwei Ying, Jacob M. Montgomery, and Brandon M. Stewart, “Topics, Concepts,
  and Measurement” (2022), <https://doi.org/10.1017/pan.2021.33> — structured
  human validation for topic words/documents and the distinction between
  interpretable topics and valid concepts.
- Bolun Zhang, Yimang Zhou, and Dai Li, “Can Human Reading Validate a Topic
  Model?” (2025), <https://doi.org/10.1177/00811750241265336> — semantically
  similar topic solutions can support conflicting downstream statistical
  results; reading/coherence alone is insufficient for measurement.
- Andrew Halterman and Katherine A. Keith, “Codebook LLMs: Evaluating LLMs as
  Measurement Tools for Political Science Concepts” (Political Analysis 34(2),
  2026), <https://doi.org/10.1017/pan.2025.10017> — five-stage codebook-LLM
  evaluation, codebook-specific behavioral tests, variable zero-shot/per-class
  performance, manual compliance/error analysis, and supervised tuning. Its
  three English political-science datasets do not establish a general LLM
  winner or performance on the future governed case.
- Margaret E. Roberts, Brandon M. Stewart, and Dustin Tingley, “stm: An R
  Package for Structural Topic Models” (2019),
  <https://doi.org/10.18637/jss.v091.i02> — official peer-reviewed package paper
  for document metadata, uncertainty, exploration, and quantities of interest.

### Current official library documentation

- quanteda 4.4 dictionary, lookup, KWIC, and package references:
  <https://quanteda.io/reference/dictionary.html>,
  <https://quanteda.io/reference/dfm_lookup.html>,
  <https://quanteda.io/reference/kwic.html>, and
  <https://quanteda.io/reference/index.html>. These establish transparent
  matching/count/context operations, not construct validity.
- scikit-learn 1.9 cross-validation/grouped splits, leakage, calibration, and
  metrics:
  <https://scikit-learn.org/stable/modules/cross_validation.html>,
  <https://scikit-learn.org/stable/common_pitfalls.html#data-leakage>,
  <https://scikit-learn.org/stable/modules/calibration.html>,
  <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html>,
  <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html>,
  and
  <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html>.
  Version is the documentation version observed on the access date, not a
  future implementation pin.
- statsmodels 0.14.6 `OrderedModel`:
  <https://www.statsmodels.org/stable/generated/statsmodels.miscmodels.ordinal_model.OrderedModel.html>
  — ordered logit/probit behavior and assumptions; official docs mark the class
  experimental.
- STM official site <https://www.structuraltopicmodel.com/> — project/package
  surface; the JSS paper above supplies the peer-reviewed method description.
- BERTopic official docs:
  <https://maartengr.github.io/BERTopic/>,
  <https://maartengr.github.io/BERTopic/api/bertopic.html>, and
  <https://maartengr.github.io/BERTopic/faq.html> — modular pipeline,
  probabilities/approximations, representative documents, mappings, outliers,
  and parameter sensitivity. These are feature claims from project docs, not
  independent validation.

### Skipped sources and why

- Proprietary lexicons/tools such as current LIWC were not selected as a
  baseline because no construct, language, license, or allowed processing
  boundary is known. quanteda's ability to import LIWC formats is not a license
  or validity finding.
- General public NLP leaderboards were skipped because their tasks, languages,
  corpora, units, and error costs do not define the future case's strongest
  relevant incumbent.
- LLM/foundation-model classifiers were not made a default. Halterman and Keith
  were consulted to define their additional codebook/compliance gates. A
  task-specific contextual model may become an incumbent only after GOV,
  privacy/rights, exact model access, baseline comparisons, behavioral tests,
  and a frozen benchmark are known.
- Lane A case/source pages were not searched; case governance is intentionally
  owned by the parallel lane. This report makes every task recommendation
  conditional on its result.
- Producer repositories were not inspected or edited. Current canonical local
  documents already define their ownership boundaries; implementation
  readiness is outside this lane.
- Generic tutorials, vendor marketing, Wikipedia, Reddit, and unreviewed
  convenience comparisons were excluded from substantive conclusions.

### Null results and unresolved evidence

- No existing local quantitative-text adapter owner, task, instrument, or
  benchmark was found in current project authority.
- No case-free source establishes a universal best dictionary, classifier,
  topic model, metric threshold, or minimum labeled sample.
- No evidence currently establishes that the proposed Brumaire packet—or any
  alternative Lane A may recommend—has enough independent documents, category
  prevalence, language stability, or labelability for supervised evaluation.
- No reviewed source makes topic coherence, face-valid labels, or embedding
  clusters sufficient evidence of a social construct measure.
- No evidence supports assigning QT to QC/PT or creating a shared engine before
  the first real slice.

### Freshness triggers

Refresh this research when any of the following occurs:

- Lane A/Brian selects a governed case, edition/language, processing boundary,
  or exact construct;
- a corpus pilot reports independent groups, label prevalence, disagreement,
  leakage, or learning curves;
- a named implementation slice chooses a library/model or a current model/API
  is required;
- quanteda, scikit-learn, statsmodels, STM, BERTopic, or the strongest relevant
  task-specific incumbent has a material release;
- a second real QT slice creates evidence for shared extraction;
- a new primary validation review or topic-model measurement result materially
  changes the failure model;
- a public mixed-methods or SOTA claim is contemplated.
