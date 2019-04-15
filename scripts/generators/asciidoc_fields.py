import sys

from generators import ecs_helpers


def generate(ecs_nested, ecs_version):
    save_asciidoc('docs/fields.asciidoc', page_field_index(ecs_nested, ecs_version))
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


def page_field_index(ecs_nested, ecs_version):
    page_text = index_header(ecs_version)
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
        fieldset_title=fieldset['title'],
        fieldset_name=fieldset['name'],
        fieldset_description=render_asciidoc_paragraphs(fieldset['description'])
    )

    for field in ecs_helpers.dict_sorted_by_keys(fieldset['fields'], 'flat_name'):
        if 'original_fieldset' not in field:
            text += render_field_details_row(field)

    text += table_footer()

    text += render_fieldset_reuse_section(fieldset, ecs_nested)

    return text


def render_asciidoc_paragraphs(string):
    '''Simply double the \n'''
    return string.replace("\n", "\n\n")


def render_field_details_row(field):
    example = ''
    if 'example' in field:
        example = "example: `{}`".format(str(field['example']))
    text = field_details_row().format(
        field_flat_name=field['flat_name'],
        field_description=render_asciidoc_paragraphs(field['description']),
        field_example=example,
        field_level=field['level'],
        field_type=field['type'],
    )
    return text


def render_fieldset_reuse_section(fieldset, ecs_nested):
    '''Render the section on where field set can be nested, and which field sets can be nested here'''
    if not ('nestings' in fieldset or 'reusable' in fieldset):
        return ''

    text = field_reuse_section().format(
        reuse_of_fieldset=render_fieldset_reuses_text(fieldset)
    )
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


def render_fieldset_reuses_text(fieldset):
    '''Render where a given field set is expected to be reused'''
    if 'reusable' not in fieldset:
        return ''

    section_name = fieldset['name']
    sorted_fields = sorted(fieldset['reusable']['expected'])
    rendered_fields = map(lambda f: "`{}.{}`".format(f, section_name), sorted_fields)
    text = "The `{}` fields are expected to be nested at: {}.\n\n".format(
        section_name, ', '.join(rendered_fields))

    if 'top_level' in fieldset['reusable'] and fieldset['reusable']['top_level']:
        template = "Note also that the `{}` fields may be used directly at the top level.\n\n"
    else:
        template = "Note also that the `{}` fields are not expected to " + \
            "be used directly at the top level.\n\n"
    text += template.format(section_name)
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


def index_header(ecs_version):
    # Not using format() because then asciidoc {ecs}, {es}, etc are resolved.
    return '''
[[ecs-field-reference]]
== {ecs} Field Reference

This is the documentation of ECS version ''' + ecs_version + '''.

ECS defines multiple groups of related fields. They are called "field sets".
The <<ecs-base,Base>> field set is the only one whose fields are defined
at the root of the event.

All other field sets are defined as objects in {es}, under which
all fields are defined.

[float]
[[ecs-fieldsets]]
=== Field Sets
[cols="<,<",options="header",]
|=====
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
=== {fieldset_title} Fields

{fieldset_description}

==== {fieldset_title} Field Details

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


# Field reuse

def field_reuse_section():
    return '''
==== Field Reuse

{reuse_of_fieldset}

'''


# Nestings table

def nestings_table_header():
    return '''
[[ecs-{fieldset_name}-nestings]]
===== Field sets that can be nested under {fieldset_title}

[options="header"]
|=====
| Nested fields | Description

// ===============================================================

'''


def nestings_row():
    return '''
| <<ecs-{nesting_name},{flat_nesting}>>
| {nesting_short}

// ===============================================================

'''
