# 0039: TSDB Dimensions
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2023-04-11** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

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

This RFC proposes the annotating of certain ecs fields as `dimension`. This change is proposed to take the advantage of using `TSDB` offered by the elasticsearch without impacting the data injection.

Annotating field as `dimension` is one of the important step in the process of TSDB adoption. Failing to annotate adequate number of fields as `dimension` when `TSDB` is enabled may lead to data loss. A large majority of fields that must be annotated as `dimension` fields are ecs fields. Presently, the Integration (Service Integration, Cloud Native, etc ) developers are expected to annotate ecs fields as `dimensions` in integration configuration. To avoid the duplicatation in configuration, minimize data loss probability, the RFC is proposed. `dimension` field takes two values - `true` and `false`.


Changes to :service mapping

```yaml
---
- name: service
  title: Service
  group: 2
  short: Fields describing the service for or from which the data was collected.
  description: >
    The service fields describe the service for or from which the data was collected.

    These fields help you find and correlate logs for a specific
    service and version.
  footnote: >
    The service fields may be self-nested under service.origin.* and service.target.*
    to describe origin or target services in the context of incoming or outgoing requests,
    respectively.
    However, the fieldsets service.origin.* and service.target.* must not be confused with
    the root service fieldset that is used to describe the actual service under observation.
    The fieldset service.origin.* may only be used in the context of incoming requests or
    events to describe the originating service of the request. The fieldset service.target.*
    may only be used in the context of outgoing requests or events to describe the target
    service of the request.
  reusable:
    top_level: true
    expected:
      - at: service
        as: origin
        beta: Reusing the `service` fields in this location is currently considered beta.
        short_override: Describes the origin service in case of an incoming request or event.
      - at: service
        as: target
        beta: Reusing the `service` fields in this location is currently considered beta.
        short_override: Describes the target service in case of an outgoing request or event.
  type: group
  fields:

    - name: address
      level: extended
      type: keyword
      dimension: true
      short: Address of this service.
      description: >
        Address where data about this service was collected from.

        This should be a URI, network address (ipv4:port or [ipv6]:port) or a resource path (sockets).
      example: 172.26.0.2:5432

```
Changes to host mapping

```yaml
---
- name: host
  title: Host
  group: 2
  short: Fields describing the relevant computing instance.
  description: >
    A host is defined as a general computing instance.

    ECS host.* fields should be populated with details about the host on which
    the event happened, or from which the measurement was taken.
    Host types include hardware, virtual machines, Docker containers, and Kubernetes nodes.
  type: group
  fields:
    - name: name
      level: core
      type: keyword
      dimension: true
      short: Name of the host.
      description: >
        Name of the host.
        It can contain what hostname returns on Unix systems, the fully
        qualified domain name (FQDN), or a name specified by the user.
        The recommended value is the lowercase FQDN of the host.

```
Changes to agent mapping

```yaml
---
- name: agent
  title: Agent
  group: 2
  short: Fields about the monitoring agent.
  description: >
    The agent fields contain the data about the software entity, if any, that collects, detects, or observes events on a host, or takes measurements on a host.

    Examples include Beats. Agents may also run on observers. ECS agent.* fields shall be populated with details of the agent running on the host or observer where the event happened or the measurement was taken.
  footnote: >
    Examples: In the case of Beats for logs, the agent.name is filebeat. For APM, it is the
    agent running in the app/service. The agent information does not change if
    data is sent through queuing systems like Kafka, Redis, or processing systems
    such as Logstash or APM Server.
  type: group
  fields:

    - name: id
      level: core
      type: keyword
      dimension: true
      short: Unique identifier of this agent.
      description: >
        Unique identifier of this agent (if one exists).

        Example: For Beats this would be beat.id.
      example: 8a4f500d
```

Changes to cloud mapping

```yaml
---
- name: cloud
  title: Cloud
  group: 2
  short: Fields about the cloud resource.
  description: >
    Fields related to the cloud or infrastructure the events
    are coming from.
  footnote: >
    Examples: If Metricbeat is running on an EC2 host and fetches data from its
    host, the cloud info contains the data about this machine. If Metricbeat
    runs on a remote machine outside the cloud and fetches data from a service
    running in the cloud, the field contains cloud data from the machine the
    service is running on.
    The cloud fields may be self-nested under cloud.origin.* and cloud.target.*
    to describe origin or target service's cloud information in the context of
    incoming or outgoing requests, respectively. However, the fieldsets
    cloud.origin.* and cloud.target.* must not be confused with the root cloud
    fieldset that is used to describe the cloud context of the actual service
    under observation. The fieldset cloud.origin.* may only be used in the
    context of incoming requests or events to provide the originating service's
    cloud information. The fieldset cloud.target.* may only be used in the
    context of outgoing requests or events to describe the target service's
    cloud information.
  reusable:
    top_level: true
    expected:
      - at: cloud
        as: origin
        beta: Reusing the `cloud` fields in this location is currently considered beta.
        short_override: Provides the cloud information of the origin entity in case of an incoming request or event.
      - at: cloud
        as: target
        beta: Reusing the `cloud` fields in this location is currently considered beta.
        short_override: Provides the cloud information of the target entity in case of an outgoing request or event.
  type: group
  fields:
    - name: project.id
      level: extended
      type: keyword
      dimension: true
      example: my-project
      short: The cloud project id.
      description: >
        The cloud project identifier.
        Examples: Google Cloud Project id, Azure Project id.


    - name: instance.id
      level: extended
      type: keyword
      dimension: true
      example: i-1234567890abcdef0
      description: >
        Instance ID of the host machine.

    - name: provider
      level: extended
      example: aws
      type: keyword
      dimension: true
      short: Name of the cloud provider.
      description: >
        Name of the cloud provider. Example values are aws, azure, gcp, or
        digitalocean.
```

Changes to container mapping

```yaml
---
- name: container
  title: Container
  group: 2
  short: Fields describing the container that generated this event.
  description: >
    Container fields are used for meta information about the specific container
    that is the source of information.
    These fields help correlate data based containers from any runtime.
  type: group
  fields:
    - name: id
      level: core
      type: keyword
      dimension: true
      description: >
        Unique container id.
```
<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

Integration package development is the key beneficiary of this change. The fields of the document that are received from an integration receives a field mapping. If and when TSDB benefits are to be utilised, along with the field mapping with a metric type, at least one of the fields  must receive `dimension: true` annotation.

Example of field mapping in integrations with the field enabled as a dimension field.
```yaml
---
- name: wait_class
  type: keyword
  dimension: true
  description: Every wait event belongs to a class of wait event.

```
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

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

## Concerns

No concerns are known as of now. Presence of the `dimension:true` does not impact functionality. Elastic Stack version 8.7 is essential for this.
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

* @agithomas | author
* @ruflin | subject matter expert
* @lalit-satapathy | reviewer
* @martijnvg | reviewer
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

* [TSDB Design Document](https://github.com/elastic/elasticsearch-adrs/blob/master/analytics/tsdb/tsdb-design.md)
* [Oracle Package Pull Request for TSDB Migraiton](https://github.com/elastic/integrations/pull/4966)

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/2172

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
