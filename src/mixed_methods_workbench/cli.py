"""Agent-drivable CLI for validating and assembling the DEMO-C1 fixture journey."""

from __future__ import annotations

import argparse
from pathlib import Path

from .assemble import assemble_core_demo_review
from .io import FIXTURE_DIR, load_demo_inputs, write_review_json


def main() -> None:
    """Validate the positive-control fixture set and optionally emit its review packet."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "assemble"))
    parser.add_argument("--fixture-dir", type=Path, default=FIXTURE_DIR)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow --output to replace an existing derived review artifact.",
    )
    args = parser.parse_args()
    packet, qc_export, pt_export, gt_export, links = load_demo_inputs(args.fixture_dir)
    review = assemble_core_demo_review(packet, qc_export, pt_export, gt_export, links)
    if args.command == "validate":
        print("DEMO-C1 fixtures and review assembly passed.")
        return
    rendered = review.model_dump_json(indent=2)
    if args.output is None:
        print(rendered)
    else:
        write_review_json(args.output, rendered, force=args.force)
        print(f"Wrote DEMO-C1 review packet to {args.output}")


if __name__ == "__main__":
    main()
