###
# Generates a JSON Schema spec based of the expected index mappings.
###

import json
import os

from generators import ecs_helpers


def generate(ecs_nested, ecs_flat, ecs_version, out_dir):
    schema_dir = os.path.join(out_dir, 'json_schema')
    ecs_helpers.make_dirs(schema_dir)
    data_types = used_data_types(ecs_flat)

    schema = {}
    schema['version'] = ecs_version
    schema['definitions'] = schema_definitions(data_types)
    schema['properties'] = {}

    eligible_schemas = candidate_schemas(ecs_nested)

    for (fieldset_name, fieldset) in eligible_schemas.items():
        field_mappings = {}
        for (flat_name, field) in fieldset['fields'].items():
            name_parts = flat_name.split('.')
            dict_add_nested(field_mappings, name_parts, entry_for(field))

        if fieldset.get('root'):
            schema['properties'].update(field_mappings)
        else:
            schema['properties'][fieldset_name] = field_mappings[fieldset_name]
            schema['properties'][fieldset_name]['type'] = 'object'
            schema['properties'][fieldset_name]['description'] = fieldset['description']
    save_schema_file('schema', ecs_version, schema_dir, schema)


def used_data_types(ecs_flat):

    types = []

    for field in ecs_flat.keys():
        current_type = ecs_flat[field]['type']
        if current_type not in types:
            types.append(current_type)

    return types

def candidate_schemas(ecs_nested):
    components = {}
    for (fieldset_name, fieldset) in ecs_nested.items():
        if fieldset.get('reusable', None):
            if not fieldset['reusable']['top_level']:
                continue
        components[fieldset_name] = fieldset
    return components


def save_schema_file(schema_name, ecs_version, out_dir, field_mappings):
    filename = f'{os.path.join(out_dir, schema_name)}.json'
    with open(filename, 'w') as jsonfile:
        jsonfile.write(json.dumps(field_mappings, indent=2, sort_keys=True))


def dict_add_nested(dct, name_parts, value):
    current_nesting = name_parts[0]
    rest_name_parts = name_parts[1:]
    # breakpoint()
    if len(rest_name_parts) > 0:
        schema_boilerplate = {
            "properties": {
                "type": "object",
                "properties": {}
            }
        }
        dct.setdefault(current_nesting, schema_boilerplate)
        dct[current_nesting]['properties'].setdefault('properties', {})
        dct[current_nesting]['properties']['properties'].setdefault('properties', {})

        dict_add_nested(
            dct[current_nesting]['properties']['properties']['properties'],
            rest_name_parts,
            value
        )

    else:
        if current_nesting in dct and 'type' in value['properties'] and 'object' in value['properties']['type']:
            return
        dct[current_nesting] = value


def entry_for(field):
    single_line_descrip = field['description'].replace('\n', ' ')
    field_entry = {
        "description": single_line_descrip,
        "type": "object",
        "properties": {
            "type": {
                "$ref": f"#/definitions/types/{field['type']}"
            }
        }
    }

    if field.get('type') != 'object':
        field_entry['required'] = ["type"]
    return field_entry


def schema_definitions(data_types):
    definitions = {
        "types": {
            "type": "object"
        }
    }

    for data_type in data_types:
        definitions['types'][data_type] = {}
        definitions['types'][data_type] = {
            "type": "string",
            "enum": [ data_type ]
        }

    return definitions
