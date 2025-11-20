# Markdown Documentation Generator

## Overview

The Markdown Generator (`generators/markdown_fields.py`) transforms ECS field schemas into human-readable documentation published on the Elastic documentation site. It's the final step in the documentation pipeline, converting structured YAML field definitions into comprehensive markdown pages.

### Purpose

This generator creates the official ECS reference documentation, including:

1. **Field Reference Pages** - Complete catalog of all fields
2. **Fieldset Pages** - Detailed documentation for each fieldset (e.g., HTTP, User, Process)
3. **OTel Alignment Documentation** - Showing convergence with OpenTelemetry
4. **Index and Navigation** - Entry points and cross-references

The output is human-friendly markdown that integrates with Elastic's documentation infrastructure.

## Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     generator.py (main)                          │
│                                                                  │
│  1. Load schemas                                                 │
│  2. Clean and finalize                                          │
│  3. Generate intermediate files                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│           markdown_fields.generate() - Entry Point               │
│                                                                  │
│  Input: Nested fieldsets + OTel generator + version info        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Page Generation Functions                       │
│                                                                  │
│  ├─ page_index()                    → index.md                  │
│  ├─ page_field_reference()          → ecs-field-reference.md    │
│  ├─ page_otel_alignment_overview()  → ecs-otel-alignment-*.md   │
│  ├─ page_otel_alignment_details()   → ecs-otel-alignment-*.md   │
│  └─ page_fieldset() [for each]      → ecs-{name}.md             │
│                                                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Jinja2 Template Rendering                           │
│                                                                  │
│  Templates (scripts/templates/):                                │
│  - index.j2                                                     │
│  - fieldset.j2                                                  │
│  - ecs_field_reference.j2                                       │
│  - otel_alignment_overview.j2                                   │
│  - otel_alignment_details.j2                                    │
│  - field_values.j2                                              │
│  - macros.j2 (shared template macros)                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Markdown Files Output                         │
│                                                                  │
│  Written to: docs/reference/                                    │
│  - index.md                                                     │
│  - ecs-field-reference.md                                       │
│  - ecs-otel-alignment-overview.md                               │
│  - ecs-otel-alignment-details.md                                │
│  - ecs-http.md, ecs-user.md, ecs-process.md, ...              │
│    (one per fieldset)                                           │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

#### 1. Generate Function

**Entry Point**: `generate(nested, docs_only_nested, ecs_version, semconv_version, otel_generator, out_dir)`

Orchestrates the entire markdown generation process:
- Creates output directory
- Generates each page type
- Saves rendered markdown to files

**Called by**: `generator.py` main script after all schema processing is complete

#### 2. Helper Functions

These prepare data for template consumption:

| Function | Purpose |
|----------|---------|
| `render_fieldset_reuse_text()` | Extract expected nesting locations |
| `render_nestings_reuse_section()` | Build reuse section data |
| `extract_allowed_values_key_names()` | Get allowed value names |
| `sort_fields()` | Sort and enrich field lists |
| `check_for_usage_doc()` | Check for usage doc existence |

#### 3. Page Generation Functions

Each decorated with `@templated()` for automatic rendering:

| Function | Template | Output File | Purpose |
|----------|----------|-------------|---------|
| `page_index()` | index.j2 | index.md | Main landing page |
| `page_field_reference()` | ecs_field_reference.j2 | ecs-field-reference.md | All fields catalog |
| `page_fieldset()` | fieldset.j2 | ecs-{name}.md | Individual fieldset docs |
| `page_otel_alignment_overview()` | otel_alignment_overview.j2 | ecs-otel-alignment-overview.md | Alignment statistics |
| `page_otel_alignment_details()` | otel_alignment_details.j2 | ecs-otel-alignment-details.md | Field mappings |
| `page_field_values()` | field_values.j2 | (not saved directly) | Event categorization fields |

#### 4. Template System

**Framework**: Jinja2

**Configuration**:
```python
template_env = jinja2.Environment(
    loader=FileSystemLoader('scripts/templates/'),
    keep_trailing_newline=True,  # Preserve trailing newlines
    trim_blocks=True,            # Remove first newline after block
    lstrip_blocks=False          # Don't strip leading whitespace
)
```

**Template Location**: `scripts/templates/`

**Shared Macros**: `macros.j2` contains reusable template components

## Template Development

### Adding a New Page Type

To add a new documentation page:

1. **Create the template** in `scripts/templates/`:
   ```jinja2
   {# my_new_page.j2 #}
   # {{ title }}
   
   Version: {{ version }}
   
   {% for item in items %}
   ## {{ item.name }}
   {{ item.description }}
   {% endfor %}
   ```

