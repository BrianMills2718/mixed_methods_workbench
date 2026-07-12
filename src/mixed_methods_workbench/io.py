"""Load committed DEMO-C1 JSON fixtures into typed contract objects."""

from __future__ import annotations

import hashlib
from pathlib import Path

from pydantic import TypeAdapter

from .models import (
    ControlledDemoPacket,
    CrossMethodLink,
    DemoFixtureManifest,
    StrictGTInspiredExport,
    StrictPTExport,
    StrictQCExport,
)


FIXTURE_DIR = Path(__file__).resolve().parents[2] / "examples" / "fixtures" / "demo_c1"


def load_model[T](path: Path, model_type: type[T]) -> T:
    """Parse one JSON file through its declared Pydantic boundary without fallback."""
    return TypeAdapter(model_type).validate_json(path.read_text(encoding="utf-8"))


def load_links(path: Path) -> list[CrossMethodLink]:
    """Parse the link array as typed neutral cross-method relationships."""
    return TypeAdapter(list[CrossMethodLink]).validate_json(path.read_text(encoding="utf-8"))


def validate_demo_manifest(fixture_dir: Path = FIXTURE_DIR) -> DemoFixtureManifest:
    """Prove the manifest exhaustively inventories the exact synthetic payload bytes."""
    if fixture_dir.is_symlink():
        raise ValueError("DEMO-C1 fixture directory must not be a symlink")
    symlinks = sorted(
        path.relative_to(fixture_dir).as_posix()
        for path in fixture_dir.rglob("*")
        if path.is_symlink()
    )
    if symlinks:
        raise ValueError(f"DEMO-C1 fixture directory contains unsupported symlinks: {symlinks}")
    manifest = load_model(fixture_dir / "manifest.json", DemoFixtureManifest)
    expected_paths = {entry.path for entry in manifest.files}
    actual_paths = {
        path.relative_to(fixture_dir).as_posix()
        for path in fixture_dir.rglob("*")
        if path.is_file()
        and path.suffix.casefold() == ".json"
        and path.relative_to(fixture_dir).as_posix() != "manifest.json"
    }
    if actual_paths != expected_paths:
        missing = sorted(expected_paths - actual_paths)
        unlisted = sorted(actual_paths - expected_paths)
        raise ValueError(
            f"DEMO-C1 fixture inventory mismatch: missing={missing}, unlisted={unlisted}"
        )
    for entry in manifest.files:
        payload = (fixture_dir / entry.path).read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        if digest != entry.sha256:
            raise ValueError(f"DEMO-C1 fixture hash mismatch: {entry.path}")
    return manifest


def load_demo_inputs(
    fixture_dir: Path = FIXTURE_DIR,
) -> tuple[
    ControlledDemoPacket,
    StrictQCExport,
    StrictPTExport,
    StrictGTInspiredExport,
    list[CrossMethodLink],
]:
    """Load the complete committed positive-control journey in assembly order."""
    validate_demo_manifest(fixture_dir)
    return (
        load_model(fixture_dir / "packet.json", ControlledDemoPacket),
        load_model(fixture_dir / "qc.json", StrictQCExport),
        load_model(fixture_dir / "pt.json", StrictPTExport),
        load_model(fixture_dir / "gt_inspired.json", StrictGTInspiredExport),
        load_links(fixture_dir / "links.json"),
    )


def write_review_json(output: Path, payload_json: str, *, force: bool = False) -> None:
    """Write a derived review artifact without silently replacing prior evidence."""
    if output.is_symlink():
        raise FileExistsError(f"refusing to write through review artifact symlink: {output}")
    if output.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing review artifact: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(payload_json + "\n", encoding="utf-8")
