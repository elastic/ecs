# 0000: Host Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **7-13-2022** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->
<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

 The host fields describe information about the host that is relevant to an event and extends the ECS host field set in several ways:

- The host field set supports additional host bios fields.
- The host field set supports additional host cpu fields.
- The host field set supports additional fields describing a supplemental details that the host can generate.
<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->
## Fields
<details><summary>Definitions</summary>
<p>

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->
Field Name | Special Instructions | Justification/Use Case
| :--: | :-- | :-- |
| memory | The numeric value is a base value for memory. The two character unit type represents a multiplication factor to determine actual memory. <br> <br>Normalize to byte value by multiplying base value by unit type as follows <br> <table>  <thead>  <tr>  <th>Unit</th>  <th>Multiplication Factor</th>  </tr>  </thead>  <tbody>  <tr>  <td>B</td>  <td><code>(2^0)    1</code></td>  </tr>  <tr>  <td>KB</td>  <td><code>(2^10)  1024</code></td> </tr>  <tr>  <td>MB</td>  <td><code>(2^20)  1,048,576</code></td> </tr>  <tr>  <td>GB</td>  <td><code>(2^30)  1,073,741,824</code></td>  </tr>  <tr>  <td>TB</td>  <td><code>(2^40)  1,099,511,627,776</code></td>  </tr>   </tbody>  </table>     | Detects specific baselines of physical configuration for asset management.
| last_logon.time | N/A | Login time tells the last time a user logged into the system, which may provide insights into events occurring on that system.|
| created | N/A | Indicates that device is known to domain.|
| distinguished_name | N/A | The distinguished name indicates ownership of the host. It uniquely identifies the host in an x509 certificate.|
| modified | N/A | Indicates when information has changed for the host in a directory service.|
| bios.manufacturer | Normalization: lower case | This is a string representing the system manufacturer of the host. Useful for supply chain issue detection.|
| bios.release_date | This date will need to be converted to a ECS date format. | The bios release date. Useful for supply chain issue detection.|
| bios.secure_boot_enabled | If disabled set to false; if enabled set to true. | Used to detect misconfiguration in Secure Boot.|
| bios.uuid | N/A | A unique identifier assigned to the computer mother board.|
| bios.version | N/A | Version of the BIOS, this string is created by the BIOS manufacturer. Useful for supply chain issue detection.|
| cpu.architecture | Normalize these entries to the following format:<br><instruction_bits>:<raw_string><br>"x64: x64-based PC"<br>"x64: x86_64"<br>"x32: x86-based PC" | Detects out of date CPUs.|
| cpu.core.count | N/A | Detects specific baselines of physical configuration for asset management.| 
| cpu.count | N/A | Detects specific baselines of physical configuration for asset management.|
| cpu.logical_processor.count | N/A | Detects specific baselines of physical configuration for asset management.|
| cpu.manufacturer | Note that a manufacturer is displayed for each CPU, select the first. Multiple manufacturers are not expected. | Useful for supply chain issue detection.|
| cpu.name | Normalize raw field into lowercase format for easier query | Useful for supply chain issue detection.|
| cpu.speed | Normalize to GHZ, do not round but use 0.28 etc, where required.| Detects specific baselines of physical configuration for asset management.|
 </p>
 </details>

    - name: memory
      level: custom
      type: unsigned long
      example: 17,179,869,184
      description: >
        Physical memory of the host machine in bytes.
        
    - name: last_logon.time
      level: custom
      type: date
      description: >
        The time of the last user logon to the host. The timestamp type represents date and time information using ISO 8601 format and is always in UTC time.

    - name: created
      level: custom
      type: date
      description: >
        Date and time of when the device was registered in the domain. 

    - name: distinguished_name
      level: custom
      type: keyword
      example: CN=foo, CN=computers, DC=acme, DC=company, DC=edu
      normalized: array
      description: >
        Distinguished name of the host.

    - name: modified
      level: custom
      type: date
      description: >
        Date the host's details were last modified.

    - name: bios.manufacturer
      level: custom
      type: keyword
      example: dell inc.
      description: > 
        This is a string representing the system manufacturer of the host.

    - name: bios.release_date
      level: custom
      type: date
      description: >
        The bios release date.

    - name: bios.secure_boot_enabled
      level: custom
      type: boolean
      description: >
        Indicator that Secure Boot is enabled on the computer.

    - name: bios.uuid
      level: custom
      type: keyword
      example: 4C4C4544-0056-5010-805A-CAC04F475132
      description: >
        A unique identifier assigned to the computer mother board.

    - name: bios.version
      level: custom
      type: keyword
      example: 1.6.13
      description: >
        Version of the BIOS. This string is created by the BIOS manufacturer.

    - name: cpu.architecture
      level: custom
      type: keyword
      example: "x64: x86_64"
      description: >
        The CPU architecture and raw string of the CPU provided by the OS.
    
    - name: cpu.core.count
      level: custom
      type: integer
      example: 10
      description: >
        Number of physical cores per CPU on host machine.

    - name: cpu.count
      level: custom
      type: integer
      example: 2
      description: >
        Number of CPUs on host machine.

    - name: cpu.logical_processor.count
      level: custom
      type: integer
      example: 40
      description: >
        Number of logical processors per CPU on host machine (physical cores multiplied by threads per core).

    - name: cpu.manufacturer
      level: custom
      type: keyword
      example: Intel
      description: >
        Manufacturer of CPU.

    - name: cpu.name
      level: custom
      type: keyword
      example: intel(r) core(tm) i3-2370m cpu
      description: >
        The full name of the cpu model.
    
    - name: cpu.speed
      level: custom
      type: float
      example: 2.21
      description: >
        Float type defining the speed of the CPU in GHZ with null and blank values stored as -1.0 and -2.0 respectively.

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->
 ### `memory`
 Detects specific baselines of physical configuration for asset management.
 
 ### `last_logon.time`
 Login time tells the last time a user logged into the system, which may provide insights into events occurring on that system.
 
 ### `created`
 Indicates that device is known to domain.
 
 ### `distinguished_name`
 The distinguished name indicates ownership of the host. It uniquely identifies the host in an x509 certificate.
 
 ### `modified`
 Indicates when information has changed for the host in a directory service.
 
 ### `bios.manufacturer`
 This is a string representing the system manufacturer of the host. Useful for supply chain issue detection.
 
 ### `bios.release_date`
 The bios release date. Useful for supply chain issue detection.
 
 ### `bios.secure_boot_enabled`
 Used to detect misconfiguration in Secure Boot.
 
 ### `bios.uuid`
 A unique identifier assigned to the computer mother board.
 
 ### `bios.version`
 Version of the BIOS, this string is created by the BIOS manufacturer. Useful for supply chain issue detection.
 
 ### `cpu.architecture`
 Detects out of date CPUs.
 
 ### `cpu.core.count`, `cpu.count`, `cpu.logical_processor.count`
 Detects specific baselines of physical configuration for asset management.
 
 ### `cpu.manufacturer`, `cpu.name`
 Useful for supply chain issue detection.
 
 ### `cpu.speed`
 Detects specific baselines of physical configuration for asset management.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->
The host fields in this RFC are sourced from the following data feeds: 
 - Host & Network Interface Information
 - Office 365 Device Audit Logs
 - Active Directory Computer Objects
 - Host Information
 
 
 Host & Network Interface Information collects information about host computer configurations, vulnerabilities and compliance from endpoint computers.
 
 Azure Active Directory (Azure AD) tracks user activity and creates reports that help you understand how your users access and use Azure AD services. The Microsoft Graph API for Azure AD provides a means to access data in the activity reports. 
 
 Active Directory (AD) stores information about objects on the network and makes this information available for administrators and users. AD uses a structured data store as the basis for a logical, hierarchical organization of directory information. This data store, also known as the directory, contains information about AD objects. These objects typically include shared resources such as Users, Computers, Groups, Organizational Units, etc.
 
 Host Information collects configuration and compliance data from endpoint computers.

 
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
 * Ingestion mechanisms (e.g. beats/logstash)
     - one
 * Usage mechanisms (e.g. Kibana applications, detections)
     - one
 * ECS project (e.g. docs, tooling)
     - one

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->
The term manufacturer is used here while in Elastic Common Schema the appropriate equivalent could be viewed as vendor which may lead to confusion.
<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @donneesdata | Author, Sponsor

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
