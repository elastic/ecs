---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-network.html
applies_to:
  stack: all
  serverless: all
---

# Network fields [ecs-network]

The network is defined as the communication path over which a host or network event happens.

The network.* fields should be populated with details about the network activity associated with an event.


## Network field details [_network_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-network-application$$$[network.application](#field-network-application) | When a specific application or service is identified from network connection details (source/dest IPs, ports, certificates, or wire format), this field captures the application’s or service’s name.<br><br>For example, the original event identifies the network connection being from a specific web service in a `https` network connection, like `facebook` or `twitter`.<br><br>The field value must be normalized to lowercase for querying.<br><br>type: keyword<br><br>example: `aim`<br> | extended |
| $$$field-network-bytes$$$[network.bytes](#field-network-bytes) | Total bytes transferred in both directions.<br><br>If `source.bytes` and `destination.bytes` are known, `network.bytes` is their sum.<br><br>type: long<br><br>example: `368`<br> | core |
| $$$field-network-community-id$$$[network.community_id](#field-network-community-id) | A hash of source and destination IPs and ports, as well as the protocol used in a communication. This is a tool-agnostic standard to identify flows.<br><br>Learn more at [https://github.com/corelight/community-id-spec](https://github.com/corelight/community-id-spec).<br><br>type: keyword<br><br>example: `1:hO+sN4H+MG5MY/8hIrXPqc4ZQz0=`<br> | extended |
| $$$field-network-direction$$$[network.direction](#field-network-direction) | Direction of the network traffic.<br><br>When mapping events from a host-based monitoring context, populate this field from the host’s point of view, using the values "ingress" or "egress".<br><br>When mapping events from a network or perimeter-based monitoring context, populate this field from the point of view of the network perimeter, using the values "inbound", "outbound", "internal" or "external".<br><br>Note that "internal" is not crossing perimeter boundaries, and is meant to describe communication between two hosts within the perimeter. Note also that "external" is meant to describe traffic between two hosts that are external to the perimeter. This could for example be useful for ISPs or VPN service providers.<br><br>Expected values for this field:<br><br>- `ingress`<br>- `egress`<br>- `inbound`<br>- `outbound`<br>- `internal`<br>- `external`<br>- `unknown`<br><br>type: keyword<br><br>example: `inbound`<br> | core |
| $$$field-network-forwarded-ip$$$[network.forwarded_ip](#field-network-forwarded-ip) | Host IP address when the source IP address is the proxy.<br><br>type: ip<br><br>example: `192.1.1.2`<br> | core |
| $$$field-network-iana-number$$$[network.iana_number](#field-network-iana-number) | IANA Protocol Number ([https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)). Standardized list of protocols. This aligns well with NetFlow and sFlow related logs which use the IANA Protocol Number.<br><br>type: keyword<br><br>example: `6`<br> | extended |
| $$$field-network-inner$$$[network.inner](#field-network-inner) | Network.inner fields are added in addition to network.vlan fields to describe the innermost VLAN when q-in-q VLAN tagging is present. Allowed fields include vlan.id and vlan.name. Inner vlan fields are typically used when sending traffic with multiple 802.1q encapsulations to a network sensor (e.g. Zeek, Wireshark.)<br><br>type: object<br> | extended |
| $$$field-network-name$$$[network.name](#field-network-name) | Name given by operators to sections of their network.<br><br>type: keyword<br><br>example: `Guest Wifi`<br> | extended |
| $$$field-network-packets$$$[network.packets](#field-network-packets) | Total packets transferred in both directions.<br><br>If `source.packets` and `destination.packets` are known, `network.packets` is their sum.<br><br>type: long<br><br>example: `24`<br> | core |
| $$$field-network-protocol$$$[network.protocol](#field-network-protocol) | In the OSI Model this would be the Application Layer protocol. For example, `http`, `dns`, or `ssh`.<br><br>The field value must be normalized to lowercase for querying.<br><br>type: keyword<br><br>example: `http`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/equivalent-1ba9f5?style=flat "equivalent") [network.protocol.name](https://opentelemetry.io/docs/specs/semconv/attributes-registry/network/#network-protocol-name)<br> | core |
| $$$field-network-transport$$$[network.transport](#field-network-transport) | Same as network.iana_number, but instead using the Keyword name of the transport layer (udp, tcp, ipv6-icmp, etc.)<br><br>The field value must be normalized to lowercase for querying.<br><br>type: keyword<br><br>example: `tcp`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [network.transport](https://opentelemetry.io/docs/specs/semconv/attributes-registry/network/#network-transport)<br> | core |
| $$$field-network-type$$$[network.type](#field-network-type) | In the OSI Model this would be the Network Layer. ipv4, ipv6, ipsec, pim, etc<br><br>The field value must be normalized to lowercase for querying.<br><br>type: keyword<br><br>example: `ipv4`<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry "") ![relation](https://img.shields.io/badge/match-93c93e?style=flat "match") [network.type](https://opentelemetry.io/docs/specs/semconv/attributes-registry/network/#network-type)<br> | core |


## Field reuse [_field_reuse_16]


### Field sets that can be nested under network [ecs-network-nestings]

| Location | Field Set | Description |
| --- | --- | --- |
| `network.inner.vlan.*` | [vlan](/reference/ecs-vlan.md) | Fields to describe observed VLAN information. |
| `network.vlan.*` | [vlan](/reference/ecs-vlan.md) | Fields to describe observed VLAN information. |

