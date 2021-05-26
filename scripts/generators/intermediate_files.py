import copy

from schema import visitor
from generators import ecs_helpers
from os.path import join


def generate(fields, out_dir, default_dirs):
    ecs_helpers.make_dirs(join(out_dir))

    # Should only be used for debugging ECS development
    if default_dirs:
        ecs_helpers.yaml_dump(join(out_dir, 'ecs.yml'), fields)
    flat = generate_flat_fields(fields)
    nested = generate_nested_fields(fields)

    ecs_helpers.yaml_dump(join(out_dir, 'ecs_flat.yml'), flat)
    ecs_helpers.yaml_dump(join(out_dir, 'ecs_nested.yml'), nested)
    return nested, flat


def generate_flat_fields(fields):
    """Generate ecs_flat.yml"""
    filtered = remove_non_root_reusables(fields)
    flattened = {}
    visitor.visit_fields_with_memo(filtered, accumulate_field, flattened)
    return flattened


def accumulate_field(details, memo):
    """Visitor function that accumulates all field details in the memo dict"""
    if 'schema_details' in details or ecs_helpers.is_intermediate(details):
        return
    field_details = copy.deepcopy(details['field_details'])
    remove_internal_attributes(field_details)

    flat_name = field_details['flat_name']
    memo[flat_name] = field_details


def generate_nested_fields(fields):
    """Generate ecs_nested.yml"""
    nested = {}
    # Flatten each field set, but keep all resulting fields nested under their
    # parent/host field set.
    for (name, details) in fields.items():
        fieldset_details = {
            **copy.deepcopy(details['field_details']),
            **copy.deepcopy(details['schema_details'])
        }

        fieldset_details.pop('node_name')
        if 'reusable' in fieldset_details:
            fieldset_details['reusable'].pop('order')

        # TODO Temporarily removed to simplify initial rewrite review
        fieldset_details.pop('dashed_name')
        fieldset_details.pop('flat_name')
        if False == fieldset_details['root']:
            fieldset_details.pop('root')

        fieldset_fields = {}
        visitor.visit_fields_with_memo(details['fields'], accumulate_field, fieldset_fields)
        fieldset_details['fields'] = fieldset_fields

        nested[name] = fieldset_details
    return nested


# Helper functions


def remove_internal_attributes(field_details):
    """Remove attributes only relevant to the deeply nested structure, but not to ecs_flat/nested.yml."""
    field_details.pop('node_name', None)
    field_details.pop('intermediate', None)


def remove_non_root_reusables(fields_nested):
    """
    Remove field sets that have top_level=false from the root of the field definitions.

    This attribute means they're only meant to be in the "reusable/expected" locations
    and not at the root of user's events.

    This is only relevant for the 'flat' field representation. The nested one
    still needs to keep all field sets at the root of the YAML file, as it
    the official information about each field set. It's the responsibility of
    users consuming ecs_nested.yml to skip the field sets with top_level=false.
    """
    fields = {}
    for (name, field) in fields_nested.items():
        if 'reusable' not in field['schema_details'] or field['schema_details']['reusable']['top_level']:
            fields[name] = field
    return fields
