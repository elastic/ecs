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

* Added default `text` analyzer as a multi-field to `user_agent.original`. #575
* Added `file.attributes`. #611
* Added `file.drive_letter`. #620
* Added `rule` fields. #665
* Added default `text` analyzer as a multi-field to around 25 more fields. #680
* Added `registry.*` fieldset for the Windows registry. #673
* Publish initial list of allowed values for the reserved fields `event.kind`,
  `event.category`, `event.type` and `event.outcome`. #684, #691, #692

#### Improvements

#### Deprecated


### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

* Fix support for multi-fields. #575

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
