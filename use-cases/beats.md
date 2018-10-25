## Beats use case

ECS fields used in Beats.

### <a name="beats"></a> Beats fields


| Field  | Level  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|---|
| <a name="id"></a>*id* | (use case) | *Unique id to describe the event.* | keyword |  |
| <a name="timestamp"></a>*timestamp* | (use case) | *Timestamp when the event was created.* | date |  |
| <a name="agent.&ast;"></a>*agent.&ast;* |  | *The agent fields are used to describe by which beat the information was collected.<br/>* |  |  |
| [agent.version](https://github.com/elastic/ecs#agent.version)  | core | Beat version. | keyword |  |
| [agent.name](https://github.com/elastic/ecs#agent.name)  | core | Beat name. | keyword |  |
| [agent.id](https://github.com/elastic/ecs#agent.id)  | core | Unique beat identifier. | keyword |  |



