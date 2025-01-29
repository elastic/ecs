# 0000: Entity Field Set

<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)**
- Date: **TBD**

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->


<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

An entity represents a discrete, identifiable component within an IT environment that can be described by a set of attributes and maintains its identity over time. Entities can be physical (like hosts or devices), logical (like containers or processes), or abstract (like applications or services).

Currently, ECS provides specific field sets for certain categories of entities (e.g., host, user, cloud, orchestrator) to capture their metadata. However, as IT infrastructure continues to evolve, we encounter an increasing number of entity types that don't cleanly fit into existing field sets – for example, storage services like S3, database instances like DynamoDB, or various other cloud services and IT related infrastructure components (both digital and physical).

This field set aims to solve several key challenges:
1. Providing a flexible way to represent different types of entities without requiring new field sets for each category
2. Supporting a consistent structure for capturing entity metadata across different entity types
3. Enabling the representation of entities that don't fit into existing field sets
4. Reducing the complexity of the ECS schema by avoiding the proliferation of entity-specific field sets

This approach would allow ECS to accommodate new types of entities without requiring continuous schema expansion through new field sets, while maintaining a consistent structure for entity representation.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| entity.id | keyword | A unique identifier for the entity. This should be a stable, unique value that persists across different observations of the same entity. For entities with dedicated field sets (e.g., host.id, user.id), this value should match the corresponding *.id field. |
| entity.source | keyword | The module or integration that provided this entity data (similar to event.module). |
| entity.category | keyword | A standardized high-level classification of the entity type. This provides a normalized way to group similar entities across different providers or systems. Example values: `bucket`, `database`, `container`, `function`, `queue`, `host`, `user`, etc.,. There will be an allowed set of values maintained for this field to ensure consistency. |
| entity.type | keyword | The specific type designation for the entity as defined by its provider or system. This field provides more granular classification than entity.category. Examples: `aws_s3_bucket`, `gcp_cloud_storage_bucket`, `azure_blob_container` would all map to category `bucket`. |
| entity.name | keyword, text | The human-readable name of the entity. The keyword field enables exact matches for filtering and aggregations, while the text field enables full-text search. For entities with dedicated field sets (e.g., `host`), this field should mirrors the corresponding *.name value. |
| entity.address | keyword | A URI, URL, or other direct reference to access or locate the entity in its source system. This could be an API endpoint, web console URL, or other addressable location. Format may vary by entity type and source system. |
| entity.Attributes.* | object |  Entity type-specific attributes using capitalized field names to indicate custom field space. The capital `A` in "Attributes" and the capitalization of all subfields (e.g., `entity.Attributes.StorageClass`, `entity.Attributes.EngineVersion`) distinguishes these as custom entity-type-specific fields that won't be enumerated in the ECS schema.  | 
| entity.metadata.* | flattened | A flexible container for entity metadata that doesn't fit into other structured fields. This field uses the flattened type to allow arbitrary key-value pairs while maintaining searchability. Useful for provider-specific or non-standardized attributes that don't warrant dedicated fields. |



The fields from the ECS [risk field set](https://www.elastic.co/guide/en/ecs/current/ecs-risk.html) can be nested under entity

| Field | Type | Description |
|-------|------|-------------|
| entity.risk.* | * | Fields for describing risk score and risk level of entities such as hosts and users. |


When representing entities that correspond to existing ECS field sets (e.g., hosts, users, services, containers), the relevant ECS field set should be used to capture detailed metadata about that entity. For example:

- Host entities should utilize the `host.*` field set to capture detailed host information
- User entities should leverage the `user.*` field set for user-specific attributes
- Cloud resource entities should use the `cloud.*` field set for cloud provider details
- Service entities should employ the `service.*` field set for service-specific metadata

This approach ensures backward compatibility, maintains existing ECS patterns, and preserves the rich metadata capabilities of established field sets while allowing the entity fields to provide a consistent way to identify and categorize all entity types. The entity fields serve as a complementary layer that enables unified entity representation, particularly for entity types that don't have dedicated field sets.

## Usage

Out Of Scope for Stage 0 (based on template)

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

Out Of Scope for Stage 0 (based on template)

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

Out Of Scope for Stage 0 (based on template)

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

## Concerns

Out Of Scope for Stage 0 (based on template)

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

<!--
Who will be or has been consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

The following are the people that consulted on the contents of this RFC.

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->

The following are the people that consulted on the contents of this RFC.

* Author: @tinnytintin10  
* Sponsor: @MikePaquette & @YulNaumenko 


## References

- Related effort in Otel: [Resource and Entities - Data Model](https://github.com/open-telemetry/opentelemetry-specification/blob/main/oteps/entities/0264-resource-and-entities.md)

<!-- Insert any links appropriate to this RFC in this section. -->


### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
* Stage 0: https://github.com/elastic/ecs/pull/TBD