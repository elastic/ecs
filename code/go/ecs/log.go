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

// Fields which are specific to log events.
type Log struct {
	// Original log level of the log event.
	// Syslog's severity label should be stored here. Syslog's numeric severity
	// is `event.severity` in ECS.
	// Some examples are `warn`, `error`, `i`.
	Level string `ecs:"level"`

	// The Syslog text-based facility of the log event, if available. See RFCs
	// 5424 or 3164.
	FacilityName string `ecs:"facility.name"`

	// The Syslog numeric facility of the log event, if available.
	// According to RFCs 5424 and 3164, this value should be an integer between
	// 0 and 23.
	FacilityCode int64 `ecs:"facility.code"`

	// Syslog numeric priority of the event, if available.
	// According to RFCs 5424 and 3164, the priority is 8 * facility +
	// severity. This number is therefore expected to contain a value between 0
	// and 191.
	Priority int64 `ecs:"priority"`

	// This is the original log message and contains the full log message
	// before splitting it up in multiple parts.
	// In contrast to the `message` field which can contain an extracted part
	// of the log message, this field contains the original, full log message.
	// It can have already some modifications applied like encoding or new
	// lines removed to clean up the log message.
	// This field is not indexed and doc_values are disabled so it can't be
	// queried but the value can be retrieved from `_source`.
	Original string `ecs:"original"`

	// The name of the logger inside an application. This is usually the name
	// of the class which initialized the logger, or can be a custom name.
	Logger string `ecs:"logger"`
}
