# Lane A Research: First Case and Source-Governance Options

Date: 2026-07-12
Status: research report only; no case, source use, or implementation is authorized
Access date for every external source below: 2026-07-12

## 1. Executive finding

**Recommended default:** use the U.S. Department of State's *Foreign Relations
of the United States, 1961–1963, Volume XI, Cuban Missile Crisis and Aftermath*
(`frus1961-63v11`) as the first governed public case, with claims explicitly
bounded to **U.S. policy decision-making and recorded diplomatic exchange**.
Treat all 390 canonical document records (`d1`–`d390`) as the source universe;
the GOV packet must freeze an exact, reviewable analytic subcorpus before any
producer run. This is a recommendation for Brian's decision, not approval.

The proposed 18 Brumaire case remains methodologically attractive, but the
**current packet is not governable as a redistributable research corpus**. It is
a 3,477-word manual paraphrase/excerpt synthesis, not a declared denominator of
source objects. Five of the six source records are not ready for governed reuse:
A, D, and E are blocked or unknown; B and C must be reacquired from the
public-domain 1904 Anderson edition because the selected host expressly
prohibits redistribution and adaptation. Only the Bourrienne record has both a
source-specific public-domain statement and a usable canonical acquisition
route. The packet also lacks edition/translation identifiers,
retrieval times, source-object hashes, excerpt-to-source maps, and item-level
rights decisions. The current packet must not pass GOV.

The evidence changes the trade-off behind the original Brumaire proposal.
Brumaire maximizes reuse of existing process-tracing work, but FRUS provides a
materially stronger first governance substrate: an official source universe,
public-domain/CC0 master files, version history, TEI P5 structure, and canonical
volume/document identifiers. FRUS is still not a neutral or complete account of
the crisis. Its editors explicitly selected a U.S.-policy record, omitted much
intelligence and allied consultation, published additional material elsewhere,
and did not have the volume individually reviewed by the Advisory Committee.
Those are claim limits, not reasons to discard the corpus.

**Confidence:** high that the current Brumaire packet fails the minimum GOV
gate; high that FRUS is the strongest governance default among the candidates
audited; medium that FRUS will be the best *methodological* first case until an
exact analytic subcorpus, rival hypotheses, and reviewer burden are piloted.

**Narrow decision requested from Brian:** choose one of these dispositions:

1. **Select `GOV-FRUS-CMC` as the first case (recommended):** authorize a later,
   separately named governance-only slice to freeze and review the FRUS source
   bundle. This does not authorize QC, PT, or workbench implementation.
2. **Retain Brumaire conditionally:** require a new rights-clean packet built
   from pinned public-domain editions or explicit permissions; do not reuse the
   current packet as the governed corpus. If the direct-source and rights gaps
   remain, switch to FRUS.

No evidence supports approving the current Brumaire packet as-is.

## 2. Search and provenance method

### Scope and competing hypotheses

The research tested three propositions:

- **H1 — Brumaire is implementation-ready after a light governance review.**
- **H2 — Brumaire remains viable only after a rights-clean source rebuild.**
- **H3 — another public case offers a better first governance substrate even
  after accounting for lost producer reuse.**

Evidence criteria were the lane requirements in
`.claude/tasks/decision_research_context.md`: an exact corpus denominator,
work/edition/translation/host separation, documented processing and publication
basis, sensitivity review, deterministic anchors, source diversity for QC and
PT, known absences, practical burden, and replaceability.

### Collection

The audit used:

- the tracked Brumaire source packet, manifest, research design, and producer
  evidence in `~/projects/process_tracing`;
- each current source page plus the host's rights or permission page where one
  was available;
- publication metadata for the Anderson and Bourrienne editions;
- current U.S. Copyright Office guidance for pre-1931 U.S. publications;
- the State Department's FRUS volume, preface, source note, official series
  description, public Git repository, license, release history, and sample
  canonical document pages;
- the NASA Rogers Commission corpus as a secondary public alternative and a
  check against the false inference that government hosting automatically
  makes every included item public domain; and
- FAIR, CARE, and BagIt sources for the minimal governance packet.

All external facts are tied to direct URLs in section 8. Local deterministic
observations were made with `wc`, `sha256sum`, `rg`, and read-only file review.
`git ls-remote` observed the FRUS repository's `master`/HEAD at
`23c6cc0cbe5e65ba8d87e4f994fe66a52c40f5e6`; this is a freshness observation,
not the approved bundle version. The latest visible release was `v1.0.18`
(2026-03-13, release commit shown as `9513d96`).

### Stopping rule

Research stopped when:

1. every current Brumaire source had an item-level rights/readiness
   disposition;
2. the current packet's denominator and anchor properties were directly
   inspected;
