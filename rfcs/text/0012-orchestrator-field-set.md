# 0012: Orchestrator field set creation

- Stage: **1 (draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-01-11** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

There is currently no ECS field set for container orchestration engines. There is an example of an ECS
[use-case][0] for Kubernetes, but it largely relies on other ECS field sets, and doesn't cover all of the
potential fields relevant to typical orchestrators. The purpose of this RFC is to propose some improvements to
the existing use-case and then turn it into a full-featured ECS field set, with a larger number of
fields that describe orchestrator-specific primitives which are currently missing (such as cluster names or
resource types, for example).

One use case for this is to allow easier work with [Kubernetes audit logs][1]. Consistent
field definitions will allow teams working with Kubernetes audit logs to share and correlate
data/alerts/visualisations far more easily than currently possible.

There should not be any breaking impact as a result of this change, due to the fact that it should solely
add a new schema rather than change existing material.

## Fields

The proposed change adds six fields, as described below:

```
---
- name: orchestrator
  title: Orchestrator
  group: 2
  short: Fields relevant to container orchestrators.
  description: >
    Fields that describe the resources which container orchestrators manage or
    act upon.
  type: group
  fields:
    - name: cluster
      level: extended
      type: object
      description: >
        Orchestrator cluster details.

    - name: type
      level: extended
      type: keyword
      example: kubernetes
      description: >
        Orchestrator cluster type (e.g. kubernetes, nomad or cloudfoundry).

    - name: organization
      level: extended
      type: keyword
      example: elastic
      description: >
        Organization affected by the event (for multi-tenant orchestrator setups).

    - name: namespace
      level: extended
      type: keyword
      example: kube-system
      description: >
        Namespace in which the action is taking place.

    - name: resource.name
      level: extended
      type: keyword
      example: test-pod-cdcws
      description: >
        Name of the resource being acted upon.

    - name: resource.type
      level: extended
      type: keyword
      example: service
      description: >
        Type of resource being acted upon.

    - name: api_version
      level: extended
      example: v1beta1
      type: keyword
      description: >
        API version being used to carry out the action
```

<!--
Stage 2: Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

The `orchestrator` field set will be used to capture typical concepts employed
by container orchestrators to manage resources. The key intent of this is to create
a consistent method by which audit logs from container orchestrators can
be compared. For example, this would allow the creation of open source detection
rulesets for suspicious Kubernetes events based on audit logs, which can be easily
transferred from one cluster to another without depending on the specifics of
parsing implementations.

This might also have use in performance and monitoring tooling which exists around
container orchestrators, allowing for the definition of shareable dashboards and
alert definitions.

## Source data

Examples of source data include:

- [Kubernetes audit logs][1]
- [Kubernetes node logs][2]
- [HashiCorp Nomad audit logs][3]
- [Falco alert logs][4]

### Kubernetes audit log

```json
{
  "_index": "filebeat-7.7.0-2020.12.31-000001",
  "_type": "_doc",
  "_id": "KbmPuXYBaTdcl42uyGfl",
  "_version": 1,
  "_score": null,
  "_source": {
    "@timestamp": "2020-12-31T16:09:35.735Z",
    "log": {
      "offset": 7248566,
      "file": {
        "path": "/tmp/host-logs/kube-apiserver-audit.log"
      }
    },
    "cloud.provider": "gcp",
    "event.action": "create",
    "orchestrator.cluster": {
        "name": "test-dev",
    },
    "orchestrator.type": "kubernetes",
    "orchestrator.subresource": "attach",
    "orchestrator.resource.type": "pod",
    "orchestrator.namespace": "default",
    "orchestrator.resource.name": "test",
    "orchestrator.api_version": "v1",
    "user.name": "system:serviceaccount:test"
  }
}
```

### Hashicorp Nomad audit log

```json
{
  "created_at": "2020-03-24T13:09:35.704224536-04:00",
  "event_type": "audit",
  "orchestrator.api_version": "v1",
  "orchestrator.namespace": "default",
  "orchestrator.resource.type": "nodes",
  "orchestrator.type": "nomad",
  "payload": {
    "id": "8b826146-b264-af15-6526-29cb905145aa",
    "stage": "OperationComplete",
    "type": "audit",
    "timestamp": "2020-03-24T13:09:35.703865005-04:00",
    "version": 1,
    "auth": {
      "accessor_id": "a162f017-bcf7-900c-e22a-a2a8cbbcef53",
      "name": "Bootstrap Token",
      "global": true,
      "create_time": "2020-03-24T17:08:35.086591881Z"
    },
    "request": {
      "id": "02f0ac35-c7e8-0871-5a58-ee9dbc0a70ea",
      "event.action": "GET",
      "request_meta": {
        "remote_address": "127.0.0.1:33648",
        "user_agent": "Go-http-client/1.1"
      },
      "node_meta": {
        "ip": "127.0.0.1:4646"
      }
    },
    "response": {
      "status_code": 200
    }
  }
}
```

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

## Concerns

### Kubernetes-specific logic

The key concern here is the dominance of one particular container orchestration
system - Kubernetes - over the rest of the ecosystem. Other orchestrators include
options like HashiCorp Nomad, Docker Swarm, and Apache Mesos, but it is unclear to
what extent the alternatives share the same logical primitives as Kubernetes. An
attempt has been made to ensure that the proposed field set is as generic and flexible 
as possible, however it would be useful to consider in some detail whether the
preference is to keep the field set as generic as possible, or large enough to 
cover all the logical primitives of popular orchestrators. Input from contributors
who have experience with the various alternative orchestration providers would be
particularly valuable.

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

* @ferozsalam | author

## References

* [Kubernetes ECS use case][0]
* [Kubernetes audit log documentation][1]

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1209
* Stage 1: https://github.com/elastic/ecs/pull/1230

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->

[0]: https://github.com/elastic/ecs/blob/master/use-cases/kubernetes.yml
[1]: https://kubernetes.io/docs/tasks/debug-application-cluster/audit/
[2]: https://kubernetes.io/docs/concepts/cluster-administration/logging/#logging-at-the-node-level
[3]: https://www.hashicorp.com/blog/hashicorp-nomad-enterprise-audit-logging
[4]: https://falco.org/docs/alerts/#file-output
