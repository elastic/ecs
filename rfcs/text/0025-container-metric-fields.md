# 0025: Container Metric Fields
<!-- Leave this ID at 0000. The ECS team will assign a unique, contiguous RFC number upon merging the initial stage of this RFC. -->

- Stage: **3 (draft)** <!-- Update to reflect target stage. See https://elastic.github.io/ecs/stages.html -->
- Date: **2022-03-02** <!-- The ECS team sets this date at merge time. This is the date of the latest stage advancement. -->

<!--
As you work on your RFC, use the "Stage N" comments to guide you in what you should focus on, for the stage you're targeting.
Feel free to remove these comments as you go along.
-->

<!--
Stage 0: Provide a high level summary of the premise of these changes. Briefly describe the nature, purpose, and impact of the changes. ~2-5 sentences.
-->

<!--
Stage 1: If the changes include field additions or modifications, please create a folder titled as the RFC number under rfcs/text/. This will be where proposed schema changes as standalone YAML files or extended example mappings and larger source documents will go as the RFC is iterated upon.
-->

This RFC proposes 6 additional container metric fields into ECS for monitoring
container CPU, memory, disk and network performance:
- container.cpu.usage
- container.memory.usage
- container.network.ingress.bytes
- container.network.egress.bytes
- container.disk.read.bytes
- container.disk.write.bytes

With existing metadata fields `container.id`, `container.image.name`, `container.image.tag`,
`container.labels`, `container.name` and `container.runtime`, these total 12
fields will become the common field schema for container metrics. These metric
fields and metadata fields are recommended or required for all events related to
containers.

## Fields

This RFC calls for the addition of metric fields to collect basic monitoring
metrics from a container such as CPU, memory, network and disk.
Please see [`container.yml`](0000/container.yml) for definitions of all fields.

<!--
Stage 1: Describe at a high level how this change affects fields. Include new or updated yml field definitions for all of the essential fields in this draft. While not exhaustive, the fields documented here should be comprehensive enough to deeply evaluate the technical considerations of this change. The goal here is to validate the technical details for all essential fields and to provide a basis for adding experimental field definitions to the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

<!--
Stage 2: Add or update all remaining field definitions. The list should now be exhaustive. The goal here is to validate the technical details of all remaining fields and to provide a basis for releasing these field definitions as beta in the schema. Use GitHub code blocks with yml syntax formatting, and add them to the corresponding RFC folder.
-->

## Usage

Container metric fields and container metadata fields can be collected from
several sources. For example, a user who uses both Docker, Cloudfoundry
and AWS Fargate would like to collect data regarding all containers and store
them in a centralized location. Without these new container metric fields,
Metricbeat is reporting container metrics under different names from different
sources. For example, for CPU usage, `docker.cpu.total.pct` is used. For
Cloudfoundry, `cloudfoundry.container.cpu.pct` is used and for AWS Fargate,
`awsfargate.task_stats.cpu.total.pct` is used.
With these different field names, Kibana Docker containers metrics UI can only
display data collected from Docker but no other sources.

With the additional container metric fields proposed here, users should be able
to see the same metric field collected from different sources and Kibana should
be able to display all containers, not only from Docker, but also Cloudfoundry,
AWS Fargate and etc.

<!--
Stage 1: Describe at a high-level how these field changes will be used in practice. Real world examples are encouraged. The goal here is to understand how people would leverage these fields to gain insights or solve problems. ~1-3 paragraphs.
-->

## Source data

- Docker
- Kubernetes
- AWS Fargate
- Cloudfoundry
- Google GKE
- Containerd

<!--
Stage 1: Provide a high-level description of example sources of data. This does not yet need to be a concrete example of a source document, but instead can simply describe a potential source (e.g. nginx access log). This will ultimately be fleshed out to include literal source examples in a future stage. The goal here is to identify practical sources for these fields in the real world. ~1-3 sentences or unordered list.
-->

<!--
Stage 2: Included a real world example source document. Ideally this example comes from the source(s) identified in stage 1. If not, it should replace them. The goal here is to validate the utility of these field changes in the context of a real world example. Format with the source name as a ### header and the example document in a GitHub code block with json formatting, or if on the larger side, add them to the corresponding RFC folder.
-->

<!--
Stage 3: Add more real world example source documents so we have at least 2 total, but ideally 3. Format as described in stage 2.
-->

### Kubernetes

#### Original log

