# 0042: Risk field extensions
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2023-07-13** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

This RFC seeks to extend the [existing risk fields](https://www.elastic.co/guide/en/ecs/current/ecs-risk.html) [(RFC 0031)](https://github.com/elastic/ecs/pull/2048) to support new/extended Risk Score investigation workflows. The workflows that this RFC intends to enable include all those described in 0031, along with the following:

1. Risk Score Explainability
  * We want to provide more insight into the anatomy of a risk score. The first (and simplest) way we intend to do this is by showing the documents (referred to commonly as Risk Inputs) that contributed to a particular risk score. Given that there may be a large number of these documents, we expect to have to choose a representative subset of these documents to persist along with the score (most obviously: top N riskiest inputs).
  * Since we cannot realistically persist the _entire_ contributing document along with the risk score (let alone several), we intend to persist just enough information to allow one to uniquely identify those documents at a later point in time (i.e. during investigation/analysis of a risk score), along with any information that would not be present on the original document (e.g. the document's calculated risk score).
2. Categorical Risk Scores
  * While the initial iteration of risk scoring ingested Detection Engine Alerts, we intend to expand risk scoring to include more data sources from multiple new categories of data. While we will still present a single risk score for most investigative purposes (composed of all these evaluated data sources), we believe that it will be useful to present individual risk scores _per category_ of data.
  * These categories (and their definitions) are still being discussed [in this internal ticket](https://github.com/elastic/security-team/issues/5485), we currently know that categories will have the following traits:
    * There will be a finite (<10) number of categories
    * These categories' definitions may be _extended_ in the future to include new data sources
  * Due to the above category traits, we need to come up with a naming convention for these categorical score fields that allows them to be extended without invalidating the existing field names.


<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

I'll enumerate the fields being introduced here grouped by their motivation/goal:

### Identifier Fields
These fields are intended to allow future extensibility of our concept of an "identifier." Currently, we leverage two such fields: `host.name` and `user.name`, to group documents for the purposes of risk scoring, but we definitely imagine this being extended in the future to allow multiple such fields for hosts and users, or more simply to allow administrators to configure fields other than those above. The presence of these two fields allows us to audit/explain how a particular risk score was identified.

* `id_field`
* `id_value`


### Risk Category Fields
Some of the context here was discussed in Stage 0; please read the above for that. More specifically, these fields seek to provide the category contributions to the score, and the number of risk inputs in that category, across each of the five proposed categories:

* `category_1_score`
* `category_1_count`
* `category_2_score`
* `category_2_count`
* `category_3_score`
* `category_3_count`
* `category_4_score`
* `category_4_count`
* `category_5_score`
* `category_5_count`

### Risk Explainability
Beyond the per-category explanations, these fields' purpose is to provide more insight/data for the analyst to further investigate the components of the risk score.

* `risk.inputs`
  * Generally, these objects are meant as a convenience for one investigating risk; they are the "most risky" inputs as determined by the risk engine, and serve as a shortcut to further investigation.
* `inputs.id`, `inputs.index`
  * These fields allow one to uniquely identify the original risk input document.
* `inputs.category`, `inputs.risk_score`
  * More "convenience" fields that could also be discovered in the original risk input document.
* `inputs.description`
  * These field is intended to be a precursor to what we are referring to as "Risk Reasons," which seek to aggregate/present multiple risk inputs in an easier to consume/analyze format.
* `notes`
  * Miscellaneous text field intended to provide more details that cannot be presented in the other fields.

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

We intend to leverage these new fields as part of the new implementation of the Risk Engine within Kibana. In fact, we have already written [the code that uses these fields](https://github.com/elastic/kibana/pull/161503/files#diff-75c9ad5c7d4b56459148fd9c08cb6cb229e932ea00f3e39725134ba429ad2915R66-R85), albeit not in the exact form described here. Beyond the existing ECS `risk` fields, the new implementation mainly seeks to improve explainability of individual risk scores.

## Source data

The new Risk Engine will initially use Detection Engine Alerts as inputs to its scoring mechanism. However, we intend also to allow ingestion from the other Risk Categories described here, provided that they conform to the appropriate schema. Said schema is outside of the scope of this RFC, but based on the current implementation all we will need are a `score` field and a `category` field in order to ingest any arbitrary document.

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

There are two broad concerns at this stage:

1. Category fields introducing a new "ordered" pattern
  * Rather than having either an array of objects, or an explicit `nested` field type, both of which allow an arbitrary number of items, we're instead opting to add 10 explicit fields (five explicit categories, each with two fields) under the _assumption_ that we won't extend the number of categories further. We have a bit of wiggle room (i.e. six categories, 12 fields wouldn't be out of question), but this is not a scalable solution if we need a large number of categories. However, that is only a potential future issue, and we can likely reevaluate and address it if/when it arises.
2. Mapping of `inputs` as a simple `object`
  * The biggest motivation for this choice is to avoid the performance/storage/syntax complexities that come with a `nested` mapping, but we also don't have any feature requirements that would currently necessitate `inputs` being `nested`.

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
* @SourinPaul | sponsor
* @ebeahan | reviewer


## References

* [existing risk fields](https://www.elastic.co/guide/en/ecs/current/ecs-risk.html)
* [previous risk fields RFC (stage 3)](https://github.com/elastic/ecs/pull/2048)
* [internal risk categories epic](https://github.com/elastic/security-team/issues/5485)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/2232
* Stage 1: https://github.com/elastic/ecs/pull/2236

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
