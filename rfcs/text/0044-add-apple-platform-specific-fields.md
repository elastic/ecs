# 0044: Apple Platform specific fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (Candidate)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date:  **2024-09-11** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->


### Summary
This RFC proposes the addition of Apple platform-specific fields to the ECS schema. This enhancement will enable security software vendors to more accurately map out data, particularly for Apple platforms.

The following feelds needs to be considered being added:

## Fields

##### Proposed New Fields for Process object

Field | Type | Example | Description
--- | --- | --- | ---
responsible	| keyword	| Terminal.app	| The responsible process on macOS, from an ancestry perspective, is the process that originally launched or spawned a given process.
platform_binary	| boolean	| true	| Indicates wethether this process executable is a default platform binary shipped with the operating system.
endpoint_security_client	| boolean	| true	| Indicates wethether this process executable is an Endpoint Security client.

##### Proposed New Fields for Code Signature object

Field | Type | Example | Description
--- | --- | --- | ---
flags	| string	| 570522385	| The flags used to sign the process.

##### Proposed New Fields for Hash object

Field | Type | Example | Description
--- | --- | --- | ---
cdhash	| keyword	| 3783b4052fd474dbe30676b45c329e7a6d44acd9	| The Code Directory (CD) hash of an executable

##### Proposed New Fields for Device object

Field | Type | Example | Description
--- | --- | --- | ---
serial_number	| keyword	| DJGAQS4CW5	| The unique serial number serves as a distinct identifier for each device, aiding in inventory management and device authentication.

### Motivation

As the number of Apple endpoints in enterprises grows, having the right fields to map data becomes increasingly valuable. This enables security researchers using Elastic, particularly those focusing on macOS, to query data more effectively by leveraging enriched data sets.

## Usage

As a developer at Jamf, working on the Elastic integration for Jamf Protect, our goal is to map as many fields as possible, especially as Jamf specializes in Apple platform security. While developing the integration, we've identified some gaps related to mapping events to ECS.

These new fields offer versatile methods. For instance, they facilitate querying process executions by platform binaries or endpoint security clients without requiring specific identifiers. The added hash fields are particularly valuable for tracking the hash of an application bundle alongside the hash of the executable in the directory itself, while the others are self-explanatory.

## Source data

This data originates from Endpoint Security software operating on a macOS host and can be transmitted through various methods, including an Elastic Agent and as example the use of the Jamf Protect integration, which supports AWS S3 or HTTPs.

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

# Scope of impact

As this RFC involves the creation of new fields, no breaking
changes are envisaged. Some existing tooling might need updates to factor in the
new fieldset's availability, however.

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

<!--## Concerns

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

* txhaflaire | author
* mjwolf | reviewer
* trisch-me | reviewer
* jamiehynds | subject matter expert

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

https://developer.apple.com/documentation/endpointsecurity/es_process_t/3228978-is_es_client

https://developer.apple.com/documentation/endpointsecurity/es_process_t/3228979-is_platform_binary

https://developer.apple.com/documentation/endpointsecurity/es_process_t/3684982-responsible_audit_token

https://developer.apple.com/documentation/endpointsecurity/es_process_t/3334987-codesigning_flags

https://developer.apple.com/documentation/endpointsecurity/es_process_t/3228976-cdhash

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/2338
* Stage 2: https://github.com/elastic/ecs/pull/2370

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
