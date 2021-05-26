<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Breaking Changes

* Removing deprecated --oss from generator #1404
* Removing use-cases directory #1405

### Schema Changes

#### Bugfixes

#### Added

* `elf.*` field set added as beta. #1410
* Remove `beta` from `orchestrator` field set. #1417
* Advanced RFC for adding a `ticket` schema to stage 1 #1436

#### Improvements

* Fix ecs GitHub repo link source branch #1393
* Add --exclude flag to Generator to support field removal testing #1411

#### Deprecated

* Note deprecation of the `host.user.*` field reuse. #1422

### Tooling and Artifact Changes

#### Bugfixes

#### Added

* Support `match_only_text` data type in Go code generator. #1418

#### Improvements

#### Deprecated

## 1.10.0 (Feature Freeze)

### Schema Changes

#### Added

* Add `data_stream` fieldset. #1307
* Add `orchestrator` fieldset as beta fields. #1326
* Extend `threat.*` experimental fields with proposed changes from RFC 0018. #1344, #1351
* Allow custom descriptions for self-nesting reuses via `short_override` #1366

#### Improvements

* Updated descriptions to use Elastic Security #1305
* Host metrics fields from RFC 0005 are now GA. #1319
* Adjustments to the field set "usage" docs #1345
* Adjustments to the sidebar naming convention for usage and examples docs #1354
* Update `user.*` field reuse descriptions. #1382

### Tooling and Artifact Changes

#### Bugfixes

* Correcting fieldset name capitalization for generated ES template #1323

#### Improvements

* Support `nested` types in go code generator. #1254, #1350
* Go code generator now supports the `flattened` data type. #1302
* Adjustments to use terminology that doesn't have negative connotation. #1315

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
