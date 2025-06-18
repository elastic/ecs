# 0000: Add user.is_privileged boolean field

- Stage: **0 (strawperson)** 
- Date: **TBD** 

This RFC proposes adding a new boolean field, `user.is_privileged`. It will explicitly flag when a user has elevated or administrative rights such as ability to grant permissions, perform `sudo`, or manage IAM roles—so analysts can more easily filter, alert on, and correlate privileged‐user activity without custom parsing.

## Fields

```yaml
- name: user.is_privileged
  type: boolean
  level: extended
  description: >
    True if the user associated with the event has elevated or administrative privileges,
    such as membership in a `sudo` or `Administrators` group, use of `sudo`, or assignment
    of owner/admin roles in cloud IAM.
  example: true
```

## Usage

Treating privileged status as a first-class field (vs. a tag) lets Kibana’s Entity Store resolve the current boolean value without extra parsing.

Analysts will often want to perform more focused monitoring on privileged users, having it as a field in ECS will simplify this querying, e.g 

```kql
event.category:authentication and user.is_privileged:true
```

## Source data

The entity centric integrations such as okta entity analytics and Entra ID entity analytics could populate this field, linux and windows integrations could also annotate command executions with this.

## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

## Concerns

- Cross-platform consistency: what counts as “privileged”?
<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @hop-dev | author
* @jaredburgettelastic | co-author
* @MikePaquette | SME



## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

* Stage 0: https://github.com/elastic/ecs/pull/2493

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
