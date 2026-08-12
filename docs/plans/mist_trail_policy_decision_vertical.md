# Mist Trail policy options to a reviewable decision

**Status:** bounded design candidate; case and design objective approved by
Brian on 2026-08-12; implementation is not authorized by this document

**Design route:** durable solo, Standard depth, prototype delivery profile

**Owner:** Mixed Methods Workbench

**Canonical example:** Yosemite National Park Mist Trail Corridor
Rehabilitation Draft Environmental Assessment

**Source baseline:** Workbench `main@9ab4d14`; Project Meta readiness decision
`main@cdbe32eea3a19775602b69081a5dce25844af12d`

**Landscape disposition:** linked to
`project-meta/investigations/2026-08-12_policy_analytic_stress_test_readiness.md`

## Decision in one paragraph

Build one manually reviewed development example in which a policy analyst can
compare the three official Mist Trail alternatives, inspect the evidence and
uncertainty behind each projected consequence, state the value judgments that
matter, and produce either a conditional recommendation or an explicit refusal
to rank. The result tests whether the Workbench can connect evidence to action
without turning different kinds of evidence into one confidence score, hiding
values in numerical weights, or presenting a development exercise as a
National Park Service decision. The valid result may be a conditional
recommendation, an unresolved conclusion, or a refusal to appraise.

This is an ordinary deliberative policy appraisal. It borrows the transparency
of evidence-to-decision frameworks and multi-criteria analysis, but the first
slice will not implement GRADE, Robust Decision Making, optimization, or an
additive weighted score.

## Why this is the selected stress test

The current Method Dashboard ranks `policy_options_to_decision` first because
it pressures the largest uncovered part of the Evidence-to-Action vision:

```text
official options and source-bound consequence claims
  + explicit objectives, affected interests, constraints, and uncertainty
  + visible human value judgments
  -> reviewable comparison
  -> conditional recommendation | unresolved | refused
  -> evidence or monitoring return path
```

The goal is architectural learning, not an empirical claim that this system
has improved the NPS decision. If one small packet cannot keep those elements
separate and inspectable, a generalized decision platform should not be built.

## Actor, job, and inspectable result

| Element | Bounded definition |
| --- | --- |
| Primary actor | A policy analyst or researcher reviewing a public decision; not an NPS decision maker |
| Recurring job | Compare feasible policy options while preserving the evidence, uncertainty, affected interests, value judgments, and reasons behind the conclusion |
| Decision being examined | Which of Alternatives A, B, or C best addresses the Mist Trail project's stated purpose and need under an explicitly reviewed set of priorities? |
| Inspectable result | One source-steppable decision packet and browser view that ends in `conditional_recommendation`, `unresolved`, or `refused` |
| Human judgment required | Confirm the decision frame, judge the relative importance of criteria, review consequence summaries, and accept or reject the draft conclusion |
| Explicit non-claim | The artifact is not an NPS decision, formal public comment, legal/NEPA analysis, or substitute for agency and Tribal consultation |

## Current state and target delta

The Workbench currently has a question-first dashboard, a policy-appraisal
method profile, and a ranked architecture stress-test portfolio. It does not
have a real options-to-decision result. The target delta is one local,
fixture-bound result that demonstrates the decision boundary; it is not a
generic decision engine.

| Current | Target after the future slice |
| --- | --- |
| A method profile says what policy appraisal requires. | One real public case shows those requirements as an inspectable packet. |
| The dashboard routes a policy question to several relevant methods. | A researcher can enter the selected policy-appraisal path and see a completed example. |
| Evidence, criteria, and values are described conceptually. | Each consequence, uncertainty, and judgment has an explicit owner and lineage. |
| No ranking is produced. | A conclusion is produced only when the stated evidence and human judgments license it; otherwise the packet refuses or stays unresolved. |

## Frozen case boundary

The official source defines three alternatives:

- **Alternative A — No action:** continue maintenance and small-scale safety
  improvements without substantial new construction.
