# 0054: Extend entity fields with additional attributes, lifecycle, relationships, and risk reuse
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

This RFC proposes a focused extension to the ECS `entity.*` schema by adding a small set of concrete `entity.attributes.*`, `entity.lifecycle.*`, and `entity.relationships.*` leaves. A separate, related change to enable `entity.risk.*` reuse is summarized under [Related work: entity-level risk](#related-work-entity-level-risk).

The goal is to make normalized entity data more useful for security, asset, and graph-oriented use cases without introducing a broad or underspecified object model. This proposal follows the direction established in [RFC 0049](https://github.com/elastic/ecs/blob/main/rfcs/text/0049-entity-fields.md) and incorporates review feedback from [elastic/ecs#2598](https://github.com/elastic/ecs/pull/2598).

## Fields

Where a field is multi-valued in ECS, the type is written as **`keyword (list)`** (schema: `normalize: [array]`). **`object`** relationship values are flat bags of keyword arrays inside the object, not a list at the top level—see [Relationship identifier structure](#relationship-identifier-structure).

**Applied Entity Type** lists which normalized entity kinds (**User**, **Host**, **Service**) the field is typically relevant for. Comma-separated means any of those; **all** means User, Host, and Service when semantically appropriate.

| Field | Type | Applied Entity Type | Description |
| ----- | ---- | ------------------- | ----------- |
| entity.attributes.storage_class | keyword | Service | The storage tier or class assigned to an object storage resource (e.g. S3/GCS/Azure object tiers). **Values:** free-text or provider-specific labels unless/until ECS defines `allowed_values`; common examples include `STANDARD`, `STANDARD_IA`, `GLACIER`, `COLDLINE` (not an exhaustive enum in this RFC). |
| entity.attributes.mfa_enabled | boolean | User | Indicates whether multi-factor authentication is enabled for this entity. |
| entity.attributes.permissions | keyword (list) | User, Host, Service | Action-level permissions associated with this entity (not roles or groups). Prefer this name over `granted_permissions` unless a future RFC introduces parallel fields for inherited or effective permissions. |
| entity.attributes.known_redirects | keyword (list) | Service | Known redirect URIs or URLs associated with this entity, commonly for OAuth applications or services. Plural name reflects ECS guidance to use singular/plural names to reflect field content. |
| entity.attributes.managed | boolean | Host, Service | Indicates whether the entity is managed by an external administration or control system. |
| entity.attributes.oauth_consent_restriction | keyword | Service | Restriction applied to OAuth consent for this entity (e.g. `admin_only`, `verified_only`, `unrestricted`). **Values:** integration-defined keywords unless standardized later. |
| entity.lifecycle.last_activity | date | User, Host, Service | Timestamp of the most recent action performed by or attributed to this entity (active use). Distinct from **`entity.last_seen_timestamp`**, which records when the entity was last observed in data; `last_activity` implies the entity was active, not only seen. |
| entity.relationships.owns | object | all | Identifiers of assets or identities this entity owns. Structure is a **flat bag of keyword arrays** (see [Relationship identifier structure](#relationship-identifier-structure)), not an array of nested objects, so storage and querying remain compatible with ESQL limitations on nested mappings. |
| entity.relationships.depends_on | object | all | Identifiers of entities this entity **requires for operation**—for example: a service depending on a database or upstream API, an application depending on an identity provider, or a workload depending on a host or cluster. Use the same flat identifier object shape as `owns`. |
| entity.relationships.supervises | object | all | Identifiers of entities this entity supervises, manages, or is responsible for (e.g. manager–reporting-line or org hierarchy). Same flat identifier object shape. |
| entity.relationships.administered_by | object | all | Identifiers of identities that administer this entity (incoming relationship: “who administers this entity”). Renamed from `administrators` so naming is directionally consistent with outgoing verbs on `owns`, `depends_on`, and `supervises`. Same flat identifier object shape. |

_Indicative only; specific integrations may justify exceptions. **all** under Applied Entity Type means User, Host, or Service whenever the relationship applies to that normalized entity._

### Relationship identifier structure

Source systems often provide relationships as **arrays of objects** (e.g. supervised users with `email`, `id`, `name`). ECS entity indices and ESQL usage favor **flat** mappings: nested object lists are difficult to query under current ESQL nested support.

**Convention:** Each `entity.relationships.*` value is an **object** whose properties are optional **keyword arrays**. Producers populate as many identifier slots as they have (e.g. `host_id`, `user_id`, `email`, `hostname`, `username`, `entity_id`). This is intentionally a **bag of identifiers**: it does not preserve which email pairs with which id in a single structure. Correlation and pairing are expected to be resolved by entity-building logic or downstream normalization (similar in spirit to populating `related.user`, `related.host`, etc. with parallel arrays).

Example:

```json
{
  "entity_id": ["abc123"],
  "host_id": ["host-uuid-123", "host-uuid-456"],
  "user_id": ["00u123"],
  "email": ["supervisor@corp.example"],
  "hostname": [],
  "username": ["jsmith"]
}
```

Integrations may emit richer structures in raw pipelines; **normalization into this flat object** is recommended before or at entity-store ingest. A documented `type:identifier` string convention (e.g. `host:workstation-123`) is **not** required by this RFC; prefer explicit keyed arrays as above to avoid divergent string formats per integration.

## Field Re-use

Per [RFC 0049](https://github.com/elastic/ecs/blob/main/rfcs/text/0049-entity-fields.md), these leaves are expected under normalized entity paths such as `host.entity.*`, `user.entity.*`, `service.entity.*`, root `entity.*`, and under `*.target.entity.*` when the parent field set uses `target` (e.g. `user.target.entity.*`).

## Usage

These fields are intended to improve normalized entity representation for security, asset inventory, and graph-oriented workflows. The `entity.attributes.*` leaves capture non-temporal properties that analysts may want to filter or correlate across providers. The `entity.relationships.*` leaves support graph enrichment, dependency mapping, ownership modeling, and organizational context using **concrete relationship leaves** and a **flat, ESQL-friendly identifier object** per relationship type.

Example:

```json
{
  "@timestamp": "2026-03-31T12:00:00Z",
  "user": {
    "name": "paul",
    "entity": {
      "type": ["user"],
      "attributes": {
        "mfa_enabled": true,
        "permissions": ["read", "write", "reset_password"]
      },
      "lifecycle": {
        "last_activity": "2026-03-31T11:42:00Z"
      },
      "relationships": {
        "owns": {
          "host_id": ["workstation-123"],
          "hostname": ["macbook-pro-01"]
        },
        "supervises": {
          "email": ["erik@corp.example"],
          "user_id": ["00u1234567890"]
        }
      }
    }
  }
}
```

## Related work: entity-level risk

Reusing the existing ECS `risk.*` field set under **`entity.risk.*`** (when the score describes the normalized entity rather than only `host.risk.*` / `user.risk.*`) is related but **may be tracked in a separate issue or PR** for easier review.

**Guidance (from maintainer discussion on #2598):**

- The entity store does not compute risk by itself; **entity maintainers** (e.g. the risk engine) enrich existing entities.
- To stay entity-type agnostic, prefer **`entity.risk.*`** for normalized entity documents produced by the entity store / maintainers when the score applies to that normalized entity.
- **Do not mirror** the same logical score into both `entity.risk.*` and `host.risk.*` / `user.risk.*` / `service.risk.*` for the same normalized entity in a way that duplicates meaning; choose one placement consistent with whether the document is the generic entity view or a type-specific host/user/service document.

## Source data

Potential sources of data include:

* Identity provider and SaaS audit logs
* Cloud asset discovery logs
* Endpoint and device management platforms
* Other integrations that already populate or derive normalized entity metadata

## Scope of impact

At a high level, this proposal should be additive. Producers that already emit `host.entity.*`, `user.entity.*`, `service.entity.*`, or root `entity.*` would be able to populate these leaves directly. Consumers such as entity stores, graph enrichment systems, and investigation workflows would gain a more concrete and queryable schema for ownership, dependencies, supervision, administration, access posture, and (via related work) entity-level risk.

## Concerns

* Should ECS later define **`allowed_values`** for `storage_class`, `oauth_consent_restriction`, or relationship object keys to reduce drift across integrations?
* If **`permissions`** is extended in a future RFC, should sibling fields such as `inherited_permissions` or `effective_permissions` be introduced for disambiguation?
* Should code generation or field subsets **omit** certain `*.entity.attributes.*` paths per entity type using the **Applied Entity Type** column in the fields table above?

## People

The following are the people that consulted on the contents of this RFC.

* @uri-weisman | author
* @erikh-elastic | co-author
* @trisch-me | subject matter expert
* @andrewkroh | subject matter expert
* @chemamartinez | subject matter expert
* @narph | subject matter expert
* @romulets | subject matter expert

## References

- [1] <https://github.com/elastic/ecs/pull/2513>
- [2] <https://github.com/elastic/ecs/pull/2577>
- [3] <https://github.com/elastic/ecs/issues/2597>
- [4] <https://github.com/elastic/ecs/pull/2598>
- [5] <https://github.com/elastic/ecs/blob/main/rfcs/text/0053-new-device-fields.md>
- [6] <https://github.com/elastic/ecs/blob/main/rfcs/text/0049-entity-fields.md>
- [7] [ECS guidelines — singular and plural field names](https://www.elastic.co/docs/reference/ecs/ecs-guidelines)

### RFC Pull Requests

- Stage 0: TBD