3. at least one alternative had an authoritative rights basis, exact source
   universe, stable identifiers, and credible QC/PT roles; and
4. the remaining uncertainty was a bounded human choice rather than a missing
   factual lookup.

This was not a legal opinion, an exhaustive archive search, a complete
historiographical review, or an empirical producer evaluation.

## 3. Candidate comparison

### Overall comparison matrix

| Criterion | Current 18 Brumaire packet | Rights-clean Brumaire rebuild | FRUS Cuban Missile Crisis volume | Rogers Commission / Challenger packet |
|---|---|---|---|---|
| Candidate question | Why did the French Revolution culminate in the 1799 coup/Consulate? Current wording is broader than the focal source window. | Prefer: why did a civilian constitutional-revision effort culminate in a Bonaparte-centered Consulate rather than voluntary revision or failed coup? | Prefer: how and why did U.S. decision-making converge on quarantine plus negotiated removal rather than immediate strike/invasion or passive acceptance? | Why was STS-51L launched despite cold-weather O-ring concerns and contrary engineering signals? |
| QC contribution | Can discover legitimation frames, actor roles, uncertainty, and differences among public, legal, memoir, and historiographical genres, but only in a manually synthesized derivative. | Can analyze genre-specific frames and patterns in traceable primary/secondary texts. QC claims remain descriptive/interpretive. | Can analyze option framing, uncertainty, escalation language, actor roles, and changes across memoranda, telegrams, meeting records, and correspondence. | Can analyze safety discourse, risk normalization, communication patterns, and organizational rationales across findings and testimony. |
| PT contribution | Existing rival mechanisms and pre-specified tests are promising, but the direct-correspondence and independent-eyewitness gaps cap causal claims. | Can test civilian initiation, military conversion/coercion, structural collapse, and failed alternatives if direct sources are acquired. | Can test sequencing and discriminating implications among risk-management, military-compellence, alliance/diplomatic, and leadership mechanisms within U.S. decision-making. It cannot infer total Soviet/Cuban intent from a U.S.-selected record. | Can test technical, communication/management, schedule-pressure, and safety-institution mechanisms, but the official report already supplies a famous causal answer. |
| Exact denominator | **Fail.** One 3,477-word, 24,131-byte curated synthesis; no complete source-object denominator or excerpt inventory. | Feasible only after exact edition objects and inclusion/exclusion rules are frozen. | **Strong.** Official volume contains documents `d1`–`d390`; canonical TEI master is one volume file. Exact analytic subset still must be frozen. | Potentially strong if a complete, named government report or exact hearing set is selected; not audited to a final packet here. |
| Rights basis | **Fail/unknown.** See item audit below. Public access was treated as if it implied permitted processing/reuse. | Potentially good for pre-1931 U.S. editions and Project Gutenberg objects; modern scholarship needs permission or cite-only treatment. Jurisdiction must be stated. | **Strong documented basis.** Official repository license says U.S. public domain plus CC0 worldwide and permits copy/modify/distribute/perform, with no warranty and no effect on third-party publicity/privacy rights. | Medium. U.S.-government-authored text may be public domain, but NASA expressly warns contractor/grantee content can remain copyrighted. Item-level audit remains necessary. |
| Stable retrieval and anchors | **Fail.** Six live HTML locators, no retrieval times or source hashes; packet lines recover the derivative, not the original assertions. | Feasible using pinned scans/eBooks, printed page/chapter locators, raw and normalized hashes, and excerpt maps. | **Strong.** Canonical volume and `dN` IDs, TEI P5 master, public version history, and document URLs. Page-break IDs are explicitly noncanonical and require a pinned commit/hash. | Strong for official PDF pages and NASA HTML headings; OCR and third-party exhibits require review. |
| Source diversity/dependence | Moderate apparent diversity, but four records are modern reprints or secondary syntheses and the packet paraphrases them into one voice. Direct correspondence and independent legislative eyewitnesses are absent. | Potentially strong, but only if contemporaneous sources and dependence clusters are added. | Strong diversity of U.S. record types and agencies; still one official edited series with U.S. selection bias. Soviet/Cuban/ally views appear mainly through U.S.-held communications. | Diverse testimony and technical/management records, but all are organized through a post-accident inquiry. |
| Sensitivity and access | Low privacy: historical public figures are deceased. Political/military violence and contested representation require claim discipline. Current sources are open-access but not all open-license. | Open tier is plausible after rights review. Re-screen if community-held, Indigenous, private, or restricted archives are added. | Open official/declassified record. Nuclear risk, intelligence, diplomatic representation, and asymmetric U.S. framing require a content note and bounded claims. Less than 1% of selected volume text was withheld at publication. | Public tragedy involving seven deaths and living institutional actors. Use dignitary framing; avoid sensational imagery and unsupported individual blame. |
| Contamination risk | Medium/high: famous case and repeated producer use, but less canonical to general models than Challenger/Cuban crisis. Current derivative can leak prior pipeline outputs. | Medium; use a frozen discovery/validation split and no prior result text in evaluation. | High: canonical and famous. Appropriate for provenance/method-boundary validation, not an uncontaminated benchmark of model discovery. | Very high: famous teaching case with an explicit official causal conclusion. Poor first benchmark for inference quality. |
| Practical burden | Low to reuse, but governance repair is not light. | Medium/high acquisition and historian review burden. | Medium: 390 structured documents; exact thin subcorpus and reviewer sample are required. Machine-readable master lowers engineering burden. | High if full five-volume/hearing corpus is used; lower for one report but source diversity falls. |
| Existing producer reuse | **High** for PT. | Medium: some PT design can carry over, but source objects and outputs must be regenerated. | None; both producers need a new named slice after GOV. | None. |
| Fit for first governed slice | **No.** Current packet is disqualified. | Conditional fallback if Brian prioritizes producer reuse and authorizes rebuild risk. | **Recommended.** Best governance substrate if Brian accepts new producer work and U.S.-scope limits. | Secondary fallback or provenance stress-test, not recommended as the first methodological benchmark. |

