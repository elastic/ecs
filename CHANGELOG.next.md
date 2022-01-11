<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

#### Breaking changes

#### Bugfixes

* Fixed the `default_field` flag for root fields in Beats generator. #1711

#### Added

#### Improvements

#### Deprecated

#### Removed

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

#### Deprecated

## 8.1.0 (Soft Feature Freeze)

### Schema Changes

#### Added

* Added two new fields (sha384,tlsh) to hash schema and one field to pe schema (pehash). #1678
* Added `email.*` beta field set. ##1688, #1705

#### Removed

- Removing `process.target.*` reuses from experimental schema. #1666
- Removing RFC 0014 `pe.*` fields from experimental schema. #1670

### Tooling and Artifact Changes

#### Bugfixes

* Add `object` as fallback for `flattened` type. #1653

#### Improvements

* Update refs from master to main in USAGE.md etc #1658
* Clean up trailing spaces and additional newlines in schemas #1667

## 8.0.0 (Hard Feature Freeze)

### Schema Changes

#### Breaking changes

* Remove `host.user.*` field reuse. #1439
* Remove deprecation notice on `http.request.method`. #1443
* Migrate `log.origin.file.line` from `integer` to `long`. #1533
* Remove `log.original` field. #1580
* Remove `process.ppid` field. #1596

#### Added

* Added `faas.*` field set as beta. #1628

#### Improvements

* Wildcard type field migration GA. #1582
* `match_only_text` type field migration GA. #1584
* Threat indicator fields GA from RFC 0008. #1586

### Tooling and Artifact Changes

#### Breaking Changes

* Removing deprecated --oss from generator #1404
* Removing use-cases directory #1405
* Remove Go code generator. #1567
* Remove template generation for ES6. #1680
* Update folder structure for generated ES artifacts. #1700

#### Improvements

* Align input options for --include and --subset arguments #1519
* Remove remaining Go deps after removing Go code generator. #1585
* Add explicit `default_field: true` for Beats artifacts. #1633
* Reorganize docs directory structure. #1679

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
