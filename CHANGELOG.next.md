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

#### Removed

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

* Adding release notes section into ECS docs. #1800

#### Improvements

#### Deprecated

## 8.1.0 (Hard Feature Freeze)

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
* Fix invalid documentation link generation in component templates `_meta`. #1728

#### Improvements

* Update refs from master to main in USAGE.md etc #1658
* Clean up trailing spaces and additional newlines in schemas #1667
* Use higher compression as default in composable index template settings. #1712
* Bump dependencies. #1782

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
