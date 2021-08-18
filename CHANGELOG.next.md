<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

#### Added

* Added `service.address` field. #1537
* Promote `threat.software.*` and `threat.group.*` fields to GA. #1540
* Added `service.environment` as a beta field. #1541
* Added `process.end` field. #1544
* Introduce container metric fields into experimental schema. #1546
* Update `user.name` and `user.id` examples for clarity. #1566
* Add `email.*` field set in the experimental fields. #1569

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

* Added `file.fork_name` field. #1288
* Beta migration on some `keyword` fields to `wildcard`. #1517
* Support ES 6.x type fallback for `match_only_text` field types. #1528

#### Improvements

* Beta migration of `text` and `.text` multi-fields to `match_only_text`. #1532, #1571
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
