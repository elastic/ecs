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
* Do not use abbreviations or word contractions, use full words.

**Exceptions**

In some cases, ECS naming conventions are overridden by common parlance, if
we think the common parlance will be much clearer. Examples: `ip`, `pid`,
`hostname`, etc.


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
    both `text` and `keyword` field can be used, but doing so on the `keyword`
    field (named `.raw`) will be much faster and less memory intensive.

**Keyword only fields**

The fields that only make sense as type `keyword` are not named `foo.raw`, the
plain field (`foo`) will be of type `keyword`, with no nested field.

### IDs are keywords not integers

Despite the fact that IDs are often integers in various systems, this is not
always the case. Since we want to make it possible to map as many data sources
to ECS as possible, we default to using the `keyword` type for IDs.

## Using non-ECS fields in your event stream

The goal of ECS is to define a common set of fields to make working across various
streams easier. Each stream will have their own particularities, however, and ECS
cannot account for all possibilities. It's therefore important that implementers
feel at ease adding fields and top level objects in their schema that are
not defined in ECS. This is expected.

Doing so will however incur a risk of conflicting with future versions of ECS.
Let's review some strategies to reduce the risk of conflicts happening.

### Conflicts

Before going into strategies, let's define what constitutes a conflict.

#### Conflicts with ECS

* A custom field has the same name as a new ECS field, but an incompatible type:
  * `int` vs `long`
  * `text` vs `keyword`
  * `keyword` vs numeric (`integer`, `long`, etc.)
  * discrete field vs nested object
* A new ECS field has a completely different purpose than the custom field.

The following does **not** constitute a conflict:

* A custom `keyword` field gets defined with the same purpose, with a different
  `ignore_above` value.
* A new field is added to ECS, and matches the name and type of an existing
  custom field.
  * E.g. you define `process.xpid` as a `keyword` field, and ECS adds
    `process.xpid` as a `keyword` field.

#### Conflicts with Third Parties

Elastic is developing ECS and is adjusting their solutions to leverage ECS.
Third parties are also gearing up to adopt ECS, in order to reap the benefits of
using a more common set of field names and definitions.

A consequence of this is that end users may pick a set tools that
include third parties (not just Elastic's) that conform to ECS. Because of this,
when thinking about avoiding conflicts, it's important to consider the
broader ecosystem, not just "will I conflict with Elastic?".

### Consequences of a Conflict

TODO

### How to Reduce the Risk of Conflicts

TODO