### Current 18 Brumaire item-level rights audit

This table distinguishes the underlying historical work, the edition or
translation actually used, and the host's permissions. A documented basis is
not a legal conclusion.

| Source | Underlying work | Edition/translation actually referenced | Host statement | Disposition for local processing | Disposition for full-text/excerpt publication |
|---|---|---|---|---|---|
| A. Bonaparte justification | 1799 proclamation; historical underlying text | John Hall Stewart, *A Documentary Survey of the French Revolution* (Macmillan, 1951), pp. 763–65, **“slightly retranslated”** by the GMU project | The FAQ expresses an opinion that class lectures/scholarly presentations are educational fair use, asks for attribution, and gives no general text-reuse license. | **Blocked pending replacement or explicit review.** The 1951/retranslation layer is not shown to be public domain or licensed. | **Blocked.** Public accessibility and a fair-use opinion do not authorize a redistributable corpus. |
| B. Brumaire decree/proclamation | 1799 official legal texts | Frank Maloy Anderson, *The Constitutions and Other Select Documents…*, 1904 | U.S. Copyright Office says all U.S. works published before 1931 are public domain. But Napoleon Series says its site content may be downloaded only for personal/noncommercial use and prohibits redistribution, adaptation, and storage elsewhere without permission. | **Do not use the host transcription.** Re-transcribe or extract from a pinned 1904 scan with a documented edition basis. | Anderson edition can support a U.S. public-domain basis; the Napoleon Series rendering cannot be the release object absent permission. |
| C. Constitution of Year VIII | 1799 constitutional text | Anderson 1904 English edition | Same as B; the page itself confirms the 1904 edition and numbered articles. | Same conditional route as B. | Same conditional route as B; printed article numbers make deterministic anchoring feasible once the edition object is pinned. |
| D. Eymeric Job narrative | Contemporary secondary article | Current Fondation Napoléon English web article | Fondation's legal page says, absent explicit contrary notice, its texts belong to the Fondation and may not be used, reproduced, or disseminated, even partially outside individual/private consultation, without written consent. | **Blocked absent written permission.** External human reading/citation is not a corpus-processing license. | **Blocked absent written permission.** |
| E. Malcolm Crook essay | Contemporary historiographical essay | H-France Napoleon Forum, 1999 | The page ends “Copyright 1999 H-France and Malcolm Crook.” No license for this Forum essay was found. H-France Review's nonprofit electronic-distribution policy applies to Reviews and should not be silently generalized to the Forum. | **Blocked/unknown absent explicit permission or a documented legal exception.** It can remain a cite-only scholarly reference. | **Blocked/unknown.** Do not redistribute the full article or assume the Review license applies. |
| F. Bourrienne memoir | Bourrienne's nineteenth-century memoir | Project Gutenberg eBook 3553, edited by R. W. Phipps, English, “Volume 03”; current packet points instead to a Britannica CDN mirror | Project Gutenberg marks eBook 3553 “Public domain in the USA.” Its permission guidance allows reuse, while warning that non-U.S. redistribution requires jurisdictional review and its trademark terms still apply. | **Conditional pass:** pin the canonical PG file/version, remove reliance on the mirror, record exact file/hash, edition metadata, and jurisdiction. | **Conditional pass** in the United States; preserve source attribution and do not imply PG endorsement. International release needs review. |

