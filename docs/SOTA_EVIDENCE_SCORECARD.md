# SOTA Evidence Scorecard

Status: current visibility artifact; not an enforcement gate
Snapshot: 2026-07-12
Overall: **F — no SOTA or beyond-SOTA claim is licensed**

## Purpose

This scorecard prevents the phrase “SOTA or beyond” from collapsing unlike
methods into a feature checklist or average. It records the current evidence,
the applicable external floor, the comparison target, and the proof required
for each declared capability family.

The executable scaffold coverage remains separately reported by
`make coverage` as 0 A, 0 B, 2 C, 5 D, and 1 F. This broader program scorecard
does not replace that report and is not yet generated from runtime evidence.

## Evidence Grades

| Grade | Meaning |
|---|---|
| A | Direct source evidence plus a discriminating test or independently observed result supports the bounded claim. |
| B | Real runtime evidence supports the claim, but no discriminating test or independent observation does. |
| C | A fixture or schema-validated example supports shape/contract claims only; it does not establish real behavior. |
| D | Documentation, plan, or design rationale only. |
| F | Required evidence is missing, wrong, contradictory, or fails. |

Evidence classes advance in order:
`doc < fixture < schema_validated < test < observed`. A grade can be lower than
the highest evidence class when a critical criterion is missing. Synthetic
fixtures can license at most C-grade claims about their shape.

## Conjunctive Claim Rule

For a named task, domain, language, method profile, and release:

```text
SOTA licensed = all applicable floors pass
             AND non-inferior to refreshed incumbent on every claimed dimension
             AND superior by a predeclared meaningful margin on >=1 dimension
             AND held-out + negative-control + raw-trace evidence passes
             AND independent reviewer signs off
             AND evidence is current
```

There is no compensatory average. Faster execution cannot offset a provenance,
validity, rights, or reproducibility failure. A feature absent from an incumbent
is an opportunity, not proof of superiority.

Before any benchmark run, an independent methodological reviewer must approve a
finite mandatory release profile: capability rows, methods, designs, domains,
languages, cases, actors, primary value dimensions, and allowed N/A exclusions.
An N/A needs evidence that the item does not apply, not merely missing
implementation. The profile is immutable after results are visible. A failing
area remains a failed claim for that profile; it cannot be relabeled
“unsupported” or removed until a new version is preregistered.

The benchmark protocol must also:

- select the strongest relevant current incumbent from a documented landscape,
  not a convenient weak comparator, and include human/current-workflow and
  simple programmatic baselines where applicable;
- preregister primary dimensions, non-inferiority margins, superiority margins,
  uncertainty estimators, expected noise, sample-size/power rationale, slice
  analyses, and multiplicity control before sealed results are opened;
- assign sealed-case custody and final adjudication to actors who did not
  implement the compared system or tune against the sealed cases, with conflicts
  disclosed and rejection authority explicit;
- freeze versions, procedures, inputs, prompts, schemas, hardware/environment,
  and contamination checks; preserve every run and null/failure result.

## Current Program Coverage

