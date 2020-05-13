## Logging use case

ECS fields used in logging use cases.

### <a name="logging"></a> Logging fields


| Field  | Description  | Level  | Type  | Example  |
|---|---|---|---|---|
| <a name="id"></a>*id* | *Unique id of the log entry.* | (use case) | keyword | `8a4f500d` |
| <a name="timestamp"></a>*timestamp* | *Timestamp of the log line.* | (use case) | date | `2016-05-23T08:05:34.853Z` |
| [message](../README.md#message)  | The log message.<br/>This can contain the full log line or based on the processing only the extracted message part. This is expected to be human readable. | core | text | `Hello World` |
| <a name="hostname"></a>*hostname* | *Hostname extracted from the log line.* | (use case) | keyword | `www.example.com` |
| <a name="ip"></a>*ip* | *IP Address extracted from the log line. Can be IPv4 or IPv6.* | (use case) | ip | `192.168.1.12` |
| [log.level](../README.md#log.level)  | Log level field. Is expected to be `WARN`, `ERR`, `INFO` etc. | core | keyword | `ERR` |
| <a name="log.line"></a>*log.line* | *Line number the log event was collected from.* | (use case) | long | `18` |
| <a name="log.offset"></a>*log.offset* | *Offset of the log event.* | (use case) | long | `12` |
| <a name="source.&ast;"></a>*source.&ast;* | *Describes from where the log entries come from.<br/>* |  |  |  |
| <a name="source.path"></a>*source.path* | *File path of the file the data is harvested from.* | (use case) | keyword | `/var/log/test.log` |



