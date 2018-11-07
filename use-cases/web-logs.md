## Parsing web server logs use case

Representing web server access logs in ECS.
This use case uses previous definitions for `http` and `user_agent` fields sets, which were taken out of ECS temporarily for Beta1. Their official definition in ECS is expected to change slightly.
Using the fields as represented here is not expected to conflict with ECS, but may require a transition, when they are re-introduced officially.

### <a name="web-logs"></a> Parsing web server logs fields


| Field  | Description  | Level  | Type  | Example  |
|---|---|---|---|---|
| [@timestamp](https://github.com/elastic/ecs#@timestamp)  | Time at which the response was sent, and the web server log created. | core | date | `2016-05-23T08:05:34.853Z` |
| <a name="http.&ast;"></a>*http.&ast;* | *Fields related to HTTP requests and responses.<br/>* |  |  |  |
| <a name="http.request.method"></a>*http.request.method* | *Http request method.* | (use case) | keyword | `GET, POST, PUT` |
| <a name="http.request.referrer"></a>*http.request.referrer* | *Referrer for this HTTP request.* | (use case) | keyword | `https://blog.example.com/` |
| <a name="http.response.status_code"></a>*http.response.status_code* | *Http response status code.* | (use case) | long | `404` |
| <a name="http.response.body"></a>*http.response.body* | *The full http response body.* | (use case) | keyword | `Hello world` |
| <a name="http.version"></a>*http.version* | *Http version.* | (use case) | keyword | `1.1` |
| <a name="user_agent.&ast;"></a>*user_agent.&ast;* | *The user_agent fields normally come from a browser request. They often show up in web service logs coming from the parsed user agent string.<br/>* |  |  |  |
| <a name="user_agent.original"></a>*user_agent.original* | *Unparsed version of the user_agent.* | (use case) | keyword |  |
| <a name="user_agent.device"></a>*user_agent.device* | *Name of the physical device.* | (use case) | keyword |  |
| <a name="user_agent.version"></a>*user_agent.version* | *Version of the physical device.* | (use case) | keyword |  |
| <a name="user_agent.major"></a>*user_agent.major* | *Major version of the user agent.* | (use case) | long |  |
| <a name="user_agent.minor"></a>*user_agent.minor* | *Minor version of the user agent.* | (use case) | long |  |
| <a name="user_agent.patch"></a>*user_agent.patch* | *Patch version of the user agent.* | (use case) | keyword |  |
| <a name="user_agent.name"></a>*user_agent.name* | *Name of the user agent.* | (use case) | keyword | `Chrome` |



