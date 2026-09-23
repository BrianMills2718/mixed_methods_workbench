from __future__ import annotations

import json
from pathlib import Path

from scripts.build_psychosisbank_public_review import API_PATH, PUBLIC, build


def test_public_review_export_preserves_governed_decision() -> None:
    build()
    payload = json.loads(API_PATH.read_text(encoding="utf-8"))
    assert (PUBLIC / "index.html").is_file()
    assert payload["title"] == "Why did PsychosisBank use controlled access?"
    receipt = payload["connected_run"]["planning_receipt"]
    assert receipt["human_decision"] == "withhold_causal_publication"
    assert receipt["terminal_review_state"] == "withhold_causal_publication_pending_human_review"
