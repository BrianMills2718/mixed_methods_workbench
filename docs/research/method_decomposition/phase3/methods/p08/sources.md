# P08 frozen sources

Frozen 2026-08-13, before the P08 records were authored. Post-freeze corrections dated 2026-10-08 are listed at the end; the frozen variant did not change.

Primary: Rob J. Hyndman and George Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed. (OTexts, 2021): §1.3 (determining what to forecast), §1.6 (the basic steps in a forecasting task), §§5.2–5.4 (simple forecasting methods, fitted values and residuals, residual diagnostics), §5.5 (distributional forecasts and prediction intervals), §§5.8–5.10 (evaluating point forecast accuracy, evaluating distributional forecast accuracy, time series cross-validation). Added 2026-10-08: §13.4 (forecast combinations). [Official text](https://otexts.com/fpp3/)

Corroborating: Tilmann Gneiting and Adrian E. Raftery, “Strictly Proper Scoring Rules, Prediction, and Estimation,” *JASA* 102(477), 2007, §§2–4. [DOI](https://doi.org/10.1198/016214506000001437)

Real-time data authority (added 2026-10-08): Dean Croushore, “Frontiers of Real-Time Data Analysis,” *Journal of Economic Literature* 49(1), 2011, pp. 72–100. [DOI](https://doi.org/10.1257/jel.49.1.72) Anchored at article level; its section numbering was not confirmed (see `uncertainty.yaml` p08.u06).

These sources require a clear forecast task, meaningful simple benchmarks, evaluation on data unavailable at forecast origin, horizon-matched scoring, and uncertainty expressed as a predictive distribution. Croushore adds that historical evaluation must use the data vintages available at each origin, not later revised values. Proper scores reward honest probabilistic forecasts; they do not establish causality.

Boundary: historical backtesting estimates performance in represented regimes. It cannot guarantee future stability, identify effects of interventions, or license rewriting an issued forecast after observing its outcome.

## Post-freeze source corrections (2026-10-08)

Made in response to the 2026-10-08 control review (`lane_receipts/reviews/2026-10-08-P3-RESEARCH-B.json`). The 2026-08-13 freeze date stays the variant's freeze date.

- **FPP3 section list corrected.** The freeze listed §§1.4 and 1.6 as "scope and task" and §3.5 as "distributional forecasts and intervals". In FPP3, §1.4 is "Forecasting data and methods" and §3.5 is "Methods used by official statistics agencies"; task scope is §1.3 and distributional forecasts are §5.5. The frozen list is now 1.3, 1.6, 5.2–5.5, 5.8–5.10. Re-anchored: target [1.3, 1.6]; issue [1.6, 5.5].
- **§13.4 added** for p08.move.select, which may issue a declared combination of evaluated procedures.
- **Croushore 2011 added** for p08.move.information's data-vintage rule, which FPP3 §§5.8/5.10 do not govern.
