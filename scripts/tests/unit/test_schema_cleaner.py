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
                'schema_details': {},
                'field_details': {
                    'name': 'process',
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

    def test_field_visitor(self):
        def print_field_details(field, path):
            if 'name' in field['field_details']:
                print("{} (from {})".format(field['field_details']['name'], path))
        print('')
        schemas = self.schema_process()
        cleaner.visit_fields(schemas, field_func=print_field_details)
