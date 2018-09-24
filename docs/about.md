
# <a name="about-ecs"></a>FAQ

## What are the benefits of using ECS?

The benefits to a user adopting these fields and names in their clusters are:

* **Data correlation.** Ability to easily correlate data from the same or different sources, including:
    * data from metrics, logs, and apm
    * data from the same machines/hosts
    * data from the same service
* **Ease of recall.** Improved ability to remember commonly used field names (because there is a single set, not a set per data source)
* **Ease of deduction.** Improved ability to deduce field names (because the field naming follows a small number of rules with few exceptions)
* **Reuse.** Ability to re-use analysis content (searches, visualizations, dashboards, alerts, reports, and ML jobs) across multiple data sources
* **Future proofing.** Ability to use any future Elastic-provided analysis content in your environment without modifications

## What if I have fields that conflict with ECS?

The [rename processor](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/rename-processor.html) can help you resolve field conflicts. For example, imagine that you already have a field called "user," but ECS employs `user` as an object. You can use the rename processor on ingest time to rename your field to the matching ECS field. If your field does not match ECS, you can rename your field to `user.value` instead.

## What if my events have additional fields?

Events may contain fields in addition to ECS fields. These fields can follow the ECS naming and writing rules, but this is not a requirement.

## Why does ECS use a dot notation instead of an underline notation?

There are two common key formats for ingesting data into Elasticsearch:

* Dot notation: `user.firstname: Nicolas`, `user.lastname: Ruflin`
* Underline notation: `user_firstname: Nicolas`, `user_lastname: Ruflin`

For ECS we decided to use the dot notation. Here's some background on this decision.

### What is the difference between the two notations?

Ingesting `user.firstname: Nicolas` and `user.lastname: Ruflin` is identical to ingesting the following JSON:

```
"user": {
  "firstname": "Nicolas",
  "lastname": "Ruflin"
}
```

In Elasticsearch, `user` is represented as an [object datatype](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/object.html). In the case of the underline notation, both are just [string datatypes](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html).

NOTE: ECS does not use [nested datatypes](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html), which are arrays of objects.

### Advantages of dot notation

With dot notation, each prefix in Elasticsearch is an object. Each object can have [parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html#object-params) that control how fields inside the object are treated. In the context of ECS, for example, these parameters would allow you to disable dynamic property creation for certain prefixes.

Individual objects give you more flexibility on both the ingest and the event sides.  In Elasticsearch, for example, you can use the remove processor to drop complete objects instead of selecting each key inside. You don't have to know ahead of time which keys will be in an object.

In Beats, you can simplify the creation of events. For example, you can treat each object as an object (or struct in Golang), which makes constructing and modifying each part of the final event easier.

### Disadvantage of dot notation

In Elasticsearch, each key can only have one type. For example, if `user` is an `object`, you can't use it as a `keyword` type in the same index, like `{"user": "nicolas ruflin"}`. This restriction can be an issue in certain datasets. For the ECS data itself, this is not an issue because all fields are predefined.

### What if I already use the underline notation?

Mixing the underline notation with the ECS dot notation is not a problem. As long as there are no conflicts, they can coexist in the same document.
