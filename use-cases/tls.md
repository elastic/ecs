## TLS use case

You can store TLS-related metadata under `tls.`, when appropriate.


### <a name="tls"></a> TLS fields


| Field  | Description  | Level  | Type  | Example  |
|---|---|---|---|---|
| [source.ip](../README.md#source.ip)  | IP address of the source.<br/>Can be one or multiple IPv4 or IPv6 addresses. | core | ip | `10.1.1.10` |
| [destination.ip](../README.md#destination.ip)  | IP address of the destination.<br/>Can be one or multiple IPv4 or IPv6 addresses. | core | ip | `5.5.5.5` |
| [destination.port](../README.md#destination.port)  | Port of the destination. | core | long | `443` |
| <a name="tls.version"></a>*tls.version* | *TLS version.* | (use case) | keyword | `TLSv1.2` |
| <a name="tls.certificates"></a>*tls.certificates* | *An array of certificates.* | (use case) | keyword |  |
| <a name="tls.servername"></a>*tls.servername* | *Server name requested by the client.* | (use case) | keyword | `localhost` |
| <a name="tls.ciphersuite"></a>*tls.ciphersuite* | *Name of the cipher used for the communication.* | (use case) | keyword | `ECDHE-ECDSA-AES-128-CBC-SHA` |



