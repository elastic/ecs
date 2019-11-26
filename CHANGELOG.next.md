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

* Added `vulnerability.*` fields to represent vulnerability information. #581
* Added `event.ingested` as the ingest timestamp. #582
* Added `package.reference`. #585
* Added `package.build_version`. #586
* Added `package.type`. #587
* Added `host.domain` field. #591
* Added `process.command_line`. #599
* Added `process.exit_code`. #600
* Added fields in `tls.*` to support analysis of TLS protocol events. #606
* Added `process.parent.*`. #612
* Added `process.args_count`. #615

#### Improvements

#### Deprecated


### Tooling and Artifact Changes

#### Breaking changes

* Changed the order and column names in the csv. #621
* Removed the file `schema.json` and the code generating it. #627
* Removed the legacy Elasticsearch template. #629
  * Note: The *good* Elasticsearch templates are available in directory
    `generated/elasticsearch`, this PR only removes an obsolete file.

#### Bugfixes

#### Added

* Added the "Indexed", "Field\_Set" and "Description" columns to the csv. #621

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
