// Licensed to Elasticsearch B.V. under one or more agreements.
// Elasticsearch B.V. licenses this file to you under the Apache 2.0 License.
// See the LICENSE file in the project root for more information.

package field

// Field represents a single ECS field.
type Field struct {
	Name          string
	Type          string
	Level         string
	Short         string
	Description   string
	AllowedValues []AllowedValue
	IsArray       bool
	Fieldsets     []*Fieldset
	Example       string
}

// AllowedValue represents a single value permitted for an ECS field.
type AllowedValue struct {
	Name        string
	Description string
}

// ExpectedEventType describes the event types expected to accompany a given
// event category (e.g. event.category).
type ExpectedEventType struct {
	Category string
	Types    []string
}
