VERSION   ?= 1.0.0-beta2
OPEN_DOCS ?= "-open"

generate: schemas readme template fields

schemas:
	python scripts/schemas.py

fmt:
	find . -name *.py -exec autopep8 --in-place --max-line-length 120 {} \;

check: generate fmt fields
	# Check if diff is empty
	git diff | cat
	git update-index --refresh
	git diff-index --exit-code HEAD --

	# Basic spell checking
	go get github.com/client9/misspell/cmd/misspell
	misspell README.md CONTRIBUTING.md

setup:
	pip install --user --upgrade --requirement ./scripts/requirements.txt
	go get -u github.com/elastic/go-ucfg/yaml
	go get -u github.com/elastic/beats/libbeat/template

clean:
	rm schema.csv schema.md
	# Clean all markdown files for use-cases
	find ./use-cases -type f -name '*.md' -not -name 'README.md' -print0 | xargs -0 rm --

readme:
	cat docs/intro.md > README.md
	python scripts/schemas.py --stdout=true >> README.md
	cat docs/use-cases-header.md >> README.md
	python scripts/use-cases.py --stdout=true >> README.md
	cat docs/implementing.md >> README.md
	cat docs/about.md >> README.md

template:
	go get github.com/elastic/go-ucfg/yaml
	go get github.com/elastic/beats/libbeat/template
	go run scripts/template.go -version=$(VERSION) > ./template.json

fields:
	cat schemas/*.yml > fields.tmp.yml
	sed -i.bak 's/^/    /g' fields.tmp.yml
	sed -i.bak 's/---//g' fields.tmp.yml
	cat scripts/fields_header.yml > fields.yml
	cat fields.tmp.yml >> fields.yml
	rm -f fields.tmp.yml fields.tmp.yml.bak

docs:
	if [ ! -d $(PWD)/build/docs ]; then \
		git clone --depth=1 https://github.com/elastic/docs.git ./build/docs ; \
	fi

	./build/docs/build_docs.pl --doc ./docs/index.asciidoc --chunk=1 $(OPEN_DOCS) -out ./build/html_docs

.PHONY: generate schemas fmt check setup clean readme template fields docs
