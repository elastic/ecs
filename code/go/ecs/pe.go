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

// These fields contain Windows Portable Executable (PE) metadata.
type Pe struct {
	// Internal name of the file, provided at compile-time.
	OriginalFileName string `ecs:"original_file_name"`

	// Internal version of the file, provided at compile-time.
	FileVersion string `ecs:"file_version"`

	// Internal description of the file, provided at compile-time.
	Description string `ecs:"description"`

	// Internal product name of the file, provided at compile-time.
	Product string `ecs:"product"`

	// Internal company name of the file, provided at compile-time.
	Company string `ecs:"company"`

	// A hash of the imports in a PE file. An imphash -- or import hash -- can
	// be used to fingerprint binaries even after recompilation or other
	// code-level transformations have occurred, which would change more
	// traditional hash values.
	// Learn more at
	// https://www.fireeye.com/blog/threat-research/2014/01/tracking-malware-import-hashing.html.
	Imphash string `ecs:"imphash"`

	// CPU architecture target for the file.
	Architecture string `ecs:"architecture"`

	// Hashes of embedded program icon.
	MainIcon map[string]interface{} `ecs:"main_icon"`

	// Debug information, if present
	Debug string `ecs:"debug"`

	// List of all imported functions
	ImportList string `ecs:"import_list"`

	// Data about sections of compiled binary PE
	Sections string `ecs:"sections"`

	// If the PE contains resources, some info about them
	ResourceDetails string `ecs:"resource_details"`

	// Digest of languages found in resources. Key is language (as string) and
	// value is how many resources there are having that language (as integer)
	ResourceLanguages string `ecs:"resource_languages"`

	// Digest of resource types. Key is resource type (as string) and value is
	// how many resources there are of that specific type (as integer)
	ResourceTypes string `ecs:"resource_types"`

	// Identifies packers used on Windows PE files by several tools and AVs.
	// Keys are tool names and values are identified packers, both strings. see
	// `file.pe.packers` for merged list of packers from all tools.
	Packers string `ecs:"packers"`

	// List of symbols exported by PE
	Exports string `ecs:"exports"`

	// Extracted when possible from the file's metadata. Indicates when it was
	// built or compiled. It can also be faked by malware creators.
	CreationDate time.Time `ecs:"creation_date"`

	// Authentihash of the PE file.
	Authentihash string `ecs:"authentihash"`

	// Compile timestamp of the PE file.
	CompileTimestamp time.Time `ecs:"compile_timestamp"`

	// Version of the compiler.
	CompilerProductVersions string `ecs:"compiler_product_versions"`

	// Hash of the PE header.
	RichPeHeaderHash string `ecs:"rich_pe_header_hash"`

	// Entry point of the PE file.
	EntryPoint int64 `ecs:"entry_point"`

	// Machine type of the PE file.
	MachineType string `ecs:"machine_type"`

	// Overlay information of the PE file.
	Overlay map[string]interface{} `ecs:"overlay"`
}
