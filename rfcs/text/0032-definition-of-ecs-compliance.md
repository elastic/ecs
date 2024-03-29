# 0032: Definitions of ECS Compliance
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (candidate)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2022-05-16** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

Events described as "ECS-compliant" follow the [ECS guidelines and best practices](https://www.elastic.co/guide/en/ecs/current/ecs-guidelines.html). While the guidelines provide an overview, more detailed, established guidance aids both mapping to and understanding of ECS events. This proposal standardizes what is and is not expected of an ECS-compliant event.

This document's usage of the terms _must_, _must not_, _should_, _should not_, _required_, and _may_ are in accordance with [IETF RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Fields

The following sections describe the required, suggested, and optional practices. Later sections include more detailed examples of the requirements and guidelines.

### Minimum requirements

An ECS-compliant event MUST:

* populate the `@timestamp` field with the date/time the event originated.
* set `ecs.version` to the ECS version this event conforms.
* index all ECS fields using the data type defined in the schema. A different type from the same type family (e.g., `keyword` for `wildcard`) may substitute
* use nested fields over dotted. ECS events should use nested objects, `{ "log": { "level": "debug" }}`), over dotted field names, `{ "log.level": "debug" }`.

### Recommended guidelines

ECS-compliant events SHOULD:

* map the contents of the original event to as many ECS fields as possible.
* populate the top-level `message` field.
* If a field expects an array, the value should always be an array even if the array contains one value (for example, `[ 10.42.42.42 ]`).
* lowercase the value if the field's description calls for it.
* set the event categorization fields using the [allowed values](https://www.elastic.co/guide/en/ecs/current/ecs-category-field-values-reference.html).
* populate `source.*` and `destination.*` as a pair, when possible.
* populate `source.*`/`destination.*` if `client.*`/`server.*` are populated.
* copy all relevant values into the `related.*` fields.
* use "breakdown" fields. Breakdown fields take an original value and deconstruct it. Examples include `user_agent.*` or `.domain`, `.sub_domain`, `.registered_domain`, etc.
* duplicate the `.address` field value into either `.ip` or `.domain`. Dot not populate the `.ip` and `.domain` fields directly.

### Optional

ECS-compliant events MAY:

* store the entire raw, original event in `event.original`. Disable indexing and doc_values on `event.original` to reduce store.
* add multi-fields not defined by ECS. For example, a text multi-field with a custom analyzer.
* remove unused ECS fields or entire field sets from an index mapping.
* use custom fields alongside ECS fields in an event following these convention:
  * ECS field names avoids using proper nouns. Nest custom fields in a namespace using a proper noun: a tool name, project, or company (e.g., `nginx`, `acme_corp`).
  * ECS field names are always lowercase. Use capitalized key names to avoid future field conflicts.
  * Place custom fields inside a dedicated namespace and not at the top-level of an event.

## Usage

An ECS-compliant event will have `@timestamp`, `ecs.version`, and at least one other field. Dots in the ECS field name represent a nested object structure. The following mapping indexes as the correct data types into Elasticsearch:

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

This compliant event builds on the required guidelines and incorporates many recommended practices.

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
  "nginx": {
    "access": {
      "remote_ip_list": [
        "10.42.42.42",
      ]
    }
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

1. Maps as many fields as possible based on what was available in the event. An Elasticsearch ingest pipeline also populates more fields.
2. Fields expecting arrays, like `event.category`, use arrays even for a single value.
3. Adds the event categorization fields (`event.kind`, `event.category`, `event.type`, and `event.outcome`).
4. Populates `source.*` and `destination.*` fields as a pair.
5. Concatenate all IP addresses into the `related.ip` field.
6. Both `source.address` and `destination.address` copy the `*.address` to its sibling `.ip` field.
7. The original user-agent value populates `user_agent.original`. Other fields hold the broken down values: `user_agent.os.*`, `user_agent.name`, `user_agent.version`, etc.
8. A custom namespace, `nginx.*`, holds any custom fields. Nginx is a proper noun and will never conflict with any future ECS field names.

## Source data

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

The ECS-compliant guidance applies to all ECS data sources.

## Scope of impact

This proposal is informational and includes no changes to ECS. Beats, Elastic Agent, and APM users already gain the benefits of ECS-compliant data. Custom sources will benefit normalizing their data into ECS-compliant events.

## Concerns

### Arrays in ECS

Any field can contain one or more values of the same type. There is no dedicated [array type](https://www.elastic.co/guide/en/elasticsearch/reference/current/array.html) in Elasticsearch. Why distinguish array vs. non-array fields in ECS?

While Elasticsearch is permissive, other software languages and configurations support array constructs. Components adopting ECS are able to expect what fields do and don't use arrays.

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

* https://www.elastic.co/guide/en/ecs/current/ecs-guidelines.html
* https://www.elastic.co/guide/en/ecs/current/ecs-principles-design.html
* https://www.elastic.co/guide/en/ecs/current/ecs-mapping-network-events.html

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 1: https://github.com/elastic/ecs/pull/1868
* Stage 2: https://github.com/elastic/ecs/pull/1877

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
