# 0000: Definitions of ECS Compliance
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1 (draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

Events following [ECS guidelines and best practices](https://www.elastic.co/guide/en/ecs/current/ecs-guidelines.html) are described as "compliant". While the guidelines outlined in the ECS docs provide a general overview, this proposal aims to standardized what is and is not expected of an ECS-compliant event.

This document's usage of the terms _must_, _must not_, _should_, _should not_, _required_, and _may_ are in accordance with [IETF RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Fields

The following sections briefly describe the required, suggested, and optional practices for complying with ECS. Later sections include more detailed examples of certain items.

### Minimum requirements

An ECS-compliant event MUST:

* populate the `@timestamp` field with the date/time when the event originated.
* set `ecs.version` to the ECS version this event conforms.
* index all ECS fields using the data type defined in the schema. A different type from the same type family (e.g., substitute `text` for `match_only_text` or `keyword` for `wildcard`) may substitute.
* use nested fields over dotted. ECS events should use nested objects, like `{ "log": { "level": "debug" }}`), over dotted field names, such as `{ "log.level": "debug" }`.

### Recommended guidelines

ECS-compliant events SHOULD:

* map the contents of the original event to as many ECS fields as possible.
* populate the top-level `message` field.
* store the entire raw, original event in `event.original`. Indexing and doc_values are disabled on `event.original` to reduce store, but the value is retrieved from `_source`.
* use an array if the field expects and array event if populating a single value.
* lowercase the value if the field's description calls for lowercasing.
* set the event categorization fields using the allowed values.
* `source.*` and `destination.*` be populated as a pair, if possible.
* populate `source.*`/`destination.*` if `client.*`/`server.*` are populated.
* copy all relevant values into the `related.*` fields.
* use "breakdown" fields.
* duplicate the `.address` field value into either `.ip` or `.domain`. The `.ip` and `.domain` fields should not be populated directly.

### Optional

ECS-compliant events MAY:

* Use custom fields alongside ECS fields in an event. Custom fields should use proper names over generic concept names to reduce the change of a future conflict. Custom fields should be nested inside an object (field set) and not leaf fields at the root (base of the event).
* Omit some ECS fields or entire field sets from an index mapping, if they would never be populated by events in those indices.
* Add additional multi-fields not defined by ECS. For example, a `text` multi-field with a custom analyzer or a `keyword` multi-field using the `lowercase` normalizer.

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

An ECS-compliant event will have `@timestamp`, `ecs.version`, and at least one other field. Dots in the ECS field name represent a nested object structure. The following mapping sets the correct data types when this document is indexed into Elasticsearch.

```json
{
  "@timestamp": "2022-03-31T18:48:35.000Z",
  "ecs": {
    "version": "8.1.0"
  },
  "message": "example.com 10.0.0.2, 10.0.0.1, 127.0.0.1 - - [07/Dec/2016:11:05:07 +0100] \"GET /ocelot HTTP/1.1\" 200 571 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0\""
}
```

```json
{
  "mappings" : {
    "properties" : {
      "@timestamp" : {
        "type" : "date"
      },
      "ecs" : {
        "properties" : {
          "version" : {
            "type" : "keyword",
            "ignore_above" : 1024
          }
        }
      },
      "message" : {
        "type" : "match_only_text"
      }
    }
  }
}
```

The following compliant event builds on the required guidelines and incorporates many recommended practices.

```json
{
  "agent": {
    "name": "test",
    "id": "a0e86cd2-d38b-4801-8d54-db5f2fb7f7e1",
    "ephemeral_id": "8568c102-6c2d-495d-800b-bc5b89cde1b6",
    "type": "filebeat",
    "version": "8.1.2"
  },
  "log": {
    "file": {
      "path": "/var/log/nginx/access.log"
    },
    "offset": 2716
  },
  "source": {
    "address": "192.168.64.1",
    "ip": "192.168.64.1"
  },
  "destination": {
    "address": "192.168.64.2",
    "ip": "192.168.64.2"
  },
  "url": {
    "path": "/",
    "original": "/"
  },
  "tags": [
    "nginx-access"
  ],
  "@timestamp": "2022-03-31T18:48:35.000Z",
  "ecs": {
    "version": "8.0.0"
  },
  "related": {
    "ip": [
      "192.168.64.1",
	  "192.168.64.2",
	  "fe80::9c5f:77ff:fe74:604"
    ]
  },
  "host": {
    "hostname": "test",
    "os": {
      "kernel": "5.4.0-105-generic",
      "codename": "focal",
      "name": "Ubuntu",
      "type": "linux",
      "family": "debian",
      "version": "20.04.4 LTS (Focal Fossa)",
      "platform": "ubuntu"
    },
    "ip": [
      "192.168.64.2",
      "fe80::9c5f:77ff:fe74:604"
    ],
    "name": "test",
    "id": "39c062dece654ac393c9f62fc2be2b11",
    "mac": [
      "9e:5f:77:74:06:04"
    ],
    "architecture": "x86_64"
  },
  "http": {
    "request": {
      "method": "GET"
    },
    "response": {
      "status_code": 304,
      "body": {
        "bytes": 0
      }
    },
    "version": "1.1"
  },
  "event": {
    "agent_id_status": "verified",
    "ingested": "2022-03-31T18:48:38Z",
    "timezone": "-05:00",
    "created": "2022-03-31T18:48:37.472Z",
    "kind": "event",
    "category": [
      "web"
    ],
    "type": [
      "access"
    ],
    "dataset": "nginx.access",
    "outcome": "success"
  },
  "user_agent": {
    "original": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "os": {
      "name": "Mac OS X",
      "version": "10.15.7",
      "full": "Mac OS X 10.15.7"
    },
    "name": "Chrome",
    "device": {
      "name": "Mac"
    },
    "version": "99.0.4844.84"
  }
}
```

1. Maps as many fields as possible based on what was available in the event. Some additional data was supplied by an Elasticsearch ingest pipeline.
2. Fields expecting an array of values, like `event.category` and `event.type`, are using arrays even if holding a single value.
3. The categorization fields, `event.kind`, `event.category`, `event.type`, and `event.outcome`, have been added with allowed values.
4. The `source.*` and `destination.*` fields are populated as a pair.
5. All IP addresses are concatenated into the `related.ip` field.
6. Both `source.address` and `destination.address` copy the `*.address` to its sibling `.ip` field.
7. The original user-agent value populates `user_agent.original`. The original value is broken down into its individual parts to populate several other user agent fields: `user_agent.os.*`, `user_agent.name`, `user_agent.version`, etc.

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

The ECS-compliant guidance formalized applies to all ECS data sources.

## Scope of impact

This proposal is informational and includes no changes to ECS. Users of Beats or Elastic Agent will already be gaining the benefits of ECS-compliant data. Custom sources will benefit from normalizing their data into ECS-compliant events.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

### Arrays in ECS

Any field can contain zero or more values of the same type, and there is has no dedicated [array type](https://www.elastic.co/guide/en/elasticsearch/reference/current/array.html) in Elasticsearch. Why distinguish array vs. non-array fields in ECS?

While Elasticsearch is permissive in handling arrays vs. non-array, other software languages and configurations need support for an array construct. For data producers or consumers, it's best to define which fields are expected to support arrays in ECS.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | author, sponsor

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

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 1: https://github.com/elastic/ecs/pull/1868

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
