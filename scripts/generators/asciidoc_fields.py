import sys

from generators import ecs_helpers


def generate(ecs_nested, ecs_version):
    save_asciidoc('docs/fields.asciidoc', page_field_index(ecs_nested))
    save_asciidoc('docs/field-details.asciidoc', page_field_details(ecs_nested))

# Helpers


def save_asciidoc(file, text):
    open_mode = "wb"
    if sys.version_info >= (3, 0):
        open_mode = "w"
    with open(file, open_mode) as outfile:
        outfile.write(text)


# Rendering

# Field Index


def page_field_index(ecs_nested):
    page_text = index_header()
    for fieldset in ecs_helpers.dict_sorted_by_keys(ecs_nested, ['group', 'name']):
        page_text += render_field_index_row(fieldset)
    page_text += table_footer()
    page_text += index_footer()
    return page_text


def render_field_index_row(fieldset):
    return index_row().format(
        fieldset_id='ecs-' + fieldset['name'],
        fieldset_title=fieldset['title'],
        fieldset_short=fieldset.get('short', fieldset['description'])
    )


# Field Details Page

def page_field_details(ecs_nested):
    page_text = ''
    for fieldset in ecs_helpers.dict_sorted_by_keys(ecs_nested, ['group', 'name']):
        page_text += render_fieldset(fieldset, ecs_nested)
    return page_text


def render_fieldset(fieldset, ecs_nested):
    text = field_details_table_header().format(
        fieldset_name=fieldset['name'],
        fieldset_description=fieldset['description'],
        fieldset_title=fieldset['title']
    )

    for field in ecs_helpers.dict_sorted_by_keys(fieldset['fields'], 'flat_name'):
        if 'original_fieldset' not in field:
            text += render_field_details_row(field)

    text += table_footer()

    if 'nestings' in fieldset:
        text += nestings_table_header().format(
            fieldset_name=fieldset['name'],
            fieldset_title=fieldset['title']
        )

        nestings = []
        for nested_fs_name in sorted(fieldset['nestings']):
            text += render_nesting_row({
                'flat_nesting': "{}.{}.*".format(fieldset['name'], nested_fs_name),
                'name': nested_fs_name,
                'short': ecs_nested[nested_fs_name]['short']
            })
        text += table_footer()

    return text


def render_field_details_row(field):
    example = ''
    if 'example' in field:
        example = "example: `{}`".format(str(field['example']))
    text = field_details_row().format(
        field_flat_name=field['flat_name'],
        field_description=field['description'],
        field_example=example,
        field_level=field['level'],
        field_type=field['type'],
    )
    return text


def render_nesting_row(nesting):
    text = nestings_row().format(
        nesting_name=nesting['name'],
        flat_nesting=nesting['flat_nesting'],
        nesting_short=nesting['short'],
    )
    return text


# Templates


def table_footer():
    return '''
|=====
'''


# Field Index


def index_header():
    return '''
[[ecs-fields]]
== {ecs} Fields

[float]
[[ecs-fieldsets]]
=== Field Sets
[cols="<,<",options="header",]
|=======================================================================
| Field Set  | Description
'''


def index_row():
    return '''
| <<{fieldset_id},{fieldset_title}>> | {fieldset_short}
'''


def index_footer():
    return '''
include::field-details.asciidoc[]
'''


# Field Details Page

# Main Fields Table


def field_details_table_header():
    return '''
[[ecs-{fieldset_name}]]
=== {fieldset_title} fields

{fieldset_description}

==== {fieldset_title} Fields

[options="header"]
|=====
| Field  | Description | Level

// ===============================================================
'''


def field_details_row():
    return '''
| {field_flat_name}
| {field_description}

type: {field_type}

{field_example}

| {field_level}

// ===============================================================
'''


# Nestings table

def nestings_table_header():
    return '''
[[ecs-{fieldset_name}-nestings]]
==== Can be nested under {fieldset_title}

[options="header"]
|=====
| Nested fields | Description

// ===============================================================

'''


def nestings_row():
    return '''
| http://localhost:8000/ecs-{nesting_name}.html[{flat_nesting}]
| {nesting_short}

// ===============================================================

'''
