# 0011: SIP Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1 (Draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2021-2-08** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

ECS SIP Fields provide normalization for fields related to Session Initiation and Session Description Protocols used in IP based real time communications (voice, video, sip based messaging).

Updates from previous version include:

- nesting url fields for sip uris moved to [text](text/0011/) directory
- corrected rfc number (0011)
- removed AD reference
- added Asserted Identities (https://tools.ietf.org/html/rfc3325)
- revised SDP audio/video breakdowns
- Built fields to enable nesting

## Fields
| **SIP Field**  | **Type**  | **Description**  | **Example**  |
| ---------------------------------- | ------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| **SIP Top level fields**           |         |                                                               |                                                                                  |
| sip.accept                         | keyword | SIP accept header                                             | application/sdp                                                                  |
| sip.allow                          | keyword | SIP allow header                                              | REGISTER, INVITE, ACK, BYE                                                       |
| sip.call\_id                       | keyword | SIP call\_id value                                            | 55112@192.168.1.100                                                              |
| sip.code                           | keyword | SIP response code                                             | 200                                                                              |
| sip.content\_length                | integer | Length of SIP message in bytes                                | 32                                                                               |
| sip.content\_type                  | keyword | SIP message content type                                      | application/sdp                                                                  |
| sip.cseq.code                      | integer | SIP CSeq Identifier                                           | 68                                                                               |
| sip.cseq.method                    | keyword | SIP CSeq Request                                              | INVITE                                                                           |
| sip.max\_forwards                  | integer | SIP maximum forward limit                                     |                                                                                  |
| sip.method                         | keyword | SIP Request Method                                            | REGISTER                                                                         |
| sip.status                         | keyword | SIP response message                                          | OK                                                                               |
| sip.supported                      | keyword | Array of supported SIP extensions                             |                                                                                  |
| sip.type                           | keyword | SIP Message type                                              | REQUEST                                                                          |
| sip.url.domain                     | keyword | Domain of the url.                                            | www.elastic.co                                                                   |
| sip.url.extension                  | keyword | File extension from the original request url.                 | png                                                                              |
| sip.url.fragment                   | keyword | Portion of the url after the \`#\`.                           |                                                                                  |
| sip.url.full                       | keyword | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.url.full.text                  | text    | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.url.original                   | keyword | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.url.original.text              | text    | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.url.password                   | keyword | Password of the request.                                      |                                                                                  |
| sip.url.path                       | keyword | Path of the request, such as "/search".                       |                                                                                  |
| sip.url.port                       | long    | Port of the request, such as 443.                             | 443                                                                              |
| sip.url.query                      | keyword | Query string of the request.                                  |                                                                                  |
| sip.url.registered\_domain         | keyword | The highest registered url domain, stripped of the subdomain. | example.com                                                                      |
| sip.url.scheme                     | keyword | Scheme of the url.                                            | https                                                                            |
| sip.url.subdomain                  | keyword | The subdomain of the domain.                                  | east                                                                             |
| sip.url.top\_level\_domain         | keyword | The effective top level domain (com, org, net, co.uk).        | co.uk                                                                            |
| sip.url.username                   | keyword | Username of the request.                                      |                                                                                  |
| sip.version                        | keyword | SIP Protocol Version                                          | 2                                                                                |
|                                    |         |                                                               |                                                                                  |
| **SIP Auth**                       |         |                                                               |                                                                                  |
| sip.auth.realm                     | keyword | SIP authorization realm realm                                 | sip.mydomain.com                                                                 |
| sip.auth.scheme                    | keyword | SIP authentication scheme                                     | digest                                                                           |
| sip.auth.url.domain                | keyword | Domain of the url.                                            | www.elastic.co                                                                   |
| sip.auth.url.extension             | keyword | File extension from the original request url.                 | png                                                                              |
| sip.auth.url.fragment              | keyword | Portion of the url after the \`#\`.                           |                                                                                  |
| sip.auth.url.full                  | keyword | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.auth.url.full.text             | text    | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.auth.url.original              | keyword | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.auth.url.original.text         | text    | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.auth.url.password              | keyword | Password of the request.                                      |                                                                                  |
| sip.auth.url.path                  | keyword | Path of the request, such as "/search".                       |                                                                                  |
| sip.auth.url.port                  | long    | Port of the request, such as 443.                             | 443                                                                              |
| sip.auth.url.query                 | keyword | Query string of the request.                                  |                                                                                  |
| sip.auth.url.registered\_domain    | keyword | The highest registered url domain, stripped of the subdomain. | example.com                                                                      |
| sip.auth.url.scheme                | keyword | Scheme of the url.                                            | https                                                                            |
| sip.auth.url.subdomain             | keyword | The subdomain of the domain.                                  | east                                                                             |
| sip.auth.url.top\_level\_domain    | keyword | The effective top level domain (com, org, net, co.uk).        | co.uk                                                                            |
| sip.auth.url.username              | keyword | Username of the request.                                      |                                                                                  |
|                                    |         |                                                               |                                                                                  |
| **SIP Contact**                    |         |                                                               |                                                                                  |
| sip.contact.display\_name          | keyword | SIP contact display name                                      | John Doe                                                                         |
| sip.contact.expires                | integer | SIP contact expiration timer                                  | 1800                                                                             |
| sip.contact.line                   | keyword | Sip contact line value                                        | aca6b97ca3f5e51a                                                                 |
| sip.contact.q                      | keyword | SIP contact preference                                        | 0.2                                                                              |
| sip.contact.transport              | keyword | SIP contact transport                                         | udp                                                                              |
| sip.contact.url.domain             | keyword | Domain of the url.                                            | www.elastic.co                                                                   |
| sip.contact.url.extension          | keyword | File extension from the original request url.                 | png                                                                              |
| sip.contact.url.fragment           | keyword | Portion of the url after the \`#\`.                           |                                                                                  |
| sip.contact.url.full               | keyword | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.contact.url.full.text          | text    | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.contact.url.original           | keyword | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.contact.url.original.text      | text    | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.contact.url.password           | keyword | Password of the request.                                      |                                                                                  |
| sip.contact.url.path               | keyword | Path of the request, such as "/search".                       |                                                                                  |
| sip.contact.url.port               | long    | Port of the request, such as 443.                             | 443                                                                              |
| sip.contact.url.query              | keyword | Query string of the request.                                  |                                                                                  |
| sip.contact.url.registered\_domain | keyword | The highest registered url domain, stripped of the subdomain. | example.com                                                                      |
| sip.contact.url.scheme             | keyword | Scheme of the url.                                            | https                                                                            |
| sip.contact.url.subdomain          | keyword | The subdomain of the domain.                                  | east                                                                             |
| sip.contact.url.top\_level\_domain | keyword | The effective top level domain (com, org, net, co.uk).        | co.uk                                                                            |
| sip.contact.url.username           | keyword | Username of the request.                                      |                                                                                  |
|                                    |         |                                                               |                                                                                  |
| **SIP From**                       |         |                                                               |                                                                                  |
| sip.from.display\_info             | keyword | Source SIP entity alias                                       | John Doe                                                                         |
| sip.from.tag                       | keyword | SIP source entity tag identifier                              | QvN92t713vSZK                                                                    |
| sip.from.url.domain                | keyword | Domain of the url.                                            | www.elastic.co                                                                   |
| sip.from.url.extension             | keyword | File extension from the original request url.                 | png                                                                              |
| sip.from.url.fragment              | keyword | Portion of the url after the \`#\`.                           |                                                                                  |
| sip.from.url.full                  | keyword | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.from.url.full.text             | text    | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.from.url.original              | keyword | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.from.url.original.text         | text    | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.from.url.password              | keyword | Password of the request.                                      |                                                                                  |
| sip.from.url.path                  | keyword | Path of the request, such as "/search".                       |                                                                                  |
| sip.from.url.port                  | long    | Port of the request, such as 443.                             | 443                                                                              |
| sip.from.url.query                 | keyword | Query string of the request.                                  |                                                                                  |
| sip.from.url.registered\_domain    | keyword | The highest registered url domain, stripped of the subdomain. | example.com                                                                      |
| sip.from.url.scheme                | keyword | Scheme of the url.                                            | https                                                                            |
| sip.from.url.subdomain             | keyword | The subdomain of the domain.                                  | east                                                                             |
| sip.from.url.top\_level\_domain    | keyword | The effective top level domain (com, org, net, co.uk).        | co.uk                                                                            |
| sip.from.url.username              | keyword | Username of the request.                                      |                                                                                  |
|                                    |         |                                                               |                                                                                  |
| **Sip Privacy**                    |         |                                                               |                                                                                  |
| sip.privacy.type                   | keyword | SIP privacy headers                                           | user                                                                             |
| sip.privacy.url.domain             | keyword | Domain of the url.                                            | www.elastic.co                                                                   |
| sip.privacy.url.extension          | keyword | File extension from the original request url.                 | png                                                                              |
| sip.privacy.url.fragment           | keyword | Portion of the url after the \`#\`.                           |                                                                                  |
| sip.privacy.url.full               | keyword | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.privacy.url.full.text          | text    | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.privacy.url.original           | keyword | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.privacy.url.original.text      | text    | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.privacy.url.password           | keyword | Password of the request.                                      |                                                                                  |
| sip.privacy.url.path               | keyword | Path of the request, such as "/search".                       |                                                                                  |
| sip.privacy.url.port               | long    | Port of the request, such as 443.                             | 443                                                                              |
| sip.privacy.url.query              | keyword | Query string of the request.                                  |                                                                                  |
| sip.privacy.url.registered\_domain | keyword | The highest registered url domain, stripped of the subdomain. | example.com                                                                      |
| sip.privacy.url.scheme             | keyword | Scheme of the url.                                            | https                                                                            |
| sip.privacy.url.subdomain          | keyword | The subdomain of the domain.                                  | east                                                                             |
| sip.privacy.url.top\_level\_domain | keyword | The effective top level domain (com, org, net, co.uk).        | co.uk                                                                            |
| sip.privacy.url.username           | keyword | Username of the request.                                      |                                                                                  |
|                                    |         |                                                               |                                                                                  |
| **SIP SDP**                        |         |                                                               |                                                                                  |
| sip.sdp.audio.format               | keyword | SIP SDP audio format                                          | 8,101                                                                            |
| sip.sdp.audio.original             | keyword | SIP SDP audio information                                     | audio 6000 RTP/AVP 8                                                             |
| sip.sdp.audio.port                 | long    | SIP SDP audio port                                            | 6000                                                                             |
| sip.sdp.audio.protocol             | keyword | SIP SDP audio protocol                                        | RTP/AVP                                                                          |
| sip.sdp.connection.address         | ip      | SIP SDP session connection address                            | 10.1.1.50                                                                        |
| sip.sdp.media.flags                | keyword | SIP SDP media flags                                           | recvonly                                                                         |
| sip.sdp.media.type                 | keyword | Array of SIP SDP media types offered                          | audio, video                                                                     |
| sip.sdp.owner.ip                   | ip      | SIP SDP session owner IP                                      | 10.1.1.50                                                                        |
| sip.sdp.owner.session\_id          | keyword | SIP SDP session id                                            | 1480144037                                                                       |
| sip.sdp.owner.username             | keyword | SIP SDP session owner name                                    | FreeSWITCH                                                                       |
| sip.sdp.owner.version              | keyword | SIP SDP session version                                       | 1480144038                                                                       |
| sip.sdp.session.name               | keyword | SIP SDP session name                                          | Company All Hands                                                                |
| sip.sdp.version                    | integer | SIP SDP version                                               | 0                                                                                |
| sip.sdp.video.format               | keyword | Array of SIP SDP video formats supported                      | 31, 32                                                                           |
| sip.sdp.video.original             | keyword | SIP SDP video information                                     | video 6001 RTP/AVP 31                                                            |
| sip.sdp.video.port                 | long    | SIP SDP video port                                            | 6001                                                                             |
| sip.sdp.video.protocol             | keyword | SIP SDP video protocol                                        | RTP/AVP                                                                          |
|                                    |         |                                                               |                                                                                  |
| **SIP To**                           |         |                                                               |                                                                                  |
| sip.to.display\_info               | keyword | Destination SIP entity alias                                  | John Doe                                                                         |
| sip.to.tag                         | keyword | SIP destination entity tag identifier                         | QvN92t713vSZK                                                                    |
| sip.to.url.domain                  | keyword | Domain of the url.                                            | www.elastic.co                                                                   |
| sip.to.url.extension               | keyword | File extension from the original request url.                 | png                                                                              |
| sip.to.url.fragment                | keyword | Portion of the url after the \`#\`.                           |                                                                                  |
| sip.to.url.full                    | keyword | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.to.url.full.text               | text    | Full unparsed URL.                                            | https://www.elastic.co:443/search?q=elasticsearch#top                            |
| sip.to.url.original                | keyword | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.to.url.original.text           | text    | Unmodified original url as seen in the event source.          | https://www.elastic.co:443/search?q=elasticsearch#top or /search?q=elasticsearch |
| sip.to.url.password                | keyword | Password of the request.                                      |                                                                                  |
| sip.to.url.path                    | keyword | Path of the request, such as "/search".                       |                                                                                  |
| sip.to.url.port                    | long    | Port of the request, such as 443.                             | 443                                                                              |
| sip.to.url.query                   | keyword | Query string of the request.                                  |                                                                                  |
| sip.to.url.registered\_domain      | keyword | The highest registered url domain, stripped of the subdomain. | example.com                                                                      |
| sip.to.url.scheme                  | keyword | Scheme of the url.                                            | https                                                                            |
| sip.to.url.subdomain               | keyword | The subdomain of the domain.                                  | east                                                                             |
| sip.to.url.top\_level\_domain      | keyword | The effective top level domain (com, org, net, co.uk).        | co.uk                                                                            |
| sip.to.url.username                | keyword | Username of the request.                                      |                                                                                  |
|                                    |         |                                                               |                                                                                  |
| ** SIP Via **                       |         |                                                               |                                                                                  |
| sip.via.branch                     | keyword | SIP Via Transaction ID                                        | z9hG4bK10\_16a83292baa1de54e0b7843\_I                                            |
| sip.via.received.address           | ip      | SIP endpoint nat address                                      | 151.101.2.217                                                                    |
| sip.via.received.port              | long    | SIP via rport                                                 | 5065                                                                             |
| sip.via.sent\_by.address           | ip      | SIP via IP address                                            | 192.168.1.10                                                                     |
| sip.via.sent\_by.port              | long    | Network port used by SIP proxy.                               | 5060                                                                             |
| sip.via.transport                  | keyword | SIP via transport                                             | udp                                                                              |
| sip.via.version                    | keyword | SIP Protocol version utilized by a proxy                      | 2                                                                                |
||||
| **Additional Fields** | |
|---------------------------    |-----------    |
| source.*          | network level ip info, uni/bi-directional concerns |
| destination.*     | network level ip info, uni/bi-directional concerns |
| client.*          | Typically used for e.g. client to SIP Server (not direct calls made up of multiple flows) |
| server.*          | Typically used for e.g. client to SIP Server (not direct calls made up of multiple flows) |
| network.*         | network level protocol information, etc. |
| user.*            | user information associated with a particular connection, typically client to SIP server vs direct endpoint to endpoint calls |
| session.*  ++     | RFC in process, session fields to normalize sessions across muultiple clients, etc. (ip phone, softphone, jabber client, etc) |
| observer.*        | Whenever SIP data is observed by a proxy, netflow records, or network sensor/capture device |
| organization.*    | Optional,  used in e.g. SIP SP environments to tag sessions, calls, etc. with an organizational identifier |
| user_agent        | Original and parsed as neccesary from SIP headers |
|||

### Field Notes
while the initial SIP field implementaiton was built around the concepts of a network level packet capture, inclusion of all of the fields presented is not necessary when normalizing e.g. SIP server or SIP proxy logs.

To do items:

1) Consider unidirectional SIP session ID implementation (https://tools.ietf.org/html/rfc7989)
2) Consider tel uri implementation (https://tools.ietf.org/html/rfc3966)

## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->
Typical implementations will utilize these fields to describe and normalize the various stages of a SIP/SDP based communcations mechanism.  Additional considerations including call analytics, fraud detection, troubleshooting, and threat detection have been identified as additional considerations.

Related nesting changes:
 - [user fields](text/0011/user.yml)
 - [url fields](text/0011/url.yml)


## Source data

Source Data will come from packet/protocol analysis from endpoints (e.g. Packetbeat) or network observers (e.g. Zeek/Corelight & Suricata), logs from SIP Servers (e.g. Cisco Call Manager, Microsoft Lync), or logs from SIP-aware perimeter devices (e.g. Palo Alto NGFW).

See this example of [raw SIP header](00011/Sip-via-ordering-example.txt).

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

No impact expected as SIP fieldsets are new, and will not impact any existing fields.
<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

## Concerns

Normalization, and the degree of normalization, of SIP URI fields may be an issue for discussion based on the potential implementation of ingesting SIP call records for the purposes of review of e.g. various types of communications fraud (e.g. should PSTN numbers be normalized with international dial codes, should implementation include capabilities to define internal call plans for more effective analysis, etc.)

Normalization of SIP/SDP and real time communication protocol connections may require the definition of a field similar to network.community_id to allow for the tracking of the full scope of a connection. Additionally the initial SDP setup phase often includes multiple audio/video codec definitions which may be difficult to normalize in such a way as to make analysis of the call setup phase effective.

Utilizing SIP fields in combination with network performance indicators (IP SLA, QOS settings, jitter, mos, etc.) would also be of interest to many users looking at SIP logging.
<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

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

Packetbeat Implementation (packet/protocol analysis)

<!--
Potential Additional Imnplementations
Zeek Implementation (packet/protocol/connection analysis)
Cisco Call Manager (Log ingestion)
Microsoft Lync (Log Analysis)
-->

<!--
Stage 4: Identify at least one real-world, production-ready implementation that uses these updated field definitions. An example of this might be a GA feature in an Elastic application in Kibana.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @DainPerkins | Author
* @marc-gr | Sponsor
* @jiriatipteldotorg | Subject Matter Expert

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
* https://tools.ietf.org/html/rfc3261
* https://tools.ietf.org/html/rfc5621
* https://tools.ietf.org/html/rfc5630
* https://tools.ietf.org/html/rfc6878
* https://tools.ietf.org/html/rfc8591
* https://tools.ietf.org/id/draft-ietf-sipclf-format-05.html
* https://www.sipforum.org/

* https://github.com/elastic/ecs/issues/420

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 1: https://github.com/elastic/ecs/pull/1014
  * Stage 1 correction: https://github.com/elastic/ecs/pull/1170
