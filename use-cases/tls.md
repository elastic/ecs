## TLS use case

You can store TLS-related metadata under `tls.`, when appropriate.


### <a name="tls"></a> TLS fields


| Field  | Level  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|---|
| [source.ip](https://github.com/elastic/ecs#source.ip)  | core | IP address of the source.<br/>Can be one or multiple IPv4 or IPv6 addresses. | ip |  |
| [destination.ip](https://github.com/elastic/ecs#destination.ip)  | core | IP address of the destination.<br/>Can be one or multiple IPv4 or IPv6 addresses. | ip |  |
| [destination.port](https://github.com/elastic/ecs#destination.port)  | core | Port of the destination. | long |  |
| <a name="tls.version"></a>*tls.version* | (use case) | *TLS version.* | keyword |  |
| <a name="tls.certificates"></a>*tls.certificates* | (use case) | *An array of certificates.* | keyword |  |
| <a name="tls.servername"></a>*tls.servername* | (use case) | *Server name requested by the client.* | keyword |  |
| <a name="tls.ciphersuite"></a>*tls.ciphersuite* | (use case) | *Name of the cipher used for the communication.* | keyword |  |



