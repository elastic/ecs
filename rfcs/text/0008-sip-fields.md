# 0000: SIP Fields
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

ECS SIP Fields provide normalization for fields related to Session Initiation and Session Description Protocols used in IP based real time communications (voice, video, sip based messaging).


## Fields

| Sip Fields                	| Example                                      	| type      	|
|---------------------------	|----------------------------------------------	|-----------	|
|                           	|                                              	|           	|
| **SIP Request**               | INVITE sip:test@10.0.2.15:5060 SIP/2.0       	|           	|
| sip.type                  	| request / response                           	| keyword   	|
| sip.method                	| invite                                       	| keyword   	|
| sip.uri.original          	| test@10.0.2.15:5060                          	| keyword   	|
| sip.uri.original.text     	| test@10.0.2.15:5060                          	| text      	|
| sip.uri.scheme            	| sip                                          	| keyword   	|
| sip.uri.username          	| test                                         	| keyword   	|
| sip.uri.host              	| sip.cybercity.dk                             	| keyword   	|
| sip.uri.port              	| 5060                                         	| long      	|
| sip.version               	| 2                                            	| keyword   	|
|                           	|                                              	|           	|
| **SIP Response**              | SIP/2.0 200 OK                               	|           	|
| sip.code                  	| 200                                          	| keyword   	|
| sip.status                	| ok                                           	| keyword   	|
| sip.version               	| 2                                            	| keyword   	|
|                           	|                                              	|           	|
| **SIP Headers**               |                                              	|           	|
| sip.accept                	| application/sdp                              	| keyword   	|
| sip.allow[]               	| REGISTER, INVITE, ACK, BYE                   	| keyword[] 	|
| sip.call_id               	| 1-1966@10.0.2.20                             	| keyword   	|
| sip.content_length        	| 0                                            	| integer   	|
| sip.content_type          	| application/sdp                              	| keyword   	|
| sip.max_forwards          	| 70                                           	| integer   	|
| sip.private.uri.original  	| sip:35104723@sip.cybercity.dk                	| keyword   	|
| sip.private.original.text 	| sip.cybercity.dk                             	| text      	|
| sip.private.uri.scheme    	| sip                                          	| keyword   	|
| sip.private.username      	| 35104723                                     	| keyword   	|
| sip.supported[]           	| timer, path, replaces                        	| keyword[] 	|
| user_agent.original       	| FreeSWITCH-mod_sofia/1.6.12-20-b91a0a6~64bit 	| keyword   	|
| user_agent.original.text  	| FreeSWITCH-mod_sofia/1.6.12-20-b91a0a6~64bit 	| text      	|
|                           	|                                              	|           	|
| **SIP Headers CSEQ**        	| 68 invite                                    	|           	|
| sip.cseq.code             	| 68                                           	| integer   	|
| sip.cseq.method           	| invite                                       	| keyword   	|
|                               |                                               |               |
| **SIP Headers Via**              | Ex 1: SIP/2.0/UDP 192.168.1.2;received=80.230.219.70;rport=5060;branch=z9hG4bKnp112903503-43a64480192.168.1.2 EX2: SIP/2.0/UDP 10.0.2.20:5060;branch=z9hG4bK-1966-1-0                                               	|             	|
| sip.via.transport             	| udp                                                                                                                                                                                                                 	| keyword     	|
| sip.via.sent_by.address       	| 192.168.1.2                                                                                                                                                                                                         	| keyword     	|
| sip.via.sent_by.port          	|                                                                                                                                                                                                                     	| long        	|
| sip.via.received.address      	| 80.230.219.70                                                                                                                                                                                                       	| keyword     	|
| sip..via.rport                	| 5060                                                                                                                                                                                                                	|             	|
| sip.via.branch                	| z9hG4bKnp112903503-43a64480192.168.1.2                                                                                                                                                                              	| keyword     	|
|                               	|                                                                                                                                                                                                                     	|             	|
| **SIP Headers To**              	| test <sip:test@10.0.2.15:5060>;tag=QvN92t713vSZK                                                                                                                                                                  |             	|
| sip.to.display_info           	| test                                                                                                                                                                                                                	| keyword     	|
| sip.to.uri.original           	| sip:test@10.0.2.15:5060                                                                                                                                                                                             	| keyword     	|
| sip.to.uri.original.text      	| sip:test@10.0.2.15:5060                                                                                                                                                                                             	| keyword     	|
| sip.to.uri.scheme             	| sip                                                                                                                                                                                                                 	| keyword     	|
| sip.to.uri.username           	| test                                                                                                                                                                                                                	| keyword     	|
| sip.to.uri.host               	| 10.0.2.15                                                                                                                                                                                                           	| keyword     	|
| sip.to.uri.port               	| 5060                                                                                                                                                                                                                	| long        	|
| sip.to.tag                    	| QvN92t713vSZK                                                                                                                                                                                                       	| keyword     	|
|                               	|                                                                                                                                                                                                                     	|             	|
|                               	|                                                                                                                                                                                                                     	|             	|
| **SIP Headers From**            	| EX1: "PCMU/8000" <sip:sipp@10.0.2.20:5060>;tag=1. EX2: "Matthew Hodgson" <sip:matthew@mxtelecom.com>;tag=5c7cdb68                                                                                                   	|             	|
| sip.from.display_info         	| PCMU/8000                                                                                                                                                                                                           	| keyword     	|
| sip.from.uri.original         	| sip:sipp@10.0.2.20:5060                                                                                                                                                                                             	| keyword     	|
| sip.from.uri.original.text    	| sip:sipp@10.0.2.20:5060                                                                                                                                                                                             	| text        	|
| sip.from.uri.scheme           	| sip                                                                                                                                                                                                                 	| keyword     	|
| sip.from.uri.username         	| sipp                                                                                                                                                                                                                	| keyword     	|
| sip.from.uri.host             	| 10.0.2.20                                                                                                                                                                                                           	| keyword     	|
| sip.from.uri.port             	| 5060                                                                                                                                                                                                                	| long        	|
| sip.from.tag                  	| 1                                                                                                                                                                                                                   	| integer     	|
|                               	|                                                                                                                                                                                                                     	|             	|
| **SIP Headers Contact**         	| <sip:test@10.0.2.15:5060;transport=udp> \| <sip:voi18062@192.168.1.2:5060;line=aca6b97ca3f5e51a>;expires=1200;q=0.500                                                                                               	|             	|
| sip.contact.display_info      	|                                                                                                                                                                                                                     	| keyword     	|
| sip.contact.uri.original      	| sip:test@10.0.2.15:5060                                                                                                                                                                                             	| keyword     	|
| sip.contact.uri.original.text 	| sip:test@10.0.2.15:5060                                                                                                                                                                                             	| text        	|
| sip.contact.uri.scheme        	| sip                                                                                                                                                                                                                 	| keyword     	|
| sip.contact.uri.username      	| test                                                                                                                                                                                                                	| keyword     	|
| sip.contact.uri.host          	| 10.0.2.15                                                                                                                                                                                                           	| keyword     	|
| sip.contact.uri.port          	| 5060                                                                                                                                                                                                                	| long        	|
| sip.contact.transport         	| udp                                                                                                                                                                                                                 	| keyword     	|
| sip.contact.line              	| aca6b97ca3f5e51a                                                                                                                                                                                                    	| keyword     	|
| sip.contact.expires           	| 1200                                                                                                                                                                                                                	| integer     	|
| sip.contact.q                 	| 0.5                                                                                                                                                                                                                 	| float       	|
|                               	|                                                                                                                                                                                                                     	|             	|
| **SIP Headers Auth**           	| Authorization: Digest username="voi18062",realm="sip.cybercity.dk",uri="sip:192.168.1.2",nonce="1701b22972b90f440c3e4eb250842bb",opaque="1701a1351f70795",nc="00000001",response="79a0543188495d288c9ebbe0c881abdc" 	|             	|
| sip.auth.scheme               	| Digest                                                                                                                                                                                                              	| keyword     	|
| sip.auth.realm                	| sip.cybercity.dk                                                                                                                                                                                                    	| keyword     	|
| sip.auth.uri.original         	| sip:192.168.1.2                                                                                                                                                                                                     	| keyword     	|
| sip.auth.uri.original.text    	| sip:192.168.1.2                                                                                                                                                                                                     	| text        	|
| sip.auth.uri.scheme           	| sip                                                                                                                                                                                                                 	| keyword     	|
| sip.auth.uri.host             	| 192.168.1.2                                                                                                                                                                                                         	| keyword     	|
| sip.auth.uri.port             	| n/a                                                                                                                                                                                                                 	| long        	|
| user.name                     	| voi18062                                                                                                                                                                                                            	|             	|
|                               	|                                                                                                                                                                                                                     	|             	|
| **SIP Body / SDP**              	| 1.20826E+12                                                                                                                                                                                                         	|             	|
| sip.sdp.version               	| 0                                                                                                                                                                                                                   	| integer     	|
| sip.sdp.owner.username        	| Matthew                                                                                                                                                                                                             	| keyword     	|
| sip.sdp.owner.session_id      	| 1.20826E+12                                                                                                                                                                                                         	| long?       	|
| sip.sdp.owner.version         	| 1.20826E+12                                                                                                                                                                                                         	| long?       	|
| sip.sdp.owner.ip              	| 127.0.0.1                                                                                                                                                                                                           	| ip          	|
| sip.sdp.session.name          	| CounterPath eyeBeam 1.5                                                                                                                                                                                             	| keyword     	|
| event.start                   	|                                                                                                                                                                                                                     	| long?       	|
| event.stop                    	|                                                                                                                                                                                                                     	|             	|
| sdp.connection.address        	| 127.0.0.1                                                                                                                                                                                                           	|             	|
|                               	|                                                                                                                                                                                                                     	|             	|
| **SIP Body / SDP Media**         	| audio 27942 RTP/AVP 0 101                                                                                                                                                                                           	|             	|
| sip.sdp.audio.description[]   	| audio 57126 RTP/AVP 8 101                                                                                                                                                                                           	| wildcard?   	|
| sip.sdp.audio.port            	| 57126                                                                                                                                                                                                               	| long        	|
| sip.sdp.media.format[]        	| 8, 101 (ITU-T G.711 PCMA, DynamicRTP-Type-101)                                                                                                                                                                      	| wildcard?[] 	|
| sip.sdp.media.attributes[]    	| 0 PCMU/8000, 101 telephone-event/8000, fmtp:101 0-16                                                                                                                                                                	| wildcard?[] 	|
|                               	|                                                                                                                                                                                                                     	|             	|
| sip.sdp.video.description[]   	| video 57126 RTP/AVP 8 101                                                                                                                                                                                           	|             	|
| sip.sdp.video.port            	| 57126                                                                                                                                                                                                               	|             	|
| sip.sdp.video.format[]        	| 8, 101 (ITU-T G.711 PCMA, DynamicRTP-Type-101)                                                                                                                                                                      	| wildcard?[] 	|
| sip.sdp.video.attributes[]    	| 0 PCMU/8000, 101 telephone-event/8000, fmtp:101 0-16                                                                                                                                                                	| wildcard?[] 	|


