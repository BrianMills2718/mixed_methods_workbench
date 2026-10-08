# P09 frozen sources

Frozen 2026-08-13, before the P09 records were authored. Post-freeze corrections dated 2026-10-08 are listed at the end; the frozen variant did not change.

Description authority: Volker Grimm et al., “The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism,” *JASSS* 23(2), 2020, §§3–4 and its element checklists. [Primary article](https://www.jasss.org/23/2/7.html) · [author checklist](https://railsback-grimm-abm-book.com/E2-Downloads/Chapter03/ODD_GuidanceChecklists_2020.pdf)

Simulation experiment-design authority (added 2026-10-08): Jack P. C. Kleijnen, *Design and Analysis of Simulation Experiments*, 2nd ed. (Springer, International Series in Operations Research & Management Science, 2015), ch. 2 “Classic Regression Metamodels and Their Designs” (pp. 23–81) and ch. 3 “Classic Assumptions Versus Simulation Practice” (pp. 83–133). [Ch. 2 DOI](https://doi.org/10.1007/978-3-319-18087-8_2) · [Ch. 3 DOI](https://doi.org/10.1007/978-3-319-18087-8_3) Anchored at chapter level (see `uncertainty.yaml` p09.u08).

ABM conduct authority beyond ODD: Steven F. Railsback and Volker Grimm, *Agent-Based and Individual-Based Modeling: A Practical Introduction*, 2nd ed. (Princeton University Press, 2019): ch. 3 (ODD), ch. 4 (implementing a first ABM; §§4.2–4.3 from ODD to NetLogo), ch. 6 (testing your program; §6.3 techniques for debugging and testing, §6.4 documentation of tests), §8.3 (simulation experiments and BehaviorSpace, pp. 105–111; a tool-oriented section), ch. 20 (parameterization and calibration; §20.3 parameterizing submodels, §20.4 calibration concepts and strategies), ch. 22 (analyzing and understanding ABMs; §22.4 statistics for understanding), and ch. 23 (§23.2 sensitivity, §23.3 uncertainty, §23.4 robustness analysis). [Author site](https://www.railsback-grimm-abm-book.com/) · [publisher table of contents](https://assets.press.princeton.edu/releases/c14270.pdf)

Corroborating verification/validation authority: Robert G. Sargent, “Verification and Validation of Simulation Models,” *Journal of Simulation* 7(1), 2013, pp. 12–24, especially the distinctions among conceptual-model validity, computerized-model verification, operational validity, and data validity, plus the recommended validation procedure. [DOI](https://doi.org/10.1057/jos.2012.20)

Corroborating policy sensitivity authority: Ivano Azzini et al., *Uncertainty and Sensitivity Analysis for Policy Decision Making*, European Commission JRC, 2020, chs. 2–4. [Official record and PDF](https://publications.jrc.ec.europa.eu/repository/handle/JRC122132)

Authority boundary: ODD tells a reader what the model is and why it was built. Kleijnen governs the design of the simulation experiment (factors, designs, replications and the treatment of stochastic output); Railsback and Grimm govern implementation testing, calibration and sensitivity practice for ABMs; Sargent separates verification from empirical validity; JRC requires uncertainty and sensitivity analysis for policy models. None permits generated runs to become observed-world evidence. Calibration data reused as validation must be disclosed and cannot count as independent corroboration.

## Post-freeze source corrections (2026-10-08)

Made in response to the 2026-10-08 control review (`lane_receipts/reviews/2026-10-08-P3-RESEARCH-B.json`). The 2026-08-13 freeze date stays the variant's freeze date.

- **Experiment-design authority added.** The freeze relied on R&G ch. 8 (“Emergence”), whose experiment section §8.3 is a BehaviorSpace tutorial, plus JRC ch. 2, which covers sensitivity. Kleijnen 2015 chs. 2–3 now anchor p09.move.design, p09.move.execute and p09.move.compare. JRC ch. 2 no longer anchors design.
- **R&G anchors narrowed.** Whole-chapter `RG2019:ch8` anchors are now `RG2019:8.3`; other R&G anchors use section numbers checked against the publisher's contents. Chapter 4, already cited by p09.move.implement, is added to the frozen list.
