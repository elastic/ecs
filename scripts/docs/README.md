# ECS Scripts Developer Documentation

This directory contains developer-focused documentation for the ECS generation scripts.

## Purpose

The ECS repository includes a comprehensive toolchain for generating various artifacts from schema definitions. These developer guides explain:

- **How each component works** internally
- **Architecture and design decisions**
- **How to make changes** and extend functionality
- **Troubleshooting** common issues

## Documentation Structure

### Module-Specific Guides

Each major generator module has its own detailed guide:

- **[otel-integration.md](otel-integration.md)** - OpenTelemetry Semantic Conventions integration
  - Validation of ECS ↔ OTel mappings
  - Loading OTel definitions from GitHub
  - Generating alignment summaries

- **[markdown-generator.md](markdown-generator.md)** - Markdown documentation generation
  - Rendering ECS schemas to human-readable docs
  - Jinja2 template system and customization
  - OTel alignment documentation
  - Adding new page types

- **[intermediate-files.md](intermediate-files.md)** - Intermediate file generation
  - Flat and nested format representations
  - Bridge between schema processing and artifact generation
  - Top-level vs. reusable fieldsets
  - Data structure reference

- **[es-template.md](es-template.md)** - Elasticsearch template generation
  - Composable vs. legacy template formats
  - Field type mapping conversion
  - Template customization and settings
  - Installation and troubleshooting

- **[ecs-helpers.md](ecs-helpers.md)** - Utility functions library
  - Dictionary operations (sorting, merging, copying)
  - File operations (YAML I/O, globbing, directories)
  - Git operations (tree access, version loading)
  - Common patterns and best practices

- **[csv-generator.md](csv-generator.md)** - CSV field reference generation
  - Spreadsheet-compatible field export
  - Column structure and multi-field handling
  - Analysis and integration examples
  - Usage in Excel, Google Sheets, databases

- **[beats-generator.md](beats-generator.md)** - Beats field definition generation
  - YAML field definitions for Elastic Beats
  - Default field selection and allowlist
  - Contextual naming and field groups
  - Integration with Beat modules

*(More module guides will be added here as documentation is expanded)*

### Quick Reference

For high-level usage information, see:
- **[../../USAGE.md](../../USAGE.md)** - User guide for running the generators
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines

## Scripts Overview

The `scripts/` directory contains several key components:

### Core Modules

| Module | Purpose | Documentation |
|--------|---------|---------------|
| `generator.py` | **Main entry point** - orchestrates complete pipeline | Comprehensive docstrings in file |
| `generators/otel.py` | OTel integration and validation | [otel-integration.md](otel-integration.md) |
| `generators/markdown_fields.py` | Markdown documentation generation | [markdown-generator.md](markdown-generator.md) |
| `generators/intermediate_files.py` | Intermediate format generation | [intermediate-files.md](intermediate-files.md) |
| `generators/es_template.py` | Elasticsearch template generation | [es-template.md](es-template.md) |
| `generators/csv_generator.py` | CSV field reference export | [csv-generator.md](csv-generator.md) |
| `generators/beats.py` | Beats field definition generation | [beats-generator.md](beats-generator.md) |
| `generators/ecs_helpers.py` | Shared utility functions | [ecs-helpers.md](ecs-helpers.md) |

### Schema Processing

The schema processing pipeline transforms YAML schema definitions through multiple stages. See [schema-pipeline.md](schema-pipeline.md) for complete pipeline documentation.

| Module | Purpose | Documentation |
|--------|---------|---------------|
| **Pipeline Overview** | Complete schema processing flow | **[schema-pipeline.md](schema-pipeline.md)** |
| `schema/loader.py` | Load and parse YAML schemas → nested structure | [schema-pipeline.md#1-loaderpy---schema-loading](schema-pipeline.md#1-loaderpy---schema-loading) |
| `schema/cleaner.py` | Validate, normalize, apply defaults | [schema-pipeline.md#2-cleanerpy---validation--normalization](schema-pipeline.md#2-cleanerpy---validation--normalization) |
| `schema/finalizer.py` | Perform field reuse, calculate names | [schema-pipeline.md#3-finalizerpy---field-reuse--name-calculation](schema-pipeline.md#3-finalizerpy---field-reuse--name-calculation) |
| `schema/visitor.py` | Traverse field hierarchies (visitor pattern) | [schema-pipeline.md#visitorpy---field-traversal](schema-pipeline.md#visitorpy---field-traversal) |
| `schema/subset_filter.py` | Filter to include only specified fields | [schema-pipeline.md#4-subset_filterpy---subset-filtering-optional](schema-pipeline.md#4-subset_filterpy---subset-filtering-optional) |
| `schema/exclude_filter.py` | Explicitly remove specified fields | [schema-pipeline.md#5-exclude_filterpy---exclude-filtering-optional](schema-pipeline.md#5-exclude_filterpy---exclude-filtering-optional) |

### Types

| Module | Purpose |
|--------|---------|
| `ecs_types/schema_fields.py` | Core ECS type definitions |
| `ecs_types/otel_types.py` | OTel-specific types |

## Getting Started

If you're new to the ECS generator codebase:

1. **Start with the main orchestrator**: Read `generator.py` docstrings to understand the pipeline
2. **Understand schema processing**: Read [schema-pipeline.md](schema-pipeline.md)
3. **Pick a generator**: Choose a specific generator that interests you
4. **Read its documentation**: Start with the module-specific guide
5. **Explore the code**: Read the source with the guide as reference
6. **Run it**: Try generating artifacts to see it in action

### Quick Command Reference

```bash
# Standard generation (from local schemas)
python scripts/generator.py --semconv-version v1.24.0

# From specific git version
python scripts/generator.py --ref v8.10.0 --semconv-version v1.24.0

# With custom schemas
python scripts/generator.py --include custom/schemas/ --semconv-version v1.24.0

# Generate subset only
python scripts/generator.py --subset schemas/subsets/minimal.yml --semconv-version v1.24.0

# Strict validation mode
python scripts/generator.py --strict --semconv-version v1.24.0

# Intermediate files only (fast iteration)
python scripts/generator.py --intermediate-only --semconv-version v1.24.0
```

See `generator.py` docstrings for complete argument documentation.

## Contributing Documentation

When adding or modifying generator code:

1. **Update docstrings**: Add comprehensive Python docstrings to all functions and classes
2. **Update/create guide**: Ensure a markdown guide exists explaining the component
3. **Update this README**: Add links to new documentation
4. **Include examples**: Show practical usage examples
5. **Document edge cases**: Explain tricky parts and gotchas

### Documentation Standards

- **Python docstrings**: Use Google-style docstrings with Args, Returns, Raises, Examples
- **Markdown guides**: Include Overview, Architecture, Usage Examples, Troubleshooting
- **Code examples**: Should be runnable (or clearly marked as pseudocode)
- **Diagrams**: Use ASCII/Unicode diagrams for flow visualization
- **Tables**: Use markdown tables for structured comparisons

## Questions?

For questions about:
- **Using the tools**: See [USAGE.md](../../USAGE.md) or ask in the [Elastic community forums](https://discuss.elastic.co/)
- **Contributing**: See [CONTRIBUTING.md](../../CONTRIBUTING.md)
- **Architecture**: Read the relevant module guide in this directory
- **Bugs**: [Open an issue](https://github.com/elastic/ecs/issues)

