# P07 frozen sources

Frozen 2026-08-13, before the P07 records were authored. Post-freeze corrections dated 2026-10-08 are listed at the end; the frozen variant did not change.

Primary: Justin Grimmer and Brandon M. Stewart, “Text as Data: The Promise and Pitfalls of Automatic Content Analysis Methods for Political Texts,” *Political Analysis* 21(3), 2013, pp. 267–297, sections 2–5: §2 four principles (§2.1 all quantitative models of language are wrong but some are useful, §2.2 methods augment humans, §2.3 no globally best method, §2.4 validate, validate, validate), §3 acquiring text, §4 reducing complexity from words to numbers (representations), and §5 classifying documents into known categories, especially §5.2 supervised learning (§5.2.1 constructing a training set, §5.2.2 applying a supervised model, §5.2.3 validation). [DOI](https://doi.org/10.1093/pan/mps028) · [archived PDF](https://unstats.un.org/unsd/trade/events/2014/Beijing/documents/socialmedia/Grimmer%20and%20Stuart%20-%20Text%20as%20Data%20-%202013.pdf)

Page map for the archived PDF, which is the Advance Access version paginated pp. 1–31 (checked 2026-10-08): §2.1 p. 3, §2.2–2.3 p. 4, §2.4 and §3 p. 5, §4 p. 6, §5 p. 7, §5.2 p. 9, §5.2.1–5.2.2 p. 10, §5.2.3 p. 13. The issue pagination (pp. 267–297) was not checked page by page.

Corroborating target-specific authority (frozen): Alejandro Moreo and Fabrizio Sebastiani, “Learning to Quantify: Estimating Class Prevalence via Supervised Learning,” SIGIR 2019, pp. 1415–1416 (a tutorial abstract). [DOI](https://doi.org/10.1145/3331184.3331389)

Conduct-level quantification authority (added 2026-10-08): Andrea Esuli, Alessandro Fabris, Alejandro Moreo and Fabrizio Sebastiani, *Learning to Quantify* (Springer, The Information Retrieval Series, 2023), ch. 3 “Evaluation of Quantification Algorithms” (pp. 33–54) and ch. 4 “Methods for Learning to Quantify” (pp. 55–85). [Ch. 3 DOI](https://doi.org/10.1007/978-3-031-20467-8_3) · [Ch. 4 DOI](https://doi.org/10.1007/978-3-031-20467-8_4)

Reliability authority (added 2026-10-08): Klaus Krippendorff, *Content Analysis: An Introduction to Its Methodology*, 4th ed. (SAGE, 2018), ch. 12 “Reliability” (pp. 277–360). [Publisher record](https://collegepublishing.sagepub.com/products/content-analysis-4-258450)

Grimmer and Stewart require problem-specific validation against a substantive target, warn that methods do not discover meaning independently of human concepts, and (§5.2.1) require coding schemes to be developed iteratively: coders apply a draft codebook, ambiguities lead to revision, and the scheme is final only when coders apply it to new documents without noticing ambiguities. Krippendorff governs how coder agreement is assessed. Moreo and Sebastiani, and Esuli et al., distinguish quantification (estimating class prevalence) from individual classification; Esuli et al. supply the estimators and the evaluation measures for prevalence error.

Construct-validity boundary: a classifier can reproduce a coding protocol on held-out items while the protocol still fails to represent the intended policy construct. Accuracy, F1, or agreement therefore supports label-reproduction claims only; construct definition, annotation validity, domain transport, and prevalence error remain separately reviewable.

## Post-freeze source corrections (2026-10-08)

Made in response to the 2026-10-08 control review (`lane_receipts/reviews/2026-10-08-P3-RESEARCH-B.json`). The 2026-08-13 freeze date stays the variant's freeze date.

- **Quantification authority added.** Esuli et al. 2023 chs. 3–4 now anchor p07.move.validate (prevalence-error evaluation) and p07.move.quantify (estimator choice under prior-probability shift). Moreo and Sebastiani 2019 stays as the frozen corroborating citation.
- **Reliability authority added.** Krippendorff 2018 ch. 12 anchors the new pilot-coding move and the annotation move, alongside Grimmer and Stewart §5.2.1.
- **Section labels and link corrected.** The freeze described §3 as representations, §4 as supervised methods and §5 as validation. The article's own numbering is §3 acquiring text, §4 representations, §5.2 supervised learning, §5.2.3 validation; the paraphrased anchors (`principle_1`, `supervised_methods`, `validation`, `representations`) are replaced by these numbers. The old archived-PDF URL returned an HTML page; the link now points at the hosted PDF.
