# 0000: Extend entity fields with additional attributes, lifecycle, relationships, and risk reuse



- Stage: **0 (strawperson)** 
- Date: **TBD** 



This RFC proposes a focused extension to the ECS `entity.`* schema by adding a small set of concrete `entity.attributes.*`, `entity.lifecycle.*`, and `entity.relationships.*` leaves, and by enabling `entity.risk.*` reuse under `entity`. The goal is to make normalized entity data more useful for security, asset, and graph-oriented use cases without introducing a broad or underspecified object model. This proposal follows the direction established in the existing entity RFC and is intended to consolidate the ongoing discussion around relationship naming and risk placement.

## Fields



| Field                                       | Type    | Description                                                                                                                |
| ------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------- |
| entity.attributes.storage_class             | keyword | The storage tier or class assigned to an object storage resource.                                                          |
| entity.attributes.mfa_enabled               | boolean | Indicates whether multi-factor authentication is enabled for this entity.                                                  |
| entity.attributes.granted_permissions       | keyword | The set of permissions explicitly granted to this entity. These are individual action-level permissions, not roles or groups. |
| entity.attributes.known_redirect            | keyword | A known redirect URI or URL associated with this entity, commonly for OAuth applications or services.                      |
| entity.attributes.managed                   | boolean | Indicates whether the entity is managed by an external administration or control system. Applies primarily to host entity. |
| entity.attributes.oauth_consent_restriction | keyword | Indicates any restriction applied to OAuth consent for this entity (e.g., `admin_only`, `verified_only`, `unrestricted`). |
| entity.lifecycle.last_activity              | date    | The timestamp of the most recent action performed by or attributed to this entity. Distinct from `last_seen`: this implies the entity was active, not just observed. |
| entity.relationships.owns                   | keyword | Captures asset ownership, such as a user owning a host, email address, Windows SID, or employee ID.                       |
| entity.relationships.depends_on             | keyword | Identifiers of entities that this entity depends on to function.                                                           |
| entity.relationships.supervises             | keyword | Identifiers of entities that this entity supervises, manages, or is responsible for.                                       |
| entity.relationships.administrators         | keyword | The list of identities (usernames, emails, or IDs) that administer this entity.                                            |


This RFC also proposes enabling `entity.risk.*` field reuse so the existing ECS `risk.*` fields can be nested under `entity` when the risk score describes the normalized entity rather than a specific entity-type field set.

## Usage



These fields are intended to improve normalized entity representation for security, asset inventory, and graph-oriented workflows. The `entity.attributes.*` leaves capture non-temporal properties that analysts may want to filter or correlate across providers, such as whether an identity has MFA enabled, whether a host or service is centrally managed, or whether an application is subject to OAuth consent restrictions.
The `entity.relationships.*` leaves are meant to support graph enrichment, dependency mapping, ownership modeling, and organizational context. Using concrete relationship leaves instead of an open-ended `entity.relationship` object should make the schema easier for ECS users to understand, query, and review. Enabling `entity.risk.*` under `entity` allows risk scores to be attached to entities generically, rather than requiring different placement depending on whether the normalized entity is a host, user, service, or a more generic type.

Example:

```json
{
  "@timestamp": "2026-03-31T12:00:00Z",
  "user": {
    "name": "paul",
    "entity": {
      "type": "user",
      "attributes": {
        "mfa_enabled": true,
        "granted_permissions": ["read", "write", "reset_password"]
      },
      "lifecycle": {
        "last_activity": "2026-03-31T11:42:00Z"
      },
      "risk": {
        "calculated_level": "Moderate",
        "calculated_score": 47.3,
        "calculated_score_norm": 47.3
      },
      "relationships": {
        "owns": ["host:workstation-123"],
        "supervises": ["user:erik@okta"]
      }
    }
  }
}
```

## Source data



Potential sources of data include:

- identity provider and SaaS audit logs
- cloud asset discovery logs
- endpoint and device management platforms
- other integrations that already populate or derive normalized entity metadata

## Scope of impact



At a high level, this proposal should be additive. Producers that already emit `host.entity.*`, `user.entity.*`, `service.entity.*`, or root `entity.*` would be able to populate these leaves directly. Consumers such as entity stores, graph enrichment systems, and investigation workflows would gain a more concrete and queryable schema for ownership, dependencies, supervision, access posture, and entity-level risk.

## Concerns



- Should `entity.relationships.administrators` remain a multi-valued `keyword` list of identifiers, or should ECS eventually define a richer identity structure for administrator references?
- Should `entity.attributes.known_redirect` remain singular in name while allowing multiple values, or should ECS prefer a pluralized field name?
- Once `entity.risk.*` is enabled under `entity`, should ECS explicitly recommend avoiding duplicate risk storage under entity-type-specific paths when the same score describes the normalized entity?

## People

The following are the people that consulted on the contents of this RFC.

- @uri-weisman | author
- @erikh-elastic | co-author
- @trisch-me | subject matter expert
- @andrewkroh | subject matter expert
- @chemamartinez | subject matter expert
-  @narph | subject matter expert
## References

- [1] [https://github.com/elastic/ecs/pull/2513](https://github.com/elastic/ecs/pull/2513)
- [2] [https://github.com/elastic/ecs/pull/2577](https://github.com/elastic/ecs/pull/2577)
- [3] [https://github.com/elastic/ecs/issues/2597](https://github.com/elastic/ecs/issues/2597)
- [4] [https://github.com/elastic/ecs/blob/main/rfcs/text/0053-new-device-fields.md](https://github.com/elastic/ecs/blob/main/rfcs/text/0053-new-device-fields.md)
- [5] [https://github.com/elastic/ecs/blob/main/rfcs/text/0049-entity-fields.md](https://github.com/elastic/ecs/blob/main/rfcs/text/0049-entity-fields.md)

### RFC Pull Requests



- Stage 0: TBD

