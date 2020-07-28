# 0003: Object Fields
<!--^ The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC, taking care not to conflict with other RFCs.-->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage -->
- Date: **2020-07-27** <!-- Update to reflect date of most recent stage advancement -->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->
Numerous SaaS Cloud Providers provide event data where the event reflects an action (Typically a CRUD action) on what can broadly be considered an "object." For some providers that Object may be a "file" wherein the existing ECS `file` fields are adequate; however other providers (Workday, Salesforce, Service Now, Zoom, etc.) an object can represent some other concept like a "record" or "setting" or "meeting." There presently isn't any location within ECS to document these as there is with "file," forcing any representation to be pushed into a custom field. This RFC proposes a new top-level field called `object` that will represent these instances.

## Fields

<!--
Stage: 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->
This RFC calls for the introduction of a top-level `object` field with an initial fieldset of the following child fields:

| field | type | description |
| --- | --- | --- |
| `object.name` | keyword | Name of the Object |
| `object.id` | keyword | ID of the Object |
| `object.type` | keyword | Type of Object Represented (e.g. `record`, `meeting`, `repository`, `organization`, etc.) |
| `object.additional_details` | object | Custom Key/Value pairs representing data relevant to the object |
| `object.owner.id` | keyword | ID of the Object Owner |
| `object.owner.name` | keyword | Name of the Object Owner |
| `object.owner.email` | keyword | Email of the Object Owner |


<!--
Stage 2: Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->
Object fields would allow for normalization of event/audit data provided by SaaS providers and facilitate the usage of ECS normalized event data to track, detect, and investigate activity across a broad spectrum of SaaS provider logs.

For example; an analyst could leverage the fields here to identify access into specific records on Salesforce; cases on Service Now; or meetings on Zoom without needing to know service specific field names and/or custom field names; They would simply be able to pivot their query on the respective `object` field and `cloud.provider` field.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->
* Cloud SaaS Providers
 * Salesforce
 * Zoom
 * Box
 * Microsoft/Office365
 * Github

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact
No breaking changes are anticipated as this is a net new introduction of fields.
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
An object is a very broad categorization, in some situations it may be hard to determine when something should be normalized into this field or another field like `file` or `package`. Additionally given the genericness of this field, a lot of finer details about the object may not be represented by this field, but rather addressed in custom key/value pairs nested under this field. Also due to the genericness of the field, the `object.type` field becomes rather critical to designate what exactly is represented within this field (e.g. is it a `record` or a `meeting`); some context might be derived from other fields in the event, but that would require some foreknowledge in order to properly search or sort. Designating specific acceptable values for `object.type` could minimize any confusion around the object being represented; however that would require specific updates to ECS to support new object "types".

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate the risk of churn and instability by resolving outstanding concerns.
-->

<!--
Stage 4: Document any new concerns and their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## Real-world implementations

<!--
Stage 4: Identify at least one real-world, production-ready implementation that uses these updated field definitions. An example of this might be a GA feature in an Elastic application in Kibana.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @drewgatchell | author

<!--
Who will be or has consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/883

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
