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

* Added `event.category` "registry". #1040
* Added `event.category` "session". #1049
* Added usage documentation for `user` fields. #1066
* Added `user` fields at `user.effective.*`, `user.target.*` and `user.changes.*`. #1066
* Added `os.type`. #1111

#### Improvements

#### Deprecated

* Deprecated `host.user.*` fields for removal at the next major. #1066

### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

#### Added

* Added ability to supply free-form usage documentation per fieldset. #988
* Added the `path` key when type is `alias`, to support the [alias field type](https://www.elastic.co/guide/en/elasticsearch/reference/current/alias.html). #877
* Added support for `scaled_float`'s mandatory parameter `scaling_factor`. #1042
* Added ability for --oss flag to fall back `constant_keyword` to `keyword`. #1046
* Added support in the generated Go source go for `wildcard`, `version`, and `constant_keyword` data types. #1050
* Added support for marking fields, field sets, or field reuse as beta in the documentation. #1051
* Added support for `constant_keyword`'s optional parameter `value`. #1112

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
