# Phase 0 Type Additions

None. All types used across the 58-row Phase 0 ledger are drawn from
rev 5.1 §5.1's controlled list without modification:

`source_document, segment, code, code_system, concept, proposition, theory,
rival_explanation, diagnostic_item, evidence_item, estimate, gap,
search_query, screening_decision, review_event, option, criterion,
consequence, value_judgment, weight_set, appraisal, recommendation, claim,
claim_set, finding, memo, dataset, parameter_set, model, model_run`.

One judgment call worth recording: `consequence` (Mist Trail step .03) and
`value_judgment` (Mist Trail step .04) were kept as two distinct types
rather than collapsed, since a consequence claim (what happens under an
option) and a value judgment (how much that consequence matters) have
incompatible downstream uses per §5.1's type-collapse guardrail — collapsing
them would have let a false collision into a future comparison against
policy-appraisal-adjacent steps in other methods.
