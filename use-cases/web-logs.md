## Parsing web server logs use case

Representing web server access logs in ECS.
This use case uses previous definitions for `http` and `user_agent` fields sets, which were taken out of ECS temporarily for Beta1. Their official definition in ECS is expected to change slightly.
Using the fields as represented here is not expected to conflict with ECS, but may require a transition, when they are re-introduced officially.

### <a name="web-logs"></a> Parsing web server logs fields


| Field  | Description  | Level  | Type  | Example  |
|---|---|---|---|---|
| [@timestamp](../README.md#@timestamp)  | Time at which the response was sent, and the web server log created. | core | date | `2016-05-23T08:05:34.853Z` |
| <a name="http.&ast;"></a>*http.&ast;* | *Fields related to HTTP requests and responses.<br/>* |  |  |  |
| [http.request.method](../README.md#http.request.method)  | Http request method. | extended | keyword | `GET, POST, PUT` |
| [http.request.referrer](../README.md#http.request.referrer)  | Referrer for this HTTP request. | extended | keyword | `https://blog.example.com/` |
| [http.response.status_code](../README.md#http.response.status_code)  | Http response status code. | extended | long | `404` |
| [http.response.body.content](../README.md#http.response.body.content)  | The full http response body. | extended | keyword | `Hello world` |
| [http.version](../README.md#http.version)  | Http version. | extended | keyword | `1.1` |
| <a name="user_agent.&ast;"></a>*user_agent.&ast;* | *The user_agent fields normally come from a browser request. They often show up in web service logs coming from the parsed user agent string.<br/>* |  |  |  |
| [user_agent.original](../README.md#user_agent.original)  | Unparsed version of the user_agent. | extended | keyword | `Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1` |
| <a name="user_agent.device"></a>*user_agent.device* | *Name of the physical device.* | (use case) | keyword |  |
| [user_agent.version](../README.md#user_agent.version)  | Version of the physical device. | extended | keyword | `12.0` |
| <a name="user_agent.major"></a>*user_agent.major* | *Major version of the user agent.* | (use case) | long |  |
| <a name="user_agent.minor"></a>*user_agent.minor* | *Minor version of the user agent.* | (use case) | long |  |
| <a name="user_agent.patch"></a>*user_agent.patch* | *Patch version of the user agent.* | (use case) | keyword |  |
| [user_agent.name](../README.md#user_agent.name)  | Name of the user agent. | extended | keyword | `Chrome` |



