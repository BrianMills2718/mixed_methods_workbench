"""Freeze a study's inputs: the published corpus and the qualitative producer's export.

Implements: study_corpus/freeze (Plan #8, slice S1).

Reads a study definition (``examples/studies/<id>/study.json``), downloads the corpus files from
the record it names, checks each against the record's published md5, and writes them unchanged
under ``source/`` with a ``corpus_manifest.json``. It then copies the qualitative producer's
grounded-theory export and the segment and document records it cites under ``qc/``, pinned by
the producer's git commit and each file's sha256.

Run once per study (network needed); everything downstream reads only the frozen files.

    uv run python scripts/freeze_study_inputs.py examples/studies/open_science/study.json \
        --qc-root ~/code2/qualitative_coding
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from mixed_methods_workbench.study_workbench import ProducerInputPin  # noqa: E402


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as response:  # noqa: S310 (fixed https host)
        data: bytes = response.read()
    return data


def freeze_corpus(study_dir: Path, study: dict[str, Any]) -> dict[str, Any]:
    source = study["source"]
    if source["kind"] != "zenodo":
        raise SystemExit(f"unsupported source kind {source['kind']!r}")
    record = json.loads(_fetch(f"https://zenodo.org/api/records/{source['record_id']}"))
    pattern = re.compile(source["document_pattern"])
    wanted = [f for f in record["files"] if pattern.match(f["key"]) or f["key"] in source["extra_files"]]
    out = study_dir / "source"
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for entry in sorted(wanted, key=lambda f: f["key"]):
        data = _fetch(entry["links"]["self"])
        algo, published = entry["checksum"].split(":", 1)
        if algo != "md5" or hashlib.md5(data).hexdigest() != published:  # noqa: S324 (matching the record)
            raise SystemExit(f"{entry['key']}: checksum differs from the record ({entry['checksum']})")
        (out / entry["key"]).write_bytes(data)
        files.append(
            {
                "name": entry["key"],
                "role": "document" if pattern.match(entry["key"]) else "supporting",
                "bytes": len(data),
                "published_md5": published,
                "sha256": _sha256(data),
            }
        )
    manifest = {
        "schema_version": "1.0",
        "record_type": "corpus_manifest",
        "study_id": study["study_id"],
        "title": record["metadata"]["title"],
        "doi": record["metadata"].get("doi", source["doi"]),
        "url": source["url"],
        "creator": source["creator"],
        "publication_date": record["metadata"]["publication_date"],
        "licence": source["licence"],
        "licence_url": source["licence_url"],
        "licence_id_in_record": record["metadata"]["license"]["id"],
        "consent_statement": source["consent_statement"],
        "retrieved_on": dt.date.today().isoformat(),
        "files": files,
    }
    (study_dir / "corpus_manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    return manifest


def freeze_qualitative(study_dir: Path, study: dict[str, Any], qc_root: Path) -> dict[str, Any]:
    producer = study["qualitative_producer"]
    out = study_dir / "qc"
    out.mkdir(parents=True, exist_ok=True)
    gt_path = qc_root / producer["theory_path"]
    state_path = qc_root / producer["project_state_path"]
    gt_bytes = gt_path.read_bytes()
    state_bytes = state_path.read_bytes()
    state = json.loads(gzip.decompress(state_bytes))

    def commit_of(path: Path) -> str:
        result = subprocess.run(
            ["git", "-C", str(qc_root), "log", "-1", "--format=%H", "--", str(path.relative_to(qc_root))],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    (out / "theory.json").write_bytes(gt_bytes)
    documents = [
        {
            "id": d["id"],
            "name": d["name"],
            "source_filename": d["metadata"]["source_filename"],
            "source_file_sha256": d["metadata"]["source_file_sha256"],
            "characters": len(d["content"]),
            "content_sha256": _sha256(d["content"].encode("utf-8")),
        }
        for d in state["corpus"]["documents"]
    ]
    segments = [
        {k: s[k] for k in ("id", "doc_id", "index", "start_char", "end_char", "speaker", "text")}
        for s in state["segments"]
    ]
    (out / "documents.json").write_text(json.dumps(documents, indent=1) + "\n", encoding="utf-8")
    (out / "segments.json").write_text(json.dumps(segments, indent=0) + "\n", encoding="utf-8")
    provenance = {
        "schema_version": "1.0",
        "record_type": "producer_input_pin",
        "producer": producer["producer"],
        "repository": producer["repository"],
        "grounded_theory": {
            "path": producer["theory_path"],
            "form": producer["theory_form"],
            "commit": commit_of(gt_path),
            "sha256": _sha256(gt_bytes),
        },
        "project_state": {
            "path": producer["project_state_path"],
            "commit": commit_of(state_path),
            "sha256": _sha256(state_bytes),
            "extracted": ["corpus.documents (without content)", "segments"],
        },
        "text_normalisation": producer["text_normalisation"],
        "pin_label": producer["pin_label"],
    }
    ProducerInputPin.model_validate(provenance)
    (out / "provenance.json").write_text(json.dumps(provenance, indent=1) + "\n", encoding="utf-8")
    return provenance


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("study", type=Path)
    parser.add_argument("--qc-root", type=Path, required=True)
    parser.add_argument("--skip-download", action="store_true", help="re-pin the producer only")
    args = parser.parse_args(argv)
    study_dir = args.study.parent
    study = json.loads(args.study.read_text(encoding="utf-8"))
    if not args.skip_download:
        manifest = freeze_corpus(study_dir, study)
        print(f"corpus: {len(manifest['files'])} files frozen, every md5 equals the record's")
    pin = freeze_qualitative(study_dir, study, args.qc_root.expanduser())
    print(f"producer: grounded theory at {pin['grounded_theory']['commit'][:10]}, state at {pin['project_state']['commit'][:10]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
