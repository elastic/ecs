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

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

#### Deprecated


## 1.9.0 (Feature Freeze)

### Schema Changes

#### Added

* Added `http.request.id`. #1208
* Added `cloud.service.name`. #1204
* Added `hash.ssdeep`. #1169
* Added `beta` host metrics fields. #1248
* Added `geo.timezone`, `geo.postal_code`, and `geo.continent_code`. #1229
* Extended `pe` fields added to experimental schema. #1256
* Added `code_signature.team_id`, `code_signature.signing_id`. #1249
* Add `threat.indicator` fields to experimental schema. #1268
* Add `elf` fieldset to experimental schema. #1261
* `data_stream.*` fieldset introduced in experimental schema and artifacts. #1215

#### Improvements

* `user.changes.*`, `user.effective.*`, and `user.target.*` field reuses are GA. #1271
* Include formatting guidance and examples for MAC address fields. #456
* New section in ECS detailing event categorization fields usage. #1242
### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

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
