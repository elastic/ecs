import sys
import yaml

from os.path import join, exists
from generators import ecs_helpers


field_type_to_protobuf_type = {
    'binary': 'string',
    'boolean': 'bool',
    'byte': 'int32',
    'date_nanos': 'long',
    'date': 'string',
    'double': 'double',
    'float': 'float',
    'geo_point': 'string',
    'half_float': 'float',
    'integer': 'int32',
    'ip': 'string',
    'keyword': 'string',
    'long': 'int64',
    'object': 'map <string, string>',
    'scaled_float': 'double',
    'short': 'int32',
    'text': 'string',
}


protobuf_legal_type_changes_for = {
    'int32': ['int32', 'uint32', 'int64', 'uint64', 'bool'],
    'uint32': ['int32', 'uint32', 'int64', 'uint64', 'bool'],
    'int64': ['int32', 'uint32', 'int64', 'uint64', 'bool'],
    'uint64': ['int32', 'uint32', 'int64', 'uint64', 'bool'],
    'bool': ['int32', 'uint32', 'int64', 'uint64', 'bool'],
    'sint32': ['sint32', 'sint64'],
    'sint64': ['sint32', 'sint64'],
    'fixed32': ['fixed32', 'sfixed32'],
    'fixed64': ['fixed64', 'sfixed64'],
    'enum': ['enum', 'int32', 'uint32', 'int64', 'uint64'],
}


valid_normalize_settings = [
    [],
    ['array'],
]


def generate(ecs_flat, ecs_version, out_dir):
    current_fields = parse_flat_fields(ecs_flat)
    cached_file = join(out_dir, 'protobuf', 'cached-fields.yaml')
    proto_file = join(out_dir, 'protobuf', 'ecs.proto')
    cached_fields = load_cached_fields(cached_file)

    sync_current_fields_with_cached_fields(current_fields, cached_fields)
    write_cached_fields(cached_file, current_fields)
    write_proto(proto_file, current_fields)


def parse_flat_fields(flat_fields):
    fields = {}

    for flat_name in sorted(flat_fields):
        flat_field = flat_fields[flat_name]
        key = 'timestamp' if flat_name == '@timestamp' else flat_name
        segments = key.split('.')
        name = segments.pop()
        scope = '.'.join(segments)
        type = field_type_to_protobuf_type[flat_field['type']]
        normalize = flat_field['normalize']

        if normalize not in valid_normalize_settings:
            print('Don\'t know how to handle {}\'s normalize setting: {}'.format(name, normalize))
            sys.exit(1)

        while len(segments) > 0:
            parent_key = '.'.join(segments)
            parent_name = segments.pop()
            parent_scope = '.'.join(segments)

            fields[parent_key] = {
                'key': parent_key,
                'name': parent_name,
                'scope': parent_scope,
                'type': camelize(parent_name),
                'deprecated': False,
            }

        if normalize == ['array']:
            type = 'repeated ' + type

        fields.setdefault(key, {
            'key': key,
            'name': name,
            'scope': scope,
            'type': type,
            'deprecated': False,
        })

    for key in fields:
        if fields[key]['type'].startswith('repeated map'):
            print('repeated map is not a valid protobuf type for ' + key)
            sys.exit(1)

    return fields


def load_cached_fields(cached_file):
    if not exists(cached_file):
        return {}

    with open(cached_file) as f:
        return yaml.safe_load(f.read())


def sync_current_fields_with_cached_fields(current_fields, cached_fields):
    current_by_scope = {}
    cached_by_scope = {}

    for field in current_fields.values():
        scope = field['scope']
        current_by_scope.setdefault(scope, {})
        current_by_scope[scope][field['key']] = field

    for field in cached_fields.values():
        scope = field['scope']
        cached_by_scope.setdefault(scope, {})
        cached_by_scope[scope][field['key']] = field

    scopes = set(list(current_by_scope.keys()) + list(cached_by_scope.keys()))

    for scope in sorted(scopes):
        scoped_current_fields = current_by_scope.get(scope, {})
        scoped_cached_fields = cached_by_scope.get(scope, {})
        next_tag = len(scoped_cached_fields) + 1

        for key in sorted(scoped_current_fields):
            current_field = scoped_current_fields[key]
            cached_field = scoped_cached_fields.get(key)

            if cached_field == None:
                tag = next_tag
                next_tag = next_tag + 1
            else:
                current_type = current_field['type']
                cached_type = cached_field['type']
                type_mismatch = current_type != cached_type
                valid_type_change = current_type in protobuf_legal_type_changes_for.get(cached_type, [])

                if type_mismatch and not valid_type_change:
                    old_key = cached_field['key']
                    new_name = 'deprecated_' + cached_field['name'] + '_' + str(cached_field['tag'])
                    new_key = scope + '.' + new_name
                    cached_field.update({'key': new_key, 'name': new_name, 'deprecated': True})
                    current_fields[new_key] = cached_field
                    tag = next_tag
                    next_tag = next_tag + 1
                    print('Cannot change {} from {} to {}. The {} version will be renamed to {}'.format(
                        old_key, cached_type, current_type, cached_type, new_key))
                else:
                    tag = cached_field['tag']

            current_field['tag'] = tag

        for key in sorted(scoped_cached_fields):
            current_field = scoped_current_fields.get(key)
            cached_field = scoped_cached_fields[key]

            if current_field == None:
                if not cached_field['deprecated']:
                    print('marking protobuf field as deprecated: ' + key)
                    cached_field.update({'deprecated': True})
                current_fields[key] = cached_field


def write_cached_fields(cached_file, fields):
    with open(cached_file, 'w') as f:
        yaml.dump(fields, f, default_flow_style=False)


def camelize(string):
    return ''.join([item.capitalize() for item in string.split('_')])


def write_proto_message(f, message_name, message, indent=0):
    spaces = ' ' * indent * 2

    f.write(spaces + 'message ' + message_name + ' {\n')

    for nested_key in sorted(message):
        if nested_key == '__fields__':
            continue
        nested_name = camelize(nested_key)
        write_proto_message(f, nested_name, message[nested_key], indent + 1)

    for field in message.get('__fields__', []):
        f_name = field['name']
        f_type = field['type']
        f_tag = str(field['tag'])
        f_deprecated = ' [deprecated=true]' if field['deprecated'] else ''

        f.write(spaces + '  ' + f_type + ' ' + f_name + ' = ' + f_tag + f_deprecated + ';\n')

    f.write(spaces + '}\n\n')


def write_proto(proto_file, fields):
    root_message = {}

    for key in sorted(fields, key=lambda k: (fields[k]['scope'], fields[k]['tag'])):
        field = fields[key]
        scope = field['scope']
        message = root_message

        if scope != '':
            for name in scope.split('.'):
                message.setdefault(name, {})
                message = message[name]

        message.setdefault('__fields__', [])
        message['__fields__'].append(field)

    with open(proto_file, 'w') as f:
        f.write('syntax = "proto3";\n\n')
        f.write('package ecs;\n\n')
        write_proto_message(f, 'Document', root_message)
