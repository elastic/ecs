import os
# import pprint
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from schema import loader


BASE_SCHEMA = {
    'base': {
        'schema_details': { 'root': True },
        'field_details': {
            'name': 'base',
            'type': 'group'
        },
        'fields': {
            'message': {
                'field_details': {
                    'name': 'message',
                    'type': 'keyword'
                }
            }
        }
    }
}

PROCESS_SCHEMA = {
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

class TestSchemaLoader(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None


    def test_load_schemas_no_custom(self):
        fields = loader.load_schemas([])
        self.assertEqual(
                ['field_details', 'fields', 'schema_details'],
                sorted(fields['process'].keys()),
                "Schemas should have 'field_details', 'fields' and 'schema_details' subkeys")
        self.assertEqual(
                ['field_details'],
                list(fields['process']['fields']['pid'].keys()),
                "Leaf fields should have only the 'field_details' subkey")
        self.assertIn(
                'fields',
                fields['process']['fields']['thread'].keys(),
                "Fields containing nested fields should at least have the 'fields' subkey")

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
        nested_process_fields = loader.nest_fields(process_fields)
        self.assertEqual(nested_process_fields, expected_nested_fields)


    def test_deep_nesting_representation(self):
        all_schemas = {
            'base': {
                'name': 'base',
                'root': True,
                'type': 'group',
                'fields': [
                    {'name': 'message', 'type': 'keyword'}
                ]
            },
            'process': {
                'name': 'process',
                'type': 'group',
                'fields': [
                    {'name': 'pid', 'type': 'keyword'},
                    {'name': 'parent.pid', 'type': 'keyword'},
                ]
            }
        }
        deeply_nested = loader.deep_nesting_representation(all_schemas)
        expected_deeply_nested = {
            'base': {
                'schema_details': { 'root': True },
                'field_details': {
                    'name': 'base',
                    'type': 'group'
                },
                'fields': {
                    'message': {
                        'field_details': {
                            'name': 'message',
                            'type': 'keyword'
                        }
                    }
                }
            },
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
        self.assertEqual(deeply_nested, expected_deeply_nested)


    def test_merge_new_schema(self):
        custom = {
            'custom': {
                'schema_details': { },
                'field_details': {
                    'name': 'custom',
                    'type': 'group'
                },
                'fields': {
                    'my_field': {
                        'field_details': {
                            'name': 'my_field',
                            'type': 'keyword'
                        }
                    }
                }
            }
        }
        expected_fields = {**BASE_SCHEMA, **custom}
        merged_fields = loader.merge_custom_fields(BASE_SCHEMA, custom)
        self.assertEqual(expected_fields, merged_fields,
                "New schemas should just be a dictionary merge")


    def test_merge_field_within_schema(self):
        custom = {
            'base': {
                'schema_details': { },
                'field_details': {
                    'name': 'base'
                },
                'fields': {
                    'my_field': {
                        'field_details': {
                            'name': 'my_field',
                            'type': 'keyword'
                        }
                    }
                }
            }
        }
        expected_fields = {
            'base': {
                'schema_details': { 'root': True },
                'field_details': {
                    'name': 'base',
                    'type': 'group'
                },
                'fields': {
                    'message': {
                        'field_details': {
                            'name': 'message',
                            'type': 'keyword'
                        }
                    },
                    'my_field': {
                        'field_details': {
                            'name': 'my_field',
                            'type': 'keyword'
                        }
                    }
                }
            }
        }
        merged_fields = loader.merge_custom_fields(BASE_SCHEMA, custom)
        self.assertEqual(['message', 'my_field'],
                sorted(expected_fields['base']['fields'].keys()))
        self.assertEqual(expected_fields, merged_fields,
                "New fields being merged in existing schemas are merged in the 'fields' dict.")


    def test_merge_leaf_field_and_nested_field(self):
        custom = {
            'base': {
                'schema_details': { },
                'field_details': {
                    'name': 'base'
                },
                'fields': {
                    'message': {
                        'fields': {
                            'subfield': {
                                'name': 'subfield',
                                'type': 'keyword'
                            }
                        }
                    }
                }
            }
        }
        with self.assertRaises(ValueError, msg="Merging leaf field with nested field should fail"):
            loader.merge_custom_fields(BASE_SCHEMA, custom)


    def test_make_schema_reusable(self):
        custom = {
            'base': {
                'schema_details': {
                    'reusable': {
                        'top_level': True,
                        'expected': [ 'foo.bar' ]
                    }
                },
                'field_details': {
                    'name': 'base'
                }
            }
        }
        merged_fields = loader.merge_custom_fields(BASE_SCHEMA, custom)
        expected_fields = {
            'base': {
                'schema_details': {
                    'root': True,
                    'reusable': {
                        'top_level': True,
                        'expected': [ 'foo.bar' ]
                    }
                },
                'field_details': {
                    'name': 'base',
                    'type': 'group'
                },
                'fields': {
                    'message': {
                        'field_details': {
                            'name': 'message',
                            'type': 'keyword'
                        }
                    }
                }
            }
        }
        self.assertEqual(merged_fields, expected_fields)

    # def test_override_schema_reuse_details(self):

    # def test_override_other_schema_attributes_works(self):

    # Not supported yet
    # def test_acceptable_leaf_field_attribute_overrides(self):

    # def test_unacceptable_field_attribute_overrides_raise(self):

    def test_field_with_subfield_mergeable(self):
        custom = {
            'process': {
                'schema_details': { },
                'field_details': {
                    'name': 'process'
                },
                'fields': {
                    'parent': {
                        'fields': {
                            'name': {
                                'field_details': {
                                    'name': 'parent.name',
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
                }
            }
        }
        merged_fields = loader.merge_custom_fields(PROCESS_SCHEMA, custom)
        expected_fields = {
            'process': {
                'schema_details': { },
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
                        'fields': {
                            'pid': {
                                'field_details': {
                                    'name': 'parent.pid',
                                    'type': 'keyword'
                                }
                            },
                            'name': {
                                'field_details': {
                                    'name': 'parent.name',
                                    'type': 'keyword'
                                }
                            }
                        }
                    }
                }
            }
        }
        self.assertEqual(merged_fields, expected_fields)



if __name__ == '__main__':
    unittest.main()
