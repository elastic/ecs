import mock
import os
import pprint
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from schema import loader


class TestSchemaLoader(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None


    # Pseudo-fixtures

    def schema_base(self):
        return {
            'base': {
                'schema_details': {'root': True},
                'field_details': {'name': 'base', 'type': 'group'},
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

    # Schema loading

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


    @mock.patch('schema.loader.read_schema_file')
    def test_load_schemas_fail_on_accidental_fieldset_redefinition(self, mock_read_schema):
        mock_read_schema.side_effect = [
            {
                'file': {
                    'name': 'file',
                    'type': 'keyword'
                }
            },
            {
                'file': {
                    'name': 'file',
                    'type': 'text'
                }
            }
        ]
        with self.assertRaises(ValueError):
            loader.load_schema_files(['a.yml', 'b.yml'])

    @mock.patch('schema.loader.read_schema_file')
    def test_load_schemas_allows_unique_fieldsets(self, mock_read_schema):
        file_map = {
            'file': {
                'name': 'file',
                'type': 'keyword'
            }
        }
        host_map = {
            'host': {
                'name': 'host',
                'type': 'text'
            }
        }
        mock_read_schema.side_effect = [file_map, host_map]
        exp = {
            'file': file_map['file'],
            'host': host_map['host']
        }
        res = loader.load_schema_files(['a.yml', 'b.yml'])
        self.assertEqual(res, exp)

    def test_nest_schema_raises_on_missing_schema_name(self):
        with self.assertRaisesRegex(ValueError, 'incomplete.yml'):
            loader.nest_schema([{'description':'just a description'}], 'incomplete.yml')

    # nesting stuff


    def test_nest_fields(self):
        process_fields = [
            {'name': 'pid' },
            {'name': 'parent.pid'},
        ]
        expected_nested_fields = {
            'fields': {
                'pid': {
                    'field_details': {
                        'name': 'pid',
                        'leaf_name': 'pid',
                    }
                },
                'parent': {
                    'field_details': {
                        'name': 'parent',
                        'type': 'object',
                        'intermediate': True,
                    },
                    'fields': {
                        'pid': {
                            'field_details': {
                                'name': 'parent.pid',
                                'leaf_name': 'pid',
                            }
                        }
                    }
                }
            }
        }
        nested_fields = loader.nest_fields(process_fields)
        self.assertEqual(nested_fields, expected_nested_fields)


    def test_nest_fields_recognizes_explicitly_defined_object_fields(self):
        dns_fields = [
            {'name': 'question.name', 'type': 'keyword'},
            {'name': 'answers', 'type': 'object' },
            {'name': 'answers.data', 'type': 'keyword'},
        ]
        expected_nested_fields = {
            'fields': {
                'answers': {
                    'field_details': {
                        'name': 'answers',
                        'leaf_name': 'answers',
                        'type': 'object',
                        'intermediate': False,
                    },
                    'fields': {
                        'data': {
                            'field_details': {
                                'name': 'answers.data',
                                'leaf_name': 'data',
                                'type': 'keyword',
                            }
                        }
                    }
                },
                'question': {
                    'field_details': {
                        'name': 'question',
                        'type': 'object',
                        'intermediate': True,
                    },
                    'fields': {
                        'name': {
                            'field_details': {
                                'name': 'question.name',
                                'leaf_name': 'name',
                                'type': 'keyword',
                            }
                        }
                    }
                }
            }
        }
        nested_fields = loader.nest_fields(dns_fields)
        self.assertEqual(nested_fields, expected_nested_fields)


    def test_nest_fields_multiple_intermediate_fields(self):
        log_fields = [{ 'name': 'origin.file.name' }]
        expected_nested_fields = {
            'fields': {
                'origin': {
                    'field_details': {
                        'name': 'origin',
                        'type': 'object',
                        'intermediate': True,
                    },
                    'fields': {
                        'file': {
                            'field_details': {
                                'name': 'origin.file',
                                'type': 'object',
                                'intermediate': True,
                            },
                            'fields': {
                                'name': {
                                    'field_details': {
                                        'name': 'origin.file.name',
                                        'leaf_name': 'name',
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        nested_log_fields = loader.nest_fields(log_fields)
        self.assertEqual(nested_log_fields, expected_nested_fields)


    def test_deep_nesting_representation(self):
        all_schemas = {
            'base': {
                'name': 'base',
                'title': 'Base',
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
                'schema_details': {
                    'root': True,
                    'title': 'Base',
                },
                'field_details': {
                    'name': 'base',
                    'type': 'group',
                },
                'fields': {
                    'message': {
                        'field_details': {
                            'name': 'message',
                            'leaf_name': 'message',
                            'type': 'keyword',
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
                            'leaf_name': 'pid',
                            'type': 'keyword',
                        }
                    },
                    'parent': {
                        'field_details': {
                            # These are made explicit for intermediate fields
                            'name': 'parent',
                            'type': 'object',
                            'intermediate': True,
                        },
                        'fields': {
                            'pid': {
                                'field_details': {
                                    'name': 'parent.pid',
                                    'leaf_name': 'pid',
                                    'type': 'keyword',
                                }
                            }
                        }
                    }
                }
            }
        }

        process_fields = deeply_nested['process']['fields']
        self.assertEqual(process_fields['parent']['field_details']['intermediate'], True)
        self.assertEqual(deeply_nested, expected_deeply_nested)

    # Merging


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
        expected_fields = {**self.schema_base(), **custom}
        merged_fields = loader.merge_fields(self.schema_base(), custom)
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
        merged_fields = loader.merge_fields(self.schema_base(), custom)
        self.assertEqual(['message', 'my_field'],
                sorted(expected_fields['base']['fields'].keys()))
        self.assertEqual(expected_fields, merged_fields,
                "New fields being merged in existing schemas are merged in the 'fields' dict.")


    def test_fields_with_subfields_mergeable(self):
        custom = {
            'process': {
                'schema_details': { },
                'field_details': {
                    'name': 'process'
                },
                'fields': {
                    'parent': {
                        'field_details': { 'type': 'object' },
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
        merged_fields = loader.merge_fields(self.schema_process(), custom)
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
                        'field_details': { 'type': 'object' },
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


    def test_merge_array_attributes(self):
        # array attributes:
        # - schema/reusable.expected
        # - field/normalize
        ecs = {
            'foo': {
                'schema_details': {
                    'reusable': {
                        'top_level': True,
                        'expected': ['normal.location']
                    }
                },
                'field_details': { 'name': 'foo', 'type': 'group' },
                'fields': {
                    'normalized_field': {
                        'field_details': {
                            'name': 'normalized_field',
                            'type': 'keyword',
                            'normalize': ['lowercase']
                        }
                    },
                    'not_initially_normalized': {
                        'field_details': {
                            'name': 'not_initially_normalized',
                            'type': 'keyword'
                        }
                    }
                }
            }
        }
        custom = {
            'foo': {
                'schema_details': {
                    'reusable': {
                        'expected': ['a_new.location']
                    }
                },
                'field_details': { 'name': 'foo', 'type': 'group' },
                'fields': {
                    'normalized_field': {
                        'field_details': {
                            'name': 'normalized_field',
                            'normalize': ['array']
                        }
                    },
                    'not_initially_normalized': {
                        'field_details': {
                            'name': 'not_initially_normalized',
                            'normalize': ['array']
                        }
                    }
                }
            }
        }
        merged_fields = loader.merge_fields(ecs, custom)
        expected_fields = {
            'foo': {
                'schema_details': {
                    'reusable': {
                        'top_level': True,
                        'expected': ['normal.location', 'a_new.location']
                    }
                },
                'field_details': { 'name': 'foo', 'type': 'group' },
                'fields': {
                    'normalized_field': {
                        'field_details': {
                            'name': 'normalized_field',
                            'type': 'keyword',
                            'normalize': ['lowercase', 'array']
                        }
                    },
                    'not_initially_normalized': {
                        'field_details': {
                            'name': 'not_initially_normalized',
                            'type': 'keyword',
                            'normalize': ['array']
                        }
                    }
                }
            }
        }
        self.assertEqual(
                merged_fields['foo']['schema_details']['reusable']['expected'],
                ['normal.location', 'a_new.location'])
        self.assertEqual(
                merged_fields['foo']['fields']['normalized_field']['field_details']['normalize'],
                ['lowercase', 'array'])
        self.assertEqual(
                merged_fields['foo']['fields']['not_initially_normalized']['field_details']['normalize'],
                ['array'])
        self.assertEqual(merged_fields, expected_fields)


    def test_merge_non_array_attributes(self):
        custom = {
            'base': {
                'schema_details': {
                    'root': False, # Override (not that I'd recommend overriding that)
                    'group': 3 # New
                },
                'field_details': {
                    'type': 'object', # Override
                    'example': 'foo' # New
                },
                'fields': {
                    'message': {
                        'field_details': {
                            'type': 'wildcard', # Override
                            'example': 'wild value' # New
                        }
                    }
                }
            }
        }
        merged_fields = loader.merge_fields(self.schema_base(), custom)
        expected_fields = {
            'base': {
                'schema_details': {
                    'root': False,
                    'group': 3
                },
                'field_details': {
                    'name': 'base',
                    'type': 'object',
                    'example': 'foo'
                },
                'fields': {
                    'message': {
                        'field_details': {
                            'name': 'message',
                            'type': 'wildcard',
                            'example': 'wild value'
                        }
                    }
                }
            }
        }
        self.assertEqual(merged_fields, expected_fields)


if __name__ == '__main__':
    unittest.main()
