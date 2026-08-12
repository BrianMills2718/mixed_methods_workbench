"""Focused contract, corruption, and presentation checks for MT-D1."""

from __future__ import annotations

import json
from http import HTTPStatus
from pathlib import Path

import pytest
from pydantic import ValidationError

from mixed_methods_workbench import mist_trail_decision as fixture_module
from mixed_methods_workbench.method_dashboard_server import mist_trail_payload
from mixed_methods_workbench.mist_trail_decision import (
    DECISION_PACKET_PATH,
    DecisionPacket,
    load_mist_trail_decision,
)

HTML_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "mixed_methods_workbench"
    / "static"
    / "mist_trail_decision.html"
)


def _packet_dict() -> dict[str, object]:
    return json.loads(DECISION_PACKET_PATH.read_text(encoding="utf-8"))


def test_source_bound_packet_covers_every_option_and_criterion() -> None:
    """The positive fixture is complete, conditional, value-sensitive, and evidence-limited."""
    artifact = load_mist_trail_decision()
    packet = artifact.packet
    assert [option.option_id for option in packet.options] == ["A", "B", "C"]
    assert len(packet.criteria) == 6
    assert len(packet.consequence_assessments) == 18
    assert packet.conclusion.state == "conditional_recommendation"
    assert packet.conclusion.basis == "workbench_appraisal"
    assert set(packet.conclusion.sensitivity_statuses) == {
        "value_sensitive",
        "evidence_limited",
    }
    assert [lens.preferred_option_id for lens in packet.priority_lenses] == ["C", "B", None]
    assert all(anchor.passage_status == "passage_unavailable" for anchor in packet.source_anchors)


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "substituted"])
def test_official_option_identity_corruptions_fail(mutation: str) -> None:
    """A, B, and C cannot disappear, duplicate, or be replaced by an invented option."""
    payload = _packet_dict()
    options = payload["options"]
    assert isinstance(options, list)
    if mutation == "missing":
        options.pop()
    elif mutation == "duplicate":
        options[2]["option_id"] = "B"
    else:
        options[2]["option_id"] = "D"
    with pytest.raises(ValidationError):
        DecisionPacket.model_validate(payload)


def test_common_action_cannot_be_misattributed_to_one_option() -> None:
    """Actions common to B and C remain common in the typed packet."""
    payload = _packet_dict()
    payload["common_actions"][0]["applies_to_option_ids"] = ["C"]
    with pytest.raises(ValidationError, match="must apply to both B and C"):
        DecisionPacket.model_validate(payload)


def test_unknown_source_anchor_fails_loud() -> None:
    """A consequence may expose a gap, but it may not cite a nonexistent source window."""
    payload = _packet_dict()
    payload["consequence_assessments"][0]["source_anchor_ids"] = ["invented-anchor"]
    with pytest.raises(ValidationError, match="unknown source anchor"):
        DecisionPacket.model_validate(payload)


def test_agency_preference_cannot_replace_workbench_appraisal() -> None:
    """The NPS proposed-action label is not a valid conclusion basis."""
    payload = _packet_dict()
    payload["conclusion"]["basis"] = "agency_proposed_action"
    with pytest.raises(ValidationError):
        DecisionPacket.model_validate(payload)


def test_missing_human_judgment_blocks_a_recommendation() -> None:
    """Every visible criterion needs an explicit human judgment."""
    payload = _packet_dict()
    payload["criterion_judgments"].pop()
    with pytest.raises(ValidationError, match="every criterion needs exactly one"):
        DecisionPacket.model_validate(payload)


def test_manifest_hash_corruption_fails_before_serving(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The API cannot silently serve a packet bound to different source metadata."""
    payload = _packet_dict()
    payload["source_manifest_sha256"] = "0" * 64
    corrupt_path = tmp_path / "decision_packet.json"
    corrupt_path.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(fixture_module, "DECISION_PACKET_PATH", corrupt_path)
    with pytest.raises(ValueError, match="source-manifest hash"):
        fixture_module.load_mist_trail_decision()


def test_unverified_passage_rendering_fails_before_serving(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Changing a passage status cannot make absent source bytes renderable."""
    payload = _packet_dict()
    payload["source_anchors"][0]["passage_status"] = "hash_verified"
    altered_path = tmp_path / "decision_packet.json"
    altered_path.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(fixture_module, "DECISION_PACKET_PATH", altered_path)
    with pytest.raises(ValueError, match="exact passages cannot render"):
        fixture_module.load_mist_trail_decision()


def test_api_and_browser_use_the_same_typed_artifact() -> None:
    """The browser has no embedded decision result that can drift from the JSON route."""
    payload = mist_trail_payload()
    assert payload == load_mist_trail_decision().model_dump(mode="json")
    assert payload["packet"]["conclusion"]["headline"] not in HTML_PATH.read_text(encoding="utf-8")


def test_browser_copy_explains_identity_result_limits_and_action() -> None:
    """A cold visitor receives a usable mental model before internal provenance."""
    html = HTML_PATH.read_text(encoding="utf-8")
    assert "Development example — not an NPS decision" in html
    assert "Which Mist Trail rehabilitation option best fits the priorities?" in html
    assert "Official Draft EA" in html
    assert "Change the priority; watch the answer change" in html
    assert "What this review cannot establish" in html
    assert "Exact passage unavailable" in html
    assert "Source identity, custody, and internal references" in html
    assert "/api/decision/mist-trail" in html


def test_decision_routes_are_declared_on_the_existing_dashboard_handler() -> None:
    """Keep the example in the existing service rather than creating another UI host."""
    server_source = (
        Path(fixture_module.__file__)
        .with_name("method_dashboard_server.py")
        .read_text(encoding="utf-8")
    )
    assert '"/decision/mist-trail"' in server_source
    assert '"/api/decision/mist-trail"' in server_source
    assert HTTPStatus.OK == 200
