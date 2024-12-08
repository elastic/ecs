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

# Build the asciidoc book.
.PHONY: docs
docs:
	if [ ! -d $(PWD)/build/docs ]; then \
		git clone --depth=1 https://github.com/elastic/docs.git ./build/docs ; \
	fi
	./build/docs/build_docs --asciidoctor --doc ./docs/index.asciidoc --chunk=2 $(OPEN_DOCS) --out ./build/html_docs

# Alias to generate experimental artifacts
.PHONY: experimental
experimental: ve
	$(PYTHON) scripts/generator.py --include experimental/schemas --subset "${SUBSETS_DIR}" "${EXP_SUBSETS_DIR}" --out experimental

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
	$(PYTHON) scripts/generator.py --strict --include "${INCLUDE}" --subset "${SUBSETS_DIR}" --force-docs

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