| ID | Capability family | Current evidence and grade | Contemporary floor / incumbent | Required A-grade evidence | Claim limit now |
|---|---|---|---|---|---|
| T0 | Truthful evidence baseline | **F** — useful synthetic controls exist, but inventory provenance is incomplete and coverage rows are declared in code. | Evidence must change when its proof changes; negative controls must reach the intended invariant. | Derived evidence ledger, exact positive/negative controls, source-bound evidence, independent audit. | Scaffold only; no engine readiness. |
| SCOPE | Frozen claim and benchmark scope | **D** — the broad product scope exists, but no finite benchmark profile or N/A adjudication is frozen. | Scope, exclusions, baselines, dimensions, margins, power, multiplicity, and custodianship must be fixed before results. | Signed preregistration, immutable profile hash, independent N/A approval, sealed-case custody, post-run scope-drift control. | No comparison claim may be designed by subtraction after results. |
| GOV | Study, source, rights, and community governance | **D** — requirements appear in plans, not a real governed bundle. | FAIR plus appropriate CARE/consent/license/access limits; source selection and gaps must bound claims. | Real source manifest, review decisions, access layers, deliberate invalid cases, observed release review. | No real corpus is approved. |
| QUAL | Methodologically faithful qualitative analysis | **D** — upstream capability exists; no real workbench export or method-profile evaluation. | Method-specific validity, anchored evidence, memo/decision lineage, negative cases; no universal reliability rule. | Real producer export, method profile, expert-reviewed frozen case, planted anchor/method failures, error analysis. | No workbench qualitative-analysis claim. |
| PT | Rival-sensitive process tracing | **D** — PT internals exist; no producer-owned workbench export. | Rival hypotheses, mechanisms/observables, scope/dependence, absence versus unsearched, sensitivity, bounded verdict. | Strict export and real packet, source/anchor tests, rival/absence/dependence controls, expert review. | No workbench causal/process-tracing claim. |
| QT | Quantitative text measurement | **F** — no task, construct, corpus, owner, or adapter. | Construct/unit/population/use first; held-out evaluation, simple baselines, uncertainty, item-level error analysis. | Preregistered measure, sealed split, baseline comparison, calibration/slice/error review, source-level drill-down. | No quantitative strand. |
| MM | Genuine mixed-methods integration | **F** — no qual–quant strand or meta-inference. | Explicit connect/build/merge/embed/transform operation, coherent timing/sampling, aligned integration artifact, divergence handling, bounded meta-inference. | Real observed design, integration controls, joint-display/equivalent review, strand-specific quality, expert adjudication. | QC + PT remains multi-method qualitative. |
| GR | Disagreement and evidence adjudication | **D** — proposed seam; upstream mechanical workflow is not a general validity result. | Preserve rival analyses, verification actions, disagreement type, uncertainty, and human disposition. | Real disputed workbench cases, blind comparison, error/override analysis, human dispositions, seam tests. | Optional enhancer only. |
| TF | Theory operationalization and revision | **D** — contract sketch; no known-green workbench export. | Constructs, mechanisms, observables, assumptions, scope, and test obligations must remain context rather than empirical evidence. | Strict real export, challenge/revision path, theory-as-evidence negative control, producer and expert validation. | Optional enhancer only. |
| LLM | Governed LLM assistance | **D** — principles only; no workbench run or role profiles. | Named intended/prohibited uses, exact run lineage, source anchors, independent-first review where appropriate, subgroup/error analysis. | Frozen human-only and simple baselines, hallucination/injection/privacy controls, reviewer effort/override evidence, monitoring. | No LLM-quality or autonomy claim. |
| REP | Provenance and reproducibility | **D** — hash-bearing synthetic manifest, no immutable real run bundle or replay. | Source/code/config/tool/model/reviewer lineage; FAIR/CARE-aware packaging; same-environment and clean-room replay. | Content-addressed real bundle, conformance checks, successful replay by an independent actor, failure/recovery record. | No reproducibility claim. |
| INT | Interoperability and loss declaration | **D** — planned semantic versions and compatible consumers; no round trip. | REFI-QDA or declared alternatives, W3C-compatible anchors/provenance, explicit unsupported-object loss ledger. | Cross-tool fixture matrix, schema plus semantic round trips, every loss surfaced, version compatibility controls. | No interoperability claim. |
| API | Human/agent semantic parity and operations | **F** — no core API, CLI, UI, or agent surface. | One typed authoritative operation layer; stable IDs, idempotency, preconditions, authorization, structured errors, audit, bounded optional MCP. | Contract-generated API, parity tests, invalid-action and recovery tests, least-privilege/security review, observed agent tasks. | “Agent-drivable” is an aspiration. |
| EVAL | Independent comparative evaluation | **F** — no registry, frozen cases, incumbent runs, or independent reviewers. | Task-specific construct and incumbent; held-out/temporal evidence; behavior controls; uncertainty, ablation, trace and contamination review. | Sealed benchmark package, refreshed incumbent runs, independent method/security/reproducibility sign-offs, published nulls/failures. | No SOTA claim. |
| ADAPT | Adaptive next-source/case/analysis loop | **F** — roadmap hypothesis only. | Human retains direction; recommendations are discriminating, provenance-aware, costed, uncertainty-bounded, and stoppable. | Preregistered experiment against non-adaptive baseline, safety/fidelity floors, utility/effort evidence, failure taxonomy. | No beyond-SOTA claim. |

Distribution: **0 A, 0 B, 0 C, 9 D, 6 F; overall F.** The lack of C rows in
this program table is deliberate: current synthetic fixtures support only the
narrow scaffold rows in `docs/coverage_report.md`, not full capability-family
claims.

## Incumbent Baseline Registry

These are comparison candidates, not a final benchmark and not proof of any
vendor's methodological validity.

| Baseline | Current demonstrated scope | Use in future comparisons | Refresh trigger |
|---|---|---|---|
| MAXQDA 26.3 | Mature CAQDAS, mixed-methods design worksheet and joint displays, variables/stats exchange, multi-document AI assistance. | Human mixed-method design, coding, integration-display, and effort baseline. | Major release or six months. |
| ATLAS.ti 26.1 | Mature CAQDAS plus built-in local MCP that can read/write documents, quotations, codes, groups, and memos. | Agent task completion, mutation safety, audit/provenance, and method-boundary baseline. | MCP/API or major product release. |
| NVivo + XLSTAT | Mature qualitative matrices/crosstabs plus quantitative companion workflow. | Established two-product integration baseline. | Major release or six months. |
| Dedoose | Collaborative qual/quant descriptors, charts, and integrated views. | Web collaboration and mixed-data workflow baseline; include documented exchange loss. | Major release or six months. |
| QualCoder | Open/local multi-modal coding, comparison, AI assistance, and REFI support. | Open/self-hosted qualitative baseline. | Stable release or six months. |
| CATMA / INCEpTION | Stand-off annotation, collaboration/curation, audit, remote API, and format breadth. | Open annotation, review, audit, and API baseline. | Major release or six months. |
| Human-only method-specific workflow | Expert qualitative/PT/mixed-methods process using ordinary tools. | Validity, diversity, reviewer effort, and automation-anchoring baseline. | New task/domain or material protocol change. |
| Simple programmatic method | Rules, dictionary, classical model, or static sampling appropriate to the task. | Required quantitative/automation baseline before complex models or agents. | New construct/task or dataset drift. |

