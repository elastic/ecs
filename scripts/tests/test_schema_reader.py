import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts import schema_reader


class TestSchemaReader(unittest.TestCase):

    # File loading stuff

    # Validation

    # Generic helpers

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
        result = schema_reader.load_schemas([])
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


if __name__ == '__main__':
    unittest.main()
