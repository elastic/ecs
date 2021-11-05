# 0028: cgroup fieldset
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-11-05** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

This is a proposal to add a top-level `cgroup` fields to ECS. We have cgroup V2 support incoming in the system/process metricset in 7.15, and cgroups V2 reports a variety of metric fields differently compared to V1. While many OSes and platforms are currently operating in "hybrid" or V1 only mode, this will become an issue as more OSes and cgroup-based platforms like docker make use of cgroups V2.
Right now, a handful of visualizations in the observability App within Kibana use cgroup metrics, and these visualizations will only work on Cgroups V1. In order to extract the same or similar metrics under V2, they will need to access different fields. This is an excellent use case for ECS, as it allows us to standardize the placement of common metrics such as cgroup cpu/memory usage, etc, particularly as visualizations are already relying on these metrics.
In the case of Cgroups V1 versus V2, we decided to report V2 metrics "natively" as opposed to conforming to the V1 fields in order to avoid mangling V2 metrics and confusing users who were expecting V2 metrics to be reported in a similarly transparent fashion as V1. Many of the field changes are the result of cgroup controllers changing names; for example, the V1 `blkio` controller becomes `io` on V2, with many of the underlying metrics remaining the same.

The scope of cgroup metrics may also expand over time, as other processors and data streams add cgroup metrics, thus requiring common fields for metrics reported across different data streams. This is also relevant to container monitoring, as we may want to report "raw" cgroup metrics from containers as our container monitoring expands.


<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

The fields added by this RFC are _not a comprehensive list of all metrics that are shared with both cgroups V1 and V2_. Rather, it is a list of all shared cgroup metrics that are most likely to be useful for future monitoring and visualization. As it stands, this is currently limited to `cpu` and `memory` metrics. We can expand this, of course, but this current PR covers the most important metrics shared across cgroups.

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

This rfc is meant to head off an oncoming problem, which is that various components in the Elastic Stack are incompatible with cgroups V2. Kibana, for example, will frequently use field names that are exclusive to cgroups V1:

```
export const METRIC_CGROUP_MEMORY_LIMIT_BYTES = 'system.process.cgroup.memory.mem.limit.bytes';
```

While cgroups V2 adoption is fairly low, particularly among LTS-style distros and software, this is going to become a problem, and we first need an ECS standard for what these fields should be called.

Aside from existing code, this will help with users running under a "hybrid" cgroups system, as the metricbeat cgroups code must decide if a process is under the control of cgroups V1 or V2, which means different processes on a system can report different cgroups code. A common set of fields will allow important metrics to be comparable across the system, even if that system is using two different versions of cgroups.
The same can be said for heterogeneous clusters running different versions of cgroups across multiple machines.

## Source data

The source data for much of cgroups comes from the cgroupfs file system on the host machine:

```
ls /sys/fs/cgroup/user.slice/user-1000.slice/session-23.scope
cgroup.controllers  cgroup.freeze     cgroup.max.descendants  cgroup.stat             cgroup.threads  cpu.pressure  io.pressure     memory.events        memory.high  memory.max  memory.numa_stat  memory.pressure  memory.swap.current  memory.swap.high  pids.current  pids.max
cgroup.events       cgroup.max.depth  cgroup.procs            cgroup.subtree_control  cgroup.type     cpu.stat      memory.current  memory.events.local  memory.low   memory.min  memory.oom.group  memory.stat      memory.swap.events   memory.swap.max   pids.events
```

The structure and content of these directories varies between V1 and V2.

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

The underlying code that reports these metrics currently exists, this RFC represents only the final step in the process to standardize metrics between two different reporting versions. Perhaps the largest potential concern here is that the problems addressed by this RFC are technically temporary. In theory, cgroups V1 will eventually get deprecated, rendering the need for a common set of fields moot. In addition, cgroups is entirely transparent
to the overwhelming majority of users, who will never interact with cgroups directly.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @fearful-symmetry | author
* @jsoriano | sponsor


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

* Stage 0: https://github.com/elastic/ecs/pull/1610
* Stage 1: https://github.com/elastic/ecs/pull/1626
  * Stage 1 date correction: https://github.com/elastic/ecs/pull/1650

