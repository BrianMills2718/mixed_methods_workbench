from scripts.validate_phase0_compliance import (
    validate_disagreements,
    validate_independent_review,
    validate_migration,
)


def test_migration_exactly_covers_all_legacy_rows() -> None:
    validate_migration()


def test_all_comparison_rows_have_section_02_dispositions() -> None:
    validate_disagreements()


def test_independent_review_is_durable() -> None:
    validate_independent_review()
