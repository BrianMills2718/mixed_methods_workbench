"""Study workbench: a frozen corpus and a producer's qualitative strand, checked and joined.

Implements: study_corpus/governed-corpus and qualitative_strand/consumer-view (Plan #8, slice S1).

The workbench does not run a qualitative method. It reads a frozen corpus (``corpus_manifest.json``
and ``source/``), Qualitative Coding's grounded-theory export through a permissive consumer view,
and the corpus author's own coding, then checks that every passage a claim rests on is the text
of the frozen source at its stated place. Nothing that fails a check is dropped: it is counted
and listed.
"""

from __future__ import annotations

import csv
import difflib
import hashlib
import io
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

SUPPORTED_GT_MAJOR = 3


class UnsupportedProducerSchema(ValueError):
    """A producer export whose major schema version this consumer view does not read."""


# ---------------------------------------------------------------- corpus


class CorpusFile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    role: Literal["document", "supporting"]
    bytes: int = Field(ge=0)
    published_md5: str = Field(pattern=r"^[0-9a-f]{32}$")
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class CorpusManifest(BaseModel):
    """The frozen corpus: where it came from, under which licence, and each file's hashes."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"]
    record_type: Literal["corpus_manifest"]
    study_id: str
    title: str
    doi: str
    url: str
    creator: str
    publication_date: str
    licence: str
    licence_url: str
    licence_id_in_record: str
    consent_statement: str
    retrieved_on: str
    files: list[CorpusFile]


class HumanCodingColumns(BaseModel):
    model_config = ConfigDict(extra="forbid")

    file: str
    code: str
    text: str
    start: str
    end: str


class HumanCoding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    file: str
    coder: str
    delimiter: str
    columns: HumanCodingColumns


class StudyDefinition(BaseModel):
    """The one file that adds a study; the code holds nothing specific to a corpus."""

    model_config = ConfigDict(extra="allow")

    schema_version: Literal["1.0"]
    record_type: Literal["study_definition"]
    study_id: str
    title: str
    human_coding: HumanCoding


class PinLabel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    reason: str
    repin_when: str
    source: str


class ProducerHumanComparison(BaseModel):
    """What the producer itself records about agreement with the author's coding (Plan #8 S1, round-16 cold review R16-B1)."""

    model_config = ConfigDict(extra="forbid")

    recorded_for_pinned_run: bool
    statement: str
    newer_run_note: str
    source: str


class PinnedFile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    commit: str
    sha256: str
    form: Literal["view", "export"] = "export"
    extracted: list[str] = []


class ProducerInputPin(BaseModel):
    """``qc/provenance.json``: which committed producer files a study reads, by commit and sha256."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"]
    record_type: Literal["producer_input_pin"]
    producer: str
    repository: str
    grounded_theory: PinnedFile
    project_state: PinnedFile
    text_normalisation: str
    pin_label: PinLabel
    producer_human_comparison: ProducerHumanComparison


# ---------------------------------------------------------------- producer consumer views


class _Permissive(BaseModel):
    model_config = ConfigDict(extra="allow")


class GTIncident(_Permissive):
    open_code: str
    meaning: str
    source_unit_ids: list[str]


class GTCategory(_Permissive):
    name: str
    definition: str
    properties: list[str] = []
    dimensions: list[str] = []
    explanatory_role: str = ""
    incident_indexes: list[int]


class GTProposition(_Permissive):
    statement: str
    category_indexes: list[int]
    supporting_source_unit_ids: list[str]
    qualifying_source_unit_ids: list[str] = []


class GTCoreProcess(_Permissive):
    category_indexes: list[int] = []
    conditions: list[str] = []
    actions_or_responses: list[str] = []
    consequences: list[str] = []


class GTProposal(_Permissive):
    categories: list[GTCategory]
    incidents: list[GTIncident]
    propositions: list[GTProposition]
    core_process: GTCoreProcess | None = None


class GTRun(_Permissive):
    model_name: str = ""
    trace_id: str = ""


class QCGroundedTheoryView(_Permissive):
    """Permissive reading of Qualitative Coding's grounded-theory package (schema major 3)."""

    schema_version: int
    proposal: GTProposal
    run: GTRun = GTRun()
    document_ids_in_order: list[str] = []


def read_grounded_theory(raw: dict[str, Any]) -> QCGroundedTheoryView:
    version = raw.get("schema_version")
    major = int(str(version).split(".")[0]) if version is not None else None
    if major != SUPPORTED_GT_MAJOR:
        raise UnsupportedProducerSchema(
            f"grounded-theory schema_version {version!r}: this view reads major {SUPPORTED_GT_MAJOR} only"
        )
    return QCGroundedTheoryView.model_validate(raw)


