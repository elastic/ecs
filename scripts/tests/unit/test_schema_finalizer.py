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
                            {'full': 'server.user', 'at': 'server', 'as': 'user'},
                            {'full': 'user.target', 'at': 'user', 'as': 'target'},
                            {'full': 'user.effective', 'at': 'user', 'as': 'effective'},
                        ]
                    }
                },
                'field_details': {
                    'name': 'user',
                    'type': 'group',
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


    def schema_server(self):
        return {
            'server': {
                'schema_details': {},
                'field_details': {
                    'name': 'server',
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

    # calculate_final_values


    def test_calculate_final_values_makes_nested_fields_fully_independent(self):
        fields = {**self.schema_user(), **self.schema_server()}
        finalizer.perform_reuse(fields)
        finalizer.calculate_final_values(fields)

    # perform_reuse


    def test_perform_reuse_with_foreign_reuse_and_self_reuse(self):
        fields = {**self.schema_user(), **self.schema_server(), **self.schema_process()}
        # If the test had multiple foreign destinations for user fields, we could compare them instead
        user_fields_identity = id(fields['user']['fields'])
        finalizer.perform_reuse(fields)
        # Expected reuse
        self.assertIn('target', fields['user']['fields'])
        self.assertIn('effective', fields['user']['fields'])
        self.assertIn('user', fields['server']['fields'])
        self.assertIn('parent', fields['process']['fields'])
        # Only foreign reuse copies fields by reference
        self.assertTrue(fields['server']['fields']['user']['referenced_fields'])
        self.assertEqual(id(fields['server']['fields']['user']['fields']), user_fields_identity)
        self.assertNotIn('referenced_fields', fields['user']['fields']['target'])
        # Leaf field sanity checks for reuse
        self.assertIn('name', fields['user']['fields']['target']['fields'])
        self.assertIn('name', fields['user']['fields']['effective']['fields'])
        self.assertIn('name', fields['server']['fields']['user']['fields'])
        self.assertIn('pid', fields['process']['fields']['parent']['fields'])
        # No unexpected cross-nesting
        self.assertNotIn('target', fields['user']['fields']['target']['fields'])
        self.assertNotIn('target', fields['user']['fields']['effective']['fields'])
        self.assertNotIn('target', fields['server']['fields']['user']['fields'])


    # field_group_at_path


    def test_field_group_at_path_root_destination(self):
        all_fields = self.schema_server()
        fields = finalizer.field_group_at_path('server', all_fields)
        self.assertIn('ip', fields.keys(),
                "should return the dictionary of server fields")


    def test_field_group_at_path_find_nested_destination(self):
        all_fields = self.schema_process()
        fields = finalizer.field_group_at_path('process.parent', all_fields)
        self.assertIn('pid', fields.keys(),
                "should return the dictionary of process.parent fields")
        self.assertEqual('parent.pid', fields['pid']['field_details']['name'])


    def test_field_group_at_path_missing_nested_path(self):
        all_fields = self.schema_server()
        with self.assertRaisesRegex(ValueError, "Field server.nonexistent not found"):
            finalizer.field_group_at_path('server.nonexistent', all_fields)


    def test_field_group_at_path_leaf_field_not_field_group(self):
        all_fields = self.schema_server()
        with self.assertRaisesRegex(ValueError, "Field server\.ip \(type ip\) already exists"):
            finalizer.field_group_at_path('server.ip', all_fields)


    def test_field_group_at_path_for_leaf_object_field_creates_the_section(self):
        all_fields = {
            'network': {
                'field_details': {
                    'name': 'network',
                },
                'fields': {
                    'ingress': {
                        'field_details': {
                            'name': 'network.ingress',
                            'type': 'object'
                        }
                    }
                }
            }
        }
        ingress_subfields = finalizer.field_group_at_path('network.ingress', all_fields)
        self.assertEqual(ingress_subfields, {})
        self.assertEqual(all_fields['network']['fields']['ingress']['fields'], {})
