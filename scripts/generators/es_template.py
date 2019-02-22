import json
import sys


def generate(ecs_flat):
    template = base_template()
    template['mappings']['_doc']['_meta']['version'] = '1.0.0-beta2'

    template_fields_root = template['mappings']['_doc']['properties']
    for flat_name in ecs_flat:
        field = ecs_flat[flat_name]
        nestings = flat_name.split('.')
        dict_add_nested(template_fields_root, nestings, entry_for(field))

    save_json('generated/elasticsearch/template.json', template)


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


def dict_copy_existing_keys(source, destination, keys):
    for key in keys:
        if key in source:
            destination[key] = source[key]


def entry_for(field):
    dict = { 'type': field['type'] }
    try:
        if 'index' in field and not field['index']:
            dict_copy_existing_keys(field, dict, ['index', 'doc_values'])

        if field['type'] == 'keyword':
            dict_copy_existing_keys(field, dict, ['ignore_above'])
        elif field['type'] == 'text':
            dict_copy_existing_keys(field, dict, ['norms'])
    except KeyError as ex:
        print ex, field
        raise ex
    return dict


def save_json(file, data):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"
    with open(file, open_mode) as jsonfile:
        jsonfile.write(json.dumps(data, indent=2, sort_keys=True))


def base_template():
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
            "mappings": {
                "_doc": {
                    "_meta": {},
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
            }
        }