```json
{
  "node": {
    "nodeName": "gke-beats-default-pool-a5b33e2e-hdww",
    "systemContainers": [
      {
        "name": "kubelet",
        "startTime": "2021-12-20T09:53:30.156Z",
        "cpu": {
          "time": "2021-12-20T09:53:30.156Z",
          "usageNanoCores": 11263994,
          "usageCoreNanoSeconds": 2357800908948
        },
        "memory": {
          "time": "2021-12-20T09:53:30.156Z",
          "usageBytes": 36683776,
          "workingSetBytes": 36495360,
          "rssBytes": 35512320,
          "pageFaults": 100835242,
          "majorPageFaults": 0
        },
        "userDefinedMetrics": null
      }
    ],
    "startTime": "2021-12-20T09:53:30.156Z",
    "cpu": {
      "time": "2021-12-20T09:53:30.156Z",
      "usageNanoCores": 18691146,
      "usageCoreNanoSeconds": 4189523881380
    },
    "memory": {
      "time": "2021-12-20T09:53:30.156Z",
      "availableBytes": 1768316928,
      "usageBytes": 2764943360,
      "workingSetBytes": 2111090688,
      "rssBytes": 2150400,
      "pageFaults": 131567,
      "majorPageFaults": 103
    },
    "network": {
      "time": "2021-12-20T09:53:30.156Z",
      "rxBytes": 1115133198,
      "rxErrors": 0,
      "txBytes": 812729002,
      "txErrors": 0
    },
    "fs": {
      "availableBytes": 98727014400,
      "capacityBytes": 101258067968,
      "usedBytes": 2514276352,
      "inodesFree": 18446744073709551615,
      "inodes": 6258720,
      "inodesUsed": 138624
    },
    "runtime": {
      "imageFs": {
        "availableBytes": 98727014400,
        "capacityBytes": 101258067968,
        "usedBytes": 860204379,
        "inodesFree": 18446744073709551615,
        "inodes": 6258720,
        "inodesUsed": 138624
      }
    }
  },
  "pods": [
    {
      "podRef": {
        "name": "nginx-deployment-2303442956-pcqfc",
        "namespace": "default",
        "uid": "beabc196-2456-11e7-a3ad-42010a840235"
      },
      "startTime": "2021-12-20T09:53:30.156Z",
      "containers": [
        {
          "name": "nginx",
          "startTime": "2017-04-18T16:47:44Z",
          "cpu": {
            "time": "2017-04-20T08:06:34Z",
            "usageNanoCores": 11263994,
            "usageCoreNanoSeconds": 43959424
          },
          "memory": {
            "time": "2017-04-20T08:06:34Z",
            "usageBytes": 1462272,
            "workingSetBytes": 1454080,
            "rssBytes": 1409024,
            "pageFaults": 841,
            "majorPageFaults": 0
          },
          "rootfs": {
            "availableBytes": 98727014400,
            "capacityBytes": 101258067968,
            "usedBytes": 61440,
            "inodesFree": 6120096,
            "inodes": 6258720,
            "inodesUsed": 21
          },
          "logs": {
            "availableBytes": 98727014400,
            "capacityBytes": 101258067968,
            "usedBytes": 28672,
            "inodesFree": 6120096,
            "inodes": 6258720,
            "inodesUsed": 138624
          },
          "userDefinedMetrics": null
        }
      ],
      "network": {
        "time": "2021-12-20T09:53:30.156Z",
        "rxBytes": 107056,
        "rxErrors": 0,
        "txBytes": 72447,
        "txErrors": 0
      },
      "volume": [
        {
          "availableBytes": 1939689472,
          "capacityBytes": 1939701760,
          "usedBytes": 12288,
          "inodesFree": 473551,
          "inodes": 473560,
          "inodesUsed": 9,
          "name": "default-token-sg8x5"
        }
      ]
    }
  ]
}
```

#### Mapped event

```json
{
  "container": {
    "cpu.usage":          0.005631997,
    "memory.usage":       0.01,
    "name": "nginx",
    "network.ingress.bytes": 107056,
    "network.egress.bytes": 72447
  },
  "kubernetes": {
    "container": {
      "start_time": "2021-12-20T09:53:30.156Z",
      "memory": {
        "rss": {
          "bytes": 1409024
        },
        "majorpagefaults": 0,
        "usage": {
          "node": {
            "pct": 0.01
          },
          "bytes": 1462272,
          "limit": {
            "pct": 0.1
          }
        },
        "available": {
          "bytes": 0
        },
        "workingset": {
          "bytes": 1454080,
          "limit": {
            "pct": 0.09943977591036414
          }
        },
        "pagefaults": 841
      },
      "rootfs": {
        "inodes": {
          "used": 21
        },
        "available": {
          "bytes": 98727014400
        },
        "used": {
          "bytes": 61440
        },
        "capacity": {
          "bytes": 101258067968
        }
      },
      "name": "nginx",
      "cpu": {
        "usage": {
          "core": {
            "ns": 43959424
          },
          "node": {
            "pct": 0.005631997
          },
          "limit": {
            "pct": 0.005631997
          },
          "nanocores": 11263994
        }
      },
      "logs": {
        "inodes": {
          "count": 13107200,
          "used": 2,
          "free": 10806621
        },
        "available": {
          "bytes": 138514030592
        },
        "used": {
          "bytes": 446464
        },
        "capacity": {
          "bytes": 211108732928
        }
      }
    }
  },
  "@timestamp": "2021-12-20T09:53:30.156Z",
  "ecs": {
    "version": "8.0.0"
  },
  "metricset": {
    "period": 10000,
    "name": "container"
  },
  "event": {
    "duration": 156057406,
    "agent_id_status": "verified",
    "ingested": "2021-12-20T09:53:30Z",
    "module": "kubernetes",
    "dataset": "kubernetes.container"
  }
}
```

