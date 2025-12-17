# ECS Tooling Usage

In addition to the published schema and artifacts, the ECS repo contains tools to generate artifacts based on ECS schemas and your custom field definitions.

## Why Use ECS Tooling?

* **Subset Generation**: ECS has ~850 fields. Generate mappings for only the fields you need.
* **Custom Fields**: Painlessly maintain your own custom field mappings alongside ECS.
* **Multiple Formats**: Generate Elasticsearch templates, Beats configs, CSV exports, and documentation.

**For detailed developer documentation**, see [scripts/docs/README.md](scripts/docs/README.md).

**NOTE** - These tools and their functionality are considered experimental.

## Table of Contents

- [Quick Start Example](#quick-start-example)
- [Setup and Install](#setup-and-install)
- [Basic Usage](#basic-usage)
- [Key Generator Options](#key-generator-options)
  * [Include Custom Fields](#include-custom-fields)
  * [Subset - Use Only Needed Fields](#subset---use-only-needed-fields)
  * [Ref - Target Specific ECS Version](#ref---target-specific-ecs-version)
  * [Other Options](#other-options)
- [Additional Resources](#additional-resources)

## Quick Start Example

Here's a complete example that generates artifacts with:
* ECS 9.1 fields as the base
* A subset of only needed fields
* Custom fields added on top
* Custom template settings

```bash
python scripts/generator.py \
  --ref v9.1.0 \
  --semconv-version v1.38.0 \
  --subset ../my-project/fields/subset.yml \
  --include ../my-project/fields/custom/ \
  --out ../my-project/
```

This generates:
* `my-project/generated/elasticsearch/composable/` - Modern Elasticsearch templates
* `my-project/generated/elasticsearch/legacy/` - Legacy templates
* `my-project/generated/beats/` - Beats field definitions
* `my-project/generated/csv/` - CSV field reference

**Note**: The `--semconv-version` flag is required. Use the version from the `otel-semconv-version` file or a specific version like `v1.38.0`.

## Setup and Install

**Requirements**: Python 3.8+, git

**Clone and setup**:

```bash
git clone https://github.com/elastic/ecs
cd ecs
git checkout v9.1.0  # Optional: target specific version
pip install -r scripts/requirements.txt  # virtualenv recommended
```

## Basic Usage

Generate artifacts from the current ECS schema:

```bash
make generate
# or
python scripts/generator.py --semconv-version v1.38.0
```

**Key points**:
* Artifacts are created in the `generated/` directory
* Documentation is written to `docs/reference/`
* Each run rewrites the entire `generated/` directory
* Must be run from the ECS repo root
* The `--semconv-version` flag is **required** for OTel integration validation

**For complete documentation on how the generator works**, see:
* [scripts/docs/README.md](scripts/docs/README.md) - Complete developer documentation
* [scripts/docs/schema-pipeline.md](scripts/docs/schema-pipeline.md) - Pipeline details
* [scripts/generator.py](scripts/generator.py) - Comprehensive inline documentation

## Key Generator Options

### Include Custom Fields

Add custom fields to ECS schemas:

```bash
python scripts/generator.py \
  --semconv-version v1.38.0 \
  --include ../myproject/custom-fields/ \
  --out ../myproject/out/
```

**Custom field format** - Use the same YAML format as ECS schemas:

```yaml
---
- name: widgets
  title: Widgets
  group: 2
  short: Fields describing widgets
  description: Widget-related fields
  type: group
  fields:
    - name: id
      level: extended
      type: keyword
      short: Unique identifier of the widget
      description: Unique identifier of the widget.
```

**Supports**: Directories, multiple paths, wildcards (`*.yml`), combining with `--ref`

**See also**: [Schema format documentation](https://github.com/elastic/ecs/tree/main/schemas#fields-supported-in-schemasyml)

### Subset - Use Only Needed Fields

Generate artifacts with only the fields you need (reduces mapping size):

```bash
python scripts/generator.py \
  --semconv-version v1.38.0 \
  --subset ../myproject/subset.yml
```

**Example subset file**:

```yaml
---
name: web_logs
fields:
  base:
    fields:
      "@timestamp": {}
  http:
    fields: "*"        # All http fields
  url:
    fields: "*"        # All url fields
  user_agent:
    fields:
      original: {}     # Specific fields only
```

**Subset format**:
* `name`: Subset name (used for output directory)
* `fields`: Declares which fieldsets/fields to include
  * `fields: "*"` - Include all fields in fieldset
  * `field_name: {}` - Include specific field
  * `docs_only: true` - Include in docs only, not artifacts

**Tips**:
* Combine with `--include` for custom fields (they must be listed in subset)
* Always include `base` fieldset with at least `@timestamp`

**For detailed subset documentation with examples**, see [scripts/docs/schema-pipeline.md](scripts/docs/schema-pipeline.md#subset-filtering)

### Ref - Target Specific ECS Version

Generate artifacts from a specific ECS version:

```bash
python scripts/generator.py \
  --semconv-version v1.38.0 \
  --ref v9.0.0
```

**Combines with other options**:

```bash
# Generate from ECS v9.0.0 + experimental + custom fields
python scripts/generator.py \
  --semconv-version v1.38.0 \
  --ref v9.0.0 \
  --include experimental/schemas ../myproject/fields/custom
```

Loads schemas from git history (tags, branches, commits). Requires git.

### Other Options

**`--out <directory>`** - Output to custom directory
```bash
python scripts/generator.py --semconv-version v1.38.0 --out ../myproject/
```

**`--exclude <files>`** - Remove specific fields (for testing deprecation impact)
```bash
python scripts/generator.py --semconv-version v1.38.0 --exclude deprecated-fields.yml
```

**`--strict`** - Enable strict validation (required for CI/CD)
```bash
python scripts/generator.py --semconv-version v1.38.0 --strict
```

**`--template-settings`** / **`--mapping-settings`** - Custom Elasticsearch template settings
```bash
python scripts/generator.py \
  --semconv-version v1.38.0 \
  --template-settings ../myproject/template.json \
  --mapping-settings ../myproject/mappings.json
```

**`--intermediate-only`** - Generate only intermediate files (for debugging)

**`--force-docs`** - Generate docs even with `--subset`/`--include`/`--exclude`

## Additional Resources

### Complete Documentation

* **[scripts/docs/README.md](scripts/docs/README.md)** - Developer documentation index
* **[scripts/docs/schema-pipeline.md](scripts/docs/schema-pipeline.md)** - Complete pipeline documentation with:
  * Detailed field reuse explanation with visual examples
  * Comprehensive subset filtering guide with real-world examples
  * Troubleshooting section for common issues
* **[scripts/generator.py](scripts/generator.py)** - Comprehensive inline documentation

### Module-Specific Guides

* [OTel Integration](scripts/docs/otel-integration.md) - OpenTelemetry mapping validation
* [Elasticsearch Templates](scripts/docs/es-template.md) - Template generation details
* [Beats Configs](scripts/docs/beats-generator.md) - Beats field definitions
* [CSV Export](scripts/docs/csv-generator.md) - CSV field reference
* [Markdown Docs](scripts/docs/markdown-generator.md) - Documentation generation

### Contributing

* [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
* [Schema Format](https://github.com/elastic/ecs/tree/main/schemas#fields-supported-in-schemasyml) - YAML field definition format