The first benchmark plan must freeze exact versions, task procedures, allowed
assistance, hardware/environment, inputs, outputs, and adjudication before any
implementation team sees the sealed cases.

## Required Control Families

| Surface | Known-positive | Known-negative / planted failure | Boundary or metamorphic check |
|---|---|---|---|
| Provenance | Fully recoverable real bundle | Missing/contradictory source, actor, hash, or transform | Reorder unrelated records without changing identity/result. |
| Qualitative | Anchored method-conformant finding | Fabricated quote, span drift, erased negative case, wrong profile obligation | Equivalent source normalization preserves anchor meaning. |
| PT | Rivals, observables, scope and bounded verdict complete | Residual rival missing, dependent sources double-counted, unsearched treated as absence | Reordering evidence cannot alter deterministic comparative math. |
| Quantitative text | Held-out item predictions and uncertainty | Leakage, label permutation, subgroup collapse, face-valid but invalid measure | Invariant representation changes preserve predictions within tolerance. |
| Integration | Aligned strands yield explicit relationship and meta-inference | Side-by-side outputs with no integration, mismatched construct/aggregation, divergence deleted | Row/order changes do not change relationship classification. |
| LLM/agent | Authorized source-grounded operation completes | Prompt injection, nonexistent source, unauthorized mutation, retry duplicate | Idempotent replay produces one audited state transition. |
| Interchange/replay | Supported objects round-trip and clean replay succeeds | Silent object loss, unsupported major, missing environment/input | Export/import/export semantic equivalence for supported subset. |

## External Evidence Basis

The full annotated bibliography and evidence limits are in
`.claude/tasks/research_sota_landscape.md`. Key current anchors, all accessed
2026-07-12, are:

- [Mixed Methods Integration Quality Framework (2024)](https://journals.sagepub.com/doi/full/10.1177/15586898241257555) — broad 44-criterion coverage scaffold; its own authors call for further validation.
- [2025 review of 28 CAQDAS tools](https://doi.org/10.14279/eceasst.v85.2709) — current open-science, audit, interoperability, collaboration, and AI-disclosure baseline.
- [2026 LLM-assisted qualitative-analysis scoping review](https://doi.org/10.1186/s12874-026-02913-1) — wide agreement range and incomplete reporting; autonomous superiority is not established.
- [REFI-QDA](https://www.qdasoftware.org/), [W3C Web Annotation](https://www.w3.org/TR/annotation-model/), [W3C PROV-O](https://www.w3.org/TR/prov-o/), [RO-Crate 1.3](https://www.researchobject.org/ro-crate/specification/1.3/index.html), and [OpenAPI 3.2](https://spec.openapis.org/oas/v3.2.0.html) — composable interchange, anchoring, provenance, packaging, and interface standards; none supplies method validity alone.
- [ATLAS.ti 26.1 update history](https://atlasti.com/updates) — current agent-operation incumbent, released 2026-06-30.
- [MAXQDA release notes](https://www.maxqda.com/products/maxqda-release-notes) and [mixed-methods functions](https://www.maxqda.com/help/mixed-methods/general) — current mixed-method workflow and joint-display incumbent.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [NIST ARIA](https://ai-challenges.nist.gov/aria), and [NSA MCP security guidance](https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf) — governance, field-testing, and agent-tool security floors.

## Freshness and Ownership

| Evidence | Owner | Expiration / refresh |
|---|---|---|
| Local coverage and contracts | Workbench | Every verified increment. |
| Producer state/schema | Producer owner plus workbench consumer | Every slice entry and producer version change. |
| Incumbent software | Evaluation owner | Six months or relevant major release, whichever is earlier. |
| Method/framework reviews | Methodological reviewer | Twelve months or material new review/standard. |
| Held-out benchmark | Independent custodian | On contamination risk, task/domain drift, or benchmark decision. |
| Public SOTA claim | Independent sign-off panel | Every release; expires when any supporting evidence expires. |

## Next Promotion

Only `T0-PROV` / coverage row W2 is presently eligible for promotion. W2 moves
from F to A only when its truthful provenance and evidence-derived inventory
pass exact controls. That bounded promotion does not close or automatically
regrade the broader T0 capability and does not change any producer, method,
mixed-methods, or SOTA row.