Additional disambiguation: the current 1799 case packet contains no Marx text.
Marx's *The Eighteenth Brumaire of Louis Bonaparte* concerns Louis-Napoleon's
1851 coup through analogy to 1799. If later added, it is retrospective theory or
historiography for the 1799 case, not contemporaneous evidence of its mechanism.
Its own edition/translation rights would require a separate record.

## 4. Facts, inferences, and recommendations

### 4.1 Observed facts

#### Current Brumaire artifact

- **Fact (high confidence):**
  `input_text/source_packets/18_brumaire_source_packet.txt` is 434 lines,
  3,477 words, and 24,131 bytes. Its SHA-256 is
  `cb3065594d10f8510e134b9b027f5cd4ef3a4d6ac2694c47131fef11d9217ceb`.
  The companion JSON SHA-256 is
  `3ea83dd195be5fad74b102f4bc606347b23642acf96c90ec60ad81c793cd3f88`.
- **Fact (high confidence):** the packet is a hand-composed chronological
  synthesis. Most assertions are introduced as “Source D says,” “Source E
  says,” and similar paraphrases; it is not a byte-preserving collection of the
  six source objects.
- **Fact (high confidence):** an exact-line and case-insensitive phrase check did
  not find a duplicated Murat/Orangerie sentence in the tracked packet. A
  duplicate/drift control must therefore use a deliberately planted mutation
  rather than claim an observed duplicate.
- **Fact (high confidence):** neither the text nor JSON stores source retrieval
  timestamps, source-object byte lengths/hashes, exact edition IDs for every
  record, per-excerpt original page/paragraph positions, item-level rights
  decisions, or a publication/access tier.
- **Fact (high confidence):** the current research design itself names missing
  private correspondence and independent legislative eyewitnesses. Producer
  evidence keeps the private-correspondence gap `partially_mitigated`, not
  acquired, and caps claim scope.
- **Fact (high confidence):** existing PT evidence showing 6/6 *packet marker*
  coverage proves that the derivative's source labels were represented. It
  does not prove faithful reconstruction of six original sources or permission
  to redistribute them.

#### FRUS alternative

- **Fact (high confidence):** the official table of contents defines Volume XI
  as 390 documents, `d1`–`d390`, covering the Cuban Missile Crisis and aftermath
  in 1962–1963.
- **Fact (high confidence):** the HistoryAtState repository publishes one TEI
  P5 master file per volume. Volume IDs and document `dN` IDs are canonical and
  are not altered; the maintainers explicitly warn that page-break IDs are not
  canonical and may be corrected.
- **Fact (high confidence):** the repository license places the project in the
  U.S. public domain and applies CC0 worldwide. It permits copying,
  modification, distribution, performance, and commercial use without
  permission, but disclaims warranties and does not waive third-party privacy,
  publicity, patent, or trademark rights.
- **Fact (high confidence):** the volume preface says the record includes
  supporting and alternative views and documents U.S. decisions. It also says
  a separate microfiche supplement contains significant additional documents;
  only a small fraction of extensive intelligence material and only important
  examples of allied consultation appear in the print volume; only a
  representative amount of finished intelligence was selected.
- **Fact (high confidence):** the preface reports less than 1% of the selected
  volume documentation withheld in declassification review, no documents
  denied in full, and that the Advisory Committee did not review this
  individual volume.
- **Fact (high confidence):** sample canonical records demonstrate source
  diversity and stable document-level anchors: `d1` is an October 1 intelligence
  briefing, `d50` an October 23 EXCOM action record, `d100` an October 28 State
  Department telegram, `d150` a November 5 presidential memorandum, and `d200`
  a November 21 telephone-conversation memorandum.

### 4.2 Inferences

- **Inference (high confidence):** deterministic anchor recovery from the
  current Brumaire packet to the packet's own line positions is possible;
  deterministic recovery from most packet claims to the exact original source
  span is not. A URL plus “Source D says” is not an anchor.
- **Inference (high confidence):** replacing only the four restrictive URLs
  would not cure the current Brumaire artifact. The source universe,
  derivation chain, excerpt selection, and claims all need regeneration from
  governed source objects.
- **Inference (medium/high confidence):** a rights-clean Brumaire rebuild is
  feasible in principle using the Anderson 1904 edition, Project Gutenberg
  Bourrienne edition, and other pinned public-domain editions. It may still fail
  the methodological gate if the direct correspondence/eyewitness denominator
  cannot support the intended causal claims.
- **Inference (high confidence):** FRUS is not a complete event history. It is a
  strong, deliberately bounded source for U.S. policy formulation and official
  diplomatic exchange. A claim about “why the Soviet Union/Cuba acted” would
  exceed this denominator unless additional governed perspectives are added.
