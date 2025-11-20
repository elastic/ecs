# Intermediate File Generator

## Overview

The Intermediate File Generator (`generators/intermediate_files.py`) is a critical component in the ECS build pipeline. It transforms processed schemas into standardized intermediate representations that serve as the foundation for all downstream artifact generation.

### Purpose

This generator bridges the gap between schema processing and artifact generation by creating two normalized formats:

1. **Flat Format** (`ecs_flat.yml`) - Single-level field dictionary
2. **Nested Format** (`ecs_nested.yml`) - Hierarchical fieldset organization

These intermediate files provide:
- **Stable Interface**: Consistent data structure for all generators
- **Separation of Concerns**: Schema processing logic separate from artifact generation
- **Debugging Aid**: Human-readable checkpoints in the pipeline
- **Multiple Consumers**: CSV, Elasticsearch templates, Beats, documentation

## Architecture

### Pipeline Position

```
┌─────────────────────────────────────────────────────────────────┐
│                     Schema Processing                            │
│                                                                  │
│  1. loader.py       - Load YAML schemas from files              │
│  2. cleaner.py      - Normalize and validate                    │
│  3. finalizer.py    - Apply transformations                     │
│  4. subset_filter.py - Optional filtering                       │
│  5. exclude_filter.py - Optional exclusions                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              intermediate_files.generate()                       │
│                    [THIS MODULE]                                 │
│                                                                  │
│  Input: Dict[str, FieldEntry] (processed schemas)               │
│                                                                  │
│  ┌───────────────────────┐  ┌───────────────────────┐          │
│  │ generate_flat_fields()│  │generate_nested_fields()│          │
│  │                       │  │                        │          │
│  │ • Filter non-root     │  │ • Keep all fieldsets   │          │
│  │ • Flatten hierarchy   │  │ • Group by fieldset    │          │
│  │ • Index by flat_name  │  │ • Preserve metadata    │          │
│  └───────────┬───────────┘  └──────────┬─────────────┘          │
│              │                         │                        │
│              ▼                         ▼                        │
│    ecs_flat.yml (850 fields)  ecs_nested.yml (45 fieldsets)    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Artifact Generators                           │
│                                                                  │
│  • CSV Generator         - Uses ecs_flat.yml                    │
│  • Elasticsearch         - Uses ecs_nested.yml                  │
│  • Beats Generator       - Uses ecs_nested.yml                  │
│  • Markdown Generator    - Uses ecs_nested.yml                  │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Input: Processed Schemas
  ↓
{
  'http': {
    'field_details': {...},
    'schema_details': {...},
    'fields': {
      'request': {
        'fields': {
          'method': {
            'field_details': {
              'flat_name': 'http.request.method',
              'type': 'keyword',
              ...
            }
          }
        }
      }
    }
  }
}
  ↓
  ├─── generate_flat_fields() ───→ Flat Format
  │                                 {
  │                                   'http.request.method': {
  │                                     'name': 'method',
  │                                     'type': 'keyword',
  │                                     ...
  │                                   }
  │                                 }
  │
  └─── generate_nested_fields() ──→ Nested Format
                                    {
                                      'http': {
                                        'name': 'http',
                                        'title': 'HTTP',
                                        'fields': {
                                          'http.request.method': {...}
                                        }
                                      }
                                    }
```

## File Formats

### Flat Format (ecs_flat.yml)

**Purpose**: Quick lookup and iteration over all fields

**Structure**:
```yaml
# Single-level dictionary, fields indexed by full dotted name
http.request.method:
  name: method
  flat_name: http.request.method
  type: keyword
  description: HTTP request method
  example: GET
  level: extended
  normalize:
    - array
  otel:
    - relation: match
      stability: stable

http.response.status_code:
  name: status_code
  flat_name: http.response.status_code
  type: long
  description: HTTP response status code
  example: 404
  level: extended
```

**Characteristics**:
- **Keys**: Full dotted field names (e.g., `http.request.method`)
- **Values**: Complete field definitions
- **Excludes**: Non-root reusable fieldsets (top_level=false)
- **Excludes**: Intermediate structural fields
- **Count**: ~850 fields in standard ECS

**Use Cases**:
- CSV generation (one row per field)
- Simple field lookups by name
- Validation scripts
- Field counting and statistics

