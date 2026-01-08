# ECS Schema Processing Pipeline

## Overview

The ECS schema processing pipeline transforms YAML schema definitions into various output formats (Elasticsearch templates, Beats configs, markdown docs, etc.). It's a multi-stage pipeline where each stage has a specific responsibility.

**Pipeline Stages:**
```
┌─────────────┐
│ YAML Schema │  Raw schema files in schemas/*.yml
│   Files     │
└──────┬──────┘
       │
       v
┌─────────────┐
│   loader.py │  Load & nest: YAML → deeply nested dict
└──────┬──────┘
       │
       v
┌─────────────┐
│  cleaner.py │  Validate, normalize, apply defaults
└──────┬──────┘
       │
       v
┌─────────────┐
│finalizer.py │  Perform field reuse, calculate names
└──────┬──────┘
       │
       v          (Optional filters)
┌─────────────┐  ┌────────────────┐
│subset_filter│─>│exclude_filter  │
│    .py      │  │      .py       │
└──────┬──────┘  └────────┬───────┘
       │                  │
       v                  v
┌─────────────────────────────┐
│   intermediate_files.py     │  Generate flat & nested YAML
└──────────────┬──────────────┘
               │
               v
     ┌────────────────────┐
     │    Generators      │
     ├────────────────────┤
     │ • es_template.py   │  Elasticsearch templates
     │ • beats.py         │  Beats field definitions
     │ • csv_generator.py │  CSV field export
     │ • markdown_fields  │  Markdown documentation
     └────────────────────┘
```

## Quick Reference

### Field Reuse Cheat Sheet

| Concept | What | When to Use | Example |
|---------|------|-------------|---------|
| **Foreign Reuse** | Copy fieldset to different location | Same fields needed elsewhere | `user` → `destination.user` |
| **Transitive** | Reuse carries nested reuses | Automatic composition | If `group` in `user`, `destination.user` gets `group` too |
| **Self-Nesting** | Copy fieldset into itself | Parent/child relationships | `process` → `process.parent` |
| **Non-Transitive** | Self-nesting stays local | Avoid unwanted propagation | `process.parent` NOT at `source.process.parent` |
| **order: 1** | High priority reuse | Has dependencies | `group` reused before `user` |
| **order: 2** | Default priority | Most fieldsets | Standard reuse timing |

**Quick Syntax:**
```yaml
# Foreign reuse (goes to other fieldsets)
fieldset:
  reusable:
    expected:
      - destination  # Simple: reuse as same name
      - at: process  # Complex: reuse with different name
        as: parent

# Self-nesting (stays in same fieldset)  
process:
  reusable:
    expected:
      - at: process  # ← Same name as fieldset = self-nesting
        as: parent
```

### Subset Definition Cheat Sheet

| Syntax | Meaning | Result |
|--------|---------|--------|
| `fields: '*'` | Include all fields | Every field in fieldset |
| `fields: { field: {} }` | Include specific field | Just that one field |
| `fields: { parent: { fields: '*' }}` | Include all nested | All fields under parent |
| `index: false` | Don't index field | Field exists but not searchable |
| `docs_only: true` | Documentation only | In docs, not in artifacts |

**Quick Syntax:**
```yaml
name: my_subset
fields:
  base:
    fields: '*'                    # All base fields
  
  http:
    fields:
      request:
        fields:
          method: {}               # Just this field
      response:
        fields: '*'                # All response fields
  
  destination:
    fields:
      user:                        # Reused fieldset
        fields:
          name: {}                 # Specific user fields
```

### Common Patterns

#### Pattern 1: Network Endpoint Fields (Foreign Reuse)

**Problem:** Need same fields for source, destination, client, server

**Solution:** Create reusable fieldset, reuse at all locations
```yaml
# In geo schema
geo:
  reusable:
    top_level: false  # Only via reuse
    expected:
      - client
      - destination  
      - host
      - observer
      - server
      - source
  fields:
    - name: city_name
    - name: country_name
    - name: location  # latitude/longitude
```

**Result:** `source.geo.city_name`, `destination.geo.city_name`, etc.

