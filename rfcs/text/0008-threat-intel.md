# 0008: Cyber Threat Intelligence Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **2 (draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-02-18** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

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
threat.indicator.first_seen | date | 2020-12-01 | The date and time when intelligence source first reported sighting this indicator
threat.indicator.last_seen | date | 2020-12-02| The date and time when intelligence source last reported sighting this indicator.
threat.indicator.sightings | long | 20 | Number of times this indicator was observed conducting threat activity
threat.indicator.type | keyword | ipv4-addr, domain-name, email-addr | Type of indicator as represented by Cyber Observable in STIX 2.0
threat.indicator.description | keyword | 201.10.10.90 was seen delivering Angler EK | Describes the type of action conducted by the threat
threat.indicator.dataset | keyword | threatintel.{abusemalware,abuseurl,misp,otx,limo} | Identifies the name of specific dataset from the intelligence source.
threat.indicator.module | keyword | threatintel | Identifies the name of specific module where the data is coming from.
threat.indicator.provider | keyword | Abuse.ch | Identifies the name of intelligence provider.
threat.indicator.confidence | keyword | High, 10, Confirmed by other sources, Certain, Almost Certain / Nearly Certain | Identifies the confidence rating assigned by the provider using STIX confidence scales (N/H/M/L, 0-10, Admirality, WEP, or DNI).
threat.indicator.ip | ip | 1.2.3.4 | Identifies a threat indicator as an IP address (irrespective of direction).
threat.indicator.domain | keyword | evil.com | Identifies a threat indicator as a domain (irrespective of direction).
threat.indicator.port | long | 443 | Identifies a threat indicator as a port number (irrespective of direction).
threat.indicator.email.address | keyword | phish@evil.com | Identifies a threat indicator as an email address (irrespective of direction).
threat.marking.tlp | keyword | RED | Data markings represent restrictions, permissions, and other guidance for how data can be used and shared. Examples could be TLP (WHITE, GREEN, AMBER, RED).
threat.indicator.scanner_stats | long | 4 | Count of Anti virus/EDR that successfully detected malicious file or URL. Sources like VirusTotal, Reversing Labs often provide these statistics.
threat.indicator.matched.atomic | keyword | 2f5207f2add28b46267dc99bc5382480 | Identifies the atomic indicator that matched a local environment endpoint or network event.
threat.indicator.matched.field | keyword | threat.indicator.ip | Identifies the field of the atomic indicator that matched a local environment endpoint or network event.
threat.indicator.matched.type | keyword | ipv4-addr, domain-name, email-addr, url | Identifies the type of the atomic indicator that matched a local environment endpoint or network event.

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
event.severity | long | 7 | severity provided by threat intelligence source
event.risk_score | float | 10 | risk score provided by threat intelligence source
event.original | keyword | 2020-10-29 19:16:38,181.120.29.49,80,2020-11-02,Heodo | raw intelligence event

### Using existing ECS Fields to store indicator information

