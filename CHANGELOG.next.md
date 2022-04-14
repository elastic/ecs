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

#### Removed

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

#### Deprecated

## 8.3.0 (Soft Feature Freeze)

### Schema Changes

#### Breaking changes

#### Bugfixes

#### Added

* Added `pattern` attribute to `.mac` fields. #1871
* Add `orchestrator.cluster.id` #1875
* Add `orchestrator.resource.id` #1878

#### Improvements

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

#### Deprecated

## 8.2.0 (Hard Feature Freeze)

### Schema Changes

#### Added

* Add beta `container.*` metric fields. #1789
* Add six new syslog fields to `log.syslog.*`. #1793
* Added `faas.id`, `faas.name` and `faas.version` fields as beta. #1796
* Added linux event model beta fields and reuses to support RFC 0030. #1842, #1847
* Added `threat.feed.dashboard_id`, `threat.feed.description`, `threat.feed.name`, `threat.feed.reference` fields. #1844

#### Improvements

* `email.*` field set now GA. #1794, #1841

### Tooling and Artifact Changes

#### Added

* Adding optional field attribute, `pattern`. #1834
* Added support for re-using a fieldset as an array. #1838

#### Improvements

* Update refs from master to main in USAGE.md etc #1658
* Clean up trailing spaces and additional newlines in schemas #1667
* Use higher compression as default in composable index template settings. #1712

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
