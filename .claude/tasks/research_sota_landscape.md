# Current SOTA Landscape for an Auditable Text-Centered Mixed-Methods Workbench

**Research cutoff:** 2026-07-12
**Access date for all external sources unless otherwise stated:** 2026-07-12
**Status:** Research synthesis for program planning; not an implementation specification and not evidence that this workbench is implemented or SOTA.
**Scope:** Mixed-methods integration and meta-inference; qualitative/CAQDAS provenance and interchange; process tracing; quantitative text analysis and qualitative-quantitative linkage; LLM-assisted qualitative research; reproducibility, FAIR, and governance; API and agent interoperability; evaluation; representative commercial and open tools.

> **Local sources consulted:** .claude/tasks/session_context.md · .claude/tasks/sota_program_progress.md · .claude/tasks/research_producer_readiness.md · .claude/HANDOFF.md · .claude/handoff.yml
> **Not used as completed evidence:** .claude/tasks/research_producer_readiness.md was an in-progress parallel-lane artifact when consulted and contained no finished readiness synthesis.
> **Local authority:** The workbench is documentation-only, producer engines retain their invariants, a quantitative strand is required before a mixed-methods claim, synthetic fixtures license at most C-grade shape claims, and research lanes are read-only (.claude/tasks/session_context.md:7-15). The verified baseline is overall F with a provenance-complete fixture-inventory gap (.claude/tasks/session_context.md:17-23). No universal SOTA score is permitted; evidence must be method-, task-, and domain-specific (.claude/tasks/sota_program_progress.md:19-26).

## 1. Executive conclusion

### Observed facts