#### Pattern 2: Parent-Child Hierarchy (Self-Nesting)

**Problem:** Need to represent parent process, effective user, session leader

**Solution:** Self-nesting
```yaml
process:
  reusable:
    expected:
      - at: process
        as: parent
      - at: process
        as: session_leader
  fields:
    - name: pid
    - name: name
```

**Result:** `process.pid`, `process.parent.pid`, `process.session_leader.pid`

#### Pattern 3: Minimal Web Subset

**Problem:** Only need basic HTTP fields for web logs

**Solution:**
```yaml
name: web_minimal
fields:
  base: { fields: '*' }
  http:
    fields:
      request: { fields: { method: {}, bytes: {} }}
      response: { fields: { status_code: {}, bytes: {} }}
  url: { fields: { domain: {}, path: {} }}
```

**Result:** ~10-15 fields instead of 850

#### Pattern 4: Security Monitoring Subset

**Problem:** Need security-relevant fields only

**Solution:**
```yaml
name: security
fields:
  base: { fields: '*' }
  event: { fields: { action: {}, category: {}, type: {}, outcome: {} }}
  source: { fields: { ip: {}, port: {}, user: { fields: { name: {} }}}}
  destination: { fields: { ip: {}, port: {} }}
  process: 
    fields:
      name: {}
      pid: {}
      parent: { fields: { name: {}, pid: {} }}
  file:
    fields:
      path: {}
      hash: { fields: { sha256: {} }}
```

**Result:** Security-focused field set

---

## Core Concepts

### Deeply Nested Structure

All pipeline stages work with a deeply nested dictionary structure:

```python
{
    'fieldset_name': {
        'schema_details': {    # Fieldset-level metadata
            'root': bool,
            'group': int,
            'reusable': {...},
            'title': str
        },
        'field_details': {     # Properties of the fieldset itself
            'name': str,
            'description': str,
            'type': 'group'
        },
        'fields': {            # Nested fields
            'field_name': {
                'field_details': {...},
                'fields': {...}  # Recursive
            }
        }
    }
}
```

### Intermediate Fields

Auto-created parent fields for nesting structure:
- Created automatically for dotted names: `request.method` → creates `request` intermediate
- Marked with `intermediate: true`
- Type: `object`
- Skipped by some validation/processing steps

### Field Reuse

**Why Field Reuse Exists:**

Without reuse, we'd need to duplicate the same fields everywhere:
```yaml
# Without reuse - lots of duplication! ❌
source:
  - name: ip
  - name: port
  - name: address
destination:
  - name: ip      # Duplicated!
  - name: port    # Duplicated!
  - name: address # Duplicated!
client:
  - name: ip      # Duplicated again!
  - name: port    # Duplicated again!
  # ... and so on
```

With reuse, we define fields once and reuse them:
```yaml
# With reuse - define once, reuse everywhere! ✅
user:
  reusable:
    top_level: false  # Not at root
    expected:
      - destination   # Reuse at destination.user
      - source        # Reuse at source.user
      - client        # Reuse at client.user
  fields:
    - name: name
    - name: email
    - name: id
```

**Two Types of Reuse:**

#### 1. Foreign Reuse (Transitive) - Copy Across Fieldsets

**What it does:** Copies a fieldset into a completely different fieldset

**Example:** `user` fields appear at `destination.user.*`, `source.user.*`

**Why "transitive":** If A is reused in B, and B is reused in C, then C automatically gets A too.

**Visual Example:**
```
Before Reuse:
┌──────────┐       ┌─────────────┐
│   user   │       │ destination │
├──────────┤       ├─────────────┤
│ • name   │       │ • ip        │
│ • email  │       │ • port      │
│ • id     │       └─────────────┘
└──────────┘

After Reuse (user → destination.user):
┌─────────────────────────────┐
│       destination           │
├─────────────────────────────┤
│ • ip                        │
│ • port                      │
│ • user ← (reused!)          │
│   ├─ name                   │
│   ├─ email                  │
│   └─ id                     │
└─────────────────────────────┘

Result: destination.user.name, destination.user.email, destination.user.id
```