- **Inference (medium confidence):** FRUS's 390 structured documents are large
  enough to expose real selection, anchoring, source-dependence, and reviewer
  problems while still being practical for a thin governed slice if the
  analytic subset and review sample are frozen before analysis.
- **Inference (high confidence):** both FRUS and Challenger are too famous to
  serve as uncontaminated model-discovery benchmarks. They can validly test
  provenance, contracts, method boundaries, item-level traceability, planted
  failures, and reviewer usability.

### 4.3 Recommendations

1. **Select FRUS as the first governance case.** Define the source universe as
   the pinned `frus1961-63v11.xml` master (`d1`–`d390`), not rendered HTML
   scraped ad hoc.
2. **Narrow the question to U.S. decision-making.** Do not use the first slice
   to assert a complete causal explanation of Soviet or Cuban motives, the
   whole crisis, or nuclear-crisis management generally.
3. **Freeze the analytic corpus before QC/PT.** The GOV review should list every
   included `dN`, every exclusion rule, date window, and source type. The full
   390-document source universe remains the denominator against which coverage
   and omissions are reported.
4. **Preserve method boundaries.** QC discovers/interprets frames and patterns
   in the governed texts. PT tests named rival mechanisms using temporally and
   diagnostically relevant traces. A QC theme does not become PT comparative
   support, and an FRUS editorial note does not silently become independent
   primary evidence.
5. **Use Brumaire later only through a new source lineage.** Existing rival
   hypotheses and research-design lessons are reusable; existing paragraph
   synthesis and output conclusions are not the governed source corpus.
6. **Treat public-domain status as one governance field, not the whole gate.**
   Rights, ethics, sensitivity, denominator, anchor fidelity, source
   dependence, selection bias, and publication scope each need an accountable
   decision.

## 5. Required acceptance evidence before implementation

### Minimal GOV acceptance packet

The smallest acceptable bundle should contain these artifacts (names are
illustrative; contracts belong to the future named slice):

1. **Study protocol:** case ID, bounded question, actors, time window, unit of
   analysis, intended and prohibited claims, QC profile, PT rivals/tests, and
   explicit multi-method integration purpose.
2. **Source-universe manifest:** one record per source object with work,
   edition/translation, creator, host/repository, canonical ID, acquisition
   timestamp, pinned repository commit/tag, media type, byte length, raw
   SHA-256, jurisdiction, asserted license/rights basis, processing basis,
   redistribution basis, publication tier, sensitivity tier, and accountable
   reviewer disposition.
3. **Corpus-selection manifest:** exact denominator, included document IDs and
   spans, exclusions with reasons, search/acquisition stopping rule, source-gap
   registry, and method-specific analytic subsets. For FRUS, `d1`–`d390` is the
   universe; the selected `dN` list must be explicit.
4. **Rights and access review:** source-by-source work/edition/translation/host
   analysis, allowed local operations, allowed public artifacts (metadata,
   short excerpts, full text, derivatives), prohibited uses, jurisdiction,
   and unresolved counsel/owner questions. “Publicly accessible” is not an
   allowed rights value.
5. **Derivation map:** raw object → extraction/transcription → normalized text →
   selected span → analysis unit. Record commands, tool versions, config,
   transformation notes, byte hashes, normalized hashes, and reviewer fixes.
6. **Anchor registry:** canonical source ID, edition locator, printed page or
   canonical document ID, structural path, quote/span hash, and local offsets.
   For FRUS, use volume + `dN` + pinned-commit structural paths; treat `<pb>`
   page IDs as display aids, not immutable identities.
7. **Source-gap and dependence register:** known absent source classes,
   overlapping provenance, derivative/editorial sources, expected
   observability, claim impact, accepted caps, and next acquisition action.
8. **Sensitivity/ethics/publication plan:** access tier, content note,
   privacy/publicity screen, community/Indigenous applicability screen,
   dignitary considerations, excerpt/full-text release policy, retention, and
   deletion/withdrawal response. CARE is not triggered by either proposed
   corpus as currently scoped; re-screen if Indigenous/community-held data are
   added rather than mechanically declaring CARE compliance.
9. **Fixity package:** BagIt 1.0 or an equivalently explicit payload and
   tag-manifest structure with SHA-256 manifests. RFC 8493 gives a useful
   completeness/validity distinction; it is an integrity transport format, not
   a semantic or rights validator.
10. **Review record:** dated decisions from source-governance/rights,
    historian/domain, QC-method, PT-method, and release reviewers, including
    dissents and residual uncertainty.

FAIR supports persistent identifiers, rich metadata, provenance, and reusable
conditions. CARE is people- and purpose-oriented and becomes relevant when the
source scope implicates Indigenous data governance. Neither substitutes for an
item-level rights decision or method-valid evidence.

### Required deterministic and adversarial controls

