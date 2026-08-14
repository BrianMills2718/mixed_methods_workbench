#!/usr/bin/env python3
"""Finalize a reviewed F1 candidate run into the strict CSS-facing ledger."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from qc_clean.core.f1_framing_review import (  # noqa: E402
    finalize_f1_bundle,
    load_coding_review,
)


def main() -> int:
    """Validate candidate/review identity and write the reviewed export."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bundle-id", required=True)
    args = parser.parse_args()
    bundle = finalize_f1_bundle(
        candidate_path=args.candidates,
        review=load_coding_review(args.review),
        bundle_id=args.bundle_id,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(bundle.model_dump_json(indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(bundle.observations)} reviewed observations to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
