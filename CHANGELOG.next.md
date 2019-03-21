## Unreleased

### Breaking changes

### Bugfixes

### Added

* Translate the documentation from README.md, to the main website. #266, #334
* New generator that supports reusable fields, for files based on ECS.
  It generates schema.csv, Elasticsearch 6 and 7 templates, and field documentation
  for the main website. #336
* Generator for the asciidoc rendering of field definitions. #347
* Generator for the Beats fields.ecs.yml file. #379
* Added field formats to all `.bytes` fields and `event.duration`. #385

### Improvements

* Make the README.md a good starting point for contributors. Redirect to main
  website for ECS documentation itself. #395

### Deprecated

* Move old `fields.yml` file from the root of the repo to `generated/legacy`. #386
* Move the old all-in-one README.md to generated/legacy/. #395

<!-- All empty sections:

## Unreleased

### Breaking changes

### Bugfixes

### Added

### Improvements

### Deprecated

-->
