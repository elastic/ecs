# 0043: Risk Input fields

- Stage: **0 (strawperson)**
- Date: **2023-09-22** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

### Summary
This RFC aims to add a few general fields that, when defined on a document, will allow that document containing them to be consumed by Kibana's Risk Engine for the purposes of entity analytics.

Broadly, we need two fields to enable this behavior:

* `risk_score`, a "base" risk score (numeric, float) defined by the data producer that is used as the basis for calculating risk for the entity represented in the document
* `risk_category`, a keyword field defining to which of the five [proposed categories](https://github.com/elastic/ecs/pull/2236)

### Motivation
Kibana's Risk Engine (all iterations) currently only ingest Detection Engine Alerts. These are straightforward to score, as they contain:

* an inherent risk score field (`kibana.alert.risk_score`)
* an implicit category (`category_1`, which is described broadly as "Alerts")

These fields are meant to allow the Risk Engine logic to be generalized to allow ingestion of any document containing these proposed fields.


### Outstanding Questions/Concerns
1. If we have need to represent multiple entities within the same document (i.e. both a host and a user), a single set of top-level fields may not be sufficient. In that case, nesting them separately under `host` and `user` would be appropriate.
2. Related to the above, the fields proposed do not account for _multiple_ of either hosts or users within a single document. However, neither does the Risk Engine in general.
3. We currently leverage the presence of either `host.name` or `user.name` to find/aggregate/score entities. It would seem reasonable that, in the future, data producers could define additional/other fields from which to "identify" host and user entities, respectively. This concept is already partly codified in the `identifier_field` and `identifier_value` fields on a [Risk Score document](https://github.com/elastic/ecs/pull/2236), but while those are meant for "outgoing" risk score documents, these fields would be used by the Risk Engine to identify incoming Risk Input documents. For complete disambiguation, this may also necessitate an explicit "entity type" field on both sides of this process.


<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

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

* @rylnd | author
* @SourinPaul | Subject Matter Expert, Product Manager

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

* Risk Score Fields RFC (Stage 1): https://github.com/elastic/ecs/pull/2236
<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests


* Stage 0: https://github.com/elastic/ecs/pull/2244
