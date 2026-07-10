# Integration Payload Mockup

This historical mockup shows an abbreviated QC/PT payload shape. It is invented,
not evidence, and represents multi-method qualitative review rather than true
mixed methods. Version 0.1 must replace it with values from real, pinned exports.

```json
{
  "research_question": {
    "id": "rq_001",
    "text": "Why did the focal organization adopt the contested strategy?",
    "method_context": "multi_method_qualitative_review",
    "outcome_or_phenomenon": "strategy adoption",
    "scope_id": "scope_001",
    "estimand_kind": "not_applicable"
  },
  "source_scope": {
    "id": "scope_001",
    "case_or_corpus_name": "demo corpus",
    "population_or_case_universe": "loaded documents only",
    "source_selection_rule": "synthetic fixture sources for contract testing",
    "known_gaps": ["no external archival sources"],
    "claim_limits": ["workflow demonstration only"]
  },
  "evidence_records": [
    {
      "id": "ev_qc_001",
      "evidence_kind": "coded_passage",
      "description": "A coded passage supporting a qualitative claim.",
      "source_anchor_ids": ["anchor_qc_001"],
      "code_ids": ["code_001"],
      "limitations": []
    },
    {
      "id": "ev_pt_001",
      "evidence_kind": "process_trace_evidence",
      "description": "A source-grounded observation used in a likelihood vector.",
      "source_anchor_ids": ["anchor_pt_001"],
      "hypothesis_ids": ["h1", "h2", "h0_residual"],
      "limitations": ["comparative support only"]
    }
  ],
  "analytic_assertions": [
    {
      "id": "assert_qc_001",
      "assertion_kind": "qualitative_claim",
      "text": "Participants frame the strategy as defensive adaptation.",
      "estimand_kind": "interpretive_claim",
      "supporting_evidence_ids": ["ev_qc_001"],
      "status": "needs_review"
    },
    {
      "id": "assert_pt_h1",
      "assertion_kind": "causal_hypothesis",
      "text": "Leadership adopted the strategy in response to resource pressure.",
      "estimand_kind": "comparative_explanatory_support",
      "supporting_evidence_ids": ["ev_pt_001"],
      "status": "supported_within_scope"
    }
  ],
  "claim_limits": [
    "Do not report population causal effects from this payload.",
    "Do not treat qualitative claim support and process-tracing comparative support as the same metric."
  ]
}
```
