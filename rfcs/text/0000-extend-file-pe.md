# 0000: Extend the PE field set

- Stage: **1 (proposal)**
- Date: **TBD**

The Portable Executable (PE) sub-field, of the `file` top-level fieldset, can be updated to include more file attributes to aid in file analysis. This additional document metadata can be used for malware research, as well as coding and other application development efforts.

## Fields

This RFC is to create 25 additional sub-fields within the `file.pe` fieldset.

| Name | Type | Description |
| ---- | ---- | ----------- |
| file.pe.authentihash | keyword | Authentihash of the PE file. |
| file.pe.compile_timestamp | date | Compile timestamp of the PE file. |
| file.pe.compiler | wildcard | Name and version of the compiler. |
| file.pe.creation_date | date | Extracted when possible from the file's metadata. Indicates when it was built or compiled. It can also be faked by malware creators. |
| file.pe.entry_point | keyword | Entry point of the PE file. |
| file.pe.exports | keyword | List of symbols exported by PE |
| file.pe.debug | flattened | Debug information, if present |
| file.pe.import_list | flattened | List of all imported functions |
| file.pe.sections | flattened | Data about sections of compiled binary PE |
| file.pe.resource_details | flattened | If the PE contains resources, some info about them |
| file.pe.resource_languages | flattened | Digest of languages found in resources. Key is language (as string) and value is how many resources there are having that language (as integer) |
| file.pe.resource_types | flattened | Digest of resource types. Key is resource type (as string) and value is how many resources there are of that specific type (as integer) |
| file.pe.packers | flattened | Identifies packers used on Windows PE files by several tools and AVs. Keys are tool names and values are identified packers, both strings. See `file.pe.packers` for merged list of packers from all tools. |
| file.pe.machine_type | keyword | Machine type of the PE file. |
| file.pe.main_icon.hash.dhash | keyword | Difference Hash for a given PE file. |
| file.pe.main_icon.hash.md5 | keyword | MD5 hash of raw icon data |
| file.pe.overlay.chi2 | float | Chi2 information of the PE file. |
| file.pe.overlay.entropy | float | Entropy information of the PE file. |
| file.pe.overlay.filetype | keyword | Filetype of the PE file. |
| file.pe.overlay.md5 | keyword | Overlay MD5 hash of the PE file. |
| file.pe.overlay.offset | long | Offset of the overlay information of the PE file. |
| file.pe.overlay.size | long | Size of the PE file. |
| file.pe.overlay.rich_pe_header_hash | keyword | Hash of the header for the PE file. |
| file.pe.packers | keyword | Merged list of all detected packers by all tools used. |
| file.pe.rich_pe_header_hash | keyword | Hash of the PE header. |

[New `pe.yml` fields](pe/pe.yml)

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

In performing file analysis, specifically for malware research, understanding file similarities can be used to chain together malware samples and families to identify campaigns and possibly attribution. Additionally, understanding how malware components are re-used is useful in understanding malware telemetry, especially in understanding the impact being made through the introduction of defensive countermeasures.

As an example, if XDR vendors deploys a new malware model to defeat a specific type of ransomware and we start observing a change and/or relationship to the headers, import tables, packers, etc of that malware family, we can make assumptions that the changes to the malware model are making an impact against the malware family.

As another example, tracking file metadata for specific families is useful in predicting new campaigns if we see similar file metadata being used for new samples. [Example](https://www.bleepingcomputer.com/news/security/maze-ransomware-is-shutting-down-its-cybercrime-operation/), the Maze ransomware family shutting down and re-purposing as Egregor.

## Source data

This type of data can be provided by logs from VirusTotal, Reversing Labs, Lockheed Martin's LAIKABOSS, Emerson's File Scanning Framework, Target's Strelka, or other file/malware analysis platforms.

* [VirusTotal Filebeat module PR](https://github.com/elastic/beats/pull/21815)
* [VirusTotal API](https://developers.virustotal.com/v3.0/reference)
* [Emerson FSF](https://github.com/EmersonElectricCo/fsf)
* [Target Strelka](https://github.com/target/strelka)
* [Lockheed Martin LAIKABOSS](https://github.com/lmco/laikaboss)

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

There should be no breaking changes, depreciation strategies, or significant refactoring as this is extending the existing fieldset.

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

* [VirusTotal Filebeat module PR](https://github.com/elastic/beats/pull/21815)
* [VirusTotal API](https://developers.virustotal.com/v3.0/reference)
* [Emerson FSF](https://github.com/EmersonElectricCo/fsf)
* [Target Strelka](https://github.com/target/strelka)
* [Lockheed Martin LAIKABOSS](https://github.com/lmco/laikaboss)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 1: https://github.com/elastic/ecs/pull/1071

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