Fieldset | Description | Reference
--- | --- | ---
File | Use existing File fields to describe file entity details involved in threat activity. No changes to existing ECS fieldset | [File Fields](https://www.elastic.co/guide/en/ecs/current/ecs-file.html)
Hash | Use existing Hash fields to describe file entity details involved in threat activity. Hash fields are expected to be nested at `file.hash` , `process.hash`. No changes to existing ECS fieldset | [Hash Fields](https://www.elastic.co/guide/en/ecs/current/ecs-hash.html)
URL | Use existing URL fields to describe internet resources involved in threat activity. No changes to existing ECS fieldset | [URL](https://www.elastic.co/guide/en/ecs/current/ecs-url.html)
Registry | Use existing Registry fields involved in threat activity. No changes to existing ECS fieldset | [Registry](https://www.elastic.co/guide/en/ecs/current/ecs-registry.html)
Autonomous System (AS) | Use existing fields to capture routing prefixes for threat activity. AS fields are expected to be nested at `source.as` , `destination.as`, or `threat.indicator`. Changes will be needed to existing fieldset to add `threat.indicator`. | [AS](https://www.elastic.co/guide/en/ecs/current/ecs-as.html)
Geographic | Use existing fields to capture geographic location for threat activity. Changes will be needed to the field reuse section to add `threat.indicator`. | [Geo](https://www.elastic.co/guide/en/ecs/current/ecs-geo.html)
x509 | Use existing fields to describe certificates involved in threat activity. No changes to existing fieldset. | [x509](https://www.elastic.co/guide/en/ecs/current/ecs-x509.html)
Portable Executable (PE) | Use existing fields to describe portable executables involved in threat activity. No changes to existing fieldset. | [PE](https://www.elastic.co/guide/en/ecs/current/ecs-pe.html)

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

1. **Storing threat intelligence as an event document in threat index(s).**

    Threat intelligence data will be collected from multiple sources stored in threat indices. The ECS fields proposed here will be used to structure the documents collected from various sources.

**Example**
```json5
{
    "@timestamp": "2019-08-10T11:09:23.000Z",
    "event.kind": "enrichment",
    "event.category": "threat",
    "event.type": "indicator",
    "event.provider": "Abuse.ch",
    "event.reference": "https://feodotracker.abuse.ch",
    "event.dataset": "threatintel.abusemalware",
    "event.module": "threatintel",

    // The top-level file object here allows expressing multiple indicators for a single file object
    "file.hash.sha256": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4",
    "file.hash.md5": "1eee2bf3f56d8abed72da2bc523e7431",
    "file.size": 656896,
    "file.name": "invoice.doc",

    // The indicator prefix here gives context of the indicators
    "indicator.marking.tlp": "WHITE",
    "indicator.time_first_seen": "2020-10-01",
    "indicator.time_last_seen": "2020-11-01",
    "indicator.sightings": "4",
    /* It's possible to have multiple related indicators in a given document,
       e.g. sha256, sha1, ssdeep, etc. If that's the case this should be an array
       of types (i.e. [sha1, sha256, ssdeep]) */
    "indicator.type": ["sha256", "md5", "file_name", "file_size"],
    "indicator.description": "file last associated with delivering Angler EK",

    // Filebeats and other fields, not part of ECS proposal
    "fileset.name": "abusemalware",
    "input.type": "log",
    "log.offset": 0,

    // Any indicators should also be copied to relevant related.* field
    "related": {
        "hash": [
            "1eee2bf3f56d8abed72da2bc523e7431",
            "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4"
        ]
    },
    "tags": [
        "threatintel",
        "forwarded"
    ],
}
```

2. **Adding threat intelligence match/enrichment to another document which could be in a source event index or signals index.**

    The Indicator Match Rule will be used to generate signals when a match occurs between a source event and threat intelligence document. The ECS fields proposed here will be used to add the enrichment and threat intel context in the signal document.

**Example**
```json5
{
    "process": {
        "name": "svchost.exe",
        "pid": 1644,
        "entity_id": "MDgyOWFiYTYtMzRkYi1kZTM2LTFkNDItMzBlYWM3NDVlOTgwLTE2NDQtMTMyNDk3MTA2OTcuNDc1OTExNTAw",
        "executable": "C:\\Windows\\System32\\svchost.exe"
    },
    "message": "Endpoint file event",
    "@timestamp": "2020-11-17T19:07:46.0956672Z",
    "file": {
        "path": "C:\\Windows\\Prefetch\\SVCHOST.EXE-AE7DB802.pf",
        "extension": "pf",
        "name": "SVCHOST.EXE-AE7DB802.pf",
        "hash": {
            "sha256": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4"
        }
    },
    "threat": {
        "indicator": [
            {
                // Each enrichment is added as a nested object under `threat.indicator.*`
                // Copy all the object indicators under `indicator.*`, providing full context
                "file": {
                    "hash": {
                        "sha256": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4",
                        "md5": "1eee2bf3f56d8abed72da2bc523e7431"
                    },
                    "size": 656896,
                    "name": "invoice.doc"
                },
                /* `matched` will provide context about which of the indicators above matched on this
                    particular enrichment. If multiple matches for this indicator object, this could
                    be a list */
                "matched": "sha256",
                "marking": {
                    "tlp": "WHITE"
                },
                "first_seen": "2020-10-01",
                "last_seen": "2020-11-01",
                "sightings": 4,
                "type": ["sha256", "md5", "file_name", "file_size"],
                "description": "file last associated with delivering Angler EK",

                // Copy event.* data from source threatintel document
                "provider": "Abuse.ch",
                "dataset": "threatintel.abusemalware",
                "module": "threatintel"
            }
        ]
    },
    // Tag the enriched document to indicate the threat enrichment matched
    "tags": [
        "threat-match"
    ],
    // This should already exist from the original ingest pipeline of the document
    "related": {
        "hash": [
            "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4"
        ]
    }
}
```

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
                "enrich_fields": ["event", "file", "indicator"]
            }
    - rename:
        field: "threat_match.file"
        target: "threat_match.indicator.file"
    - rename:
        field: "threat_match.event.provider"
        target: "threat_match.indicator.provider"
    - rename:
        field: "threat_match.event.dataset"
        target: "threat_match.indicator.dataset"
    - rename:
        field: "threat_match.event.module"
        target: "threat_match.indicator.module"
    - set:
        field: "threat_match.indicator.matched"
        value: "sha256"
    - append:
        field: "threat.indicator"
        value: "{{ threat_match.indicator }}"
    - remove:
        field: "threat_match"

**NOTE**: There may be some optimization on which enrichments we attempt based upon the event categorization fields. For instance, we know that data that presents the netflow model or "interface" doesn't contain a sha256 hash. Since those categorization fields are lists, if data presented as both netflow and file (for whatever reason), then we'd check both network-related lookups and file-related lookups

## Source data

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

There are many sources of threat intelligence including open source, closed source, and membership-based ISAC's. Depending on the source the level of details can vary from atomic indicators of compromise (IoC) to higher-order context around threat tactics, infrastructure, and motivations. Generally freely available (open source) intelligence sources will provide details more focused on indicators and commercial intelligence services will provide higher-order details.

These sources typically provide intelligence that can be downloaded through REST API or in some cases downloadable CSV's or text files. These intelligence sources will update their data repositories at varying intervals.

- Abuse.ch Malware - This dataset from Abuse.ch provides a list of malware hashes.
- Abuse.ch URL - This dataset from Abuse.ch provides a list of malware URLs.
- AlienVault OTX - This dataset from AlienVault provides a list of malware hashes, URLs, and IPs.
- Anomali Limo - This dataset from Anomali provides threat information from the Limo service.

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting.
-->

#### Abuse.ch Malware List
This dataset from Abuse.ch provides a list of malware hashes.
```
{"md5_hash":"7871286a8f1f68a14b18ae475683f724","sha256_hash":"48a6aee18bcfe9058b35b1018832aef1c9efd8f50ac822f49abb484a5e2a4b1f","file_type":"dll","file_size":"277504","signature":null,"firstseen":"2021-01-14 06:14:05","urlhaus_download":"https://urlhaus-api.abuse.ch/v1/download/48a6aee18bcfe9058b35b1018832aef1c9efd8f50ac822f49abb484a5e2a4b1f/","virustotal":null,"imphash":"68aea345b134d576ccdef7f06db86088","ssdeep":"6144:+60EDP6uCLfGw/GpxXinM1BCo1PlumGx2mx2tXd0t115JG5:X5DpBw/KViMTB1MnEWk0115JW","tlsh":"1344D022AD13DD37E1F400FCA6A58F8561626E381F00A89777D41F8A98356F1BB2B717"}
{"md5_hash":"7b4c77dc293347b467fb860e34515163","sha256_hash":"ec59538e8de8525b1674b3b8fe0c180ac822145350bcce054ad3fc6b95b1b5a4","file_type":"dll","file_size":"277504","signature":null,"firstseen":"2021-01-14 06:11:41","urlhaus_download":"https://urlhaus-api.abuse.ch/v1/download/ec59538e8de8525b1674b3b8fe0c180ac822145350bcce054ad3fc6b95b1b5a4/","virustotal":null,"imphash":"68aea345b134d576ccdef7f06db86088","ssdeep":"6144:+60EDP6uCLfGw/GpxXinM1BCo1PlumGx2mx2tXd0t115JGY:X5DpBw/KViMTB1MnEWk0115Jr","tlsh":"4E44D022AD13DD37E1F400FCA6A58F8561626E381F00A89777D41F8A98356F1BB2B717"}
{"md5_hash":"373d34874d7bc89fd4cefa6272ee80bf","sha256_hash":"b0e914d1bbe19433cc9df64ea1ca07fe77f7b150b511b786e46e007941a62bd7","file_type":"dll","file_size":"277504","signature":null,"firstseen":"2021-01-14 06:11:22","urlhaus_download":"https://urlhaus-api.abuse.ch/v1/download/b0e914d1bbe19433cc9df64ea1ca07fe77f7b150b511b786e46e007941a62bd7/","virustotal":{"result":"25 / 66","percent":"37.88","link":"https://www.virustotal.com/gui/file/b0e914d1bbe19433cc9df64ea1ca07fe77f7b150b511b786e46e007941a62bd7/detection/f-b0e914d"},"imphash":"68aea345b134d576ccdef7f06db86088","ssdeep":"6144:+60EDP6uCLfGw/GpxXinM1BCo1PlumGx2mx2tXd0t115JGG:X5DpBw/KViMTB1MnEWk0115Jd","tlsh":"7544D022AD13DD37E1F400FCA6A58F8561626E381F00A89777D41F8A98356F1BB2B717"}
```

#### Abuse.ch URL List
This dataset from Abuse.ch provides a list of botnet C&C servers associated with malware.
```
{"id":"961548","urlhaus_reference":"https://urlhaus.abuse.ch/url/961548/","url":"http://103.72.223.103:34613/Mozi.m","url_status":"online","host":"103.72.223.103","date_added":"2021-01-14 21:19:13 UTC","threat":"malware_download","blacklists":{"spamhaus_dbl":"not listed","surbl":"not listed"},"reporter":"lrz_urlhaus","larted":"false","tags":["elf","Mozi"]}
{"id":"961546","urlhaus_reference":"https://urlhaus.abuse.ch/url/961546/","url":"http://112.30.97.184:44941/Mozi.m","url_status":"online","host":"112.30.97.184","date_added":"2021-01-14 21:19:05 UTC","threat":"malware_download","blacklists":{"spamhaus_dbl":"not listed","surbl":"not listed"},"reporter":"lrz_urlhaus","larted":"false","tags":["elf","Mozi"]}
{"id":"961547","urlhaus_reference":"https://urlhaus.abuse.ch/url/961547/","url":"http://113.110.198.53:37173/Mozi.m","url_status":"online","host":"113.110.198.53","date_added":"2021-01-14 21:19:05 UTC","threat":"malware_download","blacklists":{"spamhaus_dbl":"not listed","surbl":"not listed"},"reporter":"lrz_urlhaus","larted":"false","tags":["elf","Mozi"]}
```

#### AlienVault OTX
This dataset from AlienVault provides a list of malware hashes, URLs, and IPs.
```
{"indicator":"86.104.194.30","description":null,"title":null,"content":"","type":"IPv4","id":1588938}
{"indicator":"90421f8531f963d81cf54245b72cde80","description":"MD5 of a5725af4391d21a232dc6d4ad33d7d915bd190bdac9b1826b73f364dc5c1aa65","title":"Win32:Hoblig-B","content":"","type":"FileHash-MD5","id":9751110}
{"indicator":"ip.anysrc.net","description":null,"title":null,"content":"","type":"hostname","id":16782717}
```

#### Anomali Limo
This dataset from Anomali provides threat information from the Limo service.
```
{"created":"2020-01-22T02:58:57.431Z","description":"TS ID: 55241332361; iType: mal_url; State: active; Org: Cloudflare; Source: CyberCrime","id":"indicator--44c85d4f-45ca-4977-b693-c810bbfb7a28","labels":["malicious-activity","threatstream-severity-medium","threatstream-confidence-76"],"modified":"2020-01-22T02:58:57.431Z","name":"mal_url: http://chol.cc/Work6/PvqDq929BSx_A_D_M1n_a.php","object_marking_refs":["marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"],"pattern":"[url:value = 'http://chol.cc/Work6/PvqDq929BSx_A_D_M1n_a.php']","type":"indicator","valid_from":"2020-01-22T02:58:57.431Z"}
{"created":"2020-01-22T02:58:57.503Z","description":"TS ID: 55241332307; iType: mal_url; State: active; Org: ServerMania; Source: CyberCrime","id":"indicator--f9fe5c81-6869-4247-af81-62b7c8aba209","labels":["malicious-activity","threatstream-severity-medium","threatstream-confidence-68"],"modified":"2020-01-22T02:58:57.503Z","name":"mal_url: http://worldatdoor.in/lewis/Panel/five/PvqDq929BSx_A_D_M1n_a.php","object_marking_refs":["marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"],"pattern":"[url:value = 'http://worldatdoor.in/lewis/Panel/five/PvqDq929BSx_A_D_M1n_a.php']","type":"indicator","valid_from":"2020-01-22T02:58:57.503Z"}
{"created":"2020-01-22T02:58:57.57Z","description":"TS ID: 55241332302; iType: mal_url; State: active; Org: SPRINTHOST.RU - shared/premium hosting, VDS, dedic; Source: CyberCrime","id":"indicator--b0e14122-9005-4776-99fc-00872476c6d1","labels":["malicious-activity","threatstream-severity-medium","threatstream-confidence-71"],"modified":"2020-01-22T02:58:57.57Z","name":"mal_url: http://f0387770.xsph.ru/login","object_marking_refs":["marking-definition--34098fce-860f-48ae-8e50-ebd3cc5e41da"],"pattern":"[url:value = 'http://f0387770.xsph.ru/login']","type":"indicator","valid_from":"2020-01-22T02:58:57.57Z"}
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
 * Ingestion mechanism: Primary ingestion mechanisms will be Filebeat modules and Ingest Packages. There will be no impact on ingestion mechanisms. [Filebeat module](https://www.elastic.co/guide/en/beats/filebeat/7.12/exported-fields-threatintel.html) is scheduled to be released in `7.12`.
 * Usage mechanism: The primary use of the proposed ECS fields and values is through Elastic Security solution. In 7.10 we released Indicator match rule to support the use of the proposed new fields and values.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

1. How to best represent malware{name,family,type}. Current proposal is to use `threat.indicator.classification` to describe threat delivery (Hacktool etc.) and family name.
1. Field types (Ref: https://github.com/elastic/ecs/pull/1127#issuecomment-776126293)
  - `threatintel.indicator.*` (Filebeat module) will be normal field type and will be deprecated when nested field types are better supported in Kibana
  - `threat.indicator.*` (actual threat ECS fieldset) will be nested now and used for enriched doc
  - Once there is better support for nested field types in Kibana, there will be a migration to `threat.indicator.*`
  - Do we see this development affecting the timeline for this RFC's advancement (https://github.com/elastic/ecs/pull/1127#issuecomment-777766608)?
    >I imagine many users interested in threat.indicator.* fields are looking to map their own indicator sources to threat.indicator.* and then ingest those sources for use with indicator match rules. Is this something that will still be possible until the migration to threat.indicator.* happens?
    >
    >Including the threat.indicator.* fields in ECS would still document the fields as soon as they are implemented in the signals indices. Yet, until we feel confident encouraging using these fields to normalize users' data, I'm worried about the confusion and experience that would result.

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
* @dcode | author
* @peasead | author
* @dcode | subject matter expert
* @peasead | subject matter expert
* @MikePaquette | subject matter expert
* @devonakerr | sponsor


## References

* [Threat Intel Field Set Draft](https://docs.google.com/spreadsheets/d/1hS3tF-sGmwnKb7uUGLo3Rng_q6EFgwo6UCae8Sp4E-g/edit?usp=sharing)
* [STIX Cyber Observable data model](https://docs.oasis-open.org/cti/stix/v2.1/cs01/stix-v2.1-cs01.html#_mlbmudhl16lr)

Some examples of open source intelligence are:
  * [Abuse.ch Malware Tracker](https://feodotracker.abuse.ch/)
  * [Abuse.ch URL Tracker](https://urlhaus.abuse.ch/)
  * [AlienVault OTX](https://otx.alienvault.com/api)
  * [Anomali Limo](https://www.anomali.com/resources/limo)

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
* Stage 1 (originally stage 2 prior to removal of RFC stage 4): https://github.com/elastic/ecs/pull/1127
* Stage 2: https://github.com/elastic/ecs/pull/1293


<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
