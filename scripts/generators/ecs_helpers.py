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

import glob
import os
import yaml
import git
import pathlib
from typing import (
    Any,
    Dict,
    List,
    Optional,
    OrderedDict,
    Set,
    Union,
)
import warnings

from collections import OrderedDict
from copy import deepcopy
from _types import (
    Field,
    FieldEntry,
    FieldNestedEntry,
)

# Dictionary helpers


def dict_copy_keys_ordered(dct: Field, copied_keys: List[str]) -> Field:
    ordered_dict = OrderedDict()
    for key in copied_keys:
        if key in dct:
            ordered_dict[key] = dct[key]
    return ordered_dict


def dict_copy_existing_keys(source: Field, destination: Field, keys: List[str]) -> None:
    for key in keys:
        if key in source:
            destination[key] = source[key]


def dict_sorted_by_keys(dct: FieldNestedEntry, sort_keys: List[str]) -> List[FieldNestedEntry]:
    if not isinstance(sort_keys, list):
        sort_keys = [sort_keys]

    tuples: List[List[Union[int, str, FieldNestedEntry]]] = []

    for key in dct:
        nested = dct[key]

        sort_criteria = []
        for sort_key in sort_keys:
            sort_criteria.append(nested[sort_key])
        sort_criteria.append(nested)
        tuples.append(sort_criteria)

    return list(map(lambda t: t[-1], sorted(tuples)))


def ordered_dict_insert(
    dct: Field,
    new_key: str, new_value: Union[str, bool],
    before_key: Optional[str] = None,
    after_key: Optional[str] = None
) -> None:
    output = OrderedDict()
    inserted: bool = False
    for key, value in dct.items():
        if not inserted and before_key is not None and key == before_key:
            output[new_key] = new_value
            inserted = True
        output[key] = value
        if not inserted and after_key is not None and key == after_key:
            output[new_key] = new_value
            inserted = True
    if not inserted:
        output[new_key] = new_value
    dct.clear()
    for key, value in output.items():
        dct[key] = value


def safe_merge_dicts(a: Dict[Any, Any], b: Dict[Any, Any]) -> Dict[Any, Any]:
    """Merges two dictionaries into one. If duplicate keys are detected a ValueError is raised."""
    c = deepcopy(a)
    for key in b:
        if key not in c:
            c[key] = b[key]
        else:
            raise ValueError('Duplicate key found when merging dictionaries: {0}'.format(key))
    return c


def fields_subset(subset, fields):
    retained_fields = {}
    allowed_options = ['fields']
    for key, val in subset.items():
        for option in val:
            if option not in allowed_options:
                raise ValueError('Unsupported option found in subset: {}'.format(option))
        # A missing fields key is shorthand for including all subfields
        if 'fields' not in val or val['fields'] == '*':
            retained_fields[key] = fields[key]
        elif isinstance(val['fields'], dict):
            # Copy the full field over so we get all the options, then replace the 'fields' with the right subset
            retained_fields[key] = fields[key]
            retained_fields[key]['fields'] = fields_subset(val['fields'], fields[key]['fields'])
    return retained_fields


def yaml_ordereddict(dumper, data):
    # YAML representation of an OrderedDict will be like a dictionary, but
    # respecting the order of the dictionary.
    # Almost sure it's unndecessary with Python 3.
    value = []
    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        value.append((node_key, node_value))
    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


yaml.add_representer(OrderedDict, yaml_ordereddict)


def dict_clean_string_values(dict: Dict[Any, Any]) -> None:
    """Remove superfluous spacing in all field values of a dict"""
    for key in dict:
        value = dict[key]
        if isinstance(value, str):
            dict[key] = value.strip()


# File helpers


YAML_EXT = {'yml', 'yaml'}


def is_yaml(path: str) -> bool:
    """Returns True if path matches an element of the yaml extensions set"""
    return set(path.split('.')[1:]).intersection(YAML_EXT) != set()


