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

package main

import (
	"bufio"
	"bytes"
	"flag"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
	"text/template"
	"unicode"

	wordwrap "github.com/mitchellh/go-wordwrap"

	"github.com/elastic/beats/libbeat/common"
	"github.com/elastic/go-ucfg/yaml"
)

const license = `
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
// under the License.`

const typeTmpl = `
{{.License}}

// Code generated by scripts/gocodegen.go - DO NOT EDIT.

package ecs

{{if .ImportTime -}}

import (
	"time"
)

{{end -}}

// {{.Description}}
type {{.Name}} struct {
{{- range $field := .Fields}}
	// {{$field.Comment}}
	{{$field.Name}} {{$field.Type}} \u0060ecs:"{{$field.JSONKey}}"\u0060
{{ end -}}
}

{{ range $nestedField := .NestedTypes }}
type {{$nestedField.Name}} struct {
{{- range $field := $nestedField.Fields}}
	// {{$field.Comment}}
	{{$field.Name}} {{$field.Type}} \u0060ecs:"{{$field.JSONKey}}"\u0060
{{ end -}}
}
{{ end -}}
`

const versionTmpl = `
{{.License}}

// Code generated by scripts/gocodegen.go - DO NOT EDIT.

package ecs

// Version is the Elastic Common Schema version from which this was generated.
const Version = "{{.Version}}"
`

var (
	goFileTemplate = template.Must(template.New("type").Parse(
		strings.Replace(typeTmpl[1:], `\u0060`, "`", -1)))

	versionFileTemplate = template.Must(template.New("version").Parse(
		versionTmpl[1:]))
)

type GoType struct {
	License     string
	Description string
	Name        string
	Fields      []Field
	NestedTypes map[string]*NestedField
    // NestedTypes []NestedField
	ImportTime  bool
}

type NestedField struct {
	Name       string
	Type       string
	Fields     []Field
	ImportTime bool
}

type Field struct {
	Comment string
	Name    string
	Type    string
	JSONKey string
}

// Flags
var (
	schemaDir string
	outputDir string
	version   string
)

func init() {
	flag.StringVar(&schemaDir, "schema", "schemas/", "Schema directory containing .yml files.")
	flag.StringVar(&outputDir, "out", "code/go/ecs", "Output directory for .go files.")
	flag.StringVar(&version, "version", "", "ECS Version (required)")
}

func main() {
	log.SetFlags(0)
	flag.Parse()

	if version == "" {
		log.Fatalf("Error: -version is required")
	}

	paths, err := filepath.Glob(filepath.Join(schemaDir, "*.yml"))
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	// Load schema files.
	fields := common.Fields{}
	for _, path := range paths {
		f := common.Fields{}

		cfg, err := yaml.NewConfigWithFile(path)
		if err != nil {
			log.Fatalf("Error: %v", err)
		}
		if err = cfg.Unpack(&f); err != nil {
			log.Fatalf("Error: %v", err)
		}

		for key := range f {
			// The definitions don't have the type group in and the template
			// generator assumes otherwise keyword as default.
			f[key].Type = "group"
		}

		fields = append(fields, f...)
	}

	// Generate Go source code.
	goFiles := map[string][]byte{}
	for _, group := range fields {
		if group.Type == "group" {
			t := GoType{
				License:     license[1:],
				Description: descriptionToComment("", group.Description),
				Name:        goTypeName(group.Name),
				NestedTypes: make(map[string]*NestedField),
			}

			 for _, field := range group.Fields {
				// handle `nested` fields
				if field.Type == "nested" {
					n := NestedField{
						Name: goTypeName(field.Name),
						Type: "nested",
					}

				    t.NestedTypes[field.Name] = &n
					fieldName := goTypeName(field.Name)
					t.Fields = append(t.Fields, Field{
                        Comment: descriptionToComment("\t", field.Description),
						Name:    goTypeName(fieldName),
						Type:    "[]" + goTypeName(fieldName),
					})

				} else {
					dataType := goDataType(field.Name, field.Type)
					if strings.HasPrefix(dataType, "time.") {
						t.ImportTime = true
					}

					// check if field belongs under a nested field
					if nestedField, ok := t.NestedTypes[(trimStringFromDot(field.Name))]; ok {
						prefix := strings.ToLower(nestedField.Name) + "."
						fieldNameWithoutPrefix := strings.ReplaceAll(field.Name, prefix, "")
						nestedField.Fields = append(nestedField.Fields, Field{
							Comment: descriptionToComment("\t", field.Description),
							Name:    goTypeName(fieldNameWithoutPrefix),
							Type:    dataType,
							JSONKey: fieldNameWithoutPrefix,
						})
					} else {
					    t.Fields = append(t.Fields, Field{
					    	Comment: descriptionToComment("\t", field.Description),
					    	Name:    goTypeName(field.Name),
					    	Type:    dataType,
					    	JSONKey: field.Name,
					    })
				    }
				}
			}

			b := new(bytes.Buffer)
			err := goFileTemplate.Execute(b, t)
			if err != nil {
				log.Fatal(err)
			}

			goFiles[group.Name+".go"] = b.Bytes()
		}
	}

	// Create version.go containing a the version as a constant.
	b := new(bytes.Buffer)
	err = versionFileTemplate.Execute(b, map[string]interface{}{
		"License": license[1:],
		"Version": version,
	})
	if err != nil {
		log.Fatal(err)
	}
	goFiles["version.go"] = b.Bytes()

	// Output the files if there were no errors.
	for name, data := range goFiles {
		if err := os.MkdirAll(outputDir, 0755); err != nil {
			log.Fatalf("Error: %v", err)
		}
		if err := ioutil.WriteFile(filepath.Join(outputDir, name), data, 0644); err != nil {
			log.Fatalf("Error: %v", err)
		}
	}
}

