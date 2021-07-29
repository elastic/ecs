<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

#### Added

* Added `service.address` field. #1537
* Promote `threat.software.*` and `threat.group.*` fields to GA. #1540
* Added `service.environment` as a beta field. #1541

### Tooling and Artifact Changes

### Breaking Changes

* Removing deprecated --oss from generator #1404
* Removing use-cases directory #1405
* Remove `host.user.*` field reuse. #1439
* Remove deprecation notice on `http.request.method`. #1443
* Migrate `log.origin.file.line` from `integer` to `long`. #1533

#### Bugfixes

#### Added

* Added `file.fork_name` field. #1288
* Beta migration on some `keyword` fields to `wildcard`. #1517
* Support ES 6.x type fallback for `match_only_text` field types. #1528

#### Improvements

* Beta migration of `text` and `.text` multi-fields to `match_only_text`. #1532
#### Deprecated

## 1.11.0 (Feature Freeze)

### Schema Changes

#### Added

* `elf.*` field set added as beta. #1410
* Remove `beta` from `orchestrator` field set. #1417
* Extend `threat.*` field set beta. #1438
* Added `event.agent_id_status` field. #1454
* `process.target` and `process.target.parent` added to experimental schema. #1467
* Threat indicator fields progress to beta stage. #1471, #1504
* `threat.enrichments` beta fields. #1478, #1504

#### Improvements

* Fix ecs GitHub repo link source branch #1393
* Add --exclude flag to Generator to support field removal testing #1411
* Explicitly include user identifiers in `relater.user` description. #1420
* Improve descriptions for `cloud.region` and `cloud.availability` fields. #1452

#### Deprecated

* Note deprecation of the `host.user.*` field reuse. #1422
* Note deprecation of `log.original` superseded by `event.original` #1469

### Tooling and Artifact Changes

#### Bugfixes

* Remove `ignore_above` when `index: false` and `doc_values: false`. #1483
* Ensure `doc_values` is carried into Beats artifacts. #1488

#### Added

* Support `match_only_text` data type in Go code generator. #1418
* Support for multi-level, self-nestings. #1459
* `beta` attribute now supported on categorization allowed values. #1511

#### Improvements

* Swap `Location` and `Field Set` columns in `Field Reuse` table for better readability. #1472, #1476
* Use a bullet points to list field reuses. #1473
* Improve wording in `Threat` schema #1505

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
