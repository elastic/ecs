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

* `tracing` fields should be at root of Beats `fields.ecs.yml` artifacts. #1164

#### Added

* Added component templates for ECS field sets. #1156, #1186

#### Improvements

* Added a notice highlighting that the `tracing` fields are not nested under the
  namespace `tracing.` #1162
* Add --exclude flag to Generator to support field removal testing #1411

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
