#
# Variables
#
.DEFAULT_GOAL    := generate
FIND             := find . -type f -not -path './build/*' -not -path './.git/*'
FORCE_GO_MODULES := GO111MODULE=on
OPEN_DOCS        ?= "-open"
PYTHON           := build/ve/bin/python
VERSION          ?= 1.0.0-beta2

#
# Targets (sorted alphabetically)
#

# Check verifies that all of the committed files that are generated are
# up-to-date.
.PHONY: check
check: generate fmt misspell makelint check-license-headers
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
	rm -rf schema.csv schema.md schema.json fields.yml build
	# Clean all markdown files for use-cases
	find ./use-cases -type f -name '*.md' -not -name 'README.md' -print0 | xargs -0 rm --

# Alias to generate source code for all languages.
.PHONY: codegen
codegen: gocodegen

# Build schema.csv from schema files.
.PHONY: csv
csv: ve
	$(PYTHON) scripts/schemas.py

# Build the asciidoc book.
.PHONY: docs
docs:
	if [ ! -d $(PWD)/build/docs ]; then \
		git clone --depth=1 https://github.com/elastic/docs.git ./build/docs ; \
	fi
	./build/docs/build_docs.pl --doc ./docs/index.asciidoc --chunk=1 $(OPEN_DOCS) -out ./build/html_docs

# Build the fields.yml file.
.PHONY: fields
fields:
	cat schemas/*.yml > fields.tmp.yml
	sed -i.bak 's/^/    /g' fields.tmp.yml
	sed -i.bak 's/---//g' fields.tmp.yml
	cat scripts/fields_header.yml > fields.yml
	cat fields.tmp.yml >> fields.yml
	rm -f fields.tmp.yml fields.tmp.yml.bak

# Format code and files in the repo.
.PHONY: fmt
fmt: ve
	$(FIND) -name '*.py' -exec build/ve/bin/autopep8 --in-place --max-line-length 120 {} \;
	go get golang.org/x/tools/cmd/goimports
	goimports -w -l -local github.com/elastic $(shell $(FIND) -name '*.go')

# Alias to generate everything.
.PHONY: generate
generate: csv readme template fields codegen

# Generate Go code from the schema.
.PHONY: gocodegen
gocodegen:
	find code/go/ecs -name '*.go' -not -name 'doc.go' | xargs rm
	cd scripts \
	  && $(FORCE_GO_MODULES) go run cmd/gocodegen/gocodegen.go \
	        -version=$(VERSION) \
	        -schema=../schemas \
	        -out=../code/go/ecs

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
	misspell README.md CONTRIBUTING.md

# Build README.md by concatenating various markdown snippets.
.PHONY: readme
readme:
	cat docs/intro.md > README.md
	$(PYTHON) scripts/schemas.py --stdout=true >> README.md
	cat docs/use-cases-header.md >> README.md
	$(PYTHON) scripts/use-cases.py --stdout=true >> README.md
	cat docs/implementing.md >> README.md
	cat docs/about.md >> README.md

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
	        > ../template.json

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
