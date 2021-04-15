<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

#### Breaking changes

#### Bugfixes

#### Added

* Add `orchestrator` fieldset as beta fields. #1326
* Extend `threat.*` experimental fields with proposed changes from RFC 0018. #1344, #1351

#### Improvements

* Updated descriptions to use Elastic Security #1305
* Host metrics fields from RFC 0005 are now GA. #1319
* Adjustments to the field set "usage" docs #1345
* Adjustments to the sidebar naming convention for usage and examples docs #1354

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

* Correcting fieldset name capitalization for generated ES template #1323

#### Added

#### Improvements

* Support `nested` types in go code generator. #1254, #1350
* Go code generator now supports the `flattened` data type. #1302
* Adjustments to use terminology that doesn't have negative connotation. #1315

#### Deprecated

<!-- All empty sections:

## Unreleased

### Schema Changes
### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

#### Deprecated

-->