Before any QC/PT producer run, the GOV bundle must demonstrate:

- a changed or missing payload byte makes fixity validation fail;
- an unmanifested payload file makes completeness fail;
- a source with missing edition/translation, retrieval date, or rights
  disposition cannot enter the analytic corpus;
- “public URL,” “fair use,” and “unknown” cannot silently map to
  “redistributable full text”;
- a restricted text can be excluded from public payloads while its metadata and
  claim limitation remain visible;
- planted exact and near-duplicate sentences reach their intended
  duplicate/drift diagnostics;
- sampled anchors reconstruct the same source span from a clean checkout;
- a changed upstream hash triggers a new source version and review rather than
  silently replacing bytes;
- exact source-universe, included, excluded, unavailable, and selected counts
  reconcile;
- removal of a source or anchor makes the coverage/evidence grade fall;
- an editorial summary cannot be counted as an independent primary source;
- two records with shared lineage cannot be counted as independent
  corroboration without an explicit dependence disposition;
- a QC code/pattern cannot populate PT likelihood/comparative-support fields;
- a PT rival without a discriminating observable/source class cannot pass the
  design review;
- a claim about Soviet/Cuban intent fails against an FRUS-only U.S.-policy
  scope unless linked to a governed source that can support it;
- sensitive/restricted tiers cannot leak into the public reviewer packet; and
- the public artifact states corpus and perspective limits next to its claims,
  not only in a buried appendix.

### Evidence grade implications

This report is D-grade design evidence. A schema-validated synthetic manifest
would be at most C. A real governed source bundle with deterministic tests,
observed review, negative controls, exact recovery, and approved publication
scope is needed for an A-grade GOV claim. Selecting a case does not move GOV,
QC, PT, R01, or any SOTA grade.

## 6. Failure modes and what to try next

| Failure | What it means | What to try next |
|---|---|---|
| FRUS analytic subset is chosen after seeing QC/PT results | Selection leakage; apparent support can be curated post hoc. | Freeze `dN` inclusion/exclusion and review sample before producer runs; deviations create a new bundle version. |
| FRUS produces a persuasive “why the USSR/Cuba acted” conclusion | The U.S.-record denominator was exceeded. | Narrow to U.S. decision/recorded exchange or acquire separately governed Soviet/Cuban perspectives. |
| 390 documents overwhelm reviewers | Source universe and review task are too large, not permission to hide selection. | Keep the universe manifest; define a question-led analytic subset plus a deterministic coverage table and a stratified reviewer sample. |
| FRUS document content changes while canonical IDs remain | Canonical identity is not byte identity; upstream corrections occurred. | Pin commit/tag and raw hash; show upstream diff; open a new source-object version. |
| FRUS TEI parser relies on noncanonical page IDs | Anchor contract chose a mutable identifier. | Anchor volume + `dN` + pinned structural/text hash; retain printed page only as a human locator. |
| Brumaire permission is denied or unanswered | Current modern source cannot be part of the released corpus. | Replace it with a governed public-domain edition or retain it as cite-only background; regenerate downstream derivatives. |
| Rights-clean Brumaire still lacks correspondence/eyewitnesses | Rights repair did not solve causal observability. | Narrow the question/claims, accept and display the source cap, or use FRUS first. |
| A public-domain underlying text is copied from a restrictive host | Work rights were confused with host/edition terms. | Acquire a permitted scan/eBook and create a traceable transcription from that object. |
| OCR/transcription differs across copies | Quote and position anchors can drift. | Preserve raw scan and OCR; sample against printed pages; version normalized text; map every correction. |
| QC themes are treated as causal tests | Method boundaries collapsed. | Keep QC analytic claims and PT comparative support in distinct exports linked through source/question IDs. |
| Famous-case answers appear excellent | Memorization/contamination may be masquerading as inference. | Use planted source gaps, reordered/withheld evidence, provenance tests, and boundary controls; do not score open-ended factual recall as discovery validity. |
| A government-hosted item includes contractor/third-party content | Hosting was mistaken for public-domain status. | Perform item-level rights review; use the source's explicit license/rights metadata or exclude it. |
| International redistribution is planned | U.S. public-domain assumptions may not travel. | Use FRUS's explicit CC0 basis where applicable; otherwise obtain jurisdiction-specific review or limit publication territory/artifact type. |
| Three acquisition/review attempts add no new evidence | Circuit breaker reached. | Record the null, preserve the bundle and claim cap, and move to the next candidate rather than silently weakening GOV. |

## 7. Decision requested and remaining blockers

### Exact decision for Brian

Approve one planning disposition, not an implementation:

> **Recommended:** “Use `frus1961-63v11` as the first governed public case,
> bounded to U.S. decision-making and recorded diplomatic exchange. A future
> named `GOV-FRUS-CMC` slice may freeze the real source universe/subcorpus,
> rights/access record, anchors, tests, and review packet. No QC, PT, adapter, or
> workbench implementation is authorized by this decision.”

Or, if producer reuse outweighs governance/anchor advantages:

> “Retain Brumaire as the preferred case only after a rights-clean source
> rebuild. The current six-source derivative is rejected as the governed
> corpus. A later named GOV slice must prove editions, permissions, denominator,
> direct-source adequacy, anchors, and publication scope before QC/PT work.”

### What remains blocked under either choice

- the exact FRUS analytic `dN` list or exact rights-clean Brumaire source list;
- accountable source-governance/rights signoff and publication jurisdiction;
- QC and PT producer authorization, strict exports, and new real runs;
- historian/method review of the question, rival mechanisms, source dependence,
  and claim caps;
- any workbench adapter, reviewer packet, R01 claim, or mixed-methods claim;
- quantitative-text owner/task and all later mixed-method integration; and
- any statement that the workbench or a case result is SOTA.

## 8. Sources, skipped sources, null results, and freshness triggers

### Local sources consulted

- `.claude/tasks/decision_research_context.md`
- `docs/ROADMAP.md`
- `docs/plans/001_walking_skeleton.md`
- `docs/plans/003_integration_versioning_and_clean_state.md`
- `~/projects/process_tracing/docs/source_packets/18_BRUMAIRE_SOURCE_PACKET.json`
- `~/projects/process_tracing/docs/source_packets/18_BRUMAIRE_RESEARCH_DESIGN.md`
- `~/projects/process_tracing/input_text/source_packets/18_brumaire_source_packet.txt`
- `~/projects/process_tracing/evidence/current/Evidence_Plan003_Slice1_SourcePacketContract.md`
- `~/projects/process_tracing/evidence/current/Evidence_Plan003_Slice1b_SourceCoverage.md`
- `~/projects/process_tracing/evidence/current/Evidence_Plan003_SourceGapDisposition.md`
- `~/projects/process_tracing/evidence/current/Evidence_Plan003_SourceAwareExtraction.md`

### External sources consulted

All were accessed 2026-07-12.

#### Current Brumaire sources and rights

1. GMU/Roy Rosenzweig Center, “Brumaire: Bonaparte's Justification” —
   https://revolution.chnm.org/d/461
2. *Liberty, Equality, Fraternity* FAQ/copyright guidance —
   https://revolution.chnm.org/faq
3. Napoleon Series, “Copyright” —
   https://www.napoleon-series.org/about/copyright/
4. Napoleon Series, “Brumaire Decree and Proclamation of the Consuls” —
   https://www.napoleon-series.org/research/government/legislation/c_brumaire.html
5. Napoleon Series, “Constitution of the Year VIII” —
   https://www.napoleon-series.org/research/government/legislation/c_constitution8.html
6. Fondation Napoléon, Eymeric Job, “18 Brumaire: the context and course of a
   coup d'État” —
   https://www.napoleon.org/en/history-of-the-two-empires/articles/18-brumaire-the-context-and-course-of-a-coup-detat/
7. Fondation Napoléon, “Legal” (last updated 2026-03-04) —
   https://www.napoleon.org/en/legal/
8. H-France, Malcolm Crook, “The Myth of the 18th Brumaire” —
   https://h-france.net/the-myth-of-the-18th-brumaire/
9. H-France, “Forum on Napoleon (1999)” —
   https://h-france.net/forum-on-napoleon-1999/
10. H-France Review editorial/copyright guidelines —
    https://h-france.net/h-france-review-editorial-policies/
11. Project Gutenberg eBook 3553, *Memoirs of Napoleon Bonaparte — Volume 03* —
    https://www.gutenberg.org/ebooks/3553
12. Project Gutenberg, “Permission How-to” —
    https://www.gutenberg.org/policy/permission
13. Open Library/Internet Archive catalog record for Anderson's 1904 edition —
    https://openlibrary.org/books/OL7122048M/The_constitutions_and_other_select_documents_illustrative_of_the_history_of_France_1789-1901
14. U.S. Copyright Office Circular 15A, *Duration of Copyright* —
    https://www.copyright.gov/circs/circ15a.pdf

#### Recommended FRUS alternative

15. State Department Office of the Historian, Volume XI table of contents —
    https://history.state.gov/historicaldocuments/frus1961-63v11/toc
16. Volume XI preface, scope, selection, editorial, and declassification notes —
    https://history.state.gov/historicaldocuments/frus1961-63v11/preface
17. Volume XI source collections and source limitations —
    https://history.state.gov/historicaldocuments/frus1961-63v11/sources
