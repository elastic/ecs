# 0008: Cyber Threat Intelligence Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **3 (candidate)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-06-23** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

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
threat.indicator.first_seen | date | 2020-11-05T17:25:47.000Z | The date and time when intelligence source first reported sighting this indicator
threat.indicator.last_seen | date | 2020-11-05T17:25:47.000Z | The date and time when intelligence source last reported sighting this indicator.
threat.indicator.modified_at | date | 2020-11-05T17:25:47.000Z | The date and time when intelligence source last modified information for this indicator.
threat.indicator.sightings | long | 20 | Number of times this indicator was observed conducting threat activity
threat.indicator.type | keyword | ipv4-addr | Type of indicator as represented by Cyber Observable in STIX 2.0
threat.indicator.description | keyword | 201.10.10.90 was seen delivering Angler EK | Describes the type of action conducted by the threat
threat.indicator.confidence | keyword | Almost Certain/Nearly Certain | Identifies the vendor-neutral confidence rating using the DNI STIX confidence scale. Vendor-specific confidence scales may be added as custom fields.
threat.indicator.ip | ip | 1.2.3.4 | Identifies a threat indicator as an IP address (irrespective of direction).
threat.indicator.port | long | 443 | Identifies a threat indicator as a port number (irrespective of direction).
threat.indicator.email.address | keyword | phish@evil.com | Identifies a threat indicator as an email address (irrespective of direction).
threat.marking.tlp | keyword | RED | Data markings represent restrictions, permissions, and other guidance for how data can be used and shared. Examples could be TLP (WHITE, GREEN, AMBER, RED).
threat.indicator.scanner_stats | long | 4 | Count of Anti virus/EDR that successfully detected malicious file or URL. Sources like VirusTotal, Reversing Labs often provide these statistics.
threat.indicator.reference | keyword | https://feodotracker.abuse.ch/ | URL to the intelligence source
threat.indicator.provider | keyword | lrz_urlhaus | The name of the indicator's provider

### Proposed New Values for Event Fieldset

Field | New Value | Description
--- | --- | ---
event.kind | enrichment | Propose adding this value to capture the type of information this event contains and how it should be used. Threat intelligence will be used to enrich source events and signals. Enrichment could also apply to other types of contextual data sources (not just threat intelligence) such as directory services, IPAM data, asset lists.
event.category | threat | Propose adding this value to represent a new category of event data
event.type | indicator | Propose adding this value to be used as a sub-bucket of `event.category` to represent type of threat information. In future this could be extended to other STIX 2.0 Standard Data Objects like Actor, Infrastructure etc.

### Using existing Event Fieldset
Field | Type | Example | Description
--- | ---| --- | ---
event.reference | keyword | https://feodotracker.abuse.ch/ | URL to the intelligence source
event.severity | long | 7 | severity provided by threat intelligence source
event.risk_score | float | 10 | risk score provided by threat intelligence source
event.original | keyword | 2020-10-29 19:16:38,181.120.29.49,80,2020-11-02,Heodo | raw intelligence event
event.dataset | keyword | threatintel.{abusemalware,abuseurl,misp,otx,limo} | Identifies the name of specific dataset from the intelligence source
event.module | keyword | threatintel | Identifies the name of specific module where the data is coming from.
event.provider | keyword | Abuse.ch | Identifies the name of intelligence provider.

### Using existing ECS Fields to store indicator information

