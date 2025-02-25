---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-client.html
applies_to:
  stack: all
  serverless: all
---

# Client fields [ecs-client]

A client is defined as the initiator of a network connection for events regarding sessions, connections, or bidirectional flow records.

For TCP events, the client is the initiator of the TCP connection that sends the SYN packet(s). For other protocols, the client is generally the initiator or requestor in the network transaction. Some systems use the term "originator" to refer the client in TCP connections. The client fields describe details about the system acting as the client in the network event. Client fields are usually populated in conjunction with server fields. Client fields are generally not populated for packet-level events.

Client / server representations can add semantic context to an exchange, which is helpful to visualize the data in certain situations. If your context falls in that category, you should still ensure that source and destination are filled appropriately.


## Client field details [_client_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-client-address$$$[client.address](#field-client-address) | Some event client addresses are defined ambiguously. The event will sometimes list an IP, a domain or a unix socket.  You should always store the raw address in the `.address` field.<br><br>Then it should be duplicated to `.ip` or `.domain`, depending on which one it is.<br><br>type: keyword<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [client.address](https://opentelemetry.io/docs/specs/semconv/attributes-registry/client/#client-address)<br> | extended |
| $$$field-client-bytes$$$[client.bytes](#field-client-bytes) | Bytes sent from the client to the server.<br><br>type: long<br><br>example: `184`<br> | core |
| $$$field-client-domain$$$[client.domain](#field-client-domain) | The domain name of the client system.<br><br>This value may be a host name, a fully qualified domain name, or another host naming format. The value may derive from the original event or be added from enrichment.<br><br>type: keyword<br><br>example: `foo.example.com`<br> | core |
| $$$field-client-ip$$$[client.ip](#field-client-ip) | IP address of the client (IPv4 or IPv6).<br><br>type: ip<br> | core |
| $$$field-client-mac$$$[client.mac](#field-client-mac) | MAC address of the client.<br><br>The notation format from RFC 7042 is suggested: Each octet (that is, 8-bit byte) is represented by two [uppercase] hexadecimal digits giving the value of the octet as an unsigned integer. Successive octets are separated by a hyphen.<br><br>type: keyword<br><br>example: `00-00-5E-00-53-23`<br> | core |
| $$$field-client-nat-ip$$$[client.nat.ip](#field-client-nat-ip) | Translated IP of source based NAT sessions (e.g. internal client to internet).<br><br>Typically connections traversing load balancers, firewalls, or routers.<br><br>type: ip<br> | extended |
| $$$field-client-nat-port$$$[client.nat.port](#field-client-nat-port) | Translated port of source based NAT sessions (e.g. internal client to internet).<br><br>Typically connections traversing load balancers, firewalls, or routers.<br><br>type: long<br> | extended |
| $$$field-client-packets$$$[client.packets](#field-client-packets) | Packets sent from the client to the server.<br><br>type: long<br><br>example: `12`<br> | core |
| $$$field-client-port$$$[client.port](#field-client-port) | Port of the client.<br><br>type: long<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [client.port](https://opentelemetry.io/docs/specs/semconv/attributes-registry/client/#client-port)<br> | core |
| $$$field-client-registered-domain$$$[client.registered_domain](#field-client-registered-domain) | The highest registered client domain, stripped of the subdomain.<br><br>For example, the registered domain for "foo.example.com" is "example.com".<br><br>This value can be determined precisely with a list like the public suffix list ([https://publicsuffix.org](https://publicsuffix.org)). Trying to approximate this by simply taking the last two labels will not work well for TLDs such as "co.uk".<br><br>type: keyword<br><br>example: `example.com`<br> | extended |
| $$$field-client-subdomain$$$[client.subdomain](#field-client-subdomain) | The subdomain portion of a fully qualified domain name includes all of the names except the host name under the registered_domain.  In a partially qualified domain, or if the the qualification level of the full name cannot be determined, subdomain contains all of the names below the registered domain.<br><br>For example the subdomain portion of "www.east.mydomain.co.uk" is "east". If the domain has multiple levels of subdomain, such as "sub2.sub1.example.com", the subdomain field should contain "sub2.sub1", with no trailing period.<br><br>type: keyword<br><br>example: `east`<br> | extended |
| $$$field-client-top-level-domain$$$[client.top_level_domain](#field-client-top-level-domain) | The effective top level domain (eTLD), also known as the domain suffix, is the last part of the domain name. For example, the top level domain for example.com is "com".<br><br>This value can be determined precisely with a list like the public suffix list ([https://publicsuffix.org](https://publicsuffix.org)). Trying to approximate this by simply taking the last label will not work well for effective TLDs such as "co.uk".<br><br>type: keyword<br><br>example: `co.uk`<br> | extended |


## Field reuse [_field_reuse_2]


### Field sets that can be nested under client [ecs-client-nestings]

| Location | Field Set | Description |
| --- | --- | --- |
| `client.as.*` | [as](/reference/ecs-as.md) | Fields describing an Autonomous System (Internet routing prefix). |
| `client.geo.*` | [geo](/reference/ecs-geo.md) | Fields describing a location. |
| `client.user.*` | [user](/reference/ecs-user.md) | Fields to describe the user relevant to the event. |