18. Office of the Historian, “About the Foreign Relations Series” —
    https://history.state.gov/historicaldocuments/about-frus
19. HistoryAtState `frus` repository README —
    https://github.com/HistoryAtState/frus
20. HistoryAtState `frus` license (U.S. public domain + CC0) —
    https://github.com/HistoryAtState/frus/blob/master/LICENSE.md
21. HistoryAtState release `v1.0.18` —
    https://github.com/HistoryAtState/frus/releases/tag/v1.0.18
22. Sample canonical records:
    https://history.state.gov/historicaldocuments/frus1961-63v11/d1,
    https://history.state.gov/historicaldocuments/frus1961-63v11/d50,
    https://history.state.gov/historicaldocuments/frus1961-63v11/d100,
    https://history.state.gov/historicaldocuments/frus1961-63v11/d150,
    https://history.state.gov/historicaldocuments/frus1961-63v11/d200, and
    https://history.state.gov/historicaldocuments/frus1961-63v11/d390

#### Secondary alternative and general rights check

23. NASA History, Rogers Commission report index (Volumes I–V) —
    https://www.nasa.gov/history/rogersrep/genindex.htm
24. NASA, Rogers Commission Volume I PDF —
    https://sma.nasa.gov/SignificantIncidents/assets/rogers_commission_report.pdf
25. NASA NTRS, House Report 99-1016, “Investigation of the Challenger
    Accident,” with “Work of the US Gov. Public Use Permitted” metadata —
    https://ntrs.nasa.gov/citations/19870002391
26. NASA publication policy on U.S.-government and contractor/grantee copyright
    (NPR 2200.2C, chapter 4) —
    https://nodis3.gsfc.nasa.gov/displayCA.cfm?Internal_ID=N_PR_2200_002C_&page_name=Chapter4
27. U.S. Copyright Act, 17 U.S.C. § 105 —
    https://www.copyright.gov/title17/92chap1.html

#### Governance standards/principles

28. Wilkinson et al., “The FAIR Guiding Principles for scientific data
    management and stewardship,” DOI 10.1038/sdata.2016.18 —
    https://doi.org/10.1038/sdata.2016.18
29. Global Indigenous Data Alliance, “CARE Principles for Indigenous Data
    Governance” — https://www.gida-global.org/careprinciples
30. RFC 8493, *The BagIt File Packaging Format (V1.0)* —
    https://www.rfc-editor.org/info/rfc8493/

### Skipped or non-authoritative sources

- Wikipedia, Reddit, general blogs, vendor summaries, and search-result snippets
  were not used as substantive evidence.
- Search results for the Britannica CDN mirror were not treated as a license;
  the canonical Project Gutenberg record was used instead.
- Napoleon Series statements about the legal effect of putting public-domain
  material online were recorded only as the host's asserted terms, not accepted
  as a legal interpretation.
- H-France Review redistribution rules were not generalized to the separate
  1999 H-France Forum essay.
- The NASA Challenger candidate was not taken through a final item-level packet
  design after FRUS satisfied the stopping rule with stronger machine-readable
  governance properties.
- No Soviet, Cuban, French, or international archive was exhaustively searched;
  no rights holder, archive, legal counsel, or community representative was
  contacted.

### Null results and unresolved questions

- No general reuse license was found for the GMU Stewart retranslation.
- No permission was found allowing the Fondation Napoléon article to be copied,
  processed into a distributable corpus, or republished.
- No reuse license was found on the Crook Forum page; it displays an explicit
  copyright notice.
- The current Brumaire packet provides no source-object snapshots/hashes or
  exact excerpt map from which original-source fidelity can be reconstructed.
- No public direct correspondence set closing the Brumaire private-planning gap
  was identified in this bounded audit.
- FRUS does not provide a neutral Soviet/Cuban source denominator. The volume
  preface itself documents selected intelligence, ally, and supplement gaps.
- The exact FRUS analytic `dN` list and reviewer sample remain an acceptance
  artifact for a future named GOV slice, not a decision to improvise here.

### Freshness triggers

Re-run the affected review when any of the following occurs:

- a source URL, content hash, repository commit/tag, edition metadata, or host
  rights page changes;
- a FRUS upstream commit changes `frus1961-63v11.xml`, an erratum changes a
  document boundary/content, or a new release supersedes the pinned version;
- a new publication jurisdiction or commercial use is proposed;
- full text or images replace metadata/excerpts in the release plan;
- a new source class, community, Indigenous record, living-person record, or
  restricted archive is added;
- the case question expands beyond U.S. decision-making or the governed
  denominator;
- direct Brumaire correspondence or independent eyewitness material is found;
  or
- a producer run, source selection, or reviewer outcome is reused for a new
  benchmark claim.
