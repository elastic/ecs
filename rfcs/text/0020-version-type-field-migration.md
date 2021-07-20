# 0020: Version Type Field Migration
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **X (abandoned)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-07-20** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->
## Abandoned

As the time this proposal was marked `abandoned`, adopting `version` is not a priority for the ECS team or other ECS stakeholders. The team may revisit reviewing how `version` could be beneficial later on.

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

Elasticsearch 7.10 introduced a new field data type specialized in handling software version values: `version`. The `version` type supports specialized precedence rules based on the rules outlined in [Semantic Versioning](semver.org) (semver). A `range` query against a `version` field for values between `1.0.0` and `1.5.0` will include `1.2.3` but not `1.11.2`. This differs from `keyword` fields where the `range` ordering is alphabetical.

Examples:

* Return documents with `.version` greater-than or equal to `1.1.0` and less-than `2.0.0`
* Query across multiple versions without the need to know in advance ever possible versions in the index (e.g. `ecs.version:(1.3.0 OR 1.4.0 OR 1.5.0`)
* Return all documents where minor version is 3 (`x.3.y`) or the major version is considered unstable (`0.x.y`).

The purpose of this proposal is to identify which fields may be good candidates for adopting the `version` data type and design considerations for that migration.

## Fields

* `agent.version`
* `ecs.version`
* `os.version`
* `package.version`
* `rule.version`
* `service.version`

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

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

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

### Mapping conflicts

Changing the field type will result in a mapping conflict across indices mapping version fields using `type: keyword` and indices mapping version fields as `type: version`.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

### Version fields containing non-semantic version values

Version string values that are not valid under the semver rules will still be indexed and retrieved as exact matches but will only appear _after_ any valid semver value with regular alphabetical ordering.

Fields that expect version values but often contains values that do _not_ align with semver rules are probably best to remain using `keyword`. The [list](#Fields) of proposed fields will be assessed in a later stage to determine if each field's expected values make it a good candidate for `version`.


### Kibana support

Support in Kibana for the `version` data for index patterns, aggregations, and Lens is still [in-progress](https://github.com/elastic/kibana/issues/93248).

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | author, sponsor

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

* https://github.com/elastic/ecs/issues/887
* https://github.com/elastic/ecs/issues/842
* https://www.elastic.co/guide/en/elasticsearch/reference/current/version.html
* https://github.com/elastic/kibana/issues/93248

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1309
* Stage X: https://github.com/elastic/ecs/pull/1451

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
