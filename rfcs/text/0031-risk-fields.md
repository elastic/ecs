# 0031: Risk fields for multiple entities

- Stage: **2 (candidate)**
- Date: **2022/08/15**

In 7.16, we released an experimental feature in the Security solution, called [Host Risk Score](https://www.elastic.co/guide/en/security/7.17/host-risk-score.html). Initially, the requirement of the feature was limited to surfacing risky hosts in a customer environment. As the feature matures, we want to further integrate it into the Security solution, and be able to perform filtering and sorting operations based on the risk information. Furthermore, there's also work currently in progress for a User Risk Score functionality, which will highlight users at risk within the Security solution. Both these features (and potentially others) currently could benefit from having a reusable risk field set highlighting information like risk score, risk level, contributors to risk etc.

<!--
Stage X: Provide a brief explanation of why the proposal is being marked as abandoned. This is useful context for anyone revisiting this proposal or considering similar changes later on.
-->

## Fields

The `risk` fields being proposed are as follows:

Field | Type | Example | Description | Use Case
-- | -- | -- | -- | -- 
risk.calculated_score | float | 880.73 | A risk classification score calculated by an internal system as part of entity analytics and entity risk scoring | Can be used to indicate the risk associated with a particular host
risk.calculated_score_norm | float | 88.73 | A risk classification score calculated by an internal system as part of entity analytics and entity risk scoring, and normalized to a range of 0 to 100 | Can be used to indicate the risk associated with a particular host
risk.static_score | float | 830.0 | A risk classification score obtained from outside the system, such as from some external Threat Intelligence Platform | Can be used to indicate the projected risk of a particular host based on a trusted third party intelligence feed
risk.static_score_norm | float | 83.0 | A risk classification score obtained from outside the system, such as from some external Threat Intelligence Platform, and normalized to a range of 0 to 100 | Can be used to indicate the projected risk of a particular host based on a trusted third party intelligence feed 
risk.calculated_level | keyword | High | A risk classification level calculated by an internal system as part of entity analytics and entity risk scoring | Can be used to indicate the risk associated with a particular host
risk.static_level | keyword | High | A risk classification level obtained from outside the system, such as from some external Threat Intelligence Platform | Can be used to indicate the projected risk of a particular host based on a trusted third party intelligence feed

### Nesting `risk.*` fields under other fields

The `risk.*` fields mentioned above can be used to quantify the amount of risk associated with entities like hosts, users etc. For example, a host with a high risk score would imply that the probability of the host being exposed to harm during a cyber attack or breach is high. Attaching risk to entities can help analysts identify entities that require their immediate attention and hence drive investigations in a more systematic manner.

To begin with, the `risk.*` fields could be nested under the existing `host.*` and `user.*` fields, since hosts and users tend to be important entities during investigations.

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

As mentioned previously, we have released an experimental feature called Host Risk Score in the Security solution recently. As of 7.16, the feature has some real estate on the Overview page and the Alert Flyout within the Security solution, as documented [here](https://www.elastic.co/guide/en/security/8.0/host-risk-score.html). In 8.1, users will also be able to see host risk information on the Hosts page and Host Details page as well. 

In addition to Host Risk Score, there is work currently in progress to introduce a Users page in the Security solution and a User Risk Scoring capability. Entities at risk is a new concept for users of the Security solution. Defining and normalizing this concept of entity risk using the `risk` fields will be crucial for users to get the most out of the Host and User Risk Scoring capabilities when they go GA.

Furthermore, these `risk` fields will provide users with an additional vector to filter, sort and correlate information within the Security solution. For example, users will be able to start investigations by running queries like the following:
* "Show me the most critical and high-risk Windows hosts in my environment"
* "Show me the activity that contributed towards making Host X high-risk"
* "Show me how the risk of Host X changed over time"
* "Show me Critical and high-risk users on Host X"


## Source data

* Host Risk Score Transform
* User Risk Score Transform
* Security Alerts 
* [Potential] Data sources related to other assets

### Host Risk Score Transform

An example of a mapped document produced by the host risk score transform is as follows:

```json
{
  "host": {
    "name": "My-PC",
    "risk": {
      "rule_risks": [
        {
          "rule_id": "499a4611-1a4b-11ed-bb53-ad8c26f4d942",
          "rule_name": "Malicious Behavior Prevention Alert: Regsvr32 Scriptlet Execution",
          "rule_risk": 73
        },
        {
          "rule_id": "499a4611-1a4b-11ed-bb53-ad8c26f4d942",
          "rule_name": "Malicious Behavior Prevention Alert: Remote File Execution via MSIEXEC",
          "rule_risk": 73
        },
        {
          "rule_id": "499a4611-1a4b-11ed-bb53-ad8c26f4d942",
          "rule_name": "Malicious Behavior Prevention Alert: Script Execution via Microsoft HTML Application",
          "rule_risk": 73
        }
      ],
      "calculated_score_norm": 96.68615013176895,
      "multipliers": [
        "Host is a server"
      ],
      "calculated_level": "Critical"
    }
  },
  "ingest_timestamp": "2022-08-15T16:32:16.142561766Z",
  "@timestamp": "2022-08-12T14:45:36.171Z"
}
```

### User Risk Score Transform

An example of a mapped document produced by the user risk score transform is as follows:

```json
{
  "user": {
    "name": "random-user",
    "risk": {
      "rule_risks": [
        {
          "rule_id": "499a4611-1a4b-11ed-bb53-ad8c26f4d942",
          "rule_name": "Malicious Behavior Prevention Alert: Regsvr32 Scriptlet Execution",
          "rule_risk": 73
        },
        {
          "rule_id": "499a4611-1a4b-11ed-bb53-ad8c26f4d942",
          "rule_name": "Malicious Behavior Prevention Alert: Remote File Execution via MSIEXEC",
          "rule_risk": 73
        },
        {
          "rule_id": "499a4611-1a4b-11ed-bb53-ad8c26f4d942",
          "rule_name": "Malicious Behavior Prevention Alert: Script Execution via Microsoft HTML Application",
          "rule_risk": 73
        }
      ],
      "calculated_score_norm": 96.68615013176895,
      "calculated_level": "Critical"
    }
  },
  "ingest_timestamp": "2022-08-15T16:32:16.142561766Z",
  "@timestamp": "2022-08-12T14:45:36.171Z"
}
```

### Alerts

The risk fields can be used to enrich alerts with risk information coming from internal systems such as host and user risk score, as well as external sources such as third-party threat intelligence feeds. An example of an alert document enriched with risk data from internal and external sources is provided in the RFC folder `0031`.

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

## Scope of impact

We have several views (Hosts page, Overview page, Alerts flyouts) in the Security Solution which are populated by the Host and User Risk Score indices. These views will need to be updated to use the new ECS fields. Any new workflows built on top of Host Risk Score will also need to adopt these new fields. 

We currently have a small number (<50) of customer clusters that have deployed Host Risk Score in its experimental state. If these users were to upgrade to a Kibana version where the Security App uses these ECS fields, they will have to recreate the Host Risk Score transforms, and index mappings. These users will also need to be informed that any host risk-related views in the Security App will cease to work on old (before upgrade) data.    

## Concerns

Certain views in the Security App will not work on older data for current users of Host Risk Score. Users will need to recreate the Host Risk Score transforms and related index mappings.   

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @ajosh0504 | author
* @ajosh0504 | sponsor

## References

<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1740

* Stage 1: https://github.com/elastic/ecs/pull/1744

* Stage 2: https://github.com/elastic/ecs/pull/2027
