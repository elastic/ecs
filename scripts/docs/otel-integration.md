# OpenTelemetry Semantic Conventions Integration

## Overview

The OTel integration module (`generators/otel.py`) manages the alignment between Elastic Common Schema (ECS) and OpenTelemetry Semantic Conventions. This is a critical component supporting the ECS donation to OpenTelemetry initiative.

### Purpose

As ECS and OTel Semantic Conventions converge into a single standard, this module:

1. **Validates** that ECS field mappings reference valid OTel attributes and metrics
2. **Enriches** ECS definitions with OTel stability information
3. **Generates** alignment summaries for documentation
4. **Detects** potential unmapped fields that exist in both standards

## Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        generator.py                             │
│                      (Main Entry Point)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OTelGenerator.__init__()                     │
│                                                                 │
│  1. Clone/load OTel semconv repo from GitHub                    │
│  2. Parse all YAML model files                                  │
│  3. Extract attributes and metrics                              │
│  4. Build lookup indexes                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              OTelGenerator.validate_otel_mapping()              │
│                                                                 │
│  Pass 1: Validate mapping structure                             │
│    - Check relation types are valid                             │
│    - Verify required/forbidden properties                       │
│    - Confirm referenced attributes/metrics exist                │
│                                                                 │
│  Pass 2: Enrich with stability information                      │
│    - Add stability levels from OTel definitions                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           OTelGenerator.get_mapping_summaries()                 │
│                                                                 │
│  Generate statistics for each namespace:                        │
│    - Count fields by relation type                              │
│    - Calculate coverage percentages                             │
│    - Used for documentation generation                          │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

#### 1. Model Loading (`get_model_files`, `get_tree_by_url`)

**Purpose**: Load OTel semantic conventions from GitHub

- Clones the semantic-conventions repository (or uses cached version)
- Checks out a specific version tag (e.g., `v1.24.0`)
- Recursively collects all YAML model files
- Caches the repository in `./build/otel-semconv/` for performance

**Key Files**: All `.yml`/`.yaml` files in the `model/` directory of the OTel semconv repo

#### 2. Attribute/Metric Extraction (`get_attributes`, `get_metrics`)

**Purpose**: Parse model files and build lookup indexes

- Extracts non-deprecated attributes from `attribute_group` entries
- Extracts non-deprecated metrics from `metric` entries
- Applies prefixes to attribute IDs (e.g., `http.` prefix)
- Preserves display names for documentation

**Output**: Dictionaries keyed by attribute ID / metric name

#### 3. Validation (`OTelGenerator.validate_otel_mapping`)

**Purpose**: Ensure mapping integrity

- Uses visitor pattern to traverse all ECS fields
- Validates each OTel mapping configuration
- Checks existence of referenced attributes/metrics
- Enriches mappings with stability levels
- Prints warnings for potential unmapped fields

#### 4. Summary Generation (`OTelGenerator.get_mapping_summaries`)

**Purpose**: Generate documentation statistics

- Counts fields by relation type for each namespace
- Identifies OTel-only namespaces (not yet in ECS)
- Produces data structure consumed by markdown generators
- Sorted alphabetically for consistent output

## OTel Mapping Configuration

### Relation Types

ECS fields can have one or more OTel mappings, each with a `relation` type:

#### `match`
Names and semantics are identical.

```yaml
- name: method
  flat_name: http.request.method
  otel:
    - relation: match
```

**Requirements**: No additional properties
**Generated stability**: From OTel attribute definition

#### `equivalent`
Semantically equivalent but different names.

```yaml
- name: status_code
  flat_name: http.response.status_code
  otel:
    - relation: equivalent
      attribute: http.response.status_code
```

**Requirements**: Must specify `attribute`
**Generated stability**: From OTel attribute definition

#### `related`
Related concepts but not semantically identical.

```yaml
- name: original
  flat_name: url.original
  otel:
    - relation: related
      attribute: url.full
      note: Similar but may have different encoding
```

**Requirements**: Must specify `attribute`
**Optional**: `note` explaining the relationship

#### `conflict`
Conflicting definitions that need resolution.

```yaml
- name: bytes
  flat_name: http.request.body.bytes
  otel:
    - relation: conflict
      attribute: http.request.body.size
      note: ECS uses bytes, OTel uses size
```

**Requirements**: Must specify `attribute`
**Optional**: `note` explaining the conflict

#### `metric`
Maps to an OTel metric rather than an attribute.

```yaml
- name: duration
  flat_name: http.client.request.duration
  otel:
    - relation: metric
      metric: http.client.request.duration
```

**Requirements**: Must specify `metric`
**Forbidden**: `attribute`, `otlp_field`

#### `otlp`
Maps to an OTLP protocol-specific field.

```yaml
- name: trace_id
  flat_name: trace.id
  otel:
    - relation: otlp
      otlp_field: trace_id
      stability: stable
```

**Requirements**: Must specify `otlp_field` and `stability`
**Forbidden**: `attribute`, `metric`

#### `na`
Not applicable for OTel mapping.

```yaml
- name: ecs_version
  flat_name: ecs.version
  otel:
    - relation: na
      note: ECS-specific field
```

**Requirements**: None
**Forbidden**: `attribute`, `metric`, `otlp_field`, `stability`

### Validation Rules

The validator enforces strict rules for each relation type:

