## Filebeat Apache use case

ECS fields used in Filebeat for the apache module.

### <a name="filebeat-apache-access"></a> Filebeat Apache fields


| Field  | Description  | Level  | Type  | Example  |
|---|---|---|---|---|
| <a name="id"></a>*id* | *Unique id to describe the event.* | (use case) | keyword | `8a4f500d` |
| [@timestamp](../README.md#@timestamp)  | Timestamp of the log line after processing. | core | date | `2016-05-23T08:05:34.853Z` |
| [message](../README.md#message)  | Log message of the event | core | text | `Hello World` |
| [event.module](../README.md#event.module)  | Currently fileset.module | core | keyword | `apache` |
| [event.dataset](../README.md#event.dataset)  | Currenly fileset.name | core | keyword | `access` |
| [source.ip](../README.md#source.ip)  | Source ip of the request. Currently apache.access.remote_ip | core | ip | `192.168.1.1` |
| [user.name](../README.md#user.name)  | User name in the request. Currently apache.access.user_name | core | keyword | `ruflin` |
| <a name="http.method"></a>*http.method* | *Http method, currently apache.access.method* | (use case) | keyword | `GET` |
| <a name="http.url"></a>*http.url* | *Http url, currently apache.access.url* | (use case) | keyword | `http://elastic.co/` |
| [http.version](../README.md#http.version)  | Http version, currently apache.access.http_version | extended | keyword | `1.1` |
| <a name="http.response.code"></a>*http.response.code* | *Http response code, currently apache.access.response_code* | (use case) | keyword | `404` |
| <a name="http.response.body_sent.bytes"></a>*http.response.body_sent.bytes* | *Http response body bytes sent, currently apache.access.body_sent.bytes* | (use case) | long | `117` |
| <a name="http.referer"></a>*http.referer* | *Http referrer code, currently apache.access.referrer<br/>NOTE: In the RFC its misspell as referer and has become accepted standard* | (use case) | keyword | `http://elastic.co/` |
| <a name="user_agent.&ast;"></a>*user_agent.&ast;* | *User agent fields as in schema. Currently under apache.access.user_agent.*<br/>* |  |  |  |
| [user_agent.original](../README.md#user_agent.original)  | Original user agent. Currently apache.access.agent | extended | keyword | `http://elastic.co/` |
| <a name="geoip.&ast;"></a>*geoip.&ast;* | *User agent fields as in schema. Currently under apache.access.geoip.*<br/>These are extracted from source.ip<br/>Should they be under source.geoip?<br/>* |  |  |  |
| <a name="geoip...."></a>*geoip....* | *All geoip fields.* | (use case) | keyword |  |



