# NYC Congestion-Pricing MVP Source Freeze

**Packet:** `NYC-CRZ-MVP-v1`

**Frozen:** 2026-08-13

**Decision:** **GO WITH LIMITS** to the first authentic QC Describe plus
schema-constrained extraction slice.

## Fixed policy question

> After the first operating year, which predicted changes and stakeholder
> concerns are corroborated, contradicted, or unresolved by reproducible public
> evidence, and what should decision-makers retain, change, or monitor?

This wording is deliberate. It permits comparison of predictions, public
concerns, and observations without implying that the public time series
identifies a causal effect.

## Scope

- **Policy:** New York City's Congestion Relief Zone tolling program.
- **Intervention date:** January 5, 2025.
- **Primary outcome window:** January 5 through December 31, 2025.
- **Units:** document claims and mitigations; public-hearing speaker turns and
  passages; daily vehicle entries by detection group and vehicle class; daily
  transit counts by mode.
- **Version rule:** any later legal, policy, source-byte, query, schema, or data
  change creates a new packet. It never silently updates `NYC-CRZ-MVP-v1`.

The first evaluation report sometimes uses shorter measure-specific periods.
Every extracted result must therefore carry its actual `coverage_start` and
`coverage_end`; the packet window must not be substituted for missing coverage.

## Frozen corpus

The byte-level manifest is
[`source_manifest.json`](evidence/nyc_crz_mvp_v1/source_manifest.json).

The operational document corpus is intentionally limited to:

1. the 54-page Final EA Executive Summary;
2. the 41-page final FONSI;
3. the 19-page November 2023 Traffic Mobility Review Board report;
4. the two-page adopted phased toll schedule;
5. the 17-page November 2024 Reevaluation 2;
6. the 108-page first evaluation report;
7. all six August 2022 public-hearing transcripts; and
8. the applicable six-page Open NY Terms of Use.

The full multi-volume Final EA is an authoritative expansion source, not part
of the first extraction corpus. A claim requiring detail absent from the
Executive Summary or FONSI must trigger an explicit corpus expansion and a new
manifest entry rather than an untracked lookup. The wider MTA archive, meeting
videos, press coverage, litigation filings, and later monitoring releases are
out of scope for v1.

The PDFs are not redistributed in this repository. Their official URLs,
downloaded-byte sizes, page counts, and SHA-256 digests are frozen. A consumer
must re-download and verify exact bytes before use.

## Frozen quantitative inputs

Two small public-data snapshots are committed under
[`evidence/nyc_crz_mvp_v1`](evidence/nyc_crz_mvp_v1/README.md):

- daily 2025 operating-period CRZ and excluded-roadway entries, aggregated by
  detection group and vehicle class; and
- 2024–2025 daily counts for Subway, Bus, LIRR, Metro-North, Access-A-Ride,
  and Staten Island Railway as contextual transit series.

The exact SoQL, returned CSVs, raw metadata, response headers, shapes,
missingness, and digests are retained. The CRZ data begins on the intervention
date and therefore has no pre-intervention period. The transit series has a
pre-period but is still contextual unless a separately reviewed comparison
design establishes a defensible causal estimand.

The first evaluation report's published baseline is classified as
`agency_derived_counterfactual`. It may be arithmetically audited and compared
with the frozen observations, but it is not independently reconstructable from
the CRZ public dataset alone. StreetLight, HERE, and other proprietary measures
remain `agency_cited_finding`, not executable evidence.

## Method and claim ownership

| Owner | May produce | Must not claim |
| --- | --- | --- |
| Qualitative Coding | Evidence-anchored description of concerns, support, alternatives, affected groups, contradictions, and variation within the six-hearing record | Population prevalence, representativeness, causal effects, or that silence means absence |
| Structured extraction | Validated records for predictions, criteria, mitigations, concerns, and exact anchors | Empirical confirmation, autonomous interpretation authority, or invented missing fields |
| Quantitative analysis | Reproducible descriptive aggregation and predicted-versus-observed arithmetic audit | A causal effect, unique vehicles, revenue, or independent reproduction of proprietary/agency counterfactuals |
| Policy appraisal | Criteria- and values-explicit comparison of what to retain, change, or monitor | A value-free optimum or a recommendation unsupported by its typed inputs |
| Process Tracing | Nothing in the first vertical | Generic chronology relabeled as causal-mechanism testing |

