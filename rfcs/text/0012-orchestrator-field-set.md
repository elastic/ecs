# 0012: Orchestrator field set creation

- Stage: **3 (finished)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-05-14** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

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

The proposed change adds nine fields, as described below:

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
    - name: cluster.name
      level: extended
      type: keyword
      description: >
        Name of the cluster.

    - name: cluster.url
      level: extended
      type: keyword
      description: >
        URL of the cluster.

    - name: cluster.version
      level: extended
      type: keyword
      description: >
        The version of the cluster.

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
        "version": "1.19"
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
  "orchestrator.cluster": {
    "name": "test-dev",
    "version": "1.0.4"
  },
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

## Scope of impact

As this RFC involves the creation of an entirely new fieldset, no breaking
changes are envisaged. Some existing tooling might need updates to factor in the
new fieldset's availability, however.

### Ingestion mechanisms

- The [Filebeat][5] and [Metricbeat][7] processors will need updating, as they currently
  use fields that would be out-of-sync with ECS if this is committed.
- The CloudFoundry [Filebeat][8] and [Metricbeat][9] processors will need updating for the same
  reasons.
- The Nomad [processor][10] will need updating.
- Logstash should see no significant change.

### Usage mechanisms

- Elastic's detection-rules [repo][6] should see no change as there don't appear to
  be any orchestrator-specific definitions in place.

### ECS project

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

*Resolution*: Input from various orchestrators has been considered to ensure this field
set remains as generic as possible.

## People

The following are the people that consulted on the contents of this RFC.

* @ferozsalam | author
* @exekias | sponsor
* @ChrsMark | subject matter expert
* @jsoriano | subject matter expert
* @kaiyan-sheng | subject matter expert

## References

* [Kubernetes ECS use case][0]
* [Kubernetes audit log documentation][1]

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1209
* Stage 1: https://github.com/elastic/ecs/pull/1230
* Stage 2: https://github.com/elastic/ecs/pull/1299
* Stage 3: https://github.com/elastic/ecs/pull/1343

[0]: https://github.com/elastic/ecs/blob/master/use-cases/kubernetes.yml
[1]: https://kubernetes.io/docs/tasks/debug-application-cluster/audit/
[2]: https://kubernetes.io/docs/concepts/cluster-administration/logging/#logging-at-the-node-level
[3]: https://www.hashicorp.com/blog/hashicorp-nomad-enterprise-audit-logging
[4]: https://falco.org/docs/alerts/#file-output
[5]: https://www.elastic.co/guide/en/beats/filebeat/current/running-on-kubernetes.html
[6]: https://github.com/elastic/detection-rules/tree/main/rules
[7]: https://www.elastic.co/guide/en/beats/metricbeat/current/running-on-kubernetes.html
[8]: https://www.elastic.co/guide/en/beats/filebeat/current/running-on-cloudfoundry.html
[9]: https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-module-cloudfoundry.html
[10]: https://github.com/elastic/beats/blob/master/x-pack/libbeat/processors/add_nomad_metadata/nomad.go
