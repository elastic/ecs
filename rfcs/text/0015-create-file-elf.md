# 0015: Create the ELF sub-field of the File fieldset

- Stage: **3 (candidate)**
- Date: **2021-12-07**

Create the Executable Linkable Format (ELF) sub-field, of the `file` top-level fieldset. This document metadata can be used for malware research, as well as coding and other application development efforts.

## Fields

**Stage 0**

This RFC is to create the ELF sub-field within the `file.` fieldset. This will include 25 sub-fields.

| Name | Type | Description |
| ---- | ---- | ----------- |
| elf.creation_date | date | Extracted when possible from the file's metadata. Indicates when it was built or compiled. It can also be faked by malware creators. |
| elf.exports | flattened | List of exported element names and types. |
| elf.exports.name | keyword | Name of exported symbol |
| elf.exports.type | keyword | Type of exported symbol |
| elf.segments | nested | ELF object segment list. |
| elf.segments.type | keyword | ELF object segment type. |
| elf.segments.sections | keyword | ELF object segment sections. |
| elf.header | group | Header information of the ELF file. |
| elf.header.class | keyword | Header class of the ELF file. |
| elf.header.data | keyword | Data table of the ELF header. |
| elf.header.machine | keyword | Machine architecture of the ELF header. |
| elf.header.os_abi | keyword | Application Binary Interface (ABI) of the Linux OS. |
| elf.header.type | keyword | Header type of the ELF file. |
| elf.header.version | keyword | Version of the ELF header. |
| elf.header.abi_version | keyword | Version of the ELF Application Binary Interface (ABI). |
| elf.header.entrypoint | long | Header entrypoint of the ELF file. |
| elf.header.object_version | keyword | "0x1" for original ELF files. |
| elf.imports | flattened | List of imported element names and types. |
| elf.imports.name | keyword | Name of imported symbol |
| elf.imports.type | keyword | Type of imported symbol |
| elf.packers | keyword | Packers used for the ELF file. |
| elf.sections | nested | Section information of the ELF file. |
| elf.sections.flags | keyword | ELF Section List flags. |
| elf.sections.name | keyword | ELF Section List name. |
| elf.sections.physical_offset | keyword | ELF Section List offset. |
| elf.sections.type | keyword | ELF Section List type. |
| elf.sections.physical_size | long | ELF Section List physical size. |
| elf.sections.virtual_address | long | ELF Section List virtual address. |
| elf.sections.virtual_size | long | ELF Section List virtual size. |
| elf.sections.entropy | float | Shannon entropy calculation from the section. |
| elf.sections.chi2 | float | Chi-square probability distribution of the section. |
| elf.shared_libraries | keyword | List of shared libraries used by this ELF object |
| elf.telfhash | keyword | telfhash hash for ELF files. |
| elf.architecture | keyword | Machine architecture of the ELF file. |
| elf.byte_order | keyword | Byte sequence of ELF file. |
| elf.cpu_type | keyword | CPU type of the ELF file. |


**Stage 1**

[New `elf.yml` candidate](../schemas/elf.yml)

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage


In performing file analysis, specifically for malware research, understanding file similarities can be used to chain together malware samples and families to identify campaigns and possibly attribution. Additionally, understanding how malware components are re-used is useful in understanding malware telemetry, especially in understanding the impact being made through the introduction of defensive countermeasures.

As an example, if XDR vendors deploys a new malware model to defeat a specific type of ransomware and we start observing a change and/or relationship to the headers, import tables, libraries, etc of that malware family, we can make assumptions that the changes to the malware model are making an impact against the malware family.

