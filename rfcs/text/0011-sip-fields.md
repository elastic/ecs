# 0011: SIP Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **1 (proposal)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2020-12-04** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

ECS SIP Fields provide normalization for fields related to Session Initiation and Session Description Protocols used in IP based real time communications (voice, video, sip based messaging).


## Fields

| Sip Fields                    | type          | Example                                          |
|---------------------------    |-----------    |----------------------------------------------    |
| | | |
| **SIP Request** | | INVITE sip:test@10.0.2.15:5060 SIP/2.0 |
| sip.type                      | keyword       | request / response |
| sip.method                    | keyword       | invite |
| sip.uri.original              | wildcard      | test@10.0.2.15:5060 |
| sip.uri.original.text         | text          | test@10.0.2.15:5060 |
| sip.uri.scheme                | keyword       | sip |
| sip.uri.username              | keyword       | test |
| sip.uri.host                  | keyword       | sip.cybercity.dk |
| sip.uri.port                  | long          | 5060 |
| sip.version                   | keyword       | 2 |
| | | |
| **SIP Response** | | SIP/2.0 200 OK |
| sip.status_code               | keyword       | 200 |
| sip.status                    | keyword       | ok |
| sip.version                   | keyword       | 2 |
| | | |
| **SIP Headers** | | |
| sip.accept                    | keyword       | application/sdp |
| sip.allow[]                   | keyword[]     | REGISTER, INVITE, ACK, BYE |
| sip.call_id                   | keyword       | 1-1966@10.0.2.20 |
| sip.content_length            | integer       | 0 |
| sip.content_type              | keyword       | application/sdp |
| sip.max_forwards              | integer       | 70 |
| sip.private.uri.original      | wildcard      | sip:35104723@sip.cybercity.dk |
| sip.private.uri.scheme        | keyword       | sip |
| sip.private.username          | keyword       | 35104723 |
| sip.supported[]               | keyword[]     | timer, path, replaces |
| user_agent.original           | keyword       | FreeSWITCH-mod_sofia/1.6.12-20-b91a0a6~64bit |
| user_agent.original.text      | text          | FreeSWITCH-mod_sofia/1.6.12-20-b91a0a6~64bit |
| | | |
| **SIP Headers CSEQ** | | 68 invite |
| sip.cseq.code                 | integer       | 68 |
| sip.cseq.method               | keyword       | invite |
| | | |
| **SIP Headers Via** | | SIP/2.0/UDP 192.168.1.2;received=80.230.219.70;rport=5061 branch=z9hG4bKnp112903503-43a64480192.168.1.2 |
| sip.via.transport             | keyword       | udp |
| sip.via.sent_by.address       | keyword       | 192.168.1.2 |
| sip.via.sent_by.port          | long          | 5060 |
| sip.via.received.address      | keyword       | 80.230.219.70 |
| sip.via.rport                 | long          | 5060|
| sip.via.branch                | keyword       | z9hG4bKnp112903503-43a64480192.168.1.2 |
| | | |
| **SIP Headers To** | | test <sip:test@10.0.2.15:5060>;tag=QvN92t713vSZK  |
| sip.to.display_info           | keyword       | test |
| sip.to.uri.original           | wildcard      | sip:test@10.0.2.15:5060 |
| sip.to.uri.scheme             | keyword       | sip |
| sip.to.uri.username           | keyword       | test |
| sip.to.uri.host               | keyword       | 10.0.2.15 |
| sip.to.uri.port               | long          | 5060 |
| sip.to.tag                    | keyword       | QvN92t713vSZK |
| | | |
| **SIP Headers From** | |  "PCMU/8000" <sip:sipp@10.0.2.20:5060>;tag=1 |
| sip.from.display_info         | keyword       | PCMU/8000 |
| sip.from.uri.original         | wilcard       | sip:sipp@10.0.2.20:5060  |
| sip.from.uri.scheme           | keyword       | sip | |
| sip.from.uri.username         | keyword       | sipp | |
| sip.from.uri.host             | keyword       | 10.0.2.20 | |
| sip.from.uri.port             | long          | 5060 |
| sip.from.tag                  | keyword       | 1 |
| | | |
| **SIP Headers Contact** | |  "Matthew Hodgson" <sip:voi18062@192.168.1.2:5060;line=aca6b97ca3f5e51a>;expires=1200;q=0.500 |
| sip.contact.display_info      | keyword      | |
| sip.contact.uri.original      | wildcard     | sip:test@10.0.2.15:5060 |
| sip.contact.uri.scheme        | keyword      | sip |
| sip.contact.uri.username      | keyword      | test |
| sip.contact.uri.host          | keyword      | 10.0.2.15 |
| sip.contact.uri.port          | long         | 5060 |
| sip.contact.transport         | keyword      | udp | |
| sip.contact.line              | keyword      | aca6b97ca3f5e51a |
| sip.contact.expires           | integer      | 1200 |
| sip.contact.q                 | float        | 0.5 |
| | | |
| **SIP Headers Auth** | | Authorization: Digest username="voi18062",realm="sip.cybercity.dk",uri="sip:192.168.1.2",nonce="1701b22972b90f440c3e4eb250842bb",opaque="1701a1351f70795",nc="00000001",response="79a0543188495d288c9ebbe0c881abdc" |
| sip.auth.scheme               | keyword      | Digest |
| sip.auth.realm                | keyword      | sip.cybercity.dk |
| sip.auth.uri.original         | wildcard     | sip:192.168.1.2 |
| sip.auth.uri.scheme           | keyword      | sip |
| sip.auth.uri.host             | keyword      | 192.168.1.2 |
| sip.auth.uri.port             | long         | |
| user.name                     | keyword      | voi18062 |
| | | |
| **SIP Body / SDP** | | Needs Example |
| sip.sdp.version               | integer      | 0 |
| sip.sdp.owner.username        | keyword      | Matthew |
| sip.sdp.owner.session_id      | keyword      | |
| sip.sdp.owner.version         | keyword      | |
| sip.sdp.owner.ip              | keyword      | 127.0.0.1 |
| sip.sdp.session.name          | keyword      | CounterPath eyeBeam 1.5 |
| sdp.connection.address        | keyword      | 127.0.0.1 |
| | | |
| **SIP Body / SDP Media**      |              | audio 27942 RTP/AVP 0 101 |
| sip.sdp.audio.description[]   | wildcard     | audio 57126 RTP/AVP 8 101 |
| sip.sdp.audio.port            | long         | 57126 |
| sip.sdp.media.format[]        | wildcard     | 8, 101 (ITU-T G.711 PCMA, DynamicRTP-Type-101) |
| sip.sdp.media.attributes[]    | wildcard     | 0 PCMU/8000, 101 telephone-event/8000, fmtp:101 0-16 |
| sip.sdp.video.description[]   | wildcard     | video 57126 RTP/AVP 8 101 |
| sip.sdp.video.port            | keyword      | 57126 |
| sip.sdp.video.format[]        | wildcard     | 8, 101 (ITU-T G.711 PCMA, DynamicRTP-Type-101) |
| sip.sdp.video.attributes[]    | wildcard     | 0 PCMU/8000, 101 telephone-event/8000, fmtp:101 0-16 |


## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->
Typical implementations will utilize these fields to describe and normalize the various stages of a SIP/SDP based communcations mechanism.  Additional considerations including call analytics, fraud detection, troubleshooting, and threat detection have been identified as additional considerations.

## Source data

Source Data will come from packet/protocol analysis from endpoints (e.g. Packetbeat) or network observers (e.g. Zeek/Corelight & Suricata), logs from SIP Servers (e.g. Cisco Call Manager, Microsoft Lync), or logs from SIP-aware perimeter devices (e.g. Palo Alto NGFW).

See this example of [raw SIP header](0011/Sip-via-ordering-example.txt).

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
