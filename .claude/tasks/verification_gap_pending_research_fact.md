# Pending Shared Verification-Gap Entry: Unreproduced Research Fact

Date: 2026-07-12
Target corpus: `~/projects/project-meta/verification_gap_log.md`
Status: pending because active coordination claim
`codex_project-meta_plan0137-report-vgap-20260712` exclusively names the shared
log; do not append until that claim completes or is explicitly released

## Log entry to append

## 2026-07-12 — mixed_methods_workbench — verified-by-proxy / self-reported research observation

**Declared:** Both decision-research lanes were presented as complete and the
governance report as structurally checked; its high-confidence local facts were
then used in the parent synthesis.

**Audit found:** `.claude/tasks/research_gov_case_options.md` claimed the tracked
Brumaire packet contained an exact duplicated Murat/Orangerie sentence.
`awk 'NF {print}' "$packet" | sort | uniq -d | wc -l` returned `0`, and
`rg -i -o "deputies had been dissolved" "$packet" | wc -l` returned `1`.
The report was corrected to state the negative result and require deliberately
planted exact/near-duplicate controls.

**Verification gap:** The evidence held was the researcher's completed report,
its source list, and structural/link checks. The dispositive evidence skipped
was parent re-execution of each deterministic local observation that supplied
a factual premise or negative-control rationale.

**General failure mode:** verified-by-proxy / self-reported research observation
— a sourced research report can be structurally complete while one claimed
filesystem measurement is false; synthesis transfers the error when the parent
checks citations but does not reproduce deterministic claims.

**Prevention:** Before calling research complete or synthesizing it, maintain a
fact-check ledger for every pivotal deterministic local observation and
re-execute its exact command against the named bytes. Negative-control
rationales must distinguish observed defects from deliberately planted
mutations.

## Policy-promotion disposition

This is another `verified-by-proxy` recurrence. Existing log entries and policy
proposals already cover replacing proxy evidence with direct execution, so no
duplicate policy proposal is recommended. The useful project-specific addition
is the fact-check ledger at the research-to-synthesis boundary.