### Nested Format (ecs_nested.yml)

**Purpose**: Preserve logical grouping and fieldset metadata

**Structure**:
```yaml
# Top-level: fieldsets
http:
  name: http
  title: HTTP
  group: 2
  description: Fields related to HTTP activity
  type: group
  reusable:
    top_level: true
    expected:
      - client
      - server
  reused_here:
    - full: http.request
      short: request
      schema_name: http.request
  fields:
    # Flat dictionary of all fields in this fieldset
    http.request.method:
      name: method
      flat_name: http.request.method
      type: keyword
      description: HTTP request method
      ...
    http.response.status_code:
      name: status_code
      flat_name: http.response.status_code
      type: long
      ...

user:
  name: user
  title: User
  group: 2
  description: User fields
  reusable:
    top_level: true
    expected:
      - client
      - destination
      - server
      - source
  fields:
    user.email:
      name: email
      ...
```

**Characteristics**:
- **Keys**: Fieldset names (e.g., `http`, `user`, `process`)
- **Values**: Fieldset metadata + fields dictionary
- **Includes**: All fieldsets (even top_level=false)
- **Fields**: Stored in nested `fields` dict (still flat, not hierarchical)
- **Count**: ~45 fieldsets in standard ECS

**Use Cases**:
- Documentation generation (one page per fieldset)
- Elasticsearch templates (field grouping)
- Beats configuration
- Understanding field relationships

## Key Concepts

### Top-Level vs. Non-Root Reusable Fieldsets

Some fieldsets are designed ONLY to be reused in specific locations:

**Non-Root Reusable** (top_level=false):
```yaml
# geo fieldset - only valid under client.geo, source.geo, etc.
geo:
  reusable:
    top_level: false  # Never appears as geo.* at root
    expected:
      - client.geo
      - destination.geo
      - source.geo
```

**Root Reusable** (top_level=true):
```yaml
# user fieldset - valid at root AND reused locations
user:
  reusable:
    top_level: true  # Can appear as user.* at root
    expected:
      - client.user
      - destination.user
      - source.user
```

**Filtering Behavior**:
- **Flat format**: Excludes top_level=false fieldsets
- **Nested format**: Includes all fieldsets (consumers decide)

### Intermediate Fields

Some fields exist only for structural purposes:

```yaml
# Intermediate field - creates hierarchy but isn't a real field
http.request:
  intermediate: true  # Not a field itself
  fields:
    method: {...}     # Actual field: http.request.method
    body: {...}       # Actual field: http.request.body
```

These are excluded from intermediate files as they don't represent actual data.

### Internal Attributes

Attributes removed from final output:
- `node_name`: Internal tree traversal identifier
- `intermediate`: Flag for structural-only fields
- `dashed_name`: Alternative name format (not needed in output)

## Usage Examples

### Running the Generator

Typically invoked through the main generator:

```bash
# From repository root
make clean
make SEMCONV_VERSION=v1.24.0

# Or directly with Python
python scripts/generator.py --semconv-version v1.24.0
```

### Programmatic Usage

```python
from schema import loader, cleaner, finalizer
from generators.intermediate_files import generate

# Process schemas
fields = loader.load_schemas()
cleaner.clean(fields)
finalizer.finalize(fields)

# Generate intermediate files
nested, flat = generate(
    fields=fields,
    out_dir='generated/ecs',
    default_dirs=True  # Also save raw ecs.yml
)

# Use the returned structures
print(f"Total fields: {len(flat)}")
print(f"Total fieldsets: {len(nested)}")

# Access specific field
method_field = flat['http.request.method']
print(f"Type: {method_field['type']}")

# Access fieldset
http_fieldset = nested['http']
print(f"Title: {http_fieldset['title']}")
print(f"Fields in HTTP: {len(http_fieldset['fields'])}")
```

### Reading Generated Files

```python
import yaml

# Load flat format
with open('generated/ecs/ecs_flat.yml') as f:
    flat = yaml.safe_load(f)
    
# Iterate all fields
for field_name, field_def in flat.items():
    print(f"{field_name}: {field_def['type']}")

# Load nested format
with open('generated/ecs/ecs_nested.yml') as f:
    nested = yaml.safe_load(f)

# Process by fieldset
for fieldset_name, fieldset in nested.items():
    print(f"\n{fieldset['title']} ({fieldset_name})")
    for field_name in fieldset['fields']:
        print(f"  - {field_name}")
```

