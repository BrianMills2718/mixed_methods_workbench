# P08 frozen sources

Frozen 2026-08-13, before the P08 records were authored.

Primary: Rob J. Hyndman and George Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed. (OTexts, 2021): §§1.4 and 1.6 (scope and task), §3.5 (distributional forecasts and intervals), §§5.2–5.4 (naive/seasonal baselines and residual diagnostics), §§5.8–5.10 (genuine out-of-sample and rolling-origin evaluation, including distributional accuracy). [Official text](https://otexts.com/fpp3/)

Corroborating: Tilmann Gneiting and Adrian E. Raftery, “Strictly Proper Scoring Rules, Prediction, and Estimation,” *JASA* 102(477), 2007, §§2–4. [DOI](https://doi.org/10.1198/016214506000001437)

These sources require a clear forecast task, meaningful simple benchmarks, evaluation on data unavailable at forecast origin, horizon-matched scoring, and uncertainty expressed as a predictive distribution. Proper scores reward honest probabilistic forecasts; they do not establish causality.

Boundary: historical backtesting estimates performance in represented regimes. It cannot guarantee future stability, identify effects of interventions, or license rewriting an issued forecast after observing its outcome.
