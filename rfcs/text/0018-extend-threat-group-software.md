# 0018: Extend Threat Fieldset
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **0 (strawperson)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **TBD** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

Currently the `threat` fieldset includes tactic, technique, and sub-techniques from the ATT&CK framework. ATT&CK also includes groups and software that we can easily add to the existing fieldset to include all of the ATT&CK framework. While these fields are directly referenced within the ATT&CK framework, they can also be used with other frameworks if `threat.framework` expands to use more than ATT&CK.

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

### Proposed New Fields for Threat fieldset

Field | Type | Example | Description
--- | --- | --- | ---
threat.software.id | keyword | S0552 | Software is a generic term for custom or commercial code, operating system utilities, open-source software, or other tools used to conduct behavior modeled in ATT&CK. This is the software identification number assigned by MITRE ATT&CK.
threat.software.name | keyword | AdFind | Software is a generic term for custom or commercial code, operating system utilities, open-source software, or other tools used to conduct behavior modeled in ATT&CK. This is the software name assigned by MITRE ATT&CK.
threat.software.platforms | keyword | Windows | Software is a generic term for custom or commercial code, operating system utilities, open-source software, or other tools used to conduct behavior modeled in ATT&CK. This is the software platform assigned by MITRE ATT&CK.
threat.software.reference | keyword | https://attack.mitre.org/software/S0552/ | Software reference URL assigned by MITRE for this code, OS utility, open source software, or tool used to conduct behavior modeled in ATT&CK.
threat.software.type | keyword | Tool | Software is a generic term for custom or commercial code, operating system utilities, open-source software, or other tools used to conduct behavior modeled in ATT&CK. This is the software type assigned by MITRE ATT&CK.
threat.group.id | keyword | G0037 | Groups are sets of related intrusion activity that are tracked by a common name in the security community. This is the group identification number assigned by MITRE ATT&CK.
threat.group.name | keyword | FIN6 | Groups are sets of related intrusion activity that are tracked by a common name in the security community. This is the group name assigned by MITRE ATT&CK.
threat.group.reference | keyword | https://attack.mitre.org/groups/G0037/ | Group reference URL for a set of related intrusion activity that are tracked by a common name in the security community.

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

These fields can be used to associate fields that already exist in the `threat.*` fieldset, such as tactic, technique, and sub-technique. ATT&CK has relationships built within their framework for software and groups as it relates to tactic, technique, and sub-techniques. This information will provide for a more enriched threat profile for indicators and events.

Currently, tactic, technique, and sub-techniques are also included in rules for the Detection Engine, adding software and groups would make for more contextually relevant alerts that could aid in analysis and response operations.

```json5
{
// Existing threat fields
    "threat.framework": "ATT&CK",
    "threat.tactic.id": "TA0007",
    "threat.tactic.name": "Discovery",
    "threat.tactic.reference": "https://attack.mitre.org/tactics/TA0007/",
    "threat.technique.id": "T1087",
    "threat.technique.name": "Account Discovery",
    "threat.technique.reference": "https://attack.mitre.org/techniques/T1087/",
    "threat.technique.subtechnique.id": "T1087.002",
    "threat.technique.subtechnique.name": "Domain Account",
    "threat.technique.subtechnique.reference": "https://attack.mitre.org/techniques/T1087/002/",

// New Software fields
    "threat.software.id": "S0552",
    "threat.software.name": "AdFind",
    "threat.software": {
      "platforms": [
        "Windows",
        "Azure AD"
      ]
    },
    "threat.software.reference": "https://attack.mitre.org/software/S0552/",
    "threat.software.type": "Tool",

// New Group fields
    "threat.group.id": "G0037",
    "threat.group.name": "FIN6",
    "threat.group.reference": "https://attack.mitre.org/groups/G0037/"
}
```

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
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

* @peasead | author
* @devonakerr | sponsor
* @peasead | subject matter expert
* @dcode | subject matter expert

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

[AdFind Software](https://attack.mitre.org/software/S0552/)
[FIN6 Group](https://attack.mitre.org/groups/G0037/)
[Discovery Tactic](https://attack.mitre.org/tactics/TA0007/)
[Account Discovery Technique](https://attack.mitre.org/techniques/T1087/)
[Account Discovery: Domain Account Sub Technique](https://attack.mitre.org/techniques/T1087/002/)

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1300

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