## Making Changes

### Adding New Field Attributes

If you add a new attribute to field definitions:

1. **Update schema files** (in `schemas/*.yml`)
2. **Update type definitions** (in `ecs_types/schema_fields.py`)
3. **No changes needed here** - attributes pass through automatically
4. **Update downstream consumers** if they need to use the new attribute

Example: Adding a `sensitivity` attribute
```yaml
# In schema
- name: password
  type: keyword
  sensitivity: high  # NEW attribute

# Automatically appears in both formats:
# ecs_flat.yml
user.password:
  name: password
  type: keyword
  sensitivity: high  # Passed through

# ecs_nested.yml
user:
  fields:
    user.password:
      sensitivity: high  # Passed through
```

### Filtering Additional Attributes

To remove an attribute from intermediate files:

```python
def remove_internal_attributes(field_details: Field) -> None:
    """Remove internal-only attributes."""
    field_details.pop('node_name', None)
    field_details.pop('intermediate', None)
    field_details.pop('new_internal_attr', None)  # Add this
```

### Changing Flat Format Filtering

To change which fields appear in the flat format:

```python
def generate_flat_fields(fields: Dict[str, FieldEntry]) -> Dict[str, Field]:
    """Generate flat field representation."""
    filtered: Dict[str, FieldEntry] = remove_non_root_reusables(fields)
    
    # Add additional filtering
    filtered = remove_deprecated_fields(filtered)  # NEW
    
    flattened: Dict[str, Field] = {}
    visitor.visit_fields_with_memo(filtered, accumulate_field, flattened)
    return flattened
```

### Modifying Nested Format Structure

To change fieldset-level attributes:

```python
def generate_nested_fields(fields: Dict[str, FieldEntry]) -> Dict[str, FieldNestedEntry]:
    """Generate nested fieldset representation."""
    nested: Dict[str, FieldNestedEntry] = {}
    
    for (name, details) in fields.items():
        fieldset_details = {
            **copy.deepcopy(details['field_details']),
            **copy.deepcopy(details['schema_details'])
        }
        
        # Add custom processing
        if 'beta' in fieldset_details:
            fieldset_details['stability'] = 'beta'  # NEW
        
        # ... rest of processing ...
```

## Troubleshooting

### Common Issues

#### Missing fields in flat format

**Symptom**: Field appears in schema but not in ecs_flat.yml

**Possible causes**:
1. Field is in a fieldset with `top_level: false`
   - **Check**: Look at fieldset's `reusable.top_level` setting
   - **Solution**: If field should be at root, set `top_level: true`

2. Field is marked as `intermediate: true`
   - **Check**: Look for `intermediate` attribute in schema
   - **Solution**: Remove if field should be included

3. Field is in a filtered subset
   - **Check**: Are you using `--subset` or `--exclude` flags?
   - **Solution**: Adjust filtering or run without filters

#### Fieldset missing from nested format

**Symptom**: Fieldset defined in schema but not in ecs_nested.yml

**Unlikely**: The nested format includes all fieldsets by design.

**Check**:
- Verify fieldset is properly defined in schema
- Check for schema validation errors earlier in pipeline
- Ensure schema file is in the loaded directory

#### Unexpected attributes in output

**Symptom**: Internal attributes appearing in intermediate files

**Solution**: Add to `remove_internal_attributes()`:
```python
def remove_internal_attributes(field_details: Field) -> None:
    field_details.pop('node_name', None)
    field_details.pop('intermediate', None)
    field_details.pop('unwanted_attr', None)  # Add this
```

#### File size concerns

**Symptom**: Intermediate YAML files are very large

**Context**: This is normal - ecs_flat.yml with ~850 fields is ~150KB

**Optimization options**:
1. Use YAML references for common values (complex)
2. Compress files for distribution (gzip)
3. Consider JSON format (more compact)

### Debugging Tips

#### View raw processed schemas

Enable debugging output:
```python
# In generator.py or your script
nested, flat = generate(fields, out_dir, default_dirs=True)
# This creates ecs.yml with raw processed schemas
```

