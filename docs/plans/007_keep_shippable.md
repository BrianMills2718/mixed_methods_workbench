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
   served `index.html` matches the committed one byte for byte. **Done 2026-11-06:** Worker version
   `e46676f3`; served and committed `index.html` both sha256 `eae2c256…0231`, payload both `7ff58b07…92d0`.
2. Q6 and Q9: make `build()` take an output folder; the test builds into `tmp_path` and fails when the
   committed `deploy/` page or payload differs from what `build()` produces, so a renderer change without a
   rebuild is caught by `pytest` instead of silently dirtying the checkout. **Done 2026-11-06:**
   `build(out_dir)` and `test_committed_deploy_page_matches_renderer`; a one-line change to the page source
   made the test fail with "deploy/ is stale for ['index.html']".
3. Q9: record in `deploy/psychosisbank-review/` (README) that every merge touching `deploy/` is followed by a
   wrangler deploy and a hash comparison of the served page; deploys stay manual (no hosted CI).
4. Q10: relabel the NYC findings in `src/mixed_methods_workbench/static/investigation_spine.html` as
   blanket-approved, not item-reviewed, and rebuild `deploy/`.
5. Q2: add `.agentic/repo.yaml` naming the canonical documents; rerun the durable-documents check.
6. Q3 and Q4: declare the canonical documents and `docs/planning/SYSTEM_MODEL.md`, regenerate `wiki/index.md` with
   project-meta's `generate_wiki_routing_stub.py` (it is generated, not hand-edited), mark
   `docs/ARCHITECTURE.md` as design history, and declare a cap exception for the frozen research records.
7. Rebuild this planning package from the new revision.

## Relies on

`public_review`, `publication_gate`, `method_decomposition`, `producer_export`, `workbench_view`
(see `docs/planning/DOMAIN.md`).

## Cost

No AI steps: every step is a file change, a deploy or a deterministic check.

## Done when

`make check` and `pytest` exit 0 with a clean tree afterwards; `pytest` fails on a stale `deploy/` page; the
live page hash equals the committed page; durable-documents and wiki checks exit 0 or their remaining findings are tracked questions.
