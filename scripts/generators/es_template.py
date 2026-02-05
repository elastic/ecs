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

"""Elasticsearch Template Generator.

This module generates Elasticsearch index templates from ECS schemas. It supports
both modern composable templates and legacy single-file templates, producing
JSON files that can be directly installed into Elasticsearch.

Composable Templates (Modern):
    - One component template per ECS fieldset
    - Main template that composes all components together
    - Allows selective field adoption
    - Recommended for Elasticsearch 7.8+

Legacy Templates (Deprecated):
    - Single monolithic template with all fields
    - Backwards compatibility for older Elasticsearch versions
    - Simpler but less flexible

The generator transforms ECS field definitions into Elasticsearch mapping syntax,
handling:
- Field type mappings (keyword, text, IP, etc.)
- Multi-field configurations
- Custom parameters (ignore_above, norms, etc.)
- Nested object structures
- Index and doc_values settings

Key Components:
    - generate(): Composable template generation entry point
    - generate_legacy(): Legacy template generation entry point
    - entry_for(): Converts ECS field to Elasticsearch mapping
    - dict_add_nested(): Builds nested property structures
    - Template settings: Configurable index patterns, priorities, settings

Output Files:
    Composable:
        - generated/elasticsearch/composable/template.json
        - generated/elasticsearch/composable/component/*.json (one per fieldset)
    Legacy:
        - generated/elasticsearch/legacy/template.json

These templates are ready to be installed into Elasticsearch using:
    PUT _index_template/ecs (composable)
    PUT _template/ecs (legacy)

See also: scripts/docs/es-template.md for detailed documentation
"""

import json
import sys
from typing import (
    Dict,
    List,
    Optional,
    Union
)

from os.path import join

from generators import ecs_helpers
from ecs_types import (
    Field,
    FieldNestedEntry,
)

# Composable Template


def generate(
    ecs_nested: Dict[str, FieldNestedEntry],
    ecs_version: str,
    out_dir: str,
    mapping_settings_file: str,
    template_settings_file: str
) -> None:
    """Generate all composable template artifacts for Elasticsearch.

    Creates the modern composable template approach where each ECS fieldset becomes
    a separate component template. This allows users to selectively include only
    the fieldsets they need, reducing mapping overhead.

    Args:
        ecs_nested: Nested fieldset structure from intermediate_files
        ecs_version: ECS version string (e.g., '8.11.0')
        out_dir: Output directory (typically 'generated')
        mapping_settings_file: Path to JSON file with custom mapping settings, or None
        template_settings_file: Path to JSON file with custom template settings, or None

    Generates:
        - generated/elasticsearch/composable/component/{fieldset}.json (one per fieldset)
        - generated/elasticsearch/composable/template.json (main template)

    Process:
        1. Generate individual component template for each fieldset
        2. Build list of component names following naming convention
        3. Generate main composable template that references all components

    Note:
        Composable templates require Elasticsearch 7.8 or later.
        Each component can be updated independently in production.

    Example:
        >>> generate(nested, '8.11.0', 'generated', None, None)
        # Creates:
        # - generated/elasticsearch/composable/component/base.json
        # - generated/elasticsearch/composable/component/agent.json
        # - ...
        # - generated/elasticsearch/composable/template.json
    """
    all_component_templates(ecs_nested, ecs_version, out_dir)
    component_names = component_name_convention(ecs_version, ecs_nested)
    save_composable_template(ecs_version, component_names, out_dir, mapping_settings_file, template_settings_file)