2. **Create page function** in `markdown_fields.py`:
   ```python
   @templated('my_new_page.j2')
   def page_my_new_page(items, version):
       """Generate my new documentation page.
       
       Args:
           items: List of items to document
           version: Version string
       
       Returns:
           Rendered markdown content
       """
       return dict(
           title="My New Page",
           items=items,
           version=version
       )
   ```

3. **Call in generate()** function:
   ```python
   def generate(nested, docs_only_nested, ecs_version, semconv_version, otel_generator, out_dir):
       # ... existing code ...
       
       save_markdown(
           path.join(out_dir, 'my-new-page.md'),
           page_my_new_page(some_items, ecs_version)
       )
   ```

### Template Best Practices

1. **Use macros for repeated patterns**:
   ```jinja2
   {# In macros.j2 #}
   {% macro field_row(field) -%}
   | {{ field.name }} | {{ field.type }} | {{ field.description }} |
   {%- endmacro %}
   
   {# In your template #}
   {% from 'macros.j2' import field_row %}
   {% for field in fields %}
   {{ field_row(field) }}
   {% endfor %}
   ```

2. **Handle missing data gracefully**:
   ```jinja2
   {% if field.example %}
   Example: `{{ field.example }}`
   {% endif %}
   ```

3. **Keep formatting consistent**:
   - Use consistent heading levels
   - Follow markdown best practices
   - Include blank lines between sections

4. **Comment complex logic**:
   ```jinja2
   {# Sort fields by type, then name #}
   {% for field in fields|sort(attribute='type,name') %}
   ...
   {% endfor %}
   ```

## Data Structures

### Nested Fieldsets Structure

```python
{
    'http': {
        'name': 'http',
        'title': 'HTTP',
        'group': 2,
        'description': 'HTTP request and response fields',
        'fields': {
            'http.request.method': {
                'name': 'method',
                'flat_name': 'http.request.method',
                'type': 'keyword',
                'description': 'HTTP request method',
                'example': 'GET',
                'level': 'extended',
                'otel': [{'relation': 'match', 'stability': 'stable'}],
                'allowed_values': [...]  # Optional
            },
            # ... more fields ...
        },
        'reusable': {  # If fieldset is reusable
            'expected': [
                {'full': 'client.http', 'short': 'client.http'},
                {'full': 'server.http', 'short': 'server.http'}
            ]
        },
        'reused_here': [  # Fieldsets nested here
            {
                'full': 'client.geo',
                'schema_name': 'geo',
                'short': 'geo',
                'beta': '',
                'normalize': []
            }
        ]
    },
    # ... more fieldsets ...
}
```

### OTel Mapping Summary Structure

```python
{
    'namespace': 'http',
    'title': 'HTTP',
    'nr_all_ecs_fields': 25,
    'nr_plain_ecs_fields': 20,
    'nr_otel_fields': 18,
    'nr_matching_fields': 10,
    'nr_equivalent_fields': 5,
    'nr_related_fields': 3,
    'nr_conflicting_fields': 1,
    'nr_metric_fields': 0,
    'nr_otlp_fields': 0,
    'nr_not_applicable_fields': 1
}
```

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
from generators import markdown_fields
from generators.otel import OTelGenerator

# Prepare data
nested = {...}  # From intermediate_files.generate()
docs_only = {...}
otel_gen = OTelGenerator('v1.24.0')

# Generate all markdown docs
markdown_fields.generate(
    nested=nested,
    docs_only_nested=docs_only,
    ecs_generated_version='8.11.0',
    semconv_version='v1.24.0',
    otel_generator=otel_gen,
    out_dir='docs/reference'
)
```

### Testing Template Changes

To test template modifications without full regeneration:

```python
from generators.markdown_fields import render_template

# Test a template with sample data
context = {
    'fieldset': {'name': 'http', 'title': 'HTTP'},
    'sorted_fields': [...]
}

output = render_template('fieldset.j2', **context)
print(output)
```

## Making Changes

### Modifying Existing Pages

To change an existing page's content:

1. **Locate the template**: Find the `.j2` file in `scripts/templates/`
2. **Edit the template**: Modify Jinja2 markup
3. **Update page function** (if needed): Adjust context data in `markdown_fields.py`
4. **Test**: Regenerate documentation and review output
5. **Validate**: Check markdown renders correctly

Example - Adding a field to fieldset pages:

```python
# In markdown_fields.py
@templated('fieldset.j2')
def page_fieldset(fieldset, nested, ecs_generated_version):
    # ... existing code ...
    return dict(
        fieldset=fieldset,
        sorted_fields=sorted_fields,
        # Add new data
        field_count=len(sorted_fields),  # NEW
        # ... rest of context ...
    )
