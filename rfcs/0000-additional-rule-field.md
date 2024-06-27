# 0000: Additional Rule Field
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->


<<<<<<< HEAD
=======
<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->
This RFC proposes addition of 2 new fields (rule.tags and rule.remediation) in rule fieldset to the Elastic Common Schema (ECS). The goal of these fields is to provide more context to the users in the rule fieldset, rule.tags will be used to track the set of tags applied to the rule, customers can use it to indicate metadata about the rule, and rule.remediation will be used to capture the remediation instructions associated with rules, it is generally provided by the benchmark or framework from which the rule is published. 
>>>>>>> 8ee34ce1711cf2650998fffac178295a89396c56

<!--
Stage 0: 
Proposal is to add 2 new fields in the ECS Rule fieldset, to extend the scope of this fieldset to incorporate tags and remediation information. Current fieldset does not support these two pieces of information. 
Detailed discussion in this EPIC- https://github.com/elastic/security-team/issues/7658
-->


## Fields

<<<<<<< HEAD
=======
The `rule` fields being proposed are as follows:

Field | Type | Description /Usage
-- | -- | -- 

rule.remediation | array | Used to capture remediation instructions that come from the benchmark / framework the rule is from 

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->
>>>>>>> 8ee34ce1711cf2650998fffac178295a89396c56

The `rule` fields being proposed are as follows:

Field | Type | Example | Description/Usage
-- | -- | -- 
rule.tags | array  | Used to track the set of tags applied to a rule | Customers can use it to indicate: author, benchmark partial name, rule number, rule category etc. It will be useful when we extend the capability to add more rules
rule.remediation | array | Enable encryption on all S3 buckets | Used to capture remediation instructions that come from the benchmark / framework the rule is from 



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

<<<<<<< HEAD
* @smriti0321 | author
* @tinnytintin10 | Product Manager
* @oren-zohar | Engineering Manager
* @orouz | Engineer
* @trisch-me | Security ECS team
=======
* @smriti0321 | author 
* @tinnytintin10 | Product Manager Cloud Security
* @oren-zohar | Engineering Manager Cloud Security
* @orouz | Engineer
>>>>>>> 8ee34ce1711cf2650998fffac178295a89396c56



## References

<!-- Insert any links appropriate to this RFC in this section. -->
* EPIC- https://github.com/elastic/security-team/issues/7658


### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/NNN

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
