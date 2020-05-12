import os
import pprint
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from schema import cleaner

class TestSchemaCleaner(unittest.TestCase):


    def setUp(self):
        self.maxDiff = None


    def schema_process(self):
        return {
            'process': {
                'schema_details': { 'title': 'Process' },
                'field_details': {
                    'name': 'process',
                    'description': 'Process details',
                    'type': 'group'
                },
                'fields': {
                    'pid': {
                        'field_details': {
                            'name': 'pid',
                            'type': 'keyword',
                            'description': 'The process ID',
                            'level': 'core'
                        }
                    },
                    'parent': {
                        'field_details': {
                            'name': 'parent',
                            'type': 'object'
                        },
                        'fields': {
                            'pid': {
                                'field_details': {
                                    'name': 'parent.pid',
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
                }
            }
        }


    # schemas


    def test_schema_raises_on_missing_required_attributes(self):
        schema = self.schema_process()['process']
        schema['schema_details'].pop('title')
        with self.assertRaisesRegex(ValueError, 'mandatory attributes: title'):
            cleaner.schema_cleanup(schema)

        schema = self.schema_process()['process']
        schema['field_details'].pop('description')
        with self.assertRaisesRegex(ValueError, 'mandatory attributes: description'):
            cleaner.schema_cleanup(schema)


    def test_schema_simple_cleanup(self):
        my_schema = {
            'schema_details': {
                'title': "My Schema\n",
                'type': "group\n ",
                'group': 2,
                'root': False
            },
            'field_details': {
                'name': 'my_schema',
                'short': " a really short description\n\n",
                'description': "\ta long\n\nmultiline description   ",
            }
        }
        cleaner.schema_cleanup(my_schema)
        self.assertEqual(my_schema['schema_details']['title'], 'My Schema')
        self.assertEqual(my_schema['field_details']['type'], 'group')
        self.assertEqual(my_schema['field_details']['short'], 'a really short description')
        self.assertEqual(my_schema['field_details']['description'], "a long\n\nmultiline description")


    def test_schema_cleanup_setting_defaults(self):
        my_schema = {
            'schema_details': {
                'title': 'My Schema'
            },
            'field_details': {
                'name': 'my_schema',
                'description': "a nice description   ",
            }
        }
        cleaner.schema_cleanup(my_schema)
        self.assertEqual(my_schema['schema_details']['root'], False)
        self.assertEqual(my_schema['schema_details']['group'], 2)
        self.assertEqual(my_schema['schema_details']['prefix'], 'my_schema.')
        self.assertEqual(my_schema['field_details']['type'], 'group')
        self.assertEqual(my_schema['field_details']['short'], 'a nice description')


    # fields


    def test_field_raises_on_missing_required_attributes(self):
        for missing_attribute in ['name', 'description', 'type', 'level']:
            field = self.schema_process()['process']['fields']['pid']
            field['field_details'].pop(missing_attribute)
            with self.assertRaisesRegex(ValueError,
                    "mandatory attributes: {}".format(missing_attribute)):
                cleaner.field_mandatory_attributes(field)


    def test_field_simple_cleanup(self):
        my_field = {
            'field_details': {
                'name': "my_field\t",
                'type': 'keyword',
                'level': 'core',
                'short': " a really short description\n\n",
                'description': "\ta long\n\nmultiline description   ",
            }
        }
        cleaner.field_cleanup(my_field, [])
        self.assertEqual(my_field['field_details']['name'], 'my_field')
        self.assertEqual(my_field['field_details']['short'], 'a really short description')
        self.assertEqual(my_field['field_details']['description'], "a long\n\nmultiline description")

    def test_field_defaults(self):
        field_min_details = {
            'description': 'description',
            'level': 'extended',
            'name': 'my_field',
            'type': 'unknown',
        }
        # Note: unknown datatypes simply don't have defaults (for future proofing)
        field_details = field_min_details.copy()
        cleaner.field_defaults({'field_details': field_details})
        self.assertEqual(field_details['short'], field_details['description'])
        self.assertEqual(field_details['normalize'], [])

        field_details = {**field_min_details, **{'type': 'keyword'}}
        cleaner.field_defaults({'field_details': field_details})
        self.assertEqual(field_details['ignore_above'], 1024)

        field_details = {**field_min_details, **{'type': 'text'}}
        cleaner.field_defaults({'field_details': field_details})
        self.assertEqual(field_details['norms'], False)

        field_details = {**field_min_details, **{'index': True}}
        cleaner.field_defaults({'field_details': field_details})
        self.assertNotIn('doc_values', field_details)

        field_details = {**field_min_details, **{'index': False}}
        cleaner.field_defaults({'field_details': field_details})
        self.assertEqual(field_details['doc_values'], False)


    def test_field_defaults_dont_override(self):
        field_details = {
            'description': 'description',
            'level': 'extended',
            'name': 'my_long_field',
            'type': 'keyword',
            'ignore_above': 8000,
        }
        cleaner.field_defaults({'field_details': field_details})
        self.assertEqual(field_details['ignore_above'], 8000)


    def test_field_cleanup(self):
        schema = self.schema_process()


    # common to schemas and fields


    def test_clean(self):
        '''A high level sanity test'''
        fields = self.schema_process()
        cleaner.clean(fields)
        self.assertEqual(fields['process']['schema_details']['prefix'], 'process.')


    def test_multiline_short_description_raises(self):
        schema = {'field_details': {
            'name': 'fake_schema',
            'short': "multiple\nlines"}}
        with self.assertRaisesRegex(ValueError, 'single line'):
            cleaner.single_line_short_description(schema)


