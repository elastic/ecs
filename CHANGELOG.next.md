<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

#### Breaking changes

#### Bugfixes

* The `protocol` allowed value under `event.type` should not have the `expected_event_types` defined. #964

#### Added

* Added Mime Type fields to HTTP request and response. #944
* Added `threat.technique.subtechnique` to capture MITRE ATT&CK® subtechniques. #951

#### Improvements

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

* Addressed issue where foreign reuses weren't using the user-supplied `as` value for their destination. #960

#### Added

* Introduced `--strict` flag to perform stricter schema validation when running the generator script. #937

#### Improvements

* Field details Jinja2 template components have been consolidated into one template #897

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
