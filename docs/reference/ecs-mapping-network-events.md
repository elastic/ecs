---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-mapping-network-events.html
applies_to:
  stack: all
  serverless: all
---

# Mapping network events [ecs-mapping-network-events]

Network events capture the details of one device communicating with another. The initiator is referred to as the source, and the recipient as the destination. Depending on the data source, a network event can contain details of addresses, protocols, headers, and device roles.

This guide describes the different field sets available for network-related events in ECS and provides direction on the ECS best practices for mapping to them.


### Source and destination baseline [_source_and_destination_baseline]

When an event contains details about the sending and receiving hosts, the baseline for capturing these values will be the [source](/reference/ecs-source.md) and [destination](/reference/ecs-destination.md) fields.

Some events may also indicate each host’s role in the exchange: client or server. When this information is available, the [client](/reference/ecs-client.md) and [server](/reference/ecs-server.md) fields should be used *in addition to* the `source` and `destination` fields. The fields and values mapped under `source`/`destination` should be copied under `client`/`server`.


### Network event mapping example [_network_event_mapping_example]

Below is a DNS network event. The source device (`192.168.86.222`) makes a DNS query, acting as the client and the DNS server is the destination (`192.168.86.1`).

Note this event contains additional details that would populate additional fields (such as the [DNS Fields](/reference/ecs-dns.md)) if this was a complete mapping example. These additional fields are omitted here to focus on the network details.

```json
{
  "ts":1599775747.53056,
  "uid":"CYqFPH3nOAa0kPxA0d",
  "id.orig_h":"192.168.86.222",
  "id.orig_p":54162,
  "id.resp_h":"192.168.86.1",
  "id.resp_p":53,
  "proto":"udp",
  "trans_id":28899,
  "rtt":0.02272200584411621,
  "query":"example.com",
  "qclass":1,
  "qclass_name":"C_INTERNET",
  "qtype":1,
  "qtype_name":"A",
  "rcode":0,
  "rcode_name":"NOERROR",
  "AA":false,
  "TC":false,
  "RD":true,
  "RA":true,
  "Z":0,
  "answers":["93.184.216.34"],
  "TTLs":[21209.0],
  "rejected":false
}
```


### Source and destination fields [_source_and_destination_fields]

First, the `source.*` and `destination.*` field sets are populated:

```json
  "source": {
    "ip": "192.168.86.222",
    "port": 54162
  }
```

```json
  "destination": {
    "ip": "192.168.86.1",
    "port": 53
  }
```


### Client and server fields [_client_and_server_fields]

Looking back at the original event, it shows the source device is the DNS client and the destination device is the DNS server. The values mapped under `source` and `destination` are copied and mapped under `client` and `server`, respectively:

```json
  "client": {
    "ip": "192.168.86.222",
    "port": 54162
  }
```

```json
  "server": {
    "ip": "192.168.86.1",
    "port": 53
  }
```

Mapping both pairs of field sets gives query visibility of the same network transaction in two ways.

* `source.ip:192.168.86.222` returns all events sourced from `192.168.86.222`, regardless its role in a transaction
* `client.ip:192.168.86.222` returns all events with host `192.168.86.222` acting as a client

The same applies for the `destination` and `server` fields:

* `destination.ip:192.168.86.1` returns all events destined to `192.168.86.1`
* `server.ip:192.168.86.1` returns all events with `192.168.86.1` acting as the server

It’s important to note that while the values for the `source` and `destination` fields may reverse between events in a single network transaction, the values for `client` and `server` typically will not. The following two tables demonstrate how two DNS transactions involving two clients and one server would map to `source.ip`/`destination.ip` vs. `client.ip`/`server.ip`:

| source.ip | destination.ip | event |
| --- | --- | --- |
| 192.168.86.222 | 192.168.86.1 | DNS query request 1 |
| 192.168.86.1 | 192.168.86.222 | DNS answer response 1 |
| 192.168.86.42 | 192.168.86.1 | DNS answer request 2 |
| 192.168.86.1 | 192.168.86.42 | DNS answer request 2 |

| client.ip | server.ip | event |
| --- | --- | --- |
| 192.168.86.222 | 192.168.86.1 | DNS query request 1 |
| 192.168.86.222 | 192.168.86.1 | DNS answer response 1 |
| 192.168.86.42 | 192.168.86.1 | DNS query request 2 |
| 192.168.86.42 | 192.168.86.1 | DNS answer response 2 |


## Related fields [_related_fields_2]

The `related.ip` field captures all the IPs present in the event in a single array:

```json
  "related": {
    "ip": [
      "192.168.86.222",
      "192.168.86.1",
      "93.184.216.34"
    ]
  }
```

The [related fields](/reference/ecs-related.md) are meant to facilitate pivoting. Since these IP addresses can appear in many different fields (`source.ip`, `destination.ip`, `client.ip`, `server.ip`, etc.), you can search for the IP trivially no matter what field it appears using a single query, e.g. `related.ip:192.168.86.222`.

Network events are not only limited to using `related.ip`. If hostnames or other host identifiers were present in the event, `related.hosts` should be populated too.


### Categorization using event fields [_categorization_using_event_fields]

When considering the [event categorization fields](/reference/ecs-category-field-values-reference.md), the `category` and `type` fields are populated using their respective allowed values which best classify the source network event.

```json
  "event": {
    "category": [
      "network"
    ],
    "type": [
      "connection",
      "protocol"
    ],
    "kind": "event"
  }
```

Most [event.category](/reference/ecs-allowed-values-event-category.md)/[event.type](/reference/ecs-allowed-values-event-type.md) ECS pairings are complete on their own. However, the pairing of `event.category:network` and `event.type:protocol` is an exception. When these two fields/value pairs both used to categorize an event, the `network.protocol` field should also be populated:

```json
  "network": {
    "protocol": "dns",
    "type": "ipv4",
    "transport": "udp"
  }
```


### Result [_result]

Putting everything together covered so far, we have a final ECS-mapped event:

```json
{
  "event": {
    "category": [
      "network"
    ],
    "type": [
      "connection",
      "protocol"
    ],
    "kind": "event"
  },
  "network": {
    "protocol": "dns",
    "type": "ipv4",
    "transport": "udp"
  },
  "source": {
    "ip": "192.168.86.222",
    "port": 54162
  },
  "destination": {
    "ip": "192.168.86.1",
    "port": 53
  },
  "client": {
    "ip": "192.168.86.222",
    "port": 64734
  },
  "server": {
    "ip": "192.168.86.1",
    "port": 53
  },
  "related": {
    "ip": [
      "192.168.86.222",
      "192.168.86.1",
      "93.184.216.34"
    ]
  },
  "dns": { ... }, <1>
  "zeek": { "ts":1599775747.53056, ... } <2>
}
```

1. Again, not diving into the DNS fields here but included for completeness.
2. Original fields can optionally be kept around as custom fields.


