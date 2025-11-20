# CSV Field Reference Generator

## Overview

The CSV Generator (`generators/csv_generator.py`) produces a spreadsheet-compatible field reference for all ECS fields. It exports field definitions to a simple CSV (Comma-Separated Values) format that can be easily imported into spreadsheet applications, databases, or custom analysis tools.

### Purpose

This generator creates a human-readable, machine-parseable field catalog that's useful for:

1. **Quick Reference** - Search and filter fields in Excel/Google Sheets
2. **Data Analysis** - Analyze field usage patterns and statistics
3. **Integration** - Parse for custom tooling and automation
4. **Documentation** - Include in presentations or reports
5. **Version Comparison** - Diff CSV files to see field changes

The CSV format is intentionally simple and widely compatible, making ECS field data accessible to anyone with a spreadsheet application.

## Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     generator.py (main)                          │
│                                                                  │
│  Load → Clean → Finalize → Generate Intermediate Files          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            intermediate_files.generate()                         │
│                                                                  │
│  Returns: (nested, flat)                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼ flat dictionary
┌─────────────────────────────────────────────────────────────────┐
│              csv_generator.generate()                            │
│                                                                  │
│  1. base_first() - Sort fields (base fields first)              │
│  2. save_csv() - Write CSV with header + field rows             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Output: fields.csv                            │
│                                                                  │
│  ECS_Version,Indexed,Field_Set,Field,Type,Level,Normalization   │
│  8.11.0,true,base,@timestamp,date,core,,2016-05-23...           │
│  8.11.0,true,http,http.request.method,keyword,extended,...      │
│  ...                                                            │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

#### 1. generate()

**Entry Point**: `generate(ecs_flat, version, out_dir)`

Orchestrates CSV generation:
- Creates output directory
- Sorts fields appropriately
- Writes CSV file

#### 2. base_first()

**Purpose**: Sort fields for readable output

**Logic**:
1. Base fields (no dots): @timestamp, message, tags, etc.
2. All other fields alphabetically: agent.*, as.*, client.*, ...

**Rationale**: Base fields are foundational and referenced frequently, so they appear at the top for easy access.

#### 3. save_csv()

**Purpose**: Write field data to CSV format

**Features**:
- Header row with column names
- One row per field (plus multi-fields)
- Multi-fields get separate rows
- Consistent quoting and line endings

## CSV Structure

### Columns

| Column | Description | Example Values |
|--------|-------------|----------------|
| **ECS_Version** | Version of ECS | 8.11.0, 8.11.0+exp |
| **Indexed** | Whether field is indexed | true, false |
| **Field_Set** | Fieldset name | base, http, user, agent |
| **Field** | Full dotted field name | @timestamp, http.request.method |
| **Type** | Elasticsearch field type | keyword, long, ip, date |
| **Level** | Field level | core, extended, custom |
| **Normalization** | Normalization rules | array, to_lower, array, to_lower |
| **Example** | Example value | GET, 192.0.2.1, 2016-05-23... |
| **Description** | Short field description | HTTP request method, User email |

### Field Set Logic

- **Base fields** (no dots in name): field_set = 'base'
  - Examples: @timestamp, message, tags, labels
- **Other fields**: field_set = first part before dot
  - http.request.method → field_set = 'http'
  - user.email → field_set = 'user'

### Multi-Fields

Fields with multi-fields (alternate representations) get additional rows:

```csv
8.11.0,true,event,message,match_only_text,core,,Hello world,Log message
8.11.0,true,event,message.text,match_only_text,core,,,Log message
```

Multi-field rows:
- Share version, indexed, field_set, level, description
- Have unique field name and type
- Have empty normalization and example

## Example Output

