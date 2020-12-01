# 0008: Cyber Threat Intelligence Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1 (proposal)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2020-11-09** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

Elastic Security Solution will be adding the capability to ingest, process and utilize threat intelligence information for increasing detection coverage and helping analysts making quicker investigation decisions. Threat intelligence can be collected from a number of sources with a variety of structured and semi-structured data representations. This makes threat intelligence an ideal candidate for ECS mappings. Threat intelligence data will require ECS mappings to normalize it and make it usable in our security solution. This RFC is focused on identifying new field sets and values that need to be created for threat intelligence data. Existing ECS field reuse will be prioritized where possible. If new fields are required we will utilize [STIX Cyber Observable data model](https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_mlbmudhl16lr) as guidance.

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

  * threat.time_first_seen
    _The date and time when intelligence souce first reported sighting this indicator._
  * threat.time_last_seen
    _The date and time when intelligence source last reported sighting this indicator._
  * threat.sightings
    _Number of times this indicator was observed conducting threat activity._
  * threat.type
    _Type of indicator as reprsented by Cyber Observable in STIX 2.0_
  * threat.description
    _Describes the type of action conducted by the threat._
  * threat.tlp
    _Traffic Light Protocol, which dictates sharing policies_
  * threat.classification
    _Describes type of threat delivery (Hacktool etc.) and family name.
  * threat.scanner_stats
    _Count of Anti virus/EDR that successfully detected malicious file or URL. Sources like VirusTotal, Reversing Labs often provide these statistics._
  * threat.confidence
    _The confidence rating of the threat, ranging from 0 - 100, following STIX 2.0 confidence rating _ 

### Proposed New Values

  * event.kind:enrichment _Propose adding this value to capture outcome of this event. It could also appy to other types of contextual data such as directory services, IPAM data, asset lists._
  * event.category:threat _Proposed threat.type field would be a subcategory for this value of event.category_
  * event.type:indicator _Proposed value represents type of threat information. In future this could be extended to other STIX 2.0 Standard Data Objects like Actor, Infrastucture etc._

### Existing ECS Fields For Nested Use in Threat.*

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

The additions to threat.* fields and nested use will be used to represent data collected threat intelligence sources. A new rule type Indicator match will be introduced in 7.10 and ECS threat fields will enable a new category of detection alerts that matches incoming log and event data against threat intelligence sources and generates an alert. Additionally in the future we will be able to enrich events and alerts with context from threat intelligence to assist analysts in their investigative workflows.

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

There are many sources of threat intelligence including open source, closed source and membership based ISAC's. Depending on the source the level of details can vary from atomic indicators of compromise (IoC) to higher order context around threat tactics, infrastructure and motivations. Generally freely available (open source) intelligence sources will provide details more focused on IoC's and commercial intelligence services will provide higher order details.

These sources typically provide intelligence that can be downloaded through REST API or in some cases downloadable CSV's or text files. These intelligence sources will update their data repositories at varying intervals.

Some examples of open source intelligence are:
  * [Abuse.ch Feodo Tracker](https://feodotracker.abuse.ch/downloads/ipblocklist.csv) - see below for sample data
  * [Phish Tank](https://www.phishtank.com/)

Some examples of commercial intelligence include:
  * [Anomali ThreatStream](https://www.anomali.com/products/threatstream)
  * [Virus Total](https://www.virustotal.com/gui/intelligence-overview)
  * [Domain Tools](https://www.domaintools.com/products/api-integration/)

#### Abuse.ch Feodo Tracker

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
There is a proposal to nest all IoC fields under `threat.ioc.*` instead of the current `threat.* structure.` This would make it consistent with taxonomy structure for `threat.tactic.*` and `threat.techinique.*` . This needs to be resovled in Stage 2 of the RFC process.

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

[Threat Intel Field Set Draft](https://docs.google.com/spreadsheets/d/1hS3tF-sGmwnKb7uUGLo3Rng_q6EFgwo6UCae8Sp4E-g/edit?usp=sharing)
<!-- Insert any links appropriate to this RFC in this section. -->

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/986
* Stage 1: https://github.com/elastic/ecs/pull/1037
  * Stage 1 correction: https://github.com/elastic/ecs/pull/1100

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
