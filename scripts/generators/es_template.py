import json
import sys
import copy

from os.path import join
from generators import ecs_helpers


def generate(ecs_flat, ecs_version, out_dir, template_settings_file, mapping_settings_file):
    field_mappings = {}
    for flat_name in sorted(ecs_flat):
        field = ecs_flat[flat_name]
        nestings = flat_name.split('.')
        dict_add_nested(field_mappings, nestings, entry_for(field))

    if mapping_settings_file:
        with open(mapping_settings_file) as f:
            mappings_section = json.load(f)
    else:
        mappings_section = default_mapping_settings(ecs_version)

    mappings_section['properties'] = field_mappings

    generate_template_version(6, mappings_section, out_dir, template_settings_file)
    generate_template_version(7, mappings_section, out_dir, template_settings_file)

# Field mappings


def dict_add_nested(dct, nestings, value):
    current_nesting = nestings[0]
    rest_nestings = nestings[1:]
    if len(rest_nestings) > 0:
        dct.setdefault(current_nesting, {})
        dct[current_nesting].setdefault('properties', {})

        dict_add_nested(
            dct[current_nesting]['properties'],
            rest_nestings,
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
        elif field['type'] == 'text':
            ecs_helpers.dict_copy_existing_keys(field, field_entry, ['norms'])

        if 'multi_fields' in field:
            field_entry['fields'] = {}
            for mf in field['multi_fields']:
                mf_entry = {'type': mf['type']}
                if mf['type'] == 'text':
                    ecs_helpers.dict_copy_existing_keys(mf, mf_entry, ['norms'])
                field_entry['fields'][mf['name']] = mf_entry

    except KeyError as ex:
        print("Exception {} occurred for field {}".format(ex, field))
        raise ex
    return field_entry

# Generated files


def generate_template_version(elasticsearch_version, mappings_section, out_dir, template_settings_file):
    ecs_helpers.make_dirs(join(out_dir, 'elasticsearch', str(elasticsearch_version)))
    if template_settings_file:
        with open(template_settings_file) as f:
            template = json.load(f)
    else:
        template = default_template_settings()
    if elasticsearch_version == 6:
        template['mappings'] = {'_doc': mappings_section}
    else:
        template['mappings'] = mappings_section

    filename = join(out_dir, "elasticsearch/{}/template.json".format(elasticsearch_version))
    save_json(filename, template)


def save_json(file, data):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"
    with open(file, open_mode) as jsonfile:
        jsonfile.write(json.dumps(data, indent=2, sort_keys=True))


def default_template_settings():
    return {
        "index_patterns": ["ecs-*"],
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
        "mappings": {}
    }


def default_mapping_settings(ecs_version):
    return {
        "_meta": {"version": ecs_version},
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
        ],
        "properties": {}
    }
