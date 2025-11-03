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
    """This generates all artifacts for the composable template approach"""
    all_component_templates(ecs_nested, ecs_version, out_dir)
    component_names = component_name_convention(ecs_version, ecs_nested)
    save_composable_template(ecs_version, component_names, out_dir, mapping_settings_file, template_settings_file)


def save_composable_template(ecs_version, component_names, out_dir, mapping_settings_file, template_settings_file):
    mappings_section = mapping_settings(mapping_settings_file)
    template = template_settings(ecs_version, mappings_section, template_settings_file, component_names=component_names)

    filename = join(out_dir, "elasticsearch/composable/template.json")
    save_json(filename, template)


def all_component_templates(
    ecs_nested: Dict[str, FieldNestedEntry],
    ecs_version: str,
    out_dir: str
) -> None:
    """Generate one component template per field set"""
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
    """Generate the legacy index template"""
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
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"
    with open(file, open_mode) as jsonfile:
        json.dump(data, jsonfile, indent=2, sort_keys=True)
        jsonfile.write('\n')


def default_template_settings(ecs_version: str) -> Dict:
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
