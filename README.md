# Mixed Methods Workbench

Strategy, contracts, and planning scaffold for a broad text-centered
mixed-methods research workbench delivered through versioned thin slices.

Start here:

1. `PROJECT.md`
2. `docs/PLANNING_STATUS.md`
3. `docs/ROADMAP.md`
4. `docs/CAPABILITY_DEPENDENCY_GRAPH.md`
5. `docs/PRE_IMPLEMENTATION_CHECKLIST.md`
6. `docs/MIXED_METHODS_CAPABILITY_MAP.md`
7. `docs/plans/003_integration_versioning_and_clean_state.md`
8. `docs/ARCHITECTURE.md`
9. `contracts/shared_contracts.md`
10. `docs/coverage_report.md`
11. `docs/CONCERNS.md`

The current phase is documentation and planning only. No implementation version
is active or authorized. The roadmap describes a possible future sequence:
version 0.0 would establish a trustworthy engineering baseline, version 0.1
would be the first real QC/PT review slice, and version 0.4 would be the first
genuine qualitative-quantitative mixed-methods release.

Current scaffold documentation/fixture check:

```bash
make check
```

This validates only a synthetic contract shape and discriminating controls. It
does not validate live engine readiness, typed producer schemas, research
quality, or mixed-methods integration.

To refresh the readiness evidence grades:

```bash
make coverage
```