```csv
ECS_Version,Indexed,Field_Set,Field,Type,Level,Normalization,Example,Description
8.11.0,true,base,@timestamp,date,core,,2016-05-23T08:05:34.853Z,Date/time when the event originated
8.11.0,true,base,message,match_only_text,core,,Hello World,Log message optimized for viewing
8.11.0,true,base,message.text,match_only_text,core,,,Log message optimized for viewing
8.11.0,true,base,tags,keyword,core,array,"production, eu-west-1",List of keywords for event
8.11.0,true,agent,agent.build.original,keyword,core,,,Extended build information
8.11.0,true,agent,agent.ephemeral_id,keyword,extended,,8a4f500f,Ephemeral identifier
8.11.0,true,agent,agent.id,keyword,core,,8a4f500d,Unique agent identifier
8.11.0,true,http,http.request.body.bytes,long,extended,,1437,Request body size in bytes
8.11.0,true,http,http.request.method,keyword,extended,array,GET,HTTP request method
8.11.0,true,http,http.response.status_code,long,extended,,404,HTTP response status code
```

## Usage Examples

### Running the Generator

Typically invoked through the main generator:

```bash
# From repository root
make clean
make SEMCONV_VERSION=v1.24.0

# CSV file created at:
# generated/csv/fields.csv
```

### Programmatic Usage

```python
from generators.csv_generator import generate
from generators.intermediate_files import generate as gen_intermediate

# Generate intermediate files
nested, flat = gen_intermediate(fields, 'generated/ecs', True)

# Generate CSV
generate(flat, '8.11.0', 'generated')
# Creates generated/csv/fields.csv
```

### Loading CSV in Python

```python
import csv

with open('generated/csv/fields.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['Field']}: {row['Type']} ({row['Level']})")
```

### Loading CSV in Spreadsheet

**Excel**:
1. Open Excel
2. File → Open → Select fields.csv
3. Use "Text to Columns" if needed (comma-delimited)

**Google Sheets**:
1. File → Import
2. Upload fields.csv
3. Choose "Comma" as separator

**LibreOffice Calc**:
1. Open fields.csv
2. Text Import dialog appears
3. Select "Comma" separator

### Analyzing Field Data

**Count fields by type**:
```python
import csv
from collections import Counter

with open('generated/csv/fields.csv') as f:
    reader = csv.DictReader(f)
    types = Counter(row['Type'] for row in reader)

print("Field types:")
for field_type, count in types.most_common():
    print(f"  {field_type}: {count}")
```

**Find all extended-level fields**:
```python
import csv

with open('generated/csv/fields.csv') as f:
    reader = csv.DictReader(f)
    extended = [row for row in reader if row['Level'] == 'extended']

print(f"Extended fields: {len(extended)}")
for field in extended[:5]:
    print(f"  {field['Field']}")
```

**Fields by fieldset**:
```python
import csv
from collections import defaultdict

with open('generated/csv/fields.csv') as f:
    reader = csv.DictReader(f)
    by_fieldset = defaultdict(list)
    for row in reader:
        by_fieldset[row['Field_Set']].append(row['Field'])

for fieldset in sorted(by_fieldset):
    print(f"{fieldset}: {len(by_fieldset[fieldset])} fields")
```

## Use Cases

### 1. Field Auditing

Identify fields missing examples or descriptions:

```python
import csv

with open('generated/csv/fields.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['Example']:
            print(f"Missing example: {row['Field']}")
```

### 2. Version Comparison

Compare field changes between versions:

```bash
# Generate CSV for two versions
make SEMCONV_VERSION=v1.24.0
cp generated/csv/fields.csv fields_v8.10.csv

# Update and regenerate
make clean
make SEMCONV_VERSION=v1.25.0
cp generated/csv/fields.csv fields_v8.11.csv

# Compare
diff -u fields_v8.10.csv fields_v8.11.csv > field_changes.diff
```

### 3. Custom Validation

Build custom validation tools:

```python
import csv

def validate_fields(csv_file):
    errors = []
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check for required fields
            if row['Level'] == 'core' and not row['Example']:
                errors.append(f"Core field missing example: {row['Field']}")
            
            # Check normalization consistency
            if 'array' in row['Normalization']:
                if not row['Field'].endswith('s'):
                    errors.append(f"Array field should be plural: {row['Field']}")
    
    return errors
```

