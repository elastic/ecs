## TLS use case

You can store TLS-related metadata under `tls.`, when appropriate.


### <a name="tls"></a> TLS fields


| Field  | Description  | Type  | Multi Field  | Example  |
|---|---|---|---|---|
| [source.ip](https://github.com/elastic/ecs#source.ip)  | IP address of the source.<br/>Can be one or multiple IPv4 or IPv6 addresses.  | ip  |   | `10.1.1.10`  |
| [destination.ip](https://github.com/elastic/ecs#destination.ip)  | IP address of the destination.<br/>Can be one or multiple IPv4 or IPv6 addresses.  | ip  |   | `5.5.5.5`  |
| [destination.port](https://github.com/elastic/ecs#destination.port)  | Port of the destination.  | long  |   | `443`  |
| <a name="tls.version"></a>*tls.version*  | *TLS version.*  | keyword  |   | `TLSv1.2`  |
| <a name="tls.certificates"></a>*tls.certificates*  | *An array of certificates.*  | keyword  |   |   |
| <a name="tls.servername"></a>*tls.servername*  | *Server name requested by the client.*  | keyword  |   | `localhost`  |
| <a name="tls.ciphersuite"></a>*tls.ciphersuite*  | *Name of the cipher used for the communication.*  | keyword  |   | `ECDHE-ECDSA-AES-128-CBC-SHA`  |



