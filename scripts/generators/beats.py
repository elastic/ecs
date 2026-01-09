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

"""Beats Field Definition Generator.

This module generates field definitions for Elastic Beats in YAML format. Beats
(Filebeat, Metricbeat, Packetbeat, etc.) are lightweight data shippers that need
field definitions to:
- Validate collected data structure
- Configure field behavior (indexing, doc_values, etc.)
- Provide field documentation to users
- Determine which fields are included by default

The generator transforms ECS schemas into the Beats-specific YAML structure,
handling:
- Field hierarchies and grouping
- Multi-field configurations
- Default field selection (fields enabled by default)
- Contextual naming (relative to parent group)
- Type-specific parameters

Output Structure:
    The generated YAML follows Beats field definition format:
    - Top-level 'ecs' group containing all fields
    - Nested field groups for each fieldset
    - Fields with Beats-specific properties
    - default_field flags for selective field loading

Default Fields:
    Beats can't load all ~850 ECS fields by default (performance/memory concerns).
    The generator uses an allowlist (beats_default_fields_allowlist.yml) to mark
    which fields should be enabled by default. Users can enable additional fields
    as needed.

Output:
    generated/beats/fields.ecs.yml - Beats field definitions

Use Cases:
    - Integration into Beats module configurations
    - Field validation in data collection pipelines
    - Documentation generation for Beats users
    - Custom Beat development

See also: scripts/docs/beats-generator.md for detailed documentation
"""

from os.path import join
from collections import OrderedDict
from typing import (
    Dict,
    List,
    OrderedDict,
)

from generators import ecs_helpers
from ecs_types import (
    Field,
    FieldNestedEntry,
)


def generate(
    ecs_nested: Dict[str, FieldNestedEntry],
    ecs_version: str,
    out_dir: str
) -> None:
    """Generate Beats field definitions from ECS schemas.

    Main entry point for Beats field generation. Creates a Beats-compatible YAML
    file with all ECS fields, properly structured with field groups and default_field
    settings.

    Args:
        ecs_nested: Nested fieldset structure from intermediate_files.generate()
        ecs_version: ECS version string (e.g., '8.11.0')
        out_dir: Output directory (typically 'generated')

    Generates:
        generated/beats/fields.ecs.yml - Beats field definitions

    Process:
        1. Filter out non-root reusable fieldsets (top_level=false)
        2. Process 'base' fieldset first (adds fields directly to root)
        3. Process other fieldsets in sorted order:
           - If root=true: Add fields directly to root
           - Otherwise: Create field group for fieldset
        4. Load default_fields allowlist
        5. Apply default_field flags based on allowlist
        6. Write formatted YAML with warning header

    Field Structure:
        - Base fields appear at root level
        - Other fieldsets appear as groups with nested fields
        - Each field has Beats-specific properties only
        - default_field flags control which fields load by default

    Example:
        >>> generate(nested, '8.11.0', 'generated')
        # Creates generated/beats/fields.ecs.yml
    """
    # base first
    ecs_nested = ecs_helpers.remove_top_level_reusable_false(ecs_nested)
    beats_fields: List[OrderedDict] = fieldset_field_array(ecs_nested['base']['fields'], ecs_nested['base']['prefix'])

    allowed_fieldset_keys: List[str] = ['name', 'title', 'group', 'description', 'footnote', 'type']
    # other fieldsets
    for fieldset_name in sorted(ecs_nested):
        if 'base' == fieldset_name:
            continue
        fieldset: FieldNestedEntry = ecs_nested[fieldset_name]

        # Handle when `root:true`
        if fieldset.get('root', False):
            beats_fields.extend(fieldset_field_array(fieldset['fields'], fieldset['prefix']))
            continue

        beats_field = ecs_helpers.dict_copy_keys_ordered(fieldset, allowed_fieldset_keys)
        beats_field['fields'] = fieldset_field_array(fieldset['fields'], fieldset['prefix'])
        beats_fields.append(beats_field)

    # Load temporary allowlist for default_fields workaround.
    df_allowlist = ecs_helpers.yaml_load('scripts/generators/beats_default_fields_allowlist.yml')
    # Set default_field configuration.
    set_default_field(beats_fields, df_allowlist)

    beats_file: OrderedDict = OrderedDict()
    beats_file['key'] = 'ecs'
    beats_file['title'] = 'ECS'
    beats_file['description'] = 'ECS Fields.'
    beats_file['fields'] = beats_fields

    write_beats_yaml(beats_file, ecs_version, out_dir)


