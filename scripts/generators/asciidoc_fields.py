import os.path as path
from generators import ecs_helpers

import jinja2

# jinja2 setup
TEMPLATE_DIR = path.join(path.dirname(path.abspath(__file__)), 'templates')
template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
template_env = jinja2.Environment(loader=template_loader)

def generate(nested, ecs_version, out_dir):
    save_asciidoc(path.join(out_dir, 'fields.asciidoc'), page_field_index(nested, ecs_version))
    save_asciidoc(path.join(out_dir, 'field-details.asciidoc'), page_field_details(nested))
    save_asciidoc(path.join(out_dir, 'field-values.asciidoc'), page_field_values(nested))

# Helpers


def save_asciidoc(file, text):
    with open(file, "w") as outfile:
        outfile.write(text)


# Rendering schemas

# Field Index

def page_field_index(nested, ecs_version):
    fieldsets = ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name'])
    page_text = generate_field_index(ecs_version, fieldsets)
    return page_text


# Field Details Page

def page_field_details(nested):
    page_text = ''
    for fieldset in ecs_helpers.dict_sorted_by_keys(nested, ['group', 'name']):
        page_text += render_fieldset(fieldset, nested)
    return page_text


def render_fieldset(fieldset, nested):
    text = field_details_table_header(
        title=fieldset['title'],
        name=fieldset['name'],
        description=fieldset['description']
    )

    text += render_fields(fieldset['fields'])

    text += table_footer()

    text += render_fieldset_reuse_section(fieldset, nested)

    return text


def render_fields(fields):
    text = ''
    for field_name, field in sorted(fields.items()):
        # Skip fields nested in this field set
        if 'original_fieldset' not in field:
            text += render_field_details_row(field)
    return text


def render_asciidoc_paragraphs(string):
    '''Simply double the \n'''
    return string.replace("\n", "\n\n")


def render_field_allowed_values(field):
    if not 'allowed_values' in field:
        return ''
    allowed_values = ', '.join(ecs_helpers.list_extract_keys(field['allowed_values'], 'name'))

    return field_acceptable_value_names(
        allowed_values=allowed_values,
        flat_name=field['flat_name'],
        dashed_name=field['dashed_name']
    )


def render_field_details_row(field):
    example = ''
    if 'allowed_values' in field:
        example = render_field_allowed_values(field)
    elif 'example' in field:
        example = "example: `{}`".format(str(field['example']))

    field_type_with_mf = field['type']
    if 'multi_fields' in field:
        field_type_with_mf += "\n\nMulti-fields:\n\n"
        for mf in field['multi_fields']:
            field_type_with_mf += "* {} (type: {})\n\n".format(mf['flat_name'], mf['type'])

    field_normalization = ''
    if 'array' in field['normalize']:
        field_normalization = "\nNote: this field should contain an array of values.\n\n"

    text = field_details_row(
        flat_name=field['flat_name'],
        description=field['description'],
        field_type=field_type_with_mf,
        example=example,
        normalization=field_normalization,
        level=field['level']
    )

    return text


def render_fieldset_reuse_section(fieldset, nested):
    '''Render the section on where field set can be nested, and which field sets can be nested here'''
    if not ('nestings' in fieldset or 'reusable' in fieldset):
        return ''

    text = field_reuse_section(
        reuse_of_fieldset=render_fieldset_reuses_text(fieldset)
    )

    if 'nestings' in fieldset:
        text += nestings_table_header(
            name=fieldset['name'],
            title=fieldset['title']
        )
        rows = []
        for reused_here_entry in fieldset['reused_here']:
            rows.append({
                'flat_nesting': "{}.*".format(reused_here_entry['full']),
                'name': reused_here_entry['schema_name'],
                'short': reused_here_entry['short']
            })

        for row in sorted(rows, key=lambda x: x['flat_nesting']):
            text += nestings_row(
                nesting_name=row['name'],
                flat_nesting=row['flat_nesting'],
                nesting_short=row['short']
            )

        text += table_footer()
    return text


def render_fieldset_reuses_text(fieldset):
    '''Render where a given field set is expected to be reused'''
    if 'reusable' not in fieldset:
        return ''

    section_name = fieldset['name']
    sorted_fields = sorted(fieldset['reusable']['expected'], key=lambda k: k['full'])
    rendered_fields = map(lambda f: "`{}`".format(f['full']), sorted_fields)
    text = "The `{}` fields are expected to be nested at: {}.\n\n".format(
        section_name, ', '.join(rendered_fields))

    if 'top_level' in fieldset['reusable'] and fieldset['reusable']['top_level']:
        # TODO rewording kept for follow-up PR to simplify initial rewrite PR
        # template = "Note also that the `{}` fields may be used directly at the root of the events.\n\n"
        template = "Note also that the `{}` fields may be used directly at the top level.\n\n"
    else:
        template = "Note also that the `{}` fields are not expected to " + \
            "be used directly at the top level.\n\n"
        # TODO rewording kept for follow-up PR to simplify initial rewrite PR
        # "be used directly at the root of the events.\n\n"
    text += template.format(section_name)
    return text


# Templates

def table_footer():
    return '''
|=====
'''

# Field Index

def generate_field_index(ecs_version, fieldsets, template_name='fields_template.j2'):
    template = template_env.get_template(template_name)
    return template.render(ecs_version=ecs_version, fieldsets=fieldsets)


# Field Details Page

# Main Fields Table

def field_details_table_header(title, name, description, template_name='field_details/table_header.j2'):
    template = template_env.get_template(template_name)
    return template.render(name=name, title=title, description=description)


def field_details_row(flat_name, description, field_type, normalization, example, level, template_name='field_details/row.j2'):
    template = template_env.get_template(template_name)
    return template.render(
        flat_name=flat_name,
        description=description,
        field_type=field_type,
        normalization=normalization,
        example=example,
        level=level
    )


def field_acceptable_value_names(allowed_values, dashed_name, flat_name, template_name='field_details/acceptable_value_names.j2'):
    template = template_env.get_template(template_name)
    return template.render(
        allowed_values=allowed_values,
        dashed_name=dashed_name,
        flat_name=flat_name
    )


# Field reuse

def field_reuse_section(reuse_of_fieldset, template_name='field_details/field_reuse_section.j2'):
    template = template_env.get_template(template_name)
    return template.render(reuse_of_fieldset=reuse_of_fieldset)


# Nestings table

def nestings_table_header(name, title, template_name='field_details/nestings_table_header.j2'):
    template = template_env.get_template(template_name)
    return template.render(name=name, title=title)


def nestings_row(nesting_name, flat_nesting, nesting_short, template_name='field_details/nestings_row.j2'):
    template = template_env.get_template(template_name)
    return template.render(
        nesting_name=nesting_name,
        flat_nesting=flat_nesting,
        nesting_short=nesting_short
    )


# Allowed values section

def page_field_values(nested, template_name='field_values_template.j2'):
    category_fields = ['event.kind', 'event.category', 'event.type', 'event.outcome']
    nested_fields = []
    for cat_field in category_fields:
        nested_fields.append(nested['event']['fields'][cat_field])

    template = template_env.get_template(template_name)
    return template.render(fields=nested_fields)
