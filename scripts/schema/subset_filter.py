import glob
import yaml

# This script takes all ECS and custom fields already loaded, and lets users
# filter out the ones they don't need.


def filter(fields, subset_file_globs):
    '''
    Takes the deeply nested field structure and the subset file names.

    It returns a copy of the fields that matches the whitelist defined in the subset.
    '''
    if not subset_file_globs or subset_file_globs == []:
        return fields
    subset_definitions = load_subset_definitions(subset_file_globs)
    filtered_fields = extract_matching_fields(fields, subset_definitions)
    return filtered_fields


def load_subset_definitions(file_globs):
    subsets = {}
    for f in eval_globs(file_globs):
        raw = load_yaml_file(f)
        merge_subsets(subsets, raw)
    if not subsets:
        raise ValueError('--subset specified, but no subsets found in {}'.format(file_globs))
    return subsets


def load_yaml_file(f):
    return yaml.safe_load(f.read())


def eval_globs(globs):
    '''Accepts an array of glob patterns or file names, returns the array of actual files'''
    all_files = []
    for g in globs:
        new_files = glob.glob(g)
        if len(new_files) == 0:
            warn("{} did not match any files".format(g))
        else:
            all_files.extend(new_files)
    return all_files


# You know, for silent tests
def warn(message):
    print(message)


def merge_subsets(a, b):
    '''Merges field subset definitions together. The b subset is merged into the a subset.'''
    for key in b:
        if key not in a:
            a[key] = b[key]
        elif 'fields' not in a[key] or 'fields' not in b[key] or b[key]['fields'] == '*':
            a[key]['fields'] = '*'
        elif isinstance(a[key]['fields'], dict) and isinstance(b[key]['fields'], dict):
            merge_subsets(a[key]['fields'], b[key]['fields'])


def extract_matching_fields(fields, subset_definitions):
    retained_fields = {}
    allowed_options = ['fields']
    for key, val in subset_definitions.items():
        for option in val:
            if option not in allowed_options:
                raise ValueError('Unsupported option found in subset: {}'.format(option))
        # A missing fields key is shorthand for including all subfields
        if 'fields' not in val or val['fields'] == '*':
            retained_fields[key] = fields[key]
        elif isinstance(val['fields'], dict):
            # Copy the full field over so we get all the options, then replace the 'fields' with the right subset
            retained_fields[key] = fields[key]
            retained_fields[key]['fields'] = extract_matching_fields(fields[key]['fields'], val['fields'])
    return retained_fields
