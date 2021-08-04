# 0025: Container Metric Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1 (draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-07-29** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

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

This RFC proposes 6 additional container metric fields into ECS for monitoring
container CPU, memory, disk and network performance:
- container.cpu.usage
- container.memory.usage
- container.network.ingress.bytes
- container.network.egress.bytes
- container.disk.read.bytes
- container.disk.write.bytes

With existing metadata fields `container.id`, `container.image.name`, `container.image.tag`,
`container.labels`, `container.name` and `container.runtime`, these total 12
fields will become the common field schema for container metrics. These metric
fields and metadata fields are recommended or required for all events related to
containers.

## Fields

This RFC calls for the addition of metric fields to collect basic monitoring
metrics from a container such as CPU, memory, network and disk.
Please see [`container.yml`](0000/container.yml) for definitions of all fields.

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

Container metric fields and container metadata fields can be collected from
several sources. For example, a user who uses both Docker, Cloudfoundry
and AWS Fargate would like to collect data regarding all containers and store
them in a centralized location. Without these new container metric fields,
Metricbeat is reporting container metrics under different names from different
sources. For example, for CPU usage, `docker.cpu.total.pct` is used. For
Cloudfoundry, `cloudfoundry.container.cpu.pct` is used and for AWS Fargate,
`awsfargate.task_stats.cpu.total.pct` is used.
With these different field names, Kibana Docker containers metrics UI can only
display data collected from Docker but no other sources.

With the additional container metric fields proposed here, users should be able
to see the same metric field collected from different sources and Kibana should
be able to display all containers, not only from Docker, but also Cloudfoundry,
AWS Fargate and etc.

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

- Docker
- Kubernetes
- AWS Fargate
- Cloudfoundry
- Google GKE

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

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

We need to carefully define each field because when collecting these container
metrics from different sources, the scope of these metrics change. We should
make sure when users are using these metrics, they are all collected to represent
the same thing. For example, `container.cpu.usage` needs to be a normalized value
between 0 and 1.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @kaiyan-sheng | author
* @cyrille-leclerc | sponsor
* @jsoriano | subject matter expert

<!--
Who will be or has been consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

Common Fields for Container Inventory Schema: https://github.com/elastic/beats/issues/22179

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1441
    * Stage 0 date correction: https://github.com/elastic/ecs/pull/1447

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
* Stage 1: https://github.com/elastic/ecs/pull/1529
