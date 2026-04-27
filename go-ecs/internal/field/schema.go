// Licensed to Elasticsearch B.V. under one or more agreements.
// Elasticsearch B.V. licenses this file to you under the Apache 2.0 License.
// See the LICENSE file in the project root for more information.

package field

// Schema is a parsed ECS schema, comprising its fieldsets, fields, and the
// expected event types for each event category.
type Schema struct {
	Version            string
	Fieldsets          []*Fieldset
	Fields             []*Field
	ExpectedEventTypes []*ExpectedEventType
}
