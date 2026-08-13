# Phase 2b method portfolio proposal

Status: inclusion criteria frozen; candidate application pending human review

Portfolio proposal version: `phase2b-proposal-0.1`

## Decision boundary

This document will propose the denominator for Phase 3 decomposition and the
four later coverage measures in §11 of
`METHOD_DECOMPOSITION_HANDOFF.md` rev 5.1. It is a research proposal, not an
adopted portfolio. It does not begin Phase 3, run collisions, promote a
capability, adopt a production schema, change product code, or recommend shared
infrastructure.

The approved discovery format remains method phase → analytical move →
execution action. A portfolio decision selects named method variants to study;
it does not make their similarly named moves equivalent.

## Candidate sources and source limits

Candidate names will be generated from two independent classification
surfaces before individual methodology sources are frozen:

1. The repository's 73-label, 13-category
   [RAND-derived policy-research inventory](../../reference/RAND_POLICY_METHODS_TAXONOMY.md).
   Its provenance is a pinned historical project file whose underlying email
   is not preserved. It is therefore a discovery vocabulary, **not an official
   RAND taxonomy or methodological authority**. Official RAND method
   publications will be used separately where relevant.
2. HM Treasury's 2026
   [Magenta Book Annex A](https://www.gov.uk/government/publications/the-magenta-book/magenta-book-annex-a-analytical-methods-for-use-within-an-evaluation-html),
   which classifies theory-based, experimental and quasi-experimental,
   value-for-money, evidence-synthesis, and generic research methods used in
   government evaluation.

The [UK Government Futures Toolkit](https://www.gov.uk/government/publications/futures-toolkit-for-policy-makers-and-analysts/the-futures-toolkit-html),
the [U.S. GAO guide to designing evaluations](https://www.gao.gov/products/gao-12-208g),
and the [NIH mixed-methods guide](https://obssr.od.nih.gov/research-resources/mixed-methods-research)
will be used as supplementary established classifications where the two seed
lists are thin. No catalog label will be treated as a sufficiently specified
method variant.

## Predeclared inclusion criteria

These criteria are frozen before the candidate list is scored. A later change
must be dated, justified, and applied again to every candidate rather than used
to rescue a favored method.

### Candidate-level gates

A candidate is eligible only if it passes all five gates:

1. **Catalog traceability.** A label or explicit synonym appears in at least
   one named classification above. The proposal records the exact label and
   any split, merge, or normalization.
2. **Distinct inferential leverage.** The frozen variant supports a conclusion
   that no already-selected variant supports under the same warrant. Merely
   using different software, data, or vocabulary does not count.
3. **Methodological source sufficiency.** At least one primary method source,
   consensus standard, or authoritative government methodology guide is
   available for Phase 3. A detector vocabulary, product documentation, or
   example application alone is insufficient.
4. **Real-policy prevalence proxy.** The method is either named by two
   independent established classifications/guides, or one cross-government
   guide describes its policy use and an independent method authority defines
   its conduct. This is a checkable proxy, not an invented frequency estimate.
5. **Decomposable frozen variant.** Population or case scope, evidence object,
   target conclusion, decisive design choices, and important exclusions can be
   stated now. A broad umbrella such as “machine learning,” “evaluation,” or
   “participatory methods” fails until split into a method variant.

### Portfolio-level balance tests

The eligible set is then minimized while satisfying all four tests:

1. **Evidence-form spread.** The portfolio must include methods whose central
   inputs or outputs exercise observed, reported, interpreted, derived,
   elicited, and simulated information. These origins describe provenance,
   not an evidence-strength ladder.
2. **Decision-role spread.** Collectively the methods must exercise population
   description or measurement, causal-effect estimation, mechanism or
   configurational explanation, prediction, evidence synthesis, option
   appraisal, uncertainty/foresight, and mixed-methods meta-inference.
3. **Family balance.** The portfolio must cover the following predeclared
   families: evidence synthesis; experimental causal estimation;
   quasi-experimental causal estimation; theory-based within-case or
   configurational inference; qualitative interpretation/theory construction;
   population measurement; computational text measurement; forecasting;
   simulation; decision under deep uncertainty/foresight; option appraisal;
   structured expert elicitation; and mixed-methods integration. Normally one
   variant represents a family. A second is allowed only when its inferential
   leverage is demonstrably non-substitutable.
4. **Implementation neutrality.** Existing repository support gives a candidate
   zero inclusion credit, and missing implementation gives it zero penalty.
   Selection happens before code mapping. This prevents the §11 denominator
   from being weighted toward workflows already built.

### Stop rule

Choose the smallest eligible set that covers every predeclared family and
decision role. Do not add a second near-duplicate merely to increase likely
reuse, and do not remove a hard-to-automate method to improve future coverage.

## Candidate application

Pending. The next revision will apply the frozen criteria, list exclusions,
show the expected direction of every §11 denominator effect, and present one
recommended portfolio plus one important alternative for human approval.
