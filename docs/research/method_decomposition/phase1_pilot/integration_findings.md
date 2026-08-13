# Independent-lane integration findings

Input revision: `4d25074`

Status: unresolved discovery comparison; not collision-ready

The original six read-only lanes were reported as independently proposing 90
operations, but their transient reports were not preserved. That count is now
historical and unverified. Six fresh read-only audit reruns used the same frozen
revision without reading the compact candidate. An initial concise recovery
produced 85 operations; the final detailed recovery produced 87. The 70-row
compact candidate remains unresolved. The 17-row difference, the three-operation
difference from the historical claim, and the two-operation change between audit
passes are evidence of unstable granularity rather than agent noise.

| Method | Audit-rerun operations | Compact rows | Main compression disagreement |
| --- | ---: | ---: | --- |
| Systematic review | 15 | 12 | search design/execution, record identity, study-flow accounting, compatibility, interpretation, and reporting |
| Grounded theory | 14 | 12 | segmentation, category refinement, memo sorting, adequacy, and reflexive integration |
| Process tracing | 13 | 12 | antecedent likelihood expectations, exact anchored extraction, dependence review, mechanism account, and dual terminal outcomes |
| RCT estimation | 14 | 12 | objective/estimand separation, outcome ascertainment, conduct audit, auxiliary inference, and reporting |
| Policy appraisal | 15 | 12 | counterfactual, option characterization, social-value aggregation, comparative judgment, and decision feedback |
| Agent-based simulation | 16 | 10 | implementation, empirical fitness, uncertainty design, two sensitivity forms, and refusal gate |

## Accepted findings represented in the candidate

- Each variant is frozen rather than inferred from a family label.
- Directed topology, optional and required returns, prohibited cycles, refusal,
  supported conclusions, method-owned semantics, and source basis are explicit.
- `analysis_plan` is used instead of misusing `review_protocol` for trial and
  evaluation plans.
- The graph-level integration notes preserve the generated/observed boundary,
  trial prespecification barrier, appraisal authority boundary, process-tracing
  temporal distinctions, grounded-theory reflexivity, and review refusal paths.
- The compact rows remain a candidate for testing granularity, not the
  controlling decomposition.

## Findings deliberately not normalized into the 70 rows

These are retained as open schema findings instead of being silently squeezed
into the current controlled lists:

- `decision` distinct from analyst `recommendation`;
- authority/evidence/control input roles distinct from subject/context/criteria;
- `research_question`, `sampling_plan`, `comparison_record`, and reflexive
  relationships in grounded theory;
- `refusal_event` or claim-status downgrade distinct from runtime failure;
- a first-class prespecification barrier carrying time and information-access
  provenance;
- report, study, result, randomized assignment, treatment received, and
  intercurrent-event identities;
- output epistemic origin such as observed, elicited, derived, and simulated;
- versioned feedback that starts a new analytic run rather than rewriting a
  prior result.

Adopting all of these after one pilot would be premature. Omitting them without
this record would be misleading.

## Integration decisions

1. **Do not choose 70, 85, 87, or the historical 90 as the correct granularity.**
   The audit-rerun inventory and row-level reconciliation are now durable. The
   compact candidate is structurally checkable but collision-blocked.
2. **Do not run collision grouping yet.** Signature counts would be materially
   altered by unresolved splits, roles, and types.
3. **Keep method-owned validity rules intact.** Similar verbs such as `screen`,
   `test`, and `compare` do not resolve these differences.
4. **Use the hostile simulation result as a counterexample, not a sixth vote.**
   It disproves document-first evidence and flat-validation assumptions.
5. **Take the smallest next decision at the portfolio gate.** Human review must
   decide whether to revise the row model using these stresses before selecting
   the broader Phase 3 method set.

## Uncertainties

- The book-based lanes had chapter-level rather than page-complete access.
- The process-tracing frame intentionally combines Beach–Pedersen mechanism
  work with Fairfield–Charman Bayesian rival comparison; it is not a claim that
  they are one methodology.
- The RCT sources come from clinical-trial guidance applied to an
  administrative-policy intervention; the randomized warrant transfers, while
  domain-specific operational constraints require separate authority.
- Green Book appraisal is used as a methodological frame, not a claim that its
  institutional rules legally govern the regional example.

The controlling audit evidence is `blind_reruns/step_inventory.yaml` and its
row-level disposition is `blind_reruns/reconciliation.yaml`. The missing and
non-data-carrying graph transitions are recorded in `structural_gaps.yaml`.
That file also records a source-scope mismatch: compact row `sr.11` relies on
Cochrane chapters 13-14 even though the frozen source scope is chapters 1-10.
