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

Elasticsearch can index text multiple ways:

* [text](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html)
  indexing allows for full text search, or searching arbitrary words that
  are part of the field.
* [keyword](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html)
  indexing allows for much faster
  [exact match filtering](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html),
  [prefix search](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-prefix-query.html),
  and allows for [aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)
  (what Kibana visualizations are built on).

By default, unless your index mapping or index template specifies otherwise
(as the ECS index template does),
Elasticsearch indexes text field as `text` at the canonical field name,
and indexes a second time as `keyword`, nested in a multi-field.

Default Elasticsearch convention:

* Canonical field: `myfield` is `text`
* Multi-field: `myfield.keyword` is `keyword`

For monitoring use cases, `keyword` indexing is needed almost exclusively, with
full text search on very few fields. Given this premise, ECS defaults
all text indexing to `keyword` at the top level (with very few exceptions).
Any use case that requires full text search indexing on additional fields
can simply add a [multi-field](https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-fields.html)
for full text search. Doing so does not conflict with ECS,
as the canonical field name will remain `keyword` indexed.

ECS multi-field convention for text:

* Canonical field: `myfield` is `keyword`
* Multi-field: `myfield.text` is `text`

#### Exceptions

The only exceptions to this convention are fields `message` and `error.message`,
which are indexed for full text search only, with no multi-field.
These two fields don't follow the new convention because they are deemed too big
of a breaking change with these two widely used fields in Beats.

Any future field that will be indexed for full text search in ECS will however
follow the multi-field convention where `text` indexing is nested in the multi-field.

### IDs are keywords not integers

Despite the fact that IDs are often integers in various systems, this is not
always the case. Since we want to make it possible to map as many data sources
to ECS as possible, we default to using the `keyword` type for IDs.
