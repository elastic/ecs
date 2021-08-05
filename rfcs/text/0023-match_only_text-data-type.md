# 0023: Migrate `text` fields to `match_only_text`
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **3 (finished)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

Indexing `message` fields as the `text` type in security and application logs consume significant disk space. Part of the disk space spent is on indexing to support scoring and phrase queries, which logging use cases don't frequently use. Elasticsearch 7.14 introduced a new field type called `match_only_text`, a more space-efficient variant of the `text` field type for these logging-focused use cases.

This RFC proposes migrating existing ECS `text` fields to `match_only_text`. Most current ECS datasets are focused heavily on logging use cases, and we can pass these disk space savings onto users by migrating `text` fields to `match_only_text` by default in ECS. In addition, upcoming changes in Elasticsearch will default to indexing the `message` field as `match_only_text`, and this change in ECS will also align better with this new stack default.

## Fields

### Direct Usage

The following fields are currently indexed as `text` and are candidates to migrate to `match_only_text`:

* `message`
* `error.message`

### Multi-field Usage

ECS also has `text` type multi-fields for several fields using the convention `<field-name>.text`. This RFC also proposes to migrate all `text` multi-fields to using `match_only_text`:

* `client.as.organization.name.text`
* `client.user.full_name.text`
* `client.user.name.text`
* `destination.as.organization.name.text`
* `destination.user.full_name.text`
* `destination.user.name.text`
* `error.stack_trace.text`
* `file.path.text`
* `file.target_path.text`
* `host.os.full.text`
* `host.os.name.text`
* `host.user.full_name.text`
* `host.user.name.text`
* `http.request.body.content.text`
* `http.response.body.content.text`
* `observer.os.full.text`
* `observer.os.name.text`
* `organization.name.text`
* `process.command_line.text`
* `process.executable.text`
* `process.name.text`
* `process.parent.command_line.text`
* `process.parent.executable.text`
* `process.parent.name.text`
* `process.parent.title.text`
* `process.parent.working_directory.text`
* `process.title.text`
* `process.working_directory.text`
* `server.as.organization.name.text`
* `server.user.full_name.text`
* `server.user.name.text`
* `source.as.organization.name.text`
* `source.user.full_name.text`
* `source.user.name.text`
* `threat.technique.name.text`
* `threat.technique.subtechnique.name.text`
* `url.full.text`
* `url.original.text`
* `user.changes.full_name.text`
* `user.changes.name.text`
* `user.effective.full_name.text`
* `user.effective.name.text`
* `user.full_name.text`
* `user.name.text`
* `user.target.full_name.text`
* `user.target.name.text`
* `user_agent.original.text`
* `user_agent.os.full.text`
* `user_agent.os.name.text`
* `vulnerability.description.text`

## Usage

Data is indexed the same as a `text` field that has:

* `index_options: docs`
* `norms: false`

`match_only_text` uses the `_source` for positional queries like `match_phrase`.

The `match_only_text` type supports the same feature set as `text`, except the following:

* No support for scoring: queries ignore index statistics and produce constant scores.
* Span queries are unsupported. If a span query runs, shards where the field maps as match_only_text, will return as failed in the search response, and those shard hits are ignored.
* Phrase and intervals queries run slower.

Like `text`, `match_only_text` fields support limited aggregations.

This new field is part of the text family and returns as a text field in the `_field_caps` output. Being a member of the `text` field family means migrating fields from `text` to `match_only_text` is a non-breaking change. Users can query `text` and `match_only_text` fields alongside each other.

## Source data

Example index mappings with the `match_only_type` changes:

### `message`

```json
{
  "_meta": {
    "documentation": "https://www.elastic.co/guide/en/ecs/current/ecs-base.html",
    "ecs_version": "2.0.0-dev"
  },
  "template": {
    "mappings": {
      "properties": {
        "message": {
          "type": "match_only_text"
        }
      }
    }
  }
}
```

### `error.message`

```json
{
  "_meta": {
    "documentation": "https://www.elastic.co/guide/en/ecs/current/ecs-error.html",
    "ecs_version": "2.0.0-dev"
  },
  "template": {
    "mappings": {
      "properties": {
        "error": {
          "properties": {
            "message": {
              "type": "match_only_text"
            }
          }
        }
      }
    }
  }
}
```

### Multi-field example usage

```json
{
  "mappings": {
    "properties": {
      "client": {
        "properties": {
          "as": {
            "properties": {
              "organization": {
                "properties": {
                  "name": {
                    "fields": {
                      "text": {
                        "type": "match_only_text"
                      }
                    },
                    "ignore_above": 1024,
                    "type": "keyword"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### Field capabilities example for `message`

```json
{
  "indices" : [
    "test"
  ],
  "fields" : {
    "message" : {
      "text" : {
        "type" : "text",
        "metadata_field" : false,
        "searchable" : true,
        "aggregatable" : false
      }
    }
  }
}

```

## Scope of impact

Ingestion mechanisms will need to adopt the new mappings to index fields as the new type. However, since both `text` and `match_only_text` are members of the `text` type family, this will not cause a conflict in Kibana index patterns across indices using the two types for the same field.

As with all type changes in ECS, the ECS team will benchmark and identify any significant storage, indexing, or query changes. The Elasticsearch performance will be engaged, if necessary, to determine the results. However, `match_only_text` is a `text` field with these settings:

* `index_options: docs`
* `norms: false`

ECS already sets `norms: false` on all `text` fields as a convention, so this setting should not impact performance. Setting `index_options: docs` only indexes the doc number and has already been recommended to reduce the disk usage needed for indexing.

Negative performance or storage side-effects from this change are not expected, except the noted limitation of phrase and interval queries will run slower.

## Concerns

### Limitations

As mentioned previously, there are limitations of using `match_only_text`:

* No support for scoring: queries ignore index statistics and produce constant scores.
* Span queries are unsupported. If a span query runs, shards where the field maps as match_only_text will return as failed in the search response, and those shard hits are ignored.
* Phrase and intervals queries run slower.

**Resolution**: For the logging use cases that make up most ECS adoption, disabling frequencies and positions should be acceptable in exchange for reducing index disk usage.

### Potential heavy usage of phrase and interval queries

Security or observability solutions may depend on heavy usage of interval or, more likely, phrase queries. Users could also have implemented custom phrase or interval queries in alerting or detection rules.

**Resolution**: The reduced disk overhead provided from using `match_only_text` fields will benefit most users, and it should be the default ECS experience. If desired, users can update their index mappings to use `text` over `match_only_text` with no conflicts, and an upcoming ECS docs addition will describe this interchangeability.

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | author, sponsor
* @jpountz | subject matter expert

## References

<!-- Insert any links appropriate to this RFC in this section. -->

* https://www.elastic.co/guide/en/elasticsearch/reference/master/text.html#match-only-text-field-type
* https://www.elastic.co/blog/save-10-percent-disk-space-on-your-logging-datasets-with-match-only-text
* https://github.com/elastic/elasticsearch/pull/66172
* https://github.com/elastic/ecs/issues/1377
* https://github.com/elastic/elasticsearch/issues/64467
* https://github.com/elastic/elasticsearch/blob/7.x/x-pack/plugin/core/src/main/resources/data-streams-mappings.json#L14-L22

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1396
* Stage 1: https://github.com/elastic/ecs/pull/1415
* Stage 2: https://github.com/elastic/ecs/pull/1522
* Stage 3: https://github.com/elastic/ecs/pull/1560
