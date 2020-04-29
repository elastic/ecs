import os
# import pprint
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts import schema_reader


class TestSchemaReader(unittest.TestCase):

    def schema_with(self, additionals = {}):
        minimal_schema = {
            'name': 'myschema',
            'description': 'my schema description',
        }
        return {**minimal_schema, **additionals}

    def test_load_schemas_with_empty_list_loads_nothing(self):
        result = schema_reader.load_schemas([])
        self.assertEqual(result, ({}))

    # schemas

    def test_schema_all_the_defaults(self):
        schema = {
            'name': 'myschema',
            'description': 'my schema description',
        }
        expected = {
            'name': 'myschema',
            'description': 'my schema description',
            'short': 'my schema description',
            'group': 2,
            'type': 'group',
            'root': False,
            'prefix': 'myschema.',
            'reusable': {
                'top_level': True,
                'expected': []
            }
        }
        schema_reader.schema_explicit_defaults(schema)
        self.assertEqual(schema, expected)


    def test_schema_defaults_prefix_for_root_schema(self):
        schema = self.schema_with({'root': True})
        schema_reader.schema_explicit_defaults(schema)
        self.assertEqual(schema['prefix'], '')


    def test_schema_defaults_no_overwrite(self):
        schema = self.schema_with({
            'group': 1,
            'short': 'something shorter',
            'description': 'something longer',
            'reusable': {
                'top_level': False,
                'expected': ['destination']
            }
        })
        schema_reader.schema_explicit_defaults(schema)
        self.assertEqual(schema['group'], 1)
        self.assertEqual(schema['short'], 'something shorter')
        self.assertFalse(schema['reusable']['top_level'])
        self.assertEqual(schema['reusable']['expected'], ['destination'])


    # field definitions


    def test_field_all_the_defaults(self):
        field = { 'name': 'a_field', 'description': 'a field', 'type': 'faketype' }
        schema_reader.field_explicit_defaults(field, 'fieldset.')
        self.assertEqual(field['flat_name'], 'fieldset.a_field')
        self.assertEqual(field['dashed_name'], 'fieldset-a-field')
        self.assertEqual(field['short'], 'a field')
        self.assertEqual(field['normalize'], [])
        self.assertEqual(field['type'], 'faketype')
        # Special treatment for some types, but we don't touch the type specified


    def test_multi_field_explicit_defaults_with_name(self):
        field = {
            'name': 'myfield',
            'flat_name': 'myfieldset.myfield',
            'multi_fields': [
                    {'type': 'text', 'name': 'special_mf_name'}
            ]
        }
        schema_reader.multi_field_explicit_defaults(field)
        multi_field = field['multi_fields'][0]
        self.assertEqual(multi_field['flat_name'], 'myfieldset.myfield.special_mf_name')


    def test_multi_field_explicit_defaults_missing_name(self):
        field = {
            'name': 'myfield',
            'flat_name': 'myfieldset.myfield',
            'multi_fields': [
                    {'type': 'text'}
            ]
        }
        schema_reader.multi_field_explicit_defaults(field)
        expected = {
            'name': 'myfield',
            'flat_name': 'myfieldset.myfield',
            'multi_fields': [{
                    'name': 'text',
                    'type': 'text',
                    'norms': False,
                    'flat_name': 'myfieldset.myfield.text',
            }]
        }
        self.assertEqual(field, expected)

    # nesting stuff


    def test_nest_fields(self):
        process_fields = [
            { 'name': 'pid' },
            { 'name': 'parent.pid' },
        ]
        expected_nested_fields = {
            'fields': {
                'pid': {
                    'field_details': { 'name': 'pid' }
                },
                'parent': {
                    'fields': {
                        'pid': {
                            'field_details': { 'name': 'parent.pid' }
                        }
                    }
                }
            }
        }
        nested_process_fields = schema_reader.nest_fields(process_fields)
        self.assertEqual(nested_process_fields, expected_nested_fields)


    def test_deep_nesting_representation(self):
        base_schema = self.schema_with({
            'name': 'base',
            'root': True,
            'fields': [
                { 'name': 'message', 'type': 'keyword', 'description': '...' }
            ]
        })
        process_schema = self.schema_with({
            'name': 'process',
            'fields': [
                { 'name': 'pid', 'type': 'keyword', 'description': '...' },
                { 'name': 'parent.pid', 'type': 'keyword', 'description': '...' }
            ]
        })
        schemas = { 'base': base_schema, 'process': process_schema }
        schema_reader.make_defaults_explicit(schemas)
        deeply_nested = schema_reader.deep_nesting_representation(schemas)

        # print('Flat explicit')
        # pprint.pprint(schemas)
        # print('Nested')
        # pprint.pprint(deeply_nested)

        base = deeply_nested['base']
        self.assertEqual(sorted(base.keys()),
                         ['field_details', 'fields', 'schema_details'])
        self.assertTrue(base['schema_details']['root'])
        self.assertEqual(base['schema_details']['prefix'], '')

        process = deeply_nested['process']
        self.assertEqual(sorted(process.keys()),
                         ['field_details', 'fields', 'schema_details'])
        self.assertFalse(process['schema_details']['root'])
        self.assertEqual(process['schema_details']['prefix'], 'process.')

        message = deeply_nested['base']['fields']['message']
        self.assertEqual(sorted(message.keys()), ['field_details'])
        self.assertEqual(message['field_details']['flat_name'], 'message')

        pid = deeply_nested['process']['fields']['pid']
        self.assertEqual(sorted(pid.keys()), ['field_details'])
        self.assertEqual(pid['field_details']['name'], 'pid')
        self.assertEqual(pid['field_details']['flat_name'], 'process.pid')
        self.assertEqual(pid['field_details']['dashed_name'], 'process-pid')


if __name__ == '__main__':
    unittest.main()
