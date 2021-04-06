# 0017: Remove log.original

- Stage: **1 (draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-03-11** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

This RFC supersedes issue [#841](https://github.com/elastic/ecs/issues/841) which implies breaking changes therefore the RFC Process is indicated.

The request is to consolidate `log.original` and `event.original` by removing `log.original`, since these are almost equivalent in nature. (One) justification for preserving `event.original` is that not all events are logs. Once `log.original` is removed, `event.original` will be the sole field intended to capture the original untouched event.

## Fields

| Field Set | Field(s) |
| --------- | -------- |
| [`log`](0017/log.yml) | `log.original` |
| [`event`](0017/event.yml) | `event.original` |

- The internal description of the field `log.original` in [`log`](0017/log.yml) should be amended by addition of a notice of deprecation and subsequently removal if/when Deprecation progresses to Removal

- The internal description of the field `event.original` in [`event`](0017/event.yml) should be updated to reflect the revised scope 

- The [`Beats default fields inclusion list`](../../scripts/generators/beats_default_fields_whitelist.yml) list should be updated by removing `log.original` if/when Deprecation progresses to Removal

- The extended description of `log.original` in the [`Log Fields documentation`](../../docs/field-details.asciidoc#field-log-original) should be amended by addition of a notice of deprecation and subsequently removal if/when Deprecation progresses to Removal

- The extended description of `event.original` in the [`Event Fields documentation`](../../docs/field-details.asciidoc#field-event-original) should be amended to clarify the absorption of `log.original`

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

Beats modules and Agent integration packages would be required to migrate if this change is adopted as proposed.

The removal of `log.original` will be considered a breaking change since the field is being removed from the schema. Possible migration/mitigations for users impacted may include:

- requirement to alias `log.original` for current users of this field
- TBD if there exist current users of fields with distinct content/meaning in a common index mapping

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @djptek | author
* @ebeahan | sponsor

<!--
Who will be or has been consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

* [#841](https://github.com/elastic/ecs/issues/841)
* [#777](https://github.com/elastic/integrations/issues/777)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1298
* Stage 1: https://github.com/elastic/ecs/pull/1314
