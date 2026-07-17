# 0056: Host Tags Field

- Stage: **Proposal**
- Date: **TBD**
- Target maturity: **alpha**

## Summary

Add `host.tags`: a free-form keyword field that lets users attach one or more arbitrary tags to a host (e.g. `APP-A_PROD`, `team-platform`) for search, alerting, and access control across Security and Observability. It's the host-scoped counterpart to the existing root `tags` field: where `tags` describes the event, `host.tags` describes the host asset itself, and it propagates anywhere `host` is reused (e.g. `host.target.tags`).

An earlier draft of this RFC proposed `host.group` as a single scalar value, and the originating issue also proposed a parallel `agent.group`. Both are dropped here. Reviewers pointed out that `group` collides in name with ECS's existing reusable `group` field set, and that a free-form, user-defined value fits the existing `tags` naming better than an implied membership construct. See [Concerns](#concerns) for the full reasoning, including whether this is redundant with the root `tags` field.

## Usage

Today, users who want to search, alert on, or restrict access to a subset of their fleet (e.g. all hosts belonging to a particular application, environment, or business unit) have no standardized field to do so, and typically resort to ad hoc custom fields. This leads to inconsistent naming across integrations and deployments, making cross-source queries and shared detection rules harder to build.

With `host.tags` populated (typically by a Fleet agent policy or an equivalent configuration-management mechanism at enrollment/deployment time), users could:

* **Security**: Scope detection rules to hosts carrying a given tag (e.g. only alert on privilege escalation on hosts tagged `APP-A_PROD`), and triage alerts filtered or aggregated by tag.
* **Observability**: Filter or aggregate metrics and logs by tag (e.g. compare error rates between hosts tagged `APP-A_PROD` and `APP-A_DEV`) without relying on per-integration custom fields.
* **ABAC**: Grant a user or role access only to data from hosts carrying a given tag, using a single consistent field across all data sources rather than per-integration custom fields.

Since a Fleet policy (not each integration) is what sets the value, it works the same way no matter which module or dataset produced the event.

## Fields

The proposed field definition is in [`rfcs/text/0056/host.yml`](./0056/host.yml).

```yaml
- name: host
  fields:
    - name: tags
      type: keyword
      level: extended
      short: User-configurable tags used to classify a host.
      description: >
        User-configurable, arbitrary tags used to classify a host for
        search, alerting, and access control purposes. A host can carry
        more than one tag at a time, for example an environment tag and
        a team or application tag.

        These values are expected to be assigned by the entity that
        manages the host's monitoring configuration (e.g. a Fleet
        policy or configuration management system), not derived from
        data on the host itself.
      example: '["APP-A_PROD", "team-platform"]'
      normalize:
        - array
      alpha: This field is alpha and subject to change.
```

