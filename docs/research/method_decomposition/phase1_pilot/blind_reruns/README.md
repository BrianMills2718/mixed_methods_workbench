# Blind audit reruns

Status: audit evidence, not the original transient lane outputs

The original Phase 1 integration reported six blind decompositions containing
90 operations, but did not preserve those reports. That historical count cannot
now be independently audited. To repair the evidence chain, six fresh read-only
lanes re-ran the decompositions from the frozen input revision `4d25074` without
reading the compact ledger or integration findings.

The final detailed reruns produced 87 operations. An earlier concise recovery
pass produced 85, so the two-operation change is itself evidence that step
granularity is not stable under blind decomposition. The controlling normalized operation inventory is in
`step_inventory.yaml`; `reconciliation.yaml` records how every operation relates
to the 70-row compact candidate, and `semantic_inventory.md` preserves each
operation's input/output and inferential boundary. These are audit reruns, not reconstructions of
the unavailable originals. Differences from the historical counts are evidence
about decomposition instability and must not be represented as errors that were
silently corrected.

## Rerun summaries

| Method | Operations | Controlling sources | Main topology or boundary |
| --- | ---: | --- | --- |
| Systematic review | 15 | Cochrane Handbook 6.5.1; PRISMA 2020 | Prespecified review with conditional pooling and bounded search returns |
| Constructivist grounded theory | 14 | Charmaz, third edition; Charmaz 2020 | Coding, comparison, memoing, theoretical sampling, and refinement cycles |
| Theory-testing process tracing | 13 | Beach and Pedersen 2019; Fairfield and Charman 2022 | Rival-relative appraisal with evidence-acquisition returns and refusal |
| RCT causal-effect estimation | 14 | ICH E9/E9(R1); CONSORT 2025 | Prespecified randomized DAG; outcome-informed redesign is prohibited |
| Policy option appraisal | 15 | HM Treasury Green Book 2026; MCDA manual | Branching appraisal, explicit value boundaries, decision boundary, feedback |
| Agent-based policy simulation | 16 | ODD; JRC uncertainty and sensitivity guidance | Specification, code verification, empirical fitness, ensemble experiment, sensitivity, refusal |

The full lane responses were normalized rather than copied as unstructured
prose. The normalization preserves each operation's ID, label, inputs, outputs,
method-owned boundary, refusal, ordered topology, and stated uncertainties. It
does not claim byte-for-byte preservation of the chat response.
