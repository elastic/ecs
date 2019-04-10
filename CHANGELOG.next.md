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
* Added `hash.*` field set. #426
* Added `event.code`, `event.sequence` and `event.provider`. #439
* Added `file.name` and `file.directory`. #441
* Added `file.created`, and `file.accessed`. #445

### Improvements

* Format port numbers and numeric IDs as strings. #454
* Added examples and improved definitions of many `file` fields. #441

### Deprecated


<!-- All empty sections:

## Unreleased

### Breaking changes

### Bugfixes

### Added

### Improvements

### Deprecated

-->
