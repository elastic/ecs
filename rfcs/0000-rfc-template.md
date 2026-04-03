# 0000: Name of RFC
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging this RFC. -->

- Stage: **Proposal** <!-- Do not change. -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. -->
- Target maturity: **alpha | beta** <!-- Select one. See https://github.com/elastic/ecs/blob/main/docs/reference/ecs-principles-design.md#_field_stability -->

<!--
Remove these guidance comments as you fill out each section.
-->

## Summary

<!--
Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

## Fields

<!--
If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This is where proposed schema changes as standalone YAML files or extended example mappings and larger source documents should go.

Describe how this change affects fields. Include new or updated yml field definitions for all fields in this proposal. The list should be exhaustive and comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all fields and to provide a basis for adding the field definitions to the schema at the target maturity level. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

<!--
Identify practical sources for these fields in the real world (e.g. nginx access log) and include real world example source documents. Provide at least 2, but ideally 3. The goal here is to validate the utility of these field changes in the context of real world examples. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

## Scope of impact

<!--
Identify the scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

## Concerns

<!--
Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.

Document resolutions for all concerns. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* TBD | author

<!--
Who will be or has been consulted on the contents of this RFC? Identify authorship and sponsorship, and optionally identify the nature of involvement of others. Link to GitHub aliases where possible.

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

* Proposal: https://github.com/elastic/ecs/pull/NNN
