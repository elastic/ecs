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

	// For the path tob e correct, the execution must be from the top directory
	paths, err := filepath.Glob("./schemas/*")
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

	t, err := template.New("1.0.0", "ecs", "6.0.0", template.TemplateConfig{})
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