### Docker

#### Original log

```json
{
  "blkio_stats": {
    "io_merged_recursive": [],
    "io_queue_recursive": [],
    "io_service_bytes_recursive": [
      {
        "major": 8,
        "minor": 0,
        "op": "Read",
        "value": 311296
      },
      {
        "major": 8,
        "minor": 0,
        "op": "Write",
        "value": 283956224
      },
      {
        "major": 8,
        "minor": 0,
        "op": "Sync",
        "value": 284267520
      },
      {
        "major": 8,
        "minor": 0,
        "op": "Async",
        "value": 0
      },
      {
        "major": 8,
        "minor": 0,
        "op": "Discard",
        "value": 0
      },
      {
        "major": 8,
        "minor": 0,
        "op": "Total",
        "value": 284267520
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Read",
        "value": 311296
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Write",
        "value": 283956224
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Sync",
        "value": 284267520
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Async",
        "value": 0
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Discard",
        "value": 0
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Total",
        "value": 284267520
      }
    ],
    "io_service_time_recursive": [],
    "io_serviced_recursive": [
      {
        "major": 8,
        "minor": 0,
        "op": "Read",
        "value": 10
      },
      {
        "major": 8,
        "minor": 0,
        "op": "Write",
        "value": 3469
      },
      {
        "major": 8,
        "minor": 0,
        "op": "Sync",
        "value": 3479
      },
      {
        "major": 8,
        "minor": 0,
        "op": "Async",
        "value": 0
      },
      {
        "major": 8,
        "minor": 0,
        "op": "Discard",
        "value": 0
      },
      {
        "major": 8,
        "minor": 0,
        "op": "Total",
        "value": 3479
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Read",
        "value": 10
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Write",
        "value": 2394
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Sync",
        "value": 2404
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Async",
        "value": 0
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Discard",
        "value": 0
      },
      {
        "major": 253,
        "minor": 0,
        "op": "Total",
        "value": 2404
      }
    ],
    "io_time_recursive": [],
    "io_wait_time_recursive": [],
    "sectors_recursive": []
  },
  "cpu_stats": {
    "cpu_usage": {
      "percpu_usage": [
        8989285945449,
        8802991575246,
        8723071634953,
        8812077512624
      ],
      "total_usage": 35327426668272,
      "usage_in_kernelmode": 2720580000000,
      "usage_in_usermode": 32477900000000
    },
    "online_cpus": 4,
    "system_cpu_usage": 7640294590000000,
    "throttling_data": {
      "periods": 0,
      "throttled_periods": 0,
      "throttled_time": 0
    }
  },
  "id": "86a4d10d07bf0b1ded54c7156b4362e8b0dba9d450201a9695b4714c1492829c",
  "memory_stats": {
    "limit": 15620788224,
    "max_usage": 420536320,
    "stats": {
      "active_anon": 59502592,
      "active_file": 63746048,
      "cache": 194330624,
      "dirty": 0,
      "hierarchical_memory_limit": 9223372036854771712,
      "hierarchical_memsw_limit": 9223372036854771712,
      "inactive_anon": 60268544,
      "inactive_file": 130256896,
      "mapped_file": 123408384,
      "pgfault": 37852947,
      "pgmajfault": 0,
      "pgpgin": 25772802,
      "pgpgout": 25697155,
      "rss": 119738368,
      "rss_huge": 4194304,
      "total_active_anon": 59502592,
      "total_active_file": 63746048,
      "total_cache": 194330624,
      "total_dirty": 0,
      "total_inactive_anon": 60268544,
      "total_inactive_file": 130256896,
      "total_mapped_file": 123408384,
      "total_pgfault": 37852947,
      "total_pgmajfault": 0,
      "total_pgpgin": 25772802,
      "total_pgpgout": 25697155,
      "total_rss": 119738368,
      "total_rss_huge": 4194304,
      "total_unevictable": 0,
      "total_writeback": 0,
      "unevictable": 0,
      "writeback": 0
    },
    "usage": 326488064
  },
  "name": "/elastic-package-stack_elastic-agent_1",
  "networks": {
    "eth0": {
      "rx_bytes": 23962833,
      "rx_dropped": 0,
      "rx_errors": 0,
      "rx_packets": 128811,
      "tx_bytes": 593646535,
      "tx_dropped": 0,
      "tx_errors": 0,
      "tx_packets": 186477
    }
  },
  "num_procs": 0,
  "pids_stats": {
    "current": 68
  },
  "precpu_stats": {
    "cpu_usage": {
      "percpu_usage": [
        8989283978798,
        8802978152064,
        8723042900675,
        8812068229234
      ],
      "total_usage": 35327373260771,
      "usage_in_kernelmode": 2720550000000,
      "usage_in_usermode": 32477870000000
    },
    "online_cpus": 4,
    "system_cpu_usage": 7640290600000000,
    "throttling_data": {
      "periods": 0,
      "throttled_periods": 0,
      "throttled_time": 0
    }
  },
  "preread": "2021-02-04T22:02:38.129030814Z",
  "read": "2021-02-04T22:02:39.138448063Z",
  "storage_stats": {}
}
```

