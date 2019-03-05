package main

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/elastic/beats/libbeat/common"
	"github.com/elastic/beats/libbeat/template"
	"github.com/elastic/go-ucfg/yaml"
)

func main() {

	// For the path to be correct, the execution must be from the top directory
	paths, err := filepath.Glob("./schemas/*.yml")
	if err != nil {
		fmt.Printf("Error: %s \n", err)
		os.Exit(1)
	}

	fields := common.Fields{}

	for _, path := range paths {
		f := common.Fields{}

		cfg, err := yaml.NewConfigWithFile(path)
		if err != nil {
			fmt.Printf("Error: %s \n", err)
			os.Exit(1)
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
	version := common.MustNewVersion("7.0.0")
	t, err := template.New("1.0.0", "ecs", *version, template.TemplateConfig{}, false)
	if err != nil {
		fmt.Printf("Error: %s \n", err)
		os.Exit(1)
	}

	// Start processing at the root
	properties := common.MapStr{}
	processor := template.Processor{}
	if err := processor.Process(fields, "", properties); err != nil {
		fmt.Printf("Error: %s \n", err)
		os.Exit(1)
	}
	output := t.Generate(properties, nil)

	fmt.Printf("%s", output.StringToPrint())
}
