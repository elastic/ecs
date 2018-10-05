## Metricbeat use case

ECS fields used Metricbeat.

### <a name="metricbeat"></a> Metricbeat fields


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="id"></a>*id*  | *Unique id to describe the event.*  | keyword  |   | `8a4f500d`  |
| <a name="timestamp"></a>*timestamp*  | *Timestamp when the event was created.*  | date  |   | `2016-05-23T08:05:34.853Z`  |
| [agent.version](https://github.com/elastic/ecs#agent.version)  | Beat version.  | keyword  |   | `6.0.0-rc2`  |
| [agent.name](https://github.com/elastic/ecs#agent.name)  | Beat name.  | keyword  |   | `filebeat`  |
| [agent.id](https://github.com/elastic/ecs#agent.id)  | Unique beat identifier.  | keyword  |   | `8a4f500d`  |
| <a name="service.&ast;"></a>*service.&ast;*  | *The service fields describe the service for / from which the data was collected.<br/>If logs or metrics are collected from Redis, `service.name` would be `redis`. This allows to find and correlate logs for a specicic service or even version with `service.version`.<br/>*  |   |   |   |
| [service.id](https://github.com/elastic/ecs#service.id)  | Unique identifier of the running service.<br/>This id should uniquely identify this service. This makes it possible to correlate logs and metrics for one specific service. For example in case of issues with one redis instance, it's possible to filter on the id to see metrics and logs for this single instance.  | keyword  |   | `d37e5ebfe0ae6c4972dbe9f0174a1637bb8247f6`  |
| [service.name](https://github.com/elastic/ecs#service.name)  | Name of the service data is collected from.<br/>The name is normally the same as the module name.  | keyword  |   | `elasticsearch`  |
| [service.version](https://github.com/elastic/ecs#service.version)  | Version of the service the data was collected from.<br/>This allows to look at a data set only for a specific version of a service.  | keyword  |   | `3.2.4`  |
| <a name="service.host"></a>*service.host*  | *Host address that is used to connect to the service.<br/>This normally contains hostname + port.<br/>REVIEW: Should this be service.uri instead, sometimes it's more then just the host? It could also include a path or the protocol.*  | keyword  |   | `elasticsearch:9200`  |
| <a name="request.rtt"></a>*request.rtt*  | *Request round trip time.<br/>How long did the request take to fetch metrics from the service.<br/>REVIEW: THIS DOES NOT EXIST YET IN ECS.*  | long  |   | `115`  |
| <a name="error.&ast;"></a>*error.&ast;*  | *Error namespace<br/>Use for errors which can happen during fetching information for a service.<br/>*  |   |   |   |
| [error.message](https://github.com/elastic/ecs#error.message)  | Error message returned by the service during fetching metrics.  | text  |   |   |
| [error.code](https://github.com/elastic/ecs#error.code)  | Error code returned by the service during fetching metrics.  | keyword  |   |   |
| [host.name](https://github.com/elastic/ecs#host.name)  | Hostname of the system metricbeat is running on or user defined name.  | keyword  |   |   |
| <a name="host.timezone.offset.sec"></a>*host.timezone.offset.sec*  | *Timezone offset of the host in seconds.*  | long  |   |   |
| [host.id](https://github.com/elastic/ecs#host.id)  | Unique host id.  | keyword  |   |   |
| [event.module](https://github.com/elastic/ecs#event.module)  | Name of the module this data is coming from.  | keyword  |   | `mysql`  |
| [event.dataset](https://github.com/elastic/ecs#event.dataset)  | Name of the dataset.<br/>This contains the information which is currently stored in metricset.name and metricset.module.  | keyword  |   | `stats`  |



