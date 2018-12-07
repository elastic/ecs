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
	"bytes"
	"flag"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
	"text/template"
	"unicode"

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
	ImportTime  bool
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

		for key, f2 := range f {
			// The definitions don't have the type group in and the template
			// generator assumes otherwise keyword as default.
			f[key].Type = "group"

			// Moves the docs under base to the top level.
			if f2.Name == "base" {
				f = f2.Fields
			}
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
				Name:        strings.Title(abbreviations(group.Name)),
			}

			for _, field := range group.Fields {
				var b strings.Builder
				for _, n := range strings.FieldsFunc(field.Name, isSeparator) {
					b.WriteString(strings.Title(abbreviations(n)))
				}

				dataType := goDataType(field.Name, field.Type)
				if strings.HasPrefix(dataType, "time.") {
					t.ImportTime = true
				}

				t.Fields = append(t.Fields, Field{
					Comment: descriptionToComment("\t", field.Description),
					Name:    b.String(),
					Type:    dataType,
					JSONKey: field.Name,
				})
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
// used to detect the separators in fields lik ephemeral_id or instance.name.
func isSeparator(c rune) bool {
	switch c {
	case '.', '_':
		return true
	default:
		return false
	}
}

// descriptionToComment builds a comment string that is wrapped at 80 chars.
func descriptionToComment(indent, desc string) string {
	textLength := 80 - len(strings.Replace(indent, "\t", "    ", 4)+" // ")
	lines := strings.Split(wrapString(desc, uint(textLength)), "\n")
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
	return strings.Join(lines, "\n"+indent+"// ")
}

// wrapString wraps the given string within lim width in characters.
//
// Wrapping is currently naive and only happens at white-space. A future
// version of the library will implement smarter wrapping. This means that
// pathological cases can dramatically reach past the limit, such as a very
// long word.
//
// https://github.com/mitchellh/go-wordwrap
//
// The MIT License (MIT)
//
// Copyright (c) 2014 Mitchell Hashimoto
func wrapString(s string, lim uint) string {
	// Initialize a buffer with a slightly larger size to account for breaks
	init := make([]byte, 0, len(s))
	buf := bytes.NewBuffer(init)

	var current uint
	var wordBuf, spaceBuf bytes.Buffer

	for _, char := range s {
		if char == '\n' {
			if wordBuf.Len() == 0 {
				if current+uint(spaceBuf.Len()) > lim {
					current = 0
				} else {
					current += uint(spaceBuf.Len())
					spaceBuf.WriteTo(buf)
				}
				spaceBuf.Reset()
			} else {
				current += uint(spaceBuf.Len() + wordBuf.Len())
				spaceBuf.WriteTo(buf)
				spaceBuf.Reset()
				wordBuf.WriteTo(buf)
				wordBuf.Reset()
			}
			buf.WriteRune(char)
			current = 0
		} else if unicode.IsSpace(char) {
			if spaceBuf.Len() == 0 || wordBuf.Len() > 0 {
				current += uint(spaceBuf.Len() + wordBuf.Len())
				spaceBuf.WriteTo(buf)
				spaceBuf.Reset()
				wordBuf.WriteTo(buf)
				wordBuf.Reset()
			}

			spaceBuf.WriteRune(char)
		} else {

			wordBuf.WriteRune(char)

			if current+uint(spaceBuf.Len()+wordBuf.Len()) > lim && uint(wordBuf.Len()) < lim {
				buf.WriteRune('\n')
				current = 0
				spaceBuf.Reset()
			}
		}
	}

	if wordBuf.Len() == 0 {
		if current+uint(spaceBuf.Len()) <= lim {
			spaceBuf.WriteTo(buf)
		}
	} else {
		spaceBuf.WriteTo(buf)
		wordBuf.WriteTo(buf)
	}

	return buf.String()
}

// goDataType returns the Go type to use for Elasticsearch mapping data type.
func goDataType(fieldName, elasticsearchDataType string) string {
	// Special cases.
	switch {
	case fieldName == "duration" && elasticsearchDataType == "long":
		return "time.Duration"
	}

	switch elasticsearchDataType {
	case "keyword", "text", "ip", "geo_point":
		return "string"
	case "long":
		return "int64"
	case "integer":
		return "int32"
	case "float":
		return "float64"
	case "date":
		return "time.Time"
	case "object":
		return "map[string]interface{}"
	default:
		log.Fatal("no translation for ", elasticsearchDataType)
		return ""
	}
}

// abbreviations capitalizes common abbreviations.
func abbreviations(abv string) string {
	switch strings.ToLower(abv) {
	case "id", "ppid", "pid", "mac", "ip", "iana", "uid", "ecs":
		return strings.ToUpper(abv)
	default:
		return abv
	}
}