class QCDocument(_Permissive):
    id: str
    name: str
    source_filename: str
    source_file_sha256: str
    characters: int


class QCSegment(_Permissive):
    id: str
    doc_id: str
    index: int
    start_char: int
    end_char: int
    speaker: str | None = None
    text: str


# ---------------------------------------------------------------- text handling


def normalise_newlines(text: str) -> str:
    """The producer's recorded normalisation: CRLF and CR are read as LF before counting."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _collapse(text: str) -> tuple[str, list[int]]:
    """Whitespace runs collapsed to one space, with a map back to original positions."""
    out: list[str] = []
    index: list[int] = []
    previous_space = True
    for position, char in enumerate(text):
        if char.isspace():
            if not previous_space:
                out.append(" ")
                index.append(position)
            previous_space = True
        else:
            out.append(char)
            index.append(position)
            previous_space = False
    return "".join(out), index


@dataclass(frozen=True)
class Anchor:
    status: Literal["exact", "whitespace", "text_differs", "not_found"]
    start: int | None
    end: int | None
    similarity: float


def anchor_text(source: str, passage: str) -> Anchor:
    """Locate a passage in its source by its own words; report how exact the match is.

    String location only (no meaning is inferred): exact substring first, then the same words
    with whitespace collapsed, then the longest matching opening, reported as ``text_differs``
    with the similarity of the located span so a person can compare both texts.
    """
    wanted = passage.strip()
    if not wanted:
        return Anchor("not_found", None, None, 0.0)
    start = source.find(wanted)
    if start >= 0:
        return Anchor("exact", start, start + len(wanted), 1.0)
    collapsed_source, index = _collapse(source)
    collapsed_wanted, _ = _collapse(wanted)
    collapsed_wanted = collapsed_wanted.strip()
    position = collapsed_source.find(collapsed_wanted)
    if position >= 0:
        end = index[position + len(collapsed_wanted) - 1] + 1
        return Anchor("whitespace", index[position], end, 1.0)
    length = len(collapsed_wanted)
    while length > 20:
        length = length * 3 // 4
        position = collapsed_source.find(collapsed_wanted[:length])
        if position >= 0:
            stop = min(len(index) - 1, position + len(collapsed_wanted) - 1)
            span = collapsed_source[position : stop + 1]
            ratio = difflib.SequenceMatcher(None, span, collapsed_wanted, autojunk=False).ratio()
            return Anchor("text_differs", index[position], index[stop] + 1, round(ratio, 3))
    return Anchor("not_found", None, None, 0.0)


# ---------------------------------------------------------------- the study


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()  # noqa: S324 (compared with the publisher's md5)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _location_baseline(
    passages: dict[str, dict[str, Any]],
    producer_segments: list[dict[str, Any]],
    by_file: dict[str, list[dict[str, Any]]],
    texts: dict[str, str],
) -> dict[str, Any]:
    """What chance gives for "a cited passage overlaps the author's coding" (round-17 cold review, R17-B1).

    The author coded most of the text, so overlap shows where the evidence sits, not agreement. The
    baseline is every interviewee segment of the producer's own segmentation at least as long as the
    median cited passage: how many of those overlap a passage she coded.
    """
    coded = 0
    for name, text in texts.items():
        marks = bytearray(len(text))
        for a in by_file.get(name, []):
            marks[max(a["start"], 0) : min(a["end"], len(text))] = b"\x01" * max(0, min(a["end"], len(text)) - max(a["start"], 0))
        coded += sum(marks)
    total = sum(len(t) for t in texts.values())
    lengths = sorted(p["end"] - p["start"] for p in passages.values())
    median = lengths[len(lengths) // 2] if lengths else 0
    long_turns = [
        r
        for r in producer_segments
        if r["offsets_match"] and (r["speaker"] or "").strip().lower() != "interviewer" and r["end"] - r["start"] >= median
    ]
    overlapping = sum(
        1 for r in long_turns if any(a["start"] < r["end"] and r["start"] < a["end"] for a in by_file.get(r["file"] or "", []))
    )
    inside = sum(
        1 for r in long_turns if any(a["start"] <= r["start"] and r["end"] <= a["end"] for a in by_file.get(r["file"] or "", []))
    )
    return {
        "author_coded_characters": coded,
        "corpus_characters": total,
        "median_cited_passage_characters": median,
        "interviewee_segments_at_least_that_long": len(long_turns),
        "of_those_overlapping_an_author_passage": overlapping,
        "of_those_inside_one_author_passage": inside,
    }


def _upper_tail(successes: int, trials: int, rate: float) -> float:
    """One-sided binomial tail: the chance of at least `successes` in `trials` at `rate`."""
    return sum(math.comb(trials, k) * rate**k * (1 - rate) ** (trials - k) for k in range(successes, trials + 1))


def chance_reading(cited: int, overlapping: int, inside: int, baseline: dict[str, Any], level: float = 0.05) -> dict[str, Any]:
    """Whether the cited passages sit in the author's coding more often than chance (round-18 cold review, n-nn).

    Each measure is tested one-sided against the share of the baseline turns that meet it. The page words
    its sentence from this result, so a moved pin cannot leave "chance gives the same" behind when it is
    no longer true. Either way the figure shows location, not agreement.
    """
    n = baseline["interviewee_segments_at_least_that_long"]
    if cited == 0 or n == 0:
        return {"tested": False, "above_chance": False, "level": level}
    p_overlap = _upper_tail(overlapping, cited, baseline["of_those_overlapping_an_author_passage"] / n)
    p_inside = _upper_tail(inside, cited, baseline["of_those_inside_one_author_passage"] / n)
    return {
        "tested": True,
        "level": level,
        "p_overlap": round(p_overlap, 4),
        "p_inside": round(p_inside, 4),
        "above_chance": p_overlap < level or p_inside < level,
    }


def build_study_payload(study_dir: Path) -> dict[str, Any]:
    """Every panel of the study page, built only from the frozen files in ``study_dir``."""
    study = StudyDefinition.model_validate(_read_json(study_dir / "study.json"))
    manifest = CorpusManifest.model_validate(_read_json(study_dir / "corpus_manifest.json"))
    pin = ProducerInputPin.model_validate(_read_json(study_dir / "qc" / "provenance.json"))
    gt_bytes = (study_dir / "qc" / "theory.json").read_bytes()
    theory_raw = json.loads(gt_bytes)
    # A "view" pin is QC's review-candidate file: the schema-3 package under "development" plus the cited
    # passages ("source_units", with document, speaker, offsets and text). An "export" pin is the bare
    # package, whose citations resolve through QC's segments.
    form = pin.grounded_theory.form
    gt = read_grounded_theory(theory_raw["development"] if form == "view" else theory_raw)
    source_units: dict[str, Any] = theory_raw.get("source_units", {}) if form == "view" else {}
    qc_documents = [QCDocument.model_validate(d) for d in _read_json(study_dir / "qc" / "documents.json")]
    segments = [QCSegment.model_validate(s) for s in _read_json(study_dir / "qc" / "segments.json")]

    steps: list[dict[str, Any]] = []

    # 1. corpus files against the publisher's checksums
    raw_files: dict[str, bytes] = {}
    file_rows = []
    for entry in manifest.files:
        path = study_dir / "source" / entry.name
        data = path.read_bytes() if path.exists() else b""
        raw_files[entry.name] = data
        file_rows.append(
            {
                "name": entry.name,
                "role": entry.role,
                "bytes": len(data),
                "md5_matches_publisher": bool(data) and _md5(data) == entry.published_md5,
                "sha256_matches_manifest": bool(data) and _sha256(data) == entry.sha256,
            }
        )
    steps.append(
        {
            "step": "corpus files checked against the publisher's md5 and the manifest's sha256",
            "files": len(file_rows),
            "md5_matches": sum(r["md5_matches_publisher"] for r in file_rows),
            "sha256_matches": sum(r["sha256_matches_manifest"] for r in file_rows),
        }
    )
    texts = {
        name: normalise_newlines(data.decode("utf-8"))
        for name, data in raw_files.items()
        if name in {f.name for f in manifest.files if f.role == "document"}
    }

    # 2. the producer's documents are the frozen files
    doc_by_id = {d.id: d for d in qc_documents}
    doc_rows = []
    for doc in qc_documents:
        data = raw_files.get(doc.source_filename, b"")
        doc_rows.append(
            {
                "producer_id": doc.id,
                "file": doc.source_filename,
                "same_bytes_as_frozen": bool(data) and _sha256(data) == doc.source_file_sha256,
                "same_length_after_normalisation": len(texts.get(doc.source_filename, "")) == doc.characters,
            }
        )
    steps.append(
        {
            "step": "producer documents matched to frozen files by sha256",
            "producer_documents": len(doc_rows),
            "same_bytes": sum(r["same_bytes_as_frozen"] for r in doc_rows),
            "same_length_after_normalisation": sum(r["same_length_after_normalisation"] for r in doc_rows),
        }
    )

    # 3. every producer segment against the frozen text at its offsets
    segment_rows: dict[str, dict[str, Any]] = {}
    offset_mismatches = []
    for seg in segments:
        owner = doc_by_id.get(seg.doc_id)
        source = texts.get(owner.source_filename, "") if owner else ""
        at_offsets = source[seg.start_char : seg.end_char]
        ok = owner is not None and at_offsets == seg.text
        row: dict[str, Any] = {
            "id": seg.id,
            "file": owner.source_filename if owner else None,
            "start": seg.start_char,
            "end": seg.end_char,
            "speaker": seg.speaker,
            "text": seg.text,
            "offsets_match": ok,
        }
        segment_rows[seg.id] = row
        if not ok:
            offset_mismatches.append({**row, "frozen_text_at_offsets": at_offsets})

    # 4. the theory's citations
    def cite(ids: list[str]) -> list[str]:
        return list(ids)

    cited: dict[str, None] = {}
    categories = []
    for number, category in enumerate(gt.proposal.categories, start=1):
        incidents = []
        for incident_number in category.incident_indexes:
            if 1 <= incident_number <= len(gt.proposal.incidents):
                incident = gt.proposal.incidents[incident_number - 1]
                incidents.append(
                    {
                        "number": incident_number,
                        "open_code": incident.open_code,
                        "meaning": incident.meaning,
                        "passages": cite(incident.source_unit_ids),
                    }
                )
                cited.update(dict.fromkeys(incident.source_unit_ids))
        categories.append(
            {
                "number": number,
                "name": category.name,
                "definition": category.definition,
                "properties": category.properties,
                "dimensions": category.dimensions,
                "role": category.explanatory_role,
                "incidents": incidents,
            }
        )
    propositions = []
    for number, proposition in enumerate(gt.proposal.propositions, start=1):
        cited.update(dict.fromkeys(proposition.supporting_source_unit_ids))
        cited.update(dict.fromkeys(proposition.qualifying_source_unit_ids))
        propositions.append(
            {
                "number": number,
                "statement": proposition.statement,
                "categories": proposition.category_indexes,
                "supporting": cite(proposition.supporting_source_unit_ids),
                "qualifying": cite(proposition.qualifying_source_unit_ids),
            }
        )
    # cited passages carried by the pin itself are checked against the frozen text like segments
    doc_by_name = {d.name: d for d in qc_documents}
    for unit_id, unit in source_units.items():
        owner = doc_by_name.get(unit.get("document_name", ""))
        source = texts.get(owner.source_filename, "") if owner else ""
        start, end = int(unit["start_char"]), int(unit["end_char"])
        at_offsets = source[start:end]
        ok = owner is not None and at_offsets == unit["text"]
        row = {
            "id": unit_id,
            "file": owner.source_filename if owner else None,
            "start": start,
            "end": end,
            "speaker": unit.get("speaker"),
            "text": unit["text"],
            "offsets_match": ok,
        }
        segment_rows[unit_id] = row
        if not ok:
            offset_mismatches.append({**row, "frozen_text_at_offsets": at_offsets})
    unresolved = [segment_id for segment_id in cited if segment_id not in segment_rows]
    cited_ok = sum(1 for s in cited if s in segment_rows and segment_rows[s]["offsets_match"])
    steps.append(
        {
            "step": "every passage the theory cites resolved and checked against the frozen text",
            "producer_segments": len(segments),
            "producer_segments_matching": sum(1 for s in segments if segment_rows[s.id]["offsets_match"]),
            "passages_carried_by_the_pin": len(source_units),
            "cited_passages": len(cited),
            "cited_matching": cited_ok,
            "cited_unresolved": len(unresolved),
        }
    )

    # 5. the corpus author's own coding, located by its own words
    coding = study.human_coding
    columns = coding.columns
    csv_text = raw_files[coding.file].decode("utf-8")
    author_rows: list[dict[str, Any]] = []
    reader = csv.DictReader(io.StringIO(csv_text), delimiter=coding.delimiter)
    for number, record in enumerate(reader, start=1):
        file_name = record[columns.file]
        source = texts.get(file_name, "")
        anchor = anchor_text(source, record[columns.text])
        stated_start = int(record[columns.start]) if record[columns.start].strip().isdigit() else None
        author_rows.append(
            {
                "number": number,
                "file": file_name,
                "code": record[columns.code],
                "text": record[columns.text].strip(),
                "status": anchor.status,
                "start": anchor.start,
                "end": anchor.end,
                "similarity": anchor.similarity,
                "stated_start": stated_start,
                "stated_offset_exact": stated_start is not None and stated_start == anchor.start,
            }
        )
    statuses = {s: sum(1 for r in author_rows if r["status"] == s) for s in ("exact", "whitespace", "text_differs", "not_found")}
    steps.append(
        {
            "step": "the author's coded passages located in the frozen text by their own words",
            "author_passages": len(author_rows),
            **{f"located_{k}": v for k, v in statuses.items()},
            "stated_offsets_exact": sum(r["stated_offset_exact"] for r in author_rows),
        }
    )

    # 6. author codes overlapping each cited passage
    by_file: dict[str, list[dict[str, Any]]] = {}
    for author in author_rows:
        if author["start"] is not None:
            by_file.setdefault(author["file"], []).append(author)
    passages: dict[str, dict[str, Any]] = {}
    for segment_id in cited:
        found = segment_rows.get(segment_id)
        if found is None:
            continue
        row = found
        overlapping = sorted(
            {
                a["code"]
                for a in by_file.get(row["file"] or "", [])
                if a["start"] < row["end"] and row["start"] < a["end"]
            }
        )
        passages[segment_id] = {**row, "author_codes": overlapping}
    with_codes = sum(1 for p in passages.values() if p["author_codes"])
    inside_one = sum(
        1
        for p in passages.values()
        if any(a["start"] <= p["start"] and p["end"] <= a["end"] for a in by_file.get(p["file"] or "", []))
    )
    location = _location_baseline(passages, [segment_rows[s.id] for s in segments], by_file, texts)
    steps.append(
        {
            "step": "author codes overlapping each cited passage",
            "cited_passages_with_an_author_code": with_codes,
            "cited_passages_without": len(passages) - with_codes,
            "cited_passages_inside_one_author_passage": inside_one,
            **location,
        }
    )

    documents = []
    for name, text in sorted(texts.items()):
        producer = next((d for d in qc_documents if d.source_filename == name), None)
        documents.append(
            {
                "file": name,
                "characters": len(text),
                "analysed_by_producer": producer is not None,
                "author_passages": sum(1 for a in author_rows if a["file"] == name),
                "text": text,
            }
        )

    return {
        "schema_version": "1.0",
        "record_type": "study_workbench_payload",
        "study_id": study.study_id,
        "title": manifest.title,
        "corpus": {
            "doi": manifest.doi,
            "url": manifest.url,
            "creator": manifest.creator,
            "publication_date": manifest.publication_date,
            "licence": manifest.licence,
            "licence_url": manifest.licence_url,
            "consent_statement": manifest.consent_statement,
            "retrieved_on": manifest.retrieved_on,
            "files": file_rows,
            "documents": documents,
        },
        "qualitative_strand": {
            "producer": pin.producer,
            "repository": pin.repository,
            "commit": pin.grounded_theory.commit,
            "theory_path": pin.grounded_theory.path,
            "export_sha256": _sha256(gt_bytes),
            "schema_version": gt.schema_version,
            "model": gt.run.model_name,
            "producer_trace_id": gt.run.trace_id,
            "pin_label": pin.pin_label.model_dump(),
            "agreement_with_author": {
                "location": {
                    "cited_passages": len(passages),
                    "cited_passages_overlapping_an_author_passage": with_codes,
                    "cited_passages_inside_one_author_passage": inside_one,
                    **location,
                    "chance": chance_reading(len(passages), with_codes, inside_one, location),
                    "reads_as": "location, not agreement",
                },
                "producer_comparison": pin.producer_human_comparison.model_dump(),
            },
            "text_normalisation": pin.text_normalisation,
            "core_process": gt.proposal.core_process.model_dump() if gt.proposal.core_process else None,
            "categories": categories,
            "propositions": propositions,
            "passages": passages,
            "unresolved_passage_ids": unresolved,
            "offset_mismatches": offset_mismatches,
            "producer_documents": doc_rows,
        },
        "human_coding": {
            "coder": coding.coder,
            "passages": author_rows,
            "codes": sorted({r["code"] for r in author_rows}),
        },
        "strands": [
            {"name": "Corpus", "status": "built", "slice": "S1"},
            {"name": "Qualitative strand", "status": "built", "slice": "S1"},
            {"name": "Quantitative strand", "status": "not built", "slice": "S2"},
            {"name": "Joint display and meta-inference", "status": "not built", "slice": "S3"},
            {"name": "Causal check", "status": "not built", "slice": "S4"},
        ],
        "steps": steps,
    }
