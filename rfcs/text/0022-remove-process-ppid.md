# 0022: Remove process.ppid
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **3 (finished)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-08-05** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

The `process.ppid` field has been part of ECS since 1.0.0. The `process.parent.*` fields were later introduced in ECS 1.3.0, including `process.parent.pid`. Both fields serve the same purpose: capture the process identifier (PID) of a process' parent.

There's no need to have two fields to capture the same value. ECS now includes all parent process fields under the `process.parent.*` nesting, and `process.ppid` should be deprecated and later removed.

## Fields

Removing `process.ppid` will take place in two steps:

1. ECS `1.x`: Indicate that `process.ppid` is deprecated in the fields description in an upcoming ECS minor release. Producers and consumers of `process.ppid` should use `process.parent.pid` instead.
2. Later remove `process.ppid` field as a breaking change.

Removing `process.ppid` will also eliminate `process.parent.ppid`.

## Usage

New processes are typically spawned directly from their parent, or calling, process. Capturing the parent PID (PPID) has many applications:

* Modeling process hierarchy
* Attackers may try to start a process with an arbitrary parent process set. Capturing the PPID value helps identify if an attacker is attempting privilege escalation through PPID spoofing.
* Collecting PPID as a possible data point to help with the observability of a system.

Users will still be able to capture the PPID in the `process.parent.pid` field. Having the single field available should help improve the experience for anyone trying to capture and query PPIDs from their events.

## Source data

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

Now the mapping for above document would be updated to use `process.parent.pid` instead:

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

## Scope of impact

### Ingestion mechanisms

APM, Beats, Elastic Agent, and any processors that populate `process.ppid` today will need to be identified and a migration plan to `process.parent.pid` established.

### Usage mechanisms

The security detection rules [repo](https://github.com/elastic/detection-rules) will need audited. Any usage of `process.ppid` should ideally migrate to `process.parent.pid`, but backward compatibility also remains essential.

### ECS

The field will be marked as deprecated in an upcoming ECS `1.x` release in the ECS documentation and be removed entirely from ECS and the docs in the `8.0` release.

## Concerns

### Data producers populating `process.ppid`

The `process.ppid` is populated in many data producers, so migrating to `process.parent.pid` will take coordination when `process.ppid` is removed.

**Resolution**: Field aliases might be of some use to alleviate some pain during the migration for any aggregations or visualizations relying on `process.ppid`:

```json
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

**Resolution**: [Discussed](https://github.com/elastic/ecs/pull/1450#issuecomment-854773783) with Protections, Endpoint, and Observability stakeholders. Not having a replacement field for the parent's parent PID didn't raise significant concerns.

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
  * Stage 1 date correction: https://github.com/elastic/ecs/pull/1555
* Stage 2: https://github.com/elastic/ecs/pull/1556
* Stage 3: https://github.com/elastic/ecs/pull/NNNN

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
