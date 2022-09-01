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
| name | N/A | Name of software often useful to cross reference other data sources.|
| modules.name | N/A | A module usually represents an application, a language stack, or any other logical collection of packages. Module name should represent the name of the software it ships.|
| version | N/A | Having the latest software version can prevent security issues and improve compatibility and program features. Software updates are necessary to keep computers, mobile devices and tablets running smoothly -- and they may lower security vulnerabilities.|
| add_on.name | N/A | Add-ons are usually third-party software and can affect the performance of your browser or applications and some can even be actively malicious. Keeping track of potentially hazardous add-ons that are impacting performance or acting malicious can allow for quick resolutions in order to minimize security concerns.|
| add_on.type | Use the AddonType Look up table (https://docs.microsoft.com/en-us/office/office-365-management-api/office-365-management-activity-api-schema#addontype) to transform Integer value to Member name. | Add-ons are usually third-party software and can affect the performance of your browser or applications and some can even be actively malicious. Keeping track of potentially hazardous add-ons that are impacting performance or acting malicious can allow for quick resolutions in order to minimize security concerns. The type field provides a means of understanding and correlation of events to types. |
| add_on.url.full | N/A | Add-ons are usually third-party software and can affect the performance of your browser or applications and some can even be actively malicious. Keeping track of potentially hazardous add-ons that are impacting performance or acting malicious can allow for quick resolutions in order to minimize security concerns. The url field provides a means of understanding and correlation of events to the location where the add_on can be download from.|
| family | N/A | Software product families have gained much important from the increased usage of software in consumer products. “A software product family is commonly defined to consist of a common architecture, a set of reusable assets used in systematically producing individual products, and the set of products thus produced”. One software product family normally has a very large number of products. The definition indicates that software components are reused on a common architecture because the products belonging to one family have a lot of common features and build upon a common architecture.|
| vendor | Normalize this field to lowercase. | Software vendors can develop a wide range of consumer and business applications for a variety of devices, from computers and tablets, to mobile phones, to automobiles, manufacturing equipment, and more. The applications developed by software vendors can be deployed on premise or, increasingly, are cloud based and can be accessed via the Internet.|
| type | Normalization rule: The value must be normalized to lower case. | Software packages are complete pieces of software that can work on their own, without additions or other necessary parts. Computer software packages control the physical parts of the machine so that these parts know how to work together. Other names for software are apps, programs, applications, program modules, procedures, scripts and source code. Computer software is adapted to the properties of the hardware. What works on one type of computer will not necessarily work on another. Some types of software are installed when a computer is built and are necessary for the computer to function. Other software packages can be purchased separately or downloaded from the Internet and added to the computer at any time.|
| state | N/A | Software state is information your program manipulates to accomplish some task. It is data or information that gets changed or manipulated throughout the runtime of a program. The "state" of a program at a given time refers to a snapshot of all the data the program is currently looking at or analyzing to get to the next step in it's execution.|
| patch.kb | Normalization rule: The value must be normalized to lower case. | Proper patch management can greatly improve an enterprise’s security by addressing the vulnerabilities in its software and operating systems. Keeping track of the patch ID allows for the administrator to ascertain any issues resulting from a specific patch update.| 
| install.time | N/A | Having the latest software version can prevent security issues and improve compatibility and program features. Software updates are necessary to keep computers, mobile devices and tablets running smoothly -- and they may lower security vulnerabilities.|
| locale | N/A | Knowing the software.locale makes it easier to translate and understand any instructions associated with the application.|
| patch.name | N/A | Good patch documentation including the software patch package's full name is important for letting the administrator easily identify and distinguish patches from each other.|
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
 ### `cpe`
 Common Platform Enumeration (CPE) is a standardized method of describing and identifying classes of applications, operating systems, and hardware devices present among an enterprise's computing assets.

IT management tools can collect information about installed products, identifying these products using their CPE names, and then use this standardized information to help make fully or partially automated decisions regarding the assets. For example, identifying the presence of XYZ Visualizer Enterprise Suite could trigger a vulnerability management tool to check the system for known vulnerabilities in the software, and also trigger a configuration management tool to verify that the software is configured securely in accordance with the organization's policies.
 
 ### `name`
 Name of software often useful to cross reference other data sources.
 
 ### `modules.name`
 A module usually represents an application, a language stack, or any other logical collection of packages. Module name should represent the name of the software it ships.
 
 ### `version`, `install.time`
 Having the latest software version can prevent security issues and improve compatibility and program features. Software updates are necessary to keep computers, mobile devices and tablets running smoothly -- and they may lower security vulnerabilities.
 
 ### `add_on.name`, `add_on.type`, `add_on.url.full`
 Add-ons are usually third-party software and can affect the performance of your browser or applications and some can even be actively malicious. Keeping track of potentially hazardous add-ons that are impacting performance or acting malicious can allow for quick resolutions in order to minimize security concerns.
 
 The type field provides a means of understanding and correlation of events to types.
 
 The url field provides a means of understanding and correlation of events to the location where the add_on can be download from.  
 
 ### `family`
 Software product families have gained much important from the increased usage of software in consumer products. “A software product family is commonly defined to consist of a common architecture, a set of reusable assets used in systematically producing individual products, and the set of products thus produced”. One software product family normally has a very large number of products. The definition indicates that software components are reused on a common architecture because the products belonging to one family have a lot of common features and build upon a common architecture.
 
 ### `vendor`
 Software vendors can develop a wide range of consumer and business applications for a variety of devices, from computers and tablets, to mobile phones, to automobiles, manufacturing equipment, and more. The applications developed by software vendors can be deployed on premise or, increasingly, are cloud based and can be accessed via the Internet.
 
 ### `type`
 Software packages are complete pieces of software that can work on their own, without additions or other necessary parts. Computer software packages control the physical parts of the machine so that these parts know how to work together. Other names for software are apps, programs, applications, program modules, procedures, scripts and source code. Computer software is adapted to the properties of the hardware. What works on one type of computer will not necessarily work on another. Some types of software are installed when a computer is built and are necessary for the computer to function. Other software packages can be purchased separately or downloaded from the Internet and added to the computer at any time.
 
 ### `state`
 Software state is information your program manipulates to accomplish some task. It is data or information that gets changed or manipulated throughout the runtime of a program. The "state" of a program at a given time refers to a snapshot of all the data the program is currently looking at or analyzing to get to the next step in it's execution.
 
 ### `patch.kb`
 Proper patch management can greatly improve an enterprise’s security by addressing the vulnerabilities in its software and operating systems. Keeping track of the patch ID allows for the administrator to ascertain any issues resulting from a specific patch update.
 
 ### `locale`
 Knowing the software.locale makes it easier to translate and understand any instructions associated with the application.
 
 ### `patch.name`
 Good patch documentation including the software patch package's full name is important for letting the administrator easily identify and distinguish patches from each other.

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
