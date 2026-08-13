import shutil

import pytest
import yaml

from scripts.validate_phase1_revision import REVISION, validate_revision


def test_phase1_revision_candidate_is_complete_and_bounded() -> None:
    validate_revision()


def test_exact_anchor_alias_is_rejected(tmp_path) -> None:
    candidate = tmp_path / "phase1_revision"
    shutil.copytree(REVISION, candidate)
    path = candidate / "method_records.yaml"
    records = yaml.safe_load(path.read_text(encoding="utf-8"))
    records["methods"][0]["moves"][0]["exact_anchors"] = ["gap:noncanonical-alias"]
    path.write_text(yaml.safe_dump(records, sort_keys=False), encoding="utf-8")

    with pytest.raises(AssertionError):
        validate_revision(candidate)
