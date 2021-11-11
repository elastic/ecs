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

#### Improvements

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

* Add `object` as fallback for `flattened` type. #1653 

#### Added

#### Improvements

* Apply yamllint and set sensible config #1661

#### Deprecated

## 8.0.0 (Feature Freeze)

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

#### Improvements

* Remove remaining Go deps after removing Go code generator. #1585
* Add explicit `default_field: true` for Beats artifacts. #1633

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
