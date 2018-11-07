## Parsing web server logs use case

Represenging web server access logs in ECS

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



