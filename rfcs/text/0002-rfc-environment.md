# 0002: Service Environment Field
<!--^ The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC, taking care not to conflict with other RFCs.-->

- Stage: **2 (candidate)** <!-- Update to reflect target stage -->
- Date: **2021-07-28** <!-- Update to reflect date of most recent stage advancement -->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

## Fields

<!--
Stage: 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->

This RFC calls for the addition in ECS of one field to describe the environment ("production", "staging", "qa"...) from which an event of a component of the application layer (service, application or function) is emitted.

We propose to standardise the environment field to qualify a service using the field already used by Elastic APM: `service.environment`.

No existing ECS field is impacted as no ECS field relates to this concept of "environment".

The `service.environment` field will supplement the existing fields of the [`service.*` namespace](https://www.elastic.co/guide/en/ecs/master/ecs-service.html) such as `service.name` and `service.version`.

<!--
Stage 2: Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Fields (yaml)

```
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

      example: production, staging, qa, or dev
```

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

`service.environment` will typically be used as a "static attribute" primarily defined in the APM agent and synthetics agent (ie Heartbeat) configuration. There are also use cases where the `service.environment` will be defined in Filebeat and Metricbeat collectors.


### Usage with APM agents

To define `service.environment` on APM agent configurations, we use `-Delastic.apm.environment=staging` or `export ELASTIC_APM_ENVIRONMENT=staging`, see https://www.elastic.co/guide/en/apm/agent/java/current/config-core.html#config-environment

Example

```
java -javaagent:/path/to/elastic-apm-agent-<version>.jar \
     -Delastic.apm.service_name=www-frontend \
     -Delastic.apm.environment=production \
     -Delastic.apm.server_urls=https://apm-server.my-ecommerce.com:8200 \
     -Delastic.apm.secret_token= \
     -Delastic.apm.application_packages=com.myecommerce \
     -jar www-frontend.jar
```


Note: we may want to evolve the Java system property (`-Delastic.apm.environment`) and the environment variable (`ELASTIC_APM_ENVIRONMENT`) to better reflect the ECS field name, it could look like `-Delastic.apm.service_environment` and `ELASTIC_APM_SERVICE_ENVIRONMENT`.

### Usage with Heartbeat

Synthetics tests are the second major use case to qualify the environment of a service.
An important difference with APM agents is that an Heartbeat agent is likely to simultenaously run synthetics tests on multiple services spread across multiple environments. The qualification of the `service.name`and `service.environment` are defined per `heartbeat.monitor` rather than globally.

The configuration could look like:

```yaml
# EXPERIMENT - NOT SUPPORTED CONFIGURATION SNIPPET
heartbeat.monitors:
- type: http
  id: www-frontend-monitor
  name: Website Frontend Monitor
  service:
    name: www-frontend
    environment: production
  urls: ["https://www.my-ecommerce-company.com/status"]
  schedule: '@every 10s'
  check.response.status: 200
  timeout: 2s
- type: http
  id: www-frontend-monitor-staging
  name: Website Frontend Monitor - Staging
  service:
    name: www-frontend
    environment: staging
  urls: ["https://www.staging.my-ecommerce-company.com/status"]
  schedule: '@every 10s'
  check.response.status: 200
  timeout: 5s
```

Note the support in Heartbeat of `service.name` is waiting for https://github.com/elastic/beats/pull/20330

### Usage with Filebeat and Metricbeat

Note that all the Beats come with a different example field to define the environment: `fields.env` (see filebeat.yml, metricbeat.yml, auditbeat.yml or heartbeat.yml).
This `fields.env` field is misaligned with this desire of standardisation because it cannot be standardised in ECS due to the following ECS rules:
* The namespace `fields.*` is not accepted in ECS, this namespace is dedicated to non standardised fields.
* ECS don't use abbreviations and `env` is the abbreviation of `environment`.

Note that the `fields.env` field is just an example and it not likely to be used very broadly because for infrastructure elements such as servers, the delineation between environments is often difficult to establish as servers are frequently simulatenaously running production and non production workloads.

We propose to tackle later the questions of
* Standardisating the characterization of the environment for infrastructure later.
* Specifying the `service.environment` and service.name for service/application related
   * Log files collected by filebeat: application log file collected on disk...
   * Metrics collected by metricbeat: application metrics collected via Prometheus, Jolokia, JMX...
For the metricbeat and filebeat problems described above, the solution used by Heartbeat HTTP monitors (see above) is an interesting path forward.

## Source data

Observability: data produced by the infrastruture and application layers. Data types being logs, metrics, distributed traces and uptime monitors.
Security: security data should also benefit of specifying the `environment` from which they are emitted to offer filtering (SIEM...) on Elastic cluster spreading across multiple environments (e.g. "production" and "staging").

Note: sample json documents are stored on https://gist.github.com/cyrille-leclerc/81deca4852df7754246b70d4a01bb9b0

### Sample APM Transaction JSON document

Sample of APM Transaction using `service.name` and `service.environment`

```
{
  "_index": "apm-7.10.0-transaction-000001",
  "_type": "_doc",
  "_id": "8tlyD3YBKOouY3Ui1sED",
  "_version": 1,
  "_score": null,
  "_source": {
    ...
    "service": {
      "node": {
        "name": "cyrillerclaptop.localdomain"
      },
      "environment": "staging",
      "framework": {
        "name": "Spring Web MVC",
        "version": "5.3.1"
      },
      "name": "frontend",
      "runtime": {
        "name": "Java",
        "version": "15"
      },
      "language": {
        "name": "Java",
        "version": "15"
      },
      "version": "1.0-SNAPSHOT"
    },
    ...
  }
  ```

### Sample Heartbeat HTTP Monitor Check JSON document

`service.environment` would be added next to `service.name`.

```
{
  "_index": "heartbeat-7.10.0-2020.11.24-000001",
  "_type": "_doc",
  "_id": "J9uAD3YBKOouY3UiDwhY",
  "_version": 1,
  "_score": null,
  "_source": {
    "@timestamp": "2020-11-28T15:36:58.475Z",
    "monitor": {
      "check_group": "8a44a150-318f-11eb-a924-acde48001122",
      "ip": "127.0.0.1",
      "status": "up",
      "duration": {
        "us": 2156
      },
      "id": "frontend-check",
      "name": "Frontend",
      "type": "http",
      ...
    },
    "url": {
      "domain": "localhost",
      "port": 8080,
      "path": "/actuator/health",
      "full": "http://localhost:8080/actuator/health",
      "scheme": "http"
    },
    "service": {
      "name": "frontend"
      // `service.environment` would be added here
    },
    ...
  }
}
```
### Sample Filebeat JSON document generated via the logback-ecs-encoder library

`service.environment` would be added next to `service.name`

```
{
  "_index": "filebeat-7.10.0-2020.11.24-000001",
  "_type": "_doc",
  "_id": "2duDD3YBKOouY3UiPCLK",
  "_version": 1,
  "_score": null,
  "_source": {
    "@timestamp": "2020-11-28T15:40:26.178Z",
    "event.dataset": "frontend.log",
    "service.name": "frontend", // `service.environment` would be added here
    "trace.id": "080e218993ca8b2916d8cc9bc9b38bc3",
    "message": "SUCCESS createOrder([OrderController.OrderForm@55b8d300list[[OrderProductDto@39448661 product = [Product@29587cf7 id = 4, name = 'Icecream', price = 5.0], quantity = 1]]]): price: 5.0, id:2509373",
    "input": {
      "type": "log"
    },
    "log.logger": "com.mycompany.ecommerce.controller.OrderController",
    "log.level": "INFO",
    "process.thread.name": "http-nio-8080-exec-3",
    ...
}
```

### Sample Metricbeat JSON Document collected for a Prometheus metric

`service.environment` would be added next to `service.type` and `service.address`, we would also add `service.name`


```
{
  "_index": "metricbeat-7.10.0-2020.11.24-000001",
  "_type": "_doc",
  "_id": "vNuID3YBKOouY3UivU-d",
  "_version": 1,
  "_score": null,
  "_source": {
    "@timestamp": "2020-11-28T15:46:24.391Z",
    "metricset": {
      "name": "collector",
      "period": 10000
    },
    "service": {
      // `service.environment` would be added here. We would also add `service.name`
      "address": "http://localhost:8080/actuator/prometheus",
      "type": "prometheus"
    },
    "fields": {
      "env": "staging"
    },
    "agent": {
      "type": "metricbeat",
      "version": "7.10.0",
      "hostname": "cyrillerclaptop.localdomain",
      "ephemeral_id": "d4d682a8-6944-42cb-9273-87e07b620643",
      "id": "4acf759f-74b0-4198-80e2-94f705511512",
      "name": "cyrillerclaptop.localdomain"
    },
    "ecs": {
      "version": "1.6.0"
    },

    "prometheus": {
      "order_per_country": {
        "histogram": {
          "values": [],
          "counts": []
        }
      },
      "labels": {
        "quantile": "0.75",
        "instance": "localhost:8080",
        "job": "prometheus",
        "shipping_country": "US"
      }
    },
    ...
  },
  ...
}
````

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

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

### Alternative field name proposed in Beats (Filebeat, Metricbeat, Heartbeat...)

Beats (Filebeat, Metricbeat, Heartbeat...) document in their configuration files (filebeat.yml, metricbeat.yml...) with an alternative field to characterize environments: `fields.env`.

 Example with filebeat.yml

 ```
# Optional fields that you can specify to add additional information to the
# output.
#fields:
#  env: staging
```

### "Service" namespace not suited to characterise infrastructure component

Using the namespace `service` for `service.environment` could sound awkward to some low level messages (e.g. system events). The rationale is that `service.environment` will only be used to qualify components of the application layer (ie services, application, function) but will not be used to qualify the environment of an infrastructure component (server, virtual machine...).

Note that the `environment` field is a good candidate to be reused in other namespace than the `service.*` to cover the Infrastructure use cases.

### Different standardisation chosen by OpenTelemetry

OpenTelemetry has standardized `deployment.environment`, referring to [Wikipedia: Deployment Environment](https://en.wikipedia.org/wiki/Deployment_environment). The benefit of `deployment.environment` is that it works better for the characterization of the infrastructure (e.g. physical server, vm): https://github.com/open-telemetry/opentelemetry-specification/blob/master/specification/resource/semantic_conventions/deployment_environment.md


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

* @cyrille-leclerc | co-author
* @eyalkoren | co-author
* @exekias | sponsor
* @sqren | subject matter expert

## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/891
* Stage 1: https://github.com/elastic/ecs/pull/1070
  * Update stage 1 naming: https://github.com/elastic/ecs/pull/1240
* Stage 2: https://github.com/elastic/ecs/pull/1536
