# Plan #7: keep the workbench shippable and its public page current

Status: proposed 2026-11-06 by agent; the default of open question Q1 (no new workbench capability until
Brian picks a direction).

Planning package: docs/planning/planning-package.json

## Why

The Plan #6 crosswalk is done and found no `same_capability` group, and the NYC lane is paused. What the
open questions call for is upkeep: the repository could not build or pass `make check` until 2026-11-06,
the public page lags the renderer, a test writes into tracked files, and the documentation checks fail.

## Steps

1. Q5: after pull request #57 merges, deploy `deploy/psychosisbank-review` with wrangler and confirm the
   served `index.html` matches the committed one byte for byte.
2. Q6: make `build()` take an output folder; the test builds into `tmp_path`.
3. Q2: add `.agentic/repo.yaml` naming the canonical documents; rerun the durable-documents check.
4. Q3 and Q4: link the canonical documents and `docs/planning/SYSTEM_MODEL.md` from `wiki/index.md`, mark
   `docs/ARCHITECTURE.md` as design history, and declare a cap exception for the frozen research records.
5. Rebuild this planning package from the new revision.

## Relies on

`publication_gate`, `review_packet`, `method_decomposition`, `producer_export`, `workbench_view`
(see `docs/planning/DOMAIN.md`).

## Cost

No AI steps: every step is a file change, a deploy or a deterministic check.

## Done when

`make check` and `pytest` exit 0 with a clean tree afterwards; the live page hash equals the committed
page; durable-documents and wiki checks exit 0 or their remaining findings are tracked questions.
