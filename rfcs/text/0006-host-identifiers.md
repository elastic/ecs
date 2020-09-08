# 0006: Host Identifiers
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2020-09-08** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

Many sources populating event `host.*` fields have different behaviors in how the host values are set. This can cause confusion, complexity, and frustration for users expecting to easily identify unique hosts in their environments. This RFC proposes establishing a common convention to ensure more consistent mapping of these host identifier fields.

At the time of writing, the following are several known challenges caused by these inconsistencies:

* Confusion between the `host.name` and `host.hostname` fields
* Unicity problems in raw hostnames. This can be common with workstations on certain OSes, for example a fleet of "MacBook-Pro.local"
* Unicity problems in host.ids (e.g. misconfigured config management tools, machine images, disk snapshots, etc.)
* Usage of unqualified vs. fully-qualified hostnames in the same fields (by different data sources) leads to host duplication

## People

The following are the people that consulted on the contents of this RFC.

* @ebeahan | author
* @webmat | co-author

<!--
Who will be or has consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible. This list will likely change or grow stage after stage.

e.g.:

* @Yasmina | author
* @Monique | sponsor
* @EunJung | subject matter expert
* @JaneDoe | grammar, spelling, prose
* @Mariana
-->


## References

<!-- Insert any links appropriate to this RFC in this section. -->
* https://github.com/elastic/beats/issues/1070#issuecomment-677782937
* https://github.com/elastic/kibana/pull/74272
* https://github.com/elastic/beats/issues/18043#issuecomment-623501936

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/955

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
