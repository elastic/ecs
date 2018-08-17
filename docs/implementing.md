# <a name="implementing-ecs"></a>Implementing ECS

## Guidelines

* The document MUST have the `@timestamp` field.
* The [data type](https://www.elastic.co/guide/en/elasticsearch/reference/6.2/mapping-types.html) defined for an ECS field MUST be used.
* It SHOULD have the field `event.version` to define which version of ECS it uses.
* As many fields as possible should be mapped to ECS.

**Writing fields**

* All fields must be lower case
* Combine words using underscore
* No special characters except `_`

**Naming fields**

* *Present tense.* Use present tense unless field describes historical information.
* *Singular or plural.* Use singular and plural names properly to reflect the field content. For example, use `requests_per_sec` rather than `request_per_sec`.
* *General to specific.* Organise the prefixes from general to specific to allow grouping fields into objects with a prefix like `host.*`.
* *Avoid repetition.* Avoid stuttering of words. If part of the field name is already in the prefix, do not repeat it. Example: `host.host_ip` should be `host.ip`.
* *Use prefixes.* Fields must be prefixed except for the base fields. For example all `host` fields are prefixed with `host.`. See `dot` notation in FAQ for more details.
* Do not use abbreviations. (A few exceptions like `ip` exist.)

## Understanding ECS conventions

### Multi-fields text indexing

ElasticSearch can index text multiple ways:

* [text](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) indexing allows for full text search, or searching arbitrary words that
  are part of the field.
* [keyword](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) indexing allows for much faster
  [exact match](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html)
  and [prefix search](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-prefix-query.html),
  and allows for [aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)
  (what Kibana visualizations are built on).

In some cases, only one type of indexing makes sense for a field.

However there are cases where both types of indexing can be useful, and we want
to index both ways.
As an example, log messages can sometimes be short enough that it makes sense
to sort them by frequency (that's an aggregation). They can also be long and
varied enough that full text search can be useful on them.

Whenever both types of indexing are helpful, we use multi-fields indexing. The
convention used is the following:

* `foo`: `text` indexing.
  The top level of the field (its plain name) is used for full text search.
* `foo.raw`: `keyword` indexing.
  The nested field has suffix `.raw` and is what you will use for aggregations.
  * Performance tip: when filtering your stream in Kibana (or elsewhere), if you
    are filtering for an exact match or doing a prefix search,
    both `text` and `keyword` field can be used, but doing so on the `raw`
    field will be much faster and less memory intensive.

**Keyword only fields**

The fields that only make sense as type `keyword` are not named `foo.raw`, the
plain field (`foo`) will be of type `keyword`, with no nested field.

### IDs are keywords not integers

Despite the fact that IDs are often integers in various systems, this is not
always the case. Since we want to make it possible to map as many data sources
to ECS as possible, we default to using the `keyword` type for IDs.
