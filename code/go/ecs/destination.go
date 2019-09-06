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

// Destination fields describe details about the destination of a packet/event.
// Destination fields are usually populated in conjunction with source fields.
type Destination struct {
	// Some event destination addresses are defined ambiguously. The event will
	// sometimes list an IP, a domain or a unix socket.  You should always
	// store the raw address in the `.address` field.
	// Then it should be duplicated to `.ip` or `.domain`, depending on which
	// one it is.
	Address string `ecs:"address"`

	// IP address of the destination.
	// Can be one or multiple IPv4 or IPv6 addresses.
	IP string `ecs:"ip"`

	// Port of the destination.
	Port int64 `ecs:"port"`

	// MAC address of the destination.
	MAC string `ecs:"mac"`

	// Destination domain.
	Domain string `ecs:"domain"`

	// The top level domain (TLD) also known as the domain suffix is the last
	// part of the domain name. For example, the top level domain for
	// google.com is "com".
	// The following groups of top level domain are maintained by the Internet
	// Assigned Numbers Authority (IANA).
	// Infrastructure top-level domain (ARPA) Generic top-level domains (gTLD)
	// Restricted generic top-level domains (grTLD) Sponsored top-level domains
	// (sTLD) Country code top-level domains (ccTLD) Internationalized country
	// code top-level domains (IDN ccTLDs) Test top-level domains (tTLD)
	TopLevelDomain string `ecs:"top_level_domain"`

	// Bytes sent from the destination to the source.
	Bytes int64 `ecs:"bytes"`

	// Packets sent from the destination to the source.
	Packets int64 `ecs:"packets"`

	// Translated ip of destination based NAT sessions (e.g. internet to
	// private DMZ)
	// Typically used with load balancers, firewalls, or routers.
	NatIP string `ecs:"nat.ip"`

	// Port the source session is translated to by NAT Device.
	// Typically used with load balancers, firewalls, or routers.
	NatPort int64 `ecs:"nat.port"`
}
