# 0000: Software Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **8-12-2022** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

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
| cpe | N/A | Common Platform Enumeration (CPE) is a standardized method of describing and identifying classes of applications, operating systems, and hardware devices present among an enterprise's computing assets.<br><br>IT management tools can collect information about installed products, identifying these products using their CPE names, and then use this standardized information to help make fully or partially automated decisions regarding the assets. For example, identifying the presence of XYZ Visualizer Enterprise Suite could trigger a vulnerability management tool to check the system for known vulnerabilities in the software, and also trigger a configuration management tool to verify that the software is configured securely in accordance with the organization's policies.
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

    - name: cpe
      level: custom
      type: keyword
      normalization: array
      example: ["cpe:/o:microsoft:windows", "cpe:/a:adobe:acrobat"]
      description: >
        Software identified by its common platform enumeration (CPE) value.
        
    - name: name
      level: custom
      type: keyword
      example: skype
      description: >
        The name of the software. 

    - name: modules.name
      level: custom
      type: keyword
      example: Anti-spyware protection
      description: >
        Module name. 

    - name: version
      level: custom
      type: keyword
      example: 27/1.0.0.2021090243
      description: >
        The software version.

    - name: add_on.name
      level: custom
      type: keyword
      example: Wiki
      description: >
        The name of the software add-on/extension that generated the event.

    - name: add_on.type
      level: custom
      type: keyword
      example: Bot
      description: > 
        The type of the software add-on/extension that generated the event.

    - name: add_on.url.full
      level: custom
      type: keyword
      example: https://example.com/download/my_add_on
      description: >
        Software installed on the host identified common platform enumeration (CPE) value.

    - name: family
      level: custom
      type: keyword
      example: TVD
      description: >
        A vendor provided categorization of the software.

    - name: vendor
      level: custom
      type: keyword
      example: google
      description: >
        The vendor or provider of the software.

    - name: type
      level: custom
      type: keyword
      example: exe
      description: >
        Software type.

    - name: state
      level: custom
      type: keyword
      example: running
      description: >
        Current state of the software.
    
    - name: patch.kb
      level: custom
      type: keyword
      example: KB4538461 
      description: >
        Software patch ID.

    - name: install.time
      level: custom
      type: date
      description: >
        Time the software was installed.

    - name: locale
      level: custom
      type: keyword
      example: Hungarian
      description: >
        The human language used in the application intended for the user to read.

    - name: patch.name
      level: custom
      type: keyword
      example: Microsoft.MicrosoftEdge.Stable.97.0.1072.55_neutral_8wekyb3d8bbwe
      description: >
        The software patch package's full name.

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
 - Endpoint Detection and Response System Audit Logs & Alerts
 - Office 365 Device Audit Logs
 - Active Directory Computer Objects
 - Windows Event Logs
 
 
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
 * Ingestion mechanisms
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->
 * Ingestion mechanisms
     - Custom 
 * Usage mechanisms (e.g. Kibana applications, detections)
     - Kibana
     - Custom applications

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
