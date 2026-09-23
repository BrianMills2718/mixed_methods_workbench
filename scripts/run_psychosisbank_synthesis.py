#!/usr/bin/env python3
"""Finalize the observed native PsychosisBank run into one reviewable receipt."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from mixed_methods_workbench.investigation_run import (
    RECEIPT_NAME,
    RUN_ROOT,
    generate_connected_run,
    load_connected_run,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pt-repo", required=True, type=Path)
    parser.add_argument("--pt-llm-client-root", required=True, type=Path)
    parser.add_argument("--trace-id", required=True)
    parser.add_argument("--max-budget", required=True, type=float)
    parser.add_argument("--run-root", default=RUN_ROOT, type=Path)
    args = parser.parse_args()
    if args.max_budget <= 0:
        parser.error("--max-budget must be positive")
    root = args.run_root.resolve()
    result = root / "pt-generated" / "result_blocked_prepublication.json"
    export = root / "pt-generated" / "pt_export_v2.json"
    receipt_path = root / RECEIPT_NAME
    if not result.exists():
        parser.error("native Process Tracing must complete before finalization")
    if receipt_path.exists():
        parser.error("refusing to replace a retained receipt")
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join((str(args.pt_llm_client_root), str(args.pt_repo)))
    if not export.exists():
        subprocess.run(
            [sys.executable, "-m", "pt.export", str(result), "--schema-version", "v2",
             "--output", str(export)],
            cwd=args.pt_repo,
            env=env,
            check=True,
        )
    receipt = generate_connected_run(
        trace_id=args.trace_id, max_budget=args.max_budget, root=root
    )
    receipt_path.write_text(receipt.model_dump_json(indent=2) + "\n", encoding="utf-8")
    load_connected_run(root)
    print(json.dumps({"run_id": receipt.run_id, "review_state": receipt.review_state,
                      "check_trace_id": receipt.check_trace_id,
                      "check_cost_usd": receipt.check_cost_usd}))


if __name__ == "__main__":
    main()
