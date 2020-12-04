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

<<<<<<< HEAD
* Add `orchestrator` fieldset to experimental schema. #1292
=======
* Added Mime Type fields to HTTP request and response. #944
* Added `threat.technique.subtechnique` to capture MITRE ATT&CK® subtechniques. #951
* Added `configuration` as an allowed `event.category`. #963
* Added network directions ingress and egress. #945
>>>>>>> 50167fb4 (Stage 2 RFC Updates)

#### Improvements

* Updated descriptions to use Elastic Security #1305
* Host metrics fields from RFC 0005 are now GA. #1319

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

* Correcting fieldset name capitalization for generated ES template #1323

#### Added

#### Improvements

* Go code generator now supports the `flattened` data type. #1302
* Adjustments to use terminology that doesn't have negative connotation. #1315

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
