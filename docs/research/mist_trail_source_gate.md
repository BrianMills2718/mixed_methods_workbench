# Mist Trail Flagship Source Gate

**Checked:** 2026-08-13
**Decision:** **Do not use Mist Trail as the sole first cohesive MVP case.**
Retain it as a bounded, source-grounded **pre-decision option-appraisal case**.

## Why this gate exists

The proposed MVP must demonstrate one understandable policy investigation in
which real analytical methods operate on real evidence and their outputs join
without losing provenance, disagreement, uncertainty, or method-specific
meaning. A polished, manually authored decision fixture is not enough.

The gate therefore asks whether the currently public Mist Trail record can
support all of the following:

1. source-grounded qualitative description;
2. structured extraction of options, consequences, criteria, and concerns;
3. a quantitative or computational analysis that can materially affect the
   conclusion;
4. a defensible option appraisal;
5. a completed decision or outcome against which later claims can be checked.

Mist Trail currently supports items 1, 2, and a bounded version of 4. It does
not yet support 3 or 5.

## What the public record actually contains

### Core official sources

| ID | Official source | Observed content | Custody observation |
| --- | --- | --- | --- |
| `MT-S1` | [NPS project page](https://www.nps.gov/yose/getinvolved/misttrailcorridor.htm) | Current project status, planning chronology, purpose, visitation and safety framing, meeting links | Mutable webpage; status checked 2026-08-13 |
| `MT-S2` | [NPS PEPC EA record](https://parkplanning.nps.gov/document.cfm?documentID=150212&parkID=347&projectID=105979) | Three official alternatives, preferred alternative, June 11–July 13, 2026 comment period, EA and appendices links | Mutable record; comment period was closed when checked |
| `MT-S3` | [May 2026 Environmental Assessment PDF](https://parkplanning.nps.gov/showFile.cfm?sfid=849738&projectID=105979) | Purpose and need, Alternatives A–C, NPS proposed action, affected environment, qualitative consequence analysis, consultation history | 4,495,269 bytes; SHA-256 `df5304a9116b9dc2093e1f5e2eee61b61adab3c6f65ac8214aca7e685c23cbb0` |
| `MT-S4` | [EA appendices PDF](https://parkplanning.nps.gov/showFile.cfm?sfid=849737&projectID=105979) | Operations analysis, dismissed alternatives, designs, mitigations, references, biological and cultural analyses, and the 2024 civic-engagement comment summary | 23,144,028 bytes; SHA-256 `cd67c0fc42f3598139d7b1cb4e54179fde9c88d12ad8ffe92dd7fbce825d0212` |

The two PDF hashes were recomputed from fresh downloads on 2026-08-13. The EA
digest matches the digest already recorded in the existing fixture.

### Evidence that is more useful than the existing fixture indicates

The appendices are analytically important and should not be treated as merely
illustrative attachments:

- Appendix C compares effects on park operations. It identifies expected
  capital, maintenance, staffing, emergency-access, snow-management, waste,
  shuttle, and search-and-rescue consequences, although it does not provide
  comparable dollar amounts.
- Appendix M reports the NPS analysis of the 2024 civic-engagement record: 205
  pieces of correspondence, 1,386 identified comments, 26 codes, code-level
  frequencies, and concern statements.
- Alternative B includes an adaptive-management pilot for the Stock Trail.
  The EA names four evaluation areas—visitor safety, visitor use,
  stock/human conflict, and other operational conflict—but says the actual
  metrics would be established before implementation.
- The EA reports a 2025 park-wide total of 239 search-and-rescue incidents, 69
  of them in the corridor, and 4,661 incidents with 58 unintentional deaths
  from 2001 through 2025.

These materials are sufficient for a real extraction and appraisal workflow;
the current hand-authored fixture understates the available source packet.

## Material limitations

### 1. The policy decision is not complete

The May 2026 EA identifies Alternative C as the NPS proposed action, but the
official document list contained no final EA, finding of no significant impact,
or other final decision record when checked. The NPS project page anticipated a
decision later in 2026.

Therefore the case cannot yet support:

- analysis of the actual final choice;
- process tracing of a completed decision;
- implementation or outcome evaluation; or
- comparison of predicted and observed consequences.

### 2. The underlying public comments are not public in the reviewed packet

Appendix M is an agency-produced analysis of the 2024 submissions. It does not
contain the 205 original submissions or the 1,386 comment segments. The
official document list also did not expose a corpus or summary of comments
submitted on the 2026 EA.

QC could truthfully analyze Appendix M as a secondary source. It could not
truthfully present a new coding of the public's original submissions without
obtaining those submissions.

### 3. The quantitative evidence is descriptive, not a runnable decision model

The public packet supplies useful counts and qualitative consequence
assessments, but it does not supply:

- a site-level visitor-use time series or microdata;
- incident-level safety data;
- comparable capital, staffing, and lifecycle costs;
- measured effects of the proposed interventions; or
- completed pilot or implementation observations.

The counts can describe scale and establish baselines. They are not currently
enough for a non-substitutable forecast, causal estimate, cost-benefit analysis,
or calibrated simulation that could change the recommendation.

### 4. One official quantity is internally inconsistent

The EA describes approximately 85,000 visitors **per summer month** from 2010
through 2025. Appendix M describes approximately 85,000 visitors **annually**.
The project and planning webpages use less precise “each summer” wording. A
future analysis must preserve this discrepancy and seek the underlying visitor
count source; it must not silently harmonize the figures.

### 5. Many consequence claims are professional judgments

The EA says its visitor and operations analyses combine available data,
technical expertise, staff information, public comments, professional
judgment, and experience with similar projects. Those are valid planning
inputs, but they are not observed causal effects. The product must keep that
epistemic status visible.

## Capability decision

| Product capability | Gate result | What Mist Trail can honestly demonstrate now |
| --- | --- | --- |
| Describe the problem and affected interests | **Pass** | Source-grounded description of safety, circulation, visitor services, stewardship, operational, cultural, and environmental concerns |
| Extract structured policy information | **Pass** | Alternatives, actions, consequences, mitigations, criteria, affected interests, uncertainties, and evidence gaps from the EA and appendices |
| Analyze stakeholder views | **Partial** | Analyze NPS's published summary and frequency tables, not the underlying submissions or current 2026 comments |
| Quantitative/computational strand | **Fail for MVP** | Descriptive counts only; no current analysis with distinct quantitative leverage over the choice |
| Option appraisal | **Pass with limits** | Conditional, reviewer-authored comparison under explicit priorities; not a CBA, agency decision, or empirically validated ranking |
| Process tracing | **Not yet** | The planning chronology can be described, but the final decision and sufficient internal/contemporaneous decision evidence are unavailable |
| Intervention/outcome evaluation | **Not yet** | The Stock Trail pilot creates a future evaluation opportunity; no intervention result exists now |

## Permitted bounded case

Mist Trail remains valuable if it is framed explicitly as:

> What do the May 2026 EA and appendices establish about the relative merits,
> burdens, stakeholder concerns, and uncertainties of Alternatives A–C, and
> what missing evidence prevents a fully defensible recommendation?

The corresponding workflow may perform:

1. exact-source ingestion and anchoring;
2. structured extraction of alternatives and consequence claims;
3. qualitative description of the published concern statements;
4. descriptive use of the published count tables;
5. transparent separation of empirical assessments from reviewer priorities;
6. conditional option appraisal and refusal where evidence is insufficient;
7. a ranked evidence-acquisition and future monitoring plan.

It must not claim that it coded the original public submissions, estimated
policy effects, conducted a cost-benefit analysis, reconstructed a completed
decision process, or evaluated an implemented policy.

## Consequences for the current fixture

No fixture or code is changed by this gate. If the bounded case is refreshed
later:

- add the appendices PDF and its digest to the source manifest;
- replace “appendix absent” implications with the narrower truth that numeric
  comparative costs remain absent;
- anchor every displayed consequence and concern statement to hash-matching
  bytes;
- distinguish NPS comment-analysis outputs from raw public comments;
- preserve the 85,000-visitor discrepancy as an unresolved source conflict;
- keep the hand-authored appraisal classified as human judgment rather than
  software-executed analysis; and
- recheck the official record for a final decision and 2026 comment analysis
  before every public demonstration.

## MVP routing decision

Mist Trail fails the gate **as the sole flagship for the complete MVP** because
it cannot currently exercise the required non-substitutable quantitative strand
or a completed decision/outcome boundary.

It passes as a useful secondary vertical for source-grounded option appraisal
and for testing structured extraction against a complex real public record.

The next flagship search should prefer a completed policy decision with:

1. exact, publicly reusable primary documents and a stable decision chronology;
2. raw or directly analyzable stakeholder text;
3. quantitative data sufficient for a computation that can alter the
   conclusion;
4. explicit alternatives, criteria, trade-offs, and a recorded decision;
5. at least one observable implementation or outcome; and
6. enough evidence to exercise two method-owned engines without fabricating a
   seam.

Until such a case is selected, do not build the MVP around Mist Trail merely
because its current page is polished.
