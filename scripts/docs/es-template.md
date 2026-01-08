# Elasticsearch Template Generator

## Overview

The Elasticsearch Template Generator (`generators/es_template.py`) converts ECS field schemas into Elasticsearch index templates. These templates define the mapping (field types and properties) for indices that will store ECS-structured data.

### Purpose

This generator bridges the gap between ECS schema definitions and Elasticsearch's native mapping format, producing ready-to-install JSON templates that:

1. **Define field mappings** - Specify types, parameters, and multi-fields
2. **Configure index settings** - Set codec, field limits, refresh intervals
3. **Support two template formats**:
   - **Composable** (modern): Modular component templates
   - **Legacy** (deprecated): Single monolithic template

The generated templates can be directly installed into Elasticsearch using the `_index_template` or `_template` APIs.

## Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     generator.py (main)                         │
│                                                                 │
│  Load → Clean → Finalize → Generate Intermediate Files          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              es_template.generate() / generate_legacy()         │
│                                                                 │
│  Input: nested or flat fieldsets + version + settings           │
└────────────────────────────┬────────────────────────────────────┘
                             │
          ┌──────────────────┴──────────────────┐
          │                                     │
          ▼                                     ▼
┌──────────────────────────┐         ┌──────────────────────────┐
│  Composable Templates    │         │   Legacy Template        │
│                          │         │                          │
│  For each fieldset:      │         │  All fields in one:      │
│  1. Build nested props   │         │  1. Build nested props   │
│  2. Convert fields       │         │  2. Convert fields       │
│  3. Save component       │         │  3. Save single template │
│                          │         │                          │
│  Save main template      │         └──────────────────────────┘
└──────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Elasticsearch JSON Templates                   │
│                                                                 │
│  Composable:                                                    │
│  - generated/elasticsearch/composable/component/base.json       │
│  - generated/elasticsearch/composable/component/agent.json      │
│  - generated/elasticsearch/composable/component/*.json          │
│  - generated/elasticsearch/composable/template.json             │
│                                                                 │
│  Legacy:                                                        │
│  - generated/elasticsearch/legacy/template.json                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

#### 1. Composable Template Generation

**Entry Point**: `generate(ecs_nested, ecs_version, out_dir, ...)`

**Process**:
1. For each fieldset:
   - Convert flat field names to nested `properties` structure
   - Transform ECS field defs to Elasticsearch mappings
   - Save as individual component template
2. Generate main template:
   - Build component name list
   - Create template that composes all components
   - Add index patterns, priority, settings

**Output Files**:
- `component/base.json`, `component/agent.json`, etc. (one per fieldset)
- `template.json` (main composable template)

#### 2. Legacy Template Generation

**Entry Point**: `generate_legacy(ecs_flat, ecs_version, out_dir, ...)`

**Process**:
1. Iterate all fields in sorted order
2. Convert flat field names to nested properties structure
3. Build single monolithic mappings section
4. Generate template with all mappings included

**Output File**:
- `legacy/template.json`

#### 3. Field Mapping Conversion

**Function**: `entry_for(field)`

Converts ECS field definitions to Elasticsearch mapping format:

| ECS Type | ES Mapping | Special Parameters |
|----------|------------|-------------------|
| keyword | keyword | ignore_above, synthetic_source_keep |
| text | text | norms |
| long/integer/short/byte | long/integer/short/byte | - |
| float/double/half_float | float/double/half_float | - |
| scaled_float | scaled_float | scaling_factor |
| boolean | boolean | - |
| date | date | - |
| ip | ip | - |
| geo_point | geo_point | - |
| object | object | enabled (if false) |
| nested | nested | enabled (if false) |
| flattened | flattened | ignore_above |
| constant_keyword | constant_keyword | value |
| alias | alias | path |

**Multi-fields**: Handled via `multi_fields` array in ECS definition

**Custom parameters**: Merged from `parameters` dict in field definition

## Template Formats

### Composable Template (Modern)

Recommended for Elasticsearch 7.8+. Provides modularity and flexibility.

**Component Template** (one per fieldset):
```json
{
  "template": {
    "mappings": {
      "properties": {
        "http": {
          "properties": {
            "request": {
              "properties": {
                "method": {
                  "type": "keyword",
                  "ignore_above": 1024
                }
              }
            }
          }
        }
      }
    }
  },
  "_meta": {
    "ecs_version": "8.11.0",
    "documentation": "https://www.elastic.co/guide/en/ecs/current/ecs-http.html"
  }
}
```

**Main Template**:
```json
{
  "index_patterns": ["try-ecs-*"],
  "composed_of": [
    "ecs_8.11.0_base",
    "ecs_8.11.0_agent",
    "ecs_8.11.0_http",
    "..."
  ],
  "priority": 1,
  "template": {
    "settings": {
      "index": {
        "codec": "best_compression",
        "mapping": {
          "total_fields": {
            "limit": 2000
          }
        }
      }
    },
    "mappings": {
      "date_detection": false,
      "dynamic_templates": [...]
    }
  },
  "_meta": {
    "ecs_version": "8.11.0",
    "description": "Sample composable template that includes all ECS fields"
  }
}
```

**Installation**:
```bash
# Install component templates
for file in generated/elasticsearch/composable/component/*.json; do
  name=$(basename "$file" .json)
  curl -X PUT "localhost:9200/_component_template/ecs_8.11.0_$name" \
    -H 'Content-Type: application/json' -d @"$file"
done

# Install main template
curl -X PUT "localhost:9200/_index_template/ecs" \
  -H 'Content-Type: application/json' \
  -d @generated/elasticsearch/composable/template.json
```

### Legacy Template (Deprecated)

For Elasticsearch < 7.8 or backwards compatibility.

**Structure**:
```json
{
  "index_patterns": ["try-ecs-*"],
  "order": 1,
  "settings": {
    "index": {
      "mapping": {
        "total_fields": {
          "limit": 10000
        }
      },
      "refresh_interval": "5s"
    }
  },
  "mappings": {
    "_meta": {
      "version": "8.11.0"
    },
    "date_detection": false,
    "dynamic_templates": [...],
    "properties": {
      "agent": {...},
      "http": {...},
      "...": "all fields in one place"
    }
  }
}
```

**Installation**:
```bash
curl -X PUT "localhost:9200/_template/ecs" \
  -H 'Content-Type: application/json' \
  -d @generated/elasticsearch/legacy/template.json
```

## Usage Examples

### Running the Generator

Typically invoked through the main generator:

```bash
# From repository root
make clean
make SEMCONV_VERSION=v1.24.0

# Generates both composable and legacy templates
```

### Programmatic Usage

```python
from generators.es_template import generate, generate_legacy
from generators.intermediate_files import generate as gen_intermediate

# Generate intermediate files
nested, flat = gen_intermediate(fields, 'generated/ecs', True)

# Generate composable templates
generate(
    ecs_nested=nested,
    ecs_version='8.11.0',
    out_dir='generated',
    mapping_settings_file=None,  # Use defaults
    template_settings_file=None   # Use defaults
)

# Generate legacy template
generate_legacy(
    ecs_flat=flat,
    ecs_version='8.11.0',
    out_dir='generated',
    mapping_settings_file=None,
    template_settings_file=None
)
```

### Custom Settings

**Custom Mapping Settings** (`mapping_settings.json`):
```json
{
  "date_detection": true,
  "numeric_detection": false,
  "dynamic_templates": [
    {
      "strings_as_text": {
        "match_mapping_type": "string",
        "mapping": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      }
    }
  ]
}
```

**Custom Template Settings** (`template_settings.json`):
```json
{
  "index_patterns": ["logs-*", "metrics-*"],
  "priority": 100,
  "template": {
    "settings": {
      "index": {
        "number_of_shards": 1,
        "number_of_replicas": 1,
        "codec": "best_compression",
        "mapping": {
          "total_fields": {
            "limit": 5000
          }
        }
      }
    }
  }
}
```

**Usage**:
```python
generate(
    ecs_nested=nested,
    ecs_version='8.11.0',
    out_dir='generated',
    mapping_settings_file='mapping_settings.json',
    template_settings_file='template_settings.json'
)
```

## Making Changes

### Adding Support for New Field Type

To add a new Elasticsearch field type:

1. **Update entry_for() function**:
```python
def entry_for(field: Field) -> Dict:
    field_entry: Dict = {'type': field['type']}
    try:
        # ... existing type handling ...

        elif field['type'] == 'new_type':
            ecs_helpers.dict_copy_existing_keys(
                field, field_entry,
                ['param1', 'param2']  # Type-specific parameters
            )

        # ... rest of function ...
```

2. **Update schema definitions** to use new type
3. **Test** with sample field
4. **Document** in this guide

### Customizing Component Template Naming

To change the naming convention for component templates:

```python
def component_name_convention(
    ecs_version: str,
    ecs_nested: Dict[str, FieldNestedEntry]
) -> List[str]:
    version: str = ecs_version.replace('+', '-')
    names: List[str] = []
    for (fieldset_name, fieldset) in ecs_helpers.remove_top_level_reusable_false(ecs_nested).items():
        # Change naming pattern here
        names.append("my_prefix_{}_{}".format(version, fieldset_name))
    return names
```

**Note**: If you change component names, update any deployment scripts that reference them.

### Adding Custom Metadata

To add custom metadata to templates:

**For component templates**:
```python
def save_component_template(...):
    # ... existing code ...
    template['_meta']['custom_field'] = 'custom_value'
    template['_meta']['team'] = 'security'
    # ... save ...
```

**For main template**:
```python
def finalize_template(...):
    # ... existing code ...
    if not is_legacy:
        template['_meta']['custom_info'] = {...}
```

### Modifying Default Settings

To change default template settings:

```python
def default_template_settings(ecs_version: str) -> Dict:
    return {
        "index_patterns": ["your-pattern-*"],  # Change pattern
        "priority": 500,  # Higher priority
        "template": {
            "settings": {
                "index": {
                    "number_of_shards": 1,  # Add shard config
                    "codec": "default",  # Change codec
                    "mapping": {
                        "total_fields": {
                            "limit": 5000  # Increase limit
                        }
                    }
                }
            },
        }
    }
```

## Troubleshooting

### Common Issues

#### "Total fields limit exceeded"

**Symptom**: Error when installing template or indexing documents

```
illegal_argument_exception: Limit of total fields [1000] has been exceeded
```

**Cause**: Elasticsearch default limit is 1000 fields, ECS has 800+

**Solutions**:
1. Increase limit in template settings:
   ```json
   {
     "settings": {
       "index": {
         "mapping": {
           "total_fields": {
             "limit": 2000
           }
         }
       }
     }
   }
   ```

2. Use composable templates (smaller field count per component)

3. Use selective field sets (only fields you need)

#### Component template not found

**Symptom**: Error installing main composable template

```
resource_not_found_exception: component template [ecs_8.11.0_http] not found
```

**Cause**: Component templates must be installed before main template

**Solution**: Install components first, then main template:
```bash
# Install all components
for file in generated/elasticsearch/composable/component/*.json; do
  # ... install component
done

# Then install main template
curl -X PUT "localhost:9200/_index_template/ecs" ...
```

#### Mapping conflicts

**Symptom**: Cannot update mapping with different type

```
illegal_argument_exception: mapper [field] cannot be changed from type [keyword] to [text]
```

**Cause**: Trying to change existing field type

**Solutions**:
1. Delete and recreate index:
   ```bash
   curl -X DELETE "localhost:9200/my-index"
   # Recreate with new mapping
   ```

2. Reindex to new index with updated mapping:
   ```bash
   curl -X POST "localhost:9200/_reindex" -d '{
     "source": {"index": "old-index"},
     "dest": {"index": "new-index"}
   }'
   ```

3. Use index aliases to transparently switch

#### JSON formatting issues

**Symptom**: Template JSON won't load

**Check**:
- Valid JSON syntax (no trailing commas)
- Proper escaping of special characters
- Matching brackets and braces

**Debug**:
```python
import json
with open('template.json') as f:
    try:
        template = json.load(f)
        print("Valid JSON")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
```

### Debugging Tips

- **Validate JSON**: `jq . generated/elasticsearch/composable/template.json`
- **Compare versions**: `diff -u old/template.json new/template.json`
- **Test installation**: Use a local Elasticsearch instance with `docker run -p 9200:9200 docker.elastic.co/elasticsearch/elasticsearch:8.11.0`

## Related Files

- `scripts/generator.py` - Main entry point
- `scripts/generators/intermediate_files.py` - Produces nested/flat structures
- `scripts/generators/ecs_helpers.py` - Utility functions
- `scripts/ecs_types/schema_fields.py` - Type definitions
- `schemas/*.yml` - Source ECS schemas
- `generated/elasticsearch/composable/` - Composable template output
- `generated/elasticsearch/legacy/` - Legacy template output

## References

- [Elasticsearch Composable Templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html)
- [Elasticsearch Mapping Types](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html)
- [ECS Field Reference](https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html)
- [Index Template Best Practices](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-templates.html#avoid-index-pattern-collisions)

