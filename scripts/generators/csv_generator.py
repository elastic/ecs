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

import _csv
import csv
import sys
from typing import (
    Dict,
    List,
)

from os.path import join
from generator import ecs_helpers
from ecs_types import (
    Field,
)


def generate(ecs_flat: Dict[str, Field], version: str, out_dir: str) -> None:
    ecs_helpers.make_dirs(join(out_dir, 'csv'))
    sorted_fields = base_first(ecs_flat)
    save_csv(join(out_dir, 'csv/fields.csv'), sorted_fields, version)


def base_first(ecs_flat: Dict[str, Field]) -> List[Field]:
    base_list: List[Field] = []
    sorted_list: List[Field] = []
    for field_name in sorted(ecs_flat):
        if '.' in field_name:
            sorted_list.append(ecs_flat[field_name])
        else:
            base_list.append(ecs_flat[field_name])
    return base_list + sorted_list


def save_csv(file: str, sorted_fields: List[Field], version: str) -> None:
    open_mode: str = "wb"
    if sys.version_info >= (3, 0):
        open_mode: str = "w"

    with open(file, open_mode) as csvfile:
        schema_writer: _csv._writer = csv.writer(csvfile,
                                                 delimiter=',',
                                                 quoting=csv.QUOTE_MINIMAL,
                                                 lineterminator='\n')

        schema_writer.writerow(["ECS_Version", "Indexed", "Field_Set", "Field",
                                "Type", "Level", "Normalization", "Example", "Description"])
        for field in sorted_fields:
            key_parts: List[str] = field['flat_name'].split('.')
            if len(key_parts) == 1:
                field_set: str = 'base'
            else:
                field_set: str = key_parts[0]

            indexed: str = str(field.get('index', True)).lower()
            schema_writer.writerow([
                version,
                indexed,
                field_set,
                field['flat_name'],
                field['type'],
                field['level'],
                ', '.join(field['normalize']),
                field.get('example', ''),
                field['short'],
            ])

            if 'multi_fields' in field:
                for mf in field['multi_fields']:
                    schema_writer.writerow([
                        version,
                        indexed,
                        field_set,
                        mf['flat_name'],
                        mf['type'],
                        field['level'],
                        '',
                        field.get('example', ''),
                        field['short'],
                    ])
