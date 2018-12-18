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
	"flag"
	"fmt"
	"log"
	"path/filepath"

	"github.com/elastic/beats/libbeat/common"
	"github.com/elastic/beats/libbeat/template"
	"github.com/elastic/go-ucfg/yaml"
)

// Flags
var (
	schemaDir string
	version   string
)

func init() {
	flag.StringVar(&schemaDir, "schema", "schemas/", "Schema directory containing .yml files.")
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

	fields := common.Fields{}

	for _, path := range paths {
		f := common.Fields{}

		cfg, err := yaml.NewConfigWithFile(path)
		if err != nil {
			log.Fatalf("Error: %v", err)
		}
		cfg.Unpack(&f)

		for key, f2 := range f {
			// The definitions don't have the type group in and the template
			// generator assumes otherwise keyword as default
			f[key].Type = "group"

			// Moves the docs under base to the top level
			if f2.Name == "base" {
				f = f2.Fields
			}
		}

		fields = append(fields, f...)
	}

	// If getting a failure on the following instantiation, check out / update Beats master
	esVersion := common.MustNewVersion("6.0.0")
	t, err := template.New(version, "ecs", *esVersion, template.TemplateConfig{})
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	// Start processing at the root
	properties := common.MapStr{}
	processor := template.Processor{}
	if err := processor.Process(fields, "", properties); err != nil {
		log.Fatalf("Error: %v", err)
	}
	output := t.Generate(properties, nil)

	fmt.Printf("%s", output.StringToPrint())
}
