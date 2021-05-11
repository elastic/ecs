# 0000: Migrate `text` fields to `match_only_text`
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

Indexing `message` fields as the `text` type in security and application logs consumes significant disk space. Part of the disk space spent is on indexing to support scoring and phrase queries, which aren't often used in logging use cases. Elasticsearch 7.14 introduces a new field type called `match_only_text` which is a more space-efficient variant of the `text` field type for this logging-focused use cases.

This RFC proposes migrating existing ECS `text` fields to `match_only_text`. Most current ECS datasets are focused heavily on logging use cases, and we can pass this disk space savings onto users by migrating `text` fields to `match_only_text` by default in ECS. Upcoming changes in Elasticsearch will default to indexing the `message` field as `match_only_text`, and this change in ECS will also align better with this new stack default.

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

## Fields

The following fields are currently indexed as `text` and are candidates to migrate to `match_only_text`:

* `message`
* `error.message`


<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

Data is indexed the same as a `text` field that has:

* `index_options: docs`
* `norms: false`

`match_only_text` uses the `_source` for positional queries like `match_phrase`

The `match_only_text` type supports the same feature set as `text`, except the following:

* No support for scoring: queries ignore index statistics and produce constant scores.
* Span queries are unsupported. If a span query is run, then shards where the field is mapped as match_only_text will be returned as failed in the search response and their hits will be ignored.
* Phrase and intervals queries run slower.

Like `text`, `match_only_text` fields do not support aggregations.

This new field is part of the text family, so it is returned as a text field in the `_field_caps` output. Being a member of the `text` field family means migrating fields from `text` to `match_only_text` is a non-breaking change and the fields of `text` and `match_only_text` can be queried alongside each other.

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

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

* @ebeahan | author
* @jpountz | subject matter expert

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

<!-- Insert any links appropriate to this RFC in this section. -->

* https://www.elastic.co/guide/en/elasticsearch/reference/master/text.html#match-only-text-field-type
* https://github.com/elastic/elasticsearch/pull/66172
* https://github.com/elastic/ecs/issues/1377
* https://github.com/elastic/elasticsearch/issues/64467
* https://github.com/elastic/elasticsearch/blob/7.x/x-pack/plugin/core/src/main/resources/data-streams-mappings.json#L14-L22

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1396

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