def save_composable_template(ecs_version, component_names, out_dir, mapping_settings_file, template_settings_file):
    """Save the main composable index template that references component templates.

    Creates the composable template JSON file that ties together all component
    templates. This template defines index patterns, priority, settings, and
    lists all component templates to compose.

    Args:
        ecs_version: ECS version string
        component_names: List of component template names to include
        out_dir: Output directory
        mapping_settings_file: Path to custom mapping settings JSON, or None
        template_settings_file: Path to custom template settings JSON, or None

    Generates:
        generated/elasticsearch/composable/template.json

    Template structure:
        {
            "index_patterns": ["try-ecs-*"],
            "composed_of": ["ecs_8.11.0_base", "ecs_8.11.0_agent", ...],
            "priority": 1,
            "template": {
                "mappings": {...},
                "settings": {...}
            },
            "_meta": {...}
        }
    """
    mappings_section = mapping_settings(mapping_settings_file)
    template = template_settings(ecs_version, mappings_section, template_settings_file, component_names=component_names)

    filename = join(out_dir, "elasticsearch/composable/template.json")
    save_json(filename, template)


def all_component_templates(
    ecs_nested: Dict[str, FieldNestedEntry],
    ecs_version: str,
    out_dir: str
) -> None:
    """Generate individual component templates for each ECS fieldset.

    Creates one JSON file per fieldset containing the Elasticsearch mapping
    for all fields in that fieldset. Each component template is self-contained
    and can be installed/updated independently.

    Args:
        ecs_nested: Nested fieldset structure from intermediate_files
        ecs_version: ECS version string
        out_dir: Output directory

    Generates:
        One file per fieldset in generated/elasticsearch/composable/component/:
        - base.json
        - agent.json
        - http.json
        - etc.

    Process:
        1. Filter out non-root reusable fieldsets (top_level=false)
        2. For each remaining fieldset:
           a. Build nested property structure from flat field names
           b. Convert each field to Elasticsearch mapping format
           c. Save as component template JSON

    Note:
        Uses dict_add_nested() to convert flat names like 'http.request.method'
        into nested structure: {http: {properties: {request: {properties: {method: {...}}}}}}
    """
    component_dir: str = join(out_dir, 'elasticsearch/composable/component')
    ecs_helpers.make_dirs(component_dir)

    for (fieldset_name, fieldset) in ecs_helpers.remove_top_level_reusable_false(ecs_nested).items():
        field_mappings = {}
        for (flat_name, field) in fieldset['fields'].items():
            name_parts = flat_name.split('.')
            dict_add_nested(field_mappings, name_parts, entry_for(field))

        save_component_template(fieldset_name, field['level'], ecs_version, component_dir, field_mappings)


def save_component_template(
    template_name: str,
    field_level: str,
    ecs_version: str,
    out_dir: str,
    field_mappings: Dict
) -> None:
    """Save a single component template JSON file.

    Creates a component template with the mappings for one fieldset, including
    metadata about the ECS version and documentation link.

    Args:
        template_name: Name of the fieldset (e.g., 'http', 'user')
        field_level: Field level (core/extended/custom) - used to determine if doc link needed
        ecs_version: ECS version string
        out_dir: Component template directory
        field_mappings: Nested dictionary of field mappings

    Generates:
        {out_dir}/{template_name}.json

    Template structure:
        {
            "template": {
                "mappings": {
                    "properties": {
                        "http": {
                            "properties": {
                                "request": {...},
                                "response": {...}
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

    Note:
        Documentation URL is only added for ECS fields (not custom fields).
    """
    filename: str = join(out_dir, template_name) + ".json"
    reference_url: str = "https://www.elastic.co/guide/en/ecs/current/ecs-{}.html".format(template_name)

    template: Dict = {
        'template': {'mappings': {'properties': field_mappings}},
        '_meta': {
            'ecs_version': ecs_version,
        }
    }

    """Only generate a documentation link for ECS fields"""
    if (field_level != 'custom'):
        template['_meta']['documentation'] = reference_url

    save_json(filename, template)


