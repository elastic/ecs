import os
import sys
import unittest
import collections

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts import schema_reader


class TestSchemaReader(unittest.TestCase):

    # File loading stuff

    # Validation

    # Generic helpers
    @classmethod
    def setUpClass(cls):
        # this helps with debugging test failures
        cls.maxDiff = None

    def test_clean_string_values(self):
        dict = {'dirty': ' space, the final frontier  ', 'clean': 'val', 'int': 1}
        schema_reader.dict_clean_string_values(dict)
        self.assertEqual(dict, {'dirty': 'space, the final frontier', 'clean': 'val', 'int': 1})

    # In memory representation

    # schemas

    def test_schema_set_fieldset_prefix_at_root(self):
        schema = {'root': True, 'name': 'myfieldset'}
        schema_reader.schema_set_fieldset_prefix(schema)
        self.assertEqual(schema,
                         {'prefix': '', 'root': True, 'name': 'myfieldset'})

    def test_schema_set_fieldset_prefix_root_unspecified(self):
        schema = {'name': 'myfieldset'}
        schema_reader.schema_set_fieldset_prefix(schema)
        self.assertEqual(schema,
                         {'prefix': 'myfieldset.', 'name': 'myfieldset'})

    def test_schema_set_fieldset_prefix_not_at_root(self):
        schema = {'root': False, 'name': 'myfieldset'}
        schema_reader.schema_set_fieldset_prefix(schema)
        self.assertEqual(schema,
                         {'prefix': 'myfieldset.', 'root': False, 'name': 'myfieldset'})

    def test_set_default_values_defaults(self):
        schema = {'description': '...'}
        schema_reader.schema_set_default_values(schema)
        self.assertEqual(schema, {'group': 2, 'type': 'group', 'description': '...', 'short': '...'})

    def test_set_default_values_no_overwrite(self):
        schema = {'group': 1, 'description': '...'}
        schema_reader.schema_set_default_values(schema)
        self.assertEqual(schema, {'group': 1, 'type': 'group', 'description': '...', 'short': '...'})

    # field definitions

    def test_field_set_defaults_no_short(self):
        field = {'description': 'a field', 'type': 'faketype'}
        schema_reader.field_set_defaults(field)
        self.assertEqual(field, {'description': 'a field', 'short': 'a field', 'type': 'faketype'})

    def test_field_set_multi_field_defaults_missing_name(self):
        field = {
            'name': 'myfield',
            'flat_name': 'myfieldset.myfield',
            'multi_fields': [
                    {'type': 'text'}
            ]
        }
        schema_reader.field_set_multi_field_defaults(field)
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

    def test_load_schemas_with_empty_list_loads_nothing(self):
        result = schema_reader.load_schemas([], False)
        self.assertEqual(result, ({}, {}))

    def test_flatten_fields(self):
        fields = {
            'top_level': {
                'field_details': {
                    'name': 'top_level'
                },
                'fields': {
                    'nested_field': {
                        'field_details': {
                            'name': 'nested_field'
                        },
                        'fields': {
                            'double_nested_field': {
                                'field_details': {
                                    'name': 'double_nested_field'
                                }
                            }
                        }
                    }
                }
            }
        }
        flat_fields = schema_reader.flatten_fields(fields, "")
        expected = {
            'top_level': {
                'name': 'top_level'
            },
            'top_level.nested_field': {
                'name': 'nested_field'
            },
            'top_level.nested_field.double_nested_field': {
                'name': 'double_nested_field'
            }
        }
        self.assertEqual(flat_fields, expected)

    def test_flatten_fields_reusable(self):
        fields = {
            'top_level': {
                'field_details': {
                    'name': 'top_level'
                },
                'fields': {
                    'nested_field': {
                        'reusable': {
                            'top_level': False,
                            'expected': [
                                'top_level'
                            ]
                        },
                        'fields': {
                            'double_nested_field': {
                                'field_details': {
                                    'name': 'double_nested_field'
                                }
                            }
                        }
                    }
                }
            }
        }
        flat_fields = schema_reader.flatten_fields(fields, "")
        expected = {
            'top_level': {
                'name': 'top_level'
            },
            'top_level.nested_field.double_nested_field': {
                'name': 'double_nested_field',
                'original_fieldset': 'nested_field'
            }
        }
        self.assertEqual(flat_fields, expected)

    def test_cleanup_fields_recursive(self):
        """Reuse a fieldset under two other fieldsets and check that the flat names are properly generated."""
        reusable = {
            'name': 'reusable_fieldset',
            'reusable': {
                'top_level': False,
                'expected': [
                    'test_fieldset'
                ]
            },
            'fields': {
                'reusable_field': {
                    'field_details': {
                        'name': 'reusable_field',
                        'type': 'keyword',
                        'description': 'A test field'
                    }
                }
            }
        }
        fields = {
            'base_set1': {
                'name': 'base_set1',
                'fields': {
                    'reusable_fieldset': reusable
                }
            },
            'base_set2': {
                'name': 'base_set2',
                'fields': {
                    'reusable_fieldset': reusable
                }
            }
        }
        schema_reader.cleanup_fields_recursive(fields, "")
        expected = {
            'base_set1': {
                'name': 'base_set1',
                'fields': {
                    'reusable_fieldset': {
                        'name': 'reusable_fieldset',
                        'reusable': {
                            'top_level': False,
                            'expected': [
                                'test_fieldset'
                            ]
                        },
                        'fields': {
                            'reusable_field': {
                                'field_details': {
                                    'name': 'reusable_field',
                                    'type': 'keyword',
                                    'description': 'A test field',
                                    'flat_name': 'base_set1.reusable_fieldset.reusable_field',
                                    'dashed_name': 'base-set1-reusable-fieldset-reusable-field',
                                    'ignore_above': 1024,
                                    'short': 'A test field'
                                }
                            }
                        }
                    }
                }
            },
            'base_set2': {
                'name': 'base_set2',
                'fields': {
                    'reusable_fieldset': {
                        'name': 'reusable_fieldset',
                        'reusable': {
                            'top_level': False,
                            'expected': [
                                'test_fieldset'
                            ]
                        },
                        'fields': {
                            'reusable_field': {
                                'field_details': {
                                    'name': 'reusable_field',
                                    'type': 'keyword',
                                    'description': 'A test field',
                                    'flat_name': 'base_set2.reusable_fieldset.reusable_field',
                                    'dashed_name': 'base-set2-reusable-fieldset-reusable-field',
                                    'ignore_above': 1024,
                                    'short': 'A test field'
                                }
                            }
                        }
                    }
                }
            }
        }
        self.assertEqual(fields, expected)

    def test_schema_fields_as_dict(self):
        """Test that the schema_fields_as_dictionary function correctly converts the schema."""
        host = {
            'fields': [
                {
                    'name': 'os',
                    'fields': [
                        {
                            'name': 'platform'
                        }
                    ],
                },
                {
                    'name': 'ip'
                }
            ]
        }

        exp = {
            'fields': {
                'os': {
                    'field_details': {
                        'name': 'os',
                        'order': 0
                    },
                    'fields': {
                        'platform': {
                            'field_details': {
                                'name': 'platform',
                                'order': 0
                            }
                        }
                    }
                },
                'ip': {
                    'field_details': {
                        'name': 'ip',
                        'order': 1,
                    }
                }
            }
        }
        schema_reader.schema_fields_as_dictionary(host)
        self.assertEqual(host, exp)

    def test_schema_fields_as_dict_no_fields(self):
        """Test that the function does not modify a dictionary without a fields key."""
        no_fields = {
            'name': 'no_fields'
        }
        schema_reader.schema_fields_as_dictionary(no_fields)
        self.assertEqual(no_fields, {'name': 'no_fields'})

    def test_schema_fields_as_dict_dotted_notation(self):
        """Test that the function handles dotted name notation correctly."""
        host = {
            'fields': [
                {
                    'name': 'os.test',
                    'fields': [
                        {
                            'name': 'platform'
                        }
                    ],
                },
                {
                    'name': 'os',
                    'fields': [
                        {
                            'name': 'other_os'
                        }
                    ]
                },
                {
                    'name': 'ip'
                }
            ]
        }

        exp = {
            "fields": {
                "os": {
                    "fields": {
                        "other_os": {
                            "field_details": {
                                "name": "other_os",
                                "order": 0
                            }
                        },
                        "test": {
                            "fields": {
                                "platform": {
                                    "field_details": {
                                        "name": "platform",
                                        "order": 0
                                    }
                                }
                            },
                            "field_details": {
                                "name": "os.test",
                                "order": 0
                            }
                        }
                    },
                    "field_details": {
                        "name": "os",
                        "order": 1
                    }
                },
                "ip": {
                    "field_details": {
                        "name": "ip",
                        "order": 2
                    }
                }
            }
        }
        schema_reader.schema_fields_as_dictionary(host)
        self.assertDictEqual(host, exp)

    def test_merge_dict(self):
        first = {
            'a': {
                'some_field': 1
            }
        }

        sec = {
            'a': {
                'other': 'a'
            },
            'b': 5
        }

        schema_reader.merge_dict_overwrite(first, sec, False)
        exp = {
            'a': {
                'some_field': 1,
                'other': 'a'
            },
            'b': 5
        }
        self.assertDictEqual(first, exp)

    def test_merge_dict_validate(self):
        first = {
            'a': 5
        }

        sec = {
            'a': {
                'some': 'field'
            },
            'b': 5
        }

        with self.assertRaises(schema_reader.SchemaValidationException):
            schema_reader.merge_dict_overwrite(first, sec, True)

    def test_fix_up(self):
        base = {
            'name': 'base',
            'title': 'some title',
            'root': True,
            'short': 'short',
            'description': 'long',
            'type': 'group',
            'group': 2,
            'fields': {
                '@timestamp': {
                    'name': '@timestamp',
                    'type': 'date',
                    'level': 1,
                },
                'message': {
                    'name': 'message',
                    'type': 'text',
                },
            }
        }

        custom = {
            'fields': [
                {
                    'name': '@timestamp',
                    'type': 'date'
                },
                {
                    'name': 'other_field',
                    'fields': [
                        {
                            'name': 'other',
                            'type': 'keyword',
                        }
                    ]
                }
            ]
        }
        fixed = schema_reader.fixup_custom(custom, base)
        self.assertEqual(fixed['other_field']['title'], 'other_field')
        self.assertNotIn('title', fixed['base']['fields'][0])
        # other_field should have a type now
        self.assertEqual(fixed['other_field']['type'], 'group')
        self.assertEqual(fixed['base']['fields'][0]['level'], 1)
        self.assertIn('level', fixed['other_field'])
        self.assertIn('level', fixed['other_field']['fields'][0])


if __name__ == '__main__':
    unittest.main()
