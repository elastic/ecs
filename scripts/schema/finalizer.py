import copy

from schema import visitor

# This script takes the fleshed out deeply nested fields dictionary as emitted by
# cleaner.py, and performs field reuse in two phases.
#
# Phase 1 performs field reuse across field sets. E.g. `group` fields should also be under `user`.
# This type of reuse is then carried around if the receiving field set is also reused.
# In other words, user.group.* will be in other places where user is nested:
# source.user.* will contain source.user.group.*

# Phase 2 performs field reuse where field sets are reused within themselves, with a different name.
# Examples are nesting `process` within itself, as `process.parent.*`,
# or nesting `user` within itself at `user.target.*`.
# This second kind of nesting is not carried around everywhere else the receiving field set is reused.
# So `user.target.*` is *not* carried over to `source.user.target*` when we reuse `user` under `source`.

# This script does not modify the deeply nested fields dictionary in place, but
# constructs a completely new copy.


def finalize(fields):
    perform_reuse(fields)
    calculate_final_values(fields)


def perform_reuse(fields):
    self_nestings = {}
    for schema_name, schema in fields.items():
        if not 'reusable' in schema['schema_details']:
            continue
        # Phase 1: foreign nesting
        for reuse_entry in schema['schema_details']['reusable']['expected']:
            destination_fs = reuse_entry['full'].split('.')[0]
            if destination_fs == schema_name:
                # Simply accumulate self-nestings for phase 2.
                self_nestings.setdefault(destination_fs, [])
                self_nestings[destination_fs].extend([reuse_entry])
            else:
                destination_fields = field_group_at_path(reuse_entry['at'], fields)
                schema_name = schema['field_details']['name']
                # Copying everything except the original schema_details.
                # Note that we don't deepcopy those, in order for multiple nestings
                # to all work out, no matter the order we perform them
                # (group => user, then user along with user.group => other places)
                destination_fields[schema_name] = {
                    'field_details': copy.deepcopy(schema['field_details']),
                    'fields': schema['fields'],
                    'referenced_fields': True
                }
            fields[destination_fs]['schema_details'].setdefault('nestings', [])
            fields[destination_fs]['schema_details']['nestings'].extend([reuse_entry['full']])
    # Phase 2: self-nesting
    for schema_name, reuse_entries in self_nestings.items():
        schema = fields[schema_name]
        # The fields that end up inside a field set with self-reuse (e.g. user.target.*)
        # must be a different copy than the fields that are
        # potentially nested elsewhere (e.g. what's at server.user.*).
        # So we self-nest inside a detached copy, then put this detached copy
        # back as the original field set's fields.
        detached_fields = copy.deepcopy(schema['fields'])
        for reuse_entry in reuse_entries:
            nest_as = reuse_entry['as']
            new_field_details = copy.deepcopy(schema['field_details'])
            new_field_details['name'] = nest_as
            detached_fields[nest_as] = {
                    'field_details': new_field_details,
                    'fields': copy.deepcopy(schema['fields']),
                }
        fields[schema_name]['fields'] = detached_fields


def field_group_at_path(dotted_path, fields):
    path = dotted_path.split('.')
    nesting = fields
    for next_field in path:
        field = nesting.get(next_field, None)
        if not field:
            raise ValueError("Field {} not found, failed to find {}".format(dotted_path, next_field))
        nesting = field.get('fields', None)
        if not nesting:
            field_type = field['field_details']['type']
            if field_type in ['object', 'group', 'nested']:
                nesting = field['fields'] = {}
            else:
                raise ValueError("Field {} (type {}) already exists and cannot have nested fields".format(
                    dotted_path, field_type))
    return nesting


def calculate_final_values(fields):
    visitor.visit_fields_with_path(fields, field_finalizer)
    return


def field_finalizer(details, path):
    # leaf_name not always populated
    leaf_name = details['field_details']['name'].split('.')[-1]
    print(path + [leaf_name])
    # Copy referenced fields before we start modifying them
    if 'referenced_fields' in details:
        details['fields'] = copy.deepcopy(details['fields'])
        details.pop('referenced_fields')
    flat_name = '.'.join(path + [leaf_name])
    details['field_details']['flat_name'] = flat_name
    details['field_details']['dashed_name'] = flat_name.replace('.', '-').replace('_', '-')


# def field_print(details, path):
#     print(details['field_details']['name'], path, details)
