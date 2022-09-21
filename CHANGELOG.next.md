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

#### Added

#### Improvements

#### Deprecated

## 8.5.0 (Hard Feature Freeze)

### Schema Changes

#### Added

* Adding `risk.*` fields as experimental. #1994, #2010
* Adding `process.io.*` as beta fields. #1956, #2031
* Adding `process.tty.rows` and `process.tty.columns` as beta fields. #2031
* Changed `process.env_vars` field type to be an array of keywords. #2038
* `process.attested_user` and `process.attested_groups` as beta fields. #2050
* Added `risk.*` fieldset to beta. #2051

#### Improvements

* Advances `threat.enrichments.indicator` to GA. #1928
* Added `ios` and `android` as valid values for `os.type` #1999

### Tooling and Artifact Changes

#### Bugfixes

* Added Deprecation Warning for `misspell` task #1993

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
