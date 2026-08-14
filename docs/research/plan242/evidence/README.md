# Plan 242 Registration @3 Evidence

These immutable bundles test a Workbench-local custody and replay seam. They do
not promote a shared Data Contracts capability, establish H3, or make either
method's native state subordinate to Workbench.

| Consumer case | Bundle digest |
| --- | --- |
| process_tracing positive | `sha256:091b0696404c56666b33bd271b06ecf5ccf862c0c936abe5221e502f3c7d5ad1` |
| process_tracing refusal | `sha256:5dcd3e4b4fc7bccba8a1c0e9fd0c2faf8480a4d04060eb85656d243195df26bc` |
| qualitative_coding positive | `sha256:7a62ba01d260028bd7b047bf18397bcc8ead573870db3d4a0a3093be075ee22e` |
| qualitative_coding refusal | `sha256:f5cc8c10ec015c1c7f828cbbd463267d0c88e4c437c429fd983cf532b5524900` |

The PT positive binds retained SQLite call 4, trace
`plan242-d/pt-partition-ce87f630-20260814-b`, and `llm_client` runtime
`16b9eb19ae6402c23271ee8384c0508dce0f5acd`. Replay performs no model call.
The QC positive retains native reviewed-bundle SHA-256
`c135da965f0fa61da85aa49008c7fe93711368ac8422c5c83816c69a0346934f`,
`scientific_review_status=not_performed`, and no raw source content.

Run the exact-pin verifier from the repository root:

```bash
.venv/bin/python scripts/verify_plan242_guarded_decision.py \
  --pt-root /path/to/process_tracing-at-ce87f630 \
  --qc-root /path/to/qualitative_coding-at-68ac10eb \
  --data-contracts-root /path/to/data-contracts-at-d845be0c \
  --llm-client-root /path/to/llm_client-at-16b9eb19
```

The paths are invocation inputs only; no personal absolute path is stored in a
portable bundle.
