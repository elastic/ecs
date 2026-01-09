# ECS Helper Utilities

## Overview

The ECS Helpers module (`generators/ecs_helpers.py`) provides a comprehensive collection of utility functions used across all ECS generator scripts. These helpers abstract common patterns and provide reusable building blocks for working with schemas, files, and data structures.

### Purpose

This module serves as the shared utility layer for the entire ECS build system, providing:

1. **Dictionary Operations** - Copying, sorting, merging, ordering
2. **File Operations** - YAML I/O, file discovery, directory management
3. **Git Operations** - Repository introspection, version loading
4. **List Operations** - Filtering, extraction, transformation
5. **Field Utilities** - Type checking, filtering by reusability
6. **Warning System** - Consistent warning generation

By centralizing these utilities, the module ensures consistency across generators and reduces code duplication.

## Function Categories

### Dictionary Helpers

#### dict_copy_keys_ordered()
```python
def dict_copy_keys_ordered(dct: Field, copied_keys: List[str]) -> Field
```

**Purpose**: Copy specific keys in a defined order

**Use Case**: Ensuring consistent field ordering in output files

**Example**:
```python
field = {
    'description': 'HTTP request method',
    'name': 'method',
    'type': 'keyword',
    'level': 'extended'
}

# Copy in specific order
ordered = dict_copy_keys_ordered(field, ['name', 'type', 'level', 'description'])
# OrderedDict([('name', 'method'), ('type', 'keyword'), ...])
```

#### dict_copy_existing_keys()
```python
def dict_copy_existing_keys(source: Field, destination: Field, keys: List[str]) -> None
```

**Purpose**: Selectively copy keys that exist in source

**Use Case**: Building Elasticsearch mappings with type-specific parameters

**Example**:
```python
source = {'type': 'keyword', 'ignore_above': 1024, 'index': True}
dest = {'type': 'keyword'}

dict_copy_existing_keys(source, dest, ['ignore_above', 'normalizer'])
# dest now: {'type': 'keyword', 'ignore_above': 1024}
# 'normalizer' not copied (not in source)
```

#### dict_sorted_by_keys()
```python
def dict_sorted_by_keys(dct: FieldNestedEntry, sort_keys: List[str]) -> List[FieldNestedEntry]
```

**Purpose**: Sort dictionary values by multiple criteria

**Use Case**: Sorting fieldsets for consistent documentation ordering

**Example**:
```python
fieldsets = {
    'http': {'name': 'http', 'group': 2, 'title': 'HTTP'},
    'base': {'name': 'base', 'group': 1, 'title': 'Base'},
    'agent': {'name': 'agent', 'group': 1, 'title': 'Agent'}
}

sorted_fs = dict_sorted_by_keys(fieldsets, ['group', 'name'])
# Returns: [agent, base, http]  (group 1, 1, 2; names alphabetical within group)
```

#### ordered_dict_insert()
```python
def ordered_dict_insert(
    dct: Field,
    new_key: str,
    new_value: Union[str, bool],
    before_key: Optional[str] = None,
    after_key: Optional[str] = None
) -> None
```

**Purpose**: Insert key-value pair at specific position

**Use Case**: Adding fields in specific locations for readability

**Example**:
```python
from collections import OrderedDict

d = OrderedDict([('name', 'field'), ('type', 'keyword')])
ordered_dict_insert(d, 'level', 'extended', after_key='type')
# d now: [('name', 'field'), ('type', 'keyword'), ('level', 'extended')]
```

#### safe_merge_dicts()
```python
def safe_merge_dicts(a: Dict[Any, Any], b: Dict[Any, Any]) -> Dict[Any, Any]
```

**Purpose**: Merge dictionaries with duplicate key detection

**Use Case**: Combining schema definitions safely

**Example**:
```python
base_fields = {'@timestamp': {...}, 'message': {...}}
custom_fields = {'user_id': {...}}

merged = safe_merge_dicts(base_fields, custom_fields)
# Success: All keys unique

duplicate_fields = {'message': {...}}  # Duplicate key!
merged = safe_merge_dicts(base_fields, duplicate_fields)
# Raises ValueError: Duplicate key found when merging dictionaries: message
```

#### fields_subset()
```python
def fields_subset(subset, fields)
```

**Purpose**: Extract subset of fields based on specification

**Use Case**: Generating partial schemas for specific use cases

**Example**:
```python
subset_spec = {
    'http': {'fields': '*'},  # All HTTP fields
    'user': {                 # Only specific user fields
        'fields': {
            'name': {},
            'email': {}
        }
    }
}

filtered = fields_subset(subset_spec, all_fields)
# Returns only http.* and user.name, user.email
```

### File Helpers

#### is_yaml()
```python
def is_yaml(path: str) -> bool
```

