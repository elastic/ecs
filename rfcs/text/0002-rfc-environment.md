# 0002: Environment Field
<!--^ The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC, taking care not to conflict with other RFCs.-->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage -->
- Date: **TBD** <!-- Update to reflect date of most recent stage advancement -->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

## Fields

This RFC calls for the addition in ECS of one field to describe the environment ("production", "staging", "qa"...) from which an event is emitted.

We propose to standardise the environment field already used by Elastic APM: `service.environment`.

No existing ECS field is impacted as no ECS field relates to this concept of "environment".

<!--
Stage: 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->

<!--
Stage 2: Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Fields (yaml)

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
  type: group
  fields:

    - name: environment
      level: extended
      type: keyword
      short: Environment on which the data is collected
      description: >
        Environment on which the data is collected

      example: production, qa, dev
```

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->




## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

`service.environment` will typically be used as a "static field" defined in the configuration of the collector (Filebeat, Metricbeat, APM, Auditbeat...).

Note that all the Beats come with an alternative non standard field example `fields.env` (see filebeat.yml, metricbeat.yml or auditbeat.yml) and APM use the variable `-Delastic.apm.environment`


### APM Agent

Use `-Delastic.apm.environment=staging` or `export ELASTIC_APM_ENVIRONMENT=staging`, see https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-environment

Note: we may want to adopt the official field name `-Delastic.apm.service_environment=staging`  and `export ELASTIC_APM_SERVICE_ENVIRONMENT=staging`.

```
java -javaagent:/path/to/elastic-apm-agent-<version>.jar \
     -Delastic.apm.service_name=my-application \
     -Delastic.apm.environment=staging \
     -Delastic.apm.server_urls=http://localhost:8200 \
     -Delastic.apm.secret_token= \
     -Delastic.apm.application_packages=org.example \
     -jar my-application.jar
```

### Filebeat.yml


Note: we may want to improve the configuration of Beats to not require to define a processor to specify `service.environment`, similarly to the existing solution to define `fields.*` fields.

```yaml
---
filebeat.inputs:
  - type: log
    enabled: true
    json.keys_under_root: true
    json.overwrite_keys: true
    paths:
      - /usr/local/var/log/my-shopping-cart/anti-fraud.log
processors:
  - add_fields:
      target: 'service'
      fields:
        environment: staging
```



## Source data

Observability: data produced by the infrastruture and application layers. Data types being logs, metrics, distributed traces and uptime monitors.
Security: security data should also benefit of specifying the `environment` from which they are emitted to offer filtering (SIEM...) on Elastic cluster spreading across multiple environments (e.g. "production" and "staging").


Logs are typically being collected by Filebeat, metrics are collected by Metricbeat, 
<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

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

 * Beats (Filebeat, Metricbeat, Heartbeat...) document in their configuration files (filebeat.yml...) an alternate non standardizable field `fields.env` illustrated with the demo value `staging`.

   Example with filebeat.yml

 ```yaml
# Optional fields that you can specify to add additional information to the
# output.
#fields:
#  env: staging
```

 * Using the namespace `service` for `service.environment` could sound awkward to some low level messages (e.g. system events). The rationale is
    * Reuse the naming `service.environment` already used by APM
    * Most events can eventually be attached to a `service`

 * This topic has already been discussed multiple times
    * https://github.com/elastic/ecs/issues/268 Add new top level field "environment" #268
    * https://github.com/elastic/ecs/issues/704 New field: organization.environment #704
    * https://github.com/elastic/ecs/issues/143 agent.environment and service.environment #143
 
<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

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

* Elastic APM is already using `service.environment`

```
java -javaagent:/path/to/elastic-apm-agent-<version>.jar \
     -Delastic.apm.service_name=my-application \
     -Delastic.apm.environment=staging \
     -Delastic.apm.server_urls=http://localhost:8200 \
     -Delastic.apm.secret_token= \
     -Delastic.apm.application_packages=org.example \
     -jar my-application.jar
```

* Sample filebeat.yml using an `add_fields` processor.

```yaml
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/my/file.log

setup.template.settings:
  index.number_of_shards: 0


output.elasticsearch:
  hosts: ["localhost:9200"]
  protocol: "http"
  username: "elastic"
  password: "elastic"

processors:
  - add_host_metadata: ~
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~
  - add_fields:
      target: 'service'
      fields:
        environment: staging

# Available log levels are: error, warning, info, debug
logging.level: info

```

## People


* @cyrille-leclerc | author
* ? | sponsor
* @roncohen | subject matter expert
* ? | grammar, spelling, prose
