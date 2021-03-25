# 0005: Host Metric Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **3 (finished)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-03-25** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

We are proposing to add 7 new host fields into ECS for monitoring CPU, disk and network performance using Metricbeat.
With existing `host.id` and `host.name`, these total 9 fields will become the common field schema for host metrics.

Proposed 7 new fields are:
* host.cpu.usage
* host.network.ingress.bytes
* host.network.ingress.packets
* host.network.egress.bytes
* host.network.egress.packets
* host.disk.read.bytes
* host.disk.write.bytes

## Fields
This RFC calls for the addition of host fields to collect basic monitoring metrics from a host or VM such as CPU, network and disk.
Please see [`host.yml`](0005/host.yml) for definitions of all fields.

Note: the `host.network.*` and `host.disk.*` fields are gauges which represent
IO since the last metric collection. In order to interpret these metrics, the
collection period is needed. Collection period will be added into ECS separately.

<!--
Stage 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->

<!--
Stage 2: Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

These host metrics will be collected from different kinds of hosts such as bare
metal, virtual machines or virtual machines on public clouds like AWS, Azure and
GCP. These host metrics will be the standard minimal used in resource centric UI
views. For example, when user has VMs on bare metal, AWS and Azure, these host
fields will be collected from all VMs across all platforms and displayed in a
centralized location for better monitoring experience.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->
* Bare metal
* VMs
* AWS EC2 instances
* GCP compute engines
* Azure compute VMs

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

Please see example source document from AWS EC2 instance in
[aws-ec2.json](0005/aws-ec2.json) and example source document from Azure
compute VM in [azure-compute-vm.json](0005/azure-compute-vm.json).

For system metrics, CPU, network, diskIO are reported separately from different
metricsets. Please see example source document for CPU in [system-cpu.json](0005/system-cpu.json)
and network in [system-network.json](0005/system-network.json).

## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

No breaking changes required.
These are new fields already added into Metricbeat:
* aws ec2 metricset
* googlecloud compute metricset
* azure compute_vm metricset

Only change would be once these fields are in ECS, we can remove these fields
from `metricbeat/_meta/fields.common.yml` file.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

We need to carefully define each field because when these metrics are collected
from different platforms/services, the scope of these metrics change. We need to
make sure when users are using these metrics, they are all collected to represent
the same thing. For example, `host.network.in.bytes` needs to be an aggregated
value for all network interfaces. `host.cpu.pct` needs to be a normalized value
between 0 and 1.

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
Our goal is to switch related fields to these new host metrics in Kibana Observability
metrics UI. For example: right now under hosts inventory, CPU usage will only display
metrics that are collected by Metricbeat `system` module. With using the new host
metric fields, CPU metric from `system` module will be `host.cpu.usage`, as well
as CPU metrics from all AWS EC2 instances or Azure compute VMs. With
[Kibana Metrics UI](https://github.com/elastic/kibana/issues/87508) switching to
these new proposed host metric fields, all hosts will be discovered and displayed
in a single waffle map from different data collection sources.

## People

The following are the people that consulted on the contents of this RFC.

* @kaiyan-sheng | author
* @cyrille-leclerc | sponsor
* @exekias | subject matter expert

<!--
Who will be or has consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/947
* Stage 1: https://github.com/elastic/ecs/pull/950
* Stage 2: https://github.com/elastic/ecs/pull/1028
  * Stage 2 correction: https://github.com/elastic/ecs/pull/1158
* Stage 3: https://github.com/elastic/ecs/pull/1182
  * Stage 3 mark as finished: https://github.com/elastic/ecs/pull/1316

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
