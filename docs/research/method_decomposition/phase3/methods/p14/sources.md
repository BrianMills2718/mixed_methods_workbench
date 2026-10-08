# P14 frozen sources

Frozen before decomposition on 2026-08-13.

## Primary methodological authority

Bennett A and Checkel JT, editors. *Process Tracing: From Metaphor to Analytic
Tool*. Cambridge University Press, 2015 (online publication 2014), DOI
10.1017/CBO9781139858472. [Official publisher record](https://www.cambridge.org/core/books/process-tracing/5BBC24CBF2E89114817741D0476C07A9).

Pinned sections: chapter 1, Bennett and Checkel, "Process tracing: from
philosophical roots to best practices" (pp. 3–37), for theory testing versus
inductive theory development, causal mechanisms, alternative explanations,
diagnostic evidence and Bayesian logic; chapter 10, Checkel and Bennett,
"Beyond metaphors: standards, theory, and the 'where next' for process
tracing" (pp. 260–275), for the concluding standards cited by
`p14.move.conclude`;
the concluding appendix “Disciplining our conjectures” for best-practice
checks. The volume defines Process Tracing as analysis of process, sequence,
and conjuncture evidence within a case for developing or testing hypotheses
about causal mechanisms.

## Corroborating inferential authority

Fairfield T and Charman A. “Explicit Bayesian Analysis for Process Tracing:
Guidelines, Opportunities, and Caveats.” *Political Analysis* 25(3), 2017,
363–380. [Author manuscript in the LSE repository](https://researchonline.lse.ac.uk/id/eprint/69203/2/Fairfield_Explicit%20bayesian%20analysis_author_2017%20LSERO.pdf).
Pinned sections 2–6 and appendices for priors, likelihood ratios, dependence,
sensitivity, and transparent updating. The qualitative-Bayesian variant uses
explicit comparative likelihood judgments and sensitivity; it does not claim
false numerical precision.

## Source-limit note

The workbench topology merged at `1fd01bc` may later inform execution mapping,
but it was excluded from the source freeze. Silence is diagnostic only after a
documented evidence opportunity was actually searched, and dependent evidence
must not be multiplied as if independent.

## Exact-anchor registry

`p14.bc.ch1` resolves to Bennett and Checkel chapter 1 (pp. 3–37);
`.appendix` resolves to the volume appendix “Disciplining our conjectures”;
and `.conclusion` resolves to chapter 10, "Beyond metaphors: standards,
theory, and the 'where next' for process tracing" (pp. 260–275), now inside
the frozen range. Chapter 1 and chapter 10 titles and page ranges were
confirmed on 2026-10-08 from PRIO's publication records
(https://www.prio.org/publications/7598, https://www.prio.org/publications/7600).
The appendix title was not independently re-confirmed in that check. In Fairfield and
Charman 2017, `p14.fc.sections2_3`, `.sections2_4`, `.sections2_5`,
`.sections3_6`, and `.sections4_6` resolve to the indicated inclusive numbered
sections; `.section6` resolves to §6. These are locators in the linked author
manuscript. Priors and hypothesis-conditioned dependence are modeled explicitly
rather than inferred from a generic evidence grouping.

Machine-resolvable IDs: `source:p14.bc.ch1`, `source:p14.bc.appendix`,
`source:p14.bc.conclusion`, `source:p14.fc.sections2_3`,
`source:p14.fc.sections2_4`, `source:p14.fc.sections2_5`,
`source:p14.fc.sections3_6`, `source:p14.fc.sections4_6`, and
`source:p14.fc.section6`.

## Type extension note

`analysis_plan` is a type extension added because no existing type fits the
registered evidence-search plan of a single-case Process Tracing study.
`review_protocol` is a systematic-review protocol whose search and screening
warrant this method must not inherit (p14.u04). `design_parameters` holds
numeric settings. `search_query` names one query, whereas this plan registers,
before any result is seen, each evidence opportunity's expected location,
access condition and the condition under which silence would count as absence.
Its downstream use is to let `p14.move.search` and gate `p14.c18` separate
searched silence from unsearched space, which none of those types states.
