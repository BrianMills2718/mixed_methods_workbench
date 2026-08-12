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

Reference material:

- `docs/reference/RAND_POLICY_METHODS_TAXONOMY.md` — historical 73-entry
  policy-research methods taxonomy preserved from `rand_ai_analysis`, with
  source lineage and use limits.

No implementation slice, engine integration, or product version is currently
active beyond the explicitly authorized local `METHOD-DASH-C1` review
prototype. `T0-PROV` and local `DEMO-C1` are completed bounded slices. DEMO-C1
proves typed synthetic contract behavior for separate QC, PT, and grounded-
theory-inspired lanes; it does not prove producer readiness or method validity.

## Question-first methodology dashboard

Brian authorized `METHOD-DASH-C1` on 2026-08-12 as a bounded local prototype.
It turns the methodology atlas into a researcher-facing entry point: enter a
question, select multiple analytical aims, starting point, scope, and available
evidence, then inspect several explainable method paths and a policy-research
workflow. It does not call method engines or select one universally best
method.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
make method-dashboard PYTHON=.venv/bin/python
# open http://127.0.0.1:8765
```

Focused checks:

```bash
make test-method-dashboard PYTHON=.venv/bin/python
```

Current scaffold documentation/fixture check:

```bash
make check
```

This validates the legacy fixture controls plus the DEMO-C1 typed fixtures,
assembly, strict type checks, and both-sign controls. It does not validate live
engine readiness, real producer schemas, research quality, or mixed-methods
integration.

Agent-drivable DEMO commands:

```bash
make validate-demo-fixtures
make validate-demo-controls
make assemble-demo-review
make test-demo
```

To refresh the readiness evidence grades:

```bash
make coverage
```
