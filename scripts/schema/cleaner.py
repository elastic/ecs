import copy

from generators import ecs_helpers

def clean(fields):
    fields = schema_cleanup(fields)
    return fields

def schema_cleanup(fields):
    return fields



def visit_fields(fields, fieldset_func=None, field_func=None, path=[]):
    for (name, details) in fields.items():
        current_path = path + [name]
        if fieldset_func and 'schema_details' in details:
            fieldset_func(details, current_path)
        # Note that all schemas have field_details as well, so this gets called on them too.
        if field_func and 'field_details' in details:
            field_func(details, current_path)
        if 'fields' in details:
            visit_fields(details['fields'], fieldset_func=fieldset_func, field_func=field_func, path=current_path)



        # # Both 'fields' and 'field_details' can be present (e.g. when type=object like dns.answers)
        # if 'field_details' in nested:   # it's a field!
        #     field_func(current_nesting, nested['field_details'])
        # if 'fields' in nested:          # it has nested fields!
        #     recurse_fields(field_func, nested['fields'], current_nesting)

    # # fieldset attributes at same level, not nested under 'field_details'
    # is_fieldset = (fields.get('type', None) == 'group' and
        #           type(fields.get('fields', None)) == dict and
        #           [] == field_nesting)
    # if is_fieldset:
        # if 'root' in fields:
        #     current_nesting = []
        # else:
        #     current_nesting = [fields['name']]
        # fields = fields['fields']
    # else:
        # current_nesting = [fields['name']]

    # for (name, nested) in fields.items():
        # # if 'root' in nested: # should only be "base" fields
        # #     current_nesting = field_nesting
        # # else:
        # #     current_nesting = field_nesting + [name]

        # # Both 'fields' and 'field_details' can be present (e.g. when type=object like dns.answers)
        # if 'field_details' in nested:   # it's a field!
        #     field_func(current_nesting, nested['field_details'])
        # if 'fields' in nested:          # it has nested fields!
        #     recurse_fields(field_func, nested['fields'], current_nesting)