def component_name_convention(
    ecs_version: str,
    ecs_nested: Dict[str, FieldNestedEntry]
) -> List[str]:
    """Build list of component template names following ECS naming convention.

    Generates the standardized names for component templates that will be
    referenced in the main composable template. Names follow the pattern:
    ecs_{version}_{fieldset}

    Args:
        ecs_version: ECS version string (e.g., '8.11.0' or '8.11.0+exp')
        ecs_nested: Nested fieldset structure

    Returns:
        Sorted list of component template names

    Name format:
        - Version: Replace '+' with '-' (e.g., '8.11.0+exp' -> '8.11.0-exp')
        - Fieldset: Lowercase name
        - Pattern: 'ecs_{version}_{fieldset}'

    Examples:
        >>> component_name_convention('8.11.0', nested)
        ['ecs_8.11.0_agent', 'ecs_8.11.0_base', 'ecs_8.11.0_client', ...]

        >>> component_name_convention('8.11.0+exp', nested)
        ['ecs_8.11.0-exp_agent', 'ecs_8.11.0-exp_base', ...]

    Note:
        Only includes fieldsets with top_level=true (or no reusable setting).
        Names are used in the 'composed_of' array in the main template.
    """
    version: str = ecs_version.replace('+', '-')
    names: List[str] = []
    for (fieldset_name, fieldset) in ecs_helpers.remove_top_level_reusable_false(ecs_nested).items():
        names.append("ecs_{}_{}".format(version, fieldset_name.lower()))
    return names


# Legacy template


def generate_legacy(
    ecs_flat: Dict[str, Field],
    ecs_version: str,
    out_dir: str,
    mapping_settings_file: str,
    template_settings_file: str
) -> None:
    """Generate legacy single-file index template for backwards compatibility.

    Creates the older-style index template where all field mappings are defined
    in a single monolithic JSON file. This format is supported by all versions
    of Elasticsearch but is less flexible than composable templates.

    Args:
        ecs_flat: Flat field dictionary from intermediate_files
        ecs_version: ECS version string
        out_dir: Output directory
        mapping_settings_file: Path to custom mapping settings JSON, or None
        template_settings_file: Path to custom template settings JSON, or None

    Generates:
        generated/elasticsearch/legacy/template.json

    Process:
        1. Iterate through all fields in sorted order
        2. Convert flat names to nested property structure
        3. Build complete mappings section
        4. Generate template with settings and mappings

    Template structure:
        {
            "index_patterns": ["try-ecs-*"],
            "order": 1,
            "settings": {...},
            "mappings": {
                "_meta": {...},
                "date_detection": false,
                "dynamic_templates": [...],
                "properties": {
                    "agent": {...},
                    "http": {...},
                    ...
                }
            }
        }

    Note:
        Legacy templates are deprecated in Elasticsearch 7.8+ in favor of
        composable templates. Use this only for backwards compatibility.
    """
    field_mappings = {}
    for flat_name in sorted(ecs_flat):
        field = ecs_flat[flat_name]
        name_parts = flat_name.split('.')
        dict_add_nested(field_mappings, name_parts, entry_for(field))

    mappings_section: Dict = mapping_settings(mapping_settings_file)
    mappings_section['properties'] = field_mappings

    generate_legacy_template_version(ecs_version, mappings_section, out_dir, template_settings_file)


def generate_legacy_template_version(
    ecs_version: str,
    mappings_section: Dict,
    out_dir: str,
    template_settings_file: str
) -> None:
    """Create and save the legacy template JSON file.

    Builds the complete legacy template structure and writes it to disk.

    Args:
        ecs_version: ECS version string
        mappings_section: Complete mappings dictionary including properties
        out_dir: Output directory
        template_settings_file: Path to custom template settings JSON, or None

    Generates:
        generated/elasticsearch/legacy/template.json

    Note:
        Creates the legacy directory if it doesn't exist.
    """
    ecs_helpers.make_dirs(join(out_dir, 'elasticsearch', "legacy"))
    template: Dict = template_settings(ecs_version, mappings_section, template_settings_file, is_legacy=True)

    filename: str = join(out_dir, "elasticsearch/legacy/template.json")
    save_json(filename, template)


# Common helpers


