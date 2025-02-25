---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-observer.html
applies_to:
  stack: all
  serverless: all
---

# Observer fields [ecs-observer]

An observer is defined as a special network, security, or application device used to detect, observe, or create network, security, or application-related events and metrics.

This could be a custom hardware appliance or a server that has been configured to run special network, security, or application software. Examples include firewalls, web proxies, intrusion detection/prevention systems, network monitoring sensors, web application firewalls, data loss prevention systems, and APM servers. The observer.* fields shall be populated with details of the system, if any, that detects, observes and/or creates a network, security, or application event or metric. Message queues and ETL components used in processing events or metrics are not considered observers in ECS.


## Observer field details [_observer_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-observer-egress$$$[observer.egress](#field-observer-egress) | Observer.egress holds information like interface number and name, vlan, and zone information to classify egress traffic.  Single armed monitoring such as a network sensor on a span port should only use observer.ingress to categorize traffic.<br><br>type: object<br> | extended |
| $$$field-observer-egress-zone$$$[observer.egress.zone](#field-observer-egress-zone) | Network zone of outbound traffic as reported by the observer to categorize the destination area of egress traffic, e.g. Internal, External, DMZ, HR, Legal, etc.<br><br>type: keyword<br><br>example: `Public_Internet`<br> | extended |
| $$$field-observer-hostname$$$[observer.hostname](#field-observer-hostname) | Hostname of the observer.<br><br>type: keyword<br> | core |
| $$$field-observer-ingress$$$[observer.ingress](#field-observer-ingress) | Observer.ingress holds information like interface number and name, vlan, and zone information to classify ingress traffic.  Single armed monitoring such as a network sensor on a span port should only use observer.ingress to categorize traffic.<br><br>type: object<br> | extended |
| $$$field-observer-ingress-zone$$$[observer.ingress.zone](#field-observer-ingress-zone) | Network zone of incoming traffic as reported by the observer to categorize the source area of ingress traffic. e.g. internal, External, DMZ, HR, Legal, etc.<br><br>type: keyword<br><br>example: `DMZ`<br> | extended |
| $$$field-observer-ip$$$[observer.ip](#field-observer-ip) | IP addresses of the observer.<br><br>type: ip<br><br>Note: this field should contain an array of values.<br> | core |
| $$$field-observer-mac$$$[observer.mac](#field-observer-mac) | MAC addresses of the observer.<br><br>The notation format from RFC 7042 is suggested: Each octet (that is, 8-bit byte) is represented by two [uppercase] hexadecimal digits giving the value of the octet as an unsigned integer. Successive octets are separated by a hyphen.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `["00-00-5E-00-53-23", "00-00-5E-00-53-24"]`<br> | core |
| $$$field-observer-name$$$[observer.name](#field-observer-name) | Custom name of the observer.<br><br>This is a name that can be given to an observer. This can be helpful for example if multiple firewalls of the same model are used in an organization.<br><br>If no custom name is needed, the field can be left empty.<br><br>type: keyword<br><br>example: `1_proxySG`<br> | extended |
| $$$field-observer-product$$$[observer.product](#field-observer-product) | The product name of the observer.<br><br>type: keyword<br><br>example: `s200`<br> | extended |
| $$$field-observer-serial-number$$$[observer.serial_number](#field-observer-serial-number) | Observer serial number.<br><br>type: keyword<br> | extended |
| $$$field-observer-type$$$[observer.type](#field-observer-type) | The type of the observer the data is coming from.<br><br>There is no predefined list of observer types. Some examples are `forwarder`, `firewall`, `ids`, `ips`, `proxy`, `poller`, `sensor`, `APM server`.<br><br>type: keyword<br><br>example: `firewall`<br> | core |
| $$$field-observer-vendor$$$[observer.vendor](#field-observer-vendor) | Vendor name of the observer.<br><br>type: keyword<br><br>example: `Symantec`<br> | core |
| $$$field-observer-version$$$[observer.version](#field-observer-version) | Observer version.<br><br>type: keyword<br> | core |


## Field reuse [_field_reuse_17]


### Field sets that can be nested under observer [ecs-observer-nestings]

| Location | Field Set | Description |
| --- | --- | --- |
| `observer.egress.interface.*` | [interface](/reference/ecs-interface.md) | Fields to describe observer interface information. |
| `observer.egress.vlan.*` | [vlan](/reference/ecs-vlan.md) | Fields to describe observed VLAN information. |
| `observer.geo.*` | [geo](/reference/ecs-geo.md) | Fields describing a location. |
| `observer.ingress.interface.*` | [interface](/reference/ecs-interface.md) | Fields to describe observer interface information. |
| `observer.ingress.vlan.*` | [vlan](/reference/ecs-vlan.md) | Fields to describe observed VLAN information. |
| `observer.os.*` | [os](/reference/ecs-os.md) | OS fields contain information about the operating system. |

