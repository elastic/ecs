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

// These fields contain information about a process.
// These fields can help you correlate metrics information with a process
// id/name from a log message.  The `process.pid` often stays in the metric
// itself and is copied to the global field for correlation.
type Process struct {
	// Process id.
	PID int64 `ecs:"pid"`

	// Process name.
	// Sometimes called program name or similar.
	Name string `ecs:"name"`

	// Parent process' pid.
	PPID int64 `ecs:"ppid"`

	// Identifier of the group of processes the process belongs to.
	PGID int64 `ecs:"pgid"`

	// Array of process arguments.
	// May be filtered to protect sensitive information.
	Args []string `ecs:"args"`

	// Absolute path to the process executable.
	Executable string `ecs:"executable"`

	// Process title.
	// The proctitle, some times the same as process name. Can also be
	// different: for example a browser setting its title to the web page
	// currently opened.
	Title string `ecs:"title"`

	// Thread ID.
	ThreadID int64 `ecs:"thread.id"`

	// Thread name.
	ThreadName string `ecs:"thread.name"`

	// The time the process started.
	Start time.Time `ecs:"start"`

	// Seconds the process has been up.
	Uptime int64 `ecs:"uptime"`

	// The working directory of the process.
	WorkingDirectory string `ecs:"working_directory"`

	// The exit code of the process, if this is a termination event.
	// The field should be absent if there is no exit code for the event (e.g.
	// process start).
	ExitCode int64 `ecs:"exit_code"`
}
