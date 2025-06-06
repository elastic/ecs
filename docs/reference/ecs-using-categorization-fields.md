---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-using-the-categorization-fields.html
applies_to:
  stack: all
  serverless: all
---

# Using the categorization fields [ecs-using-the-categorization-fields]

The event categorization fields work together to identify and group similar events from multiple data sources.

These general principles can help guide the categorization process:

* Events from multiple data sources that are similar enough to be viewed or analyzed together, should fall into the same `event.category` field.
* Both `event.category` and `event.type` are arrays and may be populated with multiple allowed values, if the event can be reasonably classified into more than one category and/or type.
* `event.kind`, `event.category`, `event.type` and `event.outcome` all have allowed values. This is to normalize these fields. Values that aren’t in the list of allowed values should not be used.
* Values of `event.outcome` are a very limited set to indicate success or failure. Domain-specific actions, such as deny and allow, that could be considered outcomes are not captured in the `event.outcome` field, but rather in the `event.type` and/or `event.action` fields.
* Values of `event.category`, `event.type`, and `event.outcome` are consistent across all values of `event.kind`.
* When a specific event doesn’t fit into any of the defined allowed categorization values, the field should be left empty.

The following examples detail populating the categorization fields and provides some context for the classification decisions.


### Firewall blocking a network connection [_firewall_blocking_a_network_connection]

This event from a firewall describes a successfully blocked network connection:

```json
...
  {
    "source": {
      "address": "10.42.42.42",
      "ip": "10.42.42.42",
      "port": 38842
    },
    "destination": {
      "address": "10.42.42.1",
      "ip": "10.42.42.1",
      "port": 443
    },
    "rule": {
      "name": "wan-lan",
      "id": "default"
    },
    ...
    "event": {
      "kind": "event", <1>
      "category": [ <2>
        "network"
      ],
      "type": [ <3>
        "connection",
        "denied"
      ],
      "outcome": "success", <4>
      "action": "dropped" <5>
    }
  }
...
```

1. Classifying as an `event`.
2. `event.category` categorizes this event as `network` activity.
3. The event was both an attempted network `connection` and was `denied`.
4. The blocking of this connection is expected. The outcome is a `success` from the perspective of the firewall emitting the event.
5. The firewall classifies this denied connection as `dropped`, and this value is captured in `event.action`.


A "denied" network connection could fall under different action values: "blocked", "dropped", "quarantined", etc. The `event.action` field captures the action taken as described by the source, and populating `event.type:denied` provides an independent, normalized value.

A single query will return all denied network connections which have been normalized with the same categorization values:

```sh
event.category:network AND event.type:denied
```


### Failed attempt to create a user account [_failed_attempt_to_create_a_user_account]

User `alice` attempts to add a user account, `bob`, into a directory service, but the action fails:

```json
{
  "user": {
    "name": "alice",
    "target": {
      "name": "bob"
    }
  },
  "event": {
    "kind": "event", <1>
    "category": [ <2>
      "iam"
    ],
    "type": [ <3>
      "user",
      "creation"
    ],
    "outcome": "failure" <4>
  }
}
```

1. Again classifying as an `event`.
2. Categorized using `iam` for an event user account activity.
3. Both `user` and `creation`
4. The creation of a user account was attempted, but it was not successful.



### Informational listing of a file [_informational_listing_of_a_file]

A utility, such as a file integrity monitoring (FIM) application, takes inventory of a file but does not access or modify the file:

```json
{
  "file": {
    "name": "example.png",
    "owner": "alice",
    "path": "/home/alice/example.png",
    "type": "file"
  },
  "event": {
    "kind": "event", <1>
    "category": [ <2>
      "file"
    ],
    "type": [ <3>
      "info"
    ]
  }
}
```

1. Classifying as `event`.
2. The event is reporting on a `file`.
3. The `info` type categorizes purely informational events. The target file here was not accessed or modified.


The source data didn’t include any context around the event’s outcome, so `event.outcome` should not be populated.


## Security application failed to block a network connection [_security_application_failed_to_block_a_network_connection]

An intrusion detection system (IDS) attempts to block a connection but fails. The event emitted by the IDS is considered an alert:

```json
{
  "source": {
      "address": "10.42.42.42",
      "ip": "10.42.42.42",
      "port": 38842
    },
  "destination": {
      "address": "10.42.42.1",
      "ip": "10.42.42.1",
      "port": 443
  },
  ...
  "event": {
    "kind": "alert", <1>
    "category": [ <2>
      "intrusion_detection",
      "network"
    ],
    "type": [ <3>
      "connection",
      "denied"
    ],
    "outcome": "failure" <4>
  }
}
```

1. The IDS emitted this event when a detection rule generated an alert. The `event.kind` is set to `alert`.
2. With the event emitted from a network IDS device, the event is categorized both as `network` and `intrusion_detection`.
3. The alert event is a `connection` that was `denied` by the IDS' configuration.
4. The IDS experienced an issue when attempting to deny the connection. Since the action taken by the IDS failed, the outcome is set as `failure`.


