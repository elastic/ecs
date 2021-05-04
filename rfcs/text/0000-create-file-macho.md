# 0000: Create the Mach-O sub-field of the File fieldset

- Stage: **1 (draft)**
- Date: **TBD**

Create the Mach Object (Mach-O) sub-field, of the `file` or `process` top-level fieldsets. This document metadata can be used for malware research, as well as coding and other application development efforts.

## Fields

**Stage 0**

This RFC is to create the Mach-O sub-field within the `file.` fieldset. This will include 35 sub-fields. `macho` itself is a nested
field to account for [multiarchitecture binaries](https://en.wikipedia.org/wiki/Fat_binary). Each architecture will be represented
by a nested objected located at `file.macho`.

| Name                           | Type    | Description                                                     |
|--------------------------------|---------|-----------------------------------------------------------------|
| macho.cdhash                   | keyword | Code Digest (CD) SHA256 hash of the first 20-bytes of the file. |
| macho.cpu                      | object  | CPU information for the file.                                   |
| macho.cpu.architecture         | keyword | CPU architecture target for the file.                           |
| macho.cpu.byte_order           | keyword | CPU byte order for the file.                                    |
| macho.cpu.subtype              | keyword | CPU subtype for the file.                                       |
| macho.cpu.type                 | keyword | CPU type for the file.                                          |
| macho.headers                  | nested  | Header information for the file.                                |
| macho.headers.commands.number  | long    | Number of load commands for the Mach-O header.                  |
| macho.headers.commands.size    | long    | Size of load commands of the Mach-O header.                     |
| macho.headers.commands.type    | keyword | Type of the load commands for the Mach-O header.                |
| macho.headers.magic            | keyword | Magic field of the Mach-O header.                               |
| macho.headers.flags            | keyword | Flags set in the Mach-O header.                                 |
| macho.page_size                | long    | Page size of the file.                                          |
| macho.sections                 | nested  | Section information for the segment of the file.                |
| macho.sections.chi2            | float   | Chi-square probability distribution of the section.             |
| macho.sections.entropy         | float   | Shannon entropy calculation from the section.                   |
| macho.sections.flags           | keyword | Section flags for the segment of the file.                      |
| macho.sections.name            | keyword | Section name for the segment of the file.                       |
| macho.sections.type            | keyword | Section type for the segment of the file.                       |
| macho.sections.physical_offset | keyword    | Section List offset.                                            |
| macho.sections.physical_size   | long    | Section List physical size.                                     |
| macho.sections.virtual_address | keyword    | Section List virtual address.                                   |
| macho.sections.virtual_size    | long    | Section List virtual size.                                      |
| macho.segments                 | nested  | Segment information for the file.                               |
| macho.segments.name            | keyword | Name of this segment.                                           |
| macho.segments.physical_offset | keyword    | File offset of this segment.                                    |
| macho.segments.physical_size   | long | Amount of memory to map from the file.                          |
| macho.segments.sections        | keyword | Section names contained in this segment.                        |
| macho.segments.virtual_address | keyword | Memory address of this segment.                                 |
| macho.segments.virtual_size    | long | Memory size of this segment.                                    |

**Stage 1**

[New `macho.yml` candidate](macho/macho.yml)]

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

**Stage 1**

In performing file analysis, specifically for malware research, understanding file similarities can be used to chain together malware samples and families to identify campaigns and possibly attribution. Additionally, understanding how malware components are re-used is useful in understanding malware telemetry, especially in understanding the impact being made through the introduction of defensive countermeasures.

As an example, if XDR vendors deploys a new malware model to defeat a specific type of ransomware and we start observing a change and/or relationship to the headers, import tables, libraries, etc of that malware family, we can make assumptions that the changes to the malware model are making an impact against the malware family.

As another example, tracking file metadata for specific families is useful in predicting new campaigns if we see similar file metadata being used for new samples. [Example](https://www.bleepingcomputer.com/news/security/maze-ransomware-is-shutting-down-its-cybercrime-operation/), the Maze ransomware family shutting down and re-purposing as Egregor (this is for Windows malware, but the concept is the same).

## Source data

**Stage 1**

This type of data can be provided by logs from VirusTotal, Reversing Labs, Lockheed Martin's LAIKABOSS, Emerson's File Scanning Framework, Target's Strelka, or other file/malware analysis platforms.

* [VirusTotal API](https://developers.virustotal.com/v3.0/reference)
* [Emerson FSF](https://github.com/EmersonElectricCo/fsf)
* [Target Strelka](https://github.com/target/strelka)
* [Lockheed Martin LAIKABOSS](https://github.com/lmco/laikaboss)
* [LIEF Analysis Library](https://lief.quarkslab.com/doc/latest/api/python/macho.html)

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

**Stage 2**

There should be no breaking changes, depreciation strategies, or significant refactoring as this is creating a sub-field for the existing `file.` fieldset.

While likely not a large-scale ECS project, there would be documentation updates needed to explain the new fields.

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
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate the risk of churn and instability by resolving outstanding concerns.
-->

<!--
Stage 4: Document any new concerns and their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## Real-world implementations

<!--
Stage 4: Identify at least one real-world, production-ready implementation that uses these updated field definitions. An example of this might be a GA feature in an Elastic application in Kibana.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @peasead | author
* @devonakerr | sponsor
* @dcode, @peasead | subject matter expert

## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 1: https://github.com/elastic/ecs/pull/1097

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
