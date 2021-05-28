# 0017: Remove log.original

- Stage: **2 (candidate)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-04-28** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

This RFC supersedes issue [#841](https://github.com/elastic/ecs/issues/841) which implies breaking changes therefore the RFC Process is indicated.

The request is to consolidate `log.original` and `event.original` by removing `log.original`, since these are almost equivalent in nature. (One) justification for preserving `event.original` is that not all events are logs. Once `log.original` is removed, `event.original` will be the sole field intended to capture the original untouched event.

## Fields

| Field Set | Field(s) |
| --------- | -------- |
| [`log`](0017/log.yml) | `log.original` |
| [`event`](0017/event.yml) | `event.original` |

- The internal description of the field `log.original` in [`log`](0017/log.yml) should be amended by addition of a notice of deprecation and subsequently removal if/when Deprecation progresses to Removal

- The internal description of the field `event.original` in [`event`](0017/event.yml) should be updated to reflect the revised scope 

- The extended description of `log.original` in the [`Log Fields documentation`](../../docs/field-details.asciidoc#field-log-original) should be amended by addition of a notice of deprecation and subsequently removal if/when Deprecation progresses to Removal

- The extended description of `event.original` in the [`Event Fields documentation`](../../docs/field-details.asciidoc#field-event-original) should be amended to clarify the absorption of `log.original`

 
## Usage

The following examples are taken verbatim from the existing field definitions 
and are included for completeness.

These are the raw texts of entire events, for example a log message. They 
differs from the extracted `message` field in that no processing has been 
applied and the field is not indexed by default. The field can still be 
retrieved from `_source` and is well-suited to demonstration of log integrity
or in a re-index pipeline 

## Source data

Any or all incoming log or event messages.

```
{"event.original": "Sep 19 08:26:10 host CEF:0&#124;Security&#124;
          threatmanager&#124;1.0&#124;100&#124;
          worm successfully stopped&#124;10&#124;src=10.0.0.1
          dst=2.1.2.2spt=1232"}

{"event.original": "Sep 19 08:26:10 localhost My log"}
```
<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

Beats modules, Agent integration packages and the Logging UI would be required to migrate if this change is adopted as proposed.

The removal of `log.original` will be considered a breaking change since the field is being removed from the schema. Possible migration/mitigations for users impacted may include:

- The [`Beats default fields inclusion list`](../../scripts/generators/beats_default_fields_allowlist.yml) list should be updated by removing `log.original` if/when Deprecation progresses to Removal

- The logs UI `message` column currently displays `log.original` in the absence of a `message` field. This should be updated to use `event.original` as the substitute field. See [builtin_rules](https://github.com/elastic/kibana/blob/master/x-pack/plugins/infra/server/services/log_entries/message/builtin_rules/generic.ts) and [associated test](https://github.com/elastic/kibana/blob/master/x-pack/plugins/infra/server/services/log_entries/message/builtin_rules/generic.test.ts).

- References in the [RAC Rule Registry](https://github.com/elastic/kibana/blob/master/x-pack/plugins/rule_registry/common/assets/field_maps/ecs_field_map.ts) will need to be removed - these have `required: false` so hopefully non-breaking change.

- Multiple tests in Kibana will need to be updated see e.g. [Function Test APM Mapping](https://github.com/elastic/kibana/blob/master/x-pack/test/functional/es_archives/monitoring/setup/collection/detect_apm/mappings.json)

- TBD would it be beneficial to alias `log.original` for current users of this field

- TBD if there exist current users of fields with distinct content/meaning in a common index mapping

## Concerns

As a breaking change, this would require timely communication to the Elastic Community.

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @djptek | author
* @ebeahan | sponsor
* @andrewkroh | Beats & Logging UI
* @jasonrhodes | Logging UI & RAC
* @MikePaquette  | RAC


## References

* [#841](https://github.com/elastic/ecs/issues/841)
* [#777](https://github.com/elastic/integrations/issues/777)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1298
* Stage 1: https://github.com/elastic/ecs/pull/1314
* Stage 2: https://github.com/elastic/ecs/pull/1347

