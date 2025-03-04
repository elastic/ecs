---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-conventions.html
applies_to:
  stack: all
  serverless: all
---

# Conventions [ecs-conventions]

The implementation of ECS follows a few conventions. Understanding them will help you understand ECS better.


## Datatype for integers [_datatype_for_integers]

Unless otherwise noted, the datatype used for integer fields should be `long`.


## IDs and most codes are keywords, not integers [_ids_and_most_codes_are_keywords_not_integers]

Despite the fact that IDs and codes (such as error codes) are often integers, this is not always the case. Since we want to make it possible to map as many systems and data sources to ECS as possible, we default to using the `keyword` type for IDs and codes.

Some specific kinds of codes are always integers, like HTTP status codes. If those have a specific corresponding specific field (as HTTP status does), its type can safely be an integer type. But generic fields like `error.code` cannot have this guarantee, and are therefore `keyword`.


## Text indexing and multi-fields [_text_indexing_and_multi_fields]

Elasticsearch can index text using datatypes:

* **`text`** Text indexing allows for full text search, or searching arbitrary words that are part of the field. See [Text datatype](elasticsearch://reference/elasticsearch/mapping-reference/text.md) in the {{es}} Reference Guide.
* **`keyword`** Keyword indexing offers faster exact match filtering, prefix search (like autocomplete), and makes aggregations (like {{kib}} visualizations) possible. See the {{es}} Reference Guide for more information on [exact match filtering](elasticsearch://reference/query-languages/query-dsl-term-query.md), [prefix search](elasticsearch://reference/query-languages/query-dsl-prefix-query.md), or [aggregations](elasticsearch://reference/data-analysis/aggregations/index.md).


## Default Elasticsearch convention for indexing text fields [_default_elasticsearch_convention_for_indexing_text_fields]

Unless your index mapping or index template specifies otherwise (as the [ECS index template](/reference/ecs-artifacts.md) does), Elasticsearch indexes a text field as `text` at the canonical field name, and indexes a second time as `keyword`, nested in a multi-field.

Default Elasticsearch convention:

* Canonical field: `myfield` is `text`
* Multi-field: `myfield.keyword` is `keyword`


## ECS convention for indexing text fields [_ecs_convention_for_indexing_text_fields]

ECS flips the above convention around.

For monitoring use cases, `keyword` indexing is needed almost exclusively, with full text search needed on very few fields. Moreover, indexing for full text search on lots of fields, where it’s not expected to be used is wasteful of resources.

Given these two premises, ECS defaults all text indexing to `keyword` datatype (with very few exceptions). Any use case that requires full text search indexing on additional fields can add a [multi-field](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md) for full text search. Doing so does not conflict with ECS, as the canonical field name will remain `keyword` indexed.

So the ECS multi-field convention for text is:

* Canonical field: `myfield` is `keyword`
* Multi-field: `myfield.text` is `text`

**Exceptions**

The only exceptions to this convention are fields `message` and `error.message`, which are indexed for full text search only, with no multi-field. These two fields don’t follow the new convention because they are deemed too big of a breaking change with these two widely used fields in Beats.

Any future field that will be indexed for full text search in ECS will however follow the multi-field convention where `text` indexing is nested in the multi-field.
