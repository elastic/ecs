#
# Variables
#
.DEFAULT_GOAL    := all
FIND             := find . -type f -not -path './build/*' -not -path './.git/*'
OPEN_DOCS        ?= "--open"
PYTHON           := build/ve/bin/python
SUBSETS_DIR      := schemas/subsets/
EXP_SUBSETS_DIR  := experimental/schemas/subsets/
VERSION          := $(shell cat version)
SEMCONV_VERSION  := $(shell cat otel-semconv-version)

#
# Targets (sorted alphabetically)
#

# Default build generates main and experimental artifacts
.PHONY: all
all: generate experimental

# Check verifies that all of the committed files that are generated are
# up-to-date.
.PHONY: check
check: generate experimental test fmt misspell_warn makelint
	# Check if diff is empty.
	git diff | cat
	git update-index --refresh
	git diff-index --exit-code HEAD --

# Check for license headers
.PHONY: check_license_headers
check_license_headers:
	@echo "Files missing license headers:\n"
	@find . -type f \( -path './scripts/*' -o -path './schemas/*' \) \
	\( -name '*.py' -o -name '*.yml' \) \
	-print0 | xargs -0 -n1 grep -L "Licensed to Elasticsearch B.V." \
	|| exit 0

# Clean deletes all temporary and generated content.
.PHONY: clean
clean:
	rm -rf build generated/elasticsearch/composable/component experimental/generated/elasticsearch/composable/component

# Build and serve the docs
.PHONY: docs
docs:
	@echo "Building documentation with docs-builder..."
	@mkdir -p $(PWD)/build/docs
	@if [ ! -f "$(PWD)/build/docs/docs-builder" ] && [ ! -f "$(PWD)/build/docs/docs-builder.exe" ]; then \
		echo "Downloading docs-builder..."; \
		OS=$$(uname -s 2>/dev/null || echo "Windows_NT"); \
		cd $(PWD)/build/docs && \
		if [ "$$OS" = "Darwin" ]; then \
			ARCH=$$(uname -m); \
			if [ "$$ARCH" = "arm64" ]; then \
				echo "Detected macOS on ARM64"; \
				curl -LO https://github.com/elastic/docs-builder/releases/latest/download/docs-builder-mac-arm64.zip; \
				ZIPFILE="docs-builder-mac-arm64.zip"; \
			else \
				echo "Detected macOS on x86_64"; \
				curl -LO https://github.com/elastic/docs-builder/releases/latest/download/docs-builder-mac-x86_64.zip; \
				ZIPFILE="docs-builder-mac-x86_64.zip"; \
			fi; \
		elif [ "$$OS" = "Linux" ]; then \
			echo "Detected Linux"; \
			curl -LO https://github.com/elastic/docs-builder/releases/latest/download/docs-builder-linux-x86_64.zip; \
			ZIPFILE="docs-builder-linux-x86_64.zip"; \
		elif echo "$$OS" | grep -q "Windows"; then \
			echo "Detected Windows"; \
			curl -LO https://github.com/elastic/docs-builder/releases/latest/download/docs-builder-windows-x86_64.zip; \
			ZIPFILE="docs-builder-windows-x86_64.zip"; \
		else \
			echo "Unsupported platform: $$OS"; \
			exit 1; \
		fi && \
		unzip -o $$ZIPFILE && \
		rm $$ZIPFILE && \
		if echo "$$OS" | grep -q "Windows"; then \
			chmod +x docs-builder.exe 2>/dev/null || true; \
		else \
			chmod +x docs-builder; \
		fi; \
	fi
	@echo "Running docs-builder to serve documentation..."
	@cd $(PWD) && \
	if [ -f "$(PWD)/build/docs/docs-builder.exe" ]; then \
		$(PWD)/build/docs/docs-builder.exe serve; \
	else \
		$(PWD)/build/docs/docs-builder serve; \
	fi

# Alias to generate experimental artifacts
.PHONY: experimental
experimental: ve
	$(PYTHON) scripts/generator.py --include experimental/schemas --subset "${SUBSETS_DIR}" "${EXP_SUBSETS_DIR}" --semconv-version "${SEMCONV_VERSION}" --out experimental

# Format code and files in the repo.
.PHONY: fmt
fmt: ve
	$(FIND) -name '*.py' -exec build/ve/bin/autopep8 --ignore E402 --in-place --max-line-length 120 {} \;

# Alias to generate everything.
.PHONY: generate
generate: generator
	$(PYTHON) --version

# Run the new generator
.PHONY: generator
generator: ve
	$(PYTHON) scripts/generator.py --strict --include "${INCLUDE}" --subset "${SUBSETS_DIR}" --semconv-version "${SEMCONV_VERSION}" --force-docs

# Check Makefile format.
.PHONY: makelint
makelint: SHELL:=/bin/bash
makelint:
	@diff <(grep ^.PHONY Makefile | sort) <(grep ^.PHONY Makefile) \
	  || echo Makefile targets need to be sorted.

# Check for basic misspellings.
.PHONY: misspell
misspell:
	@if [ ! -d $(PWD)/build/misspell ]; then \
	    mkdir -p ./build/misspell/bin ; \
	    curl -sLo ./build/misspell/install-misspell.sh https://git.io/misspell ; \
		chmod +x ./build/misspell/install-misspell.sh ; \
		./build/misspell/install-misspell.sh -b ./build/misspell/bin >> /dev/null 2>&1 ; \
	fi
	./build/misspell/bin/misspell -error README.md CONTRIBUTING.md schemas/* docs/* experimental/schemas/*

# Warn re misspell removal
.PHONY: misspell_warn
misspell_warn:
	@echo "Warning: due to lack of cross-platform support, misspell is no longer included in this task and may be deprecated in future\n"

.PHONY: reload_docs
reload_docs: generator docs

# Run the ECS tests
.PHONY: test
test: ve
	$(PYTHON) -m unittest discover -v --start-directory scripts/tests

# Create a virtualenv to run Python.
.PHONY: ve
ve: build/ve/bin/activate
build/ve/bin/activate: scripts/requirements.txt scripts/requirements-dev.txt
	@test -d build/ve || python3 -mvenv build/ve
	@build/ve/bin/pip install -Ur scripts/requirements.txt -r scripts/requirements-dev.txt
	@touch build/ve/bin/activate

# Check YAML syntax (currently not enforced).
.PHONY: yamllint
yamllint: ve
	build/ve/bin/yamllint -d '{extends: default, rules: {line-length: disable}}' schemas/*.yml
