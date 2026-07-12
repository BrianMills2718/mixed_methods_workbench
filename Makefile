# Mixed Methods Workbench Makefile
#
# Usage: make help

SHELL := /bin/bash
.DEFAULT_GOAL := help

# ─── Status ──────────────────────────────────────────────────────────────

.PHONY: status

status:  ## Show git status
	@git status --short --branch

.PHONY: validate-fixtures validate-negative-controls validate-coverage-negative-controls validate-generated-coverage validate-interface-contracts _coverage-prereqs coverage coverage-json check

validate-fixtures:  ## Validate synthetic fixture contract files
	@python3 scripts/validate_fixtures.py

validate-negative-controls:  ## Verify fixture validator catches known-invalid controls
	@python3 scripts/check_fixture_negative_controls.py

validate-coverage-negative-controls:  ## Verify coverage grade changes when evidence is removed
	@python3 scripts/check_coverage_negative_controls.py

validate-generated-coverage: _coverage-prereqs  ## Fail when tracked coverage reports are stale
	@python3 scripts/check_coverage.py --check-reports --format json >/dev/null

validate-interface-contracts: validate-generated-coverage  ## Verify machine-facing Make output contracts
	@python3 scripts/check_make_interface_contracts.py

_coverage-prereqs:
	@python3 scripts/validate_fixtures.py >/dev/null
	@python3 scripts/check_fixture_negative_controls.py >/dev/null
	@python3 scripts/check_coverage_negative_controls.py >/dev/null

coverage: _coverage-prereqs  ## Generate human-readable coverage report
	@python3 scripts/check_coverage.py --write-reports --format markdown

coverage-json: _coverage-prereqs  ## Print machine-readable coverage without changing files
	@python3 scripts/check_coverage.py --format json

check: validate-fixtures validate-negative-controls validate-coverage-negative-controls validate-interface-contracts  ## Run all current repo checks

# ─── Help ────────────────────────────────────────────────────────────────

.PHONY: help

help:  ## Show available targets
	@echo "Mixed Methods Workbench"
	@echo ""
	@grep -E '^[a-z][-a-zA-Z0-9_]*:.*## ' $(MAKEFILE_LIST) | \
		awk -F ':.*## ' '{printf "  make %-20s %s\n", $$1, $$2}'
