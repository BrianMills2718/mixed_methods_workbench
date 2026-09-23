"""Build the public, read-only PsychosisBank review artifact from validated inputs."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from mixed_methods_workbench.investigation_spine import investigation_spine_payload

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "deploy" / "psychosisbank-review" / "public"
SOURCE_HTML = ROOT / "src" / "mixed_methods_workbench" / "static" / "investigation_spine.html"
API_PATH = PUBLIC / "api" / "investigation" / "psychosisbank-disclosure.json"


def build() -> None:
    """Refuse to emit public bytes unless the full source-bound projection validates."""
    payload = investigation_spine_payload()
    if payload["connected_run"]["planning_receipt"]["human_decision"] != "withhold_causal_publication":
        raise ValueError("public review export requires the human publication block")
    PUBLIC.mkdir(parents=True, exist_ok=True)
    API_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_HTML, PUBLIC / "index.html")
    API_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
