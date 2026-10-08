# P02 frozen sources

Frozen before decomposition on 2026-08-13.

## Primary conduct authority

International Council for Harmonisation. *ICH E9: Statistical Principles for
Clinical Trials*, Step 5, 1998, sections 2–5 and §7.1 (Evaluation and
Reporting); and *ICH E9(R1) Addendum on
Estimands and Sensitivity Analysis in Clinical Trials*, Step 5, effective 2020,
sections A.2–A.5. [Official EMA guideline page and documents](https://www.ema.europa.eu/en/ich-e9-statistical-principles-clinical-trials-scientific-guideline).

The freeze uses E9 for confirmatory objectives, design (including §3.5 Sample
Size), conduct, analysis (including §5.5 Estimation, Confidence Intervals and
Hypothesis Testing and §5.6 Adjustment of Significance and Confidence Levels),
and §7.1 Evaluation and Reporting, and E9(R1) for the five estimand attributes, explicit intercurrent
events, treatment-policy strategy, aligned estimator, assumptions, and
sensitivity analysis. The exact frozen variant analyzes participants by their
randomized assignment regardless of declared intercurrent events.

Section numbers and titles were confirmed on 2026-10-08 against the table of
contents of the ICH E9 Step 4 PDF
(https://database.ich.org/sites/default/files/E9_Guideline.pdf): §3.4 Group
Sequential Designs, §3.5 Sample Size, §4.4 Sample Size Adjustment, §4.5
Interim Analysis and Early Stopping, §4.6 Role of Independent Data Monitoring
Committee, §5.5, §5.6, §5.8, and §7.1 Evaluation and Reporting. The variant
is fixed-sample: §§3.4 and 4.4–4.6 are cited only to name what frame.yaml
excludes.

## Corroborating policy-evaluation authority

HM Treasury and Evaluation Task Force. *Magenta Book Annex A: Analytical
methods for use within an evaluation*, updated 15 May 2026, section A2.1 on
randomized controlled trials. [Official HTML annex](https://www.gov.uk/government/publications/the-magenta-book/magenta-book-annex-a-analytical-methods-for-use-within-an-evaluation-html).

The annex corroborates random allocation as the basis for attributing outcome
differences to the intervention in policy evaluation. It does not supersede
ICH’s estimand and analysis requirements.

## Source-limit note

Clinical safety oversight and policy implementation ethics are important but
are not inferred from these statistical-method sources. Cluster, crossover,
factorial, noninferiority, and equivalence variants require new freezes.

## Exact-anchor registry

Against the linked official ICH documents: `p02.e9.2.2.2` = E9 §2.2.2,
`p02.e9.2.3.2` = §2.3.2 Randomization, `p02.e9.sections2_5` = E9 §§2–5,
`p02.e9.sections3_4` = §§3–4, `p02.e9.3.5` = §3.5 Sample Size,
`p02.e9.5.5` = §5.5 Estimation, Confidence Intervals and Hypothesis Testing,
`p02.e9.5.6` = §5.6 Adjustment of Significance and Confidence Levels
(multiplicity), `p02.e9.5.8` = §5.8 Integrity of Data and Computer Software
Validity, and `p02.e9.7.1` = §7.1 Evaluation and Reporting. `p02.e9r1.A3`, `.A4`, and `.A5`
resolve to E9(R1) §§A.3, A.4, and A.5; `.A3_A4` resolves to §§A.3–A.4.

Machine-resolvable IDs: `source:p02.e9.2.2.2`, `source:p02.e9.2.3.2`,
`source:p02.e9.3.5`, `source:p02.e9.5.5`, `source:p02.e9.5.6`,
`source:p02.e9.7.1`, `source:p02.e9.5.8`, `source:p02.e9.sections2_5`,
`source:p02.e9.sections3_4`, `source:p02.e9r1.A3`,
`source:p02.e9r1.A3_A4`, `source:p02.e9r1.A4`, and `source:p02.e9r1.A5`.

## Type extension note

`analysis_plan` is a type extension added because no existing type fits the
frozen protocol and statistical analysis plan of this trial. `review_protocol`
is the review-question protocol of an evidence synthesis (eligibility,
search, grouping); it carries no estimator, missing-data strategy,
multiplicity adjustment or sensitivity analysis bound to an estimand.
`design_parameters` are the numeric settings an execution action consumes
(allocation ratio, block size, sample size, as in `p02.move.sample_size`); they
do not record which estimator targets which estimand. The RCT plan's downstream
use is to freeze the confirmatory analysis before unblinding so that later
amendments are detectable as exploratory, which neither existing type states.
