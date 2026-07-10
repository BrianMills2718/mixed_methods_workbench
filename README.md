# Mixed Methods Workbench

Strategy, contracts, and planning scaffold for a broad text-centered
mixed-methods research workbench delivered through versioned thin slices.

Start here:

1. `PROJECT.md`
2. `docs/ROADMAP.md`
3. `docs/MIXED_METHODS_CAPABILITY_MAP.md`
4. `docs/plans/003_integration_versioning_and_clean_state.md`
5. `docs/ARCHITECTURE.md`
6. `contracts/shared_contracts.md`
7. `docs/coverage_report.md`
8. `docs/CONCERNS.md`

This is not yet a live workbench. Version 0.0 is truth and clean-state recovery;
version 0.1 is the first real QC/PT review slice. That slice is deliberately
labeled multi-method qualitative research. The first genuine
qualitative-quantitative mixed-methods release is planned for version 0.4.

Current executable check:

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
