import glob
import os
import yaml
import git
import pathlib
import warnings

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


def dict_clean_string_values(dict):
    """Remove superfluous spacing in all field values of a dict"""
    for key in dict:
        value = dict[key]
        if isinstance(value, str):
            dict[key] = value.strip()


# File helpers


YAML_EXT = ('*.yml', '*.yaml')


def get_glob_files(paths, file_types):
    all_files = []
    for path in paths:
        for t in file_types:
            all_files.extend(glob.glob(os.path.join(path, t)))
    return sorted(all_files)


def get_tree_by_ref(ref):
    repo = git.Repo(os.getcwd())
    commit = repo.commit(ref)
    return commit.tree


def path_exists_in_git_tree(tree, file_path):
    try:
        _ = tree[file_path]
    except KeyError:
        return False
    return True


def usage_doc_files():
    usage_docs_dir = os.path.join(os.path.dirname(__file__), '../../docs/fields/usage')
    usage_docs_path = pathlib.Path(usage_docs_dir)
    if usage_docs_path.is_dir():
        return [x.name for x in usage_docs_path.glob('*.asciidoc') if x.is_file()]
    return []


def ecs_files():
    """Return the schema file list to load"""
    schema_glob = os.path.join(os.path.dirname(__file__), '../../schemas/*.yml')
    return sorted(glob.glob(schema_glob))


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


def list_subtract(original, subtracted):
    """Subtract two lists. original = subtracted"""
    return [item for item in original if item not in subtracted]


def list_extract_keys(lst, key_name):
    """Returns an array of values for 'key_name', from a list of dictionaries"""
    acc = []
    for d in lst:
        acc.append(d[key_name])
    return acc


# Helpers for the deeply nested fields structure


def is_intermediate(field):
    """Encapsulates the check to see if a field is an intermediate field or a "real" field."""
    return ('intermediate' in field['field_details'] and field['field_details']['intermediate'])


# Warning helper


def strict_warning(msg):
    """Call warnings.warn(msg) for operations that would throw an Exception
       if operating in `--strict` mode. Allows a custom message to be passed.

    :param msg: custom text which will be displayed with wrapped boilerplate
                for strict warning messages.
    """
    warn_message = f"{msg}\n\nThis will cause an exception when running in strict mode.\nWarning check:"
    warnings.warn(warn_message, stacklevel=3)
