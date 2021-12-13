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

    @mock.patch('schema.loader.warn')
    def test_eval_globs(self, mock_warn):
        files = loader.eval_globs(['schemas/*.yml', 'missing*'])
        self.assertTrue(mock_warn.called, "a warning should have been printed for missing*")
        self.assertIn('schemas/base.yml', files)
        self.assertEqual(list(filter(lambda f: f.startswith('missing'), files)), [],
                         "The 'missing*' pattern should not show up in the resulting files")

    @mock.patch('schema.loader.warn')
    def test_eval_globs_pattern(self, mock_warn):
        files = loader.eval_globs(['schemas/a*.yml'])
        self.assertEqual(['schemas/agent.yml', 'schemas/as.yml'].sort(), files.sort(),
                         "glob should load all files matching 'schemas/a*.yml'")

    @mock.patch('schema.loader.warn')
    def test_eval_globs_filenames(self, mock_warn):
        files = loader.eval_globs(['schemas/agent.yml', 'schemas/x509.yml'])
        self.assertEqual(['schemas/agent.yml', 'schemas/x509.yml'], files,
                         "glob should load all files matching '['schemas/agent.yml', 'schemas/x509.yml']'")

    @mock.patch('schema.loader.warn')
    def test_eval_globs_folder(self, mock_warn):
        files = loader.eval_globs(['schemas/'])
        self.assertIn('schemas/base.yml', files,
                      "glob should load all files in folder 'schemas' including 'schemas/base.yml']'")

    @mock.patch('schema.loader.warn')
    def test_eval_globs_folders(self, mock_warn):
        files = loader.eval_globs(['schemas/', 'usage-example/fields/custom/'])
        self.assertIn('usage-example/fields/custom/acme.yml', files,
                      "glob should load all files in folders ['schemas/', 'usage-example/fields/custom/'] including 'usage-example/fields/custom/acme.yml''")

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

    def test_load_schemas_git_ref(self):
        fields = loader.load_schemas(ref='v1.6.0')
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
            loader.nest_schema([{'description': 'just a description'}], 'incomplete.yml')

    def test_load_schemas_from_git(self):
        fields = loader.load_schemas_from_git('v1.0.0', target_dir='schemas')
        self.assertEqual(
            ['agent',
             'base',
             'client',
             'cloud',
             'container',
             'destination',
             'ecs',
             'error',
             'event',
             'file',
             'geo',
             'group',
             'host',
             'http',
             'log',
             'network',
             'observer',
             'organization',
             'os',
             'process',
             'related',
             'server',
             'service',
             'source',
             'url',
             'user',
             'user_agent'],
            sorted(fields.keys()),
            "Raw schema fields should have expected fieldsets for v1.0.0")

    def test_load_schemas_from_git_missing_target_directory(self):
        with self.assertRaisesRegex(KeyError, "not present in git ref 'v1.5.0'"):
            loader.load_schemas_from_git('v1.5.0', target_dir='experimental')

    # nesting stuff

    def test_nest_fields(self):
        process_fields = [
            {'name': 'pid'},
            {'name': 'parent.pid'},
        ]
        expected_nested_fields = {
            'fields': {
                'pid': {
                    'field_details': {
                        'name': 'pid',
                        'node_name': 'pid',
                    }
                },
                'parent': {
                    'field_details': {
                        'name': 'parent',
                        'node_name': 'parent',
                        'type': 'object',
                        'intermediate': True,
                    },
                    'fields': {
                        'pid': {
                            'field_details': {
                                'name': 'parent.pid',
                                'node_name': 'pid',
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
            {'name': 'answers', 'type': 'object'},
            {'name': 'answers.data', 'type': 'keyword'},
        ]
        expected_nested_fields = {
            'fields': {
                'answers': {
                    'field_details': {
                        'name': 'answers',
                        'node_name': 'answers',
                        'type': 'object',
                        'intermediate': False,
                    },
                    'fields': {
                        'data': {
                            'field_details': {
                                'name': 'answers.data',
                                'node_name': 'data',
                                'type': 'keyword',
                            }
                        }
                    }
                },
                'question': {
                    'field_details': {
                        'name': 'question',
                        'node_name': 'question',
                        'type': 'object',
                        'intermediate': True,
                    },
                    'fields': {
                        'name': {
                            'field_details': {
                                'name': 'question.name',
                                'node_name': 'name',
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
        log_fields = [{'name': 'origin.file.name'}]
        expected_nested_fields = {
            'fields': {
                'origin': {
                    'field_details': {
                        'name': 'origin',
                        'node_name': 'origin',
                        'type': 'object',
                        'intermediate': True,
                    },
                    'fields': {
                        'file': {
                            'field_details': {
                                'name': 'origin.file',
                                'node_name': 'file',
                                'type': 'object',
                                'intermediate': True,
                            },
                            'fields': {
                                'name': {
                                    'field_details': {
                                        'name': 'origin.file.name',
                                        'node_name': 'name',
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
                    'node_name': 'base',
                    'type': 'group',
                },
                'fields': {
                    'message': {
                        'field_details': {
                            'name': 'message',
                            'node_name': 'message',
                            'type': 'keyword',
                        }
                    }
                }
            },
            'process': {
                'schema_details': {},
                'field_details': {
                    'name': 'process',
                    'node_name': 'process',
                    'type': 'group'
                },
                'fields': {
                    'pid': {
                        'field_details': {
                            'name': 'pid',
                            'node_name': 'pid',
                            'type': 'keyword',
                        }
                    },
                    'parent': {
                        'field_details': {
                            # These are made explicit for intermediate fields
                            'name': 'parent',
                            'node_name': 'parent',
                            'type': 'object',
                            'intermediate': True,
                        },
                        'fields': {
                            'pid': {
                                'field_details': {
                                    'name': 'parent.pid',
                                    'node_name': 'pid',
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
                'schema_details': {},
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
                'schema_details': {},
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
                'schema_details': {'root': True},
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
                'schema_details': {},
                'field_details': {
                    'name': 'process'
                },
                'fields': {
                    'parent': {
                        'field_details': {'type': 'object'},
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
                'field_details': {'name': 'foo', 'type': 'group'},
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
                'field_details': {'name': 'foo', 'type': 'group'},
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
                'field_details': {'name': 'foo', 'type': 'group'},
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
                    'root': False,  # Override (not that I'd recommend overriding that)
                    'group': 3  # New
                },
                'field_details': {
                    'type': 'object',  # Override
                    'example': 'foo'  # New
                },
                'fields': {
                    'message': {
                        'field_details': {
                            'type': 'wildcard',  # Override
                            'example': 'wild value'  # New
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

    def test_merge_and_overwrite_multi_fields(self):
        originalSchema = {
            'overwrite_field': {
                'field_details': {
                    'multi_fields': [
                        {
                            'type': 'text',
                            'name': 'text',
                            'norms': True
                        }
                    ]
                },
                'fields': {
                    'message': {
                        'field_details': {
                            'multi_fields': [
                                {
                                    'type': 'text',
                                    'name': 'text'
                                }
                            ]
                        }
                    }
                }
            }
        }

        customSchema = {
            'overwrite_field': {
                'field_details': {
                    'multi_fields': [
                        # this entry will completely overwrite the originalSchema's name text entry
                        {
                            'type': 'text',
                            'name': 'text'
                        }
                    ]
                },
                'fields': {
                    'message': {
                        'field_details': {
                            'multi_fields': [
                                # this entry will be merged with the originalSchema's multi_fields entries
                                {
                                    'type': 'keyword',
                                    'name': 'a_field'
                                }
                            ]
                        }
                    }
                }
            }
        }
        merged_fields = loader.merge_fields(originalSchema, customSchema)
        expected_overwrite_field_mf = [
            {
                'type': 'text',
                'name': 'text'
            }
        ]

        expected_message_mf = [
            {
                'type': 'keyword',
                'name': 'a_field'
            },
            {
                'type': 'text',
                'name': 'text'
            }
        ]
        self.assertEqual(merged_fields['overwrite_field']['field_details']['multi_fields'], expected_overwrite_field_mf)
        self.assertEqual(merged_fields['overwrite_field']['fields']['message']['field_details']
                         ['multi_fields'], expected_message_mf)


if __name__ == '__main__':
    unittest.main()
