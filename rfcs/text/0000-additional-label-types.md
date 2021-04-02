# 0000: Label fields for additional types
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

The existing `labels` field is intended to capture custom key/value pairs to add custom meta information to events. All `label` values are indexed as `keyword`.

Some uses may need different `label` fields for different Elasticsearch data types. To better accommodate those use cases, this is a proposal to introduce several new object fields within the existing `label` object.

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

### Proposed Fields

* `labels.*` fields will remain type `keyword`
* `labels.long.*` fields will be type `long`
* `labels.double.*` fields will be type `double`
* `labels.boolean.*` fields will be type `boolean`

### Proposed mapping settings

```json
{
  "mappings" : {
    "dynamic_templates" : [
      {
        "labels": {
          "path_match": "labels.*",
          "mapping": {
            "type": "keyword"
          },
          "match_mapping_type": "string"
        }
      },
      {
        "labels_boolean": {
          "path_match": "labels.boolean.*",
          "mapping": {
            "type": "boolean"
          },
          "match_mapping_type": "boolean"
        }
      },
      {
        "labels_double": {
          "path_match": "labels.double.*",
          "mapping": {
            "type": "double"
          },
          "match_mapping_type": "double"
        }
      },
      {
        "labels_long": {
          "path_match": "labels.long.*",
          "mapping": {
            "type": "long"
          },
          "match_mapping_type": "long"
        }
      },
      {
        "strings_as_keywords" : {
          "match_mapping_type" : "string",
          "mapping" : {
            "ignore_above" : 1024,
            "type" : "keyword"
          }
        }
      }
    ],
    "date_detection" : false,
    "properties": {
      "@timestamp": {
        "type": "date"
      },
      "labels": {
        "type": "object",
        "properties": {
          "long": {
            "type": "object"
          },
          "float": {
            "type": "object"
          },
          "boolean": {
            "type": "object"
          }
        }
      }
    }
  }
}
```

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

APM uses non ECS fields for other data types, such as `boolean` and `scaled_float`. Expanding `label` support for types beyond `keyword` in ECS could also better support storing OpenTelemetry attributes (key:value pairs that provide context to a distributed trace).

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

```json
    "labels" : {
      "worker": "netclient",
      "long": {
        "events_published" : 50,
        "events_original" : 50,
        "events_encoded" : 50,
        "events_failed" : 0
      }
    }
```

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

Sources such as Beats or Elastic Agent would need to adopt the new mappings and dynamic field mapping settings.

Kibana index patterns would need identify the new nested fields for each of the new `label` child objects.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

### Using flattened

There have been discussion if using the `flattened` field type could work for the `labels` field to avoid mappings explosions. However, `flattened` has limitations has of this writing:

* A `flattened` object will index all leaf values to `keyword`. Numeric flattened field support is not yet available in Elasticsearch ([elastic/elasticsearch#61550](https://github.com/elastic/elasticsearch/issues/61550))
* Kibana has limited autocompletion and KQL support for `flattened` fields ([elastic/kibana#25820](https://github.com/elastic/kibana/issues/25820)).

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | author

<!--
Who will be or has been consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

* https://github.com/elastic/apm-server/issues/3873

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/NNN

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