- **Alternative B — Existing vehicle bridge:** retain and formalize the
  present crossing, separate pedestrians and vehicles, improve the existing
  trailhead and promenade, and pilot a Stock Trail loop.
- **Alternative C — New pedestrian footbridge:** construct a crossing at the
  historic footbridge location, create a new promenade and west-side trailhead,
  and restore part of the current trailhead. The Draft EA identifies this as
  the NPS proposed action.

Actions common to B and C—including new messaging, trip-planning resources,
roadway changes, shuttle-stop and restroom improvements, trail pullouts, and
selected vista restoration—must remain common actions. The comparison must not
mistakenly attribute them only to one alternative.

The first packet is bounded to the official public materials below. It may
show an evidence gap; it must not fill one from model knowledge.

| Source | Identity and intended use |
| --- | --- |
| [NPS project page](https://www.nps.gov/yose/getinvolved/misttrailcorridor.htm) | Decision owner, purpose, need, timeline, public context, issue list |
| [NPS document record](https://parkplanning.nps.gov/document.cfm?documentID=150212&parkID=347&projectID=105979) | Official document identity, public-comment status, and file links |
| [Draft EA, `sfid=849738`](https://parkplanning.nps.gov/showFile.cfm?sfid=849738&projectID=105979) | Primary comparison source; retrieved 2026-08-12; 4,495,269 bytes; SHA-256 `df5304a9116b9dc2093e1f5e2eee61b61adab3c6f65ac8214aca7e685c23cbb0` |

The minimum source windows are Chapter 1's purpose, need, and retained impact
topics; Chapter 2's Alternative A/B/C definitions and common actions; Chapter
3's resource-specific methods and consequences; and Chapter 4's consultation
boundary. Appendices are not required for the first packet. If a material
claim depends on an appendix, the packet must mark that claim unresolved until
the appendix is separately pinned and reviewed.

## Appraisal frame

The criteria are a controlled view over the NPS purpose and retained impact
topics, not a claim that the Workbench has discovered the agency's complete
decision rule.

| Criterion | Empirical question | Value question that must remain separate |
| --- | --- | --- |
| Visitor safety and preparedness | What safety, circulation, information, construction, and rescue consequences are described for each alternative? | How much priority should prevention and preparedness receive relative to other impacts? |
| Visitor experience, orientation, and accessible arrival | How does each alternative affect arrival, wayfinding, amenities, visitor flow, and the accessibility of the new facilities? | Which visitor experiences and access improvements matter most? |
| Biological and water resources | What short- and long-term effects and mitigations are described for vegetation, wildlife, habitat, floodplains, wetlands, surface water, and the Wild and Scenic River corridor? | What level of disturbance is acceptable for the expected visitor benefit? |
| Cultural, historic, and visual stewardship | How does each alternative affect cultural landscapes, historic properties, the historic crossing, archeological or ethnographic resources, and visual character? | How should restoration, preservation, contemporary use, and visual change be balanced? |
| Park operations, constructability, and resource demand | What construction duration, closures, maintenance, staff, stock-use, and operational effects are described? What important cost or resource information is absent? | Which burdens, delays, or resource commitments are acceptable? |
| Distribution across affected interests | Which visitors, staff, rescuers, stock users, traditionally associated Tribes, and resource interests receive benefits or burdens? | Whose interests should receive special consideration, and why? |

The distribution row is an overlay, not a license to invent subgroup effects.
For example, an accessible footbridge does not establish that the wider trail
is accessible, and the EA's commitment to collaborate with traditionally
associated Tribes does not establish Tribal endorsement of an alternative.

## Comparison logic

The first slice uses a deliberative matrix rather than a numeric total.

For each `option x criterion` cell, record:

- a concise consequence statement;
- direction: `benefit | harm | mixed | negligible | unknown`;
- time: `construction | long_term | both | unspecified`;
- affected interests;
- source anchors and the source's own analysis method;
- empirical uncertainty and why it exists;
- whether mitigation is assumed; and
- review state.

For each criterion, the human reviewer separately records:

- importance: `lower | material | decisive | unresolved`;
- judgment rationale;
- whether the judgment is factual, normative, or mixed;
- any dissent or alternative judgment; and
- what information could change it.

No pairwise or group-level consequence may be inferred merely because an item
appears in the same source section. No recommendation may be computed from the
labels above. The final rationale must name the decisive consequence and value
judgments in prose.

### Sensitivity without hidden weights

The view must show at least three declared priority lenses:

1. visitor safety and preparedness prioritized;
2. minimum new physical and resource disturbance prioritized; and
3. operational burden and implementation feasibility prioritized.

These are reviewer-controlled counterfactual lenses, not claims about NPS or
public preferences. If the preferred option changes across lenses, the result
is `value_sensitive`. If missing evidence prevents comparison, the result is
`evidence_limited`. Either status may coexist with a conditional
recommendation.

## Minimal local contract

This is a fixture-local Workbench contract candidate. It must not move to
`data_contracts` or be advertised as a universal policy-decision schema.

| Object | Required meaning |
| --- | --- |
| `DecisionFrame` | Question, purpose, decision authority, analyst role, status, scope, constraints, non-claims |
| `Option` | Stable official identity, wording, status quo/action status, common actions, option-specific actions, feasibility status |
| `Criterion` | Stable identity, empirical question, distinct value question, criterion source, affected scope |
| `AffectedInterest` | Named person/group/organization/resource interest and supported relationship to the decision; never an inferred preference |
| `SourceBinding` | Source version, file hash, page/section anchor, custody state, allowed use, excluded inference |
| `ConsequenceAssessment` | One option-criterion claim with direction, time, affected interests, evidence, uncertainty, mitigation assumptions, and review state |
| `CriterionJudgment` | Human-authored importance and rationale, judgment type, dissent, and change condition |
| `TradeoffFinding` | Named advantage/disadvantage that cannot be collapsed without a value choice |
| `DecisionConclusion` | `conditional_recommendation | unresolved | refused`, rationale, decisive dependencies, sensitivity status, non-claims, and next evidence/monitoring action |
| `ReviewEvent` | Immutable proposal, revision, acceptance, rejection, or supersession record |
| `DecisionPacket` | Versioned root binding the objects above, source/contract revisions, and validation state |

### Outcome envelope

Every attempted appraisal ends in one of three states:

- `success`: a complete reviewable packet with a conditional recommendation;
- `unresolved`: a complete packet whose evidence or value judgments do not yet
  license a recommendation; or
- `refused`: the decision frame or source packet violates a required invariant.

An unresolved result is a useful result. It must name the exact missing
evidence or judgment and the next admissible action.

## Domain rules and invariants

1. Reviewed prose is authoritative; the structured matrix exposes and checks
   meaning but cannot silently replace it.
2. Official NPS preference is stored as `agency_proposed_action`, not as the
   Workbench conclusion and not as empirical evidence that C is best.
3. Alternatives and common actions come from the frozen source. The appraiser
   may not invent, substitute, or merge options.
4. Empirical consequence claims and normative judgments are distinct objects
   with distinct authorship.
5. Uncertainty stays claim-specific. There is no cross-method confidence or
   evidence-strength score.
6. Criteria cannot acquire hidden numeric weights. Any later quantitative
   decision model requires separate authorization and a visible method owner.
7. A recommendation must cite its decisive consequence claims and criterion
   judgments and show at least one reversal or stability test.
8. Missing comparative cost or operational evidence remains visible and may
   force `unresolved`; it cannot be imputed.
9. Source summaries must step down to exact page/section anchors. Exact passage
   text is displayed only from hash-matching source bytes.
10. Review history is immutable. Revising a consequence or value judgment does
    not rewrite the earlier decision packet.
11. The packet must distinguish `not analyzed`, `not found in the bounded
    source`, `no effect`, and `uncertain`.
12. The public-comment period is closed as recorded by the official document
    page. The development UI must not present submission to NPS as an action.

## Ownership boundaries

| Owner | Owns in this vertical | Does not own |
| --- | --- | --- |
| Mixed Methods Workbench | Decision frame, fixture-local consumer contract, appraisal assembly, explicit value-judgment surface, conclusion, review UI, lineage across objects | Resource-specific scientific findings, NEPA/legal sufficiency, NPS authority, generic retrieval or optimization |
| NPS public source packet | Official alternatives, agency purpose/need, source analyses, mitigations, and declared proposed action | Workbench judgment or recommendation |
| Retrieval capability, if later used | Fetching the exact authorized source bytes and returning identity/hash/custody evidence | Source interpretation or appraisal judgment |
| Method-producing repositories, if later added | Their own empirical findings, uncertainty, provenance, and method-specific review | Policy recommendation or shared scoring |
| `data_contracts` | Nothing in the first slice | This fixture-local schema and policy workflow |

No changes to Qualitative Coding, Process Tracing, Theory Forge, Cybernetic
Influence, or NPS systems are required. A later producer finding must enter
through a pinned typed export and remain method-owned.

## Researcher-visible view

The first page should answer five questions in order:

1. **What is being decided?** Plain question, decision authority, source date,
   development-only warning.
2. **What are the choices?** A/B/C cards with common actions separated from
   option-specific actions.
3. **What does the evidence say?** Option-by-criterion consequence view with
   affected interests, uncertainty, and source step-down.
4. **Where do human values enter?** Visible criterion judgments and priority
   lenses; no hidden score.
5. **What follows?** Conditional recommendation, unresolved result, or refusal;
   decisive reasons; reversal conditions; and the next evidence or monitoring
   action.

Internal IDs, hashes, contract versions, and complete lineage remain available
under provenance details. The primary path uses ordinary language. A secondary
reified graph may show:

```text
[source passage] --supports--> [consequence assessment]
        [option] --is assessed by--> [consequence assessment]
     [criterion] --frames--> [consequence assessment]
[human judgment] --prioritizes--> [criterion]
[consequence assessment] + [human judgment]
        --grounds--> [conditional conclusion]
```

Administrative containment must not be displayed as substantive support.

## Failure and containment behavior

| Failure | Required behavior |
| --- | --- |
| A/B/C identity or source hash is wrong | `refused`; render no appraisal |
| An official common action is assigned to only B or C | validation failure |
| A factual claim lacks an exact source anchor | `unresolved`; exclude it from the conclusion |
| Source bytes do not match the recorded hash | show source metadata and `passage_unavailable`; never render unverified text |
| A value judgment is absent | keep the criterion unresolved; do not derive a preference |
| A consequence is not analyzed in the source | display the gap; do not treat it as no effect |
| Official preference is used as the Workbench recommendation | validation failure |
| The conclusion cannot name decisive evidence and judgments | `refused` |
| Priority lenses produce different winners | display `value_sensitive`; do not average the lenses |
| Cost/resource information is insufficient | display `evidence_limited`; request evidence or abstain |
| The reviewer rejects a consequence summary or conclusion | retain the rejected version and create a revised or unresolved packet |

The slice has no persistent database and performs no external action, so reset
means discarding the local generated packet and reconstructing it from the
frozen fixture. Source files are never deleted by reset.

## Acceptance and disproof

Direct human inspection is required; schema checks alone cannot establish that
the decision is understandable or that the summaries preserve the source.

The prototype passes when a fresh reviewer can:

- state the decision and distinguish all three official alternatives;
- identify which actions are common to B and C;
- trace a material consequence to the exact official source window;
- distinguish empirical uncertainty from a human value judgment;
- name who or what is differently affected without inferring unsupported
  preferences;
- explain why the result is conditional, unresolved, or refused;
- identify what evidence or priority change could reverse the conclusion; and
- state that the artifact is not an NPS decision or completed NEPA analysis.

The design is disproved or must be revised if:

- a recommendation requires hidden weights or a generic confidence score;
- materially different evidence and value meanings collapse into one field;
- the reviewer mistakes the NPS proposed action for an independent Workbench
  result;
- common actions, mitigation assumptions, scope, or uncertainty disappear in
  the view;
- the system must invent consequences to complete the matrix;
- an unresolved packet is treated as a failed run rather than an actionable
  result; or
- a generic decision engine is required before this one case can be inspected.

## Smallest future implementation slice

This is one sequential prototype lane; no work graph is needed.

### Slice MT-D1 — Manually reviewed decision packet and view

**Epistemic state:** `fully_specifiable_now` once Brian separately authorizes
implementation.

**Input**

- one locally committed, hash-bound source manifest for the official Draft EA;
- manually reviewed summaries for the exact source windows;
- fixture-local A/B/C options, six criteria, affected interests, consequence
  assessments, and reviewer-authored value judgments.

**Output**

- one typed `DecisionPacket`;
- one local JSON route using the same packet;
- one plain-language browser view in the existing Method Dashboard service;
- one retained screenshot or review record from the canonical journey.

**Focused checks**

- positive packet validates and renders;
- corrupted option identity or file hash refuses;
- common-action misattribution fails;
- missing source anchor becomes unresolved;
- official preference cannot satisfy the Workbench conclusion;
- absent value judgment cannot produce a recommendation;
- a changed priority lens visibly changes or preserves the conclusion without
  numeric aggregation; and
- the JSON and browser show the same outcome state and decisive dependencies.

**Authentic observation**

A fresh human reviewer uses the browser view to perform the acceptance tasks
above. This human judgment—not the fixture tests—is the first evidence that the
artifact communicates a policy appraisal.

**Implementation non-goals**

- no model call or automated source interpretation;
- no generalized decision, MCDA, GRADE, or RDM engine;
- no new shared `data_contracts` schema;
- no producer-repository integration;
- no persistence, authentication, deployment, or NPS submission;
- no second policy case; and
- no claim of methodological validation, agency endorsement, or policy impact.

**Reset and stop boundary**

Stop after the single source-bound packet, JSON/browser parity, focused
corruptions, and one fresh comprehension review. Do not generalize from the
fixture. Perform a course check earlier if the slice requires a scoring engine,
new source-research platform, or a cross-repository contract.

## Later promotion triggers, not planned slices

- Add one method-owned empirical producer only if MT-D1 shows that the
  consequence seam is useful but the official synthesis is insufficient.
- Consider an existing MCDA tool only if the reviewer needs reproducible
  preference elicitation or formal dominance analysis that the deliberative
  packet cannot provide.
- Consider RDM only for a case with genuine deep uncertainty and an existing
  scenario/model generator; the Mist Trail fixture does not establish that
  need.
- Promote any envelope to `data_contracts` only after a second real producer
  and consumer demonstrate the same semantics.
- Select the Colorado River case only after this simpler appraisal survives;
  it is an adversarial deep-uncertainty case, not MT-D1 scope.

## Open uncertainties retained in the design

1. The main EA does not appear to provide a complete comparative cost basis.
   The first packet must expose whether this prevents a recommendation.
2. The NPS is the real decision authority, but no NPS decision maker is the
   reviewer for this development artifact. The human judgments are therefore
   demonstrative and must be labeled as such.
3. Appendix material may be necessary for some operational or mitigation
   claims. It remains outside the frozen first source packet until a specific
   consequence requires it.
4. `METHOD-DASH-C2` is the current plain-language entry surface, but its
   stakeholder re-review is still pending. Reuse it and visually review the
   full journey before implementation; do not create a second dashboard.
5. The official project page anticipated a fall 2026 finding. Any future
   implementation must refresh the decision status and retain the Draft EA as
   the analyzed source version rather than silently substituting a final
   decision.

## Recommended handoff after review

If Brian accepts this exact design revision and separately authorizes MT-D1,
hand the inline execution boundary directly to evidence-first development in
this repository. Do not activate a work-unit graph or another planning layer.