**Transitivity in Action:**
```
Step 1: group → user.group
┌──────────┐       ┌──────────────────┐
│  group   │  ───> │      user        │
│ • id     │       │ • name           │
│ • name   │       │ • email          │
└──────────┘       │ • group (copied) │
                   │   ├─ id          │
                   │   └─ name        │
                   └──────────────────┘

Step 2: user (with group!) → destination.user
┌──────────────────┐       ┌────────────────────────────────┐
│      user        │  ───> │        destination             │
│ • name           │       │ • ip                           │
│ • email          │       │ • port                         │
│ • group          │       │ • user (copied with group!)    │
│   ├─ id          │       │   ├─ name                      │
│   └─ name        │       │   ├─ email                     │
└──────────────────┘       │   └─ group ← (transitive!)     │
                           │       ├─ id                    │
                           │       └─ name                  │
                           └────────────────────────────────┘

Result: destination.user.group.id exists because transitivity!
```

#### 2. Self-Nesting (Non-Transitive) - Copy Within Same Fieldset

**What it does:** Copies a fieldset into itself with a different name

**Example:** `process` fields appear at `process.parent.*`

**Why "non-transitive":** This nesting is local only. When the fieldset is reused elsewhere, the self-nesting doesn't come along.

**Visual Example:**
```
Before Self-Nesting:
┌──────────┐
│ process  │
├──────────┤
│ • pid    │
│ • name   │
│ • args   │
└──────────┘

After Self-Nesting (process → process.parent):
┌───────────────────────────┐
│         process           │
├───────────────────────────┤
│ • pid                     │
│ • name                    │
│ • args                    │
│ • parent ← (self-nested!) │
│   ├─ pid                  │
│   ├─ name                 │
│   └─ args                 │
└───────────────────────────┘

Result: process.pid, process.name, process.parent.pid, process.parent.name
```

**Non-Transitivity in Action:**
```
Scenario: process has self-nesting, then process is reused at source

Step 1: process → process.parent (self-nesting)
┌───────────────────────┐
│      process          │
│ • pid                 │
│ • name                │
│ • parent (self-nest)  │
│   ├─ pid              │
│   └─ name             │
└───────────────────────┘

Step 2: process → source.process (foreign reuse)
┌─────────────────────────┐
│        source           │
│ • ip                    │
│ • port                  │
│ • process               │
│   ├─ pid                │
│   └─ name               │
│   └─ parent?  ← NO! ❌  │
└─────────────────────────┘

Result: source.process.parent does NOT exist!
Why? Self-nesting is NOT transitive - it stays local to original fieldset.
```

**When to Use Each Type:**

| Use Case | Type | Example |
|----------|------|---------|
| Same fields needed in multiple places | Foreign Reuse | user at destination, source, client |
| Capture hierarchical relationship | Self-Nesting | process.parent, process.session_leader |
| Build complex nested structures | Foreign Reuse | geo at client.geo, server.geo |
| Represent parent/child relationships | Self-Nesting | user.target, user.effective |

**Reuse Order:**

Some fieldsets depend on others being reused first:
```yaml
group:
  reusable:
    order: 1  # ← Reused FIRST (high priority)
    expected:
      - user  # group goes into user

user:
  reusable:
    order: 2  # ← Reused SECOND (default priority)
    expected:
      - destination  # user (now with group) goes into destination
```

**Processing Order:**
1. Order 1 fieldsets → Foreign reuse → Self-nesting
2. Order 2 fieldsets → Foreign reuse → Self-nesting

**Result:** `destination.user.group.*` exists because group was reused into user before user was reused into destination.

## Pipeline Stages

### 1. loader.py - Schema Loading

**Purpose:** Load YAML schema files and create initial nested structure

**Input:**
- YAML schema files (`schemas/*.yml`)
- Optional: git ref for specific version
- Optional: custom/experimental schemas

**Processing:**
1. Load schemas from filesystem or git
2. Nest dotted field names into hierarchical structure
3. Merge multiple sources (ECS + experimental + custom)
4. Create intermediate fields for parents

**Output:** Deeply nested field dictionary with minimal defaults