The field is a keyword array (`normalize: array`), matching the pattern of the root `tags` field, rather than the single scalar value proposed in the earlier `host.group` draft. See [Concerns](#concerns) for the tradeoffs of an array versus a single canonical value, and for whether this duplicates the root `tags` field.

## Source data

### System metrics (Metricbeat via Elastic Agent)

Two hosts, `host001` and `host002`, both enrolled under the same Fleet policy and tagged `APP-A_PROD`, emitting `system.process.summary` metricsets. Tagging lets a dashboard or alert aggregate process health across the whole tagged set rather than per host.

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
    "tags": ["APP-A_PROD"],
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

### Web server logs (Filebeat nginx module) across a horizontally scaled tier

Multiple nginx instances behind a load balancer are tagged with both a tier tag and an autoscaling-group tag. Tagging lets users compare request latency or error rates for the whole tier without listing every hostname, or narrow further to one autoscaling group.

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
    "tags": ["web-tier-prod", "asg-web-3"],
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

### Authentication events (Auditbeat) scoped by host tag

A failed SSH login on a host tagged `APP-B_DEV`. A detection rule scoped to `host.tags: APP-B_DEV` can alert on repeated failures across that set without listing every dev host by name.

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
    "tags": ["APP-B_DEV"],
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

**Ingestion:** No breaking changes; the field is purely additive. Nothing currently populates `host.tags`. In practice, Fleet would need a policy-level setting (analogous to how Fleet already lets users configure the root `tags` on an integration policy) to let users assign tags at enrollment time; until that exists, users could populate the field manually via an `add_fields` processor. Beats/Agent configuration is otherwise unaffected.

Not every data source would pick this up automatically. Elastic Defend, for example, doesn't inherit generic Fleet Agent Policy field injection the way Beats-based integrations do, since its events are constructed by the endpoint agent's own binary rather than passed through the standard elastic-agent input processor pipeline. Populating `host.tags` for Defend-originated alerts would need separate engineering work (e.g. a Defend-specific policy setting, or a downstream enrichment step), not just the generic Fleet mechanism. This should be scoped and confirmed with the Endpoint team before committing to the field working uniformly across all Security data sources.

**Usage:** The Kibana [Security fields reference](https://www.elastic.co/guide/en/security/current/siem-field-reference.html) should be updated once the field is added. Detection rules, ABAC role queries, and Observability dashboards can reference the new field directly with no code changes required, since it's a plain keyword field.

**ECS project:** One field addition to `schemas/host.yml`, plus regenerated docs and generated schema artifacts. No existing field is modified.

## Concerns

**Why rename from `host.group` to `host.tags`?** An earlier draft proposed `host.group` as a single scalar value. Reviewers pointed out that `group` collides in name with ECS's existing reusable `group` field set (`schemas/group.yml`, an `id`/`name`/`domain` object used for OS-level groups at `user.group.*`, `process.group.*`, and others). Even though the paths never actually overlap (`host` isn't in that field set's `expected` list), reusing the term risks confusion, and it would foreclose ever reusing the real `group` field set under `host` in the future. `tags` avoids that collision and matches the free-form, user-defined nature of the field better than a name that implies formal, structured membership.

**Why an array instead of the single canonical value proposed earlier?** A host commonly needs more than one classification at once (an environment, plus a team, plus an application), and an array lets those coexist without inventing a separate field for each. The tradeoff: if the actual goal is a single, authoritative value used to drive per-host configuration or access decisions, an unordered tag list is a weaker tool for that than a scalar. Nothing enforces that exactly one tag represents "the" group, so two different consumers could reasonably disagree about which tag in the list is authoritative for their purposes. If that turns out to matter in practice, a single canonical scoping value may still be worth proposing separately, rather than trying to recover it from this field by convention.

**Isn't this redundant with the existing root `tags` field?** Partially, but scoping it to `host` does real work that the root field can't. The root `tags` field (`schemas/base.yml`) tags the event as a whole and has no way to say which entity a tag describes. An event can carry more than one host (`host.*` and, via existing reuse, `host.target.*`), and root `tags` can't distinguish which one a given tag applies to. `host.tags` is scoped to the host itself, so `host.tags` and `host.target.tags` can carry different values in the same event, something the flat root field structurally cannot do.

That said, there's no existing ECS precedent for an entity-scoped keyword-array tags field. The closest analog, `container.labels`, is a key/value object, not an array. Introducing `host.tags` as a plain array is a new pattern for ECS, worth reviewers confirming rather than assuming it follows established practice. There's also a real risk of double-populating: if an integration writes the same classification into both root `tags` and `host.tags`, that's duplicate data with no benefit. The field should be populated when a tag genuinely describes the host asset itself (e.g. sourced from a Fleet policy or CMDB), not simply copied from whatever the event's own `tags` happen to be.

**Why only `host.tags`, and not `agent.tags` too?** The originating issue proposed both `agent.group` and `host.group`, with parallel example events setting them to the same value. In the common case, a Fleet-managed integration reporting on the host it runs on (Metricbeat, Filebeat, Elastic Defend), the agent's tags and the host's tags would always be identical, since a Fleet policy is assigned per enrolled agent and one agent maps to one host. Shipping both just duplicates the same values in two places for no benefit.

There is a real case where an agent's own classification would differ from the host's: when the agent is a collector for hosts other than itself, an SNMP poller reporting on many network devices, a syslog aggregator receiving events from many upstream devices, or a cloud/Kubernetes API scraper. But ECS already has a fieldset for exactly that "entity observing from outside the host" concept: `observer.*` (`schemas/observer.yml`). If collector-level tagging turns out to be needed, it belongs there, not as a new `agent.tags`. This also matches existing ECS precedent for asset-level classification fields: the reusable `risk` fieldset (`schemas/risk.yml`) is reused only at `host` and `user`, and the reusable `entity` fieldset (`schemas/entity.yml`) is reused at `user`, `cloud`, `host`, `service`, and `orchestrator`. Neither is ever reused at `agent`, because `agent` represents the collecting software, not the asset being classified.

**What about the other entities in that same list, e.g. a `service.tags`?** Checked, and none of them need one. Most already have an equivalent concept: `service.environment` exists today and its description already covers a similar use case ("can also group services and applications from the same environment"); `orchestrator.namespace` gives Kubernetes workloads a native grouping construct; `cloud.account.*` and `cloud.project.*` give cloud resources one; `container.labels` gives containers an arbitrary key/value equivalent. `host` is the one entity in that list with no classification field at all, which is exactly the gap this proposal fills. If a real need for something more structured surfaces later for one of the others, that would be its own RFC, not an extension of this one.

**Can this be trusted for ABAC with multiple values?** Only as much as whatever sets the field, same as before, the value must come from a trusted source (e.g. a Fleet policy), not from the monitored host itself. But being multi-valued changes the shape of the authorization check: instead of matching a single canonical value, an ABAC rule has to check for tag membership, for example "`host.tags` contains `APP-A_PROD`." That's a weaker guarantee than an exact-match scalar. Nothing stops an unrelated process or integration from adding an extra tag to the same host, and a role scoped to one tag has no way to know whether the other tags present on that host imply broader exposure than intended. Access-control policies built on this field should treat it as "at least one of these tags is present," not as a single source of truth, and reviewers evaluating the ABAC use case should confirm that model is acceptable.

**Does this interact with `host`'s existing reuse at `host.target.*`?** Yes, and that's expected. `host.tags` will show up everywhere `host` is already reused, the same as every other `host.*` field like `host.hostname`. No special handling needed.

## People

* @adrianchen-es | author
* @trisch-me | naming and design feedback
* @taylor-swanson | naming and design feedback

## References

- [elastic/ecs#2340](https://github.com/elastic/ecs/issues/2340): originating issue, "[Discuss] Add `agent.group` and `host.group` field"
- [ECS RFC process](https://github.com/elastic/ecs/blob/main/rfcs/PROCESS.md)
- [Elastic Security fields reference](https://www.elastic.co/guide/en/security/current/siem-field-reference.html)

### RFC Pull Requests

* Proposal: https://github.com/elastic/ecs/pull/2670
