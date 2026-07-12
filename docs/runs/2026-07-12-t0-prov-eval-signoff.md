# T0-PROV Independent Evaluation Sign-Off

Decision date: 2026-07-12

Evaluated commit: `f26bc6ade93c475c7ebc4ca608e796a9b9fe2f1a`

Decision: **SIGNED-OFF**

Scope: `T0-PROV` / legacy coverage row `W2-fixture-inventory` only

## Licensed Claim

The current synthetic fixture directory has an exhaustive, truthful,
Git-recoverable provenance inventory. The bounded W2 row is A/test because the
positive evidence and discriminating controls pass at the evaluated commit.

This decision does **not** promote fixture contents above C, close broader
T0/0.0, establish producer readiness or method validity, license a
mixed-methods claim, change the program score, or support a SOTA claim.

## Independence and Execution

A fresh evaluator with rejection authority used a clean detached clone at
`/tmp/mmw-signoff-f26-NVyGd4/repo`, pinned to the full commit above. It did not
edit the target repository and did not trust tracked reports without
re-deriving and comparing them.

Executed positive surfaces:

```bash
make check
make coverage
make coverage-json
```

The evaluator also independently compared recursive case-insensitive JSON
discovery with the manifest; ran `git log`, `git show`, SHA-256, and byte
comparisons for all four fixtures; captured JSON and Markdown transports; and
confirmed the detached checkout remained clean.

## Gate Results

| Gate | Result | Evidence |
|---|---|---|
| Validity | PASS | Positive gates passed; JSON/Markdown matched tracked reports and made no changes. |
| Representativeness | PASS | 41 independent hostile checks covered inventory, path, parser, claim, time, evidence, transport, recovery, and containment classes. |
| Diagnosis | PASS | The previously rejected root-symlink class is blocked before traversal with its exact diagnostic. |
| Generalization | PASS | Root, interior-directory, file, and broken symlinks failed; other hostile classes and the positive path did not regress. |
| Decision integrity | PASS | Invalid evidence rendered complete W2/overall F reports while `make check` failed; stale reports failed without rewrite; apparatus tampering failed. |

Held-outs included root/nested/case-variant/dotfile JSON-like artifacts;
root/interior/file/broken symlinks; duplicate keys; malformed and invalid-UTF-8
JSON; non-first entries; alternate or unknown claims; purpose/replacement
escalation; old, future, and timezone-naive timestamps; fixture, validator,
control, and evidence-deriver tampering; evidence removal; stale reports;
transport purity; exact Git recovery; and grade containment.

## Exact Containment Readout

- `W2-fixture-inventory`: A/test.
- `W1-contract-stub` and `W3-real-synthesis-payload`: C.
- Five legacy scaffold rows: D.
- Legacy scaffold coverage: 1 A, 0 B, 2 C, 5 D, 0 F; overall D.
- Every manifest fixture grade: `C-synthetic-contract-only`.
- Broader T0 and the full program scorecard: still F.

## Immutable Evidence Boundary

This sign-off applies only to the exact evaluated commit. Later documentation
commits may record the decision, but any change to the evaluated Makefile,
validator, controls, coverage deriver, manifest, fixture directory, or
generated report evidence requires a new evaluation before reusing this
decision.