**Key Functions:**
- `load_schemas()`: Main entry point
- `deep_nesting_representation()`: Convert flat to nested
- `nest_fields()`: Build nested hierarchy
- `merge_fields()`: Merge multiple sources

**Example:**
```python
from schema import loader
fields = loader.load_schemas()
# Or from specific version:
fields = loader.load_schemas(ref='v8.10.0')
```

### 2. cleaner.py - Validation & Normalization

**Purpose:** Validate schemas and apply sensible defaults

**Input:** Nested fields from loader

**Processing:**
1. Validate mandatory attributes present
2. Strip whitespace from all strings
3. Apply type-specific defaults (e.g., `ignore_above=1024` for keywords)
4. Expand shorthand notations (reuse locations)
5. Validate constraints (description length, examples, patterns)

**Output:** Validated and enriched fields

**Defaults Applied:**
- `group: 2` (fieldset priority)
- `root: false` (not a root fieldset)
- `ignore_above: 1024` (for keyword fields)
- `norms: false` (for text fields)
- `short: description` (if not specified)

**Validation:**
- Mandatory attributes: name, title, description, type, level
- Short descriptions < 120 characters (strict mode)
- Valid regex patterns
- Example values match patterns/expected_values
- Field levels: core/extended/custom

**Key Functions:**
- `clean()`: Main entry point
- `schema_cleanup()`: Process fieldsets
- `field_cleanup()`: Process fields
- `normalize_reuse_notation()`: Expand reuse shorthand

**Example:**
```python
from schema import loader, cleaner
fields = loader.load_schemas()
cleaner.clean(fields, strict=False)  # Warnings
cleaner.clean(fields, strict=True)   # Exceptions
```

### 3. finalizer.py - Field Reuse & Name Calculation

**Purpose:** Perform field reuse and calculate final field names

**Input:** Cleaned fields

**Processing:**

**Phase 1: Field Reuse**
1. Organize reuses by order and type (foreign vs self)
2. For each order level:
   a. Foreign reuses: Copy fieldset to different location (transitive)
   b. Self-nestings: Copy fieldset into itself (non-transitive)
3. Mark reused fields with `original_fieldset`
4. Record reuse metadata in `reused_here`

**Phase 2: Name Calculation**
1. Traverse all fields with path tracking
2. Calculate `flat_name`: full dotted name
3. Calculate `dashed_name`: kebab-case version
4. Calculate multi-field `flat_names`
5. Apply OTel reuse mappings

**Output:** Complete field structure with all reuses and final names

**Reuse Example:**
```
Order 1:
- group → user.group (foreign reuse)

Order 2:
- user (now with group) → destination.user (foreign reuse)
  Result: destination.user.group exists! (transitive)
- process → process.parent (self-nesting)
  Result: source.process.parent does NOT exist (non-transitive)
```

**Key Functions:**
- `finalize()`: Main entry point
- `perform_reuse()`: Execute reuse operations
- `calculate_final_values()`: Compute final names
- `field_finalizer()`: Calculate individual field names

**Example:**
```python
from schema import loader, cleaner, finalizer
fields = loader.load_schemas()
cleaner.clean(fields)
finalizer.finalize(fields)
# Fields now have flat_name, dashed_name calculated
```

### 4. subset_filter.py - Subset Filtering (Optional)

**Purpose:** Filter to include only specified fields

Subset filtering is like a **whitelist** - you specify exactly which fields to include, and everything else is excluded.

**Why Use Subsets:**

- **Reduce field count:** Full ECS has ~850 fields. Subsets let you use only 50-100 fields for specific use cases
- **Performance:** Fewer fields = smaller mappings = better Elasticsearch performance
- **Simplicity:** Only the fields you actually need
- **Domain-specific:** Create subsets for web, security, infrastructure, etc.

**Input:** Finalized fields (after reuse)

**Processing:**
1. Load subset definition files
2. Extract matching fields recursively
3. Handle `docs_only` fields separately
4. Merge multiple subsets (union)

**Output:** 
- Filtered fields (main subset)
- Docs-only fields (separate)

---

## Understanding Subset Definitions

A subset definition is a YAML file that mirrors the field structure, but only includes what you want:

