generate: schemas readme template

schemas:
	python scripts/schemas.py

fmt:
	find . -name *.py -exec autopep8 --in-place --max-line-length 120 {} \;

check:
	# Validate that all generated changes are commited
	$(MAKE) generate
	$(MAKE) fmt

	# Check if diff is empty
	git diff | cat
	git update-index --refresh
	git diff-index --exit-code HEAD --

	# Basic spell checking
	go get github.com/client9/misspell/cmd/misspell
	misspell README.md CONTRIBUTING.md

setup:
	pip install --user --upgrade --requirement ./scripts/requirements.txt

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
	go run scripts/template.go > ./template.json

.PHONY: generate schemas fmt check setup clean readme template
