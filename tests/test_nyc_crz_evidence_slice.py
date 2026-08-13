"""Focused evidence for the first authentic NYC extraction capability slice."""

from __future__ import annotations

import hashlib
import json
import shutil
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

from mixed_methods_workbench.method_dashboard_server import MethodDashboardHandler
from mixed_methods_workbench.nyc_crz_evidence_slice import (
    EXPECTED_FIXTURE_DIGESTS,
    FIXTURE_ROOT,
    NycCrzEvidenceSliceError,
    load_nyc_crz_evidence_slice,
    load_vehicle_aggregate,
    nyc_crz_evidence_slice_payload,
    verify_source_document,
)

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "src" / "mixed_methods_workbench" / "static" / "investigation_spine.html"
DASHBOARD_PATH = HTML_PATH.with_name("method_dashboard.html")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _mutable_fixtures(tmp_path: Path) -> Path:
    target = tmp_path / "nyc_crz_evidence_slice"
    shutil.copytree(FIXTURE_ROOT, target)
    return target


def _rewrite_json(path: Path, payload: object) -> str:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return _sha256(path)


def test_slice_exposes_structural_capabilities_without_accepting_analysis() -> None:
    evidence = load_nyc_crz_evidence_slice()

    assert evidence.status == "candidate_review_required"
    assert evidence.review_packet.review.status == "pending_human_review"
    assert [item.status for item in evidence.review_packet.review.field_dispositions] == [
        "rejected",
        "rejected",
    ]
    assert evidence.capability_flow == [
        "verify exact source bytes",
        "extract typed candidates from bounded text",
        "bind each quote uniquely to its source unit",
        "require attributable human review",
        "hand accepted records to method-owned analysis",
    ]
    assert all(document.exact_byte_verified for document in evidence.source_documents)
    assert evidence.run_receipt.cache_hit is False
    assert evidence.run_receipt.attempts[0].disposition == "rejected_anchor_binding"
    assert evidence.run_receipt.attempts[-1].disposition == "retained_pending_human_review"


def test_changed_source_byte_is_refused_before_parsing(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    source.write_bytes(b"%PDF-authentic-source")
    expected = _sha256(source)
    source.write_bytes(b"%PDF-authentic-sourcf")

    with pytest.raises(NycCrzEvidenceSliceError, match="source digest mismatch"):
        verify_source_document(
            source,
            expected_sha256=expected,
            expected_bytes=source.stat().st_size,
        )


def test_fixture_digest_mutation_fails_loud(tmp_path: Path) -> None:
    fixtures = _mutable_fixtures(tmp_path)
    path = fixtures / "candidate_extraction.json"
    path.write_bytes(path.read_bytes() + b"\n")

    with pytest.raises(NycCrzEvidenceSliceError, match="artifact digest mismatch"):
        load_nyc_crz_evidence_slice(fixtures)


def test_quote_must_bind_uniquely_to_declared_source_unit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixtures = _mutable_fixtures(tmp_path)
    path = fixtures / "source_units.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["anchors"][0]["selected_text"] = "a quote absent from its source unit"
    payload["anchors"][0]["selected_text_sha256"] = hashlib.sha256(
        payload["anchors"][0]["selected_text"].encode("utf-8")
    ).hexdigest()
    monkeypatch.setitem(EXPECTED_FIXTURE_DIGESTS, path.name, _rewrite_json(path, payload))

    with pytest.raises(NycCrzEvidenceSliceError, match="selected_text_must_bind_uniquely"):
        load_nyc_crz_evidence_slice(fixtures)


def test_acceptance_without_attributable_human_decision_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixtures = _mutable_fixtures(tmp_path)
    path = fixtures / "review_packet.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["review"]["status"] = "accepted"
    monkeypatch.setitem(EXPECTED_FIXTURE_DIGESTS, path.name, _rewrite_json(path, payload))

    with pytest.raises(
        NycCrzEvidenceSliceError,
        match="accepted_candidate_requires_attributable_human_decision",
    ):
        load_nyc_crz_evidence_slice(fixtures)


def test_frozen_vehicle_aggregate_is_descriptive_and_reproducible() -> None:
    aggregate = load_vehicle_aggregate()

    assert aggregate.observed_days == 361
    assert aggregate.crz_entries == 178_203_234
    assert aggregate.excluded_roadway_entries == 23_461_361
    assert aggregate.mean_daily_crz_entries == pytest.approx(493_637.7673130194)
    assert "not a causal effect" in aggregate.permitted_claim


def test_nyc_and_psychosisbank_share_one_browser_surface_and_typed_api() -> None:
    payload = nyc_crz_evidence_slice_payload()
    html = HTML_PATH.read_text(encoding="utf-8")
    dashboard = DASHBOARD_PATH.read_text(encoding="utf-8")

    assert payload["schema_version"] == "mmw.nyc_crz_evidence_slice.v0.1"
    assert "/api/investigation/nyc-congestion-relief-zone" in html
    assert "/api/investigation/psychosisbank-disclosure" in html
    assert "Validation is not interpretation." in html
    assert "/investigation/nyc-congestion-relief-zone" in dashboard
    assert "/investigation/psychosisbank-disclosure" in dashboard


def test_server_exposes_matching_nyc_html_and_json_routes() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 0), MethodDashboardHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        with urllib.request.urlopen(
            base + "/investigation/nyc-congestion-relief-zone"
        ) as response:
            html = response.read().decode("utf-8")
            assert response.headers.get_content_type() == "text/html"
            assert "renderNyc" in html
        with urllib.request.urlopen(
            base + "/api/investigation/nyc-congestion-relief-zone"
        ) as response:
            payload = json.loads(response.read())
            assert response.headers.get_content_type() == "application/json"
            assert payload["status"] == "candidate_review_required"
            assert payload["review_packet"]["review"]["status"] == "pending_human_review"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
