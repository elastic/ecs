<!-- Please add new changelog entries to CHANGELOG.next.md file -->

# CHANGELOG
All notable changes to this project will be documented in this file based on the [Keep a Changelog](http://keepachangelog.com/) Standard. This project adheres to [Semantic Versioning](http://semver.org/).

## [8.11.0](https://github.com/elastic/ecs/compare/v8.10.0...v8.11.0)

### Schema Changes

#### Bugfixes

* Remove `expected_values` from `threat.*.indicator.name` fields. #2281

#### Added

* Added `volume.*` as beta field set. #2269

### Tooling and Artifact Changes

#### Bugfixes

* Respect reusable.top_level in Beats generator #2278

## [8.10.0](https://github.com/elastic/ecs/compare/v8.9.0...v8.10.0)

### Schema Changes

#### Added

* Added `container.security_context.privileged` to indicated whether a container was started in privileged mode. #2219, #2225, #2246
* Added `process.thread.capabilities.permitted` to contain the current thread's possible capabilities. #2245
* Added `process.thread.capabilities.effective` to contain the current thread's effective capabilities. #2245

#### Improvements

* Permit `ignore_above` if explicitly set on a `flattened` field. #2248

### Tooling and Artifact Changes

#### Improvements

* Improved documentation formatting to better follow the contributing guide. #2226
* Bump `gitpython` dependency from 3.1.30 to 3.1.35 for security fixes. #2251, #2264, #2265

## [8.9.0](https://github.com/elastic/ecs/compare/v8.8.0...v8.9.0)

### Schema Changes

### Bugfixes

#### Added
* Added `process.vpid` for namespaced process ids. #2211

### Improvements

#### Deprecated
* Removed `faas.trigger: nested` since we only have one trigger. #2194

## [8.8.0](https://github.com/elastic/ecs/compare/v8.7.0...v8.8.0)

### Schema Changes

#### Added

* Add `event.type: access` as an allowed value for `event.category: file`. #2174
* Add `orchestrator.resource.annotation` and `orchestrator.resource.label`. #2181
* Add `event.kind: asset` as a beta category. #2191

### Tooling and Artifact Changes

#### Added

* Add `parameters` property for field definitions, to provide any mapping parameter. #2084

## [8.7.0](https://github.com/elastic/ecs/compare/v8.6.1...v8.7.0)

### Schema Changes

#### Bugfixes

* remove duplicated `client.domain` definition #2120

#### Added

* adding `name` field to `threat.indicator` #2121
* adding `api` option to `event.category` #2147
* adding `library` option to `event.category` #2154

#### Improvements

* description for `host.name` definition updated to encourage use of FDQN #2122

### Tooling and Artifact Changes

#### Improvements

* Updated usage docs to include `threat.indicator.url.domain` and changed `indicator.marking.tlp` and `indicator.enrichments.marking.tlp` from "WHITE" to "CLEAR" to align with TLP 2.0. #2124
* Bump `gitpython` from `3.1.27` to `3.1.30` in `/scripts`. #2139

## [8.6.1](https://github.com/elastic/ecs/compare/v8.6.0...v8.6.1)

### Schema Changes

#### Bugfixes

* Fixing `tlp_version` and `tlp` field for threat. #2156

## [8.6.0](https://github.com/elastic/ecs/compare/v8.5.2...v8.6.0)

### Schema Changes

#### Added

* Adding `vulnerability` option for `event.category`. #2029
* Added `device.*` field set as beta. #2030
* Added `tlp.version` to threat #2074
* Added fields for executable object format metadata for ELF, Mach-O and PE #2083

#### Improvements

* Added `CLEAR` and `AMBER+STRICT` as valid values for `threat.indicator.marking.tlp` and `enrichments.indicator.marking.tlp` to accept new [TLP 2.0](https://www.first.org/tlp/) markings #2022, #2074

## [8.5.2](https://github.com/elastic/ecs/compare/v8.5.1...v8.5.2)

### Schema Changes

#### Bugfixes

* Fixes invalid `number` type on 4 `process.io` subfields. #2105

## [8.5.1](https://github.com/elastic/ecs/compare/v8.5.0...v8.5.1)

### Tooling and Artifact Changes

#### Bugfixes

* Fix type of `normalize` in `process.io.bytes_skipped`. #2094

## [8.5.0](https://github.com/elastic/ecs/compare/v8.4.0...v8.5.0)

### Schema Changes

#### Added

* Adding `risk.*` fields as experimental. #1994, #2010
* Adding `process.io.*` as beta fields. #1956, #2031
* Adding `process.tty.rows` and `process.tty.columns` as beta fields. #2031
* Changed `process.env_vars` field type to be an array of keywords. #2038
* `process.attested_user` and `process.attested_groups` as beta fields. #2050
* Added `risk.*` fieldset to beta. #2051, #2058
* Moved Linux event model fields to GA. #2082

#### Improvements

* Advances `threat.enrichments.indicator` to GA. #1928
* Added `ios` and `android` as valid values for `os.type` #1999

### Tooling and Artifact Changes

#### Bugfixes

* Added Deprecation Warning for `misspell` task #1993
* Fix typo in client schema #2014

## [8.4.0](https://github.com/elastic/ecs/compare/v8.3.1...v8.4.0)

### Schema Changes

#### Added

* Initial set of `expected_values`. #1962
* Adding `service.node.roles`. #1981

### Tooling and Artifact Changes

#### Added

* Introduce `expected_values` attribute. #1952

#### Improvements

* Additional type annotations. #1950

## [8.3.1](https://github.com/elastic/ecs/compare/v8.3.0...v8.3.1)

### Schema Changes

#### Deprecated

* Deprecate `service.node.role` in favor of upcoming `service.node.roles`. #1976

## [8.3.0](https://github.com/elastic/ecs/compare/v8.2.1...v8.3.0)

### Schema Changes

#### Added

* Added `pattern` attribute to `.mac` fields. #1871
* Add `orchestrator.cluster.id` #1875
* Add `orchestrator.resource.id` #1878
* Add `orchestrator.resource.parent.type` #1889
* Add `orchestrator.resource.ip` #1889
* Add `container.image.hash.all` #1889
* Add `service.node.role` #1916
* Advanced `container.*` metric fields to GA. #1927

## [8.2.1](https://github.com/elastic/ecs/compare/v8.2.0...v8.2.1)

### Schema Changes

#### Bugfixes

* Adding missing process fields for documentation. #1906

### Tooling and Artifact Changes

#### Improvements

* Add type hints to `schema` modules. #1771
* Support `docs_only` param to subset defs. #1909

## [8.2.0](https://github.com/elastic/ecs/compare/v8.1.0...v8.2.0)

### Schema Changes

#### Added

* Add beta `container.*` metric fields. #1789
* Add six new syslog fields to `log.syslog.*`. #1793
* Added `faas.id`, `faas.name` and `faas.version` fields as beta. #1796
* Added linux event model beta fields and reuses to support RFC 0030. #1842, #1847, #1884
* Added `threat.feed.dashboard_id`, `threat.feed.description`, `threat.feed.name`, `threat.feed.reference` fields. #1844

#### Improvements

* `email.*` field set now GA. #1794, #1841

### Tooling and Artifact Changes

#### Added

* Adding optional field attribute, `pattern`. #1834
* Added support for re-using a fieldset as an array. #1838
* Added `--force-docs` option to generator. #1879

#### Improvements

* Update refs from master to main in USAGE.md etc #1658
* Clean up trailing spaces and additional newlines in schemas #1667
* Use higher compression as default in composable index template settings. #1712

## [8.1.0](https://github.com/elastic/ecs/compare/v8.0.1...v8.1.0)

### Schema Changes

#### Added

* Added two new fields (sha384,tlsh) to hash schema and one field to pe schema (pehash). #1678
* Added `email.*` beta field set. ##1688, #1705

#### Removed

- Removing `process.target.*` reuses from experimental schema. #1666
- Removing RFC 0014 `pe.*` fields from experimental schema. #1670

### Tooling and Artifact Changes

#### Bugfixes

* Fix invalid documentation link generation in component templates `_meta`. #1728

#### Improvements

* Update refs from master to main in USAGE.md etc #1658
* Clean up trailing spaces and additional newlines in schemas #1667
* Use higher compression as default in composable index template settings. #1712
* Bump dependencies. #1782

## [8.0.1](https://github.com/elastic/ecs/compare/v8.0.0...v8.0.1)

### Tooling and Artifact Changes

#### Bugfixes

* Pin `markupsafe==2.0.1` to resolve `ImportError` exception. #1804

## [8.0.0](https://github.com/elastic/ecs/compare/v1.12.2...v8.0.0)

### Schema Changes

#### Breaking changes

* Remove `host.user.*` field reuse. #1439
* Remove deprecation notice on `http.request.method`. #1443
* Migrate `log.origin.file.line` from `integer` to `long`. #1533
* Remove `log.original` field. #1580
* Remove `process.ppid` field. #1596

#### Added

* Added `faas.*` field set as beta. #1628, #1755

#### Improvements

* Wildcard type field migration GA. #1582
* `match_only_text` type field migration GA. #1584
* Threat indicator fields GA from RFC 0008. #1586

### Tooling and Artifact Changes

#### Breaking Changes

* Removing deprecated --oss from generator #1404
* Removing use-cases directory #1405
* Remove Go code generator. #1567
* Remove template generation for ES6. #1680
* Update folder structure for generated ES artifacts. #1700, #1762
* Updated support for overridable composable settings template. #1737

#### Improvements

* Align input options for --include and --subset arguments #1519
* Remove remaining Go deps after removing Go code generator. #1585
* Add explicit `default_field: true` for Beats artifacts. #1633
* Reorganize docs directory structure. #1679
* Added support for `analyzer` definitions for text fields. #1737
* Adding release notes section into ECS docs. #1800

#### Bugfixes

* Fixed the `default_field` flag for root fields in Beats generator. #1711

## [1.12.2](https://github.com/elastic/ecs/compare/v1.12.1...v1.12.2)

### Tooling and Artifact Changes

#### Bugfixes

* Add `object` as fallback for `flattened` type. #1653

## [1.12.1](https://github.com/elastic/ecs/compare/v1.12.0...v1.12.1)

### Schema Changes

#### Bugfixes

* Updating `x509` order to correct nesting. ##1621

## [1.12.0](https://github.com/elastic/ecs/compare/v1.11.0...v1.12.0)

### Schema Changes

#### Bugfixes

* Updating `hash` order to correct nesting. #1603
* Removing incorrect `hash` reuses. #1604
* Updating `pe` order to correct nesting. #1605
* Removing incorrect `pe` reuses. #1606
* Correcting `enrichments` to an `array` type. #1608

#### Added

* Added `file.fork_name` field. #1288
* Added `service.address` field. #1537
* Added `service.environment` as a beta field. #1541
* Added `process.end` field. #1544
* Added container metric fields into experimental schema. #1546
* Add `code_signature.digest_algorithm` and `code_signature.timestamp` fields. #1557
* Add `email.*` field set in the experimental fields. #1569

#### Improvements

* Beta migration on some `keyword` fields to `wildcard`. #1517
* Promote `threat.software.*` and `threat.group.*` fields to GA. #1540
* Update `user.name` and `user.id` examples for clarity. #1566
* Beta migration of `text` and `.text` multi-fields to `match_only_text`. #1532, #1571

### Tooling and Artifact Changes

#### Added

* Support ES 6.x type fallback for `match_only_text` field types. #1528

#### Bugfixes

* Prevent failure if no files need to be deleted `find | xargs rm`. #1588

#### Improvements

* Document field type family interoperability in FAQ. #1591

## [1.11.0](https://github.com/elastic/ecs/compare/v1.10.0...v1.11.0)

### Schema Changes

#### Added

* `elf.*` field set added as beta. #1410
* Remove `beta` from `orchestrator` field set. #1417
* Extend `threat.*` field set beta. #1438
* Added `event.agent_id_status` field. #1454
* `process.target` and `process.target.parent` added to experimental schema. #1467
* Threat indicator fields progress to beta stage. #1471, #1504
* `threat.enrichments` beta fields. #1478, #1504

#### Improvements

* Fix ecs GitHub repo link source branch #1393
* Add --exclude flag to Generator to support field removal testing #1411
* Explicitly include user identifiers in `relater.user` description. #1420
* Improve descriptions for `cloud.region` and `cloud.availability` fields. #1452
* Clarify `event.kind` descriptions for `alert` and `signal`. #1548

#### Deprecated

* Note deprecation of the `host.user.*` field reuse. #1422
* Note deprecation of `log.original` superseded by `event.original` #1469

### Tooling and Artifact Changes

#### Bugfixes

* Remove `ignore_above` when `index: false` and `doc_values: false`. #1483
* Ensure `doc_values` is carried into Beats artifacts. #1488

#### Added

* Support `match_only_text` data type in Go code generator. #1418
* Support for multi-level, self-nestings. #1459
* `beta` attribute now supported on categorization allowed values. #1511

#### Improvements

* Swap `Location` and `Field Set` columns in `Field Reuse` table for better readability. #1472, #1476
* Use a bullet points to list field reuses. #1473
* Improve wording in `Threat` schema #1505

## [1.10.0](https://github.com/elastic/ecs/compare/v1.9.0...v1.10.0)

### Schema Changes

#### Added

* Add `data_stream` fieldset. #1307
* Add `orchestrator` fieldset as beta fields. #1326
* Extend `threat.*` experimental fields with proposed changes from RFC 0018. #1344, #1351
* Allow custom descriptions for self-nesting reuses via `short_override` #1366

#### Improvements

* Updated descriptions to use Elastic Security #1305
* Host metrics fields from RFC 0005 are now GA. #1319
* Adjustments to the field set "usage" docs #1345
* Adjustments to the sidebar naming convention for usage and examples docs #1354
* Update `user.*` field reuse descriptions. #1382

### Tooling and Artifact Changes

#### Bugfixes

* Correcting fieldset name capitalization for generated ES template #1323

#### Improvements

* Support `nested` types in go code generator. #1254, #1350
* Go code generator now supports the `flattened` data type. #1302
* Adjustments to use terminology that doesn't have negative connotation. #1315

## [1.9.0](https://github.com/elastic/ecs/compare/v1.8.0...v1.9.0)

### Schema Changes

#### Added

* Added `hash.ssdeep`. #1169
* Added `cloud.service.name`. #1204
* Added `http.request.id`. #1208
* `data_stream.*` fieldset introduced in experimental schema and artifacts. #1215
* Added `geo.timezone`, `geo.postal_code`, and `geo.continent_code`. #1229
* Added `beta` host metrics fields. #1248
* Added `code_signature.team_id`, `code_signature.signing_id`. #1249
* Extended `pe` fields added to experimental schema. #1256
* Add `elf` fieldset to experimental schema. #1261
* Add `threat.indicator` fields to experimental schema. #1268

#### Improvements

* Include formatting guidance and examples for MAC address fields. #456
* New section in ECS detailing event categorization fields usage. #1242
* `user.changes.*`, `user.effective.*`, and `user.target.*` field reuses are GA. #1271

### Tooling and Artifact Changes

#### Improvements

* Update Python dependencies #1310, #1318
* Adjustments to use terminology that doesn't have negative connotation. #1315


## [1.8.0](https://github.com/elastic/ecs/compare/v1.7.0...v1.8.0)

### Schema Changes

#### Bugfixes

* Clean up `event.reference` description. #1181
* Go code generator fails if `scaled_float` type is used. #1250

#### Added

* Added `event.category` "registry". #1040
* Added `event.category` "session". #1049
* Added usage documentation for `user` fields. #1066
* Added `user` fields at `user.effective.*`, `user.target.*` and `user.changes.*`. #1066
* Added `os.type`. #1111

#### Improvements

* Event categorization fields GA. #1067
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

## [1.7.0](https://github.com/elastic/ecs/compare/v1.6.0...v1.7.0)

### Schema Changes

#### Bugfixes

* The `protocol` allowed value under `event.type` should not have the `expected_event_types` defined. #964
* Clarify the definition of `file.extension` (no dots). #1016

#### Added

* Added Mime Type fields to HTTP request and response. #944
* Added network directions ingress and egress. #945
* Added `threat.technique.subtechnique` to capture MITRE ATT&CK® subtechniques. #951
* Added `configuration` as an allowed `event.category`. #963
* Added a new directory with experimental artifacts, which includes all changes
  from RFCs that have reached stage 2. #993, #1053, #1115, #1117, #1118

#### Improvements

* Expanded field set definitions for `source.*` and `destination.*`. #967
* Provided better guidance for mapping network events. #969
* Added the field `.subdomain` under `client`, `destination`, `server`, `source`
  and `url`, to match its presence at `dns.question.subdomain`. #981
* Clarified ambiguity in guidance on how to use x509 fields for connections with
  only one certificate. #1114

### Tooling and Artifact Changes

#### Breaking changes

* Changed the index pattern of the sample Elasticsearch template from `ecs-*` to
  `try-ecs-*` to avoid conflicting with Logstash' `ecs-logstash-*`. #1048

#### Bugfixes

* Addressed issue where foreign reuses weren't using the user-supplied `as` value for their destination. #960
* Experimental artifacts failed to install due to `event.original` index setting. #1053

#### Added

* Introduced `--strict` flag to perform stricter schema validation when running the generator script. #937
* Added check under `--strict` that ensures composite types in example fields are quoted. #966
* Added `ignore_above` and `normalizer` support for keyword multi-fields. #971
* Added `--oss` flag for users who want to generate ECS templates for use on OSS clusters. #991

#### Improvements

* Field details Jinja2 template components have been consolidated into one template #897
* Add `[discrete]` marker before each section header in field details. #989
* `--ref` now loads `experimental/schemas` based on git ref in addition to `schemas`. #1063


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
