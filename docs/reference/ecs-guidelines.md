---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-guidelines.html
---

# Guidelines and best practices [ecs-guidelines]

The ECS schema serves best when you follow schema guidelines and best practices.


## ECS field levels [_ecs_field_levels]

ECS defines "Core" and "Extended" fields.

* **Core fields.** Fields that are most common across all use cases are defined as **core fields**.

    These generalized fields are used by analysis content (searches, visualizations, dashboards, alerts, machine learning jobs, reports) across use cases. Analysis content designed to operate on these fields should work properly on data from any relevant source.

    Focus on populating these fields first.

* **Extended fields.** Any field that is not a core field is defined as an **extended field**. Extended fields may apply to more narrow use cases, or may be more open to interpretation depending on the use case. Extended fields are more likely to change over time.

Each ECS [field](/reference/ecs-field-reference.md) in a table is identified as core or extended.


## General guidelines [_general_guidelines]

* The document MUST have the `@timestamp` field.
* Use the [data types](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) defined for an ECS field.
* Use the `ecs.version` field to define which version of ECS is used.
* Map as many fields as possible to ECS.


### Guidelines for field names [_guidelines_for_field_names]

* **Field names must be lower case**
* **Combine words using underscore**
* **No special characters except underscore**
* **Use present tense** unless field describes historical information.
* **Use singular and plural names properly** to reflect the field content.

    * For example, use `requests_per_sec` rather than `request_per_sec`.

* **Use prefixes for all fields**, except for the base fields.

    * For example, all `host` fields are prefixed with `host.`. Such a grouping is called a field set.

* **Nest fields inside a field set** with dots

    * The document structure should be nested JSON objects. If you use Beats or Logstash, the nesting of JSON objects is done for you automatically. If you’re ingesting to Elasticsearch using the API, your fields must be nested objects, not strings containing dots.
    * See [Why does ECS use a dot notation instead of an underline notation?](/reference/ecs-faq.md#dot-notation) for more details.

* **General to specific**. Organise the nesting of field sets from general to specific, to allow grouping fields into objects with a prefix like `host.*`.
* **Avoid repetition** or stuttering of words

    * If part of the field name is already in the name of the field set, avoid repeating it. Example: `host.host_ip` should be `host.ip`.
    * Exceptions can be made, when changing the name of the field would break a strong convention in the community. Example: `host.hostname` is an exception to this rule.

* **Avoid abbreviations when possible**

    * Exceptions can be made, when the name used for the concept is too strongly in favor of the abbreviation. Example: `ip` fields, or field sets such as `os`, `geo`.
