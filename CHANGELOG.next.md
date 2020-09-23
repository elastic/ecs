<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

* Added `threat.technique.subtechnique` to capture MITRE ATT&CK® subtecqhniques. #951

#### Breaking changes

#### Bugfixes

* The `protocol` allowed value under `event.type` should not have the `expected_event_types` defined. #964

#### Added

* Added Mime Type fields to HTTP request and response. #944

#### Improvements

* Expanded field set definitions for `source.*` and `destination.*`. #967

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

* Addressed issue where foreign reuses weren't using the user-supplied `as` value for their destination. #960

#### Added

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