**Purpose**: Check if file has YAML extension

**Example**:
```python
is_yaml('schemas/http.yml')    # True
is_yaml('output.json')         # False
is_yaml('file.test.yaml')      # True
```

#### glob_yaml_files()
```python
def glob_yaml_files(paths: List[str]) -> List[str]
```

**Purpose**: Find all YAML files from paths/wildcards/directories

**Example**:
```python
# Direct files
glob_yaml_files(['schemas/http.yml', 'schemas/user.yml'])
# ['schemas/http.yml', 'schemas/user.yml']

# Directory
glob_yaml_files(['schemas/'])
# ['schemas/agent.yml', 'schemas/base.yml', ...]

# Wildcard
glob_yaml_files(['schemas/*.yml'])
# All YAML files in schemas/

# Comma-separated string
glob_yaml_files('schemas/http.yml,schemas/user.yml')
# ['schemas/http.yml', 'schemas/user.yml']
```

#### make_dirs()
```python
def make_dirs(path: str) -> None
```

**Purpose**: Create directory and parents safely

**Example**:
```python
make_dirs('generated/elasticsearch/composable/component')
# Creates all parent directories if they don't exist
# No error if already exists
```

#### yaml_dump() / yaml_load()
```python
def yaml_dump(filename: str, data: Dict, preamble: Optional[str] = None) -> None
def yaml_load(filename: str) -> Set[str]
```

**Purpose**: Save/load YAML files with consistent formatting

**Example**:
```python
# Save with header
yaml_dump(
    'output.yml',
    {'name': 'http', 'fields': [...]},
    preamble='# Auto-generated - do not edit\n'
)

# Load
data = yaml_load('schemas/http.yml')
print(data['name'])  # 'http'
```

#### ecs_files() / usage_doc_files()
```python
def ecs_files() -> List[str]
def usage_doc_files() -> List[str]
```

**Purpose**: Get lists of schema or usage doc files

**Example**:
```python
schemas = ecs_files()
# ['schemas/agent.yml', 'schemas/base.yml', ...]

usage_docs = usage_doc_files()
# ['ecs-http-usage.md', 'ecs-user-usage.md', ...]
```

### Git Helpers

#### get_tree_by_ref()
```python
def get_tree_by_ref(ref: str) -> git.objects.tree.Tree
```

**Purpose**: Access repository contents at specific git reference

**Use Case**: Loading schemas from specific version/branch/tag

**Example**:
```python
# Load from tag
tree = get_tree_by_ref('v8.10.0')
http_schema = tree['schemas']['http.yml'].data_stream.read()

# Load from branch
tree = get_tree_by_ref('main')

# Load from commit
tree = get_tree_by_ref('abc123def')
```

#### path_exists_in_git_tree()
```python
def path_exists_in_git_tree(tree: git.objects.tree.Tree, file_path: str) -> bool
```

**Purpose**: Check if path exists in git tree

**Example**:
```python
tree = get_tree_by_ref('main')

if path_exists_in_git_tree(tree, 'schemas/http.yml'):
    # Load the file
    content = tree['schemas']['http.yml'].data_stream.read()
```

### List Helpers

#### list_subtract()
```python
def list_subtract(original: List[Any], subtracted: List[Any]) -> List[Any]
```

**Purpose**: Remove elements from list

**Example**:
```python
all_fields = ['name', 'type', 'description', 'example', 'internal']
public_fields = list_subtract(all_fields, ['internal'])
# ['name', 'type', 'description', 'example']
```

#### list_extract_keys()
```python
def list_extract_keys(lst: List[Field], key_name: str) -> List[str]
```

**Purpose**: Extract specific key from list of dicts

**Example**:
```python
fields = [
    {'name': 'method', 'type': 'keyword'},
    {'name': 'status', 'type': 'long'}
]

names = list_extract_keys(fields, 'name')
# ['method', 'status']

types = list_extract_keys(fields, 'type')
# ['keyword', 'long']
```

### Field Helpers

#### is_intermediate()
```python
def is_intermediate(field: FieldEntry) -> bool
```

**Purpose**: Check if field is structural (not a data field)

**Example**:
```python
# http.request is just structure
request_field = {
    'field_details': {'intermediate': True, 'name': 'request'}
}
is_intermediate(request_field)  # True

# http.request.method is actual field
method_field = {
    'field_details': {'name': 'method', 'type': 'keyword'}
}
is_intermediate(method_field)  # False
```

#### remove_top_level_reusable_false()
```python
def remove_top_level_reusable_false(ecs_nested: Dict[str, FieldNestedEntry]) -> Dict[str, FieldNestedEntry]
```

**Purpose**: Filter out non-root fieldsets