def set_default_field(fields, df_allowlist, df=False, path=''):
    """Recursively set default_field flags based on allowlist.

    Beats can't load all ECS fields by default due to performance/memory constraints.
    This function marks fields that should be loaded by default using an allowlist,
    and propagates the setting through field hierarchies and multi-fields.

    Args:
        fields: List of field definitions to process
        df_allowlist: Set of field paths that should be default fields
        df: Parent's default_field value (inherited by children)
        path: Current field path for building full field names

    Behavior:
        - Checks if field path is in allowlist
        - Groups are default if top-level (path equals name)
        - Children inherit parent's default_field setting
        - Recursively processes group fields and multi-fields
        - Inserts default_field key before 'fields' key for readability

    Default Field Logic:
        1. Field is in allowlist → default_field: true
        2. Top-level group → default_field: true
        3. Parent is default → children are default
        4. Otherwise → default_field: false

    Note:
        Modifies fields list in place by adding/updating default_field property.
        The allowlist is loaded from beats_default_fields_allowlist.yml.

    Example:
        >>> fields = [{'name': 'method', 'type': 'keyword'}]
        >>> allowlist = {'http.request.method'}
        >>> set_default_field(fields, allowlist, path='http.request')
        # fields[0] now has default_field: true
    """
    for fld in fields:
        fld_df = fld.get('default_field', df)
        fld_path = fld['name']
        if path != '' and not fld.get('root', False):
            fld_path = path + '.' + fld_path
        fld_type = fld.get('type', 'keyword')
        expected = fld_path in df_allowlist or (fld_path == fld['name'] and fld_type == 'group')
        if fld_df != expected:
            ecs_helpers.ordered_dict_insert(fld, 'default_field', expected, before_key='fields')
        if fld_type == 'group':
            set_default_field(fld['fields'], df_allowlist, df=expected, path=fld_path)
        elif 'multi_fields' in fld:
            set_default_field(fld['multi_fields'], df_allowlist, df=expected, path=fld_path)


def fieldset_field_array(
    source_fields: Dict[str, Field],
    fieldset_prefix: str
) -> List[OrderedDict]:
    """Convert ECS fields to Beats field array format.

    Transforms ECS field definitions into Beats-compatible field structures by:
    - Filtering to Beats-relevant properties only
    - Converting field names to contextual names (relative to parent)
    - Processing multi-fields appropriately
    - Sorting fields alphabetically

    Args:
        source_fields: Dictionary of ECS field definitions (keyed by flat_name)
        fieldset_prefix: Prefix of parent fieldset (empty string for base)

    Returns:
        Sorted list of Beats field definitions

    Field Properties Included:
        Main fields: name, level, required, type, object_type, ignore_above,
                    multi_fields, format, input/output_format, output_precision,
                    description, example, enabled, index, doc_values, path,
                    scaling_factor, pattern

        Multi-fields: name, type, norms, default_field, normalizer, ignore_above

    Contextual Naming:
        Beats uses relative field names within groups:
        - ECS: 'http.request.method'
        - Beats (in http group): 'request.method'
        - Beats (in base): '@timestamp'

    Example:
        >>> fields = {
        ...     'http.request.method': {
        ...         'name': 'method',
        ...         'flat_name': 'http.request.method',
        ...         'type': 'keyword',
        ...         'description': 'HTTP method'
        ...     }
        ... }
        >>> fieldset_field_array(fields, 'http')
        [OrderedDict([('name', 'request.method'), ('type', 'keyword'), ...])]
    """
    allowed_keys: List[str] = [
        'name',
        'level',
        'required',
        'type',
        'object_type',
        'ignore_above',
        'multi_fields',
        'format',
        'input_format',
        'output_format',
        'output_precision',
        'description',
        'example',
        'enabled',
        'index',
        'doc_values',
        'path',
        'scaling_factor',
        'pattern'
    ]

    multi_fields_allowed_keys: List[str] = [
        'name',
        'type',
        'norms',
        'default_field',
        'normalizer',
        'ignore_above'
    ]

    fields: List[OrderedDict] = []

    for nested_field_name in source_fields:
        ecs_field: Field = source_fields[nested_field_name]
        beats_field: OrderedDict = ecs_helpers.dict_copy_keys_ordered(ecs_field, allowed_keys)
        if '' == fieldset_prefix:
            contextual_name = nested_field_name
        else:
            contextual_name = '.'.join(nested_field_name.split('.')[1:])

        cleaned_multi_fields: OrderedDict = []
        if 'multi_fields' in ecs_field:
            for mf in ecs_field['multi_fields']:
                cleaned_multi_fields.append(
                    ecs_helpers.dict_copy_keys_ordered(mf, multi_fields_allowed_keys))
            beats_field['multi_fields'] = cleaned_multi_fields

        beats_field['name'] = contextual_name

        fields.append(beats_field)
    return sorted(fields, key=lambda x: x['name'])

# Helpers


def write_beats_yaml(
    beats_file: OrderedDict,
    ecs_version: str,
    out_dir: str
) -> None:
    """Write Beats field definitions to YAML file.

    Creates the final Beats YAML file with a warning header indicating it's
    auto-generated and should not be edited directly.

    Args:
        beats_file: Complete Beats field structure with all fields and metadata
        ecs_version: ECS version string for the header
        out_dir: Output directory

    Generates:
        generated/beats/fields.ecs.yml

    File Structure:
        - Warning header (DO NOT EDIT)
        - Single YAML document wrapped in array
        - Top-level 'ecs' key with title, description, fields

    Note:
        The file is wrapped in an array ([beats_file]) because Beats expects
        a YAML array of field definition documents.
    """
    ecs_helpers.make_dirs(join(out_dir, 'beats'))
    warning: str = file_header().format(version=ecs_version)
    ecs_helpers.yaml_dump(join(out_dir, 'beats/fields.ecs.yml'), [beats_file], preamble=warning)


# Templates


def file_header() -> str:
    """Generate warning header for generated Beats YAML file.

    Returns header text warning users not to edit the file directly, as it's
    auto-generated from ECS schemas.

    Returns:
        Formatted header string with placeholder for version

    Usage:
        >>> header = file_header().format(version='8.11.0')
        # Inserts version into the warning message
    """
    return """
# WARNING! Do not edit this file directly, it was generated by the ECS project,
# based on ECS version {version}.
# Please visit https://github.com/elastic/ecs to suggest changes to ECS fields.

""".lstrip()
