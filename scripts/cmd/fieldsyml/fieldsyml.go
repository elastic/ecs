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
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"path/filepath"
	"strings"

	"gopkg.in/yaml.v2"
)

func init() {
	//flag.StringVar(&schemaDir, "schema", "schemas/", "Schema directory containing .yml files.")
	//flag.StringVar(&outputDir, "out", "code/go/ecs", "Output directory for .go files.")
	//flag.StringVar(&version, "version", "", "ECS Version (required)")
}

func main() {

	log.SetFlags(0)
	flag.Parse()

	// READ all yml files
	// sort each key alphabetically
	// move base to top level
	// write yaml file

	files, err := filepath.Glob("schemas/*.yml")
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	var data string
	for _, file := range files {
		d, err := ioutil.ReadFile(file)
		if err != nil {
			log.Fatalf("Error: %v", err)
		}
		data = data + string(d)
	}

	data = strings.Replace(data, "---", "", -1)
	fmt.Println(data)

	var out []map[interface{}]interface{}
	err = yaml.Unmarshal([]byte(data), &out)
	if err != nil {
		log.Fatalf("Unmarshal: %v", err)
	}

	for _, val := range out {
		if val["name"] == "base" {
			fmt.Println("OOOO")
			fmt.Println(val["fields"])
			fields := val["fields"].([]interface{})
			for _, v := range fields {

				fmt.Println("")
				fmt.Println(v)
				fmt.Println("")
				out = append(out, v.(map[interface{}]interface{}))
			}
			//fmt.Println(val["fields"])
		}
	}

	b, err := json.Marshal(out)
	if err != nil {
		fmt.Printf("Error: %s", err)
		return
	}
	fmt.Println(string(b))

	//fmt.Println(files)
	//fmt.Println(err)
	//fmt.Println(out)

	//yamlFile, err := ioutil.ReadFile("conf.yaml")
	//if err != nil {
	//	log.Printf("yamlFile.Get err   #%v ", err)
	//}
	//err = yaml.Unmarshal(yamlFile, c)
	//if err != nil {
	//	log.Fatalf("Unmarshal: %v", err)
	//}

}