Process Tracing remains deferred unless a later, separately reviewed question
identifies rival mechanisms and discriminating within-case evidence.

## Evidence and anchor rules

Every document-derived record must include:

- packet and artifact identifiers;
- verified source digest;
- PDF page index and printed page label where present;
- speaker/section/table identity;
- line or passage bounds recoverable from the exact bytes;
- assertion source: agency, hearing participant, analyst, computation, or
  reviewer; and
- derivation and review state.

The transcript PDFs preserve printed line numbers and speaker turns. Locator
viability was checked across all six files by recovering the first public
speaker self-identification at PDF pages 66, 55, 82, 68, 55, and 60,
respectively. Those names need not appear in the product UI. Default output
should describe and anchor the public record while minimizing repetition of
personal names and quotations.

## Source-use disposition

- The MTA and FHWA records are official public sources, but the PDFs are linked
  and hash-verified rather than republished.
- The Open NY terms welcome download and use subject to their conditions; the
  two dataset metadata records contain no separate license value. Cite MTA and
  retain the exact terms digest. External redistribution beyond the committed
  non-personal aggregate snapshots requires a fresh terms check.
- Hearing speakers participated in a public, recorded proceeding, but public
  availability is not a reason to maximize personal quotation. Preserve exact
  internal anchors, minimize exposed names/quotes, and require human review
  before publication.

## Refusal and invalidation rules

- Source hash, query, schema, or content drift → reject and re-freeze.
- Missing or unreadable transcript pages → mark the hearing corpus incomplete.
- Missing privacy/publication disposition → metadata or aggregate summary only;
  no personal quotation.
- No adequate pre-period or comparison design → refuse causal attribution.
- Agency baseline not independently reconstructable → label it
  `agency_derived_counterfactual`.
- Proprietary measure → exclude it from executable quantitative evidence.
- Method disagreement → preserve it; do not force consensus.
- A later policy or legal change → create a new packet version; do not rewrite
  this historical observation window.

## Gate evidence

The freeze passes the bounded source gate because:

- all 13 external PDFs resolved as valid documents and have exact byte counts,
  page counts, and SHA-256 digests;
- speaker-turn/page/line locators are recoverable across all six transcripts;
- both data queries returned deterministic ordered tables with frozen metadata,
  response headers, shapes, missingness, and digests;
- direct recomputation over the frozen vehicle table produced stable receipt
  totals recorded in its README;
- the source types and permitted claims visibly separate observed data,
  extracted claims, agency-derived counterfactuals, normative judgments, and
  unavailable evidence; and
- mutation is handled as invalidation, not silent refresh.

This is a source and claim-boundary gate, not an empirical result. A human must
still review the first extracted prediction, first hearing concern, and first
quantitative comparison before the Workbench presents them as accepted.

## First post-freeze vertical

Build one visible, reviewable slice in the existing Investigation Spine:

1. verify exact source bytes;
2. extract one pre-implementation prediction and one hearing-record concern
   into schema-validated, anchor-bearing candidate records;
3. review those records rather than silently accepting model output;
4. load one frozen daily aggregate table;
5. show the prediction, concern, observation, provenance, and permitted claim
   together; and
6. refuse causal or recommendation language the evidence cannot support.

The two local seam candidates are a document-extraction request/result over
exact bytes plus evidence anchors, and a frozen-tabular-query receipt. They are
Workbench-local experiments, not adopted shared schemas. Promotion remains
conditional on a second authentic compatible producer/consumer seam.

Do not start with all outcomes, the entire MTA archive, a Process Tracing run,
an LLM-generated conclusion, a universal schema, producer changes, or a new
interface.
