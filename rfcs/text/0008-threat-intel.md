# 0008: Cyber Threat Intelligence Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (proposal)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2020-11-09** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

Elastic Security Solution will be adding the capability to ingest, process and utilize threat intelligence information for increasing detection coverage and helping analysts make quicker investigation decisions. Threat intelligence can be collected from a number of sources with a variety of structured and semi-structured data representations. This makes threat intelligence an ideal candidate for ECS mappings. Threat intelligence data will require ECS mappings to normalize it and make it usable in our security solution. This RFC is focused on identifying new field sets and values that need to be created for threat intelligence data. Existing ECS field reuse will be prioritized where possible. If new fields are required we will utilize [STIX Cyber Observable data model](https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_mlbmudhl16lr) as guidance.

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

## Fields

<!--
Stage 1: Describe at a high level how this change affects fields. Which fieldsets will be impacted? How many fields overall? Are we primarily adding fields, removing fields, or changing existing fields? The goal here is to understand the fundamental technical implications and likely extent of these changes. ~2-5 sentences.
-->

### Proposed New Fields for Threat fieldset

Field | Type | Example | Description
--- | --- | --- | ---
threat.ioc.time_first_seen | date | 2020-12-01 | The date and time when intelligence source first reported sighting this indicator
threat.ioc.time_last_seen | date | 2020-12-02| The date and time when intelligence source last reported sighting this indicator.
threat.ioc.sightings | long | 20 | Number of times this indicator was observed conducting threat activity
threat.ioc.type | keyword | IPV4 | Type of indicator as represented by Cyber Observable in STIX 2.0
threat.ioc.description | wildcard | 201.10.10.90 was seen delivering Angler EK | Describes the type of action conducted by the threat
threat.marking.tlp | keyword | RED | Data markings represent restrictions, permissions, and other guidance for how data can be used and shared. Examples could be TLP (White, Green, Amber, Red).
threat.ioc.scanner_stats | long | 4 | Count of Anti virus/EDR that successfully detected malicious file or URL. Sources like VirusTotal, Reversing Labs often provide these statistics.

### Proposed New Values for Event Fieldset

Field | New Value | Description
--- | --- | ---
event.kind | enrichment | Propose adding this value to capture the type of information this event contains and how it should be used. Threat intelligence will be used to enrich source events and signals. Enrichment could also appy to other types of contextual data sources (not just threat intelligence) such as directory services, IPAM data, asset lists.
event.category | threat | Propose adding this value to represent a new category of event data
event.type | indicator | Propose adding this value to be used as a sub-bucket of `event.category` to represent type of threat information. In future this could be extended to other STIX 2.0 Standard Data Objects like Actor, Infrastucture etc.
  
### Using existing Event Fieldset
Field | Type | Example | Description
--- | ---| --- | ---
event.reference | keyword | https://feodotracker.abuse.ch/ | URL to the intelligence source
event.dataset | keyword | Feodo tracker | name of specific dataset from the intelligence source. Intelligence sources often provide multiple datasets - IP blocklist, File hash blocklist etc.
event.provider | keyword | Abuse.ch | name of intelligence provider
event.severity | long | 7 | severity provided by threat intelligence source
event.risk_score | float | 10 | risk score provided by threat intelligence source
event.original | keyword | 2020-10-29 19:16:38,181.120.29.49,80,2020-11-02,Heodo | raw intelligence event
 

### Using existing ECS Fields to store IOC information

  * file.*
  * file.hash.*
  * url.*
  * user.*
  * registry.*
  * as.*
  * host.*
  * network.*
  * x509.*
  * pe.*
  * source.*
  * destination.*

<!--
Stage 2: Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting.
-->

<!--
Stage 3: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting.
-->

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

The additions described above will be used to enable cyber threat intelligence capabilities in Elastic Security solution. A new rule type Indicator match will be introduced in 7.10 and the proposed ECS updates will enable a new category of detection alerts that match incoming log and event data against threat intelligence sources. Additionally in the future we will also develop enrichment flows that add context from threat intelligence to alerts and events to assist analysts in their investigative workflows.

There are two primary uses for these fields.

1. *Storing threat intelligence as an event document in threat index(s).* Threat intelligence data will be collected from multiple sources stored in threat indices. The ECS fields proposed here will be used to structure the documents collected from various sources. 

