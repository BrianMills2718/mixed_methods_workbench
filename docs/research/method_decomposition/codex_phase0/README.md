# Codex Phase 0: code-derived method decomposition

Status: frozen independent candidate for later comparison with Claude

Observed: 2026-08-12

## Purpose

This is the code-first reality check for the method-decomposition and collision
exercise. It records what four observed systems actually do before idealized
methods are decomposed or shared capabilities are proposed. Across those
systems, five primary analytic variants are frozen below. `steps.yaml` contains
six workflow graphs because Process Tracing's acquisition/admission lifecycle is
modeled separately from its primary analytic workflow.

The five frozen primary variants are:

1. `qc_fixed_corpus_grounded_theory_v3` — the Open Science fixed-corpus
   grounded-theory development, expansion, appraisal, and projection path in
   Qualitative Coding.
2. `pt_single_case_rival_explanation_v2` — the current single-case,
   rival-explanation Process Tracing pipeline. Its acquisition/admission state
   machine is recorded as a companion workflow because it has a separate
   lifecycle.
3. `theory_forge_v14_compile_apply` — Theory Forge's current default
   extraction, compilation, and application path. The name is deliberately
   v14-centered: v15 reliability fields exist but are not the default
   end-to-end contract.
4. `theory_forge_cpt_choices13k_prediction` — the implemented, pinned CPT
   prediction comparison, recorded separately from the generic compiler.
5. `mist_trail_deliberative_appraisal_mtd1` — the completed Mist Trail
   policy-option appraisal fixture in Mixed Methods Workbench.

## Independence rule

This candidate was produced from repository code, fixtures, tests, and current
project authorities. Claude's decomposition and collision output was not used.
The candidates should remain separate until both Phase 0 and the five-method
pilot are frozen. Later reconciliation should compare individual steps,
signatures, edges, and implementation claims against source evidence.

## Files

- `steps.yaml` contains the normalized step inventory.
- `edges.yaml` contains branching, looping, feedback, and terminal topology.
- `reality_check.md` explains what is actually executable, merely represented,
  incomplete, or absent.
- `schema_findings.md` records what contact with the code says should change in
  the proposed row schema before the pilot.
- `comparison_rubric.md` freezes the neutral adjudication rules to use when the
  separately produced candidate becomes available.

## Interpretation rules

- A step consumes named inputs and produces named outputs that another step can
  consume.
- Workflow topology is represented separately. No method is forced to be
  linear, a DAG, or cyclic.
- `implementation_status: executable` means a callable implementation exists;
  it does not certify a fresh live LLM run.
- `implementation_status: represented_manual` means the product has a typed,
  inspectable result of a human analytical operation but does not execute that
  operation.
- `implementation_status: incomplete` means the relevant code exists but the
  normal path is not sound or fully connected.
- `method_owned_semantics` records judgment that cannot safely be inferred from
  a generic verb or signature.
- Candidate reuse is deliberately not adjudicated here.

## Frozen repository evidence

| Workflow | Repository | Revision | Working state |
| --- | --- | --- | --- |
| QC grounded theory | `/home/brian/code/qualitative_coding` | `4ea0ce6ca15a63ba91b1a3790e4737b411389902` | Clean; one remote docs-only commit behind |
| Process Tracing | `/home/brian/projects/process_tracing` | `1bf255a605d0f6f83e26b6073206ccaa46805e21` | Clean and synchronized |
| Theory Forge | `/home/brian/projects/theory-forge` | `9ec293f96b05a56115cfa4c1686ab7032fd79411` | Clean and synchronized |
| Mist Trail | `/home/brian/projects/mixed_methods_workbench` | `eb1c5df4776fcf532a045b74e00b3e47a41c4a35` | Clean; MT-D1 merged |

These revisions freeze the evidence used by this candidate. They do not make
the repositories immutable or settle later architecture.
