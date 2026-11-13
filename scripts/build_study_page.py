"""Build a study's page and its build receipt from the study's frozen files.

Legacy trace: study_corpus/study-page (Plan #8, slice S1).

Implements: kgas-theory-context/reuse-the-study-review-surface

Requirement text (generated):
    kgas-theory-context/reuse-the-study-review-surface: The existing study builder SHALL expose
        matching machine and browser theory context, support a standalone review without fabricated
        corpus evidence, and preserve ordinary study behavior when context is absent.


    uv run python scripts/build_study_page.py examples/studies/open_science
    uv run python scripts/build_study_page.py examples/studies/open_science --serve 8765

Writes ``proposals/<study>-study/index.html`` (one self-contained page) and
``<study_dir>/build_receipt.json`` (input hashes, each step with its counts, output hash).
The build is deterministic: the same frozen files give the same bytes.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import http.server
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from mixed_methods_workbench.study_workbench import build_study_payload  # noqa: E402, RUF100

TEMPLATE = REPO / "src" / "mixed_methods_workbench" / "static" / "study_workbench.html"
PLACEHOLDER = "/*STUDY_PAYLOAD*/null"


def page_dir_for(study_id: str) -> Path:
    return REPO / "proposals" / f"{study_id.replace('_', '-')}-study"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def render(study_dir: Path) -> tuple[bytes, dict[str, Any], str]:
    payload = build_study_payload(study_dir)
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    template = TEMPLATE.read_text(encoding="utf-8")
    if PLACEHOLDER not in template:
        raise ValueError(f"{TEMPLATE} has no payload placeholder")
    page = template.replace(PLACEHOLDER, data).encode("utf-8")
    return page, payload, payload["study_id"]


def receipt_for(study_dir: Path, payload: dict[str, Any], page: bytes, page_path: Path) -> dict[str, Any]:
    inputs = sorted(
        p for p in study_dir.rglob("*") if p.is_file() and p.name != "build_receipt.json"
    )
    receipt = {
        "schema_version": "1.0",
        "record_type": "study_build_receipt",
        "study_id": payload["study_id"],
        "builder": "scripts/build_study_page.py",
        "model_calls": 0,
        "inputs": [
            {"path": str(p.relative_to(REPO)), "sha256": _sha256(p.read_bytes())} for p in inputs
        ]
        + [{"path": str(TEMPLATE.relative_to(REPO)), "sha256": _sha256(TEMPLATE.read_bytes())}],
        "steps": payload["steps"],
        "outputs": [{"path": str(page_path.relative_to(REPO)), "sha256": _sha256(page)}],
    }


    if payload.get("mode") == "theory_context":
        from mixed_methods_workbench.theory_context import TheoryCalculation

        calculation = payload["theory_context"]["calculation"]
        receipt["calculations"] = (
            [TheoryCalculation.model_validate(calculation).model_dump()]
            if calculation is not None else []
        )
        context = payload['theory_context']
        if context['source_review'] is not None:
            from mixed_methods_workbench.theory_context import SourceCounterexample
            receipt['source_appraisal'] = {
                'reference': context['source_review_reference'],
                'claims': len(context['source_review']['claims']),
                'counterexample': SourceCounterexample.model_validate(context['source_review']['counterexample']).model_dump(mode='json'),
                'kgas_result': context['counterexample_result'],
                'kgas_comparator_result': context['comparator_result'],
                'claim_limit': 'Authored agent source appraisal; no automatic or empirical theory validation',
            }
    return receipt


def build(study_dir: Path, out_dir: Path | None = None) -> tuple[Path, Path]:
    study_dir = study_dir.resolve()
    page, payload, study_id = render(study_dir)
    target_dir = out_dir or page_dir_for(study_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    page_path = target_dir / "index.html"
    page_path.write_bytes(page)
    receipt = receipt_for(study_dir, payload, page, page_dir_for(study_id) / "index.html")
    if payload.get("mode") == "theory_context":
        payload_bytes = (json.dumps(payload, ensure_ascii=False, indent=1) + "\n").encode()
        (target_dir / "payload.json").write_bytes(payload_bytes)
        receipt["outputs"].append({"path": str((page_dir_for(study_id) / "payload.json").relative_to(REPO)), "sha256": _sha256(payload_bytes)})
    receipt_path = (out_dir or study_dir) / "build_receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    return page_path, receipt_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("study_dir", type=Path)
    parser.add_argument("--serve", type=int, metavar="PORT", help="serve the page locally after building")
    args = parser.parse_args(argv)
    page_path, receipt_path = build(args.study_dir)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    for step in receipt["steps"]:
        counts = ", ".join(f"{k}={v}" for k, v in step.items() if k != "step")
        print(f"- {step['step']}: {counts}")
    print(f"page: {page_path.relative_to(REPO)} ({page_path.stat().st_size} bytes)")
    print(f"receipt: {receipt_path.relative_to(REPO)}")
    if args.serve:
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(page_path.parent))
        with http.server.ThreadingHTTPServer(("127.0.0.1", args.serve), handler) as server:
            print(f"open http://127.0.0.1:{args.serve}/ (Ctrl+C stops)")
            server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
