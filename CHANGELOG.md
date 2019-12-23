<!-- Please add new changelog entries to CHANGELOG.next.md file -->

# CHANGELOG
All notable changes to this project will be documented in this file based on the [Keep a Changelog](http://keepachangelog.com/) Standard. This project adheres to [Semantic Versioning](http://semver.org/).


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
