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

// Fields related to the cloud or infrastructure the events are coming from.
type Cloud struct {
	// Name of the cloud provider. Example values are aws, azure, gcp, or
	// digitalocean.
	Provider string `ecs:"provider" json:"provider,omitempty"`

	// Availability zone in which this host is running.
	AvailabilityZone string `ecs:"availability_zone" json:"availability_zone,omitempty"`

	// Region in which this host is running.
	Region string `ecs:"region" json:"region,omitempty"`

	// Instance ID of the host machine.
	InstanceID string `ecs:"instance.id" json:"instance.id,omitempty"`

	// Instance name of the host machine.
	InstanceName string `ecs:"instance.name" json:"instance.name,omitempty"`

	// Machine type of the host machine.
	MachineType string `ecs:"machine.type" json:"machine.type,omitempty"`

	// The cloud account or organization id used to identify different entities
	// in a multi-tenant environment.
	// Examples: AWS account id, Google Cloud ORG Id, or other unique
	// identifier.
	AccountID string `ecs:"account.id" json:"account.id,omitempty"`
}
