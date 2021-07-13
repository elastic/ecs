# 0009: Data stream fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (candidate)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-04-19** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

When introducing the new indexing strategy for Elastic Agent which uses data streams, we found that adding a few [constant_keyword](https://www.elastic.co/guide/en/elasticsearch/reference/master/keyword.html#constant-keyword-field-type) fields corresponding to the central components in the new indexing strategy would be advantageous.


<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->

This RFC proposes to introduce a new fieldset called "data_stream". The fieldset consists of the following fields:
Field     | Mapping type | Description
----------|--------------|--------------
data_stream.type | constant_keyword | An overarching type for the data stream. Currently allowed values include "logs", "metrics". We expect to also add "traces" and "synthetics" in the near future
data_stream.dataset | constant_keyword | The field can contain anything that makes sense to signify the source of the data. Examples include `nginx.access`, `prometheus`, `endpoint` etc. For data streams that otherwise fit, but that do not have dataset set we use the value "generic" for the dataset value. `event.dataset` should have the same value as `data_stream.dataset`.
data_stream.namespace | constant_keyword | A user defined namespace. Namespaces are useful to allow grouping of data. Many of our customers already organize their indices this way, and now we are providing this best practice as a default. Many people will use `default` as the value.

In the new indexing strategy, the value of the data stream fields combine to the name of the actual data stream in the following manner `{data_stream.type}-{data_stream.dataset}-{data_stream.namespace}`. This means the fields can only contain characters that are valid as part of names of data streams.

The fields can be found in `rfcs/text/0009/data_stream.yml`.

### Restrictions on values

Due to the fact that the values of the `data_stream` fields make up the data stream name, the restrictions on data stream names also apply to values for the `data_stream` fields. As an example, they cannot include `\`, `/`, `*`, `?`, `"`, `<`, `>`, `|`, ` `, `,`, `#`. Please see the Elasticsearch reference for [restrictions on index/data stream names](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html#indices-create-api-path-params). Here follows the _additional_ restrictions imposed on the data stream fields:

**data_stream.type**

`data_stream.type` is restricted to `logs` or `metrics` for now.

Any future values for `data_stream.type` should also adhere to the following restrictions (these are derived from the Elasticsearch index restrictions):
* Must not contain `-`
* Must not start with `+` or `_`

**data_stream.dataset**

* Must not contain `-`
* No longer than 100 chars

**data_stream.namespace**

* No longer than 100 chars


### On the use of Constant Keyword fields

The new indexing strategy results in users having many more indices than they used to. Elasticsearch is very good at searching for specific documents across indices, but for some common queries we can make it even better by using `constant_keyword` fields. For example, it's often the case that you'd want to find only documents that contain logs from a certain service or logs from a given namespace. For a query such as `data_stream.type: logs AND data_stream.namespace: billing-app` Elasticsearch can quickly determine that only a small subset of the indices are relevant to search through.
<!--
Stage 2: Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

Data stream fields are already in use in Elastic Agent. Leveraging the data stream fields described here allow users to filter by a specific data type (logs, metrics etc.), dataset (nginx.access, prometheus) or namespace. The following are examples of common queries pertaining to specific datatypes, datasets or namespaces:

* `data_stream.type: logs`
* `data_stream.dataset: nginx.access`
* `data_stream.type: logs AND data_stream.namespace: web-frontend`

As previously described, fields mapped as `constant_keyword` allows Elasticsearch to drastically optimize queries involving those fields. See the [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/faster-filtering-with-constant-keyword.html) on `constant_keyword` for more information.


## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

Today, Elastic Agent adds the data_stream fields in all documents ingested. It's also possible to use the fields in data from other data sources. Elasticsearch 7.9+ ships with built-in index template mappings which will ensure that documents indexed into data streams that match `logs-*-*` and `metrics-*-*` will get the fields mapped correctly to `constant_keyword` types.

Here are two example events, one for logs, one for metrics. It must be noted that for better readability some of the fields were removed.

Example source document of type metrics:

```
{
  "@timestamp": "2020-12-23T10:10:45.704Z",
  "event": {
    "dataset": "system.process_summary",
    "module": "system",
    "duration": 34693020
  },
  "service": {
    "type": "system"
  },
  "system": {
    "process": {
      "summary": {
        "dead": 0,
        "total": 236,
        "sleeping": 49,
        "running": 0,
        "idle": 95,
        "stopped": 0,
        "zombie": 0,
        "unknown": 92
      }
    }
  },
  "data_stream": {
    "dataset": "system.process_summary",
    "namespace": "default",
    "type": "metrics"
  }
}
```

Example source document of type logs:

```
{
  "@timestamp": "2020-12-23T10:17:35.902Z",
  "log.level": "debug",
  "log.logger": "processors",
  "log.origin": {
    "file.name": "processing/processors.go",
    "file.line": 203
  },
  "message": "Hello world ECS",
  "input": {
    "type": "log"
  },
  "event": {
    "dataset": "elastic_agent.metricbeat"
  },
  "log": {
    "file": {
      "path": "/opt/Elastic/Agent/data/elastic-agent-1da173/logs/default/metricbeat-json.log"
    },
    "offset": 685026
  },
  "data_stream": {
    "dataset": "elastic_agent.metricbeat",
    "namespace": "default",
    "type": "logs"
  }
}
```

### Using data_stream fields with regular indices
`data_stream` fields only make sense when indexing into data streams. They should not to be used for regular indices.


<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

* We've described that `generic` is a valid value for `data_stream.dataset` in some cases. Since `event.dataset` should always have the same value, this will also apply to `event.dataset`. We should update the documentation on `event.dataset` to reflect this.
* Since `data_stream.dataset` and `event.dataset` should contain the same value, the restrictions imposed on `data_stream.dataset` might affect the `event.dataset` value. This means users may need to translate their custom dataset values (e.g. `event.dataset: firewall/config`) to an equivalent legal dataset, according to the character restrictions imposed by the use of the value in `data_stream.dataset`, for example `data_stream.dataset: firewall.config`.



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
### Relation to event.* fields
Concerns have been raised about how these fields relate to the event fields. Specifically, `event.type`, `event.kind`, `event.category` etc. Specifically, `data_stream.type` seems closer to `event.kind` than `event.type`. There are other inconsistencies here and we didn't find a way to square this concern at the time. It was decided to move forward with the `data_stream` fields for now and consider them to be unrelated to the event fields. `event.dataset` and `data_stream.dataset`, however, should contain the same value.

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

Elastic Agent already uses the data_stream fields.

Additionally, as previously described, beginning in version 7.9, Elasticsearch ships with built-in index templates for data streams which will automatically ensure that data_stream fields get correctly mapped when the data stream name match `logs-*-*` and `metrics-*-*`.


## People

The following are the people that consulted on the contents of this RFC.

* @roncohen | author, sponsor
* @ruflin | author, sponsor, subject matter expert


<!--
Who will be or has consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

<!-- Insert any links appropriate to this RFC in this section. -->

* Elasticsearch documentation on the [constant_keyword mapping type](https://www.elastic.co/guide/en/elasticsearch/reference/master/keyword.html#constant-keyword-field-type)
* https://www.elastic.co/guide/en/elasticsearch/reference/current/faster-filtering-with-constant-keyword.html
* Previous discussion on [dataset fields](https://github.com/elastic/ecs/pull/845)
* Discussion on [field value restrictions](https://github.com/elastic/kibana/issues/75846)
* Restrictions on [index names](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html)
* Blog post: [An introduction to the Elastic data stream naming scheme](https://www.elastic.co/blog/an-introduction-to-the-elastic-data-stream-naming-scheme)
* Elasticsearch documentation on [data stream naming scheme](https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-a-data-stream.html#elastic-data-stream-naming-scheme.)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 1: https://github.com/elastic/ecs/pull/980
* Stage 2: https://github.com/elastic/ecs/pull/1145
* Stage 3: https://github.com/elastic/ecs/pull/1212
  * Stage 3 date correction: https://github.com/elastic/ecs/pull/1306
* Rollback to stage 2: https://github.com/elastic/ecs/pull/1367
<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
