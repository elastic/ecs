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

* Added `device.*` field set as beta. #2030

#### Improvements

* Added `CLEAR` and `AMBER+STRICT` as valid values for `threat.indicator.marking.tlp` to accept new [TLP 2.0](https://www.first.org/tlp/) markings - [#2022](https://github.com/elastic/ecs/issues/2022)

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

#### Deprecated

## 8.5.0 (Soft Feature Freeze)

### Schema Changes

#### Breaking changes

#### Bugfixes

#### Added

* Adding `risk.*` fields as experimental. #1994, #2010
* Adding `process.io.*` as beta fields. #1956, #2031
* Adding `process.tty.rows` and `process.tty.columns` as beta fields. #2031
* Changed `process.env_vars` field type to be an array of keywords. #2038
* `process.attested_user` and `process.attested_groups` as beta fields. #2050
* Added `risk.*` fieldset to beta. #2051, #2058

#### Improvements

* Advances `threat.enrichments.indicator` to GA. #1928
* Added `ios` and `android` as valid values for `os.type` #1999

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

* Added Deprecation Warning for `misspell` task #1993

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
