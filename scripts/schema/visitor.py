def visit_fields(fields, fieldset_func=None, field_func=None):
    """
    This function navigates the deeply nested tree structure and runs provided
    functions on each fieldset or field encountered (both optional).

    The argument 'fields' should be at the named field grouping level:
    {'name': {'schema_details': {}, 'field_details': {}, 'fields': {}}

    The 'fieldset_func(details)' provided will be called for each field set,
    with the dictionary containing their details ({'schema_details': {}, 'field_details': {}, 'fields': {}).

    The 'field_func(details)' provided will be called for each field, with the dictionary
    containing the field's details ({'field_details': {}, 'fields': {}).
    """
    for (name, details) in fields.items():
        if fieldset_func and 'schema_details' in details:
            fieldset_func(details)
        elif field_func and 'field_details' in details:
            field_func(details)
        if 'fields' in details:
            visit_fields(details['fields'],
                         fieldset_func=fieldset_func,
                         field_func=field_func)


def visit_fields_with_path(fields, func, path=[]):
    """
    This function navigates the deeply nested tree structure and runs the provided
    function on all fields and field sets.

    The 'func' provided will be called for each field,
    with the dictionary containing their details ({'field_details': {}, 'fields': {})
    as well as the path array leading to the location of the field in question.
    """
    for (name, details) in fields.items():
        if 'field_details' in details:
            func(details, path)
        if 'fields' in details:
            if 'schema_details' in details and details['schema_details']['root']:
                new_nesting = []
            else:
                new_nesting = [name]
            visit_fields_with_path(details['fields'], func, path + new_nesting)


def visit_fields_with_memo(fields, func, memo=None):
    """
    This function navigates the deeply nested tree structure and runs the provided
    function on all fields and field sets.

    The 'func' provided will be called for each field,
    with the dictionary containing their details ({'field_details': {}, 'fields': {})
    as well as the 'memo' you pass in.
    """
    for (name, details) in fields.items():
        if 'field_details' in details:
            func(details, memo)
        if 'fields' in details:
            visit_fields_with_memo(details['fields'], func, memo)
