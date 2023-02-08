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

## 8.7.0 (Hard Feature Freeze)

#### Bugfixes

* remove duplicated `client.domain` definition #2120

#### Added

* adding `name` field to `threat.indicator` #2121
* adding `api` option to `event.category` #2147
* adding `library` option to `event.category` #2154

#### Improvements

* description for `host.name` definition updated to encourage use of FDQN #2122

### Tooling and Artifact Changes

#### Improvements

* Updated usage docs to include `threat.indicator.url.domain` and changed `indicator.marking.tlp` and `indicator.enrichments.marking.tlp` from "WHITE" to "CLEAR" to align with TLP 2.0. #2124
* Bump `gitpython` from `3.1.27` to `3.1.30` in `/scripts`. #2139

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
