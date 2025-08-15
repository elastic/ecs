# 0049: Entity Field Set

- Stage: **1 (draft)**
- Date: 2025-04-23
- Updated: 2025-08-15

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
| entity.definition_id | keyword | Used Elastic solutions (e.g., Security, Observability) to denote the ID of the entity definition which is used to extract entity details from ingested logs, events, intelligence, and other data types. Use of this value is reserved, and ECS producers, including data ingestion pipelines, must not populate this field|
| entity.definition_id | keyword | Used by Elastic solutions (e.g., Security, Observability) to denote the version of the entity definition which is used to extract entity details from ingested logs, events, intelligence, and other data types. Use of this value is reserved, and ECS producers, including data ingestion pipelines, must not populate this field|
| entity.schema_version | keyword | Denotes the version of the entity schema,as published in Elastic Security documentation, to which this entity information conforms. Usually conforms to the Elastic Stack version.
| entity.last_seen_timestamp | date | Indicates the date/time when this entity was last "seen," usually based upon the last event/log that is initiated by this entity. Note: this field may contain the same timestamp as is included in custom field `entity.lifecycle.Last_activity`.
| entity.id | keyword | A unique identifier for the entity. When multiple identifiers exist, this should be the most stable and commonly used identifier that: 1) persists across the entity's lifecycle, 2) ensures uniqueness within its scope, 3) is commonly used for queries and correlation, and 4) is readily available in most observations (logs/events). For entities with dedicated field sets (e.g., host, user), this value should match the corresponding *.id field. Alternative identifiers (e.g., ARNs values in AWS, URLs) can be preserved in entity.raw. |
| entity.source | keyword | The module or integration that provided this entity data (similar to event.module). |
| entity.type | keyword | A standardized high-level classification of the entity. This provides a normalized way to group similar entities across different providers or systems. Example values: `bucket`, `database`, `container`, `function`, `queue`, `host`, `user`, `application`, `session`, etc. |
| entity.sub_type | keyword | The specific type designation for the entity as defined by its provider or system. This field provides more granular classification than entity.type. Examples: `aws_s3_bucket`, `gcp_cloud_storage_bucket`, `azure_blob_container` would all map to type `bucket`.  `hardware` , `virtual` , `container` , `node` , `cloud_instance` would all map to entity type `host'.|
| entity.name | keyword, text | The name of the entity. The keyword field enables exact matches for filtering and aggregations, while the text field enables full-text search. For entities with dedicated field sets (e.g., `host`), this field should mirrors the corresponding *.name value. |
| entity.display_name | keyword, text | An optional field used when a pretty name is desired for entity-centric operations. This field should not be used for correlation with `*.name` fields for entities with dedicated field sets (e.g., `host`).  |
| entity.reference | keyword | A URI, URL, or other direct reference to access or locate the entity in its source system. This could be an API endpoint, web console URL, or other addressable location. Format may vary by entity type and source system. |
| entity.attributes.* | object | A set of static or semi-static attributes of the entity. Usually boolean or keyword field data types. Examples include: `entity.attributes.Storage_class`, `entity.attributes.Mfa_enabled` , `entity.attributes.Privileged` , `entity.attributes.Granted_permissions` , `entity.attributes.Known_redirect` , `entity.attributes.Asset` , `entity.attrbitues.Os_current` , `entity.attibutes.Os_patch_current` , `entity.attributes.Oauth_consent_restriction`). Use this field set when you need to track static or semi-static characterstics of an entity for advanced searching and correlation of normalized values across different providers/sources and entity types. Note the initial capitalization pattern for Examples indicates that any such fields are custom entity-specific fields that won't be enumerated in the ECS schema, and won't collide with any fields that may be defined by ECS in the future. |
| entity.lifecycle.* | object | A set of temporal characteristics of the entity. Usually date field data type. Examples include: `entity.lifecycle.First_seen`, `entity.lifecycle.Last_activity` , `entity.lifecycle.Issued_at` , `entity.lifecycle.Last_password_change` ,etc. ). Use this field set when you need to track temporal characterstics of an entity for advanced searching and correlation of normalized values across different providers/sources and entity types. Note the initial capitalization pattern indicates that any such fields are custom entity-specific fields that won't be enumerated in the ECS schema, and won't collide with any fields that may be defined by ECS in the future. |
| entity.behavior.* | object | A set of ephemeral characteristics of the entity, derived from observed behaviors during a specific time period. Behaviors are usually captured in event logs under fields such as `event.action` and other fields, but this field set captures "attributified" behavior indicators, using semantics like "this behavior was seen one or more times during this time period." Sytems using this field set may need to force a "reset" of these behavioral indicators at the end of their current period. Usually boolean field data type. Examples include: `entity.behavior.Used_usb_device`, `entity.behavior.Brute_force_victim` , `entity.behavior.New_country_login` ,etc. ). Use this field set when you need to capture and track ephemeral characterstics of an entity for advanced searching, correlation of normalized values across different providers/sources and entity types. Note the initial capitalization pattern indicates that any such fields are custom entity-specific fields that won't be enumerated in the ECS schema, and won't collide with any fields that may be defined by ECS in the future. |
| entity.raw.* | object | Original, unmodified fields from the source system stored in a flattened format that maintains basic searchability. While `entity.attributes` should be used for normalized fields requiring advanced queries, this field preserves all source metadata with basic search capabilities. Supports existence queries, exact value matches, and simple aggregations. |
| entity.metrics.* | object | Field set for any fields containing numeric entity metrics. These use dymanic field data type mapping. Any fields under entity.metrics.* will automatically get the appropriate numeric mapping without needing explicit definition.

When representing entities that have existing ECS entiy field sets (e.g., hosts, users, services, containers), the relevant ECS field set should continue to be used to capture a copy of the detailed metadata about that entity. For example:

- Host entities should also utilize the `host.*` field set to capture detailed host information
- User entities should also leverage the `user.*` field set for user-specific attributes
- Cloud resource entities should also use the `cloud.*` field set for cloud provider details
- Service entities should also employ the `service.*` field set for service-specific metadata

This approach ensures backward compatibility, maintains existing ECS patterns, and preserves the rich metadata capabilities of established field sets while allowing the entity fields to provide a consistent way to identify and categorize *all* entity types. The entity fields serve as a complementary layer that enables unified entity representation, particularly for entity types that don't have dedicated field sets.

## Field Re-use

### ECS Producers

For ECS producers, such as Beats, Elastic Agent integrations, ingest pipelines, and other methods for shipping data to Elastic, the `entity.*` fields are expected to be nested as follows:
- If the entity type is one of host, user, service, cloud, orchestrator), then the entity fields should be nested under the respecitve root field set, for example `host.entity.*` , `user.entity.*`, etc.
- If the entity type is not one of the above, then that `entity.*` fields should be nested under a new root-level object, called `generic`, as `generic.entity.*`

Special note for use with entity fields that use `target` fields.
If the entity type includes a provision for `target.*` fields, such as `user.target.*`, then the `entity.*` fields should be nested under the `*.target.*` field set, for example, `user.target.entity.*`.

### ECS Consumers or Data Stores

For ECS consumers, such as the Elastic Security Solution entity store indices, the `entity.*` fields should be used directly at the root of the events.

## User Benefits

This approach will enable security analysts to view all the entities discovered inside of their environment, whether from logs or other data sources. The entity field set will then begin powering all parts of our security solution experience like alerts, where we can now represent more entities beyond just users and hosts.

Essentially, this field set gives us a standard way to represent any entity's metadata, regardless of its type or source, and provides users with the same ability to standardize that information across their environments.

The entity field set enables users to normalize entity data in such a way where key attributes can be queried in a standardized way regardless of the type and source of the entity metadata. Elastic solutions normalize all entity data using this entity.* field set.


## Source data

Due to the high-level taxonomy approach we've developed for the entity field set, it doesn't exclude any data source. Any data source can model an entity using this field set, making it universally applicable across different technologies, platforms, and environments.

## Scope of impact

TO DO

## Concerns

### Entity Type Governance

The `entity.type` field needs a controlled vocabulary to maintain consistency and interoperability. However, an overly restrictive list might limit the field set's utility for emerging technologies and use cases.

**Potential solution:** Establish a governance process for `entity.type` values, including an initial set of well-defined types and a mechanism for proposing and reviewing new types. Document a clear taxonomy with examples to guide users in selecting appropriate types.

## People

The following are the people that consulted on the contents of this RFC.

- Author: @tinnytintin10
- Sponsor: @MikePaquette & @YulNaumenko

## References

TO DO

### RFC Pull Requests

- Stage 0: <https://github.com/elastic/ecs/pull/2434>
- Stage 1: <https://github.com/elastic/ecs/pull/2461>
- Stage 1 Update: 
