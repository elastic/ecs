# 0031: Risk fields for multiple entities

- Stage: **3 (finished)**
- Date: **2022/09/08**

In 7.16, we released an experimental feature in the Security solution, called [Host Risk Score](https://www.elastic.co/guide/en/security/7.17/host-risk-score.html) to surface risky hosts in a customer environment. In 8.3, we released a similar feature called [User Risk Score](https://www.elastic.co/guide/en/security/current/user-risk-score.html) to expose at-risk users. As the two features mature, we want to further integrate them into the Security App, and enable users to perform filtering, sorting and enrichment based on the risk information. To that effect, we propose a reusable risk field set highlighting information like risk score, risk level etc., which could be used to express entity risk in the Security App.

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

## Usage

As mentioned previously, we currently have two experimental entity risk features in the Security App, namely Host Risk Score and User Risk Score. Host risk information can be viewed in [several locations](https://www.elastic.co/guide/en/security/8.4/host-risk-score.html#_additional_places_to_visualize_host_risk_score_data) in the Security App, including the Overview tab and the Hosts page.

User risk information can be found on the [Users page](https://www.elastic.co/guide/en/security/8.4/user-risk-score.html#view-user-risk-score) in the Security App.

Alerts are also being enriched with host and user risk information to help with alert investigation and triage.

With `risk` information available in multiple locations in the Security App, users can use it as an additional vector to filter, sort and correlate information within the Security App. For example, users will be able to start investigations by running queries like the following:
* "Show me the most critical and high-risk Windows hosts in my environment"
* "Show me the activity that contributed towards making Host X high-risk"
* "Show me the alerts corresponding to high-risk users in my environment"
* "Show me how the risk of User X changed over time"

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

The risk fields will be used to enrich alerts with entity risk information coming from internal systems such as host and user risk score, as well as external sources such as third-party threat intelligence feeds. An example of an alert document enriched with entity risk data from internal and external sources is provided in the RFC folder `0031`.

## Scope of impact

We have several views in the Security App where host and user risk information is displayed. These views will need to be updated to use the new ECS fields. Any new workflows built on top of host and user risk scores will also need to adopt these new fields. 

We currently have a small number (~60) of customer clusters that have deployed Host Risk Score in its experimental state. If these users were to upgrade to a Kibana version where the Security App uses the new ECS fields, they will also need to install the new Host Risk Score transforms and Lens dashboards. These users will also need to be informed that any views involving host risk in the Security App will cease to work on old (before upgrade) data.

A similar process will follow for customers who have already enabled User Risk Score.

## Concerns

We have an internal plan in place to port the Host and User Risk Score transforms, dashboards, and any existing host and user risk views in the Security App, to use the new ECS fields.

For existing users, migrate buttons on the host and user risk score cards on the Overview page will delete existing artifacts and re-install new ones. This migration strategy does not involve preserving historical risk data- this is left up to the user since the features are still experimental. However, we will be sure to communicate this clearly via documentation and in the UI.

We currently have two risk fields, `risk_score` and `risk_score_norm` that can be associated with `event` object. We will clarify this in the description for the new risk fields, stating that these new fields apply to entities only and should not be nested under the event object.

## People

The following are the people that consulted on the contents of this RFC.

* @ajosh0504 | author
* @ajosh0504 | sponsor

## References

* [About Host Risk Score](https://www.elastic.co/guide/en/security/8.4/host-risk-score.html)
* [About User Risk Score](https://www.elastic.co/guide/en/security/8.4/user-risk-score.html)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1740

* Stage 1: https://github.com/elastic/ecs/pull/1744

* Stage 2: https://github.com/elastic/ecs/pull/2027

* Stage 3: https://github.com/elastic/ecs/pull/2048
