# 0029: Enforce single values for fields
- Stage: **0 (strawperson)**
- Date: **2021/11/24**

Most fields only hold single values but this is only partially documented and not formally enforced by elasticsearch mappings.
Elasticsearch is proposing some [changes to field mappings to allow arrays to be rejected](https://github.com/elastic/elasticsearch/issues/80825).
If ECS uses the new `allow_multiple_values:false` setting on single valued fields this would:

* Document more clearly which fields are single-valued for data providers and consumers.
* Ensure these declarations are enforced.

Note: this is is still proposed elasticsearch functionality so we are opening this RFC to see if there is interest in it.

## Fields

Potentially many fields. Probably best to start with clear candidates like `@timestamp` fields

## Usage

The `allow_multiple_values:false` flag will be added to elasticsearch field mappings that are single-valued (the default being multi-valued).

## Source data


## Scope of impact

Data providers that break the documented conventions for single-valued fields will have their documents rejected if they contain arrays.

## Concerns

We may not implement this elasticsearch feature (input from the ECS team will help determine how useful this feature might be)

## People

*  @markharwood | Author
*  @djptek | Sponsor

## References

https://github.com/elastic/elasticsearch/issues/80825

### RFC Pull Requests

