from __future__ import annotations

import json
from pathlib import Path

from scripts.build_psychosisbank_public_review import API_RELATIVE, BUILT_FILES, PUBLIC, build


def test_public_review_export_preserves_governed_decision(tmp_path: Path) -> None:
    out = build(tmp_path)
    payload = json.loads((out / API_RELATIVE).read_text(encoding="utf-8"))
    assert (out / "index.html").is_file()
    assert payload["title"] == "Why did PsychosisBank use controlled access?"
    receipt = payload["connected_run"]["planning_receipt"]
    assert receipt["human_decision"] == "withhold_causal_publication"
    assert receipt["terminal_review_state"] == "withhold_causal_publication_pending_human_review"


def test_committed_deploy_page_matches_renderer(tmp_path: Path) -> None:
    """A renderer or payload change without `python scripts/build_psychosisbank_public_review.py` fails here."""
    out = build(tmp_path)
    stale = [str(rel) for rel in BUILT_FILES if (out / rel).read_bytes() != (PUBLIC / rel).read_bytes()]
    assert not stale, f"deploy/ is stale for {stale}: rebuild, commit, then wrangler deploy"
