# Decision Brief: First Governed Public Case

Date: 2026-07-12
Status: decision required; documentation only
Decision owner: Brian
Recommended disposition: select `GOV-FRUS-CMC` for later governance-only
authorization

## Outcome

Select the U.S. Department of State's *Foreign Relations of the United States,
1961–1963, Volume XI, Cuban Missile Crisis and Aftermath*
(`frus1961-63v11`) as the first governed public source universe, with the first
case question bounded to **U.S. policy decision-making and recorded diplomatic
exchange**.

Do not approve the current 18 Brumaire packet as the governed corpus. It is a
hand-composed derivative whose source-object denominator, exact anchors, and
reuse rights are not recoverable from the artifact. A rights-clean Brumaire
rebuild remains a fallback if reuse of the existing process-tracing design is
more important than FRUS's stronger governance substrate.

This recommendation does not select an analytic FRUS subcorpus, authorize GOV,
authorize producer work, or move any evidence grade.

## Decision in one table

| Option | Governance finding | Method value | Cost | Disposition |
|---|---|---|---|---|
| `GOV-FRUS-CMC` | Official 390-document universe, public-domain/CC0 TEI masters, canonical document IDs, version history, and explicit editorial/source limits | Strong QC and PT roles for a bounded U.S. decision-process question; later provides enough source units to test a quantitative-text feasibility protocol | New QC/PT case work; U.S.-record selection bias must remain visible | **Recommended** |
| Rights-clean Brumaire rebuild | Feasible only by replacing/reacquiring restrictive editions and rebuilding every source/excerpt lineage | Reuses the strongest existing PT research design and rival mechanisms | High acquisition, historian, permission, transcription, and anchor-recovery burden; direct correspondence/eyewitness gaps remain | Conditional fallback |
| Current Brumaire packet as-is | No source-object denominator or excerpt map; four host/edition paths are blocked or restrictive, one is conditional, and one underlying edition needs a different acquisition route | Existing PT marker coverage and prior runs | Passing it would confuse public access, source rights, and derivative provenance | **Reject** |
| Rogers Commission / Challenger | Public official record and strong organizational/technical mechanism question | Useful later provenance or planted-failure case | Famous answer, contractor/third-party rights exceptions, post-accident inquiry framing | Do not select first |

## Why FRUS is the safer default

