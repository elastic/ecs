import yaml
import os

from collections import OrderedDict
from copy import deepcopy

# Dictionary helpers


def dict_copy_keys_ordered(dct, copied_keys):
    ordered_dict = OrderedDict()
    for key in copied_keys:
        if key in dct:
            ordered_dict[key] = dct[key]
    return ordered_dict


def dict_copy_existing_keys(source, destination, keys):
    for key in keys:
        if key in source:
            destination[key] = source[key]


def dict_sorted_by_keys(dct, sort_keys):
    if not isinstance(sort_keys, list):
        sort_keys = [sort_keys]

    tuples = []

    for key in dct:
        nested = dct[key]

        sort_criteria = []
        for sort_key in sort_keys:
            sort_criteria.append(nested[sort_key])
        sort_criteria.append(nested)
        tuples.append(sort_criteria)

    return list(map(lambda t: t[-1], sorted(tuples)))


def safe_merge_dicts(a, b):
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
    for key, val in subset.items():
        # A missing fields key is shorthand for including all subfields
        if 'fields' not in val or val['fields'] == '*':
            retained_fields[key] = fields[key]
        elif isinstance(val['fields'], dict):
            # Copy the full field over so we get all the options, then replace the 'fields' with the right subset
            retained_fields[key] = fields[key]
            retained_fields[key]['fields'] = fields_subset(val['fields'], fields[key]['fields'])
    return retained_fields


def get_reusable_fields(fields):
    reusable_fields = {}
    for key in fields:
        if 'reusable' in fields[key]:
            reusable_fields[key] = True
        if 'fields' in fields[key]:
            reusable_fields.update(get_reusable_fields(fields[key]['fields']))
    return reusable_fields

def recursive_merge_subset_dicts(a, b):
    for key in b:
        if key not in a:
            a[key] = b[key]
        elif 'fields' not in b[key] or b[key]['fields'] == '*':
            a[key]['fields'] = '*'
        elif isinstance(a[key]['fields'], dict) and isinstance(b[key]['fields'], dict):
            recursive_merge_subset_dicts(a[key]['fields'], b[key]['fields'])



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


def dict_rename_keys(dict, renames):
    for key, value in dict.iteritems():
        if key in renames:
            del dict[key]
            dict[renames[key]] = value


# File helpers

def make_dirs(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as e:
        print('Unable to create output directory: {}'.format(e))
        raise e


def yaml_dump(filename, data, preamble=None):
    with open(filename, 'w') as outfile:
        if preamble:
            outfile.write(preamble)
        yaml.dump(data, outfile, default_flow_style=False)


def yaml_load(filename):
    with open(filename) as f:
        return yaml.safe_load(f.read())

# List helpers


def list_extract_keys(lst, key_name):
    """Returns an array of values for 'key_name', from a list of dictionaries"""
    acc = []
    for d in lst:
        acc.append(d[key_name])
    return acc


def list_split_by(lst, size):
    '''Splits a list in smaller lists of a given size'''
    acc = []
    for i in range(0, len(lst), size):
        acc.append(lst[i:i + size])
    return acc
