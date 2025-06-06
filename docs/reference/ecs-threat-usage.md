---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-threat-usage.html
applies_to:
  stack: all
  serverless: all
---

# Threat fields usage and examples [ecs-threat-usage]

The `threat.*` fields map threat indicators to ECS. The data helps detect malicious events with indicator match rules and enrichment.


## Indicators [ecs-threat-usage-indicators]

Threat intelligence indicators come from many sources in different structures. Normalize these indicators using the ECS threat.indicator.* fields.  Once normalized, consistently query indicators from various sources and build indicator match rules.

The below example is from an online database. It contains several network indicators from a known malware site.

```JSON
{
    "@timestamp": "2019-08-10T11:09:23.000Z",
    "event": {
        "kind": "enrichment", <1>
        "category": "threat", <2>
        "type": "indicator", <3>
        "severity": 7,
        "risk_score": 10.0,
    },
    "threat: {
        "indicator": { <4>
            "first_seen": "2020-11-05T17:25:47.000Z",
            "last_seen": "2020-11-05T17:25:47.000Z",
            "modified_at": "2020-11-05T17:25:47.000Z",
            "sightings": 10,
            "type": [
                "ipv4-addr",
                "port",
                "domain-name",
                "email-addr"
            ],
            "description": "Email address, domain, port, and IP address observed during an Angler EK campaign.",
            "provider": "Abuse.ch",
            "reference": "https://urlhaus.abuse.ch/url/abcdefg/",
            "confidence": "High",
            "ip": 1.2.3.4,
            "port": 443,
            "email.address": "phish@malicious.evil",
            "marking": {
                "tlp": "CLEAR"
            },
            "url": {
                "domain": "malicious.evil",
            },
            "scanner_stats": 4
        }
    },
    "related": { <5>
        "hosts": [
            "malicious.evil"
        ],
        "ip": [
            1.2.3.4
        ]
    }
}
```

1. Use the `enrichment` value for `event.kind`.
2. Use the `threat` value for `event.category`.
3. The event type is set to `indicator`.
4. Capture indicator details at `threat.indicator.*`.
5. Copy indicators to the relevant `related.*` fields.


The following example maps a file-based indicator.

```JSON
{
    "@timestamp": "2019-08-10T11:09:23.000Z",
    "event": {
        "kind": "enrichment",
        "category": "threat",
        "type": "indicator",
        "severity": 7,
        "risk_score": 10,
        },
    "threat": {
        "indicator": {
            "first_seen": "2020-11-05T17:25:47.000Z",
            "last_seen": "2020-11-05T17:25:47.000Z",
            "modified_at": "2020-11-05T17:25:47.000Z",
            "sightings": 10,
            "type": [
                "file" <1>
            ],
            "description": "Implant used during an Angler EK campaign.",
            "provider": "Abuse.ch",
            "reference": "https://bazaar.abuse.ch/sample/f3ec9a2f2766c6bcf8c2894a9927c227649249ac146aabfe8d26b259be7d7055",
            "confidence": "High",
            "file": { <2>
                "hash": {
                    "sha256": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4",
                     "md5": "1eee2bf3f56d8abed72da2bc523e7431"
                },
                "size": 656896,
                "name": "invoice.doc"
                },
            "marking": {
                "tlp": "CLEAR"
            },
            "scanner_stats": 4
        }
    },
    "related": { <3>
        "hash": [
            "1eee2bf3f56d8abed72da2bc523e7431",
            "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4"
        ]
    }
}
```

1. Use the `file` value for `threat.indicator.type`.
2. Capture file attributes at `threat.indicator.file.*`.
3. Again, populate the `related.hash` field with the file hashes.



## Enrichments [ecs-threat-usage-enrichments]

Event enrichment searches for known threats using an event’s values and, if found, adds those associated details.

```JSON
{
  "process": {
    "name": "svchost.exe",
    "pid": 1644,
    "entity_id": "MDgyOWFiYTYtMzRkYi1kZTM2LTFkNDItMzBlYWM3NDVlOTgwLTE2NDQtMTMyNDk3MTA2OTcuNDc1OTExNTAw",
    "executable": "C:\\Windows\\System32\\svchost.exe"
  },
  "message": "Endpoint file event",
  "@timestamp": "2020-11-17T19:07:46.0956672Z",
  "file": {
    "path": "C:\\Windows\\Prefetch\\SVCHOST.EXE-AE7DB802.pf",
    "extension": "pf",
    "name": "SVCHOST.EXE-AE7DB802.pf",
    "hash": {
      "sha256": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4"
    }
  },
  "threat": {
    "enrichments": [ <1>
      {
        "indicator": {
          "marking": {
            "tlp": "CLEAR"
          },
          "first_seen": "2020-11-17T19:07:46.0956672Z",
          "file": {
            "hash": {
              "sha256": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4",
              "md5": "1eee2bf3f56d8abed72da2bc523e7431"
            },
            "size": 656896,
            "name": "invoice.doc"
          },
          "last_seen": "2020-11-17T19:07:46.0956672Z",
          "reference": "https://system.example.com/event/#0001234",
          "sightings": 4,
          "type": [
              "sha256",
              "md5",
              "file_name",
              "file_size"
        ],
          "description": "file last associated with delivering Angler EK"
        },
        "matched": { <2>
          "atomic": "0c415dd718e3b3728707d579cf8214f54c2942e964975a5f925e0b82fea644b4",
          "field": "file.hash.sha256",
          "id": "abc123f03",
          "index": "threat-indicators-index-000001",
          "type": "indicator_match_rule"
        }
      }
    ]
  }
}
```

1. Add each enrichment to a nested object under `threat.enrichments.*`.
2. The `matched` object provides context about the indicators this event matched on.