Fieldset | Description | Reference
--- | --- | ---
File | Use existing File fields to describe file entity details involved in threat activity. No changes to existing ECS fieldset | [File Fields](https://www.elastic.co/guide/en/ecs/current/ecs-file.html)
Hash | Use existing Hash fields to describe file entity details involved in threat activity. Hash fields are expected to be nested at `file.hash` , `process.hash`. No changes to existing ECS fieldset | [Hash Fields](https://www.elastic.co/guide/en/ecs/current/ecs-hash.html)
URL | Use existing URL fields to describe internet resources involved in threat activity. No changes to existing ECS fieldset | [URL](https://www.elastic.co/guide/en/ecs/current/ecs-url.html)
Registry | Use existing Registry fields involved in threat activity. No changes to existing ECS fieldset | [Registry](https://www.elastic.co/guide/en/ecs/current/ecs-registry.html)
Autonomous System (AS) | Use existing fields to capture routing prefixes for threat activity. No changes to existing ECS fieldset. | [AS](https://www.elastic.co/guide/en/ecs/current/ecs-as.html)
Geographic | Use existing fields to capture geographic location for threat activity. No changes to existing ECS fieldset. | [Geo](https://www.elastic.co/guide/en/ecs/current/ecs-geo.html)
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

The additions described above will be used to enable cyber threat intelligence capabilities in Elastic Security solution. A new rule type Indicator match was introduced in 7.10 and the proposed ECS updates will enable a new category of detection alerts that match incoming log and event data against threat intelligence sources. Additionally in the future we will also develop enrichment flows that add context from threat intelligence to alerts and events to assist analysts in their investigative workflows.

While there are two primary uses for these fields, this RFC deals primarily with the first: ingestion/storage of threat intelligence.

**Storing threat intelligence as an event document in threat index(s).**

Threat intelligence data will be collected from multiple sources stored in threat indices. The ECS fields proposed here will be used to structure the documents collected from various sources.

**Examples**

Network Example
```json5
{
    // Metadata about the indicator event
    "@timestamp": "2019-08-10T11:09:23.000Z",
    "event": {
        "kind": "enrichment",
        "category": "threat",
        "type": "indicator",
        "reference": "https://urlhaus.abuse.ch",
        "severity": 7,
        "risk_score": 10,
        "original": "2020-10-29 19:16:38"
    },

    // Metadata about the indicator data
    "threat.indicator": {
        "first_seen": "2020-11-05T17:25:47.000Z",
        "last_seen": "2020-11-05T17:25:47.000Z",
        "modified_at": "2020-11-05T17:25:47.000Z"
        "sightings": "10",
        "type": [
            "ipv4-addr",
            "port",
            "domain-name",
            "email-addr"
        ],
        "description": "Email address, domain, port, and IP address observed using an Angler EK campaign.",
        "provider": "Abuse.ch",
        "reference": "https://urlhaus.abuse.ch/url/1292596/",
        "confidence": "High",
        "ip": "1.2.3.4",
        "domain": "malicious.evil",
        "port": 443,
        "email.address": "phish@malicious.evil",
        "marking.tlp": "WHITE",
        "scanner_stats": 4
    },

    // Any indicators should also be copied to relevant related.* field
    "related": {
        "hash": [
            "1eee2bf3f56d8abed72da2bc523e7431",
            "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4"
        ],
        "hosts": [
            "nefarious.evil"
        ],
        "ip": [
            "1.2.3.4"
        ]
    },

    // Tags for context
    "tags": [
        "threatintel",
        "forwarded"
    ]
}
```

File Example
```json5
{
    // Metadata about the indicator event
    "@timestamp": "2019-08-10T11:09:23.000Z",
    "event": {
        "kind": "enrichment",
        "category": "threat",
        "type": "indicator",
        "reference": "https://bazaar.abuse.ch",
        "severity": 7,
        "risk_score": 10,
        "original": "2020-10-29 19:16:38"
        },

    // Metadata about the indicator data
    "threat.indicator": {
        "first_seen": "2020-11-05T17:25:47.000Z",
        "last_seen": "2020-11-05T17:25:47.000Z",
        "modified_at": "2020-11-05T17:25:47.000Z"
        "sightings": "10",
        "type": [
            "file"
        ],
        "description": "Implant used during an Angler EK campaign.",
        "provider": "Abuse.ch",
        "reference": "https://bazaar.abuse.ch/sample/f3ec9a2f2766c6bcf8c2894a9927c227649249ac146aabfe8d26b259be7d7055",
        "confidence": "High",
        "file": {
            "hash.sha256": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4",
            "hash.md5": "1eee2bf3f56d8abed72da2bc523e7431",
            "size": 656896,
            "name": "invoice.doc"
            },
        "marking.tlp": "WHITE",
        "scanner_stats": 4
    },

    // Any indicators should also be copied to relevant related.* field
    "related": {
        "hash": [
            "1eee2bf3f56d8abed72da2bc523e7431",
            "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4"
        ],
        "hosts": [
            "nefarious.evil"
        ],
        "ip": [
            "1.2.3.4"
        ]
    },

    // Tags for context
    "tags": [
        "threatintel",
        "forwarded"
    ]
}
```

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
- Malware Bazaar - This dataset from Malware Bazaar provides Malware threat information.
- ThreatFox - This dataset from ThreatFox provides malware and network threat information.

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

#### Malware Bazaar
This dataset from Malware Bazaar provides Malware threat information.
```
{"sha256_hash":"832fb4090879c1bebe75bea939a9c5724dbf87898febd425f94f7e03ee687d3b","sha3_384_hash":"a609684a08bfdd533be2a05b8649fc5f5e71642dde35d7d07fff11e5be60b9ec803959ab1be0a9225e098ca301a00b95","sha1_hash":"e7f6bf55ee9477a4208f0253d94deff4453aaa64","md5_hash":"781228e0a889c0624a5f1d8e9f5b0b30","first_seen":"2021-05-28 12:06:39","last_seen":null,"file_name":"Mozi.a","file_size":123164,"file_type_mime":"application/x-executable","file_type":"elf","reporter":"tolisec","anonymous":0,"signature":"Mozi","imphash":null,"tlsh":"A0C312E48E1121A0C5ADE566CC540FCAC3112D5E671E0DCA8F2CEE64AEC4AF45EADD6C","telfhash":null,"ssdeep":"3072:Lp2ANLHdrdTZvaSx6voDSnTi2Zr/G5kdstkUtfR1sAP/y:LF1HdrdFdrWnpp/G50sdfRmAPa","tags":["Mozi"],"code_sign":[],"intelligence":{"clamav":["Unix.Malware.Agent-7349999-0","Unix.Packed.Gafgyt-9390807-0","Unix.Packed.Gafgyt-9390815-0","Unix.Packed.Mirai-7640005-0"],"downloads":"65","uploads":"1","mail":null}}
{"sha256_hash":"57744761595c2dccdf76560c4e0fe7ea33ea85be281d1b7a9c9b4e9e9dbb0221","sha3_384_hash":"1399177d3a9d63eb342398bf3b31d151c3e02b666e181727d3628280af5adc0e5e4a17204168d994374990e126c2751c","sha1_hash":"0edecb66e625e6b07da5eab828e41b319b6aefdd","md5_hash":"cddc397ae51b9bb0bc9407a7165e33d9","first_seen":"2021-03-02 12:06:37","last_seen":null,"file_name":"sample.bin","file_size":385992,"file_type_mime":"application/x-executable","file_type":"elf","reporter":"c3rb3ru5d3d53c","anonymous":0,"signature":"Mirai","imphash":null,"tlsh":"8C84390FBF210EFBE89FDE3B02EE0B05219C950622997B397574C914F95A54B4AE3874","telfhash":null,"ssdeep":"6144:eOLyBx1SeRlVwwGsBmyjtc3LzdPvwTyughNG0FzPqOkJ:eOLyBxRIsnjtILOyuSNJxPqOkJ","tags":["botnet","mirai","Mozi"],"code_sign":[],"intelligence":{"clamav":["SecuriteInfo.com.Linux.Mirai-29.UNOFFICIAL","SecuriteInfo.com.Linux.Mirai-63.UNOFFICIAL","Unix.Dropper.Botnet-6566040-0","Unix.Dropper.Mirai-7135934-0","Unix.Dropper.Mirai-7136013-0","Unix.Dropper.Mirai-7136057-0","Unix.Dropper.Mirai-7136070-0","Unix.Exploit.Mirai-9795501-0","Unix.Packed.Botnet-6566031-0","Unix.Trojan.Gafgyt-6735924-0","Unix.Trojan.Gafgyt-6748839-0","Unix.Trojan.Mirai-7100807-0","Unix.Trojan.Mirai-8025795-0","Unix.Trojan.Mirai-9762350-0","Unix.Trojan.Mirai-9763616-0","Unix.Trojan.Mirai-9769616-0"],"downloads":"129","uploads":"1","mail":null}}
{"sha256_hash":"12013662c71da69de977c04cd7021f13a70cf7bed4ca6c82acbc100464d4b0ef","sha3_384_hash":"c8f175202c18fc7670313fc5a7221b347b2f4f204d3eaa2c5e5ed1a1ed3038f6f038c48edcbe4efb232a6b3d2a6bd51d","sha1_hash":"292559e94f1c04b7d0c65d4a01bbbc5dc1ff6f21","md5_hash":"eec5c6c219535fba3a0492ea8118b397","first_seen":"2021-01-12 20:52:19","last_seen":null,"file_name":"Mozi.m","file_size":307960,"file_type_mime":"application/x-executable","file_type":"elf","reporter":"r3dbU7z","anonymous":0,"signature":"Mirai","imphash":null,"tlsh":"13643A8AFD81AE25D5C126BBFE2F4289331317B8D2EB71029D145F2876CA94F0F7A541","telfhash":"d4014e084c695a78f066c975d0fb3172562e449af75236141b75fc2e2e638e2312192f","ssdeep":"6144:T2s/gAWuboqsJ9xcJxspJBqQgTuaJZRhVabE5wKSDP99zBa77oNsKqqfPqOJ:T2s/bW+UmJqBxAuaPRhVabEDSDP99zBT","tags":["elf","mirai","Mozi"],"code_sign":[],"intelligence":{"clamav":["SecuriteInfo.com.Linux.Mirai-29.UNOFFICIAL","SecuriteInfo.com.Linux.Mirai-63.UNOFFICIAL","Unix.Dropper.Botnet-6566040-0","Unix.Dropper.Mirai-7135934-0","Unix.Dropper.Mirai-7136013-0","Unix.Dropper.Mirai-7136057-0","Unix.Dropper.Mirai-7136070-0","Unix.Exploit.Mirai-9795501-0","Unix.Packed.Botnet-6566031-0","Unix.Trojan.Gafgyt-6735924-0","Unix.Trojan.Gafgyt-6748839-0","Unix.Trojan.Mirai-7100807-0","Unix.Trojan.Mirai-8025795-0","Unix.Trojan.Mirai-9762350-0","Unix.Trojan.Mirai-9763616-0","Unix.Trojan.Mirai-9769616-0"],"downloads":"134","uploads":"1","mail":null}}
```

#### ThreatFox
This dataset from ThreatFox provides malware and network threat information.
```
{"id":"115772","ioc":"46.229.199.126:53822","threat_type":"botnet_cc","threat_type_desc":"Indicator that identifies a botnet command&control server (C&C)","ioc_type":"ip:port","ioc_type_desc":"ip:port combination that is used for botnet Command&control (C&C)","malware":"elf.mozi","malware_printable":"Mozi","malware_alias":null,"malware_malpedia":"https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi","confidence_level":75,"first_seen":"2021-06-15 08:22:52 UTC","last_seen":null,"reference":"https://bazaar.abuse.ch/sample/4b41223ca64ab6ef4b3b9c9d4257902a32f9fa8cdf4d9f6261b24b8dee81d233/","reporter":"abuse_ch","tags":["Mozi"]}
{"id":"115771","ioc":"188.254.247.90:37294","threat_type":"botnet_cc","threat_type_desc":"Indicator that identifies a botnet command&control server (C&C)","ioc_type":"ip:port","ioc_type_desc":"ip:port combination that is used for botnet Command&control (C&C)","malware":"elf.mozi","malware_printable":"Mozi","malware_alias":null,"malware_malpedia":"https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi","confidence_level":75,"first_seen":"2021-06-15 08:22:51 UTC","last_seen":null,"reference":"https://bazaar.abuse.ch/sample/4b41223ca64ab6ef4b3b9c9d4257902a32f9fa8cdf4d9f6261b24b8dee81d233/","reporter":"abuse_ch","tags":["Mozi"]}
{"id":"115770","ioc":"119.195.9.2:5611","threat_type":"botnet_cc","threat_type_desc":"Indicator that identifies a botnet command&control server (C&C)","ioc_type":"ip:port","ioc_type_desc":"ip:port combination that is used for botnet Command&control (C&C)","malware":"elf.mozi","malware_printable":"Mozi","malware_alias":null,"malware_malpedia":"https://malpedia.caad.fkie.fraunhofer.de/details/elf.mozi","confidence_level":75,"first_seen":"2021-06-15 08:22:50 UTC","last_seen":null,"reference":"https://bazaar.abuse.ch/sample/4b41223ca64ab6ef4b3b9c9d4257902a32f9fa8cdf4d9f6261b24b8dee81d233/","reporter":"abuse_ch","tags":["Mozi"]}
```


## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->
 * Ingestion mechanism: Primary ingestion mechanisms will be Filebeat modules and Ingest Packages. There will be no impact on ingestion mechanisms. [Filebeat module](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-threatintel.html) was released in `7.12`.
 * Usage mechanism: The primary use of the proposed ECS fields and values is through Elastic Security solution. In 7.10 we released Indicator match rule to support the use of the proposed new fields and values.

## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

1. How to best represent malware{name,family,type}. Current proposal is to use `threat.indicator.classification` to describe threat delivery (Hacktool etc.) and family name.
  - This can be represented through the use of the [`threat.software.*`](https://www.elastic.co/guide/en/ecs/master/ecs-threat.html) fields.
  - Awaiting [approval](https://github.com/elastic/ecs/pull/1480#issuecomment-889312434) of this recommendation.
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
* @rylnd | author
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
  * [Malware Bazaar](https://bazaar.abuse.ch/)
  * [ThreatFox](https://threatfox.abuse.ch/)

Some examples of commercial intelligence include:
  * [Anomali ThreatStream](https://www.anomali.com/products/threatstream)
  * [Recorded Future](https://api.recordedfuture.com/v2/)
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
  * Stage 2 addendum: https://github.com/elastic/ecs/pull/1502
* Stage 3: https://github.com/elastic/ecs/pull/1480

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
