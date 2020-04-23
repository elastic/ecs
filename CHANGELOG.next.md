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

* Add architecture and imphash for PE field set. (#763)
* Added `agent.build.*` for extended agent version information. (#764)
* Added more account and project cloud metadata. (#816)

#### Improvements

* Remove misleading pluralization in the description of `user.id`, it should
  contain one ID, not many. #801
* Clarified misleading wording about multiple IPs in src/dst or cli/srv. #804

#### Deprecated


### Tooling and Artifact Changes

#### Breaking changes

* Removed field definitions at the root of documents for fieldsets that
  had `reusable.top_level:false`. This PR affects `ecs_flat.yml`, the csv file
  and the sample Elasticsearch templates. #495, #813
* Removed the `order` attribute from the `ecs_nested.yml` and `ecs_flat.yml` files. #811

#### Bugfixes

* Subsets are created after duplicating reusable fields now so subsets can
  be applied to each reused instance independently. #753
* Quoted the example for `labels` to avoid YAML interpreting it, and having
  slightly different results in different situations. #782
* Fix incorrect listing of where field sets are nested in asciidoc,
  when they are nested deep. #784
* Allow beats output to be generated when using `--include` or `--subset` flags. #814

#### Added

#### Improvements

* Add support for reusing offical fieldsets in custom schemas. #751
* Add full path names to reused fieldsets in `nestings` array in `ecs_nested.yml`. #803
* Allow shorthand notation for including all subfields in subsets. #805

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
