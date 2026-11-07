"""Build the public, read-only PsychosisBank review artifact from validated inputs."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from mixed_methods_workbench.investigation_spine import investigation_spine_payload

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "deploy" / "psychosisbank-review" / "public"
SOURCE_HTML = ROOT / "src" / "mixed_methods_workbench" / "static" / "investigation_spine.html"
API_RELATIVE = Path("api") / "investigation" / "psychosisbank-disclosure.json"
API_PATH = PUBLIC / API_RELATIVE
BUILT_FILES = (Path("index.html"), API_RELATIVE)


def build(out_dir: Path = PUBLIC) -> Path:
    """Refuse to emit public bytes unless the full source-bound projection validates.

    Writes into ``out_dir`` (the committed ``deploy/`` folder by default) and returns it.
    Tests pass a temporary folder so they never change tracked files.
    """
    payload = investigation_spine_payload()
    if payload["connected_run"]["planning_receipt"]["human_decision"] != "withhold_causal_publication":
        raise ValueError("public review export requires the human publication block")
    api_path = out_dir / API_RELATIVE
    api_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_HTML, out_dir / "index.html")
    api_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out_dir


if __name__ == "__main__":
    build()
