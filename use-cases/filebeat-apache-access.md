## Filebeat Apache use case

ECS fields used in Filebeat for the apache module.

### <a name="filebeat-apache-access"></a> Filebeat Apache fields


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| <a name="id"></a>*id*  | *Unique id to describe the event.*  | keyword  |   | `8a4f500d`  |
| [@timestamp](https://github.com/elastic/ecs#@timestamp)  | Timestamp of the log line after processing.  | date  |   | `2016-05-23T08:05:34.853Z`  |
| [message](https://github.com/elastic/ecs#message)  | Log message of the event  | date  |   | `Hello World`  |
| [event.module](https://github.com/elastic/ecs#event.module)  | Currently fileset.module  | keyword  |   | `apache`  |
| [event.dataset](https://github.com/elastic/ecs#event.dataset)  | Currenly fileset.name  | keyword  |   | `access`  |
| [source.ip](https://github.com/elastic/ecs#source.ip)  | Source ip of the request. Currently apache.access.remote_ip  | ip  |   | `192.168.1.1`  |
| [user.name](https://github.com/elastic/ecs#user.name)  | User name in the request. Currently apache.access.user_name  | keyword  |   | `ruflin`  |
| <a name="http.method"></a>*http.method*  | *Http method, currently apache.access.method*  | keyword  |   | `GET`  |
| <a name="http.url"></a>*http.url*  | *Http url, currently apache.access.url*  | keyword  |   | `http://elastic.co/`  |
| [http.version](https://github.com/elastic/ecs#http.version)  | Http version, currently apache.access.http_version  | keyword  |   | `1.1`  |
| <a name="http.response.code"></a>*http.response.code*  | *Http response code, currently apache.access.response_code*  | keyword  |   | `404`  |
| <a name="http.response.body_sent.bytes"></a>*http.response.body_sent.bytes*  | *Http response body bytes sent, currently apache.access.body_sent.bytes*  | long  |   | `117`  |
| <a name="http.referer"></a>*http.referer*  | *Http referrer code, currently apache.access.referrer<br/>NOTE: In the RFC its misspell as referer and has become accepted standard*  | keyword  |   | `http://elastic.co/`  |
| [user_agent.*](https://github.com/elastic/ecs#user_agent.*)  | User agent fields as in schema. Currently under apache.access.user_agent.*<br/>  |   |   |   |
| [user_agent.raw](https://github.com/elastic/ecs#user_agent.raw)  | Raw user agent. Currently apache.access.agent  | text  |   | `http://elastic.co/`  |
| [geoip.*](https://github.com/elastic/ecs#geoip.*)  | User agent fields as in schema. Currently under apache.access.geoip.*<br/>These are extracted from source.ip<br/>Should they be under source.geoip?<br/>  |   |   |   |
| <a name="geoip...."></a>*geoip....*  | *All geoip fields.*  | text  |   |   |



