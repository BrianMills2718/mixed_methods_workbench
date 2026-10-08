#!/usr/bin/env python3
"""Fetch the pinned STATO release (Plan #6) and write its derived term list.

Downloads stato.owl for release 2026-04-20 from the OBO PURL, refuses it unless its SHA-256 matches the pin, and
writes docs/research/method_decomposition/phase4/stato_terms_2026-04-20.json: every labelled class with its id,
label, direct parents and deprecation flag. The crosswalk checks read only that derived file. `--check` exits 1 if
the committed term list differs from what the pinned release yields.
Usage: python3 scripts/fetch_stato.py [--cache DIR] [--check]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = "2026-04-20"
URL = f"http://purl.obolibrary.org/obo/stato/releases/{RELEASE}/stato.owl"
SHA256 = "7e8f945ee30c6b24139f0064d57c2edbcfc988f3f74811cad6b5c84819ce1494"
OUT = ROOT / f"docs/research/method_decomposition/phase4/stato_terms_{RELEASE}.json"
NS = {"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
      "owl": "http://www.w3.org/2002/07/owl#"}


def owl_bytes(cache: Path) -> bytes:
    path = cache / f"stato-{RELEASE}.owl"
    if not path.is_file():
        cache.mkdir(parents=True, exist_ok=True)
        path.write_bytes(urllib.request.urlopen(URL, timeout=120).read())
    raw = path.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != SHA256:
        raise SystemExit(f"STATO {RELEASE} at {path} has sha256 {got[:16]}, not the pinned {SHA256[:16]}")
    return raw


def terms(raw: bytes) -> dict:
    root = ET.fromstring(raw)
    ident = lambda iri: (m.group(1).replace("_", ":") if (m := re.search(r"/([A-Z]+_\d+)$", iri or "")) else None)
    out = {}
    for c in root.iter(f"{{{NS['owl']}}}Class"):
        tid = ident(c.get(f"{{{NS['rdf']}}}about"))
        label = c.find("rdfs:label", NS)
        if not tid or label is None or not (label.text or "").strip():
            continue
        parents = sorted({p for s in c.findall("rdfs:subClassOf", NS) if (p := ident(s.get(f"{{{NS['rdf']}}}resource")))})
        dep = c.find("owl:deprecated", NS)
        out[tid] = {"label": label.text.strip(), "parents": parents,
                    "deprecated": dep is not None and (dep.text or "").strip().lower() == "true"}
    return dict(sorted(out.items()))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", default=str(Path.home() / ".cache/mixed_methods_workbench"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    doc = {"source": URL, "release": RELEASE, "sha256": SHA256, "terms": terms(owl_bytes(Path(a.cache)))}
    text = json.dumps(doc, indent=1) + "\n"
    if a.check:
        ok = OUT.is_file() and OUT.read_text() == text
        print(f"RESULT: {'PASS' if ok else 'FAIL'} (exit {0 if ok else 1}) terms={len(doc['terms'])}")
        return 0 if ok else 1
    OUT.write_text(text)
    print(f"RESULT: PASS (exit 0) wrote {OUT.name} terms={len(doc['terms'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
