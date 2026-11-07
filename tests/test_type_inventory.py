"""The system model's type inventory stays in step with the code."""

from __future__ import annotations

from scripts.type_inventory import OUT, build


def test_type_inventory_is_current() -> None:
    assert OUT.read_text(encoding="utf-8") == build(), "docs/planning/TYPES.md is stale: run make type-inventory"
