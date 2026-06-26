# Mixed Methods Workbench

Planning scaffold for a future research workbench that composes
`qualitative_coding` and `process_tracing` as method engines.

Start here:

1. `PROJECT.md`
2. `docs/ARCHITECTURE.md`
3. `contracts/shared_contracts.md`
4. `docs/plans/002_engine_stability_and_integration_readiness.md`
5. `docs/IMPLEMENTING_AGENT_NOTES.md`
6. `examples/fixtures/workbench_contract_v1/README.md`
7. `docs/coverage_report.md`
8. `docs/plans/001_walking_skeleton.md`
9. `docs/CONCERNS.md`

This is not yet an implementation repo. The walking skeleton is currently
blocked by engine readiness: `qualitative_coding`, `process_tracing`, and future
`theory-forge` integration need stable export artifacts before the workbench
should build adapters or UI.

Current executable check:

```bash
make check
```

This validates only synthetic contract fixtures. It does not validate live
engine readiness.

To refresh the readiness evidence grades:

```bash
make coverage
```
