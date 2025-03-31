---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-faq.html
applies_to:
  stack: all
  serverless: all
---

# Questions and answers [ecs-faq]


## What are the benefits of using ECS? [ecs-benefits]

The benefits to a user adopting these fields and names in their clusters are:

* **Data correlation.** Ability to easily correlate data from the same or different sources, including:

    * data from metrics, logs, and application performance management (apm) tools
    * data from the same machines/hosts
    * data from the same service

* **Ease of recall.** Improved ability to remember commonly used field names (because there is a single set, not a set per data source)
* **Ease of deduction.** Improved ability to deduce field names (because the field naming follows a small number of rules with few exceptions)
* **Reuse.** Ability to re-use analysis content (searches, visualizations, dashboards, alerts, reports, and machine learning jobs) across multiple data sources
* **Future proofing.** Ability to use any future Elastic-provided analysis content in your environment without modifications


## What if I have fields that conflict with ECS? [conflict]

The [rename processor](elasticsearch://reference/enrich-processor/rename-processor.md) can help you resolve field conflicts. For example, imagine that you already have a field called "user," but ECS employs `user` as an object. You can use the rename processor on ingest time to rename your field to the matching ECS field. If your field does not match ECS, you can rename your field to `user.value` instead.


## What if my events have additional fields? [addl-fields]

Events may contain fields in addition to ECS fields. These fields can follow the ECS naming and writing rules, but this is not a requirement.


## Why does ECS use a dot notation instead of an underline notation? [dot-notation]

There are two common key formats for ingesting data into Elasticsearch:

* Dot notation: `user.firstname: Nicolas`, `user.lastname: Ruflin`
* Underline notation: `user_firstname: Nicolas`, `user_lastname: Ruflin`

ECS uses the dot notation to represent nested objects.


### What is the difference between the two notations? [notation-diff]

Ingesting `user.firstname: Nicolas` and `user.lastname: Ruflin` is identical to ingesting the following JSON:

```json
    "user": {
      "firstname": "Nicolas",
      "lastname": "Ruflin"
    }
```

In Elasticsearch, `user` is represented as an [object datatype](elasticsearch://reference/elasticsearch/mapping-reference/object.md). In the case of the underline notation, both are just [string datatypes](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md).


### Advantages of dot notation [dot-adv]

With dot notation, each prefix in Elasticsearch is an object. Each object can have [parameters](elasticsearch://reference/elasticsearch/mapping-reference/object.md#object-params) that control how fields inside the object are treated. In the context of ECS, for example, these parameters would allow you to disable dynamic property creation for certain prefixes.

Individual objects give you more flexibility on both the ingest and the event sides. In Elasticsearch, for example, you can use the remove processor to drop complete objects instead of selecting each key inside. You don’t have to know ahead of time which keys will be in an object.

In Beats, you can simplify the creation of events. For example, you can treat each object as an object (or struct in Golang), which makes constructing and modifying each part of the final event easier.


### Disadvantage of dot notation [dot-disadv]

In Elasticsearch, each key can have only one type. For example, if `user` is an `object`, you can’t use it as a `keyword` type in the same index, like `{"user": "nicolas ruflin"}`. This restriction can be an issue in certain datasets. For the ECS data itself, this is not an issue because all fields are predefined.


### What if I already use the underline notation? [underline]

As long as there are no conflicts, underline notation and ECS dot notation can coexist in the same document.


## What if I want to use a different data type from the same field type family? [type-interop]

In Elasticsearch, field types are grouped by family. Types in the same family support the same search functionality but may have different space usage or performance characteristics. For example, both `keyword` and `wildcard` types are members of the `keyword` family, and `text` and `match_only_text` are members of the `text` family.

The field types defined in ECS provide the best default experience for most users. However, a different type from the same family can replace the default defined in ECS if required for a specific use cases. Users should understand any potential performance or storage differences before changing from a default field type.

The Elasticsearch [mapping types](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md) section has more information about type families.
