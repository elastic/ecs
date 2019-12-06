import yaml

from collections import OrderedDict
from generators import ecs_helpers


def generate(ecs_nested, ecs_version):
    # base first
    beats_fields = fieldset_field_array(ecs_nested['base']['fields'])

    allowed_fieldset_keys = ['name', 'title', 'group', 'description', 'footnote', 'type']
    # other fieldsets
    for fieldset_name in sorted(ecs_nested):
        if 'base' == fieldset_name:
            continue
        fieldset = ecs_nested[fieldset_name]

        beats_field = ecs_helpers.dict_copy_keys_ordered(fieldset, allowed_fieldset_keys)
        beats_field['fields'] = fieldset_field_array(fieldset['fields'])
        beats_fields.append(beats_field)

    beats_file = OrderedDict()
    beats_file['key'] = 'ecs'
    beats_file['title'] = 'ECS'
    beats_file['description'] = 'ECS Fields.'
    beats_file['fields'] = beats_fields

    write_beats_yaml(beats_file, ecs_version)


def fieldset_field_array(source_fields):
    allowed_keys = ['name', 'level', 'required', 'type', 'object_type',
                    'ignore_above', 'multi_fields', 'format', 'input_format',
                    'output_format', 'output_precision', 'description', 'example']
    multi_fields_allowed_keys = ['name', 'type', 'norms']

    fields = []
    for nested_field_name in source_fields:
        ecs_field = source_fields[nested_field_name]
        beats_field = ecs_helpers.dict_copy_keys_ordered(ecs_field, allowed_keys)

        cleaned_multi_fields = []
        if 'multi_fields' in ecs_field:
            for mf in ecs_field['multi_fields']:
                cleaned_multi_fields.append(
                    ecs_helpers.dict_copy_keys_ordered(mf, multi_fields_allowed_keys))
            beats_field['multi_fields'] = cleaned_multi_fields

        beats_field['name'] = nested_field_name
        fields.append(beats_field)
    return sorted(fields, key=lambda x: x['name'])

# Helpers


def write_beats_yaml(beats_file, ecs_version):
    warning = file_header().format(version=ecs_version)
    ecs_helpers.yaml_dump('generated/beats/fields.ecs.yml', [beats_file], preamble=warning)


# Templates


def file_header():
    return '''
# WARNING! Do not edit this file directly, it was generated by the ECS project,
# based on ECS version {version}.
# Please visit https://github.com/elastic/ecs to suggest changes to ECS fields.

'''.lstrip()
