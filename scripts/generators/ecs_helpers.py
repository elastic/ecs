import yaml

from collections import OrderedDict

# Dictionary helpers


def dict_copy_keys_ordered(dict, copied_keys):
    ordered_dict = OrderedDict()
    for key in copied_keys:
        if key in dict:
            ordered_dict[key] = dict[key]
    return ordered_dict


def dict_copy_existing_keys(source, destination, keys):
    for key in keys:
        if key in source:
            destination[key] = source[key]


def dict_sorted_by_keys(dict, sort_keys):
    if not isinstance(sort_keys, list):
        sort_keys = [sort_keys]
    tuples = []
    for key in dict:
        nested = dict[key]

        sort_criteria = []
        for sort_key in sort_keys:
            sort_criteria.append(nested[sort_key])
        sort_criteria.append(nested)
        tuples.append(sort_criteria)

    return list(map(lambda t: t[-1], sorted(tuples)))


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

# File helpers


def yaml_dump(filename, data, preamble=None):
    with open(filename, 'w') as outfile:
        if preamble:
            outfile.write(preamble)
        yaml.dump(data, outfile, default_flow_style=False)