### Basic Subset Structure

```yaml
name: minimal                # Subset name (used for output directory)
fields:                      # Top-level: list fieldsets to include
  base:                      # Fieldset name
    fields: '*'              # '*' = include ALL fields in this fieldset
  
  http:                      # Another fieldset
    fields:                  # Specify which fields to include
      request:               # Nested field
        fields:              # Go deeper
          method: {}         # Include this field
          bytes: {}          # Include this field
      response:
        fields: '*'          # Include ALL response fields
```

### Visual Representation

**Before Subset (Full ECS):**
```
base
├─ @timestamp
├─ message
├─ tags
└─ labels

http
├─ request
│   ├─ method
│   ├─ bytes
│   ├─ referrer
│   └─ body
└─ response
    ├─ status_code
    ├─ bytes
    └─ body

user
├─ name
├─ email
└─ id
```

**Subset Definition:**
```yaml
name: minimal
fields:
  base:
    fields: '*'              # All base fields
  http:
    fields:
      request:
        fields:
          method: {}         # Just method
          bytes: {}          # Just bytes
```

**After Subset:**
```
base                    ✓ (all fields kept)
├─ @timestamp
├─ message
├─ tags
└─ labels

http                    ✓ (partially kept)
├─ request
│   ├─ method          ✓ (explicitly included)
│   ├─ bytes           ✓ (explicitly included)
│   ├─ referrer        ✗ (not in subset)
│   └─ body            ✗ (not in subset)
└─ response            ✗ (entire section excluded)

user                    ✗ (not in subset at all)
```

---

## Field Options in Subsets

Beyond just including fields, you can set options:

### Disable Indexing

```yaml
http:
  fields:
    request:
      fields:
        body:
          index: false    # Don't index this field
          enabled: false  # Don't process at all
```

**Result:** `http.request.body` exists but isn't indexed (saves space, still in _source)

### docs_only Fields

```yaml
http:
  fields:
    request:
      fields:
        referrer:
          docs_only: true  # In documentation but not artifacts
```

**Result:** Field appears in markdown docs but NOT in Elasticsearch templates, Beats configs, etc.

**Use Case:** Deprecated fields you still want documented for legacy data

---

## Multiple Subsets (Union)

You can specify multiple subset files - they're merged together:

```bash
python generator.py \
  --subset subsets/base.yml subsets/web.yml \
  --semconv-version v1.24.0
```

**Merging Logic:**
- Field in ANY subset → Included in result
- `enabled: false` in subset A, `enabled: true` in subset B → Result: `enabled: true`
- Union operation: More permissive wins

**Example:**

`subsets/base.yml`:
```yaml
fields:
  base:
    fields: '*'
  http:
    fields:
      request:
        fields:
          method: {}
```

`subsets/security.yml`:
```yaml
fields:
  http:
    fields:
      request:
        fields:
          bytes: {}    # Different field
  source:
    fields:
      ip: {}
```

**Merged Result:**
```
base.*                    (from base.yml)
http.request.method       (from base.yml)
http.request.bytes        (from security.yml)
source.ip                 (from security.yml)
```

---

## Common Subset Pitfalls

### ❌ Mistake 1: Forgetting Intermediate Fields

**Wrong:**
```yaml
http:
  fields:
    method: {}  # ❌ Wrong! method is under request
```

**Right:**
```yaml
http:
  fields:
    request:     # ✓ Need intermediate field
      fields:
        method: {}
```

### ❌ Mistake 2: Including Fieldset Without Fields Key

**Wrong:**
```yaml
base: {}  # ❌ Missing fields key
```

**Right:**
```yaml
base:
  fields: '*'  # ✓ Must have fields
```

### ❌ Mistake 3: Using Wildcards at Wrong Level

**Wrong:**
```yaml
fields: '*'  # ❌ Can't wildcard top level
```

**Right:**
```yaml
fields:
  base:
    fields: '*'  # ✓ Wildcard inside fieldset
  http:
    fields: '*'
```

---

## Subset Best Practices

