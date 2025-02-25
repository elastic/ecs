---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-products-solutions.html
applies_to:
  stack: all
  serverless: all
---

# Products and solutions that support ECS [ecs-products-solutions]

The following Elastic products support ECS out of the box, as of version 7.0:

* [{{beats}}](beats://docs/reference/index.md)
* [APM](docs-content://solutions/observability/apps/application-performance-monitoring-apm.md)
* [Elastic Security](docs-content://solutions/security.md)

    * [Elastic Security Field Reference](docs-content://reference/security/fields-and-object-schemas/siem-field-reference.md) - a list of ECS fields used in the Security app

* [Elastic Endpoint Security Server](https://www.elastic.co/products/endpoint-security)
* [Log Monitoring](docs-content://solutions/observability/logs/explore-logs.md)
* Log formatters that support ECS out of the box for various languages can be found [here](https://github.com/elastic/ecs-logging/blob/master/README.md).
* [Metrics Monitoring](docs-content://solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md)
* {{ls}}' {{es}} output has an [ECS compatibility mode](logstash://docs/reference/plugins-outputs-elasticsearch.md#_compatibility_with_the_elastic_common_schema_ecs)

