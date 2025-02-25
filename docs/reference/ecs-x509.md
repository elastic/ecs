---
mapped_pages:
  - https://www.elastic.co/guide/en/ecs/current/ecs-x509.html
applies_to:
  stack: all
  serverless: all
---

# x509 certificate fields [ecs-x509]

This implements the common core fields for x509 certificates. This information is likely logged with TLS sessions, digital signatures found in executable binaries, S/MIME information in email bodies, or analysis of files on disk.

When the certificate relates to a file, use the fields at `file.x509`. When hashes of the DER-encoded certificate are available, the `hash` data set should be populated as well (e.g. `file.hash.sha256`).

Events that contain certificate information about network connections, should use the x509 fields under the relevant TLS fields: `tls.server.x509` and/or `tls.client.x509`.


## x509 certificate field details [_x509_certificate_field_details]

| Field | Description | Level |
| --- | --- | --- |
| $$$field-x509-alternative-names$$$[x509.alternative_names](#field-x509-alternative-names) | List of subject alternative names (SAN). Name types vary by certificate authority and certificate type but commonly contain IP addresses, DNS names (and wildcards), and email addresses.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `*.elastic.co`<br> | extended |
| $$$field-x509-issuer-common-name$$$[x509.issuer.common_name](#field-x509-issuer-common-name) | List of common name (CN) of issuing certificate authority.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `Example SHA2 High Assurance Server CA`<br> | extended |
| $$$field-x509-issuer-country$$$[x509.issuer.country](#field-x509-issuer-country) | List of country (C) codes<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `US`<br> | extended |
| $$$field-x509-issuer-distinguished-name$$$[x509.issuer.distinguished_name](#field-x509-issuer-distinguished-name) | Distinguished name (DN) of issuing certificate authority.<br><br>type: keyword<br><br>example: `C=US, O=Example Inc, OU=www.example.com, CN=Example SHA2 High Assurance Server CA`<br> | extended |
| $$$field-x509-issuer-locality$$$[x509.issuer.locality](#field-x509-issuer-locality) | List of locality names (L)<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `Mountain View`<br> | extended |
| $$$field-x509-issuer-organization$$$[x509.issuer.organization](#field-x509-issuer-organization) | List of organizations (O) of issuing certificate authority.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `Example Inc`<br> | extended |
| $$$field-x509-issuer-organizational-unit$$$[x509.issuer.organizational_unit](#field-x509-issuer-organizational-unit) | List of organizational units (OU) of issuing certificate authority.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `www.example.com`<br> | extended |
| $$$field-x509-issuer-state-or-province$$$[x509.issuer.state_or_province](#field-x509-issuer-state-or-province) | List of state or province names (ST, S, or P)<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `California`<br> | extended |
| $$$field-x509-not-after$$$[x509.not_after](#field-x509-not-after) | Time at which the certificate is no longer considered valid.<br><br>type: date<br><br>example: `2020-07-16T03:15:39Z`<br> | extended |
| $$$field-x509-not-before$$$[x509.not_before](#field-x509-not-before) | Time at which the certificate is first considered valid.<br><br>type: date<br><br>example: `2019-08-16T01:40:25Z`<br> | extended |
| $$$field-x509-public-key-algorithm$$$[x509.public_key_algorithm](#field-x509-public-key-algorithm) | Algorithm used to generate the public key.<br><br>type: keyword<br><br>example: `RSA`<br> | extended |
| $$$field-x509-public-key-curve$$$[x509.public_key_curve](#field-x509-public-key-curve) | The curve used by the elliptic curve public key algorithm. This is algorithm specific.<br><br>type: keyword<br><br>example: `nistp521`<br> | extended |
| $$$field-x509-public-key-exponent$$$[x509.public_key_exponent](#field-x509-public-key-exponent) | Exponent used to derive the public key. This is algorithm specific.<br><br>type: long<br><br>example: `65537`<br> | extended |
| $$$field-x509-public-key-size$$$[x509.public_key_size](#field-x509-public-key-size) | The size of the public key space in bits.<br><br>type: long<br><br>example: `2048`<br> | extended |
| $$$field-x509-serial-number$$$[x509.serial_number](#field-x509-serial-number) | Unique serial number issued by the certificate authority. For consistency, this must be encoded in base 16 and formatted without colons and uppercase characters.<br><br>type: keyword<br><br>example: `55FBB9C7DEBF09809D12CCAA`<br> | extended |
| $$$field-x509-signature-algorithm$$$[x509.signature_algorithm](#field-x509-signature-algorithm) | Identifier for certificate signature algorithm. We recommend using names found in Go Lang Crypto library. See [https://github.com/golang/go/blob/go1.14/src/crypto/x509/x509.go#L337-L353](https://github.com/golang/go/blob/go1.14/src/crypto/x509/x509.go#L337-L353).<br><br>type: keyword<br><br>example: `SHA256-RSA`<br> | extended |
| $$$field-x509-subject-common-name$$$[x509.subject.common_name](#field-x509-subject-common-name) | List of common names (CN) of subject.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `shared.global.example.net`<br> | extended |
| $$$field-x509-subject-country$$$[x509.subject.country](#field-x509-subject-country) | List of country (C) code<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `US`<br> | extended |
| $$$field-x509-subject-distinguished-name$$$[x509.subject.distinguished_name](#field-x509-subject-distinguished-name) | Distinguished name (DN) of the certificate subject entity.<br><br>type: keyword<br><br>example: `C=US, ST=California, L=San Francisco, O=Example, Inc., CN=shared.global.example.net`<br> | extended |
| $$$field-x509-subject-locality$$$[x509.subject.locality](#field-x509-subject-locality) | List of locality names (L)<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `San Francisco`<br> | extended |
| $$$field-x509-subject-organization$$$[x509.subject.organization](#field-x509-subject-organization) | List of organizations (O) of subject.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `Example, Inc.`<br> | extended |
| $$$field-x509-subject-organizational-unit$$$[x509.subject.organizational_unit](#field-x509-subject-organizational-unit) | List of organizational units (OU) of subject.<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br> | extended |
| $$$field-x509-subject-state-or-province$$$[x509.subject.state_or_province](#field-x509-subject-state-or-province) | List of state or province names (ST, S, or P)<br><br>type: keyword<br><br>Note: this field should contain an array of values.<br><br>example: `California`<br> | extended |
| $$$field-x509-version-number$$$[x509.version_number](#field-x509-version-number) | Version of x509 format.<br><br>type: keyword<br><br>example: `3`<br> | extended |


## Field reuse [_field_reuse_32]

The `x509` fields are expected to be nested at:

* `file.x509`
* `threat.enrichments.indicator.x509`
* `threat.indicator.x509`
* `tls.client.x509`
* `tls.server.x509`

Note also that the `x509` fields are not expected to be used directly at the root of the events.

