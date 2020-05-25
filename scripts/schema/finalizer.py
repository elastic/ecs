import copy
import pprint

# This script takes the fleshed out deeply nested fields dictionary as emitted by
# cleaner.py, and performs field reuse in two phases.
#
# The first phase performs field reuse across field sets. E.g. `group` fields should also be under `user`.
# This type of reuse is then carried around if the receiving field set is also reused.
# In other words, user.group.* will be in other places where user is nested:
# source.user.* will contain source.user.group.*

# The second phase performs field reuse where field sets are reused within themselves, with a different name.
# Examples are nesting `process` within itself, as `process.parent.*`,
# or nesting `user` within itself at `user.target.*`.
# This second kind of nesting is not carried around everywhere else the receiving field set is reused.
# So `user.target.*` is *not* carried over to `source.user.target*` when we reuse `user` under `source`.

# This script does not modify the deeply nested fields dictionary in place, but
# constructs a completely new copy.

def finalize(fields):
    self_nestings = []
    # reuse_per_destination = {}
    # self_nestings = {}
    # foreign_nestings = {}
    for schema_name, details in fields.items():
        if not 'reusable' in details['schema_details']:
            continue
        expected = details['schema_details']['reusable']['expected']
        for reuse_entry in expected:
            destination_fs = reuse_entry['full'].split('.')[0]
            if destination_fs == schema_name:
                self_nestings.extend(reuse_entry)
                # self_nestings.setdefault(schema_name, {})
                # self_nestings[schema_name][reuse_entry['as']] = reuse_entry
            else:
                nest_at(reuse_entry, details, fields)
                # foreign_nestings.setdefault(destination_fs, {})
                # foreign_nestings[destination_fs][schema_name] = reuse_entry

            # reuse_per_destination.setdefault(destination_fs, [])
            # reuse_per_destination[destination_fs].extend([schema_name])

    # print("\n", "Per destination")
    # pprint.pprint(reuse_per_destination)
    # print("\n", "Self nestings")
    # pprint.pprint(self_nestings)
    # print("\n", "Foreign nestings")
    # pprint.pprint(foreign_nestings)
    return fields


def nest_at(reuse_entry, details, fields):
    nest_at = reuse_entry['at']
    nest_as = reuse_entry['as']
    # parent_fields = nest_at.split('.')
    destination = field_group_at_path(nest_at, fields)

    # receiving_fieldset = parent_fields[0]
    # # Copying everything except the original schema_details
    # fields = {
    #     'field_details': details['field_details'],
    #     'fields': details['fields'],
    # }


def field_group_at_path(dotted_path, fields):
    path = dotted_path.split('.')
    nesting = fields
    for next_field in path:
        field = nesting.get(next_field, None)
        if not field:
            raise ValueError("Field {} not found, failed to find {}".format(dotted_path, next_field))
        nesting = field.get('fields', None)
        if not nesting:
            raise ValueError("Field {} is not a field group and doesn't have sub-fields".format(
                dotted_path, next_field))
    return nesting
