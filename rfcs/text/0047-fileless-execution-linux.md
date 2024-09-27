# 0047: Fileless execution on Linux
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2024-09-26** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

This RFC proposes adding new fields and event types to enhance the detection of fileless malware execution and related malicious activities on Linux systems.

The new fields include:
 * file.is_memfd - Indicates if the file is an anonymous file descriptor (memfd) created using the memfd_create system call.
 * file.is_shmem - Indicates if the file is a POSIX shared memory object created using the shm_open system call, typically located in /dev/shm.
 * process.is_setuid - Indicates if the process has the setuid bit set, allowing it to run with the privileges of its owner.
 * process.is_setgid - Indicates if the process has the setgid bit set, allowing it to run with the privileges of its group.
 * process.is_memfd - Indicates if the process was executed from a memory file descriptor (memfd).
 * process.inode_nlink - Number of links to the inode of the process executable file, obtained from the i_nlink variable in the inode structure.

New process event types:
 * memfd_create
 * shmget (SystemV shared memory API)
 * ptrace
 * load_module

New file event types:
 * memfd_open
 * shmem_open

These additions will enable the detection and investigation of various malware execution techniques, such as executing code from memory file descriptors (memfd), hiding malicious binaries in shared memory objects (shm_open and shmget), debugging other processes for code injection (ptrace), and loading kernel modules for rootkits (load_module). The proposed fields also cover privilege escalation using setuid/setgid binaries.

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

The data can be collected by monitoring system calls and events on Linux hosts using kernel instrumentation techniques like eBPF or kprobes.

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

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

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

 * @stanek-michal    | author

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

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
