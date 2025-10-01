---
navigation_title: "ECS"
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/releasenotes.html
---

# ECS release notes [ecs-release-notes]

Review the changes, fixes, and more in each version of ECS.

To check for security updates, go to [Security announcements for the Elastic stack](https://discuss.elastic.co/c/announcements/security-announcements/31).

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.

% ## version.next [ecs-next-release-notes]

% ### Features and enhancements [ecs-next-features-enhancements]
% *

% ### Fixes [ecs-next-fixes]
% *

## 9.1.0 [ecs-9-1-0-release-notes]

### Features and enhancements [ecs-9-1-0-features-enhancements]

* Add `gen_ai` fields to schema as beta. [#2475](https://github.com/elastic/ecs/pull/2475)
* Allow Unicode characters in generated ECS yml files. [#2478](https://github.com/elastic/ecs/pull/2478)
* Update semconv version used in file generation to v1.34.0 [#2483](https://github.com/elastic/ecs/pull/2483)

### Fixes [ecs-9-1-0-fixes]

* Add `origin_referrer_url` and `origin_url` fields, which indicate the origin information to the file, process and dll schemas [#2441](https://github.com/elastic/ecs/pull/2441)
* Add `thumbprint_sha256` to `code_signature` schema. [#2452](https://github.com/elastic/ecs/pull/2452)
* Fix otel urls for fieldsets with underscores. [#2486](https://github.com/elastic/ecs/pull/2486)


## 9.0.0 [ecs-9-0-0-release-notes]

### Features and enhancements [ecs-9-0-0-features-enhancements]

* Define base encoding of `x509.serial_number`. [#2383](https://github.com/elastic/ecs/pull/2383)
* Restrict the encoding of `x509.serial_number` to base 16. [#2398](https://github.com/elastic/ecs/pull/2398)
* Promote beta fields to GA. [#2411](https://github.com/elastic/ecs/pull/2411)
* Add mapping between ECS and OpenTelemetry. [#2415](https://github.com/elastic/ecs/pull/2415)
* Set synthetic_source_keep = none on fields that represent sets. [#2422](https://github.com/elastic/ecs/pull/2422)
* Increase ignore_above value for url.query. [#2424](https://github.com/elastic/ecs/pull/2424)
* Add `origin_referrer_url` and `origin_url` fields, which indicate the origin information to the file, process and dll schemas. [#2441](https://github.com/elastic/ecs/pull/2441)

### Fixes [ecs-9-0-0-fixes]

* Fix link rendering issues and usage of http in links. [#2423](https://github.com/elastic/ecs/pull/2423)
* Fix link rendering for additional fields. [#2458](https://github.com/elastic/ecs/pull/2458)
