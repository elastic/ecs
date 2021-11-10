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

from schema import loader

# This script should be run downstream of the subset filters - it takes
# all ECS and custom fields already loaded by the latter and explicitly
# removes a subset, for example, to simulate impact of future removals


def exclude(fields, exclude_file_globs):
    excludes = load_exclude_definitions(exclude_file_globs)

    if excludes:
        fields = exclude_fields(fields, excludes)

    return fields


def long_path(path_as_list):
    return '.'.join([e for e in path_as_list])


def pop_field(fields, node_path, path, removed):
    """pops a field from yaml derived dict using path derived from ordered list of nodes"""
    if node_path[0] in fields:
        if len(node_path) == 1:
            flat_name = long_path(path)
            fields.pop(node_path[0])
            return flat_name
        else:
            inner_field = node_path.pop(0)
            if 'fields' in fields[inner_field]:
                popped = pop_field(fields[inner_field]['fields'], node_path, path, removed)
                # if object field with no remaining fields and not 'base', pop it
                if fields[inner_field]['fields'] == {} and inner_field != 'base':
                    fields.pop(inner_field)
                return popped
            else:
                raise ValueError(
                    '--exclude specified, but no path to field {} found'.format(long_path(path)))
    else:
        this_long_path = long_path(path)
        # Check in case already removed parent
        if not any([this_long_path.startswith(long_path) for long_path in removed if long_path != None]):
            raise ValueError('--exclude specified, but no field {} found'.format(this_long_path))


def exclude_trace_path(fields, item, path, removed):
    """traverses paths to one or more nodes in a yaml derived dict"""
    for list_item in item:
        node_path = path.copy()
        # cater for name.with.dots
        for name in list_item['name'].split('.'):
            node_path.append(name)
        if not 'fields' in list_item:
            parent = node_path[0]
            removed.append(pop_field(fields, node_path, node_path.copy(), removed))
            # if parent field has no remaining fields and not 'base', pop it
            if parent != 'base' and parent in fields and len(fields[parent]['fields']) == 0:
                fields.pop(parent)
        else:
            raise ValueError('--exclude specified, can\'t parse fields in file {}'.format(item))


def exclude_fields(fields, excludes):
    """Traverses fields and eliminates any field which matches the excludes"""
    if excludes:
        for ex_list in excludes:
            for item in ex_list:
                exclude_trace_path(fields, item['fields'], [item['name']], [])
    return fields


def load_exclude_definitions(file_globs):
    if not file_globs:
        return []
    excludes = loader.load_definitions(file_globs)
    if not excludes:
        raise ValueError('--exclude specified, but no exclusions found in {}'.format(file_globs))
    return excludes