1. **Start with base:** Almost always include `base: {fields: '*'}`
2. **Be specific:** Only include fields you actually use
3. **Test thoroughly:** Generate and verify the output
4. **Document why:** Add comments explaining the subset purpose
5. **Version control:** Keep subset definitions in git
6. **Iterate:** Start small, add fields as needed

---

**Key Functions:**
- `filter()`: Main entry point
- `extract_matching_fields()`: Recursive filtering
- `combine_all_subsets()`: Merge multiple subsets

**Example:**
```python
from schema import subset_filter
fields, docs = subset_filter.filter(
    fields,
    ['subsets/minimal.yml'],
    'generated'
)
```

### 5. exclude_filter.py - Exclude Filtering (Optional)

**Purpose:** Explicitly remove specified fields

**Input:** Fields (optionally after subset filter)

**Processing:**
1. Load exclude definition files
2. Remove specified fields
3. Auto-remove empty parents (except base)

**Output:** Fields with exclusions removed

**Exclude Definition:**
```yaml
- name: http
  fields:
    - name: request.referrer  # Remove this field
    - name: response.body
```

**Key Functions:**
- `exclude()`: Main entry point
- `exclude_fields()`: Remove matching fields
- `pop_field()`: Recursive removal

**Example:**
```python
from schema import exclude_filter
fields = exclude_filter.exclude(
    fields,
    ['excludes/deprecated.yml']
)
```

### 6. intermediate_files.py - Generate Intermediate Formats

**Purpose:** Generate standardized intermediate YAML representations

**Input:** Final processed fields

**Processing:**
1. Generate flat format: `{flat_name: field_def}`
2. Generate nested format: `{fieldset: {fields: {...}}}`
3. Remove internal attributes (node_name, intermediate)
4. Filter non-root reusables (flat format only)

**Output:**
- `ecs_flat.yml`: Flat dictionary
- `ecs_nested.yml`: Nested by fieldset
- `ecs.yml`: Raw debug format (optional)

**Key Functions:**
- `generate()`: Main entry point
- `generate_flat_fields()`: Create flat representation
- `generate_nested_fields()`: Create nested representation

**Example:**
```python
from generators import intermediate_files
nested, flat = intermediate_files.generate(
    fields,
    'generated/ecs',
    default_dirs=True
)
```

## Helper Modules

### visitor.py - Field Traversal

**Purpose:** Traverse deeply nested structures using visitor pattern

**Functions:**
- `visit_fields()`: Call different functions for fieldsets vs fields
- `visit_fields_with_path()`: Pass path array to callback
- `visit_fields_with_memo()`: Pass accumulator object

**Example:**
```python
from schema import visitor

# Count all fields
count = {'total': 0}
def counter(details, memo):
    memo['total'] += 1
visitor.visit_fields_with_memo(fields, counter, count)
```

## Common Patterns

### Running the Full Pipeline

```python
from schema import loader, cleaner, finalizer
from generators import intermediate_files

# Load schemas
fields = loader.load_schemas()

# Clean and validate
cleaner.clean(fields, strict=False)

# Perform reuse and calculate names
finalizer.finalize(fields)

# Generate intermediate files
nested, flat = intermediate_files.generate(
    fields,
    'generated/ecs',
    default_dirs=True
)

# Now ready for generators (es_template, beats, etc.)
```

### With Subset Filtering

```python
from schema import subset_filter

# ... run pipeline through finalizer ...

# Apply subset filter
fields, docs = subset_filter.filter(
    fields,
    ['subsets/minimal.yml'],
    'generated'
)

# Continue with generators
```

### With Exclude Filtering

```python
from schema import exclude_filter

# ... run pipeline through finalizer ...

# Apply exclude filter
fields = exclude_filter.exclude(
    fields,
    ['excludes/deprecated.yml']
)

# Continue with generators
```

## Debugging Tips

### View Intermediate Structure

```python
import yaml

# After loader
with open('debug_loaded.yml', 'w') as f:
    yaml.dump(fields, f, default_flow_style=False)

# After cleaner
with open('debug_cleaned.yml', 'w') as f:
    yaml.dump(fields, f, default_flow_style=False)

# After finalizer
with open('debug_finalized.yml', 'w') as f:
    yaml.dump(fields, f, default_flow_style=False)
```

