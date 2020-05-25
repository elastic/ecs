import os
import pprint
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from schema import finalizer

class TestSchemaFinalizer(unittest.TestCase):


    def setUp(self):
        self.maxDiff = None


    def schema_process(self):
        return {
            'process': {
                'schema_details': {'title': 'Process'},
                'field_details': {
                    'name': 'process',
                },
                'fields': {
                    'pid': {
                        'field_details': {
                            'name': 'pid',
                        }
                    },
                    'parent': {
                        'field_details': {
                            'name': 'parent',
                            'intermediate': True,
                        },
                        'fields': {
                            'pid': {
                                'field_details': {
                                    'name': 'parent.pid',
                                }
                            }
                        }
                    }
                }
            }
        }


    def schema_user(self):
        return {
            'user': {
                'schema_details': {
                    'reusable':{
                        'top_level': True,
                        'expected': [
                            # TODO
                        ]
                    }
                },
                'field_details': {
                    'name': 'user',
                },
                'fields': {
                    'name': {
                        'field_details': {
                            'name': 'name',
                        }
                    }
                }
            }
        }


    def schema_destination(self):
        return {
            'destination': {
                'schema_details': {},
                'field_details': {
                    'name': 'destination',
                    'type': 'group'
                },
                'fields': {
                    'ip': {
                        'field_details': {
                            'name': 'ip',
                            'type': 'ip'
                        }
                    }
                }
            }
        }


    # def test_nest_at_raises_on_missing_destination(self):
    #     fields = self.schema_destination()
    #     reuse_entry = {
    #             'at': 'destination.missing.parent.field',
    #             'as': 'user',
    #             'full': 'destination.missing.parent.field.user'
    #         }
    #     reused_details = self.schema_user()['user']
    #     with self.assertRaises(ValueError):
    #         finalizer.nest_at(reuse_entry, reused_details, fields)


    def test_find_nested_path(self):
        all_fields = self.schema_process()
        fields = finalizer.field_group_at_path('process.parent', all_fields)
        self.assertIn('pid', fields.keys(),
                "should return the dictionary of process.parent fields")
        self.assertEqual('parent.pid', fields['pid']['field_details']['name'])


    def test_find_path_at_root(self):
        all_fields = self.schema_destination()
        fields = finalizer.field_group_at_path('destination', all_fields)
        self.assertIn('ip', fields.keys(),
                "should return the dictionary of destination fields")


    def test_missing_nested_path(self):
        all_fields = self.schema_destination()
        with self.assertRaisesRegex(ValueError, "Field destination.nonexistent not found"):
            finalizer.field_group_at_path('destination.nonexistent', all_fields)


    def test_leaf_field_not_field_group(self):
        all_fields = self.schema_destination()
        with self.assertRaisesRegex(ValueError, "Field destination.ip is not a field group"):
            finalizer.field_group_at_path('destination.ip', all_fields)
