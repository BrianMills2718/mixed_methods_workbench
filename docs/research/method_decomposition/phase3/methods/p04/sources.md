# P04 frozen sources

Frozen before decomposition on 2026-08-13.

## Primary conduct authority

Schneider CQ and Wagemann C. *Set-Theoretic Methods for the Social Sciences: A
Guide to Qualitative Comparative Analysis*. Cambridge University Press, 2012.
[Official publisher contents](https://www.cambridge.org/core/books/settheoretic-methods-for-the-social-sciences/236C162386C1188966FE269D625CA289).

Pinned chapters, with titles as listed in the book's contents: Part I
"Set-Theoretic Methods: The Basics": 1 (Sets, set membership, and
calibration), 2 (Notions and operations in set theory), 3 (Set relations), 4
(Truth tables); Part II "Neat Formal Logic Meets Noisy Social Science Data": 5
(Parameters of fit), 6 (Limited diversity and logical remainders), 7 (The
truth table algorithm); Part III "Potential Pitfalls and Suggestions for
Solutions": 8 (Potential pitfalls in the standard analysis procedure and
suggestions for improvement, the source of Enhanced Standard Analysis and the
bar on untenable remainder assumptions), and 9 (Potential pitfalls in the
analysis of necessity and sufficiency and suggestions for avoiding them,
pp. 220–250).

Verification, 2026-10-08: chapters 1–8 and their part titles come from a
bookseller contents listing (Thalia, https://www.thalia.de/shop/home/artikeldetails/A1022828291) returned by web
search; chapter 9's title and pages come from its Cambridge Core chapter page
(https://www.cambridge.org/core/books/settheoretic-methods-for-the-social-sciences/potential-pitfalls-in-the-analysis-of-necessity-and-sufficiency-and-suggestions-for-avoiding-them/BB079153A6DEEDCD5FEA0A6777588FB8).
The Cambridge contents page itself returned HTTP 403. A published review
states the book has 12 chapters in four parts, and the closing chapter is
"Looking back: looking ahead"; the numbers and titles of chapters 10 and 11
could not be confirmed, so no record cites chapters 10–12 (p04.u05). The
earlier labels "8–9 necessity and sufficiency analysis" and "11 good
practice" were wrong and are withdrawn.

## Corroborating methodological authority

Ragin CC. *Redesigning Social Inquiry: Fuzzy Sets and Beyond*. University of
Chicago Press, 2008. [Official publisher page](https://press.uchicago.edu/ucp/books/book/chicago/R/bo5973952.html).
Pinned chapters: 1–3 (asymmetric set relations, consistency, coverage), 4–5
(substantive calibration), 6–7 (configurations and truth tables), and 8–9
(limited diversity and counterfactual cases).

## Source-limit note

The freeze is one fsQCA variant. It preserves substantive case knowledge and
does not treat necessity, sufficiency, correlation, mechanism, and marginal
effect as interchangeable warrants.

## Exact-anchor registry

`p04.sw.ch1`, `.ch3`, `.ch4`, `.ch5`, `.ch6`, `.ch7`, `.ch8`, and `.ch9`
resolve to the identically numbered chapters of Schneider and Wagemann 2012
listed above (`.ch11` is withdrawn);
compound tokens such as `.ch5_7` and `.ch6_7` resolve to those inclusive chapter
ranges. `p04.ragin.ch1`, `.ch1_2`, `.ch4_5`, `.ch5`, `.ch7_9`, and `.ch8_9`
resolve to the named chapters or inclusive ranges in Ragin 2008. No record now
cites Ragin chapter 10, which lies outside the frozen conduct range.

Machine-resolvable IDs: `source:p04.sw.ch1`, `source:p04.sw.ch3`, `source:p04.sw.ch4`,
`source:p04.sw.ch5`, `source:p04.sw.ch5_7`, `source:p04.sw.ch6`,
`source:p04.sw.ch6_7`, `source:p04.sw.ch7`, `source:p04.sw.ch8`,
`source:p04.sw.ch9`, `source:p04.ragin.ch1`,
`source:p04.ragin.ch1_2`, `source:p04.ragin.ch4_5`,
`source:p04.ragin.ch5`, `source:p04.ragin.ch7_9`, and
`source:p04.ragin.ch8_9`.

## Type extension note

`analysis_plan` is a type extension added because no existing type fits the
fsQCA calibration plan or remainder policy. `review_protocol` is an
evidence-synthesis protocol. `design_parameters` holds numeric settings, and
`parameter_set` already carries the frequency and consistency thresholds; the
calibration plan and remainder policy are instead substantive commitments
(external membership anchors with their conceptual justification;
directional expectations and which counterfactuals are easy, difficult or
untenable) that the minimization and calibration actions must obey but cannot
choose. Their downstream use is to make software defaults detectable as
unlicensed (p04.c20), which neither existing type states.
