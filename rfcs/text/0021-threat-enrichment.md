# 0021: Threat Enrichment

- Stage: **3 (finished)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-07-06** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

As [documented](https://github.com/elastic/ecs/pull/1293#issuecomment-825212880) in the [existing threat intel RFC](https://github.com/elastic/ecs/pull/1293), this proposal aims to solve the threat intel enrichment use case by reusing the `threat.indicator` fieldset under a new name and as an array of objects, where each object represents an indicator that matched the (now enriched) event, and the `matched.*` fields on each object provide context for that particular indicator match.

Moving this list of indicators to a new field allows us to:

* reuse the existing `threat.indicator` fieldset
* sidestep the documentation/mapping complexities around when `threat.indicator` is an object (indicator) vs. when it's an array of objects (enrichment)

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

As these fields represent the enrichment of an existing event with indicator information, they are comprised of two categories of data:

1. The indicator's indicator fields, as defined in RFC 0018
2. Fields representing the context of the enrichment itself

### Proposed new fields

Field | Type | Example | Description
--- | --- | --- | ---
threat.enrichments.matched.atomic | keyword | 2f5207f2add28b46267dc99bc5382480 | The value that matched between the event and the indicator
threat.enrichments.matched.id | keyword | db8fb691ffdb4432a09ef171659c8993e6ddea1ea9b21381b93269d1bf2d0bc2 | The _id of the indicator document that matched the event
threat.enrichments.matched.index | keyword | threat-index-000001 | The _index of the indicator document that matched the event
threat.enrichments.matched.field | keyword | host.name | Identifies the field on the enriched event that matched the indicator
threat.enrichments.matched.type | keyword | indicator_match_rule | Identifies the type of the atomic indicator that matched a local environment endpoint or network event.

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

### Adding threat intelligence match/enrichment to another document

If it is determined that an event matches a given indicator, that event can be enriched with said indicator. Presently, Indicator Match Detection rules will perform that enrichment automatically, but ad hoc/manual enrichment is an expected feature that analysts will leverage in the future.

#### Example document

```json5
{
  "process": {
    "name": "svchost.exe",
    "pid": 1644,
    "entity_id": "MDgyOWFiYTYtMzRkYi1kZTM2LTFkNDItMzBlYWM3NDVlOTgwLTE2NDQtMTMyNDk3MTA2OTcuNDc1OTExNTAw",
    "executable": "C:\\Windows\\System32\\svchost.exe"
  },
  "message": "Endpoint file event",
  "@timestamp": "2020-11-17T19:07:46.0956672Z",
  "file": {
    "path": "C:\\Windows\\Prefetch\\SVCHOST.EXE-AE7DB802.pf",
    "extension": "pf",
    "name": "SVCHOST.EXE-AE7DB802.pf",
    "hash": {
      "sha256": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4"
    }
  },
  "threat": {
    "enrichments": [
      {
        // Each enrichment is added as a nested object under `threat.enrichments.*`
        // Copy all the object indicators under `indicator.*`, providing full context
        "indicator": {
          "confidence": "High",
          "marking": {
            "tlp": "WHITE"
          },
          "first_seen": "2020-10-01",
          "file": {
            "hash": {
              "sha256": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4",
              "md5": "1eee2bf3f56d8abed72da2bc523e7431"
            },
            "size": 656896,
            "name": "invoice.doc"
          },
          "last_seen": "2020-11-01",
          "reference": "https://system.example.com/event/#0001234",
          "sightings": 4,
          "type": ["sha256", "md5", "file_name", "file_size"],
          "description": "file last associated with delivering Angler EK"
        },
        /* `matched` will provide context about which of the indicators above matched on this
              particular enrichment. If multiple matches for this indicator object, this could
              be a list */
        "matched": {
          "atomic": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4",
          "field": "file.hash.sha256",
          "id": "abc123f03",
          "index": "threat-indicators-index-000001",
          "type": "indicator_match_rule"
        }
      }
    ]
  },
  // Tag the enriched document to indicate the threat enrichment matched
  "tags": ["threat-match"],
  // This should already exist from the original ingest pipeline of the document
  "related": {
    "hash": ["0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4"]
  }
}
```

### Proposed enrichment pipeline mechanics pseudocode

1. Original document completes its standard pipeline for the given source (i.e. filebeat module pipeline)
2. Original document is sent to "threat lookup" pipeline
3. For each indicator type, we perform the following (a file sha256 for example):
   - if exists "file.hash.sha256":
     - enrich processor:
       "policy_name": "file-sha256-policy",
       "field" : "file.hash.sha256",
       "target_field": "threat_match",
       "max_matches": "1"
     - policy file-sha256-policy:
       "match": {
         "indices": "threat-\*",
         "match_field": "threat.indicator.file.hash.sha256",
         "enrich_fields": ["threat.indicator"]
       }
   - set:
     field: "threat_match.threat.matched.type"
     value: "file-sha256-policy"
   - set:
     field: "threat_match.threat.matched.field"
     value: "file.hash.sha256"
   - set:
     field: "threat_match.threat.matched.atomic"
     value: "{{ file.hash.sha256 }}"
   - set:
     field: "threat.enrichments"
     value: []
     override: false
   - append:
     field: "threat.enrichments"
     value: "{{ threat_match.threat }}"
   - remove:
     field: "threat_match"

**NOTE**: There may be some optimization on which enrichments we attempt based upon the event categorization fields. For instance, we know that data that presents the netflow model or "interface" doesn't contain a sha256 hash. Since those categorization fields are lists, if data presented as both netflow and file (for whatever reason), then we'd check both network-related lookups and file-related lookups

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

Source data are ECS indicator documents as specified RFC 0008. At present, the best source of these documents is the [filebeat threatintel module](https://github.com/elastic/beats/tree/master/x-pack/filebeat/module/threatintel).

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

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

I believe this format should actually simplify much of the enrichment logic originally proposed in RFC 0008, since a naive implementation would simply copy the fields directly from each indicator document into `threat.enrichments`, and add the appropriate `matched` fields.

While not a concern for ECS consumers at large, our existing experimental implementation within Kibana Security Solution will have to change significantly (for the better!), with accompanying data migration: https://github.com/elastic/kibana/issues/100510

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @rylnd | author
* @devonakerr | sponsor

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

<!-- Insert any links appropriate to this RFC in this section. -->

* Inciting comment: https://github.com/elastic/ecs/pull/1293#issuecomment-825212880
* Threat Intel RFC: https://github.com/elastic/ecs/pull/1293

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1386
* Stage 1: https://github.com/elastic/ecs/pull/1400
* Stage 2: https://github.com/elastic/ecs/pull/1460
  * Stage 2 addendum: https://github.com/elastic/ecs/pull/1502
* Stage 3: https://github.com/elastic/ecs/pull/1581

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