#### Mapped event by docker.cpu dataset

```json
{
  "@timestamp": "2017-10-12T08:05:34.853Z",
  "container": {
    "id": "7f3ca1f1b2b310362e90f700d2b2e52ebd46ef6ddf10c0704f22b25686c466ab",
    "image": {
      "name": "metricbeat_beat"
    },
    "name": "metricbeat_beat_run_8ba23fa682a6",
    "runtime": "docker",
    "cpu": {
      "usage": 0.015459536757425743
    }
  },
  "docker": {
    "cpu": {
      "kernel": {
        "norm": {
          "pct": 0.007425742574257425
        },
        "pct": 0.0594059405940594,
        "ticks": 26810000000
      },
      "system": {
        "norm": {
          "pct": 1
        },
        "pct": 8,
        "ticks": 65836400000000
      },
      "total": {
        "norm": {
          "pct": 0.015459536757425743
        },
        "pct": 0.12367629405940594
      },
      "user": {
        "norm": {
          "pct": 0.006188118811881188
        },
        "pct": 0.04950495049504951,
        "ticks": 35720000000
      }
    }
  },
  "event": {
    "dataset": "docker.cpu",
    "duration": 115000,
    "module": "docker"
  },
  "metricset": {
    "name": "cpu",
    "period": 10000
  },
  "service": {
    "address": "/var/run/docker.sock",
    "type": "docker"
  }
}
```

#### Mapped event by docker.memory dataset
```json
{
    "@timestamp": "2017-10-12T08:05:34.853Z",
    "container": {
        "id": "aa41902101351f415e6e983b0673c0ba715dd4bc316bd5fc0ebd6fcf94287f86",
        "image": {
            "name": "redis:latest"
        },
        "name": "amazing_cohen",
        "runtime": "docker",
        "memory": {
          "usage": 0.000672283359618831
        }
    },
    "docker": {
        "memory": {
            "fail": {
                "count": 0
            },
            "limit": 2095878144,
            "rss": {
                "pct": 0.0004025882909345325,
                "total": 843776
            },
            "stats": {
                "active_anon": 421888,
                "active_file": 36864,
                "cache": 86016,
                "dirty": 0,
                "hierarchical_memory_limit": 9223372036854771712,
                "hierarchical_memsw_limit": 9223372036854771712,
                "inactive_anon": 421888,
                "inactive_file": 49152,
                "mapped_file": 53248,
                "pgfault": 1587,
                "pgmajfault": 1,
                "pgpgin": 2426,
                "pgpgout": 2199,
                "rss": 843776,
                "rss_huge": 0,
                "total_active_anon": 421888,
                "total_active_file": 36864,
                "total_cache": 86016,
                "total_dirty": 0,
                "total_inactive_anon": 421888,
                "total_inactive_file": 49152,
                "total_mapped_file": 53248,
                "total_pgfault": 1587,
                "total_pgmajfault": 1,
                "total_pgpgin": 2426,
                "total_pgpgout": 2199,
                "total_rss": 843776,
                "total_rss_huge": 0,
                "total_unevictable": 0,
                "total_writeback": 0,
                "unevictable": 0,
                "writeback": 0
            },
            "usage": {
                "max": 7860224,
                "pct": 0.000672283359618831,
                "total": 1409024
            }
        }
    },
    "event": {
        "dataset": "docker.memory",
        "duration": 115000,
        "module": "docker"
    },
    "metricset": {
        "name": "memory"
    },
    "service": {
        "address": "/var/run/docker.sock",
        "type": "docker"
    }
}
```

