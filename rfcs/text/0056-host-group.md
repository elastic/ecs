# 0056: Host Group Field

- Stage: **Proposal**
- Date: **TBD**
- Target maturity: **alpha**

## Summary

Add `host.group`: a free-form keyword field that lets users assign an arbitrary label to a set of hosts (e.g. `APP-A_PROD`, `APP-A_DEV`). This plays the same role `data_stream.namespace` plays for data streams: a single field Security and Observability can search, alert, and grant access on by group.

The originating issue also proposed a parallel `agent.group` field. This proposal drops it: see [Concerns](#concerns) for why the host is the right level and the agent is not.

## Usage

Today, users who want to search, alert on, or restrict access to a subset of their fleet (e.g. all hosts belonging to a particular application, environment, or business unit) have no standardized field to do so, and typically resort to ad hoc custom fields. This leads to inconsistent naming across integrations and deployments, making cross-source queries and shared detection rules harder to build.

With `host.group` populated (typically by a Fleet agent policy or an equivalent configuration-management mechanism at enrollment/deployment time), users could:

* **Security**: Scope detection rules to a group of hosts (e.g. only alert on privilege escalation within `APP-A_PROD`), and triage alerts filtered or aggregated by group.
* **Observability**: Filter or aggregate metrics and logs by group (e.g. compare error rates between `APP-A_PROD` and `APP-A_DEV`) without relying on per-integration custom fields.
* **ABAC**: Grant a user or role access only to data from hosts in a given group, using a single consistent field across all data sources rather than per-integration custom fields.

Since a Fleet policy (not each integration) is what sets the value, it works the same way no matter which module or dataset produced the event.

## Fields

The proposed field definition is in [`rfcs/text/0056/host.yml`](./0056/host.yml).

```yaml
- name: host
  fields:
    - name: group
      type: keyword
      level: extended
      short: User-configurable label used to group a set of hosts.
      description: >
        A user-configurable, arbitrary label used to group a set of hosts
        for search, alerting, and access control purposes.

        This value is expected to be assigned by the entity that manages
        the host's monitoring configuration (e.g. a Fleet policy or
        configuration management system), not derived from data on the
        host itself.
      example: APP-A_PROD
      alpha: This field is alpha and subject to change.
```

The field is modeled as a single scalar keyword, not an array, matching `data_stream.namespace`: a given host belongs to one grouping label at a time. See [Concerns](#concerns) for the naming choice, the alternative of reusing `tags`/`labels`, and single vs. multi-value grouping.

## Source data

### System metrics (Metricbeat via Elastic Agent)

Two hosts, `host001` and `host002`, both enrolled under the same Fleet policy for the `APP-A_PROD` group, emitting `system.process.summary` metricsets. Grouping lets a dashboard or alert aggregate process health across the whole group rather than per host.

```json
{
  "@timestamp": "2024-05-04T13:30:09.885Z",
  "agent": {
    "ephemeral_id": "85174b4b-4415-46c4-89ce-160e27a56bc5",
    "id": "a8435320-1d60-49f7-b1e7-25ed5d5eb59c",
    "name": "host001",
    "type": "metricbeat",
    "version": "8.13.3"
  },
  "data_stream": {
    "dataset": "system.process.summary",
    "namespace": "default",
    "type": "metrics"
  },
  "host": {
    "hostname": "host001",
    "name": "host001",
    "group": "APP-A_PROD",
    "id": "0ba1be1199e74165a458a3bb0f65fb8f",
    "os": {
      "family": "redhat",
      "name": "Red Hat Enterprise Linux",
      "platform": "rhel"
    }
  },
  "metricset": {
    "name": "process_summary",
    "period": 10000
  },
  "system": {
    "process": {
      "summary": {
        "sleeping": 272,
        "total": 370,
        "zombie": 1
      }
    }
  }
}
```

### Web server logs (Filebeat nginx module) across a horizontally scaled group

Multiple nginx instances behind a load balancer are enrolled under the `web-tier-prod` group. Grouping lets users compare request latency or error rates for the whole tier without listing every hostname.

```json
{
  "@timestamp": "2026-06-01T09:12:44.201Z",
  "agent": {
    "id": "5b6e6a9a-1cf1-4d3a-9c0b-2f2d6a2e9a11",
    "name": "web-03",
    "type": "filebeat",
    "version": "8.15.0"
  },
  "host": {
    "hostname": "web-03",
    "name": "web-03",
    "group": "web-tier-prod",
    "id": "5c9a2c3e7f4a4e6d9a7b3e2c1d0f9a8b"
  },
  "http": {
    "request": {
      "method": "GET"
    },
    "response": {
      "status_code": 200
    }
  },
  "url": {
    "original": "/checkout"
  },
  "event": {
    "dataset": "nginx.access",
    "duration": 8213000
  }
}
```

### Authentication events (Auditbeat) scoped by host group

A failed SSH login on a host in the `APP-B_DEV` group. A detection rule scoped to `host.group: APP-B_DEV` can alert on repeated failures within that group without listing every dev host by name.

```json
{
  "@timestamp": "2026-06-02T17:45:03.912Z",
  "agent": {
    "id": "e2a1f9d4-7b3c-4a2e-9f1d-8c6b5a4e3d2f",
    "name": "dev-app-07",
    "type": "auditbeat",
    "version": "8.15.0"
  },
  "host": {
    "hostname": "dev-app-07",
    "name": "dev-app-07",
    "group": "APP-B_DEV",
    "os": {
      "family": "debian",
      "name": "Ubuntu"
    }
  },
  "event": {
    "category": ["authentication"],
    "type": ["start"],
    "outcome": "failure"
  },
  "user": {
    "name": "deploy"
  },
  "source": {
    "ip": "203.0.113.44"
  }
}
```

## Scope of impact

**Ingestion:** No breaking changes; the field is purely additive. Nothing currently populates `host.group`. In practice, Fleet would need a policy-level setting (analogous to how Fleet already lets users configure `tags` on an integration policy) to let users assign a group label at enrollment time; until that exists, users could populate the field manually via an `add_fields` processor. Beats/Agent configuration is otherwise unaffected.

Not every data source would pick this up automatically. Elastic Defend, for example, doesn't inherit generic Fleet Agent Policy field injection the way Beats-based integrations do, since its events are constructed by the endpoint agent's own binary rather than passed through the standard elastic-agent input processor pipeline. Populating `host.group` for Defend-originated alerts would need separate engineering work (e.g. a Defend-specific policy setting, or a downstream enrichment step), not just the generic Fleet mechanism. This should be scoped and confirmed with the Endpoint team before committing to the field working uniformly across all Security data sources.

**Usage:** The Kibana [Security fields reference](https://www.elastic.co/guide/en/security/current/siem-field-reference.html) should be updated once the field is added. Detection rules, ABAC role queries, and Observability dashboards can reference the new field directly with no code changes required, since it's a plain keyword field.

**ECS project:** One field addition to `schemas/host.yml`, plus regenerated docs and generated schema artifacts. No existing field is modified.

## Concerns

**Why only `host.group`, and not `agent.group` too?** The originating issue proposed both, with parallel example events setting them to the same value. In the common case, a Fleet-managed integration reporting on the host it runs on (Metricbeat, Filebeat, Elastic Defend), the two values would always be identical, since a Fleet policy is assigned per enrolled agent and one agent maps to one host. Shipping both fields just duplicates the same string in two places for no benefit.

There is a real case where an agent's own grouping would differ from the host's: when the agent is a collector for hosts other than itself, an SNMP poller reporting on many network devices, a syslog aggregator receiving events from many upstream devices, or a cloud/Kubernetes API scraper. But ECS already has a fieldset for exactly that "entity observing from outside the host" concept: `observer.*` (`schemas/observer.yml`). If collector-level grouping turns out to be needed, it belongs there, not as a new `agent.group`. This also matches existing ECS precedent for asset-level classification fields: the reusable `risk` fieldset (`schemas/risk.yml`) is reused only at `host` and `user`, and the reusable `entity` fieldset (`schemas/entity.yml`) is reused at `user`, `cloud`, `host`, `service`, and `orchestrator`. Neither is ever reused at `agent`, because `agent` represents the collecting software, not the asset being classified.

**What about the other entities in that same list, e.g. a `service.group`?** Checked, and none of them need one. Most already have an equivalent concept: `service.environment` exists today and its description already covers this exact use case ("can also group services and applications from the same environment"); `orchestrator.namespace` gives Kubernetes workloads a native grouping construct; `cloud.account.*` and `cloud.project.*` give cloud resources one; `container.labels` gives containers an arbitrary key/value equivalent. `host` is the one entity in that list with no grouping field at all, which is exactly the gap this proposal fills. If a real need for something more structured than `service.environment` surfaces later, that would be its own RFC, not an extension of this one.

**Does `group` collide with the existing reusable `group` field set?** Not in the schema, but the name overlaps in a confusing way. ECS already has a reusable `group` field set (`schemas/group.yml`) for OS/directory-level groups: an object with `id`, `name`, and `domain`, reused today as `user.group.*`, `process.group.*`, `process.real_group.*`, and others. `host.group` is a different concept: a flat, user-assigned deployment label, not OS group membership. `host` isn't in that field set's `expected` list, so the paths never collide and there's no mapping conflict. What's left is a naming question: someone searching for "group" fields might expect the `id`/`name`/`domain` shape instead of a plain string. `group` matches the term used in the originating issue, and the two concepts sit on separate paths, but a more specific name like `host.deployment_group` may be worth weighing against that familiarity.

**Why not just reuse `tags` or `labels`?** Neither guarantees a consistent key across producers. `tags` (`schemas/base.yml`) is a general-purpose keyword array already used for many unrelated things per event, so nothing marks which value means "group." `labels` is an arbitrary key/value object with the same issue: one integration might use `labels.group`, another `labels.env`. A dedicated field gives every integration and consumer the same path to query, the same reasoning behind `data_stream.namespace` for a similar arbitrary-label need.

**Should the field support more than one group per host?** Not in this proposal. Every example in the originating issue shows a host in exactly one group, so the field is a scalar keyword, not an array, matching `data_stream.namespace`. Elasticsearch won't stop someone from indexing multiple values into a keyword field, but the field isn't designed or documented for that. Multi-group membership can be revisited later if it's actually needed.

**Can this be trusted for ABAC?** Only as much as whatever sets the field. The issue proposes granting access by `host.group`, so the value needs to come from a trusted source, not from the monitored host itself. The field description says the value should be assigned by whatever manages the host's monitoring configuration, a Fleet policy, for example. That's the same trust assumption already made today for namespace-based access control on `data_stream.namespace`.

**Does this interact with `host`'s existing reuse at `host.target.*`?** Yes, and that's expected. `host.group` will show up everywhere `host` is already reused, the same as every other `host.*` field like `host.hostname`. No special handling needed.

## People

* @adrianchen-es | author

## References

- [elastic/ecs#2340](https://github.com/elastic/ecs/issues/2340): originating issue, "[Discuss] Add `agent.group` and `host.group` field"
- [ECS RFC process](https://github.com/elastic/ecs/blob/main/rfcs/PROCESS.md)
- [Elastic Security fields reference](https://www.elastic.co/guide/en/security/current/siem-field-reference.html)

### RFC Pull Requests

* Proposal: https://github.com/elastic/ecs/pull/2670
