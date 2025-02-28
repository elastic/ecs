# ECS & OpenTelemetry [ecs-opentelemetry]

In April 2023, Elastic donated ECS to OpenTelemetry and together with the OTel community [jointly announced](https://opentelemetry.io/blog/2023/ecs-otel-semconv-convergence/) the intention to achieve convergence of ECS and [OTel Semantic Conventions (SemConv)](https://opentelemetry.io/docs/specs/semconv/). This donation should be seen as a directional decision for the evolution of both standards rather than a single event that merged both schemas into a single standard.

While both schemes complement each other in large areas and thus offer mutual added value and great potential for convergence, it is important to understand that in some areas convergence is not achievable due to conceptual differences or consistency reasons. For example, while ECS contains a few fields (e.g. [container.disk.read.bytes](/reference/ecs-container.md#field-container-disk-read-bytes)) that are meant to be used in a metric-like way, metrics in OpenTelemetry are following a completely different data model (with metric name, type, dimensions, etc.). Also, in OTel semantic conventions there are some stable (or quasi-stable) attributes that have semantically equivalent, stable fields in ECS, however, with different field names. This kind of differences require explicit handling to achieve compatibility.


## Relation between ECS and Semantic Conventions [ecs-opentelemetry-relation]

The [ECS schema files](https://github.com/elastic/ecs/tree/main/schemas) contain an explicit mapping between ECS fields and corresponding OTel semnatic convention attributes. This can be used to generate tooling for compatibility between ECS and semnatic conventions (e.g. alias fields in Elasticsearch). The relation between individual ECS fields and corresponding OTel semantic conventions attributes follows one of the following categories:

| Category | Description |
| --- | --- |
| ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") | The name of the ECS field is identical to the SemConv attribute name and has (practically) the same semantics. |
| ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") | The ECS field name is different but has the same semantics as the corresponding SemConv attribute.For this type of relation aliasing approaches (e.g. [Elasticsearch field aliases](elasticsearch://reference/elasticsearch/mapping-reference/field-alias.md)) can be used to achieve compatibility between ECS and OTel SemConv. |
| ![relation](https://img.shields.io/badge/related-efc20d?style=flat "related") | The ECS field name is different and has related - yet different - semantics as the corresponding SemConv attribute.An aliasing approach is not sufficient to resolve compatibility for this type of relation. |
| ![relation](https://img.shields.io/badge/conflict-910000?style=flat "conflict") | The ECS field name is the same as an OTel SemConv namespace or an attribute that has significantly different semantics. |
| ![relation](https://img.shields.io/badge/OTLP-ffdcb2?style=flat "OTLP") | The ECS field has a corresponding representation in [OpenTelemetry’s protocol definition](https://github.com/open-telemetry/opentelemetry-proto). |
| ![relation](https://img.shields.io/badge/metric-cb00cb?style=flat "metric") | For this ECS field there is a corresponding metric defined in OTel SemConv. |
| ![relation](https://img.shields.io/badge/n%2Fa-f2f4fb?style=flat "na") | The ECS field is not applicable in the context of OTel or won’t be aligned due to significant, conceptual conflict with OTel concepts in that area. |

The following documentation pages provide an overview and more details on the alignment between ECS and OTel semantic conventions:

* [OTel Alignment Overview](/reference/ecs-otel-alignment-overview.md)
* [Field & Attributes Alignment](/reference/ecs-otel-alignment-details.md)



