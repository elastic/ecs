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
* Added `container.security_context.privileged` to indicated whether a container was started in privileged mode. #2219, #2225
* Added `process.thread.capabilities.permitted` to contain the current thread's possible capabilities. #2245
* Added `process.thread.capabilities.effective` to contain the current thread's effective capabilities. #2245

#### Improvements
* Permit `ignore_above` if explicitly set on a `flattened` field. #2248

#### Deprecated

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

#### Deprecated

## 8.9.0 (Feature Freeze)

### Schema Changes

### Bugfixes

#### Added
* Added `process.vpid` for namespaced process ids. #2211

### Improvements

#### Deprecated
* Removed `faas.trigger: nested` since we only have one trigger. #2194

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
