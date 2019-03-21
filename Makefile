#
# Variables
#
.DEFAULT_GOAL    := generate
FIND             := find . -type f -not -path './build/*' -not -path './.git/*'
FORCE_GO_MODULES := GO111MODULE=on
OPEN_DOCS        ?= "-open"
PYTHON           := build/ve/bin/python
VERSION          := $(shell cat version)

#
# Targets (sorted alphabetically)
#

# Check verifies that all of the committed files that are generated are
# up-to-date.
.PHONY: check
check: generate test fmt misspell makelint check-license-headers
	# Check if diff is empty.
	git diff | cat
	git update-index --refresh
	git diff-index --exit-code HEAD --

# Check license headers on files (currently .go files only).
.PHONY: check-license-headers
check-license-headers:
	go get github.com/elastic/go-licenser
	go-licenser -d

# Clean deletes all temporary and generated content.
.PHONY: clean
clean:
	rm -rf schema.json build
	rm -rf generated/legacy/{README.md,schema.csv,template.json,fields.yml}
	# Clean all markdown files for use-cases
	find ./use-cases -type f -name '*.md' -not -name 'README.md' -print0 | xargs -0 rm --

# Alias to generate source code for all languages.
.PHONY: codegen
codegen: gocodegen

# Build schema.csv from schema files.
# Build the asciidoc book.
.PHONY: docs
docs:
	if [ ! -d $(PWD)/build/docs ]; then \
		git clone --depth=1 https://github.com/elastic/docs.git ./build/docs ; \
	fi
	./build/docs/build_docs.pl --doc ./docs/index.asciidoc --chunk=1 $(OPEN_DOCS) -out ./build/html_docs

# Format code and files in the repo.
.PHONY: fmt
fmt: ve
	$(FIND) -name '*.py' -exec build/ve/bin/autopep8 --ignore E402 --in-place --max-line-length 120 {} \;
	go get golang.org/x/tools/cmd/goimports
	goimports -w -l -local github.com/elastic $(shell $(FIND) -name '*.go')

# Alias to generate everything.
.PHONY: generate
generate: template legacy_fields legacy_csv legacy_readme codegen generator

# Run the new generator
.PHONY: generator
generator:
	$(PYTHON) scripts/generator.py

# Generate Go code from the schema.
.PHONY: gocodegen
gocodegen:
	find code/go/ecs -name '*.go' -not -name 'doc.go' | xargs rm
	cd scripts \
	  && $(FORCE_GO_MODULES) go run cmd/gocodegen/gocodegen.go \
	        -version=$(VERSION) \
	        -schema=../schemas \
	        -out=../code/go/ecs

.PHONY: legacy_csv
legacy_csv: ve
	$(PYTHON) scripts/schemas.py

# Build the legacy fields.yml file.
.PHONY: legacy_fields
legacy_fields:
	cat schemas/*.yml > fields.tmp.yml
	sed -i.bak 's/^/    /g' fields.tmp.yml
	sed -i.bak 's/---//g' fields.tmp.yml
	cat generated/legacy/fields_header.yml > generated/legacy/fields.yml
	cat fields.tmp.yml >> generated/legacy/fields.yml
	rm -f fields.tmp.yml fields.tmp.yml.bak

.PHONY: legacy_readme
legacy_readme: ve
	cat docs/legacy/intro.md > generated/legacy/README.md
	$(PYTHON) scripts/schemas.py --stdout=true >> generated/legacy/README.md
	cat docs/legacy/use-cases-header.md >> generated/legacy/README.md
	$(PYTHON) scripts/use-cases.py --stdout=true >> generated/legacy/README.md
	cat docs/legacy/implementing.md >> generated/legacy/README.md
	cat docs/legacy/about.md >> generated/legacy/README.md
	cat docs/legacy/generated-files.md >> generated/legacy/README.md


# Check Makefile format.
.PHONY: makelint
makelint: SHELL:=/bin/bash
makelint:
	@diff <(grep ^.PHONY Makefile | sort) <(grep ^.PHONY Makefile) \
	  || echo Makefile targets need to be sorted.

# Check for basic misspellings.
.PHONY: misspell
misspell:
	go get github.com/client9/misspell/cmd/misspell
	misspell README.md CONTRIBUTING.md generated/legacy/README.md

# Download and setup tooling dependencies.
.PHONY: setup
setup: ve
	cd scripts && $(FORCE_GO_MODULES) go mod download

# Build an Elasticsearch index template.
.PHONY: template
template:
	cd scripts \
	  && $(FORCE_GO_MODULES) go run cmd/template/template.go \
	        -version=$(VERSION) \
	        -schema=../schemas \
	        > ../generated/legacy/template.json

# Run the ECS tests
.PHONY: test
test:
	$(PYTHON) -m unittest discover --start-directory scripts/tests

# Create a virtualenv to run Python.
.PHONY: ve
ve: build/ve/bin/activate
build/ve/bin/activate: scripts/requirements.txt
	@test -d build/ve || virtualenv build/ve
	@build/ve/bin/pip install -Ur scripts/requirements.txt
	@touch build/ve/bin/activate

# Check YAML syntax (currently not enforced).
.PHONY: yamllint
yamllint: ve
	build/ve/bin/yamllint schemas/*.yml
