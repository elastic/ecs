import glob
import yaml
import os
from schema import loader

# This script should be run downstream of the subset filters - it takes
# all ECS and custom fields already loaded by the latter and explicitly
# removes a subset, for example, to simulate impact of future removals


def exclude(fields, exclude_file_globs, out_dir):
    excludes = load_exclude_definitions(exclude_file_globs)

    if excludes:
        fields = exclude_fields(fields, excludes)

    return fields


def pop_field(fields, node_path, path):
    """pops a field from yaml derived dict using path derived from ordered list of nodes"""
    if node_path[0] in fields:
        if len(node_path) == 1:
            print('Removed field {0}'.format(str(fields.pop(node_path[0]).get('field_details').get('flat_name'))))
        else:
            inner_field = node_path.pop(0)
            pop_field(fields[inner_field]['fields'], node_path, path)
    else:
        raise ValueError('--exclude specified, but no field {} found'.format('.'.join([e for e in path])))


def exclude_trace_path(fields, item, path):
    """traverses paths to one or more nodes in a yaml derived dict"""
    for list_item in item:
        node_path = path.copy()
        node_path.append(list_item['name'])
        if not 'fields' in list_item:
            pop_field(fields, node_path, node_path.copy())
        else:
            exclude_trace_path(fields, list_item['fields'], node_path)


def exclude_fields(fields, excludes):
    """Traverses fields and eliminates any field which matches the excludes"""
    if excludes:
        for ex_list in excludes:
            for item in ex_list:
                exclude_trace_path(fields, item['fields'], [item['name']])
    return fields


def load_exclude_definitions(file_globs):
    if not file_globs:
        return []
    excludes = loader.load_definitions(file_globs)
    if not excludes:
        raise ValueError('--exclude specified, but no exclusions found in {}'.format(file_globs))
    return excludes
