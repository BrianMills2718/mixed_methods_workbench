# NYC-INTEGRATE-1 — accepted qualitative integration

Date: 2026-10-02

## Inputs

NYC-INTEGRATE-1 consumes three already bounded strands:

- the accepted NYC extraction/source-custody baseline;
- the reproducible quantitative audit, whose causal status remains `not_identified`;
- the human-approved NYC-QC-1 review from Qualitative Coding revision
  `5560ce71546a30dc6aa4a264dacbce3028b005eb`.

The qualitative handoff is pinned at SHA-256
`d3b02dcb4e7ce9e3ec8b9d06489ced3e444c425a2099bc5b287e503f4092f3cc`.
The approved analyst review is pinned at SHA-256
`76e8271a8645336bcf8fde730c3043304a9ab9f92085fefe21b796c1cbeb51ea`.

Workbench does not import Qualitative Coding internals. It consumes the pinned typed artifacts through a narrow compatible projection.

## Integrated result

The existing NYC API and investigation page now expose the accepted qualitative result alongside the quantitative audit and extraction baseline.

The qualitative projection preserves:

- 12 human-approved substantive findings;
- one approved boundary case;
- one approved unresolved/insufficient-evidence negative-case-search result;
- exact evidence-anchor identities and source coordinates;
- the six-hearing corpus boundary;
- the explicit no-prevalence, non-representativeness, and noncausal limits.

The Workbench adds four explicit cross-strand dispositions:

- **convergence** — the agency prediction and descriptive first-year comparison move in the same reduction direction; some hearing passages also discuss potential traffic/emissions benefits;
- **complementarity** — hearing evidence adds burden, transit-alternative, transparency, exemption, toll-cap, and implementation concerns that traffic arithmetic does not measure;
- **divergence** — the descriptive comparison is about 11.39% below the agency baseline, smaller than the 13.4% prediction;
- **silence** — neither strand establishes net policy benefit; quantitative arithmetic is silent on lived burdens and qualitative hearings do not identify causal traffic effects or population prevalence.

No scalar cross-method confidence score is created.

## Baseline versus federated

The capable baseline could reconstruct the agency prediction, compare it descriptively with frozen observed entry events, and retain one accepted medical-access concern. It could not provide a genuine six-hearing qualitative account.

The federated result improves:

- reconstruction and exact source traceability;
- preservation of native method semantics;
- visibility of human review standing;
- preservation of variation, a boundary case, and an unresolved state;
- revision readiness through exact producer revisions and artifact hashes.

It does **not** improve:

- underlying evidence quality;
- causal identification;
- population representativeness or prevalence;
- policy value judgments or priority weights.

This real consumer did not require a universal analytical IR, universal O→A ontology, new revision engine, or generic warrant calculus.

## Appraisal boundary

Policy appraisal remains `needs_human_priorities`.

The evidence package does not contain accepted human-owned weights or priority judgments sufficient to choose among retain/change/monitor. Workbench therefore does not manufacture a recommendation.

## Verification

Focused NYC verification after integration:

- `tests/test_nyc_crz_integrated.py`: 5 passed;
- existing NYC extraction and quantitative suites: 17 passed;
- combined focused result: 22 passed;
- `git diff --check`: passed;
- full repository run reached 159 passing tests but 21 guarded-decision tests refused because this checkout imports `data_contracts` from site-packages rather than an editable Git checkout; those tests require a verifiable tracked Data Contracts revision and are outside NYC-INTEGRATE-1.

NYC-INTEGRATE-1 is ready for completion review. NYC-MVP-REVIEW-1 remains unaccepted.
