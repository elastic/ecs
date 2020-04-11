import sys
import yaml

from os.path import join, exists
from generators import ecs_helpers

field_type_to_protobuf_type = {
    'boolean':    'bool',
    'date':       'string',
    'float':      'float',
    'geo_point':  'string',
    'integer':    'int32',
    'ip':         'string',
    'keyword':    'string',
    'long':       'int64',
    'object':     'map <string, string>',
    'text':       'string',
}


def generate(ecs_flat, ecs_version, out_dir):
    current_fields = parse_flat_fields(ecs_flat)
    cached_file    = join(out_dir, 'protobuf', 'cached-fields.yaml')
    proto_file     = join(out_dir, 'protobuf', 'ecs.proto')
    cached_fields  = load_cached_fields(cached_file)

    sync_current_fields_with_cached_fields(current_fields, cached_fields)
    write_cached_fields(cached_file, current_fields)
    write_proto(proto_file, current_fields)


def parse_flat_fields(flat_fields):
    fields = {}

    for flat_name in sorted(flat_fields):
        flat_field  = flat_fields[flat_name]
        key         = 'timestamp' if flat_name == '@timestamp' else flat_name
        segments    = key.split('.')
        name        = segments.pop()
        scope       = '.'.join(segments)

        if len(segments) > 0:
            parent_name = segments.pop()
            fields.setdefault(scope, {
                'key': scope,
                'name': parent_name,
                'scope': '.'.join(segments),
                'type': camelize(parent_name),
                'deprecated': False,
            })

        fields[key] = {
            'key':         key,
            'name':        name,
            'scope':       scope,
            'type':        field_type_to_protobuf_type[flat_field['type']],
            'deprecated':  False,
        }

    return fields


def load_cached_fields(cached_file):
    if not exists(cached_file):
        return {}

    with open(cached_file) as f:
        return yaml.safe_load(f.read())


def sync_current_fields_with_cached_fields(current_fields, cached_fields):
    current_by_scope = {}
    cached_by_scope  = {}

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
        scoped_cached_fields  = cached_by_scope.get(scope, {})
        next_tag              = len(scoped_cached_fields) + 1

        for key in sorted(scoped_current_fields):
            current_field = scoped_current_fields[key]
            cached_field  = scoped_cached_fields.get(key)

            if cached_field == None:
                tag = next_tag
                next_tag = next_tag + 1
            else:
                tag = cached_field['tag']

            current_field['tag'] = tag

        for key in sorted(scoped_cached_fields):
            current_field = scoped_current_fields.get(key)
            cached_field  = scoped_cached_fields[key]

            if current_field == None:
                if not cached_field['deprecated']:
                    print('marking protobuf field as deprecated: ' + key)
                    cached_field.update({'deprecated': True})
                current_fields[key] = cached_field
            elif current_field['type'] != cached_field['type']:
                print('ERROR: cannot change ' + key + ' from ' + cached_field['type'] + ' to ' + current_field['type'])
                sys.exit(1)


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
        f_name       = field['name']
        f_type       = field['type']
        f_tag        = str(field['tag'])
        f_deprecated = ' [deprecated=true]' if field['deprecated'] else ''

        f.write(spaces + '  ' + f_type + ' ' + f_name + ' = ' + f_tag + f_deprecated + ';\n')

    f.write(spaces + '}\n\n')


def write_proto(proto_file, fields):
    root_message = {}

    for key in sorted(fields):
        field   = fields[key]
        scope   = field['scope']
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
