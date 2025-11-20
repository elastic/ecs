# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""CSV Field Reference Generator.

This module generates a CSV (Comma-Separated Values) export of all ECS fields,
providing a simple, spreadsheet-compatible format for field reference and analysis.

The CSV format is useful for:
- **Quick field lookup** - Search and filter in spreadsheet applications
- **Data analysis** - Import into analytics tools for field statistics
- **Integration** - Easy parsing for custom tooling
- **Documentation** - Lightweight reference for presentations/reports
- **Diff analysis** - Compare field changes between versions

CSV Structure:
    Each row represents one field with columns:
    - ECS_Version: Version of ECS (e.g., '8.11.0')
    - Indexed: Whether field is indexed in Elasticsearch (true/false)
    - Field_Set: Fieldset name (e.g., 'http', 'user', 'base')
    - Field: Full dotted field name (e.g., 'http.request.method')
    - Type: Field data type (e.g., 'keyword', 'long', 'ip')
    - Level: Field level (core/extended/custom)
    - Normalization: Normalization rules (array/to_lower/etc.)
    - Example: Example value for the field
    - Description: Short field description

Multi-fields:
    Fields with multi-fields (alternate representations) get additional rows,
    one per multi-field variant (e.g., 'message.text' for 'message' field).

Output:
    generated/csv/fields.csv - Single CSV file with all fields

Use Cases:
    - Load into Excel/Google Sheets for analysis
    - Import into database for field registry
    - Parse for custom validation tools
    - Compare versions with diff tools
    - Generate reports on field usage

See also: scripts/docs/csv-generator.md for detailed documentation
"""

import _csv
import csv
import sys
from typing import (
    Dict,
    List,
)

from os.path import join
from generator import ecs_helpers
from ecs_types import (
    Field,
)


def generate(ecs_flat: Dict[str, Field], version: str, out_dir: str) -> None:
    """Generate CSV field reference from flat ECS field definitions.
    
    Main entry point for CSV generation. Creates a single CSV file containing
    all ECS fields with their metadata, sorted with base fields first.
    
    Args:
        ecs_flat: Flat field dictionary from intermediate_files.generate()
        version: ECS version string (e.g., '8.11.0')
        out_dir: Output directory (typically 'generated')
    
    Generates:
        generated/csv/fields.csv - Complete field reference
    
    Process:
        1. Create output directory (generated/csv/)
        2. Sort fields with base fields first, then alphabetically
        3. Write CSV with header and field rows
    
    Example:
        >>> from generators.intermediate_files import generate as gen_intermediate
        >>> nested, flat = gen_intermediate(fields, 'generated/ecs', True)
        >>> generate(flat, '8.11.0', 'generated')
        # Creates generated/csv/fields.csv
    """
    ecs_helpers.make_dirs(join(out_dir, 'csv'))
    sorted_fields = base_first(ecs_flat)
    save_csv(join(out_dir, 'csv/fields.csv'), sorted_fields, version)


def base_first(ecs_flat: Dict[str, Field]) -> List[Field]:
    """Sort fields with base fields first, then remaining fields alphabetically.
    
    Base fields are top-level fields without dots in their names (e.g., '@timestamp',
    'message', 'tags'). These are placed first, followed by all other fields in
    alphabetical order by field name.
    
    Args:
        ecs_flat: Flat field dictionary mapping field names to definitions
    
    Returns:
        List of field definitions in desired sort order
    
    Sorting logic:
        1. Base fields (no dots): @timestamp, ecs, labels, message, tags
        2. All other fields alphabetically: agent.*, as.*, client.*, ...
    
    Example:
        >>> fields = {
        ...     'http.request.method': {...},
        ...     'message': {...},
        ...     'agent.name': {...},
        ...     '@timestamp': {...}
        ... }
        >>> sorted_fields = base_first(fields)
        >>> [f['flat_name'] for f in sorted_fields]
        ['@timestamp', 'message', 'agent.name', 'http.request.method']
    
    Note:
        Base fields appear at the top of the CSV for easy reference.
    """
    base_list: List[Field] = []
    sorted_list: List[Field] = []
    for field_name in sorted(ecs_flat):
        if '.' in field_name:
            sorted_list.append(ecs_flat[field_name])
        else:
            base_list.append(ecs_flat[field_name])
    return base_list + sorted_list


def save_csv(file: str, sorted_fields: List[Field], version: str) -> None:
    """Write field definitions to CSV file.
    
    Creates a CSV file with one row per field (plus header row), including
    all field metadata. Multi-fields (alternate representations) get their
    own rows.
    
    Args:
        file: Output file path
        sorted_fields: List of field definitions in desired order
        version: ECS version string
    
    CSV Format:
        Columns: ECS_Version, Indexed, Field_Set, Field, Type, Level,
                 Normalization, Example, Description
        
        Example row:
        8.11.0,true,http,http.request.method,keyword,extended,array,GET,"HTTP method"
    
    Field Set Logic:
        - Base fields (no dots): field_set = 'base'
        - Other fields: field_set = first part before dot (e.g., 'http.x' -> 'http')
    
    Multi-fields:
        If field has multi_fields, each gets its own row with:
        - Same version, indexed, field_set, level, example, description
        - Different field name and type (e.g., 'message.text', type='match_only_text')
        - Empty normalization
    
    Indexed Column:
        - 'true' if field is indexed (default)
        - 'false' if field has index=false
        - Lowercase for consistency
    
    Normalization Column:
        - Comma-separated list of normalizations (e.g., 'array, to_lower')
        - Empty if no normalizations
    
    Note:
        - Uses QUOTE_MINIMAL to only quote fields containing special characters
        - Unix line endings (\n) for consistency
        - Python 2/3 compatible file opening
    
    Example output:
        ECS_Version,Indexed,Field_Set,Field,Type,Level,Normalization,Example,Description
        8.11.0,true,base,@timestamp,date,core,,2016-05-23T08:05:34.853Z,Date/time
        8.11.0,true,http,http.request.method,keyword,extended,array,GET,HTTP method
        8.11.0,true,http,http.request.method.text,match_only_text,extended,,,HTTP method
    """
    open_mode: str = "wb"
    if sys.version_info >= (3, 0):
        open_mode: str = "w"

    with open(file, open_mode) as csvfile:
        schema_writer: _csv._writer = csv.writer(csvfile,
                                                 delimiter=',',
                                                 quoting=csv.QUOTE_MINIMAL,
                                                 lineterminator='\n')

        schema_writer.writerow(["ECS_Version", "Indexed", "Field_Set", "Field",
                                "Type", "Level", "Normalization", "Example", "Description"])
        for field in sorted_fields:
            key_parts: List[str] = field['flat_name'].split('.')
            if len(key_parts) == 1:
                field_set: str = 'base'
            else:
                field_set: str = key_parts[0]

            indexed: str = str(field.get('index', True)).lower()
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
            ])

            if 'multi_fields' in field:
                for mf in field['multi_fields']:
                    schema_writer.writerow([
                        version,
                        indexed,
                        field_set,
                        mf['flat_name'],
                        mf['type'],
                        field['level'],
                        '',
                        field.get('example', ''),
                        field['short'],
                    ])
