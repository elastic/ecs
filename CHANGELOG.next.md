<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

#### Breaking changes

#### Bugfixes

* remove duplicated `client.domain` definition #212

#### Added

* adding `name` field to `threat.indicator` #2121

#### Improvements
* Updated usage docs to include `threat.indicator.url.domain` and changed `indicator.marking.tlp` and `indicator.enrichments.marking.tlp` from "WHITE" to "CLEAR" to align with TLP 2.0. #2124

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