### Check Specific Field

```python
# Find a specific field
def find_field(details):
    if 'flat_name' in details['field_details']:
        if details['field_details']['flat_name'] == 'http.request.method':
            print(details['field_details'])

from schema import visitor
visitor.visit_fields(fields, field_func=find_field)
```

### Validate Reuse

```python
# Check what was reused where
for name, schema in fields.items():
    if 'reused_here' in schema['schema_details']:
        print(f"{name} contains:")
        for reuse in schema['schema_details']['reused_here']:
            print(f"  - {reuse['full']}")
```

## Extending the Pipeline

### Adding New Validation

Add to `cleaner.py`:

```python
def my_custom_validation(field):
    if 'my_custom_attr' in field['field_details']:
        # Validate it
        pass

# In field_cleanup():
def field_cleanup(field):
    # ... existing code ...
    my_custom_validation(field)
```

### Adding New Calculated Fields

Add to `finalizer.py`:

```python
def field_finalizer(details, path):
    # ... existing calculations ...
    
    # Add new calculated field
    details['field_details']['my_calculated'] = calculate_something(path)
```

### Adding New Filter Type

Create new module like `custom_filter.py`:

```python
def filter(fields, config):
    # Your custom filtering logic
    return filtered_fields
```

## Testing

### Unit Tests

Located in `scripts/tests/unit/`:
- `test_loader.py`: Schema loading
- `test_cleaner.py`: Validation
- `test_finalizer.py`: Reuse logic

### Integration Tests

Run full pipeline:
```bash
cd scripts
python3 generator.py --strict
```

## Related Documentation

- [otel-integration.md](otel-integration.md) - OTel integration
- [markdown-generator.md](markdown-generator.md) - Markdown docs
- [intermediate-files.md](intermediate-files.md) - Intermediate formats
- [es-template.md](es-template.md) - Elasticsearch templates
- [ecs-helpers.md](ecs-helpers.md) - Utility functions
- [csv-generator.md](csv-generator.md) - CSV export
- [beats-generator.md](beats-generator.md) - Beats configs

## Troubleshooting

### Common Errors

**ValueError: Missing mandatory attribute**
- Fix: Add required attribute to schema YAML
- Required: name, title, description, type, level

**ValueError: Schema has root=true and cannot be reused**
- Fix: Don't try to reuse base or other root fieldsets
- Root fieldsets appear at document root, can't be nested

**KeyError during reuse**
- Fix: Check reuse order; dependencies must be reused first
- Use `order: 1` for fieldsets that others depend on

**Duplicate field names**
- Fix: Check for conflicting custom schemas
- Use `safe_merge_dicts` which raises on conflicts

---

### Field Reuse Troubleshooting

#### Problem: Field not appearing where expected

**Symptom:** Expected `destination.user.group.id` but it doesn't exist

**Cause:** Reuse order is wrong - `group` not reused into `user` before `user` reused into `destination`

**Solution:**
```yaml
# Ensure correct order
group:
  reusable:
    order: 1  # ← FIRST
    expected:
      - user

user:
  reusable:
    order: 2  # ← SECOND
    expected:
      - destination
```

**How to verify:**
```python
# Check what's in destination.user
from schema import visitor

def show_fields(details):
    if 'flat_name' in details['field_details']:
        name = details['field_details']['flat_name']
        if name.startswith('destination.user'):
            print(name)

visitor.visit_fields(fields, field_func=show_fields)
```

#### Problem: Self-nesting appearing in reused locations

**Symptom:** Expected `source.process.parent` NOT to exist, but it does

**Cause:** Something went wrong with non-transitive logic, or it's actually foreign reuse

**Solution:**
1. Check if `process.parent` is foreign reuse (wrong) or self-nesting (correct):
```yaml
process:
  reusable:
    expected:
      - at: process     # ← Self-nesting (correct)
        as: parent
      - source          # ← Foreign reuse
```

2. If it's self-nesting, it should NOT appear at `source.process.parent`
3. If you WANT it everywhere, change to foreign reuse:
```yaml
# Create separate parent_process fieldset
parent_process:
  reusable:
    order: 1
    expected:
      - at: process
        as: parent
```

