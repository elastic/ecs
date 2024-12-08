# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from os.path import join
from collections import OrderedDict
from typing import (
    Dict,
    List,
    OrderedDict,
)

from generators import ecs_helpers
from _types import (
    Field,
    FieldNestedEntry,
)


def generate(
    ecs_nested: Dict[str, FieldNestedEntry],
    ecs_version: str,
    out_dir: str
) -> None:
    # base first
    ecs_nested = ecs_helpers.remove_top_level_reusable_false(ecs_nested)
    beats_fields: List[OrderedDict] = fieldset_field_array(ecs_nested['base']['fields'], ecs_nested['base']['prefix'])

    allowed_fieldset_keys: List[str] = ['name', 'title', 'group', 'description', 'footnote', 'type']
    # other fieldsets
    for fieldset_name in sorted(ecs_nested):
        if 'base' == fieldset_name:
            continue
        fieldset: FieldNestedEntry = ecs_nested[fieldset_name]

        # Handle when `root:true`
        if fieldset.get('root', False):
            beats_fields.extend(fieldset_field_array(fieldset['fields'], fieldset['prefix']))
            continue

        beats_field = ecs_helpers.dict_copy_keys_ordered(fieldset, allowed_fieldset_keys)
        beats_field['fields'] = fieldset_field_array(fieldset['fields'], fieldset['prefix'])
        beats_fields.append(beats_field)

    # Load temporary allowlist for default_fields workaround.
    df_allowlist = ecs_helpers.yaml_load('scripts/generators/beats_default_fields_allowlist.yml')
    # Set default_field configuration.
    set_default_field(beats_fields, df_allowlist)

    beats_file: OrderedDict = OrderedDict()
    beats_file['key'] = 'ecs'
    beats_file['title'] = 'ECS'
    beats_file['description'] = 'ECS Fields.'
    beats_file['fields'] = beats_fields

    write_beats_yaml(beats_file, ecs_version, out_dir)


def set_default_field(fields, df_allowlist, df=False, path=''):
    for fld in fields:
        fld_df = fld.get('default_field', df)
        fld_path = fld['name']
        if path != '' and not fld.get('root', False):
            fld_path = path + '.' + fld_path
        fld_type = fld.get('type', 'keyword')
        expected = fld_path in df_allowlist or (fld_path == fld['name'] and fld_type == 'group')
        if fld_df != expected:
            ecs_helpers.ordered_dict_insert(fld, 'default_field', expected, before_key='fields')
        if fld_type == 'group':
            set_default_field(fld['fields'], df_allowlist, df=expected, path=fld_path)
        elif 'multi_fields' in fld:
            set_default_field(fld['multi_fields'], df_allowlist, df=expected, path=fld_path)


def fieldset_field_array(
    source_fields: Dict[str, Field],
    fieldset_prefix: str
) -> List[OrderedDict]:
    allowed_keys: List[str] = [
        'name',
        'level',
        'required',
        'type',
        'object_type',
        'ignore_above',
        'multi_fields',
        'format',
        'input_format',
        'output_format',
        'output_precision',
        'description',
        'example',
        'enabled',
        'index',
        'doc_values',
        'path',
        'scaling_factor',
        'pattern'
    ]

    multi_fields_allowed_keys: List[str] = [
        'name',
        'type',
        'norms',
        'default_field',
        'normalizer',
        'ignore_above'
    ]

    fields: List[OrderedDict] = []

    for nested_field_name in source_fields:
        ecs_field: Field = source_fields[nested_field_name]
        beats_field: OrderedDict = ecs_helpers.dict_copy_keys_ordered(ecs_field, allowed_keys)
        if '' == fieldset_prefix:
            contextual_name = nested_field_name
        else:
            contextual_name = '.'.join(nested_field_name.split('.')[1:])

        cleaned_multi_fields: OrderedDict = []
        if 'multi_fields' in ecs_field:
            for mf in ecs_field['multi_fields']:
                cleaned_multi_fields.append(
                    ecs_helpers.dict_copy_keys_ordered(mf, multi_fields_allowed_keys))
            beats_field['multi_fields'] = cleaned_multi_fields

        beats_field['name'] = contextual_name

        fields.append(beats_field)
    return sorted(fields, key=lambda x: x['name'])

# Helpers


def write_beats_yaml(
    beats_file: OrderedDict,
    ecs_version: str,
    out_dir: str
) -> None:
    ecs_helpers.make_dirs(join(out_dir, 'beats'))
    warning: str = file_header().format(version=ecs_version)
    ecs_helpers.yaml_dump(join(out_dir, 'beats/fields.ecs.yml'), [beats_file], preamble=warning)


# Templates


def file_header() -> str:
    return """
# WARNING! Do not edit this file directly, it was generated by the ECS project,
# based on ECS version {version}.
# Please visit https://github.com/elastic/ecs to suggest changes to ECS fields.

""".lstrip()