#### Compare before/after

```bash
# Generate with current code
python scripts/generator.py --semconv-version v1.24.0 --out /tmp/test1

# Make changes

# Generate again
python scripts/generator.py --semconv-version v1.24.0 --out /tmp/test2

# Compare
diff /tmp/test1/ecs/ecs_flat.yml /tmp/test2/ecs/ecs_flat.yml
```

#### Field counts

```python
import yaml

with open('generated/ecs/ecs_flat.yml') as f:
    flat = yaml.safe_load(f)
    print(f"Total fields: {len(flat)}")
    
with open('generated/ecs/ecs_nested.yml') as f:
    nested = yaml.safe_load(f)
    total_fields = sum(len(fs['fields']) for fs in nested.values())
    print(f"Total fields (from nested): {total_fields}")
    print(f"Total fieldsets: {len(nested)}")
```

#### Field type distribution

```python
from collections import Counter

with open('generated/ecs/ecs_flat.yml') as f:
    flat = yaml.safe_load(f)
    types = Counter(f['type'] for f in flat.values())
    for field_type, count in types.most_common():
        print(f"{field_type}: {count}")
```

## Performance Considerations

### Memory Usage

The visitor pattern used for field traversal is memory-efficient:
- Processes fields one at a time
- Deep copies only when needed
- Accumulates results incrementally

For very large schemas (1000+ fields):
- Memory usage: ~50-100MB during generation
- Most memory used by YAML serialization

### Execution Time

Typical generation times:
- Small schema (10 fieldsets): <100ms
- Standard ECS (~45 fieldsets): ~500ms
- Large schema (100+ fieldsets): ~2-3s

Bottlenecks:
1. Deep copying field definitions
2. Visitor traversal
3. YAML serialization (yaml.dump)

### Optimization Strategies

If generation becomes too slow:

1. **Profile to find bottlenecks**:
   ```python
   import cProfile
   cProfile.run('generate(fields, out_dir, default_dirs)')
   ```

2. **Optimize deep copies**:
   - Only copy fields that will be modified
   - Use shallow copies where possible

3. **Parallel processing** (advanced):
   - Process fieldsets in parallel for nested format
   - Requires careful handling of shared state

## Related Files

- `scripts/generator.py` - Main entry point, calls this generator
- `scripts/schema/loader.py` - Loads raw schemas
- `scripts/schema/cleaner.py` - Validates and normalizes
- `scripts/schema/finalizer.py` - Applies transformations
- `scripts/schema/visitor.py` - Field traversal utilities
- `scripts/generators/csv_generator.py` - Consumes flat format
- `scripts/generators/es_template.py` - Consumes nested format
- `scripts/generators/markdown_fields.py` - Consumes nested format
- `scripts/generators/beats.py` - Consumes nested format
- `schemas/*.yml` - Source schema definitions
- `generated/ecs/ecs_flat.yml` - Flat output
- `generated/ecs/ecs_nested.yml` - Nested output

## Testing

Currently no automated tests exist for the intermediate file generator.

### Manual Testing

```bash
# Generate with current code
make clean
make SEMCONV_VERSION=v1.24.0

# Verify output files exist
ls -lh generated/ecs/ecs_flat.yml
ls -lh generated/ecs/ecs_nested.yml

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('generated/ecs/ecs_flat.yml'))"

# Check field counts
python -c "import yaml; print(len(yaml.safe_load(open('generated/ecs/ecs_flat.yml'))))"
```

### Future Test Coverage

Recommended tests to add:

1. **Unit tests** for helper functions:
   - `remove_internal_attributes()`
   - `remove_non_root_reusables()`
   - `accumulate_field()`

2. **Integration tests** for generation:
   - Generate from minimal schema
   - Verify field counts
   - Check attribute presence/absence

3. **Regression tests**:
   - Compare output against known-good baseline
   - Detect unexpected changes

## References

- [ECS Schema Structure](../../USAGE.md)
- [Visitor Pattern Documentation](../schema/visitor.py)
- [ECS Type Definitions](../ecs_types/schema_fields.py)
- [CSV Generator](csv-generator.md) *(coming soon)*
- [Elasticsearch Template Generator](es-template.md) *(coming soon)*

