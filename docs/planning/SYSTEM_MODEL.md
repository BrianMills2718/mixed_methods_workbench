# System model: Mixed Methods Workbench

What the code stores, changes, records and shows, as of 2026-11-06 (main `bb7390f`, with Plan #8's planned
additions marked "planned"). The context graph is [context.graph.json](context.graph.json); the concepts are in
[DOMAIN.md](DOMAIN.md); every class in the code, where it is defined, what builds it and what reads it, is in
the generated [type inventory](TYPES.md) (195 classes; `pytest` fails when it is stale). [docs/ARCHITECTURE.md](../ARCHITECTURE.md) is the 2026-07 scaffold design and does
not describe the modules below (open question Q4).

## What it is

An integration authority, not a method engine. It reads exports that producer repositories
(`qualitative_coding`, `process_tracing`) write, checks them against typed consumer contracts, joins them
into review packets, and records planning and method-comparison research. It runs no server in
production; one static page is deployed.

## Stores

Everything is files in git; there is no database.

| What | Where |
| --- | --- |
| Synthetic contract fixtures (DEMO-C1) | `examples/fixtures/demo_c1/` |
| Investigation spine inputs and the independent challenge | `examples/fixtures/investigation_spine/` |
| Connected-run receipts and model-call traces | `examples/runs/` |
| Method decompositions, crosswalk and adjudication | `docs/research/method_decomposition/phase3/`, `phase4/`, `phase5/` |
| Built public review page | `deploy/psychosisbank-review/public/` |
| Study definitions, frozen corpora, producer pins, build receipts (planned, Plan #8) | `examples/studies/<study>/` |

## Changes and computes

| Module | Does |
| --- | --- |
| `src/mixed_methods_workbench/models.py`, `assemble.py`, `cli.py` | Strict producer-export models, permissive consumer views, cross-method links; assembles the DEMO-C1 review packet |
| `investigation_spine.py` | Builds the PsychosisBank investigation payload: evidence anchors, publication gate, process-tracing return |
| `investigation_run.py`, `investigation_verification.py` | Hand-run live steps: a connected run and a second-model challenge, both through `llm_client` (today the only model calls; Plan #8 S2 and S3 add the measure and integrate steps, also through `llm_client`) |
| `guarded_decision/` | Checks a decision request against bound artifacts, evidence and policy |
| `method_dashboard.py`, `method_dashboard_server.py`, `method_topology.py` | Local question-first method routing and the three-level method topology |
| `nyc_crz_*.py`, `mist_trail_decision.py`, `simulation_policy_appraisal.py` | Bounded case slices (NYC paused 2026-10-04) |
| `scripts/validate_phase3_methods.py`, `scripts/crosswalk_phase4.py`, `scripts/fetch_stato.py` | Validate the 14 decompositions; generate and check the crosswalk collisions and verdicts |
| `scripts/build_psychosisbank_public_review.py` | Copies the investigation page and payload into `deploy/` |

### Planned by Plan #8

| Slice | Type or module (planned) | Built by | Read by |
| --- | --- | --- | --- |
| S1 | `StudyDefinition`, `CorpusManifest` (`study_workbench.py`); `scripts/freeze_study_inputs.py` | the freeze script, from a study's `study.json` and the Zenodo record | `build_study_payload`, the study page builder |
| S1 | Grounded-theory view of QC's export (schema major 3), segment and document records | `read_grounded_theory` from the frozen `qc/` files | the study payload |
| S1 | Study page `proposals/<study>-study/index.html` and `build_receipt.json` | `scripts/build_study_page.py` | a person; the stale-page test |
| S2 | Feasibility readout, split manifest, measured result per measure, run receipt | the measure step (task `mixed_methods_workbench.open_science.measure`) | the measurement tab, S3 |
| S3 | Proposition-to-measure mapping, joint-display row, draft meta-inference, its number and passage check | the integrate step (task `...integrate`) and a deterministic check | the joint-display tab, S5 review |
| S4 | `pt_export_v2` reader extended with `publication_gate.publishable` | `investigation_run.py` | the causal tab |
| S5 | Investigation record (general over studies), review decision, reflexivity memo, review log, research bundle manifest | the local study workbench server | a person; the bundle |
| S6 | Benchmark record (per corpus: agreement, planted failures caught, cost, files changed) | the benchmark builder | the benchmark page |

It executes no typed rules: the models validate shapes, and the crosswalk checks verdict records; no rule
with named roles runs effects (`scripts/crosswalk_phase4.py:144`).

## Records

Run receipts with trace ids, model, tokens and cost per call (`examples/runs/*/trace_receipt.json`);
`make check` and `pytest` print counts and exit status.

## Shows

Today:

- The public PsychosisBank review page, a Cloudflare Worker serving `deploy/psychosisbank-review/public/`.
- The local method dashboard (`make method-dashboard`).
- The DEMO-C1 review packet as JSON (`make assemble-demo-review`).

Planned by Plan #8: the study page per corpus (S1–S4), the local study workbench with review and bundle
download (S5), the benchmark page (S6); where they are served is open question Q11.
