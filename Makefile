# Mixed Methods Workbench Makefile
#
# Usage: make help

SHELL := /bin/bash
.DEFAULT_GOAL := help

# ─── Status ──────────────────────────────────────────────────────────────

.PHONY: status

status:  ## Show git status
	@git status --short --branch

# ─── Help ────────────────────────────────────────────────────────────────

.PHONY: help

help:  ## Show available targets
	@echo "Mixed Methods Workbench"
	@echo ""
	@grep -E '^[a-z][-a-zA-Z0-9_]*:.*## ' $(MAKEFILE_LIST) | \
		awk -F ':.*## ' '{printf "  make %-20s %s\n", $$1, $$2}'
