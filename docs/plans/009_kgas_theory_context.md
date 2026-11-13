# Plan 9 KGAS theory context

Source: Brian, 2026-11-12, "i approve", accepting the proposal to connect one preserved KGAS theory artifact to Workbench, showing construct definitions and source references, observations/assumptions, available operations and inference limits. This separately authorized optional artifact-consumption slice does not resume NYC or Vision milestone 4 and does not change Plan 8's general finish sequence.

## Outcome and existing owners

A person can build and open a Workbench review of the preserved Stakeholder Theory example, inspect the exact artifact fields, distinguish declared steps from implemented operations, and calculate its declared salience rule from supplied inputs. The artifact has no verified paper-level source anchors. Its definitions, numeric thresholds and claims of validation remain unverified source assertions.

Capability row: bounded partial `TF-SPEC` consumption in `docs/CAPABILITY_DEPENDENCY_GRAPH.md`, not `TF-RUN` or empirical method validation. KGAS owns the preserved example; Workbench owns the permissive typed artifact consumer, study payload, deterministic calculation and display. `theory-forge` remains the prospective general theory producer, with no runtime dependency introduced here.

Adoption: `wrap` the tracked `kgas1/docs/examples/stakeholder_theory_v10.json` at revision `0fb0d7873e1510091a89a8c08e7dcbe82f7b1e35`, SHA256 `dc9f2366366de704414752ed609ce36ae3e10f90b1e4c2af972071fb94df6c5b`; `extend` Workbench's existing study payload and static page. Preserve the exact bytes and origin in the consumer example. No producer code is copied or imported. This is an explicit bounded exception to deferring general theory integration until after 1.0, authorized by the conversation above.

## Contract and behavior

- A strict versioned reference identifies a confined local file, expected digest, upstream repository/revision/path. Local hashing verifies captured bytes; the origin pin records lineage rather than claiming verified scholarly authorship.
- A permissive KGAS major-version-1 consumer reads required fields and retains the full original. Unknown majors, missing required content, digest mismatch, path escape and invalid numeric inputs fail explicitly.
- Construct definitions, operationalization rules, boundary cases and declared operations carry resolvable JSON Pointers into the preserved artifact. Paper/page/quote anchors are absent and shown as absent, not manufactured.
- Required evidence and illustrative scenarios are not empirical observations. Theory context is never counted as corpus evidence or a causal result. Producer metadata such as `schema_validated` and `test_coverage` remains an attributed, unverified assertion.
- Only the preserved geometric-mean rule may execute locally on explicitly supplied finite values from zero to one. No formula is evaluated as code. Its result establishes arithmetic under that rule, not theory validity, measured stakeholder attributes or a warranted management recommendation.
- Ordinary study behavior stays compatible when theory context is absent. Standalone review needs no fabricated qualitative exports or unrelated corpus.
- Machine JSON and the existing static HTML expose the same context. A build receipt records actual inputs/hashes, steps, calculation inputs/output and produced files. Model calls: zero; no AI step or estimated AI cost.

## Scope and checks

Owned implementation: new typed consumer module, existing study payload/page builder, existing HTML, focused tests and a frozen example. Supporting edits: this plan, OpenSpec capability, reading order, consumer documentation, capability-adoption note, system model/type inventory and UI registration.

Success is one inspectable real-artifact import and calculation, supported by positive and negative tests, a deterministic build receipt, and browser observation of the resulting page. Tests must cover artifact hash/version/path refusal, exact source membership, finite numeric inputs including zero, invalid/missing input, truthful unexecuted-operation status and preserved ordinary study output. Run the relevant study tests, strict typecheck, then repository merge check. A cold review checks the changed contract and source semantics before merge.

The existing Open Science study is a compatibility control, not a new run. No live engine, LLM, graph database, source-paper reconstruction, general planner, repository archival, public deployment, empirical calibration or overall 1.0 claim is included. New public distribution would need a separate rights/privacy check.

## Progress

- [x] Inspected current architecture, owner contracts and preserved artifact; recorded source gap.
- [x] Implement typed import and exact artifact references.
- [x] Integrate machine payload and existing review surface with calculation.
- [x] Run source-bound example, failure controls, browser observation and affected checks.
- [x] Cold review and OpenSpec archive completed; repository merge and Vision result link follow the passing gate.

## Verification receipt

- Preserved input SHA256 matches the KGAS original. The build emits 13 constructs, seven declared steps and one illustrative calculation; six declared analysis steps remain unexecuted. Arithmetic result for 0.8, 0.6, 0.4 is 0.5768998281229634. The original test expectation 0.573 remains in the preserved source; it is not a gold result.
- `PYTHONPATH=src:. uv run pytest -q tests/test_theory_context.py tests/test_study_workbench.py`: 34 passed, exit 0. Real-build tests verify the calculation inputs/result/rule in the receipt and hashes of both HTML and JSON outputs.
- `uv run --extra dev make check`: exit 0; 75 pytest cases across its four groups (11 + 30 + 15 + 19), 41 fixture negative controls and three coverage negative controls passed; strict mypy passed for 21 source files. Type inventory regenerated with 230 types.
- `make docs-specs`: one capability specification passed, zero failed, exit 0. The change is archived under `openspec/changes/archive/2026-11-12-kgas-theory-context/`.
- Browser observation: source definition and calculation visible; source detail opened; all 31 source-summary tooltips visible on hover. At width 390, document scroll width was 390. Desktop screenshot inspected at 1280 by 900. Reload after adding an inline favicon produced zero console errors. This is a bounded review-page observation, not a complete product accessibility audit.
- Independent cold review initially found that the receipt omitted calculation details. After adding the validated calculation and a real-build regression assertion, the reviewer returned pass. No other material findings remained.

Build artifacts: [review page](../../proposals/kgas-stakeholder-study/index.html), [machine payload](../../proposals/kgas-stakeholder-study/payload.json), [build receipt](../../examples/theory/kgas_stakeholder/build_receipt.json). The receipt retains inputs, hashes, actual calculation and output hashes. Model calls: zero.
