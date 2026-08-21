# 0058: Narrow entity field reuse

- Stage: **Proposal**
- Date: **TBD**
- Target maturity: **mixture**

This RFC does not add or change field definitions. `entity.id` remains GA; the other `entity.*` leaves remain beta. The change is where those fields are allowed to nest.

## Summary

Narrow `entity` reuse so the field set appears only at `entity.*`, `entity.target.*`, `user.entity.*`, `user.target.entity.*`, `host.entity.*`, and `service.entity.*`.

Two mechanics produce the extra copies today. First, `entity` is listed on `cloud` and `orchestrator`, which publishes `cloud.entity.*` and `orchestrator.entity.*`. Second, `entity` reuses at the default `order: 2`, the same pass as `user`, `cloud`, `service`, and `host`. Those field sets copy themselves into `effective`, `origin`, `changes`, and `target` after `entity` has already nested, so `entity` rides along into paths such as `user.effective.entity.*` and `cloud.origin.entity.*`.

This RFC deletes `cloud` and `orchestrator` from `entity`'s `expected` list and raises `entity` reuse to `order: 3`, then lists `user.target` explicitly so `user.target.entity.*` is kept. Producers that currently write `cloud.entity.*` or `orchestrator.entity.*` should use root `entity.*` instead. Self-nested copies such as `user.effective.entity.*` should not be populated.

## Usage

Entity-centric workflows still use `entity.*` as the common identity and classification layer on top of dedicated field sets. After this change, the nesting rule is:

- Host, user, and service entities keep `entity` under the matching dedicated field set: `host.entity.*`, `user.entity.*`, `service.entity.*`.
- When an event names both an acting user and a targeted user, the target carries `user.target.entity.*`.
- When an event names a targeted entity that is not a user (or has no dedicated field set), use `entity.target.*`.
- Cloud, orchestrator, and every other entity type without a dedicated identity field set in this allowlist use root `entity.*`.

Queries and entity-store pipelines that already key off `user.entity.id`, `host.entity.id`, `service.entity.id`, or root `entity.id` are unchanged. Dashboards or detections that filter `cloud.entity.*` or `orchestrator.entity.*` need to read root `entity.*` (typically with `entity.type` of `cloud` or `orchestrator`).

## Fields

No field definitions change. The proposed `reusable` block is in [`rfcs/text/0058/entity.yml`](./0058/entity.yml) and replaces the current block in [`schemas/entity.yml`](../../schemas/entity.yml):

```yaml
reusable:
  top_level: true
  order: 3
  expected:
    - user
    - user.target
    - host
    - service
    - at: entity
      as: target
      short_override: Targeted entity of action taken.
```

`order: 3` runs after the default `order: 2` pass in which `user`, `cloud`, `service`, and `host` copy themselves. Those copies therefore no longer include `entity`. `user.target` is listed explicitly because it is no longer created automatically.

`entity_reference.yml` stays at `order: 1`. Relationship identifier fields continue to nest under `entity.relationships.*` and under the remaining `*.entity.relationships.*` locations.

### Locations kept

| Location | How it is produced |
| --- | --- |
| `entity.*` | Top-level reuse (`top_level: true`) |
| `entity.target.*` | Self-nesting (`at: entity`, `as: target`) |
| `user.entity.*` | Foreign reuse into `user` |
| `user.target.entity.*` | Foreign reuse into `user.target` |
| `host.entity.*` | Foreign reuse into `host` |
| `service.entity.*` | Foreign reuse into `service` |

### Locations removed

| Location | Why it goes away |
| --- | --- |
| `cloud.entity.*` | `cloud` dropped from `expected` |
| `orchestrator.entity.*` | `orchestrator` dropped from `expected` |
| `cloud.origin.entity.*`, `cloud.target.entity.*` | Accidental copy; `entity` no longer nests under `cloud` before `cloud` self-nests |
| `user.effective.entity.*`, `user.changes.entity.*` | Accidental copy; `order: 3` runs after `user` self-nests |
| `service.origin.entity.*`, `service.target.entity.*` | Accidental copy; `order: 3` runs after `service` self-nests |
| `host.target.entity.*` | Accidental copy; not added to `expected` |

Maturity of the leaves is unchanged: `entity.id` is GA; `entity.name`, `entity.type`, `entity.source`, and the remaining `entity.*` fields are beta.

## Source data

### User entity (kept)

An identity-provider event describing a user continues to nest `entity` under `user`:

```json
{
  "@timestamp": "2026-08-21T12:00:00.000Z",
  "event": { "kind": "event", "category": ["iam"], "type": ["user", "info"] },
  "user": {
    "id": "00u1a2b3c4d5",
    "name": "jsmith",
    "entity": {
      "id": "00u1a2b3c4d5",
      "name": "jsmith",
      "type": ["user"],
      "source": "okta"
    }
  }
}
```

