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

## 8.6.0 (Hard Feature Freeze)

### Schema Changes

#### Added

* Adding `vulnerability` option for `event.category`. #2029
* Added `device.*` field set as beta. #2030
* Added `tlp.version` to threat #2074
* Added fields for executable object format metadata for ELF, Mach-O and PE #2083

#### Improvements

* Added `CLEAR` and `AMBER+STRICT` as valid values for `threat.indicator.marking.tlp` and `enrichments.indicator.marking.tlp` to accept new [TLP 2.0](https://www.first.org/tlp/) markings #2022, #2074

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
