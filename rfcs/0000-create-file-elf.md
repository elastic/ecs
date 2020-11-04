# 0000: Create the ELF sub-field of the File fieldset

- Stage: **0 (strawperson)**
- Date: **TBD**

Create the Executable Linkable Format (ELF) sub-field, of the `file` top-level fieldset. This document metadata can be used for malware research, as well as coding and other application development efforts.

## Fields

**Stage 0**

This RFC is to create the ELF sub-field within the `file.` fieldset. This will include 25 sub-fields.

| Name | Type | Description |
| ---- | ---- | ----------- |
| file.elf.creation_date | date | Extracted when possible from the file's metadata. Indicates when it was built or compiled. It can also be faked by malware creators. |
| file.elf.exports.name | keyword | Name of exported symbol |
| file.elf.exports.type | keyword | Type of exported symbol |
| file.elf.segment_list | keyword | ELF object segment list. |
| file.elf.header.class | keyword | Header class of the ELF file. |
| file.elf.header.data | keyword | Data table of the ELF header. |
| file.elf.header.machine | keyword | Machine architecture of the ELF header. |
| file.elf.header.os_abi | keyword | NEED TO ADD |
| file.elf.header.type | keyword | Header type of the ELF file. |
| file.elf.header.version | keyword | Version of the ELF header. |
| file.elf.header.abi_version | keyword | Version of the ELF Application Binary Interface (ABI). |
| file.elf.header.entrypoint | long | Header entrypoint of the ELF file. |
| file.elf.header.object_version | keyword | "0x1" for original ELF files. |
| file.elf.imports.name | keyword | Name of imported symbol |
| file.elf.imports.type | keyword | Type of imported symbol |
| file.elf.number_program_headers | long | Number of ELF Program Headers. |
| file.elf.number_section_headers | long | Number of ELF Section Headers. |
| file.elf.sections.flags | keyword | ELF Section List flags. |
| file.elf.sections.name | keyword | ELF Section List name. |
| file.elf.sections.physical_offset | keyword | ELF Section List offset. |
| file.elf.sections.section_type | keyword | ELF Section List type. |
| file.elf.sections.size | long | ELF Section List size. |
| file.elf.sections.virtual_address | long | ELF Section List virtual address. |
| file.elf.shared_libraries | keyword | List of shared libraries used by this ELF object |
| file.elf.telfhash | keyword | telfhash hash for ELF files. |


**Stage 1**  

[New `elf.yml` candidate](../schemas/pe.yml)]

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

* [VirusTotal Filebeat module PR](https://github.com/elastic/beats/pull/21815)
* [VirusTotal API](https://developers.virustotal.com/v3.0/reference)
* [Emerson FSF](https://github.com/EmersonElectricCo/fsf)
* [Target Strelka](https://github.com/target/strelka)
* [Lockheed Martin LAIKABOSS](https://github.com/lmco/laikaboss)

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

**Stage 2**

### VirusTotal Filebeat Module

```json
- name: file.elf
  default_field: false
  description: >
    ELF events from VirusTotal Intelligence Live Hunt results.
  overwrite: true
  type: group
  release: beta
  fields:
    - name: creation_date
      default_field: false
      description: >
        extracted when possible from the file's metadata. Indicates when it was
        built or compiled. It can also be faked by malware creators.
      type: date
    - name: header
      default_field: false
      description: >
        Header information of the ELF file.
      release: beta
      type: group
      fields:
        - name: class
          description: >
            Header class of the ELF file.
          type: keyword
        - name: data
          description: >
            Data table of the ELF header.
          type: keyword
        - name: machine
          description: >
            Machine architecture of the ELF header.
          type: keyword
        - name: os_abi
          description: >
            NEED TO ADD
          type: keyword
        - name: type
          description: >
            Header type of the ELF file.
          type: keyword
        - name: version
          description: >
            Version of the ELF header.
          type: keyword
        - name: abi_version
          type: keyword
          description: >
            Version of the ELF Application Binary Interface (ABI).
        - name: entrypoint
          format: string
          type: long
          description: >
            Header entrypoint of the ELF file.
        - name: object_version
          type: keyword
          description: >
            "0x1" for original ELF files.

    - name: number_program_headers
      description: >
        Number of ELF Program Headers.
      type: long
    - name: number_section_headers
      description: >
        Number of ELF Section Headers.
      type: long
    - name: sections
      default_field: false
      description: >
        Section information of the ELF file.
      release: beta
      type: group
      fields:
        - name: flags
          description: >
            ELF Section List flags.
          type: keyword
        - name: name
          description: >
            ELF Section List name.
          type: keyword
        - name: physical_offset
          description: >
            ELF Section List offset.
          type: keyword
        - name: section_type
          description: >
            ELF Section List type.
          type: keyword
        - name: size
          description: >
            ELF Section List size.
          format: bytes
          type: long
        - name: virtual_address
          description: >
            ELF Section List virtual address.
          format: string
          type: long
    - name: exports
      description: >
        List of exported element names and types
      release: beta
      type: group
      fields:
        - name: name
          description: >
            Name of exported symbol
          type: keyword
          default_field: false
        - name: type
          description: >
            Type of exported symbol
          type: keyword
          default_field: false
    - name: imports
      description: >
        List of imported element names and types
      release: beta
      type: group
      fields:
        - name: name
          description: >
            Name of imported symbol
          type: keyword
          default_field: false
        - name: type
          description: >
            Type of imported symbol
          type: keyword
          default_field: false
    - name: shared_libraries
      description: >
        List of shared libraries used by this ELF object
      type: keyword
    - name: telfhash
      description: >
        telfhash hash for ELF files.
      type: keyword
    - name: flattened
      default_field: false
      description: >
        Flattened ELF events from VirusTotal Intelligence Live Hunt results.
      release: beta
      type: group
      fields:
        - name: segment_list
          description: >
            ELF object segment list.
          type: flattened
```

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
* @dcode | subject matter expert

## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1077

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
