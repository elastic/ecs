# 0037: Host metrics
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawman)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2023-03-01** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

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

## Fields

The following high level metrics should be per host to indicate its health:

* CPU used (in %) and load
* Memory used (in %, used, total)
* Disk usage (in %)  and io -> summary
* Network (traffic in / out)


This translates to the following metrics. The goal is to have as few as possible.

* host.cpu.system.norm.pct
* host.cpu.user.norm.pct
* host.fsstats.total_size.used (in bytes)
* host.fsstats.total_size.total (in bytes)
* host.fsstats.total_size.used.pct
* host.load.norm.1
* host.load.norm.5
* host.load.norm.15
* host.memory.actual.used.bytes
* host.memory.actual.used.pct
* host.memory.total
* host.network.egress.bytes
* host.network.ingress.bytes


cgroup metrics were left out of the proposal by design and might be added later on. More details around cgroups can be found in the [cgroup RFC](https://github.com/elastic/ecs/pull/1627).

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

These metrics can be used to give a quick overview on how a specific host is doing. Some examples:

* A agent is running on a host and reports metrics about some services running on it. These metrics are shipped in addition to show how the host is doing.
* A user is looking at service metrics delivered by APM. These metrics are used to show how the host the service is running on is doing.

In the context if usage, it is also important what is NOT part of the fields by design:

* Process metrics: Details around process metrics. For this, detailed collection around processes must be enabled
* Cgroup metrics: cgroup metrics might follow at a later stage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

The source of this data comes from monitoring a host like a Linux machine, laptop or a k8s node. The can come delivered through different shippers like Elastic Agent system metrics inputs, apm agents, prometheus node exporter and other host metric collectors.

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

Currently Elastic Agent and metricbeat ship data host/system metrics under the `system.*` prefix. This would change it to `host.*`. One of the reasons for this is that some metrics for network already exist under this prefix in ECS so conflicts can be prevented. Another advantage is that some of these fields might use newer field types like `gauge` and `counter` delivered by TSDB in Elasticsearch which is possible without a breaking change.

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

## Concerns


* One of the concerns is it needs to be figured out how to migrate to the new fields with the existing shippers.
* Not all metrics might be available on all operating systems. How will we deal with this limitation?
* [host.cpu.usage](https://github.com/elastic/ecs/blob/main/schemas/host.yml#L122) already exist, how do the new fields relate to it.
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

The following are the people that consulted on the contents of this RFC.

* @ruflin | author
* @andrewkroh | reviewer
* @felixbarny | reviewer
* @gizas | reviewer
* @lalit-satapathy | reviewer
* @neptunian | reviewer
* @tommyers-elastic | reviewer

<!--
Who will be or has been consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:
-->


## References

<!-- Insert any links appropriate to this RFC in this section. -->

* [Schema for metrics in ECS](https://github.com/elastic/ecs/issues/474)
* [Otel host metrics](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/hostmetricsreceiver/README.md)
* [ECS cgroup rfc](https://github.com/elastic/ecs/blob/main/rfcs/text/0028-cgroups.md)
* [Prometheus Node Exporter](https://prometheus.io/docs/guides/node-exporter/)
* [APM System metrics fields](https://www.elastic.co/guide/en/apm/server/current/exported-fields-system.html)
* [APM Agent system metrics fields](https://www.elastic.co/guide/en/apm/agent/java/current/metrics.html#metrics-system)
* [APM addition of Cgroup metrics](https://github.com/elastic/apm/issues/368)
* [Host metrics used in Inventory view of Kibana](https://www.elastic.co/guide/en/observability/master/host-metrics.html) ([related queries](https://github.com/elastic/kibana/tree/main/x-pack/plugins/infra/common/inventory_models/host/metrics/snapshot))

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/2129

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
