<!-- Please add new changelog entries to CHANGELOG.next.md file -->

# CHANGELOG
All notable changes to this project will be documented in this file based on the [Keep a Changelog](http://keepachangelog.com/) Standard. This project adheres to [Semantic Versioning](http://semver.org/).

## [1.7.0](https://github.com/elastic/ecs/compare/v1.6.0...v1.7.0)

### Schema Changes

#### Bugfixes

* The `protocol` allowed value under `event.type` should not have the `expected_event_types` defined. #964

#### Added

* Added Mime Type fields to HTTP request and response. #944
* Added network directions ingress and egress. #945
* Added `threat.technique.subtechnique` to capture MITRE ATT&CK® subtechniques. #951
* Added `configuration` as an allowed `event.category`. #963

#### Improvements

* Expanded field set definitions for `source.*` and `destination.*`. #967
* Provided better guidance for mapping network events. #969
* Added the field `.subdomain` under `client`, `destination`, `server`, `source`
  and `url`, to match its presence at `dns.question.subdomain`. #981

### Tooling and Artifact Changes

#### Bugfixes

* Addressed issue where foreign reuses weren't using the user-supplied `as` value for their destination. #960

#### Added

* Introduced `--strict` flag to perform stricter schema validation when running the generator script. #937
* Added check under `--strict` that ensures composite types in example fields are quoted. #966
* Added `ignore_above` and `normalizer` support for keyword multi-fields. #971
* Added `--oss` flag for users who want to generate ECS templates for use on OSS clusters. #991
* Added a new directory with experimental artifacts, which includes all changes
  from RFCs that have reached stage 2. #993

#### Improvements

* Field details Jinja2 template components have been consolidated into one template #897
* Add `[discrete]` marker before each section header in field details. #989


## [1.6.0](https://github.com/elastic/ecs/compare/v1.5.0...v1.6.0)

### Schema Changes

#### Bugfixes

* Field `registry.data.strings` should have been marked as an array field. #790

#### Added

* Added `x509.*` field set. #762
* Add architecture and imphash for PE field set. #763
* Added `agent.build.*` for extended agent version information. #764
* Added `log.file.path` to capture the log file an event came from. #802
* Added more account and project cloud metadata. #816
* Added missing field reuse of `pe` at `process.parent.pe` #868
* Added `span.id` to the tracing fieldset, for additional log correlation #882
* Added `event.reason` for the reason why an event's outcome or action was taken. #907
* Added `user.roles` to capture a list of role names that apply to the user. #917

#### Improvements

* Removed misleading pluralization in the description of `user.id`, it should
  contain one ID, not many. #801
* Clarified misleading wording about multiple IPs in src/dst or cli/srv. #804
* Improved verbiage about the MITRE ATT&CK® framework. #866
* Removed the default `object_type=keyword` that was being applied to `object` fields.
  This attribute is Beats-specific. It's still supported, but needs to be set explicitly
  on a case by case basis now. This default being removed affects `dns.answers`,
  `log.syslog`, `network.inner`, `observer.egress`, and `observer.ingress`. #871
* Improved attribute `dashed_name` in `generated/ecs/*.yml` to also
  replace `@` with `-`. #871
* Updated several URLs in the documentation with "example.com" domain. #910

#### Deprecated

* Deprecate guidance to lowercase `http.request.method` #840


### Tooling and Artifact Changes

#### Breaking changes

* Removed field definitions at the root of documents for fieldsets that
  had `reusable.top_level:false`. This PR affects `ecs_flat.yml`, the csv file
  and the sample Elasticsearch templates. #495, #813
* Removed the `order` attribute from the `ecs_nested.yml` and `ecs_flat.yml` files. #811
* In `ecs_nested.yml`, the array of strings that used to be in `reusable.expected`
  has been replaced by an array of objects with 3 keys: 'as', 'at' and 'full'. #864
* The subset format now requires `name` and `fields` keys at the top level. #873

#### Bugfixes

* Subsets are created after duplicating reusable fields now so subsets can
  be applied to each reused instance independently. #753
* Quoted the example for `labels` to avoid YAML interpreting it, and having
  slightly different results in different situations. #782
* Fix incorrect listing of where field sets are nested in asciidoc,
  when they are nested deep. #784
* Allow beats output to be generated when using `--include` or `--subset` flags. #814
* Field parameter `index` is now correctly populated in the Beats field definition file. #824

#### Improvements

* Add support for reusing official fieldsets in custom schemas. #751
* Add full path names to reused fieldsets in `nestings` array in `ecs_nested.yml`. #803
* Allow shorthand notation for including all subfields in subsets. #805
* Add support for Elasticsearch `enabled` field parameter. #824
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
* Jinja2 templates now define the doc structure for the AsciiDoc generator. #865
* Intermediate `ecs_flat.yml` and `ecs_nested.yml` files are now generated for each individual subset,
  in addition to the intermediate files generated for the combined subset. #873

#### Deprecated

* In `ecs_nested.yml`, we're deprecating the attribute `nestings`. It will be
  removed in a future release. The deprecated `nestings` attribute was an array of
  flat field names describing where fields are nested within the field set.
  This is replaced with the attribute `reused_here`, which is an array of objects.
  The new format still lists where the fields are nested via the same flat field name,
  but also specifies additional information about each field reuse. #864


## [1.5.0](https://github.com/elastic/ecs/compare/v1.4.0...v1.5.0)

### Schema Changes

#### Added

* Added `dll.*` fields #679
* Added `related.hash` to keep track of all hashes seen on an event. #711
* Added fieldset for PE metadata. #731
* Added `code_signature` fieldset. #733
* Added missing `hash` fields at `process.parent.hash.*`. #739
* Added globally unique identifier `entity_id` to `process` and `process.parent`. #747
* Added interface, vlan, observer zone fields #752
* Added `rule.author`, `rule.license` fields #754
* Added iam value for `event.category` and three related values for `event.type`. #756
* Added fields `event.reference` and `event.url` to hold link to additional event info/actions. #757
* Added `file.mime_type` to include MIME type information on file structures #760
* Added `event.category` value of network and associated `event.type` values. #761

#### Improvements

* Temporary workaround for Beats templates' `default_field` growing too big. #687
* Identify which fields should contain arrays of values, rather than scalar values. #727, #661
* Clarified examples and definitions regarding vulnerabilities. #758
* Updated definition of `event.outcome` based on community feedback. #759


### Tooling and Artifact Changes

#### Improvements

* ECS scripts now use Python 3.6+. #674
* schema\_reader.py now reliably supports chaining reusable fieldsets together. #722
* Allow the artifact generator to consider and output only a subset of fields. #737
* Add support for reusing fields in places other than the top level of the destination fieldset. #739
* Add support for specifying the directory to write the generated files. #748


## [1.4.0](https://github.com/elastic/ecs/compare/v1.3.1...v1.4.0)

### Schema Changes

#### Added

* Added default `text` analyzer as a multi-field to `user_agent.original`. #575
* Added `file.attributes`. #611
* Added `file.drive_letter`. #620
* Added `rule` fields. #665
* Added default `text` analyzer as a multi-field to around 25 more fields. #680
* Added `registry.*` fieldset for the Windows registry. #673
* Publish initial list of allowed values for the categorization fields (previously reserved)
  `event.kind`, `event.category`, `event.type` and `event.outcome`. #684, #691, #692
* Added `related.user` #694


### Tooling and Artifact Changes

#### Bugfixes

* Fix support for multi-fields. #575


## [1.3.1](https://github.com/elastic/ecs/compare/v1.3.0...v1.3.1)

### Schema Changes

#### Bugfixes

* Removed unnecessary field `tls.server.supported_ciphers`. #662


## [1.3.0](https://github.com/elastic/ecs/compare/v1.2.0...v1.3.0)

### Schema Changes

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

### Tooling and Artifact Changes

#### Breaking changes

* Changed the order and column names in the csv. #621
* Removed the file `schema.json` and the code generating it. #627
* Removed the legacy Elasticsearch template. #629
  * Note: The *good* Elasticsearch templates are available in directory
    `generated/elasticsearch`, this PR only removes an obsolete file.

#### Added

* Added the "Indexed", "Field\_Set" and "Description" columns to the csv. #621


## [1.2.0](https://github.com/elastic/ecs/compare/v1.1.0...v1.2.0)

### Added

* Added `threat.*` fields to apply a taxonomy to events and alerts. #505
* Added fields in `log.*` to allow for full Syslog mapping. #525
* Added `package.*` to installed software packages. #532
* Added `registered_domain` to `url`, `source`, `destination`, `client`, and `server`. #533
* Added `top_level_domain` field to `url`, `dns.question`,
  `source`, `destination`, `client`, and `server`. #542, #572
* Added `group.domain` field. #547
* Added `url.extension`. #551, #573
* Added `observer.name` and `observer.product`. #557, #571
* Added `dns.question.subdomain` field. #561, #574
* Added `error.stack_trace` field. #562
* Added `log.origin.file.name`, `log.origin.function` and `log.origin.file.line` fields. #563, #568
* Added `service.node.name` to allow distinction between different nodes of the
  same service running on the same host. #565
* Added `error.type` field. #566


## [1.1.0](https://github.com/elastic/ecs/compare/v1.0.1...v1.1.0)

### Added

* Added `as` fields for Autonomous System information (i.e. ASN). #341
* Added field formats to all `.bytes` fields and `event.duration`. #385, #425
* Added `hash.*` field set. #426
* Added `dns.*` field set, to describe DNS traffic. #438
* Added `event.code`, `event.sequence` and `event.provider`. #439
* Added `file.name` and `file.directory`. #441
* Added `file.created`, and `file.accessed`. #445
* Added `process.uptime` and `host.uptime` fields. #477
* Added `domain` field to user. #486
* Added `.nat.ip` and `.nat.port` to `source`, `destination`, `client` and `server`. #491
* Added `process.thread.name` field. #517
* Added `trace.id` and `transaction.id` fields for tracing across different services. #519
* Added `log.logger` field. #521

### Improvements

* Added examples and improved definitions of many `file` fields. #441
* Changed the `service.id` description so it works better for clustered services. #502


## [1.0.1](https://github.com/elastic/ecs/compare/v1.0.0...v1.0.1)

### Added

* Add generated source code for Go. #249
* Translate the documentation from README.md, to the main website. #266, #334, #400, #430, #437
* New generator that supports reusable fields, for files based on ECS.
  It generates schema.csv, Elasticsearch 6 and 7 templates, and field documentation
  for the main website. #336
* Generator for the asciidoc rendering of field definitions. #347
* Generator for the Beats fields.ecs.yml file. #379
* Remove many legacy generated files. #399
* Specify static output format for event.duration. #425
* Format port numbers and numeric IDs as strings. #454
* Add example for `process.pid` and `process.ppid`. #464, #470


## [1.0.0](https://github.com/elastic/ecs/compare/v1.0.0-beta2...v1.0.0)

### Breaking changes

* Remove the `user.group` `keyword` field, introduced in #204. Instead,
  the `group` field set can be nested at `user.group`. #308

### Bugfixes

* Field set name "group" was being used as a leaf field at `user.group`, instead
  of being a nesting of the field set. This goes against a driving principle of ECS,
  and has been corrected. #308
* Replaced incorrect examples in `cloud.provider`. #330, #348
* Changed the `url.port` type to `long`. #339

### Added

* Added pointer in description of `http` field set to `url` field set. #330
* Added an optional short field description. #330

### Improvements

* Clarified the definition of the host fields #325
* Clarified the difference between `@timestamp` and `event.created`. #329
* Make phrasing of lowercasing directive more relevant, no matter where it's shown. #332
* Specify the `object_type` for field `labels`. #331
* Loosen up definition of `geo` field set. Not necessarily geo-ip based, since `geo.name`. #333
* Clarified guidelines on ID fields. #349


## [1.0.0-beta2](https://github.com/elastic/ecs/compare/v1.0.0-beta1...v1.0.0-beta2)

### Breaking changes

* Changed `device.*` fields to `observer.*` fields to eliminate user confusion. #238
* Rename `network.total.bytes` to `network.bytes` and `network.total.packets`
  to `network.packets`. #179
* Remove `network.inbound.bytes`, `network.inbound.packets`,
  `network.outbound.bytes` and `network.outbound.packets`. #179
* Changed the `event.type` definition to be only reserved. #242

### Bugfixes

* Fix obvious mistake in the definition of "source", where it said "destination"
  instead of "source". #211

### Added

* Add `host.name` field and clarify usage of `host.hostname`. #187
* Add `event.start` and `event.end` date fields. #185
* Add `process.thread.id` field. #200
* Add `host.name` field and clarify usage of `host.hostname`.
* Add `event.start` and `event.end` date fields.
* Create new `related` field set with `related.ip`. #206
* Add `user.group` field. #204
* Create new `group` field set with `group.id` and `group.name`. #203
* Add `url.full` field. #207
* Add `process.executable` field. #209
* Add `process.working_directory` and `process.start`. #215
* Reintroduce `http`. #237
  * Move `http.response.body` to `http.response.body.content`. #239
  * Add `http.request.body.content`. #239
  * Add HTTP size metric fields. #239
* Add `user.full_name` field. #201
* Add `network.community_id` field. #208
* Add fields `geo.country_name` and `geo.region_iso_code`. #214
* Add `event.kind` and `event.outcome`. #242
* Add `client` and `server` objects and fields. #236
* Reintroduce a streamlined `user_agent` field set. #240, #262
* Add `geo.name` for ad hoc location names. #248
* Add `event.timezone` to allow for proper interpretation of incomplete timestamps. #258
* Add fields `source.address`, `destination.address`, `client.address`, and
  `server.address`. #247
* Add `os.full` to capture full OS name, including version. #259
* Add generated source code for Go. #249

### Improvements

* Improved the definition of the file fields #196
* Improved the definition of the agent fields #192
* Improve definition of events, logs, and metrics in event section #194
* Improved the definition of network fields in intro section #197
* Improved the definition of host fields #195
* Improved the definitions for `event.category` and `event.action`. #242
* Clarify the semantics of `network.direction`. #212
* Add `source.bytes`, `source.packets`, `destination.bytes` and `destination.packets`. #179
* Add a readme section to declare some top level field sets are reserved for
  future use. #257
* Clarify that `network.transport`, `network.type`, `network.application`,
  and `network.protocol` must be lowercase. #251
* Clarify that `http.request.method` must be lowercase. #251
* Clarify that source/destination should be filled, even if client/server is
  being used. #265


## [1.0.0-beta1](https://github.com/elastic/ecs/compare/v0.1.0...v1.0.0-beta1)

### Breaking changes

* Change structure of URL. #7
* Rename `url.href` `multi_field`. #18
* Rename `geoip.*` to `geo`. #58
* Rename log.message to log.original. #106
* Rename `event.raw` to `event.original`. #107
* Rename `user_agent.raw` to `user_agent.original` and make it a keyword. #107
* Rename `file.path.raw` to `file.path.keyword`, `file.target_path.raw` to `file.target_path.keyword`,
  `url.href.raw` to `url.href.keyword`, `url.path.raw` to `url.path.keyword`,
  `url.query.raw` to `url.query.keyword`, and `network.name.raw` to `network.name.keyword`. #103
* Remove `log.offset` and `log.line` as too specific for ECS. #131
* Remove top level objects `kubernetes` and `tls`. #132
* Remove `*.timezone.offset.sec` fields as too specific for ECS at the moment. #134
* Make the following fields keyword: device.vendor, file.path, file.target_path, http.response.body, network.name, organization.name, url.href, url.path, url.query, user_agent.original
* Rename `url.host.name` to `url.hostname` to better align with industry convention. #147
* Make the following fields keyword: device.vendor, file.path, file.target_path, http.response.body, network.name, organization.name, url.href, url.path, url.query, user_agent.original. #137
  * Only two fields using `text` indexing at this time are `message` and `error.message`.
* Rename `host.name` to `host.hostname` to better align with industry convention. #144
* Update definition of `service.type` and `service.name`.
* Redefine purpose of `agent.name` field to be user defined field.
* Rename `url.href` to `url.original`.
* Remove `source.subdomain` and `destination.subdomain` fields.
* Rename `event.version` to `ecs.version`. #169
* Remove the `http` field set temporarily. #171
* Remove the `user_agent` field set temporarily. #172
* Rename `url.hostname` to `url.domain`. #175
* Remove `source.hostname` and `destination.hostname`. #175

### Added

* Add `network.total.packets` and `network.total.bytes` field. PR#2
* Add `event.action` field. #21
* Add `network.name`, to track network names in the monitoring pipeline. #25
* Adds cloud.account.id for top level organizational level. #11
* Add `http.response.status_code` and `http.response.body` fields. #4
* Add fields for Operating System data. #5
* Add `log.message`. #3
* Add http.request.method and http.version
* Add `host.os.kernel` containing the OS kernel version. #60
* Add `agent.type` field.
* Add `http.request.referrer` field. #164
* Add `network.type`, `network.iana_number`, `network.transport` and
  `network.application`. #81 and #170

### Improvements

* Remove duplicate definitions of the reuseable `os` field set from `host.os` and
  `user_agent.os`.  #168


## 0.1.0

Initial draft release
