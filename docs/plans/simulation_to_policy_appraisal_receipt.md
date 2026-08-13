# Simulation-to-policy-appraisal development receipt

Observed at `2026-08-13T17:22:10Z` from Mixed Methods Workbench base
revision `f5bb0f7fa023cc589cb2635d6f18a670ada19f4c`.

## Authentic producer check

The public Cybernetic Influence comparison endpoint still returned all three
pinned runs. Recomputing SHA-256 over each complete producer row as sorted,
compact UTF-8 JSON followed by one newline matched the frozen identities:

| Run | Condition | SHA-256 result |
| --- | --- | --- |
| `run_8924342b56ce` | baseline | match |
| `run_946a10a820fc` | capacity conflict | match |
| `run_05acbaea1137` | capacity conflict plus verified allocation | match |

This check verifies retained source identity. It does not validate the
simulation as real-world evidence.

## Local critical-flow check

The existing dashboard service returned HTTP 200 for both the new browser page
and its typed JSON endpoint. The JSON retained:

- evidence origin: `model_generated`;
- conclusion: `insufficient_for_recommendation`;
- permitted use: `investigate_design_candidate`;
- all three source runs.

The page exposed the plain-language sections “What happened inside the model,”
“Why this does not select a real policy,” and “Evidence needed before a
recommendation.” The existing dashboard landing page, catalog endpoint, and
Mist Trail page remained reachable.

No browser automation runtime is installed in this checkout, so this is an
HTTP/API development checkpoint rather than a visual-browser verification
claim. A fresh-browser observation remains appropriate before deployment.
