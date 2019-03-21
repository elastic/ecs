import json
import sys

from generators import ecs_helpers


def generate(ecs_flat, ecs_version):
    field_mappings = {}
    for flat_name in ecs_flat:
        field = ecs_flat[flat_name]
        nestings = flat_name.split('.')
        dict_add_nested(field_mappings, nestings, entry_for(field))

    mappings_section = mapping_settings(ecs_version)
    mappings_section['properties'] = field_mappings

    generate_template_version(6, mappings_section)
    generate_template_version(7, mappings_section)

# Field mappings


def dict_add_nested(dict, nestings, value):
    current_nesting = nestings[0]
    rest_nestings = nestings[1:]
    if len(rest_nestings) > 0:
        if current_nesting not in dict:
            dict[current_nesting] = {'properties': {}}
        dict_add_nested(
            dict[current_nesting]['properties'],
            rest_nestings,
            value)
    else:
        dict[current_nesting] = value


def entry_for(field):
    dict = {'type': field['type']}
    try:
        if 'index' in field and not field['index']:
            ecs_helpers.dict_copy_existing_keys(field, dict, ['index', 'doc_values'])

        if field['type'] == 'keyword':
            ecs_helpers.dict_copy_existing_keys(field, dict, ['ignore_above'])
        elif field['type'] == 'text':
            ecs_helpers.dict_copy_existing_keys(field, dict, ['norms'])
    except KeyError as ex:
        print ex, field
        raise ex
    return dict

# Generated files


def generate_template_version(elasticsearch_version, mappings_section):
    template = template_settings()
    if elasticsearch_version == 6:
        template['mappings'] = {'_doc': mappings_section}
    else:
        template['mappings'] = mappings_section

    filename = "generated/elasticsearch/{}/template.json".format(elasticsearch_version)
    save_json(filename, template)


def save_json(file, data):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"
    with open(file, open_mode) as jsonfile:
        jsonfile.write(json.dumps(data, indent=2, sort_keys=True))


def template_settings():
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


def mapping_settings(ecs_version):
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
