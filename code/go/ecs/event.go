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

// The event fields are used for context information about the log or metric
// event itself.
// A log is defined as an event containing details of something that happened.
// Log events must include the time at which the thing happened. Examples of
// log events include a process starting on a host, a network packet being sent
// from a source to a destination, or a network connection between a client and
// a server being initiated or closed. A metric is defined as an event
// containing one or more numerical or categorical measurements and the time at
// which the measurement was taken. Examples of metric events include memory
// pressure measured on a host, or vulnerabilities measured on a scanned host.
type Event struct {
	// Unique ID to describe the event.
	ID string `ecs:"id"`

	// The kind of the event.
	// This gives information about what type of information the event
	// contains, without being specific to the contents of the event.  Examples
	// are `event`, `state`, `alarm`. Warning: In future versions of ECS, we
	// plan to provide a list of acceptable values for this field, please use
	// with caution.
	Kind string `ecs:"kind"`

	// Event category.
	// This contains high-level information about the contents of the event. It
	// is more generic than `event.action`, in the sense that typically a
	// category contains multiple actions. Warning: In future versions of ECS,
	// we plan to provide a list of acceptable values for this field, please
	// use with caution.
	Category string `ecs:"category"`

	// The action captured by the event.
	// This describes the information in the event. It is more specific than
	// `event.category`. Examples are `group-add`, `process-started`,
	// `file-created`. The value is normally defined by the implementer.
	Action string `ecs:"action"`

	// The outcome of the event.
	// If the event describes an action, this fields contains the outcome of
	// that action. Examples outcomes are `success` and `failure`. Warning: In
	// future versions of ECS, we plan to provide a list of acceptable values
	// for this field, please use with caution.
	Outcome string `ecs:"outcome"`

	// Reserved for future usage.
	// Please avoid using this field for user data.
	Type string `ecs:"type"`

	// Name of the module this data is coming from.
	// This information is coming from the modules used in Beats or Logstash.
	Module string `ecs:"module"`

	// Name of the dataset.
	// The concept of a `dataset` (fileset / metricset) is used in Beats as a
	// subset of modules. It contains the information which is currently stored
	// in metricset.name and metricset.module or fileset.name.
	Dataset string `ecs:"dataset"`

	// Severity describes the original severity of the event. What the
	// different severity values mean can very different between use cases.
	// It's up to the implementer to make sure severities are consistent across
	// events.
	Severity int64 `ecs:"severity"`

	// Raw text message of entire event. Used to demonstrate log integrity.
	// This field is not indexed and doc_values are disabled. It cannot be
	// searched, but it can be retrieved from `_source`.
	Original string `ecs:"original"`

	// Hash (perhaps logstash fingerprint) of raw field to be able to
	// demonstrate log integrity.
	Hash string `ecs:"hash"`

	// Duration of the event in nanoseconds.
	// If event.start and event.end are known this value should be the
	// difference between the end and start time.
	Duration time.Duration `ecs:"duration"`

	// This field should be populated when the event's timestamp does not
	// include timezone information already (e.g. default Syslog timestamps).
	// It's optional otherwise.
	// Acceptable timezone formats are: a canonical ID (e.g.
	// "Europe/Amsterdam"), abbreviated (e.g. "EST") or an HH:mm differential
	// (e.g. "-05:00").
	Timezone string `ecs:"timezone"`

	// event.created contains the date when the event was created.
	// This timestamp is distinct from @timestamp in that @timestamp contains
	// the processed timestamp. For logs these two timestamps can be different
	// as the timestamp in the log line and when the event is read for example
	// by Filebeat are not identical. `@timestamp` must contain the timestamp
	// extracted from the log line, event.created when the log line is read.
	// The same could apply to package capturing where @timestamp contains the
	// timestamp extracted from the network package and event.created when the
	// event was created.
	// In case the two timestamps are identical, @timestamp should be used.
	Created time.Time `ecs:"created"`

	// event.start contains the date when the event started or when the
	// activity was first observed.
	Start time.Time `ecs:"start"`

	// event.end contains the date when the event ended or when the activity
	// was last observed.
	End time.Time `ecs:"end"`

	// Risk score or priority of the event (e.g. security solutions). Use your
	// system's original value here.
	RiskScore float64 `ecs:"risk_score"`

	// Normalized risk score or priority of the event, on a scale of 0 to 100.
	// This is mainly useful if you use more than one system that assigns risk
	// scores, and you want to see a normalized value across all systems.
	RiskScoreNorm float64 `ecs:"risk_score_norm"`
}
