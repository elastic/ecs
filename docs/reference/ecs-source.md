---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-source.html
applies_to:
  stack: all
  serverless: all
---
% This file is automatically generated. Don't edit it manually!

# Source fields [ecs-source]

Source fields capture details about the sender of a network exchange/packet. These fields are populated from a network event, packet, or other event containing details of a network transaction.

Source fields are usually populated in conjunction with destination fields. The source and destination fields are considered the baseline and should always be filled if an event contains source and destination details from a network transaction. If the event also contains identification of the client and server roles, then the client and server fields should also be populated.

## Source field details [_source_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-source-address$$$ [source.address](#field-source-address) | Some event source addresses are defined ambiguously. The event will sometimes list an IP, a domain or a unix socket.  You should always store the raw address in the `.address` field.<br><br>Then it should be duplicated to `.ip` or `.domain`, depending on which one it is.<br><br>type: keyword<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry) [![match](https://img.shields.io/badge/match-93c93e?style=flat)](/reference/ecs-opentelemetry.md#ecs-opentelemetry-relation) [source.address](https://opentelemetry.io/docs/specs/semconv/attributes-registry/source/#source-address) | extended |
| $$$field-source-bytes$$$ [source.bytes](#field-source-bytes) | Bytes sent from the source to the destination.<br><br>type: long<br><br>example: `184` | core |
| $$$field-source-domain$$$ [source.domain](#field-source-domain) | The domain name of the source system.<br><br>This value may be a host name, a fully qualified domain name, or another host naming format. The value may derive from the original event or be added from enrichment.<br><br>type: keyword<br><br>example: `foo.example.com` | core |
| $$$field-source-ip$$$ [source.ip](#field-source-ip) | IP address of the source (IPv4 or IPv6).<br><br>type: ip | core |
| $$$field-source-mac$$$ [source.mac](#field-source-mac) | MAC address of the source.<br><br>The notation format from RFC 7042 is suggested: Each octet (that is, 8-bit byte) is represented by two [uppercase] hexadecimal digits giving the value of the octet as an unsigned integer. Successive octets are separated by a hyphen.<br><br>type: keyword<br><br>example: `00-00-5E-00-53-23` | core |
| $$$field-source-nat-ip$$$ [source.nat.ip](#field-source-nat-ip) | Translated ip of source based NAT sessions (e.g. internal client to internet)<br><br>Typically connections traversing load balancers, firewalls, or routers.<br><br>type: ip | extended |
| $$$field-source-nat-port$$$ [source.nat.port](#field-source-nat-port) | Translated port of source based NAT sessions. (e.g. internal client to internet)<br><br>Typically used with load balancers, firewalls, or routers.<br><br>type: long | extended |
| $$$field-source-packets$$$ [source.packets](#field-source-packets) | Packets sent from the source to the destination.<br><br>type: long<br><br>example: `12` | core |
| $$$field-source-port$$$ [source.port](#field-source-port) | Port of the source.<br><br>type: long<br><br>![OTel Badge](https://img.shields.io/badge/OpenTelemetry-4a5ca6?style=flat&logo=opentelemetry) [![match](https://img.shields.io/badge/match-93c93e?style=flat)](/reference/ecs-opentelemetry.md#ecs-opentelemetry-relation) [source.port](https://opentelemetry.io/docs/specs/semconv/attributes-registry/source/#source-port) | core |
| $$$field-source-registered-domain$$$ [source.registered_domain](#field-source-registered-domain) | The highest registered source domain, stripped of the subdomain.<br><br>For example, the registered domain for "foo.example.com" is "example.com".<br><br>This value can be determined precisely with a list like the public suffix list (https://publicsuffix.org). Trying to approximate this by simply taking the last two labels will not work well for TLDs such as "co.uk".<br><br>type: keyword<br><br>example: `example.com` | extended |
| $$$field-source-subdomain$$$ [source.subdomain](#field-source-subdomain) | The subdomain portion of a fully qualified domain name includes all of the names except the host name under the registered_domain.  In a partially qualified domain, or if the the qualification level of the full name cannot be determined, subdomain contains all of the names below the registered domain.<br><br>For example the subdomain portion of "www.east.mydomain.co.uk" is "east". If the domain has multiple levels of subdomain, such as "sub2.sub1.example.com", the subdomain field should contain "sub2.sub1", with no trailing period.<br><br>type: keyword<br><br>example: `east` | extended |
| $$$field-source-top-level-domain$$$ [source.top_level_domain](#field-source-top-level-domain) | The effective top level domain (eTLD), also known as the domain suffix, is the last part of the domain name. For example, the top level domain for example.com is "com".<br><br>This value can be determined precisely with a list like the public suffix list (https://publicsuffix.org). Trying to approximate this by simply taking the last label will not work well for effective TLDs such as "co.uk".<br><br>type: keyword<br><br>example: `co.uk` | extended |

## Field reuse [_field_reuse]

The `source` fields are expected to be nested at:

* `process.entry_meta.source`

Note also that the `source` fields may be used directly at the root of the events.


### Field sets that can be nested under Source [ecs-source-nestings]

| Location | Field Set | Description |
| --- | --- | --- |
| `source.as.*` | [as](/reference/ecs-as.md) | Fields describing an Autonomous System (Internet routing prefix). |
| `source.geo.*` | [geo](/reference/ecs-geo.md) | Fields describing a location. |
| `source.user.*` | [user](/reference/ecs-user.md) | Fields to describe the user relevant to the event. |