### 4. Documentation Generation

Generate custom field reference:

```python
import csv

def generate_markdown(csv_file, fieldset):
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        fields = [row for row in reader if row['Field_Set'] == fieldset]
    
    print(f"# {fieldset.title()} Fields\n")
    print("| Field | Type | Level | Description |")
    print("|-------|------|-------|-------------|")
    for field in fields:
        print(f"| {field['Field']} | {field['Type']} | {field['Level']} | {field['Description']} |")

generate_markdown('generated/csv/fields.csv', 'http')
```

### 5. Database Import

Load into SQL database for querying:

```sql
-- PostgreSQL example
CREATE TABLE ecs_fields (
    ecs_version TEXT,
    indexed BOOLEAN,
    field_set TEXT,
    field TEXT,
    type TEXT,
    level TEXT,
    normalization TEXT,
    example TEXT,
    description TEXT
);

COPY ecs_fields FROM '/path/to/fields.csv' CSV HEADER;

-- Query examples
SELECT field_set, COUNT(*) as field_count
FROM ecs_fields
WHERE level = 'core'
GROUP BY field_set
ORDER BY field_count DESC;

SELECT field, type, description
FROM ecs_fields
WHERE field_set = 'http'
AND indexed = true;
```

## Making Changes

### Adding New Columns

To add a new column to the CSV:

1. **Update header row**:
```python
schema_writer.writerow([
    "ECS_Version", "Indexed", "Field_Set", "Field",
    "Type", "Level", "Normalization", "Example", "Description",
    "New_Column"  # Add here
])
```

2. **Add to data rows**:
```python
schema_writer.writerow([
    version,
    indexed,
    field_set,
    field['flat_name'],
    field['type'],
    field['level'],
    ', '.join(field['normalize']),
    field.get('example', ''),
    field['short'],
    field.get('new_property', 'default_value')  # Add here
])
```

3. **Update multi-field rows** similarly

4. **Update documentation** in this file

### Changing Field Sorting

To change sort order:

```python
def base_first(ecs_flat: Dict[str, Field]) -> List[Field]:
    # Custom sorting logic
    fields_list = list(ecs_flat.values())
    
    # Sort by level, then name
    return sorted(fields_list, key=lambda f: (f['level'], f['flat_name']))
    
    # Or by fieldset, then name
    return sorted(fields_list, key=lambda f: (f['flat_name'].split('.')[0], f['flat_name']))
```

### Changing CSV Format

To modify CSV formatting:

```python
schema_writer = csv.writer(
    csvfile,
    delimiter=';',  # Use semicolon instead
    quoting=csv.QUOTE_ALL,  # Quote all fields
    quotechar='"',
    lineterminator='\r\n'  # Windows line endings
)
```

### Filtering Fields

To exclude certain fields:

```python
def generate(ecs_flat: Dict[str, Field], version: str, out_dir: str) -> None:
    ecs_helpers.make_dirs(join(out_dir, 'csv'))
    
    # Filter out custom fields
    filtered = {k: v for k, v in ecs_flat.items() if v['level'] != 'custom'}
    
    sorted_fields = base_first(filtered)
    save_csv(join(out_dir, 'csv/fields.csv'), sorted_fields, version)
```

## Troubleshooting

### Common Issues

#### CSV not opening correctly in Excel

**Symptom**: Fields appear in wrong columns or all in one column

**Solutions**:
1. Use "Text to Columns" feature:
   - Select data → Data tab → Text to Columns
   - Choose "Delimited" → Next
   - Select "Comma" → Finish

2. Change Excel import settings:
   - File → Options → Advanced → Edit Custom Lists
   - Set default delimiter to comma

3. Save as Excel format after import:
   - File → Save As → Excel Workbook (.xlsx)

#### Unicode/special character issues

**Symptom**: Strange characters in descriptions or examples

**Solutions**:
1. Ensure UTF-8 encoding when opening:
   - In Excel: Data → Get Data → From File → From Text/CSV
   - Select UTF-8 encoding

