# P03 frozen sources

Frozen before decomposition on 2026-08-13.

## Primary conduct authority

Baker A, Callaway B, Cunningham S, Goodman-Bacon A, Sant’Anna PHC.
“Difference-in-Differences Designs: A Practitioner’s Guide.” *Journal of
Economic Literature* 64(2), 2026, 498–557. DOI 10.1257/jel.20251650.
[Official AEA article](https://www.aeaweb.org/articles?id=10.1257%2Fjel.20251650).

Pinned scope: the organizing framework and guidance for the canonical simple
design, covariates, weights, multiple periods, identifying assumptions,
diagnostics, and sensitivity. The article explicitly distinguishes the simple
two-group design from staggered and other extensions; only the single-adoption
multi-period variant is frozen here.

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

Tokens resolve to the linked Baker et al. article as follows:
`p03.baker.simple_design` = canonical/simple-design section;
`data_design` = data organization and design framework; `identification` =
parallel-trends/no-anticipation assumptions; `pretrends` = pretrend and event-
study diagnostics; `estimation` = non-staggered estimation and inference;
`sensitivity` = robustness/sensitivity guidance; and `conclusions` = concluding
practice guidance. `p03.magenta.A2.7` resolves to Magenta Annex A §A2.7.
These heading locators bind the current official article/PDF; no staggered-
adoption content is imported into this variant.

Machine-resolvable IDs: `source:p03.baker.simple_design`,
`source:p03.baker.data_design`, `source:p03.baker.identification`,
`source:p03.baker.pretrends`, `source:p03.baker.estimation`,
`source:p03.baker.sensitivity`, `source:p03.baker.conclusions`, and
`source:p03.magenta.A2.7`.
