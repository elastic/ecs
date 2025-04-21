# 0049: Entity Field Set

- Stage: **1 (draft)**
- Date:

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
| entity.id | keyword | A unique identifier for the entity. When multiple identifiers exist, this should be the most stable and commonly used identifier that: 1) persists across the entity's lifecycle, 2) ensures uniqueness within its scope, 3) is commonly used for queries and correlation, and 4) is readily available in most observations (logs/events). For entities with dedicated field sets (e.g., host, user), this value should match the corresponding *.id field. Alternative identifiers (e.g., ARNs values in AWS, URLs) can be preserved in entity.raw. |
| entity.source | keyword | The module or integration that provided this entity data (similar to event.module). |
| entity.type | keyword | A standardized high-level classification of the entity. This provides a normalized way to group similar entities across different providers or systems. Example values: `bucket`, `database`, `container`, `function`, `queue`, `host`, `user`, etc. There will be an allowed set of values maintained for this field to ensure consistency. |
| entity.sub_type | keyword | The specific type designation for the entity as defined by its provider or system. This field provides more granular classification than entity.type. Examples: `aws_s3_bucket`, `gcp_cloud_storage_bucket`, `azure_blob_container` would all map to type `bucket`. |
| entity.name | keyword, text | The name of the entity. The keyword field enables exact matches for filtering and aggregations, while the text field enables full-text search. For entities with dedicated field sets (e.g., `host`), this field should mirrors the corresponding *.name value. |
| entity.reference | keyword | A URI, URL, or other direct reference to access or locate the entity in its source system. This could be an API endpoint, web console URL, or other addressable location. Format may vary by entity type and source system. |
| entity.attributes.* | object | Normalized entity attributes using capitalized field names (e.g., `entity.attributes.StorageClass`, `entity.attributes.MfaEnabled`). Use this field set when you need specific data types, advanced search capabilities, or normalized values across different providers/sources. The capitalization pattern indicates these are entity-specific fields that won't be enumerated in the ECS schema. |
| entity.raw.* | flattened | Original, unmodified fields from the source system stored in a flattened format that maintains basic searchability. While `entity.attributes` should be used for normalized fields requiring advanced queries, this field preserves all source metadata with basic search capabilities. Supports existence queries, exact value matches, and simple aggregations. |

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

The entity field set enables us to normalize entity data in such a way where we can easily query key attributes in a standardized way regardless of the type and source of the entity. This will be how we'll normalize all entity data in the upcoming inventory experience that we're planning for the security solution.

This approach will enable security analysts to view all the entities discovered inside of their environment, whether from logs or other data sources. The entity field set will then begin powering all parts of our security solution experience like alerts, where we can now represent more entities beyond just users and hosts.

Essentially, this field set gives us a standard way to represent any entity's metadata, regardless of its type or source, and provides customers with the same ability to standardize that information across their environments.

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