2. Or fix in code:
```python
with open(file, 'w', encoding='utf-8') as csvfile:
    # ... write CSV
```

#### Missing multi-fields

**Symptom**: Multi-fields not appearing in CSV

**Check**:
```python
# Verify field has multi_fields
field = flat['message']
print('multi_fields' in field)
print(field.get('multi_fields'))

# Check multi-field structure
if 'multi_fields' in field:
    for mf in field['multi_fields']:
        print(f"  {mf['flat_name']}: {mf['type']}")
```

#### Empty normalization column

**Symptom**: Normalization column is always empty

**Check** field definitions have `normalize` key:
```python
field = flat['some.field']
print(field.get('normalize', []))  # Should be a list
```

### Debugging Tips

#### Verify field count

```python
import csv

with open('generated/csv/fields.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    
# Compare with flat format
from generators.intermediate_files import generate as gen_intermediate
nested, flat = gen_intermediate(fields, 'generated/ecs', True)
print(f"Flat fields: {len(flat)}")

# Count multi-fields
multi_field_count = sum(
    len(f.get('multi_fields', [])) for f in flat.values()
)
print(f"Multi-fields: {multi_field_count}")
print(f"Expected total: {len(flat) + multi_field_count}")
```

#### Check field sets

```python
import csv
from collections import Counter

with open('generated/csv/fields.csv') as f:
    reader = csv.DictReader(f)
    fieldsets = Counter(row['Field_Set'] for row in reader)
    
print("Fields per fieldset:")
for fieldset, count in sorted(fieldsets.items()):
    print(f"  {fieldset}: {count}")
```

#### Validate CSV syntax

```python
import csv

try:
    with open('generated/csv/fields.csv') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            # Check required columns
            required = ['Field', 'Type', 'Level']
            for col in required:
                if not row[col]:
                    print(f"Row {i}: Missing {col}")
    print("CSV validation passed")
except csv.Error as e:
    print(f"CSV error: {e}")
```

## Performance Considerations

### Generation Time

Typical generation times:
- Small schema (100 fields): < 100ms
- Standard ECS (850 fields): ~200ms  
- Large schema (2000 fields): ~500ms

**Bottlenecks**:
1. Field sorting (negligible for <10k fields)
2. CSV writing (I/O bound)
3. String operations (normalization join)

### File Size

Approximate CSV sizes:
- ~850 ECS fields: 150-200 KB
- With multi-fields: 200-250 KB
- Gzip compressed: 30-40 KB

### Memory Usage

- Entire file built in memory before writing
- ~1 MB RAM for standard ECS
- ~10 MB RAM for 10k fields

## Related Files

- `scripts/generator.py` - Main entry point
- `scripts/generators/intermediate_files.py` - Produces flat format
- `scripts/generators/ecs_helpers.py` - Utility functions
- `schemas/*.yml` - Source ECS schemas
- `generated/csv/fields.csv` - Output file

## Testing

Currently no automated tests for CSV generator.

### Manual Testing

```bash
# Generate CSV
make clean
make SEMCONV_VERSION=v1.24.0

# Verify file exists
ls -lh generated/csv/fields.csv

# Check line count (should be ~850 + header + multi-fields)
wc -l generated/csv/fields.csv

# Validate CSV syntax
python -c "import csv; list(csv.DictReader(open('generated/csv/fields.csv')))"

# Check for duplicates
cut -d',' -f4 generated/csv/fields.csv | sort | uniq -d
```

### Future Test Coverage

Recommended tests:

1. **Unit tests** for functions:
   - `base_first()` sorting logic
   - Field set extraction
   - Multi-field handling

2. **Integration tests**:
   - Generate from sample schema
   - Verify row count
   - Check column names
   - Validate CSV syntax

3. **Regression tests**:
   - Compare with known-good output
   - Field count consistency

## References

- [CSV Format Specification (RFC 4180)](https://tools.ietf.org/html/rfc4180)
- [Python csv Module Documentation](https://docs.python.org/3/library/csv.html)
- [ECS Field Reference](https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html)