**Example**:
```python
nested = {
    'http': {'reusable': {'top_level': True}},
    'geo': {'reusable': {'top_level': False}},  # Only for nesting
    'user': {}  # No reusable = included by default
}

filtered = remove_top_level_reusable_false(nested)
# Contains: http, user
# Excludes: geo (can only be used as client.geo, source.geo, etc.)
```

### Warning Helper

#### strict_warning()
```python
def strict_warning(msg: str) -> None
```

**Purpose**: Issue warning that becomes error in strict mode

**Example**:
```python
if 'description' not in field:
    strict_warning(f"Field '{field['name']}' is missing description")
    # Normal mode: Warning
    # Strict mode (--strict flag): Exception
```

## Common Patterns

### Sorting Fieldsets for Output

```python
from generators import ecs_helpers

# Sort by group, then name
fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])

# Generate output in consistent order
for fieldset in fieldsets:
    generate_documentation(fieldset)
```

### Loading Schemas from Git

```python
from generators import ecs_helpers

# Load from specific version
tree = ecs_helpers.get_tree_by_ref('v8.10.0')

# Check if file exists before loading
if ecs_helpers.path_exists_in_git_tree(tree, 'schemas/http.yml'):
    content = tree['schemas']['http.yml'].data_stream.read().decode('utf-8')
    schema = yaml.safe_load(content)
```

### Building Type-Specific Mappings

```python
from generators import ecs_helpers

def build_mapping(field):
    mapping = {'type': field['type']}

    if field['type'] == 'keyword':
        ecs_helpers.dict_copy_existing_keys(
            field, mapping,
            ['ignore_above', 'normalizer']
        )
    elif field['type'] == 'text':
        ecs_helpers.dict_copy_existing_keys(
            field, mapping,
            ['norms', 'analyzer']
        )

    return mapping
```

### Safe Directory Creation

```python
from generators import ecs_helpers
from os.path import join

def save_output(content, out_dir):
    # Ensure directory exists
    full_dir = join(out_dir, 'elasticsearch', 'composable', 'component')
    ecs_helpers.make_dirs(full_dir)

    # Now safe to write files
    with open(join(full_dir, 'template.json'), 'w') as f:
        f.write(content)
```

### Filtering with Subsets

```python
from generators import ecs_helpers

# Define what to include
subset = {
    'http': {'fields': '*'},                    # All HTTP fields
    'user': {'fields': {                        # Selected user fields
        'name': {},
        'email': {},
        'roles': {'fields': '*'}                # Nested subset
    }},
    'event': {'fields': {                       # Core event fields
        'kind': {},
        'category': {},
        'type': {}
    }}
}

# Apply subset filter
filtered_fields = ecs_helpers.fields_subset(subset, all_fields)
```

## Design Principles

- **Single Responsibility**: Each function does one thing well
- **No Side Effects**: Most functions don't modify inputs (except those explicitly documented to do so like `dict_copy_existing_keys`)
- **Type Safety**: All functions have type hints
- **Composability**: Functions chain together for complex operations

## Troubleshooting

### Common Issues

#### OrderedDict not maintaining order

**Symptom**: Keys appear in wrong order after processing

**Solution**: Ensure using `OrderedDict` explicitly:
```python
from collections import OrderedDict

# Correct
d = OrderedDict([('name', 'x'), ('type', 'keyword')])

# Won't preserve order in Python < 3.7
d = {'name': 'x', 'type': 'keyword'}
```

#### Duplicate key errors in safe_merge_dicts

**Symptom**: ValueError when merging schemas

**Solution**: Check for unintended duplicates:
```python
# Find duplicates before merging
common_keys = set(a.keys()) & set(b.keys())
if common_keys:
    print(f"Duplicate keys: {common_keys}")
    # Decide: use a's values, b's values, or merge differently
```

#### glob_yaml_files returns empty list

**Symptom**: No files found when expected

**Debug**:
```python
import glob
import os

path = 'schemas/*.yml'
print(f"Looking for: {path}")
print(f"Current dir: {os.getcwd()}")
print(f"Files found: {glob.glob(path)}")

# Check if path is correct relative to current directory
```

#### YAML unicode errors

**Symptom**: UnicodeDecodeError when loading YAML

**Solution**: Ensure UTF-8 encoding:
```python
# In yaml_load:
with open(filename, encoding='utf-8') as f:
    return yaml.safe_load(f.read())
```

## Related Files

- `scripts/generator.py` - Main script using these helpers
- `scripts/generators/*.py` - All generators use these utilities
- `scripts/schema/*.py` - Schema processors use these utilities
- `scripts/ecs_types/schema_fields.py` - Type definitions used by helpers

## References

- [Python OrderedDict Documentation](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [GitPython Documentation](https://gitpython.readthedocs.io/)
- [Python glob Module](https://docs.python.org/3/library/glob.html)

