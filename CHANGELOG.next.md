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
* Added `x509.*` field set. (#762)
* Added more account and project cloud metadata. (#816)
* Added missing field reuse of `pe` at `process.parent.pe` #868

#### Improvements

* Remove misleading pluralization in the description of `user.id`, it should
  contain one ID, not many. #801
* Clarified misleading wording about multiple IPs in src/dst or cli/srv. #804
* Improved verbiage about the MITRE ATT&CK® framework. #866
* Remove the default `object_type=keyword` that was being applied to `object` fields.
  This attribute is Beats-specific. It's still supported, but needs to be set explicitly
  on a case by case basis now. This default being removed affects `dns.answers`,
  `log.syslog`, `network.inner`, `observer.egress`, and `observer.ingress`. #871

#### Deprecated

* Deprecate guidance to lowercase `http.request.method` #840
* In `ecs_nested.yml`, we're deprecating the attribute `nestings`. It will be
  removed in a future release. The deprecated `nestings` attribute was an array of
  flat field names describing where fields are nested within the field set.
  This is replaced with the attribute `reused_here`, which is an array of objects.
  The new format still lists where the fields are nested via the same flat field name,
  but also specifies additional information about each field reuse.


### Tooling and Artifact Changes

#### Breaking changes

* Removed field definitions at the root of documents for fieldsets that
  had `reusable.top_level:false`. This PR affects `ecs_flat.yml`, the csv file
  and the sample Elasticsearch templates. #495, #813
* Removed the `order` attribute from the `ecs_nested.yml` and `ecs_flat.yml` files. #811
* In `ecs_nested.yml`, the array of strings that used to be in `reusable.expected`
  has been replaced by an array of objects with 3 keys: 'as', 'at' and 'full'. #864

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
* Add `ref` option to generator allowing schemas to be built for a specific ECS version. #851
* Add `template-settings` and `mapping-settings` options to allow override of defaults in generated ES templates. #856
* When overriding ECS field sets via the `--include` flag, it's no longer necessary
  to duplicate the field set's mandatory attributes. The customizations are merged
  before validation. #864
* Add ability to nest field sets as another name. #864
* Add ability to nest field sets within themselves (e.g. `process` => `process.parent`). #864
* New attribute `reused_here` is added in `ecs_nested.yml`. It obsoletes the
  previous attribute `nestings`, and is able to fully capture details of other
  field sets reused under this one. #864
* When chained reuses are needed (e.g. `group` => `user`, then `user` => many places),
  it's now necessary to force the order with new attribute `reusable.order`. This
  attribute is otherwise optional. It's currently only needed for `group`. #864
* There's a new representation of ECS at `generated/ecs/ecs.yml`, which is a deeply nested
  representation of the fields. This file is not in git, as it's only meant for
  developers working on the ECS tools. #864

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
