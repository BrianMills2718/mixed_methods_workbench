# Mixed Methods Workbench Makefile
#
# Usage: make help

SHELL := /bin/bash
.DEFAULT_GOAL := help

# ─── Status ──────────────────────────────────────────────────────────────

.PHONY: status

status:  ## Show git status
	@git status --short --branch

.PHONY: validate-fixtures validate-negative-controls coverage coverage-json check

validate-fixtures:  ## Validate synthetic fixture contract files
	@python3 scripts/validate_fixtures.py

validate-negative-controls:  ## Verify fixture validator catches known-invalid controls
	@python3 scripts/check_fixture_negative_controls.py

coverage:  ## Generate human-readable coverage report
	@python3 scripts/check_coverage.py --format markdown

coverage-json:  ## Generate machine-readable coverage report
	@python3 scripts/check_coverage.py --format json

check: validate-fixtures validate-negative-controls  ## Run all current repo checks

# ─── Help ────────────────────────────────────────────────────────────────

.PHONY: help

help:  ## Show available targets
	@echo "Mixed Methods Workbench"
	@echo ""
	@grep -E '^[a-z][-a-zA-Z0-9_]*:.*## ' $(MAKEFILE_LIST) | \
		awk -F ':.*## ' '{printf "  make %-20s %s\n", $$1, $$2}'
