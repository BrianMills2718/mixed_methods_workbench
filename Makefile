# Mixed Methods Workbench Makefile
#
# Usage: make help

SHELL := /bin/bash
PYTHON ?= python3
.DEFAULT_GOAL := help

# ─── Status ──────────────────────────────────────────────────────────────

.PHONY: status

status:  ## Show git status
	@git status --short --branch

.PHONY: validate-fixtures validate-negative-controls validate-coverage-negative-controls validate-generated-coverage validate-interface-contracts validate-demo-fixtures validate-demo-controls assemble-demo-review test-demo typecheck-demo method-dashboard test-method-dashboard test-investigation-spine test-nyc-crz-evidence-slice test-mist-trail-decision demo-coverage coverage coverage-json check

validate-fixtures:  ## Validate synthetic fixture contract files
	@python3 scripts/validate_fixtures.py

validate-negative-controls:  ## Verify fixture validator catches known-invalid controls
	@python3 scripts/check_fixture_negative_controls.py

validate-coverage-negative-controls:  ## Verify coverage grade changes when evidence is removed
	@python3 scripts/check_coverage_negative_controls.py

validate-generated-coverage:  ## Fail when tracked coverage reports are stale
	@python3 scripts/check_coverage.py --check-reports --format json >/dev/null

validate-interface-contracts: validate-generated-coverage  ## Verify machine-facing Make output contracts
	@python3 scripts/check_make_interface_contracts.py

validate-demo-fixtures:  ## Validate and assemble the typed DEMO-C1 positive fixture
	@PYTHONPATH=src python3 -m mixed_methods_workbench.cli validate
	@PYTHONPATH=src pytest -q tests/test_demo_positive.py

validate-demo-controls:  ## Run invariant-specific DEMO-C1 negative controls
	@PYTHONPATH=src pytest -q tests/test_demo_negative_controls.py

assemble-demo-review:  ## Print the typed DEMO-C1 review packet as JSON
	@PYTHONPATH=src python3 -m mixed_methods_workbench.cli assemble

test-demo:  ## Run all DEMO-C1 tests
	@PYTHONPATH=src pytest -q tests

typecheck-demo:  ## Type-check the DEMO-C1 package strictly
	@mypy --strict src/mixed_methods_workbench

method-dashboard:  ## Run the local METHOD-DASH-C1 review dashboard
	@PYTHONPATH=src $(PYTHON) -m mixed_methods_workbench.method_dashboard_server

test-method-dashboard:  ## Run focused question-first routing and dashboard checks
	@PYTHONPATH=src $(PYTHON) -m pytest -q tests/test_method_dashboard.py

test-investigation-spine:  ## Run the cohesive QC-to-Process-Tracing journey checks
	@PYTHONPATH=src $(PYTHON) -m pytest -q tests/test_investigation_spine.py

test-nyc-crz-evidence-slice:  ## Run the review-gated NYC extraction and anchor checks
	@PYTHONPATH=src $(PYTHON) -m pytest -q tests/test_nyc_crz_evidence_slice.py

test-mist-trail-decision:  ## Run the MT-D1 packet, corruption, and UI contract checks
	@PYTHONPATH=src $(PYTHON) -m pytest -q tests/test_mist_trail_decision.py

demo-coverage:  ## Regenerate coverage including DEMO-C1 rows
	@python3 scripts/check_coverage.py --write-reports --format markdown

coverage:  ## Generate human-readable coverage report
	@python3 scripts/check_coverage.py --write-reports --format markdown

coverage-json:  ## Print machine-readable coverage without changing files
	@python3 scripts/check_coverage.py --format json

check: validate-fixtures validate-negative-controls validate-coverage-negative-controls validate-interface-contracts validate-demo-fixtures validate-demo-controls typecheck-demo  ## Run all current repo checks

# ─── Help ────────────────────────────────────────────────────────────────

.PHONY: help

help:  ## Show available targets
	@echo "Mixed Methods Workbench"
	@echo ""
	@grep -E '^[a-z][-a-zA-Z0-9_]*:.*## ' $(MAKEFILE_LIST) | \
		awk -F ':.*## ' '{printf "  make %-20s %s\n", $$1, $$2}'