// isSeparate returns true if the character is a field name separator. This is
// used to detect the separators in fields like ephemeral_id or instance.name.
func isSeparator(c rune) bool {
	switch c {
	case '.', '_':
		return true
	case '@':
		// This effectively filters @ from field names.
		return true
	default:
		return false
	}
}

// descriptionToComment builds a comment string that is wrapped at 80 chars.
func descriptionToComment(indent, desc string) string {
	textLength := 80 - len(strings.Replace(indent, "\t", "    ", 4)+" // ")
	lines := strings.Split(wordwrap.WrapString(desc, uint(textLength)), "\n")
	if len(lines) > 0 {
		// Remove empty first line.
		if strings.TrimSpace(lines[0]) == "" {
			lines = lines[1:]
		}
	}
	if len(lines) > 0 {
		// Remove empty last line.
		if strings.TrimSpace(lines[len(lines)-1]) == "" {
			lines = lines[:len(lines)-1]
		}
	}
	for i := 0; i < len(lines); i++ {

	}
	return trimTrailingWhitespace(strings.Join(lines, "\n"+indent+"// "))
}

func trimTrailingWhitespace(text string) string {
	var lines [][]byte
	s := bufio.NewScanner(bytes.NewBufferString(text))
	for s.Scan() {
		lines = append(lines, bytes.TrimRightFunc(s.Bytes(), unicode.IsSpace))
	}
	if err := s.Err(); err != nil {
		log.Fatal(err)
	}
	return string(bytes.Join(lines, []byte("\n")))
}

// goDataType returns the Go type to use for Elasticsearch mapping data type.
func goDataType(fieldName, elasticsearchDataType string) string {
	// Special cases.
	switch {
	case fieldName == "duration" && elasticsearchDataType == "long":
		return "time.Duration"
	case fieldName == "args" && elasticsearchDataType == "keyword":
		return "[]string"
	}

	switch elasticsearchDataType {
	case "keyword", "wildcard", "version", "constant_keyword", "text", "ip", "geo_point", "flattened":
		return "string"
	case "long":
		return "int64"
	case "integer":
		return "int32"
	case "float", "scaled_float":
		return "float64"
	case "date":
		return "time.Time"
	case "boolean":
		return "bool"
	case "object", "flattened":
		return "map[string]interface{}"
	default:
		log.Fatalf("no translation for %v (field %s)", elasticsearchDataType, fieldName)
		return ""
	}
}

// abbreviations capitalizes common abbreviations.
func abbreviations(abv string) string {
	switch strings.ToLower(abv) {
	case "id", "ppid", "pid", "pgid", "mac", "ip", "iana", "uid", "ecs", "as":
		return strings.ToUpper(abv)
	default:
		return abv
	}
}

// goTypeName removes special characters ('_', '.', '@') and returns a
// camel-cased name.
func goTypeName(name string) string {
	var b strings.Builder
	for _, w := range strings.FieldsFunc(name, isSeparator) {
		b.WriteString(strings.Title(abbreviations(w)))
	}
	return b.String()
}

// trim strings after "." character
func trimStringFromDot(s string) string {
	if idx := strings.Index(s, "."); idx != -1 {
		return s[:idx]
	}
	return s
}