def dict_add_nested(
    dct: Dict,
    name_parts: List[str],
    value: Dict
) -> None:
    """Recursively build nested Elasticsearch properties structure from flat field name.

    Converts a flat field name like 'http.request.method' into nested Elasticsearch
    mapping structure:

    {
        "http": {
            "properties": {
                "request": {
                    "properties": {
                        "method": {<field_mapping>}
                    }
                }
            }
        }
    }

    Args:
        dct: Dictionary being built (modified in place)
        name_parts: List of name components (e.g., ['http', 'request', 'method'])
        value: Field mapping to place at the leaf (e.g., {'type': 'keyword'})

    Behavior:
        - Recursively creates nested 'properties' dictionaries
        - If current level already exists as object type, skips (avoids overwriting)
        - Sets value at the deepest nesting level

    Example:
        >>> mapping = {}
        >>> dict_add_nested(mapping, ['http', 'request', 'method'], {'type': 'keyword'})
        >>> mapping
        {
            'http': {
                'properties': {
                    'request': {
                        'properties': {
                            'method': {'type': 'keyword'}
                        }
                    }
                }
            }
        }

    Note:
        Modifies the dictionary in place. Used to build the complete mapping
        structure from individual fields.
    """
    current_nesting: str = name_parts[0]
    rest_name_parts: List[str] = name_parts[1:]
    if len(rest_name_parts) > 0:
        dct.setdefault(current_nesting, {})
        dct[current_nesting].setdefault('properties', {})

        dict_add_nested(
            dct[current_nesting]['properties'],
            rest_name_parts,
            value)

    else:
        if current_nesting in dct and 'type' in value and 'object' == value['type']:
            return
        dct[current_nesting] = value


def entry_for(field: Field) -> Dict:
    """Convert an ECS field definition to Elasticsearch mapping format.

    Transforms ECS field metadata into the appropriate Elasticsearch mapping
    configuration, handling type-specific parameters and multi-fields.

    Args:
        field: ECS field definition with type, parameters, multi_fields, etc.

    Returns:
        Dictionary containing Elasticsearch mapping for this field

    Mapping rules by type:
        - keyword/flattened: Copy ignore_above, synthetic_source_keep
        - constant_keyword: Copy value parameter
        - text: Copy norms setting
        - alias: Copy path (field being aliased)
        - scaled_float: Copy scaling_factor
        - object/nested: Copy enabled flag if false
        - All others: Copy index, doc_values if index=false

    Multi-fields:
        If field has multi_fields, creates 'fields' section with alternate
        representations (e.g., keyword field with text.match_phrase multi-field)

    Custom parameters:
        If field has 'parameters' dict, merges directly into mapping

    Example:
        >>> field = {
        ...     'type': 'keyword',
        ...     'ignore_above': 1024,
        ...     'multi_fields': [{
        ...         'name': 'text',
        ...         'type': 'match_only_text'
        ...     }]
        ... }
        >>> entry_for(field)
        {
            'type': 'keyword',
            'ignore_above': 1024,
            'fields': {
                'text': {'type': 'match_only_text'}
            }
        }

    Raises:
        KeyError: If required field properties are missing

    Note:
        This function handles the core logic of translating ECS semantics
        into Elasticsearch mapping syntax.
    """
    field_entry: Dict = {'type': field['type']}
    try:
        if field['type'] == 'object' or field['type'] == 'nested':
            if 'enabled' in field and not field['enabled']:
                ecs_helpers.dict_copy_existing_keys(field, field_entry, ['enabled'])
        # the index field is only valid for field types that are not object and nested
        elif 'index' in field and not field['index']:
            ecs_helpers.dict_copy_existing_keys(field, field_entry, ['index', 'doc_values'])

        if field['type'] == 'keyword' or field['type'] == 'flattened':
            ecs_helpers.dict_copy_existing_keys(field, field_entry, ['ignore_above', 'synthetic_source_keep'])
        elif field['type'] == 'constant_keyword':
            ecs_helpers.dict_copy_existing_keys(field, field_entry, ['value'])
        elif field['type'] == 'text':
            ecs_helpers.dict_copy_existing_keys(field, field_entry, ['norms'])
        elif field['type'] == 'alias':
            ecs_helpers.dict_copy_existing_keys(field, field_entry, ['path'])
        elif field['type'] == 'scaled_float':
            ecs_helpers.dict_copy_existing_keys(field, field_entry, ['scaling_factor'])

        if 'multi_fields' in field:
            field_entry['fields'] = {}
            for mf in field['multi_fields']:
                mf_type = mf['type']
                mf_entry = {'type': mf_type}
                if mf_type == 'keyword':
                    ecs_helpers.dict_copy_existing_keys(mf, mf_entry, ['normalizer', 'ignore_above'])
                elif mf_type == 'text':
                    ecs_helpers.dict_copy_existing_keys(mf, mf_entry, ['norms', 'analyzer'])
                if 'parameters' in mf:
                    mf_entry.update(mf['parameters'])
                field_entry['fields'][mf['name']] = mf_entry

        if 'parameters' in field:
            field_entry.update(field['parameters'])

    except KeyError as ex:
        print("Exception {} occurred for field {}".format(ex, field))
        raise ex
    return field_entry