2. *Adding threat intelligence match/enrichment to another document which could be in a source event index or signals index.* The Indicator Match Rule will be used to generate signals when a match occurs between a source event and threat intelligence document. The ECS fields proposed here will be used to add the enrichment and threat intel context in the signal document. 

### Proposed enrichment pipeline mechanics pseudocode

1. Original document completes its standard pipeline for the given source (i.e. filebeat module pipeline)
2. Original document is sent to "threat lookup" pipeline
3. For each indicator type, we perform the following (a file sha256 for example):
    - if exists "file.hash.sha256":
        - enrich processor:
            "policy_name": "file-sha256-policy",
            "field" : "file.hash.sha256",
            "target_field": "threat_match",
            "max_matches": "1"
        - policy file-sha256-policy:
            "match": {
                "indices": "threat-*",
                "match_field": "file.hash.sha256",
                "enrich_fields": ["event", "file", "ioc", "malware", "threat_actor"]
            }
    - rename:
        field: "threat_match.file"
        target: "threat_match.ioc.file"
    - set:
        field: "theat_match.matched"
        value: "sha256"
    - append:
        field: "threat"
        value: "{{ threat_match }}"
    - remove:
        field: "threat_match"

**NOTE**: There may be some optimization on which enrichments we attempt based upon the event categorization fields. For instance, we know that data that presents the netflow model or "interface" doesn't contain a sha256 hash. Since those categorization fields are lists, if data presented as both netflow and file (for whatever reason), then we'd check both network-related lookups and file-related lookups

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

There are many sources of threat intelligence including open source, closed source and membership based ISAC's. Depending on the source the level of details can vary from atomic indicators of compromise (IoC) to higher order context around threat tactics, infrastructure and motivations. Generally freely available (open source) intelligence sources will provide details more focused on IoC's and commercial intelligence services will provide higher order details.

These sources typically provide intelligence that can be downloaded through REST API or in some cases downloadable CSV's or text files. These intelligence sources will update their data repositories at varying intervals.

#### Abuse.ch Feodo Tracker
This dataset from Abuse.ch provides a list of botnet C&C servers associated with the Feodo malware family (Dridex, Emotet).
```
# Firstseen,DstIP,DstPort,LastOnline,Malware
2020-10-29 19:16:38,181.120.29.49,80,2020-11-02,Heodo
2020-10-29 19:16:35,190.45.24.210,80,2020-11-02,Heodo
2020-10-29 19:16:32,109.242.153.9,80,2020-11-02,Heodo
2020-10-29 19:16:28,169.1.39.242,80,2020-11-02,Heodo
2020-10-29 19:14:24,201.171.244.130,80,2020-11-02,Heodo
2020-10-29 19:14:20,64.207.182.168,8080,2020-11-02,Heodo
2020-10-29 19:14:19,173.173.254.105,80,2020-11-02,Heodo
2020-10-29 19:14:16,153.204.122.254,80,2020-10-30,Heodo
2020-10-29 19:14:13,201.163.74.203,80,2020-11-02,Heodo
```
<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->

#### Botvrij.eu

Freely available source of IOC's which includes Network IOCs, File Details, Email and Registry Key

```
cc2477cf4d596a88b349257cba3ef356 # md5 - AZORult spreads as a fake ProtonVPN installer (191)
573ff02981a5c70ae6b2594b45aa7caa # md5 - AZORult spreads as a fake ProtonVPN installer (191)
c961a3e3bd646ed0732e867310333978 # md5 - AZORult spreads as a fake ProtonVPN installer (191)
2a98e06c3310309c58fb149a8dc7392c # md5 - AZORult spreads as a fake ProtonVPN installer (191)
f21c21c2fceac5118ebf088653275b4f # md5 - AZORult spreads as a fake ProtonVPN installer (191)
0ae37532a7bbce03e7686eee49441c41 # md5 - AZORult spreads as a fake ProtonVPN installer (191)
974b6559a6b45067b465050e5002214b # md5 - AZORult spreads as a fake ProtonVPN installer (191)
7966c2c546b71e800397a67f942858d0 # md5 - This Is Not a Test: APT41 Initiates Global Intrusion Campaign Using Multiple Exploits (194)
5909983db4d9023e4098e56361c96a6f # md5 - This Is Not a Test: APT41 Initiates Global Intrusion Campaign Using Multiple Exploits (194)
3e856162c36b532925c8226b4ed3481c # md5 - This Is Not a Test: APT41 Initiates Global Intrusion Campaign Using Multiple Exploits (194)
659bd19b562059f3f0cc978e15624fd9 # md5 - This Is Not a Test: APT41 Initiates Global Intrusion Campaign Using Multiple Exploits (194)

```
#### AlienVault OTX

