## Beats use case

ECS fields used in Beats.

### <a name="beats"></a> Beats fields


| Field  | Description  | Level  | Type  | Multi Field  | Example  |
|---|---|---|---|---|---|
| <a name="id"></a>*id* | *Unique id to describe the event.* | (use case) | keyword |  | `8a4f500d` |
| <a name="timestamp"></a>*timestamp* | *Timestamp when the event was created.* | (use case) | date |  | `2016-05-23T08:05:34.853Z` |
| <a name="agent.&ast;"></a>*agent.&ast;* | *The agent fields are used to describe by which beat the information was collected.<br/>* |  |  |  |  |
| [agent.version](https://github.com/elastic/ecs#agent.version)  | Beat version. | core | keyword |  | `6.0.0-rc2` |
| [agent.name](https://github.com/elastic/ecs#agent.name)  | Beat name. | core | keyword |  | `filebeat` |
| [agent.id](https://github.com/elastic/ecs#agent.id)  | Unique beat identifier. | core | keyword |  | `8a4f500d` |



