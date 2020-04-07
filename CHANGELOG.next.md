<!-- When adding an entry to the Changelog:

- Please follow the Keep a Changelog: http://keepachangelog.com/ guidelines.
- Please insert your changelog line ordered by PR ID.
- Make sure you add your entry to the correct section (schema or tooling).

Thanks, you're awesome :-) -->

## Unreleased

### Schema Changes

* Added `log.file.path` to capture the log file an event came from. #802

#### Breaking changes

#### Bugfixes

* Field `registry.data.strings` should have been marked as an array field. #790

#### Added

* Added `search.*` fields #729
* Add architecture and imphash for PE field set. (#763)
* Added `agent.build.*` for extended agent version information. (#764)

#### Improvements

* Remove misleading pluralization in the description of `user.id`, it should
  contain one ID, not many. #801
* Clarified misleading wording about multiple IPs in src/dst or cli/srv. #804

#### Deprecated


### Tooling and Artifact Changes

#### Breaking changes

#### Bugfixes

* Quoted the example for `labels` to avoid YAML interpreting it, and having
  slightly different results in different situations. #782
* Fix incorrect listing of where field sets are nested in asciidoc,
  when they are nested deep. #784

#### Added

#### Improvements

* Add support for reusing offical fieldsets in custom schemas. #751
* Add full path names to reused fieldsets in `nestings` array in ecs_nested.yml. #803

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
