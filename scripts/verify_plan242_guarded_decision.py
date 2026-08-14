#!/usr/bin/env python3
"""Run the exact-pin Plan 242 guarded-decision checks and cold bundle replay."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

PT_PIN = "ce87f630546a9193c999943aeb3319940e89cc95"
QC_PIN = "68ac10eb3d7588bed547b89d58f0186db3f9ac85"
DATA_CONTRACTS_PIN = "d845be0c5813ab26e9bf2f1eaf4473a262ac541b"
EXPECTED_BUNDLES = 4


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pt-root", type=Path, required=True)
    parser.add_argument("--qc-root", type=Path, required=True)
    parser.add_argument("--data-contracts-root", type=Path, required=True)
    parser.add_argument(
        "--contracts-only",
        action="store_true",
        help="Run B3 contracts and native controls before C3/D3 bundles exist.",
    )
    return parser


def _head(root: Path) -> str:
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


def _require_revision(label: str, root: Path, expected: str) -> Path:
    resolved = root.resolve()
    actual = _head(resolved)
    if actual != expected:
        raise RuntimeError(f"{label} revision mismatch: expected {expected}, got {actual}")
    return resolved


def _run_tests(
    repository_root: Path,
    *,
    pt_root: Path,
    qc_root: Path,
    data_contracts_root: Path,
) -> None:
    python = pt_root / ".venv/bin/python"
    if not python.is_file():
        raise RuntimeError(f"missing pinned process_tracing interpreter: {python}")
    import_roots = (
        repository_root / "src",
        data_contracts_root / "src",
        pt_root,
        qc_root,
    )
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(str(path) for path in import_roots)
    environment["PLAN242_PT_ROOT"] = str(pt_root)
    environment["PLAN242_QC_ROOT"] = str(qc_root)
    subprocess.run(
        [
            str(python),
            "-m",
            "pytest",
            "-q",
            "tests/test_guarded_decision.py",
            "tests/test_guarded_decision_native.py",
        ],
        cwd=repository_root,
        env=environment,
        check=True,
    )


def _replay_bundles(repository_root: Path, data_contracts_root: Path) -> None:
    sys.path[:0] = [
        str(repository_root / "src"),
        str(data_contracts_root / "src"),
    ]
    from mixed_methods_workbench.guarded_decision import (
        load_evidence_bundle,
        verify_evidence_bundle,
    )

    evidence_root = repository_root / "docs/research/plan242/evidence"
    bundle_paths = sorted(evidence_root.glob("*/*/bundle.json"))
    if len(bundle_paths) != EXPECTED_BUNDLES:
        raise RuntimeError(
            f"expected {EXPECTED_BUNDLES} immutable bundles, found {len(bundle_paths)}"
        )

    def resolve_content(ref: str) -> bytes:
        candidate = Path(ref)
        if candidate.is_absolute():
            raise LookupError(f"portable evidence ref must be relative: {ref}")
        resolved = (repository_root / candidate).resolve()
        if not resolved.is_relative_to(repository_root):
            raise LookupError(f"evidence ref escapes repository: {ref}")
        try:
            return resolved.read_bytes()
        except FileNotFoundError as exc:
            raise LookupError(f"unresolved evidence ref: {ref}") from exc

    for bundle_path in bundle_paths:
        digest_path = bundle_path.with_suffix(".sha256")
        expected_digest = digest_path.read_text(encoding="utf-8").strip()
        bundle = load_evidence_bundle(bundle_path)
        verify_evidence_bundle(
            bundle,
            resolve_content=resolve_content,
            expected_bundle_digest=expected_digest,
        )
        print(f"replayed {bundle_path.relative_to(repository_root)} {expected_digest}")


def main() -> int:
    args = _parser().parse_args()
    repository_root = Path(__file__).resolve().parents[1]
    pt_root = _require_revision("process_tracing", args.pt_root, PT_PIN)
    qc_root = _require_revision("qualitative_coding", args.qc_root, QC_PIN)
    data_contracts_root = _require_revision(
        "data-contracts", args.data_contracts_root, DATA_CONTRACTS_PIN
    )
    _run_tests(
        repository_root,
        pt_root=pt_root,
        qc_root=qc_root,
        data_contracts_root=data_contracts_root,
    )
    if not args.contracts_only:
        _replay_bundles(repository_root, data_contracts_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
