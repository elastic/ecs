import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts import schema_processor


class TestSchemaProcessor(unittest.TestCase):

    # schemas

    def test_resolve_reusable_shorthands(self):
        reusable_with_shorthand = [
            'destination',
            {'at': 'user', 'as': 'effective'}
        ]
        schema = {
            'name': 'user',
            'reusable': {'top_level': False, 'expected': reusable_with_shorthand}
        }
        schema_processor.resolve_reusable_shorthands(schema)
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
            'reusable': {'top_level': False, 'expected': reusable_with_key_errors}
        }
        with self.assertRaises(ValueError):
            schema_processor.resolve_reusable_shorthands(schema)

    # navigating fields recursively

    def test_print_fields_recursively(self):
        fields = {
            'event': {
                'fields': {
                    'id': { 'field_details': { 'type': 'keyword' } },
                    'type': { 'field_details': { 'type': 'keyword' } }
                }
            }
        }
        expected = {
            'event': {
                'fields': {
                    'id': { 'field_details': {
                        'type': 'keyword',
                        'flat_name': 'event.id'
                    } },
                    'type': { 'field_details': {
                        'type': 'keyword',
                        'flat_name': 'event.type'
                    } }
                }
            }
        }
        def precalculate_field_details(field_nesting, nested):
            nested['flat_name'] = '.'.join(field_nesting)
        schema_processor.recurse_fields(precalculate_field_details, fields)
        self.assertEqual(fields, expected)

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
        flat_fields = schema_processor.flatten_fields(fields, "")
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
        schema_processor.cleanup_fields_recursive(fields, "")
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
        schema_processor.merge_schema_fields(fieldset1, fieldset2)
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
            schema_processor.merge_schema_fields(fieldset1, fieldset2)

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
        schema_processor.duplicate_reusable_fieldsets(fieldset['reusable_fieldset1'], fieldset)
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
            schema_processor.duplicate_reusable_fieldsets(fieldset['reusable_fieldset2'], fieldset)
        schema_processor.duplicate_reusable_fieldsets(fieldset['reusable_fieldset1'], fieldset)
        # Then this should fail because even though test_fieldset.reusable_fieldset1 now exists, test_fieldset.reusable_fieldset1 is not
        # an allowed reusable location (it's the destination of another reusable)
        with self.assertRaises(ValueError):
            schema_processor.duplicate_reusable_fieldsets(fieldset['reusable_fieldset2'], fieldset)

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
        self.assertEqual(schema_processor.find_nestings(field['sub_field']['fields'], 'sub_field.'), expected)


if __name__ == '__main__':
    unittest.main()