#### Problem: Reused fields have wrong OTel mappings

**Symptom:** `destination.user.name` has different OTel mapping than `user.name`

**Cause:** Need to use `otel_reuse` for location-specific mappings

**Solution:**
```yaml
# In user schema
- name: name
  otel_reuse:
    - ecs: destination.user.name     # ← Specific location
      mapping:
        relation: equivalent
        attribute: destination.user.name
    - ecs: source.user.name
      mapping:
        relation: equivalent
        attribute: source.user.name
```

#### Problem: Can't reuse fieldset

**Symptom:** `ValueError: Schema X has attribute root=true and cannot be reused`

**Cause:** Trying to reuse a root fieldset (`base`, etc.)

**Why:** Root fieldsets have fields at document root level. Can't nest them.

**Solution:** Don't reuse root fieldsets. If you need similar functionality, create a new non-root fieldset.

---

### Subset Filtering Troubleshooting

#### Problem: Subset includes too many fields

**Symptom:** Wanted 50 fields, got 200

**Cause:** Used `fields: '*'` wildcard on wrong fieldsets

**Solution:** Be more specific:
```yaml
# Too broad
http:
  fields: '*'  # ← Gets ALL http fields

# More specific
http:
  fields:
    request:
      fields:
        method: {}
        bytes: {}
```

**How to verify field count:**
```bash
# Count lines in CSV (minus header)
wc -l generated/csv/fields.csv
# Or
grep -c "^" generated/csv/fields.csv
```

#### Problem: Subset excludes fields I need

**Symptom:** Missing `http.request.method` in generated artifacts

**Cause 1:** Forgot to include it in subset definition

**Solution:**
```yaml
http:
  fields:
    request:
      fields:
        method: {}  # ← Must explicitly include
```

**Cause 2:** Forgot intermediate fields in path

**Solution:**
```yaml
# Wrong - missing 'request' intermediate
http:
  fields:
    method: {}  # ❌

# Right - include full path
http:
  fields:
    request:      # ✓
      fields:
        method: {}
```

**How to debug:**
```bash
# Check what's in flat YAML
grep "http.request.method" generated/ecs/ecs_flat.yml

# If nothing found, field wasn't included in subset
```

#### Problem: ValueError: 'fields' key expected, not found

**Symptom:** `ValueError: 'fields' key expected, not found in subset for http`

**Cause:** Schema has nested fields but subset doesn't specify them

**Solution:**
```yaml
# Wrong
http: {}  # ❌ Missing fields key

# Right
http:
  fields: '*'  # ✓ Or specific fields
```

#### Problem: ValueError: 'fields' key not expected

**Symptom:** `ValueError: 'fields' key not expected, found in subset for @timestamp`

**Cause:** Trying to add nested fields to a leaf field (one that doesn't have children)

**Solution:**
```yaml
# Wrong - @timestamp is a leaf field, can't have nested fields
base:
  fields:
    @timestamp:
      fields:  # ❌ @timestamp doesn't have nested fields
        value: {}

# Right - @timestamp is included as-is
base:
  fields:
    @timestamp: {}  # ✓ Just include it
```

#### Problem: Subset doesn't include reused fields

**Symptom:** Subset has `destination` but not `destination.user.*`

**Cause:** Subset filtering happens AFTER reuse, must include destination in subset

**Solution:**
```yaml
# Include both the parent and nested fields
destination:
  fields:
    ip: {}
    port: {}
    user:        # ← Include reused fieldset
      fields:
        name: {}
        email: {}
```

**Remember:** Subset sees the FINAL structure after reuse. If `user` is reused at `destination.user`, your subset must explicitly include `destination.user` fields.

#### Problem: Multiple subsets not merging as expected

**Symptom:** Field in subset A but not in final output

**Cause:** Typo in subset definition or field path. Check each subset independently and verify field paths match the schema structure.

---

### Strict Mode Issues

If `--strict` fails with warnings:
- Review the warning messages
- Fix schema YAMLs to meet requirements
- Or run without `--strict` (warnings only)
