# 0022: Remove process.ppid
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1 (draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-05-03** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

The `process.ppid` field has been part of ECS since 1.0.0. The `process.parent.*` fields were later introduced in ECS 1.3.0, including `process.parent.pid`. Both fields serve the same purpose: capture the process identifier (PID) of a process' parent.

There's no need to have two fields to capture the same value and to avoid unneeded duplication and confusion, one of the fields should be removed. All of the parent process fields are now included in ECS with the `process.parent.*` nesting, and `process.ppid` should be deprecated and later removed.

## Fields

Removing `process.ppid` will take place in two steps:

1. ECS `1.x`: Indicate that `process.ppid` is deprecated in the fields description in an upcoming ECS minor release. Producers and consumers of `process.ppid` should transition to using `process.parent.pid` instead.
2. Later remove `process.ppid` field as a breaking change.

Removing `process.ppid` will also eliminate the unnecessary `process.parent.ppid` field that exists in ECS due to the `process.*` field set being reused as `process.parent.*`.

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

New processes are typically spawned directly from their parent, or calling, process. Capturing the parent PID (PPID) has many applications:

* Modeling process hierarchy
* Attackers may try to start a process with an arbitrary parent process set. Capturing the PPID value helps identify if an attacker is attempting privilege escalation through PPID spoofing.
* Collecting PPID as a possible data point to help with the observability of a system.

Users will still be able to capture the PPID in the `process.parent.pid` field. Having the one single field available should help improve the experience for anyone trying to capture and query PPIDs from their events.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

The `process.ppid` is populated across several data sources:

* APM Server and agents
* Beats modules
* Beats `add_process_metadata` processor
* Elastic agent integration packages

An example of how `process.ppid` is populated:

```json
{
    "@timestamp": "2016-12-07T02:16:24.827Z",
    "process": {
        "executable": "/usr/bin/kmod",
        "exit_code": 0,
        "name": "modprobe",
        "pid": 391,
        "ppid": 390,
    },
    "service": {
        "type": "auditd",
    }
}
```

Now how the above document would be updated for `process.parent.pid` instead:

```json
{
    "@timestamp": "2016-12-07T02:16:24.827Z",
    "process": {
        "executable": "/usr/bin/kmod",
        "exit_code": 0,
        "name": "modprobe",
        "pid": 391,
        "parent": {
            "pid": 390
        }
    },
    "service": {
        "type": "auditd",
    }
}
```

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
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

### Ingestion mechanisms

APM, Beats, Elastic Agent, and any processors that populate `process.ppid` today will need to be identified and a migration plan to `process.parent.pid` established.

### Usage mechanisms

The security detection rules [repo](https://github.com/elastic/detection-rules) will need audited. Any usage of `process.ppid` should ideally migrate to `process.parent.pid`, but backward compatibility also remains essential.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

### Data producers populating `process.ppid`

The `process.ppid` is populated in many data producers. Migrating to `process.parent.pid` will take coordination before removing the field from ECS entirely.

Field aliases might be of some use to alleviate some pain during the migration for any aggregations or visualizations relying on `process.ppid`:

```
PUT rfc_0018/_mapping
{
  "properties": {
    "process": {
      "properties": {
        "ppid": {
          "type": "alias",
          "path": "process.parent.pid"
        },
        "parent": {
          "properties": {
            "pid": {
              "type": "long"
            }
          }
        }
      }
    }
  }
}
```

### Removing `process.parent.ppid`

Removing `process.ppid` will also remove its reuse in `process.parent`: `process.parent.ppid` (parent's parent PID). This will leave ECS without an equivalent, replacement field.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | author, sponsor
* @jonathan-buttner | subject matter expert
* @gabriellandau | subject matter expert
* @ferullo | subject matter expert
* @rw-access | subject matter expert


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

* Stage 0: https://github.com/elastic/ecs/pull/1337
* Stage 1: https://github.com/elastic/ecs/pull/1450

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
