"""Plan #8 slice S1: the frozen Open Science corpus and Qualitative Coding's strand."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from pydantic import ValidationError

from mixed_methods_workbench.study_workbench import (
    UnsupportedProducerSchema,
    anchor_text,
    build_study_payload,
    chance_reading,
    read_grounded_theory,
)
from scripts.build_study_page import build, page_dir_for, render

REPO = Path(__file__).resolve().parents[1]
STUDY = REPO / "examples" / "studies" / "open_science"


@pytest.fixture(scope="module")
def payload() -> dict:
    return build_study_payload(STUDY)


def _step(payload: dict, words: str) -> dict:
    return next(s for s in payload["steps"] if words in s["step"])


def test_every_frozen_file_matches_the_publisher(payload: dict) -> None:
    step = _step(payload, "publisher's md5")
    assert step["files"] == 28
    assert step["md5_matches"] == step["sha256_matches"] == 28
    documents = [f for f in payload["corpus"]["files"] if f["role"] == "document"]
    assert len(documents) == 26
    assert payload["corpus"]["licence"] == "CC BY-SA 4.0"


def test_producer_documents_are_the_frozen_files(payload: dict) -> None:
    step = _step(payload, "producer documents")
    assert step["producer_documents"] == step["same_bytes"] == step["same_length_after_normalisation"] == 25
    analysed = {d["file"] for d in payload["corpus"]["documents"] if d["analysed_by_producer"]}
    assert "A01.txt" not in analysed  # the one German interview; the producer did not analyse it
    assert len(analysed) == 25


def test_every_cited_passage_is_the_frozen_text_at_its_offsets(payload: dict) -> None:
    step = _step(payload, "theory cites")
    assert step["producer_segments"] == step["producer_segments_matching"] == 1277
    assert step["passages_carried_by_the_pin"] == 194
    assert step["cited_passages"] == step["cited_matching"] == 100
    assert step["cited_unresolved"] == 0
    strand = payload["qualitative_strand"]
    assert len(strand["categories"]) == 4 and len(strand["propositions"]) == 6
    for passage in strand["passages"].values():
        document = next(d for d in payload["corpus"]["documents"] if d["file"] == passage["file"])
        assert document["text"][passage["start"] : passage["end"]] == passage["text"]


def test_author_passages_are_all_accounted_for(payload: dict) -> None:
    step = _step(payload, "author's coded passages")
    located = sum(step[f"located_{k}"] for k in ("exact", "whitespace", "text_differs", "not_found"))
    assert step["author_passages"] == located == 837
    assert step["located_exact"] + step["located_whitespace"] >= 790
    assert len(payload["human_coding"]["passages"]) == 837


def test_quantitative_and_integration_strands_say_not_built(payload: dict) -> None:
    status = {s["name"]: s["status"] for s in payload["strands"]}
    assert status["Qualitative strand"] == "built"
    assert status["Quantitative strand"] == status["Joint display and meta-inference"] == "not built"


def test_page_labels_the_pinned_producer_run(payload: dict) -> None:
    """Plan #8 S1 and open question Q26: the pinned run is named and labelled as not QC's published run."""
    strand = payload["qualitative_strand"]
    assert strand["pin_label"]["label"] == (
        "Qualitative Coding's October 2026 theory (run e131eb55), not its newest run (a67d7d6a)"
    )
    assert "e131eb55" in strand["producer_trace_id"]
    assert strand["commit"] == "7f5a8af9056eb3c8b44685ed68c7ae505636fd7b"
    assert "Q26" in strand["pin_label"]["repin_when"]
    # QC's own verdict on the pinned run is stated (round-13 cold review, R13-B2).
    assert "rejects 46% of proposed quotes" in strand["pin_label"]["reason"]
    # The verdict is quoted with its source line (round-16 cold review, n-ii).
    assert "docs/CURRENT_STATE_AND_ROADMAP.md:32" in strand["pin_label"]["reason"]
    template = (REPO / "src" / "mixed_methods_workbench" / "static" / "study_workbench.html").read_text()
    assert "S.pin_label.label" in template and 'id: "pin-label"' in template


def test_passage_location_is_shown_with_its_chance_rate_not_as_agreement(payload: dict) -> None:
    """Plan #8 S1, A3 (round-17 cold review, R17-B1): overlap with the author's coding is location, shown beside chance."""
    location = payload["qualitative_strand"]["agreement_with_author"]["location"]
    assert location["cited_passages"] == 100
    assert location["cited_passages_overlapping_an_author_passage"] == 100
    assert location["cited_passages_inside_one_author_passage"] == 73
    assert (location["author_coded_characters"], location["corpus_characters"]) == (397446, 571307)
    assert location["median_cited_passage_characters"] == 970
    assert (location["of_those_overlapping_an_author_passage"], location["interviewee_segments_at_least_that_long"]) == (135, 135)
    assert location["of_those_inside_one_author_passage"] == 89
    assert location["chance"]["tested"] is True and location["chance"]["above_chance"] is False
    assert location["reads_as"] == "location, not agreement"
    comparison = payload["qualitative_strand"]["agreement_with_author"]["producer_comparison"]
    assert comparison["recorded_for_pinned_run"] is False
    assert comparison["statement"] == "QC has committed no comparison with the author's coding for this run."
    assert "79.8%" in comparison["newer_run_note"] and "77.4%" in comparison["newer_run_note"]
    template = (REPO / "src" / "mixed_methods_workbench" / "static" / "study_workbench.html").read_text()
    assert "location, not agreement" in template and "Chance gives the same" in template
    assert "cannot show agreement" in template


