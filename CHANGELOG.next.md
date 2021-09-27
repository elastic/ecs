<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

#### Breaking changes

* Remove `host.user.*` field reuse. #1439
* Remove deprecation notice on `http.request.method`. #1443
* Migrate `log.origin.file.line` from `integer` to `long`. #1533

#### Bugfixes

#### Added

#### Improvements

#### Deprecated

### Tooling and Artifact Changes

#### Breaking Changes

* Removing deprecated --oss from generator #1404
* Removing use-cases directory #1405

#### Bugfixes

#### Added

#### Improvements

#### Deprecated

## 1.12.0 (Feature Freeze)

### Schema Changes

#### Bugfixes

* Updating `hash` order to correct nesting. #1603
* Removing incorrect `hash` reuses. #1604
* Updating `pe` order to correct nesting. #1605
* Removing incorrect `pe` reuses. #1606
* Correcting `enrichments` to an `array` type. #1608

#### Added

* Added `file.fork_name` field. #1288
* Added `service.address` field. #1537
* Added `service.environment` as a beta field. #1541
* Added `process.end` field. #1544
* Added container metric fields into experimental schema. #1546
* Add `code_signature.digest_algorithm` and `code_signature.timestamp` fields. #1557
* Add `email.*` field set in the experimental fields. #1569

#### Improvements

* Beta migration on some `keyword` fields to `wildcard`. #1517
* Promote `threat.software.*` and `threat.group.*` fields to GA. #1540
* Update `user.name` and `user.id` examples for clarity. #1566
* Beta migration of `text` and `.text` multi-fields to `match_only_text`. #1532, #1571

### Tooling and Artifact Changes

#### Added

* Support ES 6.x type fallback for `match_only_text` field types. #1528

#### Bugfixes

* Prevent failure if no files need to be deleted `find | xargs rm`. #1588
#### Improvements

* Document field type family interoperability in FAQ. #1591

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
