from generators import ecs_helpers
from os.path import join


def generate(fields, out_dir):
    nested, flat = generate_nested_flat(fields)

    ecs_helpers.make_dirs(join(out_dir, 'ecs'))
    ecs_helpers.yaml_dump(join(out_dir, 'ecs/ecs_flat.yml'), flat)
    ecs_helpers.yaml_dump(join(out_dir, 'ecs/ecs_nested.yml'), nested)
    ecs_helpers.yaml_dump(join(out_dir, 'ecs/ecs.yml'), fields)
    return nested, flat


def generate_nested_flat(fields_intermediate):
    for field_name, field in fields_intermediate.items():
        nestings = find_nestings(field['fields'], field_name + ".")
        nestings.sort()
        if len(nestings) > 0:
            field['nestings'] = nestings
    fields_nested = generate_partially_flattened_fields(fields_intermediate)
    fields_flat = generate_fully_flattened_fields(fields_intermediate)
    return (fields_nested, fields_flat)


def find_nestings(fields, prefix):
    """Recursively finds all reusable fields in the fields dictionary."""
    nestings = []
    for field_name, field in fields.items():
        if 'reusable' in field:
            nestings.append(prefix + field_name)
        if 'fields' in field:
            nestings.extend(find_nestings(field['fields'], prefix + field_name + '.'))
    return nestings


def generate_partially_flattened_fields(fields_nested):
    flat_fields = {}
    for (name, field) in fields_nested.items():
        # assigning field.copy() adds all the top level schema fields, has to be a copy since we're about
        # to reassign the 'fields' key and we don't want to modify fields_nested
        flat_fields[name] = field.copy()
        flat_fields[name]['fields'] = flatten_fields(field['fields'], "")
    return flat_fields


def generate_fully_flattened_fields(fields_nested):
    flattened = flatten_fields(remove_non_root_reusables(fields_nested), "")
    return flattened


def remove_non_root_reusables(fields_nested):
    fields = {}
    for (name, field) in fields_nested.items():
        if 'reusable' not in field or ('reusable' in field and field['reusable']['top_level']):
            fields[name] = field
    return fields


def flatten_fields(fields, key_prefix):
    flat_fields = {}
    for (name, field) in fields.items():
        new_key = key_prefix + name
        if 'field_details' in field:
            flat_fields[new_key] = field['field_details'].copy()
        if 'fields' in field:
            new_prefix = new_key + "."
            if 'root' in field and field['root']:
                new_prefix = ""
            flat_fields.update(flatten_fields(field['fields'], new_prefix))
    return flat_fields