def test_chance_reading_follows_the_figures_not_fixed_text() -> None:
    """Round-18 cold review, n-nn: the page's chance sentence is computed, so a moved pin cannot keep a stale claim."""
    baseline = {
        "interviewee_segments_at_least_that_long": 100,
        "of_those_overlapping_an_author_passage": 50,
        "of_those_inside_one_author_passage": 30,
    }
    assert chance_reading(100, 52, 31, baseline)["above_chance"] is False
    assert chance_reading(100, 90, 31, baseline)["above_chance"] is True
    assert chance_reading(0, 0, 0, baseline) == {"tested": False, "above_chance": False, "level": 0.05}


def test_pin_record_is_typed_and_refuses_unknown_fields(tmp_path: Path) -> None:
    """The pin (qc/provenance.json) is read through ProducerInputPin, not as a raw dict."""
    study = _copy_study(tmp_path)
    pin_path = study / "qc" / "provenance.json"
    pin = json.loads(pin_path.read_text(encoding="utf-8"))
    assert pin["repository"] == "BrianMills2718/qc"
    pin["grounded_theory"]["unexpected"] = "x"
    pin_path.write_text(json.dumps(pin), encoding="utf-8")
    with pytest.raises(ValidationError):
        build_study_payload(study)


def test_unsupported_producer_schema_is_refused() -> None:
    raw = json.loads((STUDY / "qc" / "theory.json").read_text(encoding="utf-8"))["development"]
    assert read_grounded_theory(raw).schema_version == 3
    for version in (2, 4, "4.0", None):
        raw["schema_version"] = version
        with pytest.raises(UnsupportedProducerSchema):
            read_grounded_theory(raw)


def _copy_study(tmp_path: Path) -> Path:
    target = tmp_path / "study"
    shutil.copytree(STUDY, target)
    return target


def test_planted_altered_passage_is_listed_not_dropped(tmp_path: Path) -> None:
    study = _copy_study(tmp_path)
    theory_path = study / "qc" / "theory.json"
    theory = json.loads(theory_path.read_text(encoding="utf-8"))
    cited = theory["development"]["proposal"]["propositions"][0]["supporting_source_unit_ids"][0]
    victim = theory["source_units"][cited]
    words = victim["text"].split(" ")
    words[1] = "NOT"
    victim["text"] = " ".join(words)
    theory_path.write_text(json.dumps(theory), encoding="utf-8")
    payload = build_study_payload(study)
    step = _step(payload, "theory cites")
    assert step["cited_matching"] == step["cited_passages"] - 1
    mismatch = payload["qualitative_strand"]["offset_mismatches"]
    assert [m["id"] for m in mismatch] == [cited]
    assert mismatch[0]["frozen_text_at_offsets"] != mismatch[0]["text"]


def test_planted_fabricated_passage_id_is_reported(tmp_path: Path) -> None:
    study = _copy_study(tmp_path)
    gt_path = study / "qc" / "theory.json"
    gt = json.loads(gt_path.read_text(encoding="utf-8"))
    gt["development"]["proposal"]["propositions"][0]["supporting_source_unit_ids"].append("segment-" + "0" * 32)
    gt_path.write_text(json.dumps(gt), encoding="utf-8")
    payload = build_study_payload(study)
    assert payload["qualitative_strand"]["unresolved_passage_ids"] == ["segment-" + "0" * 32]
    assert _step(payload, "theory cites")["cited_unresolved"] == 1


def test_planted_changed_source_file_fails_its_checksum(tmp_path: Path) -> None:
    study = _copy_study(tmp_path)
    path = study / "source" / "A05.txt"
    path.write_bytes(path.read_bytes() + b" ")
    step = _step(build_study_payload(study), "publisher's md5")
    assert step["md5_matches"] == step["sha256_matches"] == 27


def test_anchor_text_reports_how_exact_the_match_is() -> None:
    source = "Interviewer: Hello.\nInterviewee: We share   data openly,\nmostly."
    assert anchor_text(source, "share   data").status == "exact"
    found = anchor_text(source, "We share data openly, mostly.")
    assert found.status == "whitespace"
    assert source[found.start : found.end] == "We share   data openly,\nmostly."
    differs = anchor_text(source, "We share   data openly, mostly, always and everywhere in public.")
    assert differs.status == "text_differs" and 0 < differs.similarity < 1
    assert anchor_text(source, "nothing like this at all, unrelated words entirely").status == "not_found"


def test_committed_page_and_receipt_match_the_builder(tmp_path: Path) -> None:
    page, payload, study_id = render(STUDY)
    committed = page_dir_for(study_id) / "index.html"
    assert committed.read_bytes() == page, "study page is stale: run make study-page and commit"
    build(STUDY, out_dir=tmp_path)
    assert (tmp_path / "build_receipt.json").read_bytes() == (STUDY / "build_receipt.json").read_bytes(), (
        "build_receipt.json is stale: run make study-page and commit"
    )
