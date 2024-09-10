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

import copy
import os
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

from generators import intermediate_files
from schema import (
    cleaner,
    loader,
)
from _types import (
    FieldEntry
)

# This script takes all ECS and custom fields already loaded, and lets users
# filter out the ones they don't need.


def filter(
    fields: Dict[str, FieldEntry],
    subset_file_globs: List[str],
    out_dir: str
) -> Tuple[Dict[str, FieldEntry], Dict[str, FieldEntry]]:
    subsets: List[Dict[str, Any]] = load_subset_definitions(subset_file_globs)
    for subset in subsets:
        subfields: Dict[str, FieldEntry] = extract_matching_fields(fields, subset['fields'])
        intermediate_files.generate(subfields, os.path.join(out_dir, 'ecs', 'subset', subset['name']), False)

    merged_subset: Dict[str, Any] = combine_all_subsets(subsets)
    if merged_subset:
        fields = extract_matching_fields(fields, merged_subset)

    # Looks for the `docs_only` attribute, which generates a second field subset
    # to pass to the ascii_doc generator
    # After second subset is generated, `docs_only: True` fields are removed
    # from the `fields` subset
    docs_only_field_paths = generate_docs_only_paths(merged_subset)
    if docs_only_field_paths:
        docs_only_subset = generate_docs_only_subset(docs_only_field_paths)
        docs_only_fields = extract_matching_fields(fields, docs_only_subset)
        fields = remove_docs_only_entries(docs_only_field_paths, fields)
    else:
        docs_only_fields = {}
    return fields, docs_only_fields


def generate_docs_only_subset(paths: List[str]) -> Dict[str, Any]:
    """
    Takes paths list of `docs_only` fields and generates a subset
    """
    docs_only_subset = {}
    for path in paths:
        # split and reverse
        split_path = path.split('.')[::-1]
        current_obj = docs_only_subset
        while len(split_path) > 1:
            temp_path = split_path.pop()
            if not current_obj.get(temp_path):
                current_obj[temp_path] = {'fields': {}}
            current_obj = current_obj[temp_path]['fields']
        current_obj[split_path[-1]] = {}
    return docs_only_subset


def generate_docs_only_paths(
    subset: Dict[str, Any],
    filtered: Optional[Dict[str, Any]] = {},
    parent: Optional[str] = '',
    path: Optional[str] = '',
    paths: Optional[List[str]] = [],
) -> List[str]:
    """
    Returns a list of field paths: ['process.same_as_process'] for subset fields
    marked as `docs_only: True`
    """
    for current in subset:
        if subset[current].get('docs_only'):
            path += f'.{current}'
            paths.append(path)
        if 'fields' in subset[current] and isinstance(subset[current]['fields'], dict):
            if not parent:
                path_name = current
            else:
                path_name = f'{parent}.{current}'
            generate_docs_only_paths(subset[current]['fields'],
                                     filtered=filtered,
                                     parent=current,
                                     path=path_name,
                                     paths=paths
                                     )
    return paths


def remove_docs_only_entries(paths: List[str], fields: Dict[str, FieldEntry]) -> Dict[str, FieldEntry]:
    """
    Removed each path in paths list from the fields object
    """
    for path in paths:
        split_path = path.split('.')
        field_set = split_path[0]
        field = split_path[1]
        del (fields[field_set]['fields'][field])
    return fields


def combine_all_subsets(subsets: Dict[str, Any]) -> Dict[str, Any]:
    """Merges N subsets into one. Strips top level 'name' and 'fields' keys as well as non-ECS field options since we can't know how to merge those."""
    merged_subset = {}
    for subset in subsets:
        strip_non_ecs_options(subset['fields'])
        merge_subsets(merged_subset, subset['fields'])
    return merged_subset


def load_subset_definitions(file_globs: List[str]) -> List[Dict[str, Any]]:
    if not file_globs:
        return []
    subsets: List[Dict[str, Any]] = loader.load_definitions(file_globs)
    if not subsets:
        raise ValueError('--subset specified, but no subsets found in {}'.format(file_globs))
    return subsets


ecs_options: List[str] = ['fields', 'enabled', 'index', 'docs_only']


def strip_non_ecs_options(subset: Dict[str, Any]) -> None:
    for key in subset:
        subset[key] = {x: subset[key][x] for x in subset[key] if x in ecs_options}
        if 'fields' in subset[key] and isinstance(subset[key]['fields'], dict):
            strip_non_ecs_options(subset[key]['fields'])


def merge_subsets(a: Dict[str, Any], b: Dict[str, Any]) -> None:
    """Merges field subset definitions together. The b subset is merged into the a subset. Assumes that subsets have been stripped of non-ecs options."""
    for key in b:
        if key not in a:
            a[key] = b[key]
        elif 'fields' in a[key] and 'fields' in b[key]:
            if b[key]['fields'] == '*':
                a[key]['fields'] = '*'
            elif isinstance(a[key]['fields'], dict) and isinstance(b[key]['fields'], dict):
                merge_subsets(a[key]['fields'], b[key]['fields'])
        elif 'fields' in a[key] or 'fields' in b[key]:
            raise ValueError("Subsets unmergeable: 'fields' found in key '{}' in only one subset".format(key))
        # If both subsets have enabled set to False, this will leave enabled: False in the merged subset
        # Otherwise, enabled is removed and is implicitly true
        if a[key].get('enabled', True) or b[key].get('enabled', True):
            a[key].pop('enabled', None)
        # Same logic from 'enabled' applies to 'index'
        if a[key].get('index', True) or b[key].get('index', True):
            a[key].pop('index', None)


def extract_matching_fields(
    fields: Dict[str, FieldEntry],
    subset_definitions: Dict[str, Any]
) -> Dict[str, FieldEntry]:
    """Removes fields that are not in the subset definition. Returns a copy without modifying the input fields dict."""
    retained_fields: Dict[str, FieldEntry] = {x: fields[x].copy() for x in subset_definitions}
    for key, val in subset_definitions.items():
        retained_fields[key]['field_details'] = fields[key]['field_details'].copy()
        for option in val:
            if option != 'fields':
                if 'intermediate' in retained_fields[key]['field_details']:
                    retained_fields[key]['field_details']['intermediate'] = False
                    retained_fields[key]['field_details'].setdefault(
                        'description', 'Intermediate field included by adding option with subset')
                    retained_fields[key]['field_details']['level'] = 'custom'
                    cleaner.field_cleanup(retained_fields[key])
                retained_fields[key]['field_details'][option] = val[option]
        # If the field in the schema has a 'fields' key, we expect a 'fields' key in the subset
        if 'fields' in fields[key]:
            if 'fields' not in val:
                raise ValueError("'fields' key expected, not found in subset for {}".format(key))
            elif isinstance(val['fields'], dict):
                retained_fields[key]['fields'] = extract_matching_fields(fields[key]['fields'], val['fields'])
            elif val['fields'] != "*":
                raise ValueError("Unexpected value '{}' found in 'fields' key".format(val['fields']))
        # If the field in the schema does not have a 'fields' key, there should not be a 'fields' key in the subset
        elif 'fields' in val:
            raise ValueError("'fields' key not expected, found in subset for {}".format(key))
    return retained_fields
