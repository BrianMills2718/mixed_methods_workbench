# P03 frozen sources

Frozen before decomposition on 2026-08-13.

## Primary conduct authority

Baker A, Callaway B, Cunningham S, Goodman-Bacon A, Sant’Anna PHC.
“Difference-in-Differences Designs: A Practitioner’s Guide.” *Journal of
Economic Literature* 64(2), 2026, 498–557. DOI 10.1257/jel.20251650.
[Official AEA article](https://www.aeaweb.org/articles?id=10.1257%2Fjel.20251650).

Pinned scope, by numbered section: §3 2×2 DiD designs (§3.1 Causal effects
and target parameters: the ATT, including Assumption NA no-anticipation; §3.2
Identifying assumptions: parallel trends; §3.3 Estimation and inference); §4
Incorporating covariates into 2×2 DiD (§4.1 Covariate balance; §4.2
Identification under conditional parallel trends; §4.3 TWFE with covariates;
§4.4 Estimators with covariates that target the ATT; §4.5 Heterogeneity
analysis); §5.1 Simple event studies (2×T) (§5.1.1 post-treatment estimates;
§5.1.2 pre-period estimates, including the Rambachan and Roth bounds on
parallel-trends violations; §5.1.3 estimation and aggregation; §5.1.4
covariates in event studies); §6 Conclusion; and Appendix A.5 Repeated
cross-sections and unbalanced panel data (compositional change).

Explicitly excluded: §5.2 Staggered treatment adoption and all its
subsections, §5.3 Limitations of TWFE regressions, and Appendix A.1–A.4
(treatment turning on and off, continuous or multi-valued treatments, triple
differences, distributional DiD). §1–2 (introduction and running example) are
not cited as conduct authority.

Section numbers and titles were read on 2026-10-08 from arXiv 2503.13323v3
(https://arxiv.org/html/2503.13323v3), the authors' revised version of the
JEL article. The JEL page (https://www.aeaweb.org/articles?id=10.1257/jel.20251650)
confirms the citation but does not show internal headings, so the published
numbering is assumed to match and is recorded as source_limited in p03.u06.
The same reading found that inference with few clusters is not covered by the
article: footnote 32 in §6 lists it as out of scope and points to Roth et al.
(2023, §5).

## Corroborating policy-evaluation authority

HM Treasury and Evaluation Task Force. *Magenta Book Annex A: Analytical
methods for use within an evaluation*, updated 15 May 2026, section A2.7.
[Official PDF](https://assets.publishing.service.gov.uk/media/6a049bf75f39105e0848a21e/CCS0126982978-004_PN10640792_Magenta_Book_Annex_A_WEB_ACCESSIBLE__4_.pdf).

Section A2.7 describes comparing treated and untreated outcome trends before
and after intervention and requires the pre-intervention trends to support the
counterfactual. It corroborates policy use but does not make a pretrend test
proof of parallel untreated potential outcomes.

## Source-limit note

No staggered-adoption estimator, synthetic control, or generic regression
workflow is licensed by this freeze. Pretrend diagnostics can reveal problems;
they cannot verify the identifying assumption by themselves.

## Exact-anchor registry

Tokens resolve to numbered sections of Baker et al. (numbering per arXiv
2503.13323v3) as follows: `p03.baker.simple_design` = §3 with §3.1 (ATT and
no-anticipation); `identification` = §3.2 and §4.2; `covariates` = §4;
`covariate_balance` = §4.1; `estimation` = §3.3 and §§5.1.1–5.1.3;
`pretrends` = §5.1.2; `data_design` = §5.1 (2×T event-time structure) and
Appendix A.5 (repeated cross-sections, unbalanced panels and compositional
change); `sensitivity` = §5.1.2 (bounds on parallel-trends violations) only,
with the rest of the sensitivity move source_limited (p03.u05); and
`conclusions` = §6. `p03.magenta.A2.7` resolves to Magenta Annex A §A2.7.
These heading locators bind the current official article/PDF; no staggered-
adoption content is imported into this variant.

Machine-resolvable IDs: `source:p03.baker.simple_design`,
`source:p03.baker.covariates`, `source:p03.baker.covariate_balance`,
`source:p03.baker.data_design`, `source:p03.baker.identification`,
`source:p03.baker.pretrends`, `source:p03.baker.estimation`,
`source:p03.baker.sensitivity`, `source:p03.baker.conclusions`, and
`source:p03.magenta.A2.7`.

## Type extension note

`analysis_plan` is a type extension added because no existing type fits the
frozen DiD design and its conditioning specification. `review_protocol` is an
evidence-synthesis protocol and says nothing about treated and comparison
groups, adoption date, event-time windows, the parallel-trends form or the
inference method. `design_parameters` holds numeric settings an execution
consumes; the DiD design is a set of identifying commitments (which group is
the counterfactual, which covariates are conditioned on, which inference is
used) whose downstream use is to make a result-driven change detectable as a
prohibited transition (p03.c18, p03.c23), which neither existing type states.
