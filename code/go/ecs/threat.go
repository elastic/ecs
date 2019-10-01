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

// Fields to classify events and alerts according to a threat taxonomy such as
// the Mitre ATT&CK framework.
// These fields are for users to classify alerts from all of their sources
// (e.g. IDS, NGFW, etc.) within a  common taxonomy. The threat.technique.* are
// meant to capture the high level category of the threat  (e.g.
// "exfiltration"). The threat.tactic.* fields are meant to capture which kind
// of approach is used by  this detected threat, to accomplish the goal (e.g.
// "data compressed").
type Threat struct {
	// Name of the threat framework used to further categorize and classify the
	// tactic and technique of the reported threat.   Framework classification
	// can be provided by detecting systems, evaluated at ingest time, or
	// retrospectively tagged to events.
	Framework string `ecs:"framework"`

	// Name of the type of tactic used by this threat. You can use the Mitre
	// ATT&CK Matrix Tactic categorization, for example. (ex.
	// https://attack.mitre.org/tactics/TA0040/ )
	TacticName string `ecs:"tactic.name"`

	// The id of tactic used by this threat. You can use the Mitre ATT&CK
	// Matrix Tactic categorization, for example. (ex.
	// https://attack.mitre.org/tactics/TA0040/ )
	TacticID string `ecs:"tactic.id"`

	// The reference url of tactic used by this threat. You can use the Mitre
	// ATT&CK Matrix Tactic categorization, for example. (ex.
	// https://attack.mitre.org/tactics/TA0040/ )
	TacticReference string `ecs:"tactic.reference"`

	// The name of technique used by this tactic. You can use the Mitre ATT&CK
	// Matrix Tactic categorization, for example. (ex.
	// https://attack.mitre.org/techniques/T1499/ )
	TechniqueName string `ecs:"technique.name"`

	// The id of technique used by this tactic. You can use the Mitre ATT&CK
	// Matrix Tactic categorization, for example. (ex.
	// https://attack.mitre.org/techniques/T1499/ )
	TechniqueID string `ecs:"technique.id"`

	// The reference url of technique used by this tactic. You can use the
	// Mitre ATT&CK Matrix Tactic categorization, for example. (ex.
	// https://attack.mitre.org/techniques/T1499/ )
	TechniqueReference string `ecs:"technique.reference"`
}
