# 0000: Remove process.ppid
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

The `process.ppid` field has been part of ECS since 1.0.0. The `process.parent.*` fields were later introduced in ECS 1.3.0, including `process.parent.pid`. Both fields serve the same purpose: capture the process identifier (PID) of a process' parent.

There's no need to have two fields capturing the same value, and to avoid duplication or user confusion, one of the fields should be removed. With all of the parent process fields are now included in ECS with the `process.parent.*` nesting, `process.ppid` could be deprecated and then later removed.

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

### Timeline

* ECS `1.x`: Indicate that `process.ppid` is deprecated in the fields description in an upcoming ECS minor release. Advise sources populating `process.ppid` to transition to `process.parent.id` instead.
* Next ECS major: Remove `process.ppid` field in the next ECS major release.

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

New processes are typically spawned directly from their parent, or calling, process. Capturing the parent pid (PPID) has many applications:

* Modeling process hierarchy
* Attackers may try to start a process with an arbitrary parent process set. Capturing the PPID value helps identify if an attacker is attempting privilege escalation through PPID spoofing.
* Collecting PPID as a possible datapoint to help with the observability of a system.

Users will still be able to capture the PPID in the `process.parent.pid` field. Having the one single field available should hep improve the experience for anyone trying to capture PPIDs from their events.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

`process.ppid` is actively populated across several data sources:

* APM Server and agents
* Beats modules
* Beats `add_process_metadata` processor
* Elastic agent integration packages

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

The security detection rules [repo](https://github.com/elastic/detection-rules) will need audited. Any usage of `process.ppid` should ideally migrate to `process.parent.id`.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

Since capturing the PPID is useful across the solutions, it will take coordination to complete eliminate it's use before removing from ECS. Field aliases might be of some use to alleviate some pain during the migration for any aggregations or visualizations relying on `process.ppid`.

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

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/NNN

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