1. **The most current comprehensive integration framework is promising but not yet a validated benchmark.** The 2024 Mixed Methods Integration Quality Framework (MMIQF) synthesized 135 methodological sources into 44 criteria across planning/data work, interpretation, reporting, and joint displays. Its authors explicitly call it a first iteration and say content validity, reliability, and applicability still require testing. Joint displays are treated as useful but not universally mandatory. [Fàbregues et al., 2024](https://journals.sagepub.com/doi/full/10.1177/15586898241257555) (accessed 2026-07-12).

2. **Published practice remains well below that methodological target.** A 2024 systematic review of 119 education studies found that, among 91 studies using generic integration strategies, 85.71% did not report a mixed-methods question and 74.73% did not report a data-mixing strategy; only 17 used a joint display. [Zhou, Zhou, and Machtmes, 2024](https://journals.sagepub.com/doi/10.1177/20597991231217937) (accessed 2026-07-12). A protocol to update GRAMMS to GRAMMS 2.0 was published in 2026, so the updated reporting guideline was not yet a completed standard at this cutoff. [GRAMMS 2.0 protocol, 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13040166/) (accessed 2026-07-12).

3. **No reviewed CAQDAS tool currently supplies the whole open-science stack.** A December 2025 systematic review of 28 tools found only 9 claiming REFI interoperability, 7 with audit features, 5 with real-time collaboration, 6 with Docker support, 3 with custom scripting, and 1 with a plugin architecture; no product met all selected FAIR/open-science criteria. It also found that none of the AI-enabled products disclosed system prompts and that no proprietary product offered on-premises AI analysis. [Küster and Wolf, 2025](https://doi.org/10.14279/eceasst.v85.2709) (accessed 2026-07-12).

4. **Process tracing has a substantial conduct/reporting gap.** A 2025 scoping review found 84 health applications, but only 19 provided greater methodological detail and only 8 of those demonstrated all four reported good-practice areas: explicit mechanistic theory, evidence linked to it, clear tracing of the mechanism, and analysis of counterfactuals or alternatives. [Johnson, Beach, and Al-Janabi, 2025](https://doi.org/10.1016/j.socscimed.2024.117539) (accessed 2026-07-12).

5. **LLM-assisted qualitative analysis is exploratory, uneven, and under-reported—not established autonomous SOTA.** A June 2026 peer-reviewed scoping review of 75 studies found GPT models in 93%, coding assistance in 43 studies, and theme identification in 41. Human/LLM agreement ranged from 36% to 99%; only 13 studies reported temperature, 12 context length, 4 top_p, and 10 gave no prompt detail. The review concludes that robust comparative evidence against high-quality human analysis is sparse and calls superiority claims premature. [Kempny et al., 2026](https://doi.org/10.1186/s12874-026-02913-1) (accessed 2026-07-12).

6. **The strongest technical direction is standards composition, not another monolith.** REFI-QDA provides open project/codebook exchange but warns that feature mismatch can cause data loss. W3C Web Annotation provides portable bodies, targets, selectors, lifecycle, agents, and rights. W3C PROV-O provides entity-activity-agent provenance. RO-Crate 1.3, released 2026-06-22, packages research objects and provenance. OpenAPI 3.2 describes agent- and human-usable HTTP interfaces. None alone supplies methodological validity. [REFI-QDA](https://www.qdasoftware.org/) · [W3C Web Annotation](https://www.w3.org/TR/annotation-model/) · [W3C PROV-O](https://www.w3.org/TR/prov-o/) · [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/index.html) · [OpenAPI 3.2](https://spec.openapis.org/oas/v3.2.0.html) (all accessed 2026-07-12).

### Inferences

- **High confidence:** There is no credible single product or accepted end-to-end benchmark against which “the mixed-methods workbench is SOTA” can be scored. The defensible unit of comparison is a named capability on a frozen task, corpus, method profile, and incumbent.
- **High confidence:** A workbench can plausibly exceed the demonstrated software landscape by joining cell-level evidence provenance, method-specific validity, loss-declared interchange, reproducible run packaging, and independent reproduction. Merely combining product features would not prove this.
- **High confidence:** Quantitative text analysis is the critical claim boundary. QC plus process tracing remains multi-method qualitative, consistent with the repo’s explicit constraint (.claude/tasks/session_context.md:9-14); true mixed-methods evidence starts only when a quantitative strand is linked and integrated.
- **Medium confidence:** MMIQF is the best current coverage scaffold for integration, but using all 44 items as an enforced pass/fail score would outrun its present validation. It should first be used for visible coverage and evidence collection.
- **Medium confidence:** LLMs are presently best treated as reviewable assistants for bounded, predominantly descriptive or deductive tasks. Their usefulness for interpretive synthesis is method-, construct-, language-, corpus-, model-, and prompt-dependent.

### Recommendations

- Define “SOTA” as **all applicable domain gates pass**, not a weighted average. A red provenance, governance, integration, or causal-claim gate cannot be offset by high model accuracy.
- Freeze a modular public benchmark plus a sealed held-out component, compare against task-appropriate incumbents, record uncertainty, and require independent artifact review before any SOTA claim.
- Make every meta-inference traversable to its qualitative and quantitative strand inferences, each evidence item, the source version/anchor, transformation history, reviewer decisions, and caveats.
- Adopt standards through explicit profiles and conformance tests: REFI-QDA for CAQDAS interchange, W3C Web Annotation for anchors, PROV-O for lineage, RO-Crate 1.3 for research packaging, DataCite 4.7 for citable/versioned releases, and OpenAPI 3.2 for the HTTP contract. Do not claim semantic round-trip fidelity from schema validity alone.
- Keep MCP optional and downstream of a stable core/API. The May 2026 NSA guidance documents unresolved access-control, validation, approval, isolation, idempotency, and audit risks in MCP deployments. [NSA MCP Security Design Considerations, 2026](https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf) (accessed 2026-07-12).

## 2. Research method, scope, and stopping rule

### Questions

1. What current methodological criteria distinguish genuine mixed methods from parallel or multi-method work?
2. What standards and products can preserve source-to-claim provenance and exchange qualitative analysis?
3. What evidence discipline is required for process-tracing causal claims?
4. What constitutes defensible quantitative text measurement and linkage to qualitative constructs?
5. What is actually known—not marketed—about LLM-assisted qualitative validity and oversight?
6. What reproducibility, governance, interface, and evaluation evidence would license SOTA or beyond-SOTA claims?

### Collection protocol

- Searched methodological journals, PubMed/PMC, publisher pages, ACL/ACM proceedings, official standards bodies, government guidance, official project documentation, official vendor manuals, and recent systematic/scoping reviews.
- Preferred peer-reviewed methodological reviews and original framework papers for scientific claims; official specifications and vendor/project documentation for current features; preprints only where the field has no mature peer-reviewed benchmark.
- Separated reported product capability from independent evidence of methodological quality.
- Stopped once each domain had at least one contemporary review or benchmark plus primary/official framework evidence, and additional searches repeated the same gap: no general end-to-end mixed-methods workbench benchmark.

### Claim labels

- **Fact:** Directly reported by the cited source.
- **Inference:** Synthesis across sources; not asserted by any one source.
- **Recommendation:** Candidate design or gate for this program; not a consensus standard unless explicitly noted.
- Confidence is High when supported by a standard or convergent peer-reviewed sources, Medium for a single strong source or a cross-domain transfer, and Low for emerging preprints or incomplete tool evidence.

## 3. Mixed-methods integration and meta-inference quality

### Facts

- Fetters, Curry, and Creswell distinguish integration at design, methods, and interpretation/reporting levels. At methods level, their canonical mechanisms are connecting, building, merging, and embedding; at interpretation/reporting level they describe narrative, data transformation, and joint displays, with fit expressed as confirmation, expansion, or discordance. [Fetters, Curry, and Creswell, 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC4097839/) (accessed 2026-07-12).
- The NIH/OBSSR best-practices resource remains an authoritative foundation for rigorous design and grant review, but it dates from 2011 and is not a contemporary software or benchmark specification. [NIH OBSSR Best Practices](https://obssr.od.nih.gov/research-resources/mixed-methods-research) (accessed 2026-07-12).
- GRAMMS has six reporting criteria: rationale; design, priority, and sequence; separate component methods; where/how/by whom integration occurred; limitations of one method revealed by the other; and insights gained by mixing. EQUATOR continues to list the 2008 guideline, while a 2026 protocol is developing GRAMMS 2.0. [EQUATOR GRAMMS record](https://www.equator-network.org/reporting-guidelines/the-quality-of-mixed-methods-studies-in-health-services-research/) · [GRAMMS 2.0 protocol](https://pmc.ncbi.nlm.nih.gov/articles/PMC13040166/) (accessed 2026-07-12).
- MMAT 2018 is an appraisal instrument, not a reporting or execution standard. Its mixed-methods criteria address rationale, effective integration, adequate interpretation of integration, divergences/inconsistencies, and whether each component meets its own methodological criteria. [MMAT 2018 criteria](https://mixedmethodsappraisaltoolpublic.pbworks.com/w/file/fetch/127916259/MMAT_2018_criteria.pdf) (accessed 2026-07-12).
- MMIQF’s 44 criteria ask whether integration was planned; is coherent with design; creates interdependence; generates new meta-inferences; considers alternatives and oversimplification; answers the mixed-methods question; examines discrepancies; reports added value and barriers; and, where joint displays are used, aligns sources/constructs/aggregation and includes meta-inferences. Its authors explicitly say the framework still needs validation and optimization. [MMIQF, 2024](https://journals.sagepub.com/doi/full/10.1177/15586898241257555) (accessed 2026-07-12).
- Joint displays can support analysis rather than merely presentation. An empirical methodological paper used two levels of displays to identify confirmed, discordant, and expanded inferences. [Younas, Inayat, and Sundus, 2021](https://journals.sagepub.com/doi/10.1177/2632084320984374) (accessed 2026-07-12).

### Inferences

- **High confidence:** The defining technical object is not a dashboard containing qualitative and quantitative panels. It is a versioned integration plan plus explicit cross-strand relations that produce an added-value meta-inference.
- **High confidence:** Reporting completeness, methodological conduct, and appraisal quality are different dimensions. GRAMMS, MMAT, and MMIQF should not be collapsed into one checklist score.
- **Medium confidence:** MMIQF currently offers the strongest content coverage, but an independent reviewer rubric should distinguish its required workbench capabilities from items that are optional or not applicable to a given design.

### Recommendations

For every true mixed-methods study artifact, require:

1. A mixed-methods question and rationale that cannot be answered by either strand alone.
2. A declared design, priority, timing, sampling relation, and procedural diagram.
3. One or more typed integration operations—connect, build, merge, embed, or transform—with actor, input, output, and decision provenance.
4. A joint-display or equivalent integration artifact whose rows/cells identify constructs, strand evidence, aggregation level, relationship type, and resulting inference. The workbench may require this as a product contract even though MMIQF does not make joint displays universally mandatory.
5. Meta-inferences that explicitly classify convergence/confirmation, complementarity/expansion, discordance/divergence, or unresolved absence; examine rival explanations; state added value; and carry transfer/claim limits.
6. Separate strand-quality assessments before integration. Weak qualitative or quantitative evidence cannot become strong merely by being mixed.

## 4. Qualitative provenance, CAQDAS interchange, and method-specific validity

### Facts

- COREQ is a 32-item reporting checklist specifically for interviews and focus groups; SRQR is a 21-item general qualitative reporting standard. Neither is a provenance or interchange format. [EQUATOR COREQ](https://www.equator-network.org/reporting-guidelines/coreq/) · [SRQR primary record](https://pubmed.ncbi.nlm.nih.gov/24979285/) (accessed 2026-07-12).
- Qualitative quality is method-dependent. Audit trails, reflexivity, negative/deviant cases, thick description, and peer or participant engagement are widely discussed, but checklist techniques are not universal validity tests. Triangulation can increase comprehensiveness and reflexivity without automatically proving one “true” account. [Mays and Pope, 2000](https://pmc.ncbi.nlm.nih.gov/articles/PMC1117321/) · [Korstjens and Moser, 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC8816392/) (accessed 2026-07-12).
- Reflexive thematic analysis, codebook thematic analysis, and coding-reliability thematic analysis embody different assumptions. Applying inter-rater reliability as a universal gate would be inappropriate for reflexive thematic analysis, where researcher subjectivity and reflexive interpretation are analytic resources rather than noise to eliminate. [Byrne, 2022](https://doi.org/10.1007/s11135-021-01182-y) (accessed 2026-07-12).
- REFI-QDA defines open XML exchange for codebooks (.qdc) and projects (.qdpx), provides XSDs, and expects bidirectional import/export validated against the schema. The standard itself warns that software feature differences may cause loss or modification. [REFI-QDA overview](https://www.qdasoftware.org/) · [Project implementation files](https://www.qdasoftware.org/project-implementation-files) · [Codebook implementation files](https://www.qdasoftware.org/codebook-implementation-files) (accessed 2026-07-12).
- REFI-QDA is a preferred archival format at DANS and was developed by major vendors including ATLAS.ti, Dedoose, MAXQDA, NVivo, QDA Miner, Quirkos, and Transana. [DANS format guidance](https://dans.knaw.nl/en/file-formats/computer-assisted-qualitative-data-analysis-caqdas/refi-qda-qualitative-data-analysis/) (accessed 2026-07-12).
- W3C Web Annotation is a Recommendation designed for portable annotations. Its data model supplies bodies, targets, agents, lifecycle, rights, motivations, and selectors including text quote, text position, data position, XPath, CSS, fragments, SVG, and time state. [W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/) (accessed 2026-07-12).
- Annotation for Transparent Inquiry (ATI) links specific publication passages to source excerpts, full citations, analytic notes explaining generation/analysis/support, and—where ethical, legal, and practical—underlying repository data. It distinguishes data access, production transparency, and analytic transparency. [QDR ATI Guide](https://qdr.syr.edu/ati/guide-ati) · [QDR ATI project instructions](https://qdr.syr.edu/node/20665) (accessed 2026-07-12).
- The 2025 CAQDAS review found widespread deficits in auditability, interoperability, collaboration, security policy, and sustainable open tooling. REFI claims were present in 9 of 28 tools, detailed audit features in 7, and no tool satisfied the review’s complete selected open-science bundle. [Küster and Wolf, 2025](https://eceasst.org/index.php/eceasst/article/view/2709) (accessed 2026-07-12).

### Inferences

- **High confidence:** XSD-valid QDPX proves syntax, not semantic preservation. Cross-tool round trips need element-by-element manifests and explicit loss reports.
- **High confidence:** A durable internal annotation model should preserve both a quotation-based selector and a position/version selector. Position alone drifts under edits; quotation alone can be ambiguous.
- **High confidence:** Provenance must include analytical decisions—who proposed, accepted, rejected, merged, split, or redefined a code—not only file origin and timestamps.
- **Medium confidence:** W3C Web Annotation is a better internal anchoring substrate than adopting any one vendor’s project structure, while REFI-QDA remains the pragmatic CAQDAS exchange surface.

### Recommendations

- Define method profiles that declare which validity practices are applicable, optional, or epistemically incompatible. Never enforce coder agreement across every qualitative method.
- For each source, preserve a persistent study-local ID, original identifier, content hash, media type, language, corpus denominator membership, license/rights, sensitivity/access tier, version, and source lineage.
- For each annotation, preserve source version, exact excerpt, quote selector, position/time/data selector, annotator or model identity, timestamp, codebook version, motivation, confidence/uncertainty where methodologically appropriate, review state, and edit lineage.
- For each claim, preserve supporting, challenging, and absence evidence plus analytic memo and review history. ATI’s claim-to-source logic is the minimum intellectual model even when source access must remain restricted.
- Test REFI with a fixture matrix spanning Unicode, overlapping and discontinuous spans, code hierarchies, memos, cases/variables, multimedia/time anchors, multiple coders, and unsupported vendor-specific objects. Every omitted or transformed object must be surfaced; silent loss is a failure.

## 5. Process tracing and causal-claim discipline

### Facts

- Process tracing is a within-case method for drawing descriptive and causal inferences from diagnostic evidence about hypothesized causal mechanisms. Contemporary accounts distinguish narrative, test-based, Bayesian, and fuller mechanism-elucidation approaches. [Bennett, Fairfield, and Soifer, 2019](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3333405) · [Collier, 2011](https://www.cambridge.org/core/journals/ps-political-science-and-politics/article/understanding-process-tracing/183A057AD6A36783E678CB37440346D1) (accessed 2026-07-12).
- The familiar straw-in-the-wind, hoop, smoking-gun, and doubly-decisive tests differ in necessity and sufficiency. They organize diagnostic value; they are not interchangeable numeric confidence scores. [Collier, 2011](https://www.cambridge.org/core/journals/ps-political-science-and-politics/article/understanding-process-tracing/183A057AD6A36783E678CB37440346D1) · [World Bank IEG guidance](https://ieg.worldbankgroup.org/evaluation-international-development/chapter-3-guidance-notes-evaluation-approaches-and-methods) (accessed 2026-07-12).
- Bayesian process tracing asks how much more likely evidence is under one hypothesis than under rivals. Full formal Bayesian analysis is often impractical, and even advocates caution against forcing precise numbers for every item. [Fairfield and Charman, 2017](https://www.cambridge.org/core/journals/political-analysis/article/abs/explicit-bayesian-analysis-for-process-tracing-guidelines-opportunities-and-caveats/F93D3EA784730ED731AC910EEF306231) · [Bennett, 2022](https://www.cambridge.org/core/books/case-for-case-studies/process-tracing-for-program-evaluation/3282EBD903031583252019931E5C3BB9) (accessed 2026-07-12).
- Good contemporary applied practice operationalizes the mechanism into expected observables, links each observation to a mechanism step, evaluates alternatives/counterfactuals, and reports the trace. The 2025 health review shows this is still uncommon. [World Bank IEG operationalization guidance](https://ieg.worldbankgroup.org/evaluations/process-tracing-method-program-evaluation/chapter-2-tracing-process-theory-change) · [Johnson, Beach, and Al-Janabi, 2025](https://doi.org/10.1016/j.socscimed.2024.117539) (accessed 2026-07-12).
- A 2026 philosophy-of-science critique argues that process-tracing literature still lacks a consistent definition of causal mechanism and faces a real challenge connecting actual within-case observations to singular counterfactual causal claims. [Wang, 2026](https://doi.org/10.1177/00483931261441189) (accessed 2026-07-12).

### Inferences

- **High confidence:** The workbench must preserve PT’s rival-hypothesis and diagnostic-evidence logic instead of reducing it to a list of themes or code counts.
- **High confidence:** Source reliability, motivation, access, temporal proximity, and dependence affect evidence weight. Multiple reports deriving from one origin are not independent corroboration.
- **High confidence:** A PT verdict is case-bounded and mechanism-bounded. It does not estimate population effect size and must not inherit generalizability from an adjacent quantitative strand without a separate warrant.
- **Medium confidence:** Both categorical tests and explicit Bayesian judgments can be represented, but the schema must not fabricate pseudo-precision. Numeric, ordinal, and qualitative support modes should be discriminated and carry their rationales.

### Recommendations

Require every PT analysis to identify:

1. PT purpose: theory testing, theory building, or explaining an outcome.
2. Case and source-scope denominator, time bounds, outcome, mechanism, and each causal step.
3. Primary and rival hypotheses defined before decisive evidence is judged, with expected observations and expected absences under each.
4. Evidence identity, anchor, source provenance, reliability/credibility assessment, access/motivation, independence cluster, timing, and diagnostic assessment relative to every relevant rival.
5. Observed absences distinguished from unsearched or inaccessible evidence.
6. Update history, sensitivity to priors/weights/assumptions, unresolved contradictions, alternatives/counterfactuals, and bounded verdict language.
7. ATI-like links from each contestable causal claim to the evidence and analytic reasoning supporting it.

Hard negative controls should include duplicated dependent sources presented as independent, temporally impossible evidence, evidence outside the case scope, missing expected observations mislabeled as observed absence, a rival omitted from comparative assessment, and a strong verdict supported only by low-diagnostic evidence.

## 6. Quantitative text analysis and qualitative-quantitative linkage

### Facts

- Grimmer and Stewart’s durable principles remain that automated text models are useful but wrong abstractions, augment rather than replace close reading, have no universally best method, and require extensive application-specific validation. For supervised tasks they call for replication of human coding; for unsupervised measures they require experimental, substantive, and statistical validation. [Grimmer and Stewart, 2013](https://doi.org/10.1093/pan/mps028) (accessed 2026-07-12).
- A 2023 systematic review found no unified validation approach tailored to computational text analysis and proposed practical recommendations grounded in measurement validity. [Birkenmaier, Lechner, and Wagner, 2024](https://doi.org/10.1080/19312458.2023.2285765) (accessed 2026-07-12).
- Nelson’s computational grounded theory proposes pattern detection, qualitative refinement through deep reading, and computational confirmation. A later critique demonstrated instability and class-imbalance failures in LDA and argued for computer-assisted learning and measurement rather than computer-led discovery. [Nelson, 2020](https://csuned.github.io/resources/nelson-computational-grounded-theory-rotated.pdf) · [Carlsen and Ralund, 2022](https://doi.org/10.1177/20539517221080146) (accessed 2026-07-12).
- Human-readable topics are not automatically valid quantitative measures. A 2025 paper shows that semantically similar topic-model solutions can yield conflicting downstream statistical results and recommends validating downstream measurement stability, not only labels and exemplar documents. [Zhang, Zhou, and Li, 2025](https://doi.org/10.1177/00811750241265336) (accessed 2026-07-12).
- Established libraries cover different tasks rather than one SOTA stack. quanteda provides corpus/docvar management, Unicode-aware tokenization, document-feature matrices, dictionaries, scaling, and converters; STM adds document covariates and uncertainty; BERTopic is a modular embedding/clustering/topic-representation pipeline whose own documentation acknowledges difficult subjective evaluation. [quanteda](https://quanteda.io/reference/quanteda-package.html) · [STM](https://www.structuraltopicmodel.com/) · [BERTopic](https://bertopic.readthedocs.io/en/latest/) (accessed 2026-07-12).
- MMIQF specifically asks that side-by-side joint displays align qualitative and quantitative sources on the same constructs and aggregation level. [MMIQF criterion 39](https://journals.sagepub.com/doi/full/10.1177/15586898241257555) (accessed 2026-07-12).

### Inferences

- **High confidence:** “Use topic modeling” is not a quantitative-text task or a validation plan. The workbench first needs a construct, unit, intended inference/use, population/corpus, measurement model, and error costs.
- **High confidence:** The linkage key must be designed before analysis: stable case, source, segment, time, and construct IDs are needed to connect quantitative outputs to qualitative evidence without ecological or aggregation mistakes.
- **High confidence:** Close reading belongs inside the quantitative-text validation loop, not only after model selection.
- **Medium confidence:** For the first true mixed-methods slice, a bounded supervised classification or dictionary/measurement task with an adjudicated held-out set will usually be easier to validate than unconstrained topic discovery. This is a risk-order recommendation, not a universal methodological preference.

### Recommendations

- Choose the first quantitative-text task by intended use and failure cost, then compare simple transparent baselines (counts/dictionary or regularized linear model as applicable) with more complex incumbents.
- Freeze corpus membership and train/development/held-out partitions before tuning. Keep a sealed or temporally later set where possible; document all overlap and contamination checks.
- Report construct validity, annotation/codebook quality where applicable, class prevalence, precision/recall or task-appropriate metrics by class, calibration/uncertainty, subgroup/language/domain slices, robustness to preprocessing and seeds, and a qualitative error analysis.
- Preserve item-level model outputs and transformations so every aggregate can be drilled back to source text.
- Integrate at matched units and constructs. A joint-display cell must declare the denominator and aggregation level for both strands; mismatched case, time, or source scopes are a hard failure.
- The handoff confirms that no quantitative-text owner, task, instrument, or evaluation design currently exists, making this the largest local gap before a mixed-methods claim (.claude/HANDOFF.md:134-137).

## 7. LLM-assisted qualitative analysis, validity, and oversight

### Facts

- The strongest current peer-reviewed synthesis is Kempny et al.'s 2026 scoping review of 75 studies. Most work used GPT-family models; common tasks were coding assistance and theme identification. Reported human/model agreement ranged from 36% to 99%, while prompt and sampling details were often absent. The review found stronger evidence for descriptive or deductive assistance than deep interpretive analysis and judged superiority claims premature. [Kempny et al., 2026](https://doi.org/10.1186/s12874-026-02913-1) (accessed 2026-07-12).
- A June 2026 preprint systematic review of 39 studies reports highly variable agreement and a recurring drop from semantic/descriptive tasks to contextual or interpretive ones. It is useful emerging evidence, not a settled benchmark. [Sciety record and preprint, 2026](https://sciety.org/articles/activity/10.31234/osf.io/gnx8p_v1) (accessed 2026-07-12).
- COREQ does not cover LLM-specific disclosure. A COREQ+LLM reporting extension is under development, but the available 2025 publication is a protocol rather than a completed guideline. [COREQ+LLM protocol, 2025](https://www.researchprotocols.org/2025/1/e78682/) (accessed 2026-07-12).
- CollabCoder operationalizes a human-centered workflow of independent open coding, comparison, discussion/conflict resolution, and a final codebook with decision records. CoAIcoder found that an AI mediator could improve early agreement but could also reduce code diversity. These are research prototypes and do not establish general validity. [CollabCoder, CHI 2024](https://doi.org/10.1145/3613904.3642002) · [CoAIcoder, CSCW 2023](https://doi.org/10.1145/3617362) (accessed 2026-07-12).
- A 2026 benchmark preprint covering 46 LLMs and 150 high-fidelity synthetic interview transcripts found that aggregate reliability remained inadequate for autonomous deductive coding and recommended theme-specific, tiered oversight. Synthetic data and preprint status limit the claim. [Humanitarian qualitative coding benchmark, 2026](https://arxiv.org/abs/2606.26541) (accessed 2026-07-12).
- NIST's AI RMF organizes risk work around Govern, Map, Measure, and Manage, including defined human/AI roles, documented testing/evaluation/verification/validation, and monitoring after deployment. It is a governance framework, not evidence that any qualitative output is valid. [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) · [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) (accessed 2026-07-12).

### Inferences

- **High confidence:** An LLM completion is a proposal or measurement output, not an analytic decision. Validity comes from the method-specific review process, source-grounded evidence, and documented resolution—not model fluency.
- **High confidence:** Aggregate agreement conceals theme-, class-, language-, subgroup-, and difficulty-specific failure. Oversight must be allocated from observed risk at that granularity.
- **High confidence:** Reproducibility requires the exact provider/model version, prompt/template/schema versions, full parameters, input manifest, tool/retrieval context, output, parser/validation results, cost/latency record, reviewer actions, and run lineage. A model name alone is inadequate.
- **Medium confidence:** Independent-first coding followed by disclosed comparison is safer for exploratory coding than exposing the human to an AI-generated codebook first, because automation anchoring may narrow the interpretive space.

### Recommendations

- Permit only named LLM roles with explicit intended use, prohibited uses, risk tier, review policy, and escalation path. Autonomous causal verdicts, final themes, or meta-inferences should be prohibited until a task-specific benchmark and independent review license them.
- Make every suggestion source-anchored and visibly attributable to a model run. Preserve rejected suggestions and human edits so agreement is not manufactured by deleting disagreement.
- Use a frozen adjudicated test set and negative controls for hallucinated quotations, nonexistent sources, span drift, minority-class erasure, prompt injection, sensitive-data leakage, unsupported causal language, and persuasive but evidence-free synthesis.
- Evaluate assistance against both human-only and simple programmatic baselines. Measure error, omission, diversity loss, reviewer effort/time, override patterns, subgroup performance, and downstream inference changes—not agreement alone.
- Keep sensitive material local or within an explicitly governed processing boundary. Annotaid demonstrates that bounded local/browser inference is feasible, but its CSV coding scope is not an end-to-end validity result. [Annotaid, 2026](https://doi.org/10.1016/j.softx.2026.102702) (accessed 2026-07-12).

## 8. Reproducibility, FAIR, CARE, provenance, and release governance

### Facts

- FAIR means Findable, Accessible, Interoperable, and Reusable for data and metadata. FAIR does not mean open, and it does not by itself address ethics or collective rights. [Wilkinson et al., 2016](https://doi.org/10.1038/sdata.2016.18) · [GO FAIR clarification](https://www.go-fair.org/resources/faq/what-fair-is-not/) (accessed 2026-07-12).
- CARE complements FAIR for Indigenous data governance through Collective Benefit, Authority to Control, Responsibility, and Ethics. [Global Indigenous Data Alliance CARE Principles](https://www.gida-global.org/careprinciples) · [Carroll et al., 2020](https://datascience.codata.org/articles/dsj-2020-043) (accessed 2026-07-12).
- W3C PROV-O models entities, activities, agents, generation, use, derivation, attribution, association, and delegation. It is intentionally generic and needs a domain profile to make research actions and roles precise. [W3C PROV-O](https://www.w3.org/TR/prov-o/) (accessed 2026-07-12).
- RO-Crate 1.3 became a Recommendation on 2026-06-22 and packages a research object using JSON-LD metadata. Workflow Run Crate profiles at this cutoff still identify RO-Crate 1.1 as their base; the RO-Crate project says updates are forthcoming. [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/index.html) · [Process Run Crate 0.5](https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/) · [1.3 release note](https://www.researchobject.org/ro-crate/blog/2026-06-23/announcing-ro-crate-1-3) (accessed 2026-07-12).
- DataCite Metadata Schema 4.7, released in March 2026, is the current citable-resource metadata schema and includes version and relation semantics. [DataCite schema](https://schema.datacite.org/) · [version history](https://schema.datacite.org/versions.html) (accessed 2026-07-12).
- The US National Academies distinguish computational reproducibility—consistent results using the same inputs, code, methods, and conditions—from replicability, which obtains consistent results from new data addressing the same question. [National Academies, 2019](https://www.nationalacademies.org/read/25303/chapter/3) (accessed 2026-07-12).
- ACM artifact review separates artifacts that are Available, Functional, or Reusable from results independently Reproduced. A functional artifact is therefore not evidence of independent reproduction. [ACM artifact review and badging](https://www.acm.org/articles/pubs-newsletter/2021/blue-diamond-may-2021) (accessed 2026-07-12).

### Inferences

- **High confidence:** Public openness cannot be a universal gate for sensitive qualitative research. The gate is FAIR, access-governed metadata plus an executable or reviewable pathway appropriate to consent, law, licenses, and community authority.
- **High confidence:** Reproducibility must bind source snapshots, code/environment, configuration, prompts/schemas, model/tool versions, reviewer decisions, and generated outputs into one immutable run identity.
- **Medium confidence:** RO-Crate plus PROV-O is a strong packaging direction, but the new 1.3/profile version mismatch makes immediate profile selection and conformance testing necessary rather than assuming compatibility.

### Recommendations

- Produce a manifest for every run containing content-addressed inputs/outputs, source/version IDs, environment lock, code commit, configuration, random seeds, model/tool identities, rights/access metadata, actors, timestamps, and derivation edges.
- Maintain separate public metadata, controlled-access evidence, and restricted or non-exportable data layers. A denied access request can still be FAIR when the access conditions are discoverable and justified.
- Create immutable versioned releases with DataCite-compatible metadata and explicit isNewVersionOf/isPreviousVersionOf relations. Never overwrite an evidentiary artifact in place.
- Require two distinct tests: same-environment replay and clean-room replay from the packaged artifact. Beyond-SOTA evidence requires reproduction by a person or team independent of the implementer.
- Treat ethics, consent, Indigenous/community governance, and source licensing as release gates, not prose appended after analysis.

## 9. Interoperability, APIs, and agent-drivability

### Facts

- OpenAPI 3.2.0, released 2025-09-19, describes language-agnostic HTTP interfaces so both humans and computers can discover and interact with a service. Its schema dialect is based on JSON Schema Draft 2020-12. [OpenAPI 3.2.0](https://spec.openapis.org/oas/v3.2.0.html) · [JSON Schema specification](https://json-schema.org/specification) (accessed 2026-07-12).
- CATMA exposes a read-only OpenAPI JSON API over collaborative, stand-off qualitative annotations; INCEpTION exposes remote APIs alongside curation, agreement, audit logs, recommenders, and broad annotation-format support. These demonstrate useful components, not full mixed-methods integration. [CATMA JSON API](https://catma.de/documentation/access-your-project-data/json-api/) · [INCEpTION administration guide](https://inception-project.github.io/documentation/latest/admin-guide) (accessed 2026-07-12).
- MCP can make tools and resources discoverable to model clients, but the May 2026 NSA guidance identifies recurring risks including weak access boundaries, insufficient schema validation, inadequate approvals, missing idempotency/audit, context leakage, and tool injection. [NSA MCP Security Design Considerations](https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf) (accessed 2026-07-12).

### Inferences

- **High confidence:** Agent-drivable means semantic parity with human operations through typed, documented, observable, authorized interfaces. Merely exposing an MCP server or command line does not meet that standard.
- **High confidence:** A core typed library and OpenAPI surface should be authoritative; UI, CLI, notebooks, and optional MCP adapters should invoke the same operations and policies.
- **High confidence:** Every mutating operation needs stable identities, idempotency, preconditions, actor attribution, structured errors, audit events, and a machine-readable dry-run or preview when consequences are material.

### Recommendations

- Publish a versioned OpenAPI 3.2 contract generated from the same typed domain models as the core. Validate requests and responses, reject unknown durable fields at producer boundaries, and test backward-compatible consumers against supported versions.
- Provide discovery, pagination, filtering, export, provenance traversal, and task-status endpoints. Long operations need durable run IDs and resumable event streams rather than hidden client state.
- Enforce API/UI/CLI parity with contract tests: every display has a read endpoint; every human action has a typed operation; authorization and validation cannot exist only in the UI.
- Keep MCP an optional least-privilege adapter with explicit tool allowlists, bounded result sizes, injection-resistant data/tool separation, human approval for high-consequence writes, and the same immutable audit trail.
- Benchmark agents by completion correctness, invalid-action rejection, provenance completeness, recovery/idempotency, and least-privilege behavior—not by whether an agent eventually produced a plausible screen state.

## 10. Evaluation, negative controls, held-out evidence, and independent review

### Facts

- Negative controls are exposures or outcomes for which a causal relation is not expected; unexpected associations can reveal confounding or other systematic bias. The principle transfers to software and analytic pipelines as deliberately invalid cases that should fail for known reasons. [Lipsitch, Tchetgen Tchetgen, and Cohen, 2010](https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/) (accessed 2026-07-12).
- CheckList showed that aggregate held-out accuracy misses important behavioral failures. Its minimum-functionality, invariance, and directional-expectation tests found critical bugs in commercial and research NLP systems; practitioners created more tests and found more bugs using the method. [Ribeiro et al., ACL 2020](https://aclanthology.org/2020.acl-main.442/) (accessed 2026-07-12).
- Evaluation leakage and grader gaming can invalidate agent benchmarks. NIST identifies solution contamination and gaming of graders as distinct ways an agent can appear capable without solving the intended task. [NIST on cheating in AI-agent evaluations](https://www.nist.gov/caisi/cheating-ai-agent-evaluations) (accessed 2026-07-12). A 2024 ACL survey likewise documents benchmark data contamination as a live LLM-evaluation problem. [Deng et al., 2024](https://aclanthology.org/2024.findings-acl.951/) (accessed 2026-07-12).
- NIST ARIA evaluates model testing, red-teaming, and field testing as distinct levels, reinforcing that laboratory benchmark performance is not deployment evidence. [NIST ARIA](https://ai-challenges.nist.gov/aria) (accessed 2026-07-12).

### Inferences

- **High confidence:** A green happy-path fixture is demonstration, not validation. Every gate needs known-positive, known-negative, boundary, metamorphic, and realistic held-out cases where applicable.
- **High confidence:** Benchmark development and final adjudication must be separated. A test authored and repeatedly seen by the implementing agent cannot serve as the only held-out evidence.
- **High confidence:** Independent review must verify raw trace and artifacts, not only a final report. Plausible meta-inferences can conceal broken anchors, starved inputs, silent loss, or omitted rivals.

### Recommendations

- Build a benchmark registry recording construct, intended use, corpus, license/consent, split policy, contamination risk, provenance, adjudication, metrics, uncertainty, incumbent, and expiration trigger.
- For deterministic seams require complete invariant coverage and deliberately broken fixtures. For statistical/LLM tasks pre-register task-specific metrics and decision margins, report uncertainty and slices, and retain qualitative error analysis.
- Keep a public development suite plus a sealed held-out or temporally later suite administered by a different actor. Rotate it when leakage is plausible.
- Require reproducibility review, methodological review, security/privacy review, and adversarial negative-control review before a cross-domain SOTA claim. Reviewers must have authority to reject it.
- Publish failures and null comparisons. A capability that does not beat its incumbent remains useful engineering but is not SOTA evidence.

## 11. Incumbent tool landscape

The table is a capability baseline assembled from official product/project documentation and the independent 2025 CAQDAS review. Vendor feature claims are not evidence of research validity, and a blank does not prove the feature is impossible.

| Incumbent | Demonstrated or claimed strengths | Important boundary for this program |
|---|---|---|
| MAXQDA 26 | Qualitative coding, Stats module, mixed-methods worksheets, joint displays, SPSS exchange, REFI | Closed product; feature breadth does not prove source-to-meta-inference provenance or independent reproducibility. [Official mixed-methods guide](https://www.maxqda.com/help/mixed-methods/general) · [release notes](https://www.maxqda.com/products/maxqda-release-notes) |
| NVivo + XLSTAT | Mature qualitative matrices/crosstabs and a separately marketed quantitative companion | Two-product workflow; official material does not establish lossless open round-trip or a validated meta-inference engine. [Official mixed-methods page](https://lumivero.com/solutions/mixed-methods-research-software/) |
| ATLAS.ti | Mature CAQDAS, collaboration, AI features, QDPX exchange | Proprietary; QDPX support still inherits cross-product feature mismatch; AI validity must be independently tested. [Features](https://atlasti.com/features) · [QDPX manual](https://manuals.atlasti.com/Mac/en/manual/Export/ExportQDPXUniversalDataExchange.html) |
| Dedoose | Web collaboration, descriptors, charts, integrated qualitative/quantitative views | Official converter notes loss of weighted codes, descriptor structures, links, datasets, and some memos in REFI conversion. [Product](https://www.dedoose.com/) · [converter limitations](https://wwwstage.dedoose.com/resources/converters) |
| QualCoder | Open source, local text/image/audio/video coding, reports, coder comparison, AI support, REFI | Strong open CAQDAS baseline; not an end-to-end mixed-methods provenance/reproduction benchmark. [Project repository](https://github.com/ccbogel/QualCoder) |
| Taguette | Simple open-source/self-hosted collaborative text coding; Docker deployment | QDC codebook exchange and project SQLite rather than a demonstrated full QDPX mixed-methods stack. [About](https://www.taguette.org/about.html) · [self-hosting](https://www.taguette.org/self-host.html) |
| CATMA | Open, collaborative stand-off annotation, TEI roots, OpenAPI read access | Annotation-centered and read-only API; not a quantitative integration or causal-analysis workbench. [Project](https://catma.de/) · [technology](https://catma.de/documentation/technology-and-versions/) |
| INCEpTION | Open annotation, curation, agreement, audit logs, recommenders, many formats, remote API | Strong annotation/review incumbent; not mixed-methods integration or process tracing. [User guide 40.3](https://inception-project.github.io/releases/40.3/docs/user-guide.html) |
| CollabCoder / CoAIcoder | Human-AI collaborative coding designs and conflict discussion | Research prototypes; narrow studies, not production/open-science stacks or general validity evidence. [CollabCoder](https://gaojie058.github.io/CollabCoder/) · [CoAIcoder](https://doi.org/10.1145/3617362) |

**Incumbent conclusion:** no reviewed product supplies, in one independently validated system, method-specific qualitative validity, rival-sensitive process tracing, validated quantitative text measurement, explicit mixed-methods operations and meta-inferences, loss-declared exchange, complete provenance, governed LLM assistance, reproducible packaging, typed agent parity, and independent benchmark evidence. That gap is an opportunity, not proof that this repo already exceeds the field.
