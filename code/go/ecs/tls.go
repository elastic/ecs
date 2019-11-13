// Licensed to Elasticsearch B.V. under one or more contributor
// license agreements. See the NOTICE file distributed with
// this work for additional information regarding copyright
// ownership. Elasticsearch B.V. licenses this file to you under
// the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

// Code generated by scripts/gocodegen.go - DO NOT EDIT.

package ecs

import (
	"time"
)

// Fields related to TLS activity.
type Tls struct {
	// Normalized protocol name parsed from original string (e.g. ssl, tls).
	VersionProtocol string `ecs:"version.protocol"`

	// Numeric part of the version parsed from the original string (e.g. 1.2,
	// 3).
	VersionNumber string `ecs:"version.number"`

	// String indicating the cipher used during the current connection.
	Cipher string `ecs:"cipher"`

	// String indicating the curve used for the given cipher, when applicable.
	Curve string `ecs:"curve"`

	// Boolean flag indicating if this TLS connection was resumed from an
	// existing TLS negotiation.
	Resumed bool `ecs:"resumed"`

	// String indicating the protocol being tunneled (e.g. http/1.1, spdy/3,
	// imap, webrtc)
	NextProtocol string `ecs:"next_protocol"`

	// A hash that identifies clients based on how they perform an SSL/TLS
	// handshake.
	ClientJa3 string `ecs:"client.ja3"`

	// Also called an SNI, this tells the server which hostname to which the
	// client is attempting to connect.
	ClientServerName string `ecs:"client.server_name"`

	// List of ciphers offered by the client during the client hello.
	ClientSupportedCiphers string `ecs:"client.supported_ciphers"`

	// Subject of the x.509 certificate presented by the client.
	ClientSubject string `ecs:"client.subject"`

	// Subject of the issuer of the x.509 certificate presented by the client.
	ClientIssuer string `ecs:"client.issuer"`

	// Timestamp indicating when client certificate is first considered valid.
	ClientNotBefore time.Time `ecs:"client.not_before"`

	// Timestamp indicating when client certificate is no longer considered
	// valid.
	ClientNotAfter time.Time `ecs:"client.not_after"`

	// List of PEM-encoded certificates that make up the certificate chain
	// offered by the client.
	ClientCertificateChain string `ecs:"client.certificate_chain"`

	// PEM-encoded stand-alone certificate offered by the client.
	ClientCertificate string `ecs:"client.certificate"`

	// Certificate fingerprint using the MD5 digest of DER-encoded version of
	// certificate offered by the client. For consistency with other hash
	// values, this value should be formatted as an uppercase hash (e.g.
	// `0F76C7F2C55BFD7D8E8B8F4BFBF0C9EC`).
	ClientHashMd5 string `ecs:"client.hash.md5"`

	// Certificate fingerprint using the SHA1 digest of DER-encoded version of
	// certificate offered by the client. For consistency with other hash
	// values, this value should be formatted as an uppercase hash (e.g.
	// `9E393D93138888D288266C2D915214D1D1CCEB2A`).
	ClientHashSha1 string `ecs:"client.hash.sha1"`

	// Certificate fingerprint using the SHA256 digest of DER-encoded version
	// of certificate offered by the client. For consistency with other hash
	// values, this value should be formatted as an uppercase hash (e.g.
	// `0687F666A054EF17A08E2F2162EAB4CBC0D265E1D7875BE74BF3C712CA92DAF0`).
	ClientHashSha256 string `ecs:"client.hash.sha256"`

	// A hash that identifies servers based on how they perform an SSL/TLS
	// handshake.
	ServerJa3s string `ecs:"server.ja3s"`

	// List of ciphers offered by the server during the server hello.
	ServerSupportedCiphers string `ecs:"server.supported_ciphers"`

	// Subject of the x.509 certificate presented by the server.
	ServerSubject string `ecs:"server.subject"`

	// Subject of the issuer of the x.509 certificate presented by the server.
	ServerIssuer string `ecs:"server.issuer"`

	// Timestamp indicating when server certificate is first considered valid.
	ServerNotBefore time.Time `ecs:"server.not_before"`

	// Timestamp indicating when server certificate is no longer considered
	// valid.
	ServerNotAfter time.Time `ecs:"server.not_after"`

	// List of PEM-encoded certificates that make up the certificate chain
	// offered by the server.
	ServerCertificateChain string `ecs:"server.certificate_chain"`

	// PEM-encoded stand-alone certificate offered by the server.
	ServerCertificate string `ecs:"server.certificate"`

	// Certificate fingerprint using the MD5 digest of DER-encoded version of
	// certificate offered by the server. For consistency with other hash
	// values, this value should be formatted as an uppercase hash (e.g.
	// `0F76C7F2C55BFD7D8E8B8F4BFBF0C9EC`).
	ServerHashMd5 string `ecs:"server.hash.md5"`

	// Certificate fingerprint using the SHA1 digest of DER-encoded version of
	// certificate offered by the server. For consistency with other hash
	// values, this value should be formatted as an uppercase hash (e.g.
	// `9E393D93138888D288266C2D915214D1D1CCEB2A`).
	ServerHashSha1 string `ecs:"server.hash.sha1"`

	// Certificate fingerprint using the SHA256 digest of DER-encoded version
	// of certificate offered by the server. For consistency with other hash
	// values, this value should be formatted as an uppercase hash (e.g.
	// `0687F666A054EF17A08E2F2162EAB4CBC0D265E1D7875BE74BF3C712CA92DAF0`).
	ServerHashSha256 string `ecs:"server.hash.sha256"`
}