def safe_list(o: Union[str, List[str]]) -> List[str]:
    """converts o to a list if it isn't already a list"""
    if isinstance(o, list):
        return o
    else:
        return o.split(',')


def glob_yaml_files(paths: List[str]) -> List[str]:
    """Accepts string, or list representing a path, wildcard or folder. Returns list of matched yaml files"""
    all_files: List[str] = []
    for path in safe_list(paths):
        if is_yaml(path):
            all_files.extend(glob.glob(path))
        else:
            for t in YAML_EXT:
                all_files.extend(glob.glob(os.path.join(path, '*.' + t)))
    return sorted(all_files)


def get_tree_by_ref(ref: str) -> git.objects.tree.Tree:
    repo: git.repo.base.Repo = git.Repo(os.getcwd())
    commit: git.objects.commit.Commit = repo.commit(ref)
    return commit.tree


def path_exists_in_git_tree(tree: git.objects.tree.Tree, file_path: str) -> bool:
    try:
        _ = tree[file_path]
    except KeyError:
        return False
    return True


def usage_doc_files() -> List[str]:
    usage_docs_dir: str = os.path.join(os.path.dirname(__file__), '../../docs/fields/usage')
    usage_docs_path: pathlib.PosixPath = pathlib.Path(usage_docs_dir)
    if usage_docs_path.is_dir():
        return [x.name for x in usage_docs_path.glob('*.asciidoc') if x.is_file()]
    return []


def ecs_files() -> List[str]:
    """Return the schema file list to load"""
    schema_glob: str = os.path.join(os.path.dirname(__file__), '../../schemas/*.yml')
    return sorted(glob.glob(schema_glob))


def make_dirs(path: str) -> None:
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print('Unable to create output directory: {}'.format(e))
        raise e


def yaml_dump(
    filename: str,
    data: Dict[str, FieldNestedEntry],
    preamble: Optional[str] = None
) -> None:
    with open(filename, 'w') as outfile:
        if preamble:
            outfile.write(preamble)
        yaml.dump(data, outfile, default_flow_style=False)


def yaml_load(filename: str) -> Set[str]:
    with open(filename) as f:
        return yaml.safe_load(f.read())

# List helpers


def list_subtract(original: List[Any], subtracted: List[Any]) -> List[Any]:
    """Subtract two lists. original = subtracted"""
    return [item for item in original if item not in subtracted]


def list_extract_keys(lst: List[Field], key_name: str) -> List[str]:
    """Returns an array of values for 'key_name', from a list of dictionaries"""
    acc = []
    for d in lst:
        acc.append(d[key_name])
    return acc


# Helpers for the deeply nested fields structure


def is_intermediate(field: FieldEntry) -> bool:
    """Encapsulates the check to see if a field is an intermediate field or a "real" field."""
    return ('intermediate' in field['field_details'] and field['field_details']['intermediate'])


def remove_top_level_reusable_false(ecs_nested: Dict[str, FieldNestedEntry]) -> Dict[str, FieldNestedEntry]:
    """Returns same structure as ecs_nested, but skips all field sets with reusable.top_level: False"""
    components: Dict[str, FieldNestedEntry] = {}
    for (fieldset_name, fieldset) in ecs_nested.items():
        if fieldset.get('reusable', None):
            if not fieldset['reusable']['top_level']:
                continue
        components[fieldset_name] = fieldset
    return components


# Warning helper


def strict_warning(msg: str) -> None:
    """Call warnings.warn(msg) for operations that would throw an Exception
       if operating in `--strict` mode. Allows a custom message to be passed.

    :param msg: custom text which will be displayed with wrapped boilerplate
                for strict warning messages.
    """
    warn_message: str = f"{msg}\n\nThis will cause an exception when running in strict mode.\nWarning check:"
    warnings.warn(warn_message, stacklevel=3)
