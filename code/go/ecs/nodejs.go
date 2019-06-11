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

// Fields describing a Node.js runtime.
// These fields can be used for monitoring the performance of a Node.js
// application.
type Nodejs struct {
	// Current number of active libuv handles.
	// The number of active libuv handles, likely held open by currently
	// running I/O operations.
	HandlesActive int64 `ecs:"handles.active"`

	// Current number of active libuv requests.
	// The number of active libuv requests, likely waiting for a response to an
	// I/O operation.
	RequestsActive int64 `ecs:"requests.active"`

	// The average event loop delay for the reporting period.
	// Event loop delay is periodically sampled, e.g. every 10 milliseconds,
	// but this may vary by source. Delays shorter than the sampling period may
	// not be observed, for example if a blocking operation starts and ends
	// within the same sampling period.
	EventloopDelayAvg int64 `ecs:"eventloop.delay.avg"`

	// The current allocated heap size in bytes.
	MemoryHeapAllocated int64 `ecs:"memory.heap.allocated"`

	// The currently used heap size in bytes.
	MemoryHeapUsed int64 `ecs:"memory.heap.used"`
}
