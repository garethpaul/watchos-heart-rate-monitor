PYTHON ?= python3
XCODEBUILD ?= xcodebuild
ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PROJECT := $(ROOT)/HeartyMonitor.xcodeproj
SCHEME := HeartyMonitor
CONTRACT_SCRIPT := \
	$(ROOT)/scripts/check_watchos_contracts.py
WORKFLOW_CONTRACT_SCRIPT := \
	$(ROOT)/scripts/test_workflow_contract.py

.PHONY: clean lint test contract-test build verify check

clean:
	find "$(ROOT)" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
	find "$(ROOT)" -type d -name '__pycache__' -prune -exec rm -rf {} +

lint:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m py_compile $(CONTRACT_SCRIPT)

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(CONTRACT_SCRIPT)

contract-test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) $(WORKFLOW_CONTRACT_SCRIPT)

build:
	@if command -v $(XCODEBUILD) >/dev/null 2>&1; then \
		$(XCODEBUILD) -project "$(PROJECT)" -scheme "$(SCHEME)" -configuration Debug CODE_SIGNING_ALLOWED=NO build; \
	else \
		echo "Skipping xcodebuild: xcodebuild is not installed."; \
	fi

verify: lint test contract-test build

check: clean verify
	$(MAKE) -f "$(abspath $(lastword $(MAKEFILE_LIST)))" clean
