## Logging use case

ECS fields used in logging use cases.

### <a name="logging"></a> Logging fields


| Field  | Level  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|---|
| <a name="id"></a>*id* | (use case) | *Unique id of the log entry.* | keyword |  |
| <a name="timestamp"></a>*timestamp* | (use case) | *Timestamp of the log line.* | date |  |
| [message](https://github.com/elastic/ecs#message)  | core | The log message.<br/>This can contain the full log line or based on the processing only the extracted message part. This is expected to be human readable. | text |  |
| <a name="hostname"></a>*hostname* | (use case) | *Hostname extracted from the log line.* | keyword |  |
| <a name="ip"></a>*ip* | (use case) | *IP Address extracted from the log line. Can be IPv4 or IPv6.* | ip |  |
| [log.level](https://github.com/elastic/ecs#log.level)  | core | Log level field. Is expected to be `WARN`, `ERR`, `INFO` etc. | keyword |  |
| <a name="log.line"></a>*log.line* | (use case) | *Line number the log event was collected from.* | long |  |
| <a name="log.offset"></a>*log.offset* | (use case) | *Offset of the log event.* | long |  |
| <a name="source.&ast;"></a>*source.&ast;* |  | *Describes from where the log entries come from.<br/>* |  |  |
| <a name="source.path"></a>*source.path* | (use case) | *File path of the file the data is harvested from.* | keyword |  |



