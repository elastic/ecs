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

* Added `dll.*` fields #679
* Fieldset for PE metadata. #731
* Globally unique identifier `entity_id` for `process` and `process.parent`. #747
* Added interface, vlan, observer zone fields #752
* Added `rule.author`, `rule.license` fields #754
* Added iam value for `event.category` and three related values for `event.type`. #756
* Added `file.mime_type` to include MIME type information on file structures #760

* Added fields `event.reference` and `event.url` to hold link to additional event info/actions. (#757)

#### Improvements

* Temporary workaround for Beats templates' `default_field` growing too big. #687
* Identify which fields should contain arrays of values, rather than scalar values. #727, #661
* Clarified examples and definitions regarding vulnerabilities #758
* Updated definition of `event.outcome` based on community feedback #759

#### Deprecated


### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

#### Improvements

* ECS scripts now use Python 3.6+. #674
* schema_reader.py now reliably supports chaining reusable fieldsets together. #722
* Allow the artifact generator to consider and output only a subset of fields. #737
* Add support for reusing fields in places other than the top level of the destination fieldset. #739
* Add support for specifying the directory to write the generated files. #748

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