| Relation | Required Properties | Forbidden Properties | Validates Existence |
|----------|---------------------|---------------------|---------------------|
| `match` | - | attribute, metric, otlp_field, stability | Yes (attribute) |
| `equivalent` | attribute | metric, otlp_field, stability | Yes (attribute) |
| `related` | attribute | metric, otlp_field, stability | Yes (attribute) |
| `conflict` | attribute | metric, otlp_field, stability | Yes (attribute) |
| `metric` | metric | attribute, otlp_field, stability | Yes (metric) |
| `otlp` | otlp_field, stability | attribute, metric | No |
| `na` | - | attribute, metric, otlp_field, stability | No |

## Usage Examples

### Running the Generator

The OTel generator is invoked as part of the main ECS generator:

```bash
# From repository root
make clean
make SEMCONV_VERSION=v1.24.0
```

This triggers `scripts/generator.py`, which:
1. Creates an `OTelGenerator` instance
2. Validates all mappings
3. Generates documentation with summaries

### Programmatic Usage

```python
from generators.otel import OTelGenerator
from schema import loader

# Initialize generator with specific OTel version
generator = OTelGenerator('v1.24.0')

# Load ECS schemas
fields = loader.load_schemas()

# Validate all OTel mappings
generator.validate_otel_mapping(fields)

# Generate summaries for documentation
from generators.intermediate_files import generate_nested_fields
nested = generate_nested_fields(fields)
summaries = generator.get_mapping_summaries(nested)

# Use summaries in documentation
for summary in summaries:
    print(f"{summary['namespace']}: {summary['nr_matching_fields']} matches")
```

## Making Changes

### Adding New Relation Types

If a new relation type is needed:

1. **Update validation** in `OTelGenerator.__check_mapping()`:
   ```python
   elif otel['relation'] == 'new_type':
       must_have(ecs_field_name, otel, otel['relation'], 'required_property')
       must_not_have(ecs_field_name, otel, otel['relation'], 'forbidden_property')
       # Add validation logic
   ```

2. **Update summary counting** in `OTelGenerator.get_mapping_summaries()`:
   ```python
   elif otel['relation'] == "new_type":
       summary['nr_new_type_fields'] += 1
   ```

3. **Update type definition** in `ecs_types/otel_types.py`:
   ```python
   class OTelMappingSummary(TypedDict, total=False):
       # ... existing fields ...
       nr_new_type_fields: int
   ```

4. **Update documentation templates** in `templates/otel_alignment_*.j2`

5. **Update this documentation** with the new relation type

### Updating OTel Semconv Version

To use a newer version of OTel semantic conventions:

1. **Check available versions**:
   Visit https://github.com/open-telemetry/semantic-conventions/tags

2. **Update version file**:
   ```bash
   echo "v1.25.0" > otel-semconv-version
   ```

3. **Regenerate**:
   ```bash
   make clean
   make SEMCONV_VERSION=v1.25.0
   ```

4. **Handle validation errors**:
   - If attributes were renamed: Update ECS mappings in `schemas/*.yml`
   - If attributes were deprecated: Update or remove mappings
   - If validation rules changed: Update `otel.py` validator

### Testing Changes

After modifying the OTel generator:

1. **Run validation**:
   ```bash
   python scripts/generator.py --semconv-version v1.24.0
   ```

2. **Check generated files**:
   - `docs/reference/otel-*.md` - Alignment documentation
   - Verify summary statistics are correct

3. **Run tests** (if applicable):
   ```bash
   python -m pytest scripts/tests/
   ```

## Troubleshooting

### Common Issues

#### "Attribute 'X' does not exist in Semantic Conventions version Y"

**Cause**: ECS field references an OTel attribute that doesn't exist in the specified version

**Solutions**:
- Check if attribute was renamed in OTel
- Update the `attribute` value in the ECS schema
- Verify the semconv version is correct
- Check if attribute was deprecated/removed

#### "OTel mapping must specify the property 'attribute'"

**Cause**: Mapping has relation type requiring the `attribute` property, but it's missing

**Solution**: Add the required property to the mapping:
```yaml
otel:
  - relation: equivalent
    attribute: otel.attribute.name  # Add this
```

#### "Clone is too slow / Network timeout"

**Cause**: First-time clone of semantic-conventions repo can be large

**Solutions**:
- Be patient on first run (repo is cached after)
- Check network connectivity
- Manually clone: `git clone https://github.com/open-telemetry/semantic-conventions.git ./build/otel-semconv/`

#### "WARNING: Field 'X' exists in OTel but is not mapped"

**Cause**: Field name matches OTel attribute but has no mapping defined

**Action**: Consider if this should be mapped:
- If yes: Add appropriate OTel mapping to schema
- If no: Add `otel: [{relation: na}]` to suppress warning

## Related Files

- `scripts/generator.py` - Main entry point, orchestrates generation
- `scripts/generators/markdown_fields.py` - Uses summaries for docs
- `scripts/ecs_types/otel_types.py` - Type definitions
- `scripts/schema/visitor.py` - Field traversal mechanism
- `templates/otel_alignment_*.j2` - Jinja2 templates for docs
- `schemas/*.yml` - ECS field definitions with OTel mappings
- `otel-semconv-version` - File containing target OTel version

## References

- [ECS Documentation](https://www.elastic.co/guide/en/ecs/current/index.html)
- [OTel Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
- [ECS-OTel Convergence Announcement](https://opentelemetry.io/blog/2023/ecs-otel-semconv-convergence/)
- [Semantic Conventions Repository](https://github.com/open-telemetry/semantic-conventions)