As another example, tracking file metadata for specific families is useful in predicting new campaigns if we see similar file metadata being used for new samples. [Example](https://www.bleepingcomputer.com/news/security/maze-ransomware-is-shutting-down-its-cybercrime-operation/), the Maze ransomware family shutting down and re-purposing as Egregor (this is for Windows malware, but the concept is the same).

## Source data

**Stage 1**

This type of data can be provided by logs from VirusTotal, Reversing Labs, Lockheed Martin's LAIKABOSS, Emerson's File Scanning Framework, Target's Strelka, or other file/malware analysis platforms.

* [Elastic Threat Intel Filebeat Module](https://www.elastic.co/guide/en/beats/filebeat/master/filebeat-module-threatintel.html)
* [VirusTotal Filebeat module PR](https://github.com/elastic/beats/pull/21815)
* [VirusTotal API](https://developers.virustotal.com/v3.0/reference)
* [Emerson FSF](https://github.com/EmersonElectricCo/fsf)
* [Target Strelka](https://github.com/target/strelka)
* [Lockheed Martin LAIKABOSS](https://github.com/lmco/laikaboss)

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

**Stage 2**

### Real world examples
<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->
```
"file": {
  "elf": {
    "packers": [
      "upx"
    ],
    "header": {
      "object_version": "0x1",
      "data": "2's complement, little endian",
      "os_abi": "UNIX - Linux",
      "machine": "Advanced Micro Devices X86-64",
      "entrypoint": 4846016,
      "abi_version": 0,
      "type": "EXEC (Executable file)",
      "version": "1 (current)",
      "class": "ELF64"
    },
    "segments": [
      {
        "type": "LOAD",
        "sections": []
      },
      {
        "type": "LOAD",
        "sections": []
      }
    ]
  }
}
```
```
"file": {
  "elf": {
    "header": {
      "object_version": "0x1",
      "data": "2's complement, little endian",
      "machine": "Intel 80386",
      "os_abi": "UNIX - System V",
      "entrypoint": 0,
      "abi_version": 0,
      "type": "DYN (Shared object file)",
      "class": "ELF32",
      "version": "1 (current)"
    },
    "segments": [
      {
        "type": "PHDR",
        "sections": []
      },
      {
        "type": "LOAD",
        "sections": []
      },
      {
        "type": "LOAD",
        "sections": []
      },
      {
        "type": "DYNAMIC",
        "sections": []
      },
      {
        "type": "GNU_EH_FRAME",
        "sections": []
      },
      {
        "type": "GNU_STACK",
        "sections": []
      },
      {
        "type": "GNU_RELRO",
        "sections": []
      }
    ]
  }
}
```

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

**Stage 2**

There should be no breaking changes, depreciation strategies, or significant refactoring as this is creating a sub-field for the existing `file.` fieldset.

* Ingestion mechanism - Elastic Threat Intel Filebeat module (https://www.elastic.co/guide/en/beats/filebeat/master/exported-fields-threatintel.html), Elastic VirusTotal Live Hunt Filebeat module (https://github.com/elastic/beats/pull/21815)
* Usage mechanisms - threat hunting, file analysis, identifying file similarities

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
    # https://github.com/elastic/ecs/tree/master/docs/usage#usage-docs
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

**ELF Imports**

Type flattened won't allow explicit field mappings to be defined, so I don't think it's necessary to explicitly list them here. However, is there intent to still describe for data sources on how to "shape" the data for these flattened fields? There are no type: flattened fields today in ECS, so how to best capture provide that type of guidance will need to be hashed out.

* Field: `elf.imports`
* Comment: https://github.com/elastic/ecs/pull/1077#discussion_r572274291, https://github.com/elastic/ecs/pull/1294#pullrequestreview-618911963


## People

The following are the people that consulted on the contents of this RFC.

* @peasead | author
* @devonakerr | sponsor
* @dcode, @peasead | subject matter expert

## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 1: https://github.com/elastic/ecs/pull/1077
* Stage 2: https://github.com/elastic/ecs/pull/1294
  * Stage 2 advancement date correction: https://github.com/elastic/ecs/pull/1409
* Stage 3: https://github.com/elastic/ecs/pull/nnnn