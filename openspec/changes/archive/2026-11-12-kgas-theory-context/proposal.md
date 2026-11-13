## Why

Preserved KGAS theory examples cannot currently enter Workbench as inspectable, source-bound theory context. Brian approved this first integration on 2026-11-12 after the KGAS/Vision consolidation assessment.

## What Changes

- Consume a pinned KGAS v1 example through typed reference and producer views.
- Expose definitions, declared procedures, evidence requirements and limitations in the existing machine payload and study review surface.
- Provide a standalone theory review and an explicit-input calculation of the example's geometric-mean rule.
- Preserve the distinction between unverified theory context and empirical findings; refuse incompatible or corrupted input.

## Capabilities

### New Capabilities
- `kgas-theory-context`: Source-bound preserved theory context and bounded deterministic calculation.

### Modified Capabilities

## Impact

Workbench consumer, study builder, existing static page, tests and a preserved example. No upstream producer mutations, live analysis or public deployment. Native implementation plan: docs/plans/009_kgas_theory_context.md.
