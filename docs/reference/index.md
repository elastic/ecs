---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-reference.html
  - https://www.elastic.co/guide/en/ecs/current/index.html
---

# ECS reference [ecs-reference]

This is the documentation of ECS version 9.1.0-dev.


## What is ECS? [_what_is_ecs]

The Elastic Common Schema (ECS) is an open source specification, developed with support from the Elastic user community. ECS defines a common set of fields to be used when storing event data in Elasticsearch, such as logs and metrics.

ECS specifies field names and Elasticsearch datatypes for each field, and provides descriptions and example usage. ECS also groups fields into ECS levels, which are used to signal how much a field is expected to be present. You can learn more about ECS levels in [Guidelines and Best Practices](/reference/ecs-guidelines.md). Finally, ECS also provides a set of naming guidelines for adding custom fields.

The goal of ECS is to enable and encourage users of Elasticsearch to normalize their event data, so that they can better analyze, visualize, and correlate the data represented in their events. ECS has been scoped to accommodate a wide variety of events, spanning:

* **Event sources**: whether the source of your event is an Elastic product, a third- party product, or a custom application built by your organization.
* **Ingestion architectures**: whether the ingestion path for your events includes Beats processors, Logstash, Elasticsearch ingest node, all of the above, or none of the above.
* **Consumers**: whether consumed by API, Kibana queries, dashboards, apps, or other means.


## New to ECS? [_new_to_ecs]

If you’re new to ECS and looking for an introduction to its benefits and examples of the core concepts, [Getting Started](/reference/ecs-getting-started.md) is a great place to start.


## My events don’t map with ECS [_my_events_dont_map_with_ecs]

ECS is a permissive schema. If your events have additional data that cannot be mapped to ECS, you can simply add them to your events, using custom field names.


## Maturity [_maturity]

ECS improvements are released following [Semantic Versioning](https://semver.org/). Major ECS releases are planned to be aligned with major Elastic Stack releases.

Any feedback on the general structure, missing fields, or existing fields is appreciated. For contributions please read the [Contribution Guidelines](https://github.com/elastic/ecs/blob/master/CONTRIBUTING.md).

