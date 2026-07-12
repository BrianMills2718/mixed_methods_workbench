# Mixed Methods Workbench

Strategy, contracts, and planning scaffold for a broad text-centered
mixed-methods research workbench delivered through versioned thin slices.

Start here:

1. `PROJECT.md`
2. `docs/PLANNING_STATUS.md`
3. `plan/goals/2026-07-12-sota-or-beyond.md`
4. `docs/SOTA_EVIDENCE_SCORECARD.md`
5. `docs/ROADMAP.md`
6. `docs/CAPABILITY_DEPENDENCY_GRAPH.md`
7. `docs/PRE_IMPLEMENTATION_CHECKLIST.md`
8. `docs/MIXED_METHODS_CAPABILITY_MAP.md`
9. `docs/plans/current_t0_truthful_fixture_inventory.md`
10. `docs/plans/003_integration_versioning_and_clean_state.md`
11. `docs/ARCHITECTURE.md`
12. `contracts/shared_contracts.md`
13. `docs/coverage_report.md`
14. `docs/CONCERNS.md`

The current phase is documentation and planning; no implementation slice,
engine integration, or product version is active. `T0-PROV` is completed and
independently signed off for W2 inventory provenance only. It did not close or
activate version 0.0. The roadmap describes a possible future sequence:
version 0.0 would establish a trustworthy engineering baseline, version 0.1
would be the first real QC/PT review slice, and version 0.4 would be the first
genuine qualitative-quantitative mixed-methods release.

Current scaffold documentation/fixture check:

```bash
make check
```

This validates C-grade synthetic contract shapes plus the A-grade bounded
fixture-inventory controls. Current executable coverage is 1 A, 0 B, 2 C, 5 D,
and 0 F; overall D. It does not validate live engine readiness, typed producer
schemas, research quality, or mixed-methods integration.

To refresh the readiness evidence grades:

```bash
make coverage
```
