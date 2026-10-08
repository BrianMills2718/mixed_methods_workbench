# P06 frozen sources

Frozen 2026-08-13, before the P06 records were authored. Post-freeze corrections dated 2026-10-08 are listed at the end; the frozen variant did not change.

Primary: U.S. Office of Management and Budget, *Standards and Guidelines for Statistical Surveys* (September 2006), Standards 1.1–1.4 (survey planning, survey design, survey response rates, pretesting survey systems), 2.1–2.3 (developing sampling frames, required notifications, data collection methodology), 3.1–3.5 (data editing, nonresponse analysis and response rate calculation, coding, data protection, evaluation), 4.1 (developing estimates and projections), 5.1–5.2 (analysis and report planning, inference and comparisons), 6.1 (review of information products), and 7.1–7.3 (releasing information, data protection and disclosure avoidance for dissemination, survey documentation). [Archived official PDF](https://obamawhitehouse.archives.gov/sites/default/files/omb/inforeg/statpolicy/standards_stat_surveys.pdf)

Corroborating conduct authority: Robert M. Groves et al., *Survey Methodology*, 2nd ed. (Wiley, 2009), chapters 2 (inference and error), 3 (target populations, sampling frames, coverage error), 4 (sample design and sampling error), 5 (methods of data collection), 6 (nonresponse; §6.6 design features to reduce unit nonresponse), 7 (questions and answers), 8 (evaluating survey questions; §8.5 field pretests), and 10 (postcollection processing; §10.2 coding, §10.4 editing, §10.5 weighting, §10.7 sampling variance estimation for complex samples, §10.8 documentation and metadata). [Publisher record](https://www.wiley.com/en-us/Survey+Methodology%2C+2nd+Edition-p-9780470465462) · [publisher table of contents (PDF)](https://media.wiley.com/product_data/excerpt/68/04704654/0470465468-1.pdf)

The OMB standard requires a survey plan, explicit concepts and target population, probability-based design or statistical justification, design for high response rates, pretesting, response/nonresponse analysis, documented estimation and error estimates, review, and release documentation. Groves et al. corroborate that sampling, coverage, nonresponse, measurement, and processing errors are distinct; a narrow confidence interval does not erase nonsampling error.

Boundary: these sources license population measurement under a declared frame and error model. They do not license causal claims, inference to frame-excluded units, or treating weights as a cure for unknown nonresponse or measurement bias.

## Post-freeze source corrections (2026-10-08)

Made in response to the 2026-10-08 control review (`lane_receipts/reviews/2026-10-08-P3-RESEARCH-B.json`). The 2026-08-13 freeze date stays the variant's freeze date.

- **OMB section scope.** The freeze said "§§1.1–1.4 … §§4.1–5.3 (estimation, inference, review, release, documentation)". OMB 4.2, 4.3, 4.4 and 5.3 do not exist; the PDF's contents list 4.1, 5.1–5.2, 6.1 and 7.1–7.4. The frozen scope is now §§1.1–7.3, with review = 6.1 and release/documentation = 7.1–7.3. Records re-anchored: estimate [OMB 4.1, 5.2]; compute_variance [OMB 4.1]; report [OMB 5.1, 6.1, 7.1, 7.2, 7.3]; OMB 1.3 added to design and collect; OMB 3.4 added to process (it handles protected microdata).
- **Groves chapter scope.** The freeze cited ch. 5 for sampling; the publisher's contents put sample design in ch. 4. Chapters 4 and 8 are added; select is re-anchored to ch. 4, pretest to §8.5, and weighting, variance and documentation to §§10.5, 10.7 and 10.8.