The official FRUS volume defines documents `d1` through `d390`. The State
Department's public source repository publishes one TEI P5 master per volume,
declares volume/document identifiers canonical, retains version history, and
states that repository files are in the U.S. public domain and CC0 worldwide.
The repository also warns that page-break identifiers are not canonical, so a
future bundle must pin a source commit and bytes rather than trusting display
pages. [FRUS repository and license](https://github.com/HistoryAtState/frus),
[Volume XI](https://history.state.gov/historicaldocuments/frus1961-63v11).

FRUS's strength is not neutrality. Its own preface describes an official record
of U.S. decisions, selected documentation, a separate supplement, limited
intelligence and allied material, and less than one percent withholding from
the selected volume. Therefore the first question must not become “why the
Soviet Union or Cuba acted” or a complete account of the crisis.
[Volume XI preface](https://history.state.gov/historicaldocuments/frus1961-63v11/preface),
[source statement](https://history.state.gov/historicaldocuments/frus1961-63v11/sources).

Recommended question frame:

> How and why did U.S. decision-making converge on quarantine plus negotiated
> removal rather than immediate strike/invasion or passive acceptance during
> the Cuban Missile Crisis, as represented in the governed U.S. record?

QC may discover and anchor option framing, uncertainty, escalation language,
actor roles, disagreement, and changes across source genres. PT may compare
predeclared risk-management, military-compellence, alliance/diplomatic, and
leadership mechanisms through diagnostic traces. QC patterns remain
descriptive/interpretive; they do not become PT comparative support.

## Why the current Brumaire packet fails GOV

The packet is a 3,477-word chronological paraphrase/excerpt synthesis, not six
preserved source objects. It lacks source-object hashes, edition and translation
identity, retrieval observations, exact excerpt maps, rights dispositions,
publication tiers, and original-span recovery.

- The GMU Bonaparte item is a “slightly retranslated” 1951 Stewart edition; its
  FAQ gives no general reuse license.
- Fondation Napoléon's legal terms prohibit reuse outside private consultation
  without written consent.
- H-France marks the Crook essay copyright 1999 and supplies no located reuse
  license for that Forum item.
- The Napoleon Series prohibits redistribution/adaptation of its renderings;
  the underlying 1904 Anderson edition must be reacquired from a permitted
  public-domain object.
- Project Gutenberg marks Bourrienne eBook 3553 public domain in the USA, but
  the packet points to a mirror rather than a pinned canonical file and still
  lacks edition/hash/jurisdiction review.

These are documented rights-basis findings, not legal advice. Public
accessibility is not a redistribution or processing license.

## Future `GOV-FRUS-CMC` contract

If Brian selects this option and later authorizes the named governance slice,
requirements must be derived in this order before any schema or producer run:

1. **Protocol:** case ID, bounded question, actors, time window, unit, intended
   and prohibited claims, QC profile, PT rivals/tests, and multi-method purpose.
2. **Source universe:** pinned FRUS release/commit and raw TEI hash; every
   `d1`–`d390` record remains in the denominator.
3. **Selection:** exact analytic `dN` list, exclusion reasons, date window,
   source types, stopping rule, stratified review sample, and source-gap ledger,
   frozen before QC/PT results are visible.
4. **Rights/access:** item-level work/edition/host basis, processing and
   publication permissions, jurisdiction, sensitivity tier, prohibited uses,
   and accountable reviewer.
5. **Derivation:** raw TEI to normalized text to selected span to analysis unit,
   with commands, versions, transformations, hashes, and reviewer corrections.
6. **Anchors:** volume + canonical `dN` + pinned structural path + quote/span
   hash + local offsets; printed page is only a human locator.
7. **Dependence/gaps:** source lineage, editorial versus primary status,
   expected observability, known absent perspectives, claim impact, and next
   acquisition action.
8. **Release:** public/controlled tiers, content note, privacy/publicity and
   community-governance screen, retention/withdrawal plan, fixity package, and
   dated historian, rights, QC, PT, and release review.

## Acceptance evidence and controls

The future slice may promote only the bounded claim that its named corpus is
governed and recoverable when all of these are observed:

- source-universe, selected, excluded, unavailable, and reviewed counts
  reconcile;
- clean-checkout sampled anchors recover the same source spans;
- raw and normalized bytes are fixed to a source version and hashes;
- every selected object has edition, acquisition, rights, sensitivity,
  processing, redistribution, and publication dispositions;
- perspective and source-gap limits appear beside claims;
- historian/domain, QC-method, PT-method, source-governance, and release
  reviewers record approval, dissent, and residual uncertainty.

Required controls include changed/missing bytes, unmanifested files, absent
edition or rights fields, public-URL-to-redistributable escalation, duplicate
sentences, upstream byte drift under a stable ID, unrecoverable anchors,
editorial summaries counted as independent primary evidence, lineage-dependent
sources counted as corroboration, QC fields entering PT inference, PT rivals
without discriminating observables, Soviet/Cuban-intent claims under a
FRUS-only scope, and restricted material leaking into the public packet.

Synthetic manifests remain at most C. A real reviewed bundle with
discriminating tests and observed recovery is required for A. This brief is D
design evidence and does not move GOV from F.

## Failure modes and stop points

| Failure | Required action |
|---|---|
| Analytic subset chosen after QC/PT output | Reject the run; freeze a new bundle version before rerunning. |
| Review burden for 390 documents is excessive | Keep all 390 in the universe; narrow a question-led analytic subset and stratified review sample visibly. |
| A claim exceeds U.S. decisions/recorded exchange | Narrow it or separately govern Soviet/Cuban/other sources. |
| Upstream content changes under a canonical ID | Preserve old bytes, diff, version, and re-review; never overwrite. |
| Page-break ID used as immutable identity | Replace with pinned `dN` structural/text anchors. |
| Rights or historian review is unresolved | Stop GOV promotion; metadata-only/cite-only status is not full-text approval. |
| Three acquisition/review attempts add no new evidence | Record the null and claim cap, then use the next candidate. |

## Exact decision requested

Brian may approve this planning sentence:

> Use `frus1961-63v11` as the first governed public case, bounded to U.S.
> decision-making and recorded diplomatic exchange. A future separately named
> `GOV-FRUS-CMC` slice may freeze and review the real source universe,
> subcorpus, rights/access, anchors, controls, and release packet. This decision
> does not authorize QC, PT, adapters, or other implementation.

If Brian prefers Brumaire, the alternative decision must explicitly reject the
current derivative and authorize only a later rights-clean source rebuild.

## Synthesis provenance

The parent read every existing research/session artifact before writing this
brief. No identified research artifact was skipped:

- `.claude/tasks/session_context.md`
- `.claude/tasks/sota_program_progress.md`
- `.claude/tasks/research_artifact_authority.md`
- `.claude/tasks/research_producer_readiness.md`
- `.claude/tasks/research_sota_landscape.md`
- `.claude/tasks/decision_research_context.md`
- `.claude/tasks/research_gov_case_options.md`
- `.claude/tasks/research_qt_first_task_options.md`
- `~/projects/investigations/mixed_methods_workbench/2026-07-12-sota-program-baseline.md`
- `~/projects/investigations/cross-project/2026-06-26-mixed-methods-repo-assessment.md`
- `~/projects/investigations/cross-project/2026-06-26-theory-forge-ac-coupling.md`

Canonical sources reconciled were `docs/PLANNING_STATUS.md`, `docs/ROADMAP.md`,
`docs/MIXED_METHODS_CAPABILITY_MAP.md`, `docs/CAPABILITY_DEPENDENCY_GRAPH.md`,
`docs/SOTA_EVIDENCE_SCORECARD.md`, `docs/CONCERNS.md`, the long-term goal,
handoff files, and the current process-tracing Brumaire design/packet/source
text. The complete external bibliography, null results, and freshness triggers
are in `.claude/tasks/research_gov_case_options.md`; pivotal primary sources are
linked above.