def mapping_settings(mapping_settings_file: str) -> Dict:
    """Load mapping settings from file or use defaults.

    Mapping settings control how Elasticsearch handles unmapped fields and
    other mapping behaviors like date detection and dynamic templates.

    Args:
        mapping_settings_file: Path to JSON file with custom settings, or None/empty

    Returns:
        Dictionary with mapping settings including:
        - date_detection: Whether to auto-detect date fields
        - dynamic_templates: Rules for mapping unmapped fields

    Example custom settings file:
        {
            "date_detection": false,
            "dynamic_templates": [{
                "strings_as_keyword": {
                    "match_mapping_type": "string",
                    "mapping": {"type": "keyword", "ignore_above": 1024}
                }
            }]
        }
    """
    if mapping_settings_file:
        with open(mapping_settings_file) as f:
            mappings = json.load(f)
    else:
        mappings = default_mapping_settings()
    return mappings


def template_settings(
    ecs_version: str,
    mappings_section: Dict,
    template_settings_file: Union[str, None],
    is_legacy: Optional[bool] = False,
    component_names: Optional[List[str]] = None
) -> Dict:
    """Load and finalize template settings (index patterns, priority, settings).

    Template settings define which indices the template applies to, its priority,
    index settings, and other metadata. Can be customized via JSON file or use defaults.

    Args:
        ecs_version: ECS version string
        mappings_section: Mapping settings and field properties
        template_settings_file: Path to custom template settings JSON, or None
        is_legacy: Whether generating legacy template format
        component_names: List of component names (for composable templates only)

    Returns:
        Complete template dictionary ready to save

    Structure for composable:
        {
            "index_patterns": ["try-ecs-*"],
            "composed_of": ["ecs_8.11.0_base", ...],
            "priority": 1,
            "template": {
                "settings": {...},
                "mappings": {...}
            },
            "_meta": {"ecs_version": "8.11.0", ...}
        }

    Structure for legacy:
        {
            "index_patterns": ["try-ecs-*"],
            "order": 1,
            "settings": {...},
            "mappings": {
                "_meta": {...},
                "properties": {...}
            }
        }

    Note:
        Calls finalize_template() to merge mappings and component names.
    """
    if template_settings_file:
        with open(template_settings_file) as f:
            template = json.load(f)
    else:
        if is_legacy:
            template = default_legacy_template_settings(ecs_version)
        else:
            template = default_template_settings(ecs_version)

    finalize_template(template, ecs_version, is_legacy, mappings_section, component_names)

    return template


