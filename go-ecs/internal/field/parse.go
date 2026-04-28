// Licensed to Elasticsearch B.V. under one or more agreements.
// Elasticsearch B.V. licenses this file to you under the Apache 2.0 License.
// See the LICENSE file in the project root for more information.

package field

import (
	"slices"
	"sort"

	"github.com/goccy/go-yaml"
)

type allowedValueDef struct {
	Name               string   `yaml:"name"`
	Description        string   `yaml:"description"`
	ExpectedEventTypes []string `yaml:"expected_event_types"`
}

type fieldDef struct {
	Type             string            `yaml:"type"`
	Level            string            `yaml:"level"`
	Short            string            `yaml:"short"`
	Example          string            `yaml:"example"`
	Description      string            `yaml:"description"`
	AllowedValues    []allowedValueDef `yaml:"allowed_values"`
	Normalize        any               `yaml:"normalize"`
	OriginalFieldset string            `yaml:"original_fieldset"`
}

type fieldsetDef struct {
	Fields      map[string]fieldDef `yaml:"fields"`
	Description string              `yaml:"description"`
	Short       string              `yaml:"short"`

	Reusable *struct {
		TopLevel bool `yaml:"top_level"`
	} `yaml:"reusable"`
}

func (f *fieldsetDef) allowedAtRoot() bool {
	if f.Reusable != nil && !f.Reusable.TopLevel {
		return false
	}

	return true
}

// Parse will parse Fieldsets and Fields from the provided data. The data is
// expected to be in the format of a generated ecs_nested.yml file.
func Parse(data []byte) (*Schema, error) {
	var schema Schema

	var raw map[string]fieldsetDef
	if err := yaml.Unmarshal(data, &raw); err != nil {
		return nil, err
	}

	fieldsetMap := map[string]*Fieldset{}
	fieldMap := map[string]*Field{}

	// Pass 1: Get fieldsets
	for kfs, vfs := range raw {
		fs := &Fieldset{
			Name:        kfs,
			Short:       vfs.Short,
			Description: vfs.Description,
			TopLevel:    true,
		}
		if vfs.Reusable != nil {
			fs.TopLevel = vfs.Reusable.TopLevel
		}
		fieldsetMap[kfs] = fs
	}

	// Pass 2: Get fields
	for kfs, vfs := range raw {
		if !vfs.allowedAtRoot() {
			continue
		}
		for kf, vf := range vfs.Fields {
			f := &Field{
				Name:        kf,
				Type:        vf.Type,
				Level:       vf.Level,
				Short:       vf.Short,
				Description: vf.Description,
				Fieldsets:   []*Fieldset{fieldsetMap[kfs]},
				Example:     vf.Example,
			}
			switch v := vf.Normalize.(type) {
			case []any:
				slices.ContainsFunc(v, func(item any) bool {
					switch vi := item.(type) {
					case string:
						if vi == "array" {
							f.IsArray = true
							return true
						}
					}
					return false
				})
			case string:
				f.IsArray = v == "array"
			}
			if vf.OriginalFieldset != "" {
				fs := fieldsetMap[vf.OriginalFieldset]
				if !slices.Contains(f.Fieldsets, fs) {
					f.Fieldsets = append(f.Fieldsets, fieldsetMap[vf.OriginalFieldset])
				}
			}
			if len(vf.AllowedValues) > 0 {
				f.AllowedValues = make([]AllowedValue, 0, len(vf.AllowedValues))
				for _, v := range vf.AllowedValues {
					f.AllowedValues = append(f.AllowedValues, AllowedValue{
						Name:        v.Name,
						Description: v.Description,
					})
					if len(v.ExpectedEventTypes) > 0 {
						eet := &ExpectedEventType{
							Category: v.Name,
							Types:    make([]string, 0, len(v.ExpectedEventTypes)),
						}
						for _, eev := range v.ExpectedEventTypes {
							eet.Types = append(eet.Types, eev)
						}
						schema.ExpectedEventTypes = append(schema.ExpectedEventTypes, eet)
					}
				}
			}

			fieldMap[kf] = f
		}
	}

	schema.Fieldsets = make([]*Fieldset, 0, len(fieldsetMap))
	for _, fieldset := range fieldsetMap {
		schema.Fieldsets = append(schema.Fieldsets, fieldset)
	}
	sort.Slice(schema.Fieldsets, func(i, j int) bool {
		return schema.Fieldsets[i].Name < schema.Fieldsets[j].Name
	})

	schema.Fields = make([]*Field, 0, len(fieldMap))
	for _, field := range fieldMap {
		schema.Fields = append(schema.Fields, field)
	}
	sort.Slice(schema.Fields, func(i, j int) bool {
		return schema.Fields[i].Name < schema.Fields[j].Name
	})
	sort.Slice(schema.ExpectedEventTypes, func(i, j int) bool {
		return schema.ExpectedEventTypes[i].Category < schema.ExpectedEventTypes[j].Category
	})

	return &schema, nil
}
