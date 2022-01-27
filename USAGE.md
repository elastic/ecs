# ECS Tooling Usage

In addition to the published schema and artifacts, the ECS repo also contains tools to generate artifacts based on the current published and custom schemas.

You may be asking if ECS is a specification for storing event data, where does the ECS tooling fit into the picture?  As users implement ECS into their Elastic stack, common questions arise:

* ECS has too many fields. Users don't want to generate mappings for fields they don't plan on using soon.
* Users want to adopt ECS but also want to painlessly maintain their own custom field mappings alongside ECS.

Users can use the ECS tools to tackle both problems. What artifacts are relevant will also vary based on need. Many users will find the Elasticsearch templates most useful, but Beats
contributors will instead find the Beats-formatted YAML field definition files valuable. By maintaining only their customizations and use the tools provided by ECS, they can generate
relevant artifacts for their unique set of data sources.

**NOTE** - These tools and their functionality are considered experimental.

## Table of Contents

- [TLDR Example](#tldr-example)
- [Terminology](#terminology)
- [Setup and Install](#setup-and-install)
  * [Prerequisites](#prerequisites)
    + [Clone from GitHub](#clone-from-github)
    + [Install dependencies](#install-dependencies)
- [Usage](#usage)
  * [Getting Started - Generating Artifacts](#getting-started---generating-artifacts)
  * [Generator Options](#generator-options)
    + [Out](#out)
    + [Include](#include)
    + [Exclude](#exclude)
    + [Subset](#subset)
    + [Ref](#ref)
    + [Mapping & Template Settings](#mapping--template-settings)
    + [Strict Mode](#strict-mode)
    + [Intermediate-Only](#intermediate-only)

## TLDR Example

Before diving into the details, here's a complete example that:

* takes ECS 1.6 fields
* selects only the subset of fields relevant to the project's use case
* includes custom fields relevant to the project
* outputs the resulting artifacts to a project directory
* replace the ECS project's sample template settings and
  mapping settings with ones appropriate to the project

```bash
python scripts/generator.py --ref v1.6.0 \
  --subset            ../my-project/fields/subset.yml \
  --include           ../my-project/fields/custom/ \
  --out               ../my-project/ \
  --template-settings ../my-project/fields/template-settings.json \
  --mapping-settings  ../my-project/fields/mapping-settings.json
```

The generated Elasticsearch template would be output at

`my-project/generated/elasticsearch/legacy/template.json`

If this sounds interesting, read on to learn all about each of these settings.

See [usage-example/](usage-example/) for a complete example with source files.

## Terminology

| Term | Definition |
| ---- | ---------- |
| ECS | Elastic Common Schema. For the purposes of this guide, ECS may refer to either the schema itself or the repo/tooling used to maintain the schema |
| artifacts | Various kinds of files or programs that can be generated based on ECS |
| field set | Groups of related fields in ECS |
| schema | Another term for a group of related fields in ECS. Used interchangeably with field set |
| schema definition | The markup used to define a schema in ECS |
| attributes | The properties of a field or field set that are used to define that field or field set in a schema definition |

## Setup and Install

### Prerequisites

* [Python 3.8+](https://www.python.org/)
* [make](https://www.gnu.org/software/make/)
* [pip](https://pypi.org/project/pip/)
* [git](https://git-scm.com/)

#### Clone from GitHub

The recommended way to download the ECS repo is `git clone`:

```
$ git clone https://github.com/elastic/ecs
$ cd ecs
```

Prior to installing dependencies or running the tools, it's recommended to check out the `git` branch for the ECS version being targeted.

**Example**: For ECS `1.5.0`:

```
$ git checkout v1.5.0
```

#### Install dependencies

Install dependencies using `pip` (An active `virtualenv` is recommended):

```
$ pip install -r scripts/requirements.txt
```

## Usage

### Getting Started - Generating Artifacts

Using the defaults, the [generator](scripts/generator.py) script generates the artifacts based on the [current](schemas) ECS schema.

```
$ python scripts/generator.py
Loading schemas from local files
Running generator. ECS version 1.5.0
```

**Points to note on the defaults**:

* Artifacts are created in the [`generated`](generated) directory and the entire schema is included
* Documentation updates will be written to the appropriate file under the `docs` directory. More specifics on generated doc files is covered in the [contributor's file](https://github.com/elastic/ecs/blob/main/CONTRIBUTING.md#generated-documentation-files)
* Each run of the script will rewrite the entirety of the `generated` directory
* The script will need to be executed from the top-level of the ECS repo
* The `version` displayed when running `generator.py` is based on the current value of the [version](version) file in the top-level of the repo

The generator's defaults are how the ECS team maintains the official artifacts published in the repo. For your own use cases, you may wish to add your own fields or remove others that are unused. The following section details the available options for controlling the output of those artifacts.

### Generator Options

#### Out

Generate the ECS artifacts in a different output directory. If the specified directory doesn't exist, it will be created:

```
$ python scripts/generator.py --out ../myproject/ecs/out/
```

Inside the directory passed in as the target dir to the `--out` flag, two directories, `generated` and `docs`, will be created. `docs` will contain three asciidoc files based on the contents of the provided schema. `generated` will contain the various artifacts laid out as in the published repo (`beats`, `csv`, `ecs`, `elasticsearch`).

> Note: When running using either the `--subset` or `--include` options, the asciidoc files will _not_ be generated.

#### Include

Use the `--include` flag to generate ECS artifacts based on the current ECS schema field definitions plus provided custom fields:

```
$ python scripts/generator.py --include ../myproject/ecs/custom-fields/
$ python scripts/generator.py --include ../myproject/ecs/custom-fields/ ../myproject/ecs/more-custom-fields/
$ python scripts/generator.py --include ../myproject/ecs/custom-fields/myprefix*.yml
$ python scripts/generator.py --include ../myproject/ecs/custom-fields/[some]*[re].yml
$ python scripts/generator.py --include ../myproject/ecs/custom-fields/myfile1.yml ../myproject/ecs/custom-fields/myfile2.yml
```

The `--include` flag expects one or more directories or subsets of schema YAML files using the same [file format](https://github.com/elastic/ecs/tree/master/schemas#fields-supported-in-schemasyml) as the ECS schema files. This is useful for maintaining custom field definitions that are _outside_ of the ECS schema, but allows for merging the custom fields with the official ECS fields for your deployment.

For example, if we defined the following schema definition in a file named `myproject/ecs/custom-fields/widget.yml`:

```yaml
---
- name: widgets
  title: Widgets
  group: 2
  short: Fields describing widgets
  description: >
    The widget fields describe a widget and all its widget-related details.
  type: group
  fields:

    - name: id
      level: extended
      type: keyword
      short: Unique identifier of the widget
      description: >
        Unique identifier of the widget.
```

Multiple directory targets can also be provided:

```
$ python scripts/generator.py \
    --include ../myproject/custom-fields-A/  ../myproject/custom-fields-B \
    --out ../myproject/out/
```

Generate artifacts using `--include` to load our custom definitions in addition to `--out` to place them in the desired output directory:

```
$ python scripts/generator.py --include ../myproject/custom-fields/ --out ../myproject/out/
Loading schemas from local files
Running generator. ECS version 1.5.0
Loading user defined schemas: ['../myproject/custom-fields/']
```

We see the artifacts were generated successfully:

```
$ ls -lah ../myproject/out/
total 0
drwxr-xr-x  2 user  ecs    64B Jul  8 13:12 docs
drwxr-xr-x  6 user  ecs   192B Jul  8 13:12 generated
```

And looking at a specific artifact, `../myprojects/out/generated/elasticsearch/legacy/template.json`, we see our custom fields are included:

```json
...
      "widgets": {
        "properties": {
          "id": {
            "ignore_above": 1024,
            "type": "keyword"
          }
        }
      }
...
```

Include can be used together with the `--ref` flag to merge custom fields into a targeted ECS version. See [`Ref`](#ref).

> NOTE: The `--include` mechanism will not validate custom YAML files prior to merging. This allows for modifying existing ECS fields in a custom schema without having to redefine all the mandatory field attributes.

#### Exclude

Use the `--exclude` flag to generate ephemeral ECS artifacts based on the current ECS schema field definitions minus fields considered for removal, e.g. to assess impact of removing these. Warning! This is not the recommended route to remove a field permanently as it is not intended to be invoked during the build process. Definitive field removal should be implemented using a custom [Subset](#subset) or via the [RFC process](https://github.com/elastic/ecs/tree/main/rfcs/README.md). Example:

```
$ python scripts/generator.py --exclude ../myproject/ecs/custom-fields/
$ python scripts/generator.py --exclude ../myproject/ecs/custom-fields/ ../myproject/ecs/more-custom-fields/
$ python scripts/generator.py --exclude ../myproject/ecs/custom-fields/myprefix*.yml
$ python scripts/generator.py --exclude ../myproject/ecs/custom-fields/[some]*[re].yml
$ python scripts/generator.py --exclude ../myproject/ecs/custom-fields/myfile1.yml ../myproject/ecs/custom-fields/myfile2.yml
```

The `--exclude` flag expects one or more directories or subsets of schema YAML files using the same [file format](https://github.com/elastic/ecs/tree/master/schemas#fields-supported-in-schemasyml) as the ECS schema files. You can also use a subset, provided that relevant `name` and `fields` fields are preserved.

```
---
- name: log
  fields:
    - name: original
```

The root Field Set `name` must always be present and specified with no dots `.`. Subfields may be specified using dot notation, for example:

```
---
- name: log
  fields:
    - name: syslog.severity.name
```

Generate artifacts using `--exclude` to load our custom definitions in addition to `--out` to place them in the desired output directory:

```
$ python scripts/generator.py --exclude ../myproject/exclude-set.yml/ --out ../myproject/out/
Loading schemas from local files
Running generator. ECS version 1.11.0
```

#### Subset

If your indices will never populate particular ECS fields, there's no need to include those field definitions in your index mappings, with the exception of the `base` fieldset, which must exist and which must contain at least the `@timestamp` field. The `--subset` argument allows for passing a subset definition YAML file which indicates which field sets or specific fields to include in the generated artifacts.

```
$ python scripts/generator.py --subset ../myproject/ecs/subset-fields/
$ python scripts/generator.py --subset ../myproject/ecs/subset-fields/ ../myproject/ecs/more-subset-fields/
$ python scripts/generator.py --subset ../myproject/ecs/custom-fields/subset.yml
$ python scripts/generator.py --subset ../myproject/ecs/custom-fields/[some]*[re].yml
$ python scripts/generator.py --subset ../myproject/ecs/custom-fields/myfile1.yml ../myproject/ecs/custom-fields/myfile2.yml
```

Example subset file:

```yaml
---
name: malware_event
fields:
  base:
    fields:
      "@timestamp": {}
  agent:
    fields: "*"
  dll:
    fields: "*"
  ecs:
    fields: "*"
```

The subset file has a defined format, starting with the two top-level required fields:

* `name`: The name of the subset. Also used to name the directory holding the generated subset intermediate files (e.g. `<outputTarget>/generated/ecs/subset/<name>`)
* `fields` Contains the subset field filters

The `fields` object declares which fields to include:

* The targeted field sets are declared underneath `fields` by their top-level name (e.g. `base`, `agent`, etc.)
* Underneath each field set, all sub-fields can be captured using a wildcard syntax: `fields: "*"`
* Individual leafs fields can also be targeted: `@timestamp: {}`

Reviewing the above example, the generator using subset will output artifacts containing:

* The `@timestamp` field from the `base` field set
* All `agent.*` fields, `dll.*`, and `ecs.*` fields

It's also possible to combine `--include` and `--subset` together! Do note that your subset YAML filter file will need to list any custom fields being passed with `--include`. Otherwise, `--subset` will filter those fields out.

Example with `--include` and `--subset` file:

```
python scripts/generator.py --subset ./usage-example/fields/subset.yml --include ./usage-example/fields/custom/acme.yml
```

#### Ref

The `--ref` argument allows for passing a specific `git` tag (e.g. `v1.5.0`) or commit hash (`1454f8b`) that will be used to build ECS artifacts.

```
$ python scripts/generator.py --ref v1.5.0
```

The `--ref` argument loads field definitions from the specified git reference (branch, tag, etc.) from directories [`./schemas`](./schemas) and [`./experimental/schemas`](./experimental/schemas) (when specified via `--include`).

Here's another example loading both ECS fields and [experimental](experimental/README.md) changes *from branch "1.7"*, then adds custom fields on top.

```
$ python scripts/generator.py --ref 1.7 --include experimental/schemas ../myproject/fields/custom --out ../myproject/out
```

The command above will produce artifacts based on:

* main ECS field definitions as of branch 1.7
* experimental ECS changes as of branch 1.7
* custom fields in `../myproject/fields/custom` as they are on the filesystem

> Note: `--ref` does have a dependency on `git` being installed and all expected commits/tags fetched from the ECS upstream repo. This will unlikely be an issue unless you downloaded the ECS as a zip archive from GitHub vs. cloning it.

#### Mapping & Template Settings

The `--template-settings` and `--mapping-settings` arguments allow overriding the default template and mapping settings, respectively, in the generated Elasticsearch template artifacts. Both artifacts expect a JSON file which contains custom settings defined.

```
$ python scripts/generator.py --template-settings ../myproject/es-overrides/template.json --mapping-settings ../myproject/es-overrides/mappings.json
```

The `--template-settings` argument defines [index level settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html#index-modules-settings) that will be applied to the index template in the generated artifacts. This is an example `template.json` to be passed with `--template-setting`:

```json
{
  "index_patterns": ["mylog-*"],
  "order": 1,
  "settings": {
    "index": {
      "mapping": {
        "total_fields": {
          "limit": 10000
        }
      },
      "refresh_interval": "1s"
    }
  },
  "mappings": {}
}
```

`--mapping-settings` works in the same way except now with the [mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html) settings for the index. This is an example `mapping.json` file:

```json
{
  "_meta": {
    "version": "1.5.0"
  },
    "date_detection": false,
    "dynamic_templates": [
      {
        "strings_as_keyword": {
          "mapping": {
            "ignore_above": 1024,
            "type": "keyword"
          },
          "match_mapping_type": "string"
        }
      }
    ],
    "properties": {}
}
```

For `template.json`, the `mappings` object is left empty: `{}`. Likewise the `properties` object remains empty in the `mapping.json` example. This will be filled in automatically by the script.

#### Strict Mode

The `--strict` argument enables "strict mode". Strict mode performs a stricter validation step against the schema's contents.

Basic usage:

```
$ python scripts/generator.py --strict
```

Strict mode requires the following conditions, else the script exits on an exception:

* Short descriptions must be less than or equal to 120 characters.
* Example values containing arrays or objects must be quoted to avoid unexpected YAML interpretation when the schema files or artifacts are relied on downstream.

The current artifacts generated and published in the ECS repo will always be created using strict mode. However, older ECS versions (pre `v1.5.0`) will cause
an exception if attempting to generate them using `--strict`. This is due to schema validation checks introduced after that version was released.

Example:

```
$ python scripts/generator.py --ref v1.4.0 --strict
Loading schemas from git ref v1.4.0
Running generator. ECS version 1.4.0
...
ValueError: Short descriptions must be single line, and under 120 characters (current length: 134).
Offending field or field set: number
Short description:
  Unique number allocated to the autonomous system. The autonomous system number (ASN) uniquely identifies each network on the Internet.
```

Removing `--strict` will display a warning message, but the script will finish its run successfully:

```
$ python scripts/generator.py --ref v1.4.0
Loading schemas from git ref v1.4.0
Running generator. ECS version 1.4.0
/Users/ericbeahan/dev/ecs/scripts/generators/ecs_helpers.py:176: UserWarning: Short descriptions must be single line, and under 120 characters (current length: 134).
Offending field or field set: number
Short description:
  Unique number allocated to the autonomous system. The autonomous system number (ASN) uniquely identifies each network on the Internet.

This will cause an exception when running in strict mode.
```

#### Intermediate-Only

The `--intermediate-only` argument is used for debugging purposes. It only generates the ["intermediate files"](generated/ecs), `ecs_flat.yml` and `ecs_nested.yml`, without generating the rest of the artifacts.
More information on the different intermediate files can be found in the generated directory's [README](generated/README.md).
