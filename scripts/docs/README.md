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
| `generator.py` | Main entry point, orchestrates all generators | *(coming soon)* |
| `generators/otel.py` | OTel integration and validation | [otel-integration.md](otel-integration.md) |
| `generators/markdown_fields.py` | Markdown documentation generation | [markdown-generator.md](markdown-generator.md) |
| `generators/intermediate_files.py` | Intermediate format generation | [intermediate-files.md](intermediate-files.md) |
| `generators/es_template.py` | Elasticsearch template generation | [es-template.md](es-template.md) |
| `generators/csv_generator.py` | CSV field reference export | [csv-generator.md](csv-generator.md) |
| `generators/beats.py` | Beats field definition generation | [beats-generator.md](beats-generator.md) |
| `generators/ecs_helpers.py` | Shared utility functions | [ecs-helpers.md](ecs-helpers.md) |

### Schema Processing

| Module | Purpose | Documentation |
|--------|---------|---------------|
| `schema/loader.py` | Load and parse YAML schemas | *(coming soon)* |
| `schema/cleaner.py` | Normalize and validate schemas | *(coming soon)* |
| `schema/finalizer.py` | Apply final transformations | *(coming soon)* |
| `schema/visitor.py` | Traverse field hierarchies | *(coming soon)* |
| `schema/subset_filter.py` | Filter for subsets | *(coming soon)* |
| `schema/exclude_filter.py` | Exclude specified fields | *(coming soon)* |

### Types

| Module | Purpose |
|--------|---------|
| `ecs_types/schema_fields.py` | Core ECS type definitions |
| `ecs_types/otel_types.py` | OTel-specific types |

## Getting Started

If you're new to the ECS generator codebase:

1. **Start with high-level flow**: Read `generator.py` to understand the overall pipeline
2. **Pick a component**: Choose a generator that interests you
3. **Read its documentation**: Start with the module-specific guide
4. **Explore the code**: Read the source with the guide as reference
5. **Run it**: Try generating artifacts to see it in action

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