def finalize_template(
    template: Dict,
    ecs_version: str,
    is_legacy: bool,
    mappings_section: Dict,
    component_names: List[str]
) -> None:
    """Finalize template by merging mappings and metadata.

    Completes the template structure by adding mappings, component references
    (for composable), and metadata. Handles structural differences between
    legacy and composable template formats.

    Args:
        template: Base template dictionary (modified in place)
        ecs_version: ECS version string
        is_legacy: Whether this is a legacy template
        mappings_section: Complete mappings with properties
        component_names: List of component template names (composable only)

    Legacy modifications:
        - Mappings placed directly under 'mappings' key
        - Moves _meta from root into mappings section

    Composable modifications:
        - Mappings placed under template.mappings
        - Adds composed_of array with component names
        - Adds _meta at root level

    Note:
        Modifies the template dictionary in place.
    """
    if is_legacy:
        if mappings_section:
            template['mappings'] = mappings_section

            # _meta can't be at template root in legacy templates, so moving back to mappings section
            # if present
            if '_meta' in template:
                mappings_section['_meta'] = template.pop('_meta')

    else:
        template['template']['mappings'] = mappings_section
        template['composed_of'] = component_names
        template['_meta'] = {
            "ecs_version": ecs_version,
            "description": "Sample composable template that includes all ECS fields"
        }


def save_json(file: str, data: Dict) -> None:
    """Save dictionary as formatted JSON file.

    Writes JSON with consistent formatting: 2-space indentation, sorted keys,
    and trailing newline.

    Args:
        file: Path to output file
        data: Dictionary to serialize

    Format:
        - 2-space indentation for readability
        - Sorted keys for consistent diffs
        - Trailing newline (Unix convention)

    Note:
        Python 2/3 compatible (uses binary mode for Python 2).
    """
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"
    with open(file, open_mode) as jsonfile:
        json.dump(data, jsonfile, indent=2, sort_keys=True)
        jsonfile.write('\n')


def default_template_settings(ecs_version: str) -> Dict:
    """Generate default settings for composable template.

    Provides sensible defaults for a composable template including index
    patterns, priority, and index settings.

    Args:
        ecs_version: ECS version string

    Returns:
        Template settings dictionary with:
        - index_patterns: Matches 'try-ecs-*' indices (safe for testing)
        - priority: 1 (very low, won't override production templates)
        - codec: best_compression (saves disk space)
        - total_fields.limit: 2000 (enough for all ECS fields)

    Note:
        These are sample settings. Production use should customize:
        - index_patterns to match actual indices
        - priority based on template precedence needs
        - settings based on cluster capacity and use case
    """
    return {
        "index_patterns": ["try-ecs-*"],
        "_meta": {
            "ecs_version": ecs_version,
            "description": "Sample composable template that includes all ECS fields"
        },
        "priority": 1,  # Very low, as this is a sample template
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
        }
    }


def default_legacy_template_settings(ecs_version: str) -> Dict:
    """Generate default settings for legacy template.

    Provides sensible defaults for a legacy template with higher total_fields
    limit and refresh_interval setting.

    Args:
        ecs_version: ECS version string

    Returns:
        Legacy template settings with:
        - index_patterns: Matches 'try-ecs-*' indices
        - order: 1 (low priority)
        - total_fields.limit: 10000 (legacy templates need higher limits)
        - refresh_interval: 5s (balance between real-time and performance)

    Note:
        Legacy templates require higher total_fields limits because they
        include all mappings in one template. Adjust for production use.
    """
    return {
        "index_patterns": ["try-ecs-*"],
        "_meta": {"version": ecs_version},
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
        }
    }


def default_mapping_settings() -> Dict:
    """Generate default mapping settings for dynamic field handling.

    Provides sensible defaults for how Elasticsearch handles unmapped fields.
    These settings prevent common issues like:
    - Automatic date detection causing mapping conflicts
    - String fields being mapped as text (memory intensive)

    Returns:
        Mapping settings with:
        - date_detection: false (prevents auto-detection of date strings)
        - dynamic_templates: Maps unmapped strings as keyword with ignore_above

    Dynamic template behavior:
        All unmapped string fields become:
        - type: keyword (not text)
        - ignore_above: 1024 (truncates very long strings)

    Note:
        These settings apply to fields not explicitly defined in ECS.
        Customize based on your data characteristics.
    """
    return {
        "date_detection": False,
        "dynamic_templates": [
            {
                "strings_as_keyword": {
                    "mapping": {
                        "ignore_above": 1024,
                        "type": "keyword"
                    },
                    "match_mapping_type": "string"
                }
            }
        ]
    }
