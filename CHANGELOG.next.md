<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

#### Breaking changes

* Remove deprecated fields from previous major release; `process.pgid`, `service.node.role`, and inherited users. #2410

#### Bugfixes

* Fix link rendering issues and usage of http in links. #2423

#### Added
* Add `origin_referrer_url` and `origin_url` fields, which indicate the origin information to the file, process and dll schemas #2441

#### Improvements
* Allow ECS from any directory #2019
* Added ability to specify a prefix for es_templates #2019
* Allow projects to create their own ACSIIDOC templates #2019


* Promote beta fields to GA. #2411
* Define base encoding of `x509.serial_number`. #2383
* Restrict the encoding of `x509.serial_number` to base 16. #2398
* Set synthetic_source_keep = none on fields that represent sets. #2422
* Increase ignore_above value for url.query. #2424

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

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