```

```jinja2
{# In fieldset.j2 #}
# {{ fieldset.title }}

This fieldset contains {{ field_count }} fields.  {# NEW #}

{# ... rest of template ... #}
```

### Changing Field Display Order

To modify how fields are sorted:

```python
def sort_fields(fieldset):
    """Sort fields by custom criteria."""
    fields_list = list(fieldset['fields'].values())
    for field in fields_list:
        field['allowed_value_names'] = extract_allowed_values_key_names(field)
    
    # Change sorting key
    return sorted(fields_list, key=lambda f: (f.get('level'), f['name']))
    # Now sorts by level first, then name
```

### Adding Conditional Sections

To show content only for certain fieldsets:

```jinja2
{% if fieldset.name == 'event' %}
## Special Event Categorization

The event fieldset includes special categorization fields...
{% endif %}
```

## Troubleshooting

### Common Issues

#### "Template not found: xyz.j2"

**Cause**: Template file doesn't exist or path is wrong

**Solution**: 
- Verify template exists in `scripts/templates/`
- Check template name spelling
- Ensure `TEMPLATE_DIR` path is correct

#### Markdown not rendering correctly

**Cause**: Jinja2 whitespace control or markdown syntax issues

**Solutions**:
- Check for extra/missing blank lines
- Use `{%-` and `-%}` for whitespace control
- Validate markdown with a linter
- Review `trim_blocks` and `lstrip_blocks` settings

Example whitespace issue:
```jinja2
{# BAD - Creates unwanted blank lines #}
{% for field in fields %}
{{ field.name }}
{% endfor %}

{# GOOD - Cleaner output #}
{% for field in fields -%}
{{ field.name }}
{% endfor %}
```

#### Context variable not available in template

**Cause**: Variable not passed in context dictionary

**Solution**: Update the page function's return dict:
```python
@templated('my_template.j2')
def page_something(...):
    return dict(
        existing_var=value,
        new_var=new_value  # Add missing variable
    )
```

#### Jinja2 syntax errors

**Cause**: Invalid template syntax

**Common mistakes**:
- Unclosed blocks: `{% if x %}` without `{% endif %}`
- Wrong syntax: `{{ if x }}` instead of `{% if x %}`
- Missing filters: `{{ var|missing_filter }}`

**Debugging**:
```python
try:
    output = render_template('my_template.j2', **context)
except jinja2.TemplateError as e:
    print(f"Template error: {e}")
    print(f"Line: {e.lineno}")
```

### Performance Considerations

For large schemas (100+ fieldsets):

1. **Avoid redundant processing**:
   ```python
   # BAD - Sorts multiple times
   for fieldset in fieldsets:
       sorted_fields = sorted(fieldset['fields'].values(), ...)
   
   # GOOD - Sort once, reuse
   for fieldset in fieldsets:
       if not hasattr(fieldset, '_sorted_fields'):
           fieldset['_sorted_fields'] = sorted(fieldset['fields'].values(), ...)
       sorted_fields = fieldset['_sorted_fields']
   ```

2. **Use generators for large datasets**:
   ```python
   # Instead of building large lists
   results = [generate_page(fs) for fs in fieldsets]
   
   # Use generator
   results = (generate_page(fs) for fs in fieldsets)
   ''.join(results)  # Consume as needed
   ```

## Related Files

- `scripts/generator.py` - Main entry point, calls this generator
- `scripts/generators/intermediate_files.py` - Produces nested structures
- `scripts/generators/otel.py` - Provides OTel summaries
- `scripts/generators/ecs_helpers.py` - Utility functions
- `scripts/templates/*.j2` - Jinja2 templates
- `docs/fields/usage/*.md` - Usage documentation (manually written)
- `docs/reference/*.md` - Generated markdown output

## Testing

Currently there are no automated tests for the markdown generator. Manual testing is required:

1. **Generate docs**: Run full generation process
2. **Visual inspection**: Review generated markdown files
3. **Build docs site**: Verify rendering in documentation site
4. **Link checking**: Ensure cross-references work
5. **Diff comparison**: Compare with previous version

**Future improvement**: Add unit tests for:
- Helper functions (sort_fields, render_fieldset_reuse_text, etc.)
- Template rendering with known inputs
- Edge cases (empty fieldsets, missing data)

## References

- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Markdown Guide](https://www.markdownguide.org/)
- [ECS Documentation](https://www.elastic.co/guide/en/ecs/current/index.html)
- [Elastic Doc Build Tools](https://github.com/elastic/docs)

