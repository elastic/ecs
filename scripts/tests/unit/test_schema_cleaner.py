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
                            'type': 'keyword'
                        }
                    },
                    'parent': {
                        'field_details': {'type': 'object'},
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


    # schema_cleanup


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


    # def test_field_visitor(self):
    #     def print_field_details(field, path):
    #         if 'name' in field['field_details']:
    #             print("{} (from {})".format(field['field_details']['name'], path))
    #     print('')
    #     schemas = self.schema_process()
    #     cleaner.visit_fields(schemas, field_func=print_field_details)
