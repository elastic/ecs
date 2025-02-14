# 0000: Additional Rule Field
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->



<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->
This RFC proposes addition of 1 new field (rule.remediation) in rule fieldset to the Elastic Common Schema (ECS). The goal of this field is to provide more context to the users in the rule fieldset, rule.remediation will be used to capture the remediation instructions associated with rules, it is generally provided by the benchmark or framework from which the rule is published. 



## Fields

The `rule` fields being proposed are as follows:

Field | Type | Example | Description/Usage
-- | -- | -- | --
rule.remediation | array | Enable encryption on all S3 buckets | Used to capture remediation instructions that come from the benchmark / framework the rule is from 



## Usage

<!--
The new remediation field will be used to track and manage remediation actions for compliance findings identified by the CIS benchmarks across AWS, GCP, and Azure environments. This field will help security teams to document the steps taken to address non-compliance issues, ensuring that all actions are recorded and can be audited. For example, if a CIS benchmark identifies that multi-factor authentication (MFA) is not enabled for all users, the remediation field will include details on how MFA was enabled and verified.

In practice, this field will be leveraged by security operations teams to ensure that all compliance gaps are addressed promptly and effectively. It will also be used by auditors to verify that the organization is adhering to security best practices and regulatory requirements. By having a standardized field for remediation, organizations can streamline their compliance processes and improve their overall security posture.

## Source data

<!--
Potential sources of data for the remediation field include:

AWS Config rules and AWS Security Hub findings
GCP Security Command Center findings
Azure Security Center and Azure Policy compliance data
-->

## Scope of impact

<!--
Currently this is achieved in product using a custom field, adding this new field will standardize the mapping for new and existing integrations. No major impact on Ingestion/ Kibana and Documentation expected.
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

* @smriti0321 | author
* @tinnytintin10 | Product Manager
* @oren-zohar | Engineering Manager
* @orouz | Engineer
* @trisch-me | Security ECS team




## References

<!-- Insert any links appropriate to this RFC in this section. -->



### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/NNN

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
