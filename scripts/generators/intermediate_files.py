import copy

from schema import visitor
from generators import ecs_helpers
from os.path import join


def generate(fields, out_dir):
    flat = generate_fully_flattened_fields(fields)
    nested = {} #generate_partially_flattened_fields(fields)

    ecs_helpers.make_dirs(join(out_dir, 'ecs'))
    ecs_helpers.yaml_dump(join(out_dir, 'ecs/ecs_flat.yml'), flat)
    ecs_helpers.yaml_dump(join(out_dir, 'ecs/ecs_nested.yml'), nested)
    ecs_helpers.yaml_dump(join(out_dir, 'ecs/ecs.yml'), fields)
    return nested, flat


def generate_fully_flattened_fields(fields):
    filtered = remove_non_root_reusables(fields)
    flattened = {}
    visitor.visit_fields_with_memo(filtered, get_flat_fields, flattened)
    return flattened


def get_flat_fields(details, memo):
    '''Visitor function that accumulates all flat field details in the memo dict'''
    if 'schema_details' in details or ecs_helpers.is_intermediate(details):
        return
    field_details = copy.deepcopy(details['field_details'])
    if 'leaf_name' in field_details:
        field_details.pop('leaf_name')
    flat_name = field_details['flat_name']
    memo[flat_name] = field_details


def remove_non_root_reusables(fields_nested):
    fields = {}
    for (name, field) in fields_nested.items():
        if 'reusable' not in field['schema_details'] or field['schema_details']['reusable']['top_level']:
            fields[name] = field
    return fields


def generate_partially_flattened_fields(fields):
    flat_fields = {}
    for (name, field) in fields.items():
        # assigning field.copy() adds all the top level schema fields, has to be a copy since we're about
        # to reassign the 'fields' key and we don't want to modify fields_nested
        flat_fields[name] = field.copy()
        flat_fields[name]['fields'] = flatten_fields(field['fields'], "")
    return flat_fields


def flatten_fields(fields, key_prefix):
    flat_fields = {}
    for (name, field) in fields.items():
        new_key = key_prefix + name
        if 'field_details' in field:
            flat_fields[new_key] = field['field_details'].copy()
        if 'fields' in field:
            new_prefix = new_key + "."
            if 'root' in field['schema_details'] and field['schema_details']['root']:
                new_prefix = ""
            flat_fields.update(flatten_fields(field['fields'], new_prefix))
    return flat_fields
