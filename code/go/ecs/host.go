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

// A host is defined as a general computing instance.
// ECS host.* fields should be populated with details about the host on which
// the event happened, or from which the measurement was taken. Host types
// include hardware, virtual machines, Docker containers, and Kubernetes nodes.
type Host struct {
	// Name of the host.
	// It can contain what `hostname` returns on Unix systems, the fully
	// qualified domain name, or a name specified by the user. The sender
	// decides which value to use.
	Name string `ecs:"name"`

	// Unique host id.
	// As hostname is not always unique, use values that are meaningful in your
	// environment.
	// Example: The current usage of `beat.name`.
	ID string `ecs:"id"`

	// Host ip addresses.
	IP string `ecs:"ip"`

	// Host mac addresses.
	MAC string `ecs:"mac"`

	// Type of host.
	// For Cloud providers this can be the machine type like `t2.medium`. If
	// vm, this could be the container, for example, or other information
	// meaningful in your environment.
	Type string `ecs:"type"`

	// Seconds the host has been up.
	Uptime int64 `ecs:"uptime"`

	// Operating system architecture.
	Architecture string `ecs:"architecture"`

	// Name of the domain of which the host is a member.
	// For example, on Windows this could be the host's Active Directory domain
	// or NetBIOS domain name. For Linux this could be the domain of the host's
	// LDAP provider.
	Domain string `ecs:"domain"`

	// Hostname of the system.
	// It normally contains what the `hostname` command returns on the host
	// machine, or the host portion of a fully qualified domain name.
	// For example, the hostname portion of "www.east.mydomain.co.uk " is
	// "www".
	Hostname string `ecs:"hostname"`

	// The highest registered domain, stripped of the subdomain.
	// For example, the registered domain for " www.east.mydomain.co.uk " is
	// "mydomain.co.uk".
	// This value can be determined precisely with a list like the public
	// suffix list (http://publicsuffix.org). Trying to approximate this by
	// simply taking the last two labels will not work well for TLDs such as
	// "co.uk".
	RegisteredDomain string `ecs:"registered_domain"`

	// The effective top level domain (eTLD), also known as the domain suffix,
	// is the last part of the domain name and is typically inclusive of the
	// top level domain (e.g. "co"), as well as including country code and
	// region codes For example, the top level domain for
	// www.east.mydomain.co.uk is "co.uk".
	// This value can be determined precisely with a list like the public
	// suffix list (http://publicsuffix.org).
	TopLevelDomain string `ecs:"top_level_domain"`

	// The subdomain portion of a fully qualified domain name includes all of
	// the names except  the host name under the registered_domain.  In a
	// partially qualified domain, or if the  the qualification level of the
	// full name cannot be determined, subdomain contains all of the names
	// below the registered domain.
	// For example the subdomain portion of "www.east.mydomain.co.uk " is
	// "east".
	// If the domain has multiple levels of subdomain, such as
	// "sub2.sub1.example.com", the subdomain field should contain "sub2.sub1",
	// with no trailing period.
	Subdomain string `ecs:"subdomain"`

	// Internationalized domain names may contain non LDH-ASCII character
	// encoding used to represent full unicode characters in the ASCII
	// representation used by DNS. For example the  internationalized country
	// code TLD for Israel is .xn--4dbrk0ce.
	IsInternationalized bool `ecs:"is_internationalized"`
}