## Usage

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->
Typical implementations will utilize these fields to describe and normalize the various stages of a SIP/SDP based communcations mechanism.  Additional considerations including call analytics, fraud detection, troubleshooting, and threat detection have been identified as additional considerations.

## Source data

Source Data will come from packet/protocol analysis from endpoints (e.g. Packetbeat) or network observers (e.g. Zeek/Corelight & Suricata), logs from SIP Servers (e.g. Cisco Call Manager, Microsfot Lync), or logs from SIP-aware perimeter devices (e.g. Palo Alto NGFW).
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

Normalization, and the degree of normalization, of SIP URI fields may be an issue for discussion based on the potential implementation of ingesting SIP call records for the purposes of review for e.g. various types of communications fraud (e.g. should PSTN numbers be normalized with international dial codes, should implementaiton include capabilities to define internal call plans for more effective analysis, etc.)

Normalization of SIP/SDP and real time communication protocol connections may require the definition of a field similar to network.community_id to allow for the tracking of the full scope of a connection. Additionally the initial SDP setup phase often includes
multiple audio/video codec definitions which may be difficult to normalize in such a way as to make analysis of the call setup phase effective.

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
Zeek Implementation (packet/protocol/connection analysis)
Cisco Call Manager (Log ingestion)
Mictosoft Lync (Log Analysis)
<!--
Stage 4: Identify at least one real-world, production-ready implementation that uses these updated field definitions. An example of this might be a GA feature in an Elastic application in Kibana.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @DainPerkins | Author

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
https://tools.ietf.org/html/rfc3261
https://tools.ietf.org/html/rfc5621
https://tools.ietf.org/html/rfc5630
https://tools.ietf.org/html/rfc6878
https://tools.ietf.org/html/rfc8591
https://tools.ietf.org/id/draft-ietf-sipclf-format-05.html
https://www.sipforum.org/

https://github.com/elastic/ecs/issues/420

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1014

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
