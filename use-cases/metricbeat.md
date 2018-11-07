## Metricbeat use case

ECS fields used Metricbeat.

### <a name="metricbeat"></a> Metricbeat fields


| Field  | Description  | Level  | Type  | Example  |
|---|---|---|---|---|
| <a name="id"></a>*id* | *Unique id to describe the event.* | (use case) | keyword | `8a4f500d` |
| <a name="timestamp"></a>*timestamp* | *Timestamp when the event was created.* | (use case) | date | `2016-05-23T08:05:34.853Z` |
| [agent.version](../README.md#agent.version)  | Beat version. | core | keyword | `6.0.0-rc2` |
| [agent.name](../README.md#agent.name)  | Beat name. | core | keyword | `filebeat` |
| [agent.id](../README.md#agent.id)  | Unique beat identifier. | core | keyword | `8a4f500d` |
| <a name="service.&ast;"></a>*service.&ast;* | *The service fields describe the service for / from which the data was collected.<br/>If logs or metrics are collected from Redis, `service.name` would be `redis`. This allows to find and correlate logs for a specicic service or even version with `service.version`.<br/>* |  |  |  |
| [service.id](../README.md#service.id)  | Unique identifier of the running service.<br/>This id should uniquely identify this service. This makes it possible to correlate logs and metrics for one specific service. For example in case of issues with one redis instance, it's possible to filter on the id to see metrics and logs for this single instance. | core | keyword | `d37e5ebfe0ae6c4972dbe9f0174a1637bb8247f6` |
| [service.name](../README.md#service.name)  | Name of the service data is collected from.<br/>The name is normally the same as the module name. | core | keyword | `elasticsearch` |
| [service.version](../README.md#service.version)  | Version of the service the data was collected from.<br/>This allows to look at a data set only for a specific version of a service. | core | keyword | `3.2.4` |
| <a name="service.host"></a>*service.host* | *Host address that is used to connect to the service.<br/>This normally contains hostname + port.<br/>REVIEW: Should this be service.uri instead, sometimes it's more then just the host? It could also include a path or the protocol.* | (use case) | keyword | `elasticsearch:9200` |
| <a name="request.rtt"></a>*request.rtt* | *Request round trip time.<br/>How long did the request take to fetch metrics from the service.<br/>REVIEW: THIS DOES NOT EXIST YET IN ECS.* | (use case) | long | `115` |
| <a name="error.&ast;"></a>*error.&ast;* | *Error namespace<br/>Use for errors which can happen during fetching information for a service.<br/>* |  |  |  |
| [error.message](../README.md#error.message)  | Error message returned by the service during fetching metrics. | core | text |  |
| [error.code](../README.md#error.code)  | Error code returned by the service during fetching metrics. | core | keyword |  |
| [host.hostname](../README.md#host.hostname)  | Hostname of the system metricbeat is running on or user defined name. | core | keyword |  |
| <a name="host.timezone.offset.sec"></a>*host.timezone.offset.sec* | *Timezone offset of the host in seconds.* | (use case) | long |  |
| [host.id](../README.md#host.id)  | Unique host id. | core | keyword |  |
| [event.module](../README.md#event.module)  | Name of the module this data is coming from. | core | keyword | `mysql` |
| [event.dataset](../README.md#event.dataset)  | Name of the dataset.<br/>This contains the information which is currently stored in metricset.name and metricset.module. | core | keyword | `stats` |