#### Mapped event by docker.network dataset
```json
{
    "@timestamp": "2017-10-12T08:05:34.853Z",
    "agent": {
        "hostname": "host.example.com",
        "name": "host.example.com"
    },
    "container": {
      "id": "cc78e58acfda4501105dc4de8e3ae218f2da616213e6e3af168c40103829302a",
      "image": {
        "name": "metricbeat_elasticsearch"
      },
      "name": "metricbeat_elasticsearch_1_df866b3a7b3d",
      "runtime": "docker",
      "network": {
        "ingress": {
          "bytes": 23047
        },
        "egress": {
          "bytes": 0
        }
      }
    },
    "docker": {
        "network": {
            "in": {
                "bytes": 0,
                "dropped": 0,
                "errors": 0,
                "packets": 0
            },
            "inbound": {
                "bytes": 23047,
                "dropped": 0,
                "errors": 0,
                "packets": 241
            },
            "interface": "eth0",
            "out": {
                "bytes": 0,
                "dropped": 0,
                "errors": 0,
                "packets": 0
            },
            "outbound": {
                "bytes": 0,
                "dropped": 0,
                "errors": 0,
                "packets": 0
            }
        }
    },
    "event": {
        "dataset": "docker.network",
        "duration": 115000,
        "module": "docker"
    },
    "metricset": {
        "name": "network"
    },
    "service": {
        "address": "/var/run/docker.sock",
        "type": "docker"
    }
}
```

## Scope of impact

<!--
Stage 2: Identifies scope of impact of changes. Are breaking changes required? Should deprecation strategies be adopted? Will significant refactoring be involved? Break the impact down into:
 * Ingestion mechanisms (e.g. beats/logstash)
 * Usage mechanisms (e.g. Kibana applications, detections)
 * ECS project (e.g. docs, tooling)
The goal here is to research and understand the impact of these changes on users in the community and development teams across Elastic. 2-5 sentences each.
-->

This is a new field set, and the changes introduced will not affect existing ECS implementations.

Integrations or other data sources mapping to ECS will need to map their original events to the new fields as well.

The new field names will allow Kibana Docker containers metrics UI to
display data collected from different container sources, therefore it should be renamed to
a more generic title.
Currently, it can only display data from Docker.
## Concerns

<!--
Stage 1: Identify potential concerns, implementation challenges, or complexity. Spend some time on this. Play devil's advocate. Try to identify the sort of non-obvious challenges that tend to surface later. The goal here is to surface risks early, allow everyone the time to work through them, and ultimately document resolution for posterity's sake.
-->

We need to carefully define each field because when collecting these container
metrics from different sources, the scope of these metrics change. We should
make sure when users are using these metrics, they are all collected to represent
the same thing. For example, `container.cpu.usage` needs to be a normalized value
between 0 and 1.

We need to carefully distinguish metrics of containers with the metrics coming from the host
where these containers are running. For example, events from Kubernetes contain information for
both the container and the host(kubernetes node)(e.g., `container.id` and `host.id`).
For that reason host metrics should be stored under `host.*` while container metrics should be stored
under `container.*`.

<!--
Stage 2: Document new concerns or resolutions to previously listed concerns. It's not critical that all concerns have resolutions at this point, but it would be helpful if resolutions were taking shape for the most significant concerns.
-->

<!--
Stage 3: Document resolutions for all existing concerns. Any new concerns should be documented along with their resolution. The goal here is to eliminate risk of churn and instability by ensuring all concerns have been addressed.
-->

## People

The following are the people that consulted on the contents of this RFC.

* @kaiyan-sheng | author
* @cyrille-leclerc | sponsor
* @jsoriano | subject matter expert

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

Common Fields for Container Inventory Schema: https://github.com/elastic/beats/issues/22179

### RFC Pull Requests

<!-- An RFC should link to the PRs for each of it stage advancements. -->

* Stage 0: https://github.com/elastic/ecs/pull/1441
    * Stage 0 date correction: https://github.com/elastic/ecs/pull/1447

<!--
* Stage 1: https://github.com/elastic/ecs/pull/NNN
...
-->
* Stage 1: https://github.com/elastic/ecs/pull/1529

* Stage 2: https://github.com/elastic/ecs/pull/1747
