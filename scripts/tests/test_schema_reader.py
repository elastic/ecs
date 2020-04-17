import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts import schema_reader


class TestSchemaReader(unittest.TestCase):

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

    def test_resolve_reusable_shorthands(self):
        reusable_with_shorthand = [
            'destination',
            {'at': 'user', 'as': 'effective'}
        ]
        schema = {
            'name': 'user',
            'reusable': { 'top_level': False, 'expected': reusable_with_shorthand }
        }
        schema_reader.resolve_reusable_shorthands(schema)
        expected_reusable = [
            {'at': 'destination', 'as': 'user', 'full': 'destination.user'},
            {'at': 'user', 'as': 'effective', 'full': 'user.effective'}
        ]
        self.assertEqual(expected_reusable, schema['reusable']['expected'])

    def test_resolve_reusable_shorthands_raises_when_missing_keys_as_at(self):
        reusable_with_key_errors = [
            {'hat': 'user', 'has': 'effective'}
        ]
        schema = {
            'name': 'user',
            'reusable': { 'top_level': False, 'expected': reusable_with_key_errors }
        }
        with self.assertRaises(ValueError):
            schema_reader.resolve_reusable_shorthands(schema)

    # field definitions

    def test_field_set_defaults_no_short(self):
        field = {'description': 'a field', 'type': 'faketype'}
        schema_reader.field_set_defaults(field)
        self.assertEqual(field, {'description': 'a field', 'short': 'a field', 'type': 'faketype', 'normalize': []})

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
        self.assertEqual(result, ({}))

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
                                    'short': 'A test field',
                                    'normalize': [],
                                    'original_fieldset': 'reusable_fieldset'
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
                                    'short': 'A test field',
                                    'normalize': [],
                                    'original_fieldset': 'reusable_fieldset'
                                }
                            }
                        }
                    }
                }
            }
        }
        self.assertEqual(fields, expected)

    def test_merge_schema_fields(self):
        fieldset1 = {
            'test_fieldset': {
                'name': 'test_fieldset',
                'reusable': {
                    'top_level': False,
                    'expected': ['location1, location2']
                },
                'fields': {
                    'test_field1': {
                        'field_details': {
                            'name': 'test_field1',
                            'type': 'keyword',
                            'description': 'A test field'
                        }
                    },
                    'test_field2': {
                        'field_details': {
                            'name': 'test_field2',
                            'type': 'keyword',
                            'description': 'Another test field'
                        }
                    }
                }
            }
        }
        fieldset2 = {
            'test_fieldset': {
                'name': 'test_fieldset',
                'reusable': {
                    'top_level': True,
                    'expected': ['location3, location4']
                },
                'fields': {
                    'test_field1': {
                        'field_details': {
                            'name': 'test_field1',
                            'type': 'keyword',
                            'description': 'A test field with matching type but custom description'
                        }
                    },
                    'test_field3': {
                        'field_details': {
                            'name': 'test_field3',
                            'type': 'keyword',
                            'description': 'A third test field'
                        }
                    }
                }
            }
        }
        expected = {
            'test_fieldset': {
                'name': 'test_fieldset',
                'reusable': {
                    'top_level': True,
                    'expected': ['location1, location2', 'location3, location4']
                },
                'fields': {
                    'test_field1': {
                        'field_details': {
                            'name': 'test_field1',
                            'type': 'keyword',
                            'description': 'A test field'
                        }
                    },
                    'test_field2': {
                        'field_details': {
                            'name': 'test_field2',
                            'type': 'keyword',
                            'description': 'Another test field'
                        }
                    },
                    'test_field3': {
                        'field_details': {
                            'name': 'test_field3',
                            'type': 'keyword',
                            'description': 'A third test field'
                        }
                    }
                }
            }
        }
        schema_reader.merge_schema_fields(fieldset1, fieldset2)
        self.assertEqual(fieldset1, expected)

    def test_merge_schema_fields_fail(self):
        fieldset1 = {
            'test_fieldset': {
                'name': 'test_fieldset',
                'fields': {
                    'test_field1': {
                        'field_details': {
                            'name': 'test_field1',
                            'type': 'keyword',
                            'description': 'A test field'
                        }
                    }
                }
            }
        }
        fieldset2 = {
            'test_fieldset': {
                'name': 'test_fieldset',
                'fields': {
                    'test_field1': {
                        'field_details': {
                            'name': 'test_field1',
                            'type': 'long',
                            'description': 'A conflicting field'
                        }
                    }
                }
            }
        }
        with self.assertRaises(ValueError):
            schema_reader.merge_schema_fields(fieldset1, fieldset2)

    def test_reusable_dot_notation(self):
        fieldset = {
            'reusable_fieldset1': {
                'name': 'reusable_fieldset1',
                'reusable': {
                    'top_level': False,
                    'expected': [
                        'test_fieldset.sub_field'
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
            },
            'test_fieldset': {
                'name': 'test_fieldset',
                'fields': {
                    'sub_field': {
                        'fields': {}
                    }
                }
            }
        }
        expected = {
            'sub_field': {
                'fields': {
                    'reusable_fieldset1': {
                        'name': 'reusable_fieldset1',
                        'reusable': {
                            'top_level': False,
                            'expected': [
                                {
                                    'at': 'test_fieldset.sub_field',
                                    'as': 'reusable_fieldset1',
                                    'full': 'test_fieldset.sub_field.reusable_fieldset1'
                                }
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
                }
            }
        }
        schema_reader.duplicate_reusable_fieldsets(fieldset['reusable_fieldset1'], fieldset)
        self.assertEqual(fieldset['test_fieldset']['fields'], expected)

    def test_improper_reusable_fails(self):
        fieldset = {
            'reusable_fieldset1': {
                'name': 'reusable_fieldset1',
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
            },
            'reusable_fieldset2': {
                'name': 'reusable_fieldset2',
                'reusable': {
                    'top_level': False,
                    'expected': [
                        'test_fieldset.reusable_fieldset1'
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
            },
            'test_fieldset': {
                'name': 'test_fieldset',
                'fields': {}
            }
        }
        # This should fail because test_fieldset.reusable_fieldset1 doesn't exist yet
        with self.assertRaises(ValueError):
            schema_reader.duplicate_reusable_fieldsets(fieldset['reusable_fieldset2'], fieldset)
        schema_reader.duplicate_reusable_fieldsets(fieldset['reusable_fieldset1'], fieldset)
        # Then this should fail because even though test_fieldset.reusable_fieldset1 now exists, test_fieldset.reusable_fieldset1 is not
        # an allowed reusable location (it's the destination of another reusable)
        with self.assertRaises(ValueError):
            schema_reader.duplicate_reusable_fieldsets(fieldset['reusable_fieldset2'], fieldset)

    def test_find_nestings(self):
        field = {
            'sub_field': {
                'reusable': {
                    'top_level': True,
                    'expected': [
                        'some_other_field'
                    ]
                },
                'fields': {
                    'reusable_fieldset1': {
                        'name': 'reusable_fieldset1',
                        'reusable': {
                            'top_level': False,
                            'expected': [
                                'sub_field'
                            ]
                        },
                        'fields': {
                            'nested_reusable_field': {
                                'reusable': {
                                    'top_level': False,
                                    'expected': 'sub_field.nested_reusable_field'
                                },
                                'field_details': {
                                    'name': 'reusable_field',
                                    'type': 'keyword',
                                    'description': 'A test field'
                                }
                            }
                        }
                    }
                }
            }
        }
        expected = ['sub_field.reusable_fieldset1', 'sub_field.reusable_fieldset1.nested_reusable_field']
        self.assertEqual(schema_reader.find_nestings(field['sub_field']['fields'], 'sub_field.'), expected)


if __name__ == '__main__':
    unittest.main()
