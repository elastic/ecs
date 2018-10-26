## APM use case

ECS usage for the APM data.

### <a name="apm"></a> APM fields


| Field  | Description  | Level  | Type  | Multi Field  | Example  |
|---|---|---|---|---|---|
| <a name="id"></a>*id* | *Unique id to describe the event.* | (use case) | keyword |  | `8a4f500d` |
| [@timestamp](https://github.com/elastic/ecs#@timestamp)  | Timestamp when the event was created in the app / service. | core | date |  | `2016-05-23T08:05:34.853Z` |
| <a name="agent.&ast;"></a>*agent.&ast;* | *The agent fields are used to describe which agent did send the information.<br/>* |  |  |  |  |
| [agent.version](https://github.com/elastic/ecs#agent.version)  | APM Agent version. | core | keyword |  | `3.14.0` |
| [agent.name](https://github.com/elastic/ecs#agent.name)  | APM agent name. | core | keyword |  | `elastic-node` |
| <a name="service.&ast;"></a>*service.&ast;* | *The service fields describe the service inside which the APM agent is running.<br/>* |  |  |  |  |
| [service.id](https://github.com/elastic/ecs#service.id)  | Unique identifier of the running service. | core | keyword |  | `d37e5ebfe0ae6c4972dbe9f0174a1637bb8247f6` |
| [service.name](https://github.com/elastic/ecs#service.name)  | Name of the service the agent is running in. This is normally a user defined name. | core | keyword |  | `user-service` |
| [service.version](https://github.com/elastic/ecs#service.version)  | Version of the service the agent is running in. This depends on if the service is given a version. | core | keyword |  | `3.2.4` |



