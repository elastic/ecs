
# <a name="about-ecs"></a>About ECS

## Scope

The Elastic Common Schema defines a common set of document fields (and their respective field names) to be used in event messages stored in Elasticsearch as part of any logging or metrics use case of the Elastic Stack, including IT operations analytics and security analytics.

## Goals

The ECS has the following goals:

* Correlate data between metrics, logs and APM
* Correlate data coming from the same machines / hosts
* Correlate data coming from the same service

Priority on which fields are added is based on these goals.


## Benefits

The benefits to a user adopting these fields and names in their clusters are:

- Ability to simply correlate data from different data sources
- Improved ability to remember commonly used field names (since there is only a single set, not a set per data source)
- Improved ability to deduce unremembered field names (since the field naming follows a small number of rules with few exceptions)
- Ability to re-use analysis content (searches, visualizations, dashboards, alerts, reports, and ML jobs) across multiple data sources
- Ability to use any future Elastic-provided analysis content in their environment without modifications


## FAQ

### Why is ECS using a dot nation instead of an underline notation?

There are two common formats on how keys are formatted when ingesting data into Elasticsearch:

* Dot notation: `user.firstname: Nicolas`, `user.lastname: Ruflin`
* Underline notation: `user_firstname: Nicolas`, `user_lastname: Ruflin`

In ECS the decision was made to use the dot notation and this entry is intended to share some background on this decision.

**What is the difference between the two notations?**

When ingesting `user.firstname` and `user.lastname` it is identical to ingesting the following JSON:

```
"user": {
  "firstname": "Nicolas",
  "lastname": "Ruflin"
}
```

This means internally in Elasticsearch `user` is represented as an [object datatype](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/object.html). In the case of the underline notation both are just [string datatypes](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html).

NOTE: ECS does not used [nested datatypes](https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html) which is an array of objects.

**Advantages of dot notation**

The advantage of the dot notation is that on the Elasticsearch side each prefix is an object. Each object can have [parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/object.html#object-params) on how fields inside the object should be treated, for example if they should be index or mappings should be extended. In the context of ECS this allows for example to disable dynamic property creation for certain prefixes.

On the ingest side of Elasticsearch it makes it simpler to for example drop complete objects with the remove processor instead of selecting each key inside it. It does not require prior knowledge which keys will end up in the object.

On the event producing side like in Beats it simplifies the creation of the events as on the code side each object can be treated as an object (or struct in Golang as an example) which makes constructing and modifying each part of the final event easier.

**Disadvantage of dot notation**

In Elasticsearch each key can only have one type. So if `user` is an object it's not possible to have in the same index `user` as type `keyword` like `{"user": "nicolas ruflin"}`. This can be an issue in certain datasets.

For the ECS data itself this is not an issue as all fields are predefined.

**What if I already use the underline notation?**

It's not a problem to mix the underline notation with the ECS do notation. They can coexist in the same document as long as there are not conflicts.

**I have conflicting fields with ECS?**

Assuming you already have a field user but ECS uses `user` as an object, you can use the [rename processor](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/rename-processor.html) on ingest time to rename your field to either the matching ECS field or rename it to `user.value` instead if your field does not match ECS.
