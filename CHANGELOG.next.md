<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

#### Breaking changes

#### Bugfixes

* Add `thumbprint_sha256` to `code_signature` schema. #2452
* Add `origin_referrer_url` and `origin_url` fields, which indicate the origin information to the file, process and dll schemas #2441

#### Added

* Add `gen_ai` fields to schema as beta. #2475
* Add `device` value to `event.type` #2524

#### Improvements

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

* Fix otel urls for fieldsets with underscores. #2486

#### Added

#### Improvements

* Allow Unicode characters in generated ECS yml files. #2478
* Update semconv version used in file generation to v1.34.0 #2483

#### Deprecated

<!-- All empty sections:

## Unreleased

### Schema Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

#### Deprecated

-->
