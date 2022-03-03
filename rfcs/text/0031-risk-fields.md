# 0031: Risk fields for multiple entities

- Stage: **1 (draft)**
- Date: **2022/01/27**

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->
In 7.16, we released an experimental feature in the Security solution, called [Host Risk Score](https://www.elastic.co/guide/en/security/7.17/host-risk-score.html). Initially, the requirement of the feature was limited to surfacing risky hosts in a customer environment. As the feature matures, we want to further integrate it into the Security solution, and be able to perform filtering and sorting operations based on the risk information. Furthermore, there's also work currently in progress for a User Risk Score functionality, which will highlight users at risk within the Security solution. Both these features (and potentially others) currently could benefit from having a reusable risk field set highlighting information like risk score, risk level, contributors to risk etc.

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
The `risk` fields being proposed are as follows:

Field | Type | Example | Description | Use Case
-- | -- | -- | -- | -- 
risk.calculated_score_norm | float | 88.73 | A risk classifications core (0-100) calculates by an internal system as part of entity analytics and entity risk scoring | Can be used to indicate the risk associated with a particular host
risk.calculated_level | keyword | High | A risk classification level calculated by an internal system as part of entity analytics and entity risk scoring | Can be used to indicate the risk associated with a particular host
risk.static_score_norm | float | 83.0 | A risk classification score (0-100) obtained from outside the system, such as from some external Threat Intelligence Platform | Can be used to indicate the projected risk of a particular host based on a trusted third party intelligence feed 
risk.static_level | keyword | High | A risk classification level obtained from outside the system, such as from some external Threat Intelligence Platform | Can be used to indicate the projected risk of a particular host based on a trusted third party intelligence feed
risk.factors| object | See Source data section | Factors that contributed to the risk | Explainability about what contributed to the risk
risk.factors.alerts | array of objects (Optional) | See Source data section | Alerts that contributed to the risk | Explainability about what contributed to the risk
risk.factors.others | array of strings (Optional) | See Source data section | Factors apart from alerts that contributed to the risk | Explainability about what contributed to the risk

### Nesting `risk.*` fields under other fields
The `risk.*` fields mentioned above can be used to quantify the amount of risk associated with entities like hosts, users etc. For example, a host with a high risk score would imply that the probability of the host being exposed to harm during a cyber attack or breach is high. Attaching risk to entities can help analysts identify entities that require their immediate attention and hence drive investigations in a more systematic manner.

To begin with, the `risk.*` fields could be nested under the existing `host.*` and `user.*` fields, since hosts and users tend to be important entities during investigations.

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->
As mentioned previously, we have released an experimental feature called Host Risk Score in the Security solution recently. As of 7.16, the feature has some real estate on the Overview page and the Alert Flyout within the Security solution, as documented [here](https://www.elastic.co/guide/en/security/8.0/host-risk-score.html). In 8.1, users will also be able to see host risk information on the Hosts page and Host Details page as well. 

In addition to Host Risk Score, there is work currently in progress to introduce a Users page in the Security solution and a User Risk Scoring capability. Entities at risk is a new concept for users of the Security solution. Defining and normalizing this concept of entity risk using the `risk` fields will be crucial for users to get the most out of the Host and User Risk Scoring capabilities when they go GA.

Furthermore, these `risk` fields will provide users with an additional vector to filter, sort and correlate information within the Security solution. For example, users will be able to start investigations by running queries like the following:
* "Show me the most critical and high-risk Windows hosts in my environment"
* "Show me the activity that contributed towards making Host X high-risk"
* "Show me how the risk of Host X changed over time"
* "Show me Critical and high-risk users on Host X"


## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->
The Host and User Risk Score views in the Security solution are/will be backed by indices produced as a result of running [transforms](https://www.elastic.co/guide/en/elasticsearch/reference/current/put-transform.html) on a variety of data sources, not limited to the alerts data streams. An example document produced by the Host Risk Score transform in the absence of ECS `risk` fields looks as follows:

```
{
  "risk_stats": {
    "rule_risks": [
      {
        "rule_id": "c7ce36c0-32ff-4f9a-bfc2-dcb242bf99f9",
        "rule_name": "Unusual File Modification by dns.exe",
        "rule_risk": 73
      },
      {
        "rule_id": "343a0b6b-71bb-4a8c-a7a7-afcdfc4df019",
        "rule_name": "Unusual Windows Path Activity [Duplicate]",
        "rule_risk": 2.4057357238464423
      },
      {
        "rule_id": "43b68103-7eda-4687-9c0d-31308837a082",
        "rule_name": "Anomalous Windows Process Creation [Duplicate]",
        "rule_risk": 2.4057357238464423
      },
      {
        "rule_id": "99cb72b7-ab55-4375-8bbe-696e3e1b8fe2",
        "rule_name": "Unusual Windows Path Activity",
        "rule_risk": 2.4057357238464423
      },
      {
        "rule_id": "c3324b51-6d64-47e6-b220-2daa421e0468",
        "rule_name": "Unusual Process For a Windows Host [Duplicate]",
        "rule_risk": 21
      }
    ],
    "risk_score": 78.61701409613882,
    "risk_multipliers": [
      "Host is a server",
      "Tactic TA0001"
    ]
  },
  "risk": "High"
}
```

With the introduction of ECS `risk` fields, fields in the above document would look as follows:

```
{
  "risk": {
    "factors": {
      "alerts": [
        {
          "rule_id": "c7ce36c0-32ff-4f9a-bfc2-dcb242bf99f9",
          "rule_name": "Unusual File Modification by dns.exe",
          "rule_risk": 73
        },
        {
          "rule_id": "343a0b6b-71bb-4a8c-a7a7-afcdfc4df019",
          "rule_name": "Unusual Windows Path Activity [Duplicate]",
          "rule_risk": 2.4057357238464423
        },
        {
          "rule_id": "43b68103-7eda-4687-9c0d-31308837a082",
          "rule_name": "Anomalous Windows Process Creation [Duplicate]",
          "rule_risk": 2.4057357238464423
        },
        {
          "rule_id": "99cb72b7-ab55-4375-8bbe-696e3e1b8fe2",
          "rule_name": "Unusual Windows Path Activity",
          "rule_risk": 2.4057357238464423
        },
        {
          "rule_id": "c3324b51-6d64-47e6-b220-2daa421e0468",
          "rule_name": "Unusual Process For a Windows Host [Duplicate]",
          "rule_risk": 21
        }
      ],
      "others": [
        "Host is a server",
        "Tactic TA0001"
      ]
    },
    "calculated_risk_score_norm": 78.61701409613882,
    "calculated_risk_level": "High"
  }
}
```
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
Events and detection rules in the Security solution already have a risk score and/or severity associated with them. We might need to update these assets to use the new `risk` fieldset, otherwise it might potentially get confusing for users. 

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @ajosh0504 | author
* @ajosh0504 | sponsor

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

* Stage 0: https://github.com/elastic/ecs/pull/1740

* Stage 1: https://github.com/elastic/ecs/pull/1744