### Targeted user (kept)

An IAM action that names both actor and target keeps `entity` on `user.target`:

```json
{
  "@timestamp": "2026-08-21T12:01:00.000Z",
  "event": { "kind": "event", "category": ["iam"], "type": ["user", "change"], "action": "user-privilege-change" },
  "user": {
    "id": "00u-admin",
    "name": "admin",
    "entity": {
      "id": "00u-admin",
      "type": ["user"]
    },
    "target": {
      "id": "00u-jsmith",
      "name": "jsmith",
      "entity": {
        "id": "00u-jsmith",
        "type": ["user"]
      }
    }
  }
}
```

### Cloud resource without a dedicated field set (moved to root `entity.*`)

An S3 bucket or similar cloud object should no longer use `cloud.entity.*`. Put classification on root `entity.*` and keep `cloud.*` for provider context:

```json
{
  "@timestamp": "2026-08-21T12:02:00.000Z",
  "event": { "kind": "event", "category": ["configuration"], "type": ["info"] },
  "cloud": {
    "provider": "aws",
    "region": "us-east-1",
    "account": { "id": "123456789012" }
  },
  "entity": {
    "id": "arn:aws:s3:::logs-bucket",
    "name": "logs-bucket",
    "type": ["bucket"],
    "sub_type": "aws_s3_bucket",
    "source": "aws"
  }
}
```

## Scope of impact

This is a breaking schema change: generated mappings, CSV, Beats fields, and reference docs stop listing the removed paths.

**Ingestion:** Beats, Elastic Agent integrations, and ingest pipelines that currently write `cloud.entity.*` or `orchestrator.entity.*` must map those values to root `entity.*`. Pipelines that copied `entity` onto `user.effective`, `user.changes`, `cloud.origin`, `cloud.target`, `service.origin`, `service.target`, or `host.target` should stop doing so. Integrations that already populate `user.entity.*`, `host.entity.*`, `service.entity.*`, `user.target.entity.*`, or root `entity.*` do not need to change.

**Usage:** Entity analytics, asset inventory, and detections that query the removed paths will miss data until they switch to the kept locations. `entity.id` at the root and under `user` / `host` / `service` remains the correlation key.

**ECS project:** `schemas/entity.yml` reuse metadata, `schemas/subsets/main.yml` (drop the `cloud.entity` whitelist entry), generated artifacts, and `docs/reference/ecs-entity.md` field-reuse lists. `entity_reference` reuse is unchanged.

## Concerns

**Does dropping `cloud.entity.*` conflict with RFC 0049?** RFC 0049 told producers to nest `entity` under `host`, `user`, `service`, `cloud`, or `orchestrator` when the type matched those field sets. This RFC revises that allowlist to host, user, and service only. Cloud and orchestrator remain valid `entity.type` values; they are represented at root `entity.*` plus the existing `cloud.*` / `orchestrator.*` field sets. That matches how types without a dedicated field set were already modeled.

**Why keep `user.target.entity.*` but not `host.target.entity.*` or `service.target.entity.*`?** User events routinely name an actor and a distinct targeted identity (`user` vs `user.target`). Host and service `target` copies were an artifact of reuse order, not an established producer pattern. They can be added later with an explicit `expected` entry if a use case appears.

**Will `order: 3` break `entity_reference`?** No. `entity_reference` stays at `order: 1` and nests under `entity` before `entity` is copied into `user`, `host`, and `service`. Relationship fields remain available at the kept locations.

**Can this wait for a major version?** The extra nestings are unused accidental copies plus two roots (`cloud`, `orchestrator`) that duplicate root `entity.*` for the same types. Removing them now avoids integrations adopting paths that will have to be undone. Because field removal is breaking, this RFC is required; the ECS team can still defer the schema merge to a major if they prefer.

**OTel overlap?** None. This change only relocates ECS reuse of `entity`; it does not add or rename leaves or introduce OTel mappings.

## People

* Quan Nguyen | author

## References

- [RFC 0049: Entity Field Set](./0049-entity-fields.md) — original field set and reuse guidance
- [RFC 0054: Extend entity fields](./0054-extend-entity-fields.md) — attributes, lifecycle, and relationships under the same reuse model
- [ECS field reuse](https://www.elastic.co/docs/reference/ecs/ecs-guidelines#_field_reuse) — `order` and `expected` semantics
- [Field stability](https://github.com/elastic/ecs/blob/main/docs/reference/ecs-principles-design.md#_field_stability)

### RFC Pull Requests

* Proposal: https://github.com/elastic/ecs/pull/NNNN
