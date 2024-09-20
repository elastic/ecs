# 0000: Event Entities

- Stage: **0 (strawperson)**
- Date: **TBD**


This RFC proposes enhancements to the Elastic Common Schema (ECS) to improve how we capture actor and target information in events, particularly for security use cases. The proposal aims to address current limitations in representing and querying this information, especially for cloud-based events (but this is broadly applicable).

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

Field | Type | Description /Usage
-- | -- | -- 
source.entity.id | keyword | All the entity identifiers that triggered the event. If the document contains multiple source entities, identifiers belonging to different entities will be present. Example identifiers include cloud resource IDs, ARNs, email addresses, or hostnames.
target.entity.id | keyword | All the entity identifiers that were affected by the event. If the document contains multiple target entities, identifiers belonging to different entities will be present. Example identifiers include cloud resource IDs, ARNs, email addresses, or hostnames.


### Proposed Changes
- Extend source.entity.id to capture actor information within the existing source.* fields.
- Introduce a new top-level target.* field set to explicitly represent the target of an action.
- Allow nesting of entity fields under target.*, such as target.user, target.entity, and target.group.
- Provide guidelines for consistently mapping common cloud event information (like role names, instance IDs, etc.) to these standardized fields.
<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

Currently, ECS lacks a standardized way to explicitly capture/distinguish between the actor (entity performing an action) and the target (entity being acted upon) in events. This limitation makes it challenging to represent certain security events accurately and consistently across different data sources and cloud providers. Specific issues include:

1. Difficulty in querying nested JSON objects containing critical information.
2. Inconsistent data structures across different services and API calls.
3. Field length limitations preventing effective searching and filtering.
4. Challenges in correlating related events involving the same actors or targets.

These issues are exemplified in the AWS CloudTrail integration (see [Issue #9586](https://github.com/elastic/integrations/issues/9586) and [Issue #10818](https://github.com/elastic/integrations/issues/10818)), but are not limited to AWS and likely affect other cloud providers and services.

What we expect to gain with this proposal:

- Improved clarity and consistency in representing security events across different platforms and data sources.
- Enhanced ability to query and analyze events without relying on complex string parsing or wildcard searches.
- Better correlation of related events, particularly in cloud environments with complex identity and access management scenarios.
- Avoidance of field length limitations by extracting key information into separate fields.
- Improved capability for creating effective detection rules and performing security analysis.
- Maintains compatibility with existing ECS structure while expanding capabilities.

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

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

- Asymmetry between using source.* for actor and target.* for target

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

* @romulets | author
* @tinnytintin10 | sponsor, subject matter expert
* @terrancedejesus | subject matter expert

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

* Stage 0: https://github.com/elastic/ecs/pull/2384

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->