Rest Endpoint: `/api/v1/indicators/export`

Schema
```
{
  "$schema": "http://json-schema.org/draft-04/schema",
  "additionalProperties": false,
  "required": ["count", "next", "results", "previous"],
  "properties": {
    "count": {"type": "integer"},
    "next": {"type": ["string", "null"]},
    "results": {
        "type": "array", 
        "items": {
            "additionalProperties": false,
            "required": ["indicator", "title", "content", "type", "id", "description"],
            "properties": {
                "indicator": {"type": "string"},
                "title": {"type": ["string", "null"]},
                "content": {"type": ["string", "null"]},
                "type": {"type": "string"},
                "id": {"type": "integer"},
                "description": {"type": ["string", "null"]}
            }
        }
    },
    "previous": {"type": ["string", "null"]}
  } 
}
```

Example
```
{
    "count": 3,
    "next": null,
    "results": [
        {
            "indicator": "rustybrooks.com",
            "description": null,
            "title": null,
            "content": "",
            "type": "domain",
            "id": 1
        },
        {
            "indicator": "roll20.com",
            "description": null,
            "title": null,
            "content": "",
            "type": "domain",
            "id": 3
        },
        {
            "indicator": "redacted.ch",
            "description": null,
            "title": null,
            "content": "",
            "type": "domain",
            "id": 6
        }
    ],
    "previous": null
}
```
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
 * Ingestion mechanism: Primary ingestion mechanisms will be Filebeat modules and Ingest Packages. There will be no impact on ingestion mechanisms.
 * Usage mechanism: The primary use of the proposed ECS fields and values is through Elastic Security solution. In 7.10 we released Indicator match rule to support the use of the proposed new fields and values.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

1. Identified in Stage 1: There is a proposal to nest all IoC fields under `threat.ioc.*` instead of the current `threat.* structure.` This would make it consistent with taxonomy structure for `threat.tactic.*` and `threat.techinique.*`.
 * Proposed resolution: Nest all IoC fields under `threat.ioc.*`
2. How to use `event.module`
 * Proposed resolution: pending
3. How to best represent malware{name,family,type}. Current proposal is to use `threat.ioc.classification` to describe threat delivery (Hacktool etc.) and family name.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate the risk of churn and instability by resolving outstanding concerns.
-->

<!--
Stage 4: Document any new concerns and their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## Real-world implementations

<!--
Stage 4: Identify at least one real-world, production-ready implementation that uses these updated field definitions. An example of this might be a GA feature in an Elastic application in Kibana.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @shimonmodi | author
* @peasead | subject matter expert
* @MikePaquette | subject matter expert


## References

* [Threat Intel Field Set Draft](https://docs.google.com/spreadsheets/d/1hS3tF-sGmwnKb7uUGLo3Rng_q6EFgwo6UCae8Sp4E-g/edit?usp=sharing)
* [STIX Cyber Observable data model](https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_mlbmudhl16lr)

Some examples of open source intelligence are:
  * [Abuse.ch Feodo Tracker](https://feodotracker.abuse.ch/downloads/ipblocklist.csv) - see below for sample data
  * [Botvrij](https://botvrij.eu/data/)
  * [Phish Tank](https://www.phishtank.com/)
  * [AlienVault OTX](https://otx.alienvault.com/api)

Some examples of commercial intelligence include:
  * [Anomali ThreatStream](https://www.anomali.com/products/threatstream)
  * [Virus Total](https://www.virustotal.com/gui/intelligence-overview)
  * [Domain Tools](https://www.domaintools.com/products/api-integration/)
   
<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/986
* Stage 1: https://github.com/elastic/ecs/pull/1037
  * Stage 1 correction: https://github.com/elastic/ecs/pull/1100
* Stage 2: https://github.com/elastic/ecs/pull/1127

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
