def visit_fields(fields, fieldset_func=None, field_func=None):
    '''
    This function navigates the deeply nested tree structure and runs provided
    functions on each fieldset or field encountered (both optional).

    The 'fieldset_func' provided will be called for each field set,
    with the dictionary containing their details ({'schema_details': {}, 'field_details': {}, 'fields': {}).

    The 'field_func' provided will be called for each field, with the dictionary
    containing the field's details ({'field_details': {}, 'fields': {}).
    '''
    for (name, details) in fields.items():
        if fieldset_func and 'schema_details' in details:
            fieldset_func(details)
        elif field_func and 'field_details' in details:
            field_func(details)
        if 'fields' in details:
            visit_fields(details['fields'],
                    fieldset_func=fieldset_func,
                    field_func=field_func)
