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

from os.path import join

from generators import ecs_helpers

# Composable Template


def generate(ecs_nested, ecs_version, out_dir, mapping_settings_file):
    """This generates all artifacts for the composable template approach"""
    analyzers = all_component_templates(ecs_nested, ecs_version, out_dir)
    component_names = component_name_convention(ecs_version, ecs_nested)
    save_composable_template(ecs_version, component_names, out_dir, mapping_settings_file, analyzers)


def save_composable_template(ecs_version, component_names, out_dir, mapping_settings_file, analyzers):
    """Generate the master sample composable template"""
    template = {
        "index_patterns": ["try-ecs-*"],
        "composed_of": component_names,
        "priority": 1,  # Very low, as this is a sample template
        "_meta": {
            "ecs_version": ecs_version,
            "description": "Sample composable template that includes all ECS fields"
        },
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
            "mappings": mapping_settings(mapping_settings_file)
        }
    }

    """Adding an empty configuration for each custom analyzer for the user to utilize"""
    if (analyzers):
        template['template']['settings']['analysis'] = {
            'analyzer': {}
        }
        for analyzer in analyzers:
            template['template']['settings']['analysis']['analyzer'] = {
                analyzer: { }
            }

    filename = join(out_dir, "elasticsearch/composable/template.json")
    save_json(filename, template)


def all_component_templates(ecs_nested, ecs_version, out_dir):
    """Generate one component template per field set"""
    component_dir = join(out_dir, 'elasticsearch/composable/component')
    ecs_helpers.make_dirs(component_dir)
    analyzers = set()

    for (fieldset_name, fieldset) in candidate_components(ecs_nested).items():
        field_mappings = {}
        
        for (flat_name, field) in fieldset['fields'].items():
            name_parts = flat_name.split('.')
            field_entry = entry_for(field)
            field_level = field['level']
            dict_add_nested(field_mappings, name_parts, field_entry)

            if ('fields' in field_entry):
                for field in field_entry['fields'].items():
                    if ('analyzer' in field[1]):
                        analyzers.add(field[1]['analyzer'])

        save_component_template(fieldset_name, field_level, ecs_version, component_dir, field_mappings)

    return analyzers


def save_component_template(template_name, field_level, ecs_version, out_dir, field_mappings):
    filename = join(out_dir, template_name) + ".json"
    reference_url = "https://www.elastic.co/guide/en/ecs/current/ecs-{}.html".format(template_name)

    template = {
        'template': {'mappings': {'properties': field_mappings}},
        '_meta': {
            'ecs_version': ecs_version,
        }
    }

    """Only generate a documentation link for ECS fields"""
    if (field_level != 'custom'):
        template['_meta']['documentation'] = reference_url

    save_json(filename, template)


def component_name_convention(ecs_version, ecs_nested):
    version = ecs_version.replace('+', '-')
    names = []
    for (fieldset_name, fieldset) in candidate_components(ecs_nested).items():
        names.append("ecs_{}_{}".format(version, fieldset_name.lower()))
    return names


def candidate_components(ecs_nested):
    """Returns same structure as ecs_nested, but skips all field sets with reusable.top_level: False"""
    components = {}
    for (fieldset_name, fieldset) in ecs_nested.items():
        if fieldset.get('reusable', None):
            if not fieldset['reusable']['top_level']:
                continue
        components[fieldset_name] = fieldset
    return components


# Legacy template


def generate_legacy(ecs_flat, ecs_version, out_dir, template_settings_file, mapping_settings_file):
    """Generate the legacy index template"""
    field_mappings = {}
    analyzers = set()
    for flat_name in sorted(ecs_flat):
        field = ecs_flat[flat_name]
        name_parts = flat_name.split('.')
        field_entry = entry_for(field)
        dict_add_nested(field_mappings, name_parts, field_entry)

        if ('fields' in field_entry):
            for field in field_entry['fields'].items():
                if ('analyzer' in field[1]):
                    analyzers.add(field[1]['analyzer'])

    mappings_section = mapping_settings(mapping_settings_file)
    mappings_section['properties'] = field_mappings

    generate_legacy_template_version(ecs_version, mappings_section, out_dir, analyzers, template_settings_file)


def generate_legacy_template_version(ecs_version, mappings_section, out_dir, analyzers, template_settings_file):
    ecs_helpers.make_dirs(join(out_dir, 'elasticsearch', "legacy"))
    template = template_settings(ecs_version, mappings_section, analyzers, template_settings_file)

    filename = join(out_dir, "elasticsearch/legacy/template.json")
    save_json(filename, template)


# Common helpers


def dict_add_nested(dct, name_parts, value):
    current_nesting = name_parts[0]
    rest_name_parts = name_parts[1:]
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


def entry_for(field):
    field_entry = {'type': field['type']}
    try:
        if field['type'] == 'object' or field['type'] == 'nested':
            if 'enabled' in field and not field['enabled']:
                ecs_helpers.dict_copy_existing_keys(field, field_entry, ['enabled'])
        # the index field is only valid for field types that are not object and nested
        elif 'index' in field and not field['index']:
            ecs_helpers.dict_copy_existing_keys(field, field_entry, ['index', 'doc_values'])

        if field['type'] == 'keyword':
            ecs_helpers.dict_copy_existing_keys(field, field_entry, ['ignore_above'])
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
                field_entry['fields'][mf['name']] = mf_entry

    except KeyError as ex:
        print("Exception {} occurred for field {}".format(ex, field))
        raise ex
    return field_entry


def mapping_settings(mapping_settings_file):
    if mapping_settings_file:
        with open(mapping_settings_file) as f:
            mappings = json.load(f)
    else:
        mappings = default_mapping_settings()
    return mappings


def template_settings(ecs_version, mappings_section, analyzers, template_settings_file):
    if template_settings_file:
        with open(template_settings_file) as f:
            template = json.load(f)
    else:
        template = default_template_settings(ecs_version)

    template['mappings'] = mappings_section

    """Adding an empty configuration for each custom analyzer for the user to utilize"""
    if (analyzers):
        template['settings']['analysis'] = {
            'analyzer': {}
        }
        for analyzer in analyzers:
            template['settings']['analysis']['analyzer'] = {
                analyzer: { }
            }

    # _meta can't be at template root in legacy templates, so moving back to mappings section
    # if present
    if '_meta' in template:
        mappings_section['_meta'] = template.pop('_meta')

    return template


def save_json(file, data):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"
    with open(file, open_mode) as jsonfile:
        json.dump(data, jsonfile, indent=2, sort_keys=True)
        jsonfile.write('\n')


def default_template_settings(ecs_version):
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


def default_mapping_settings():
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
