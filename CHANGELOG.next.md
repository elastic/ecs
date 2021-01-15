<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes
### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

* Added `http.request.id`. #1208
* Added `cloud.service.name`. #1204
* Added `hash.ssdeep`. #1169

#### Improvements

#### Deprecated


## 1.8.0 (Feature Freeze)

### Schema Changes

#### Bugfixes

* Clean up `event.reference` description. #1181

#### Added

* Added `event.category` "registry". #1040
* Added `event.category` "session". #1049
* Added usage documentation for `user` fields. #1066
* Added `user` fields at `user.effective.*`, `user.target.*` and `user.changes.*`. #1066
* Added `os.type`. #1111

#### Improvements

* Event categorization fields GA. #1067
* `wildcard` field type adoption. #1098
* Note `[` and `]` bracket characters may enclose a literal IPv6 address when populating `url.domain`. #1131
* Reinforce the exclusion of the leading dot from `url.extension`. #1151

#### Deprecated

* Deprecated `host.user.*` fields for removal at the next major. #1066

### Tooling and Artifact Changes

#### Bugfixes

* `tracing` fields should be at root of Beats `fields.ecs.yml` artifacts. #1164

#### Added

* Added the `path` key when type is `alias`, to support the [alias field type](https://www.elastic.co/guide/en/elasticsearch/reference/current/alias.html). #877
* Added support for `scaled_float`'s mandatory parameter `scaling_factor`. #1042
* Added ability for --oss flag to fall back `constant_keyword` to `keyword`. #1046
* Added support in the generated Go source go for `wildcard`, `version`, and `constant_keyword` data types. #1050
* Added support for marking fields, field sets, or field reuse as beta in the documentation. #1051
* Added support for `constant_keyword`'s optional parameter `value`. #1112
* Added component templates for ECS field sets. #1156, #1186, #1191
* Added functionality for merging custom and core multi-fields. #982

#### Improvements

* Make all fields linkable directly. #1148
* Added a notice highlighting that the `tracing` fields are not nested under the
  namespace `tracing.` #1162
* ES 6.x template data types will fallback to supported types. #1171, #1176, #1186
* Add a documentation page discussing the experimental artifacts. #1189


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
