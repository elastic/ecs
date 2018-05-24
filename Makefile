generate:
	python scripts/schemas.py
	$(MAKE) readme
	$(MAKE) template

generate3:
	python3 scripts/schemas.py
	python3 scripts/use-cases.py

fmt:
	find . -name *.py -exec autopep8 --in-place --max-line-length 120 {} \;

check:
	#
	# Validate that all generated changes are commited
	$(MAKE) generate
	git diff | cat
	git update-index --refresh
	git diff-index --exit-code HEAD --

	# Check python code
	find . -name *.py -exec autopep8 --in-place --max-line-length 120  {} \; | \
		(! grep . -q) || (echo "Code differs from autopep8's style" && false)
	
	# Basic spell checking
	go get github.com/client9/misspell
	misspell README.md CONTRIBUTING.md

setup:
	pip install -Ur ./scripts/requirements.txt

setup3:
	pip3 install -Ur ./scripts/requirements.txt

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
	go run scripts/template.go > ./template.json
