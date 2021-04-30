import json
import os
import sys
import unittest
from unittest.mock import patch, mock_open

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generators import es_mappings_schema


class TestGeneratorsEsMappingsSchema(unittest.TestCase):

    def test_add_not_nested(self):
        schema = {}
        es_mappings_schema.add_nested(schema, ['field'], {'subfield': 'details'})
        self.assertEqual(schema, {'field': {'subfield': 'details'}})

    def test_add_nested(self):
        schema = {}
        expected = {
            'parent': {
                'properties': {
                    'type': 'object',
                    'properties': {
                        'properties': {
                            'leaf_field': {
                                'field': 'details'
                            }
                        }
                    }
                }
            }
        }

        es_mappings_schema.add_nested(schema, ['parent', 'leaf_field'], {'field': 'details'})
        self.assertEqual(schema, expected)

    def test_add_siblings(self):
        schema = {
            'field1': {
                'field': 'details 1',
            },
            'field2': {
                'properties': {
                    'leaf1': {
                        'field': 'details 2-1'
                    }
                }
            }
        }

        expected = {
            'field1': {
                'field': 'details 1'
            },
            'field2': {
                'properties': {
                    'leaf1': {
                        'field': 'details 2-1'
                    },
                    'properties': {
                        'properties': {
                            'leaf2': {
                                'field': 'details 2-2'
                            }
                        }
                    }
                }
            },
            'field3': {
                'field': 'details 3'
            }
        }

        es_mappings_schema.add_nested(schema, ['field3'], {'field': 'details 3'})
        es_mappings_schema.add_nested(schema, ['field2', 'leaf2'], {'field': 'details 2-2'})

        self.assertEqual(schema, expected)


    def test_add_nested_to_explicit_object(self):
        schema = {
            'answers': {
                'type': 'object',
                'properties': {
                    'type': 'object'
                }
            }
        }

        expected = {
            'answers': {
                'type': 'object',
                'properties': {
                    'type': 'object',
                    'properties': {
                        'properties': {
                            'ttl': {
                                'type': 'long'
                            }
                        }
                    }
                }
            }
        }

        es_mappings_schema.add_nested(schema, ['answers', 'ttl'], {'type': 'long'})
        self.assertEqual(schema, expected)

    def test_add_nested_should_not_clobber_with_objects(self):
        schema = {
            'answers': {
                'type': 'object',
                'properties': {
                    'properties': {
                        'ttl': {
                            'type': 'long'
                        }
                    }
                }
            }
        }

        expected = {
            'answers': {
                'type': 'object',
                'properties': {
                    'properties': {
                        'ttl': {
                            'type': 'long'
                        }
                    }
                }
            }
        }

        es_mappings_schema.add_nested(schema, ['answers'], { 'properties': {'type': 'object' }})
        self.assertEqual(schema, expected)


    def test_entry_for_expected_structure(self):
        field = {
            'description': 'This is\nmy field.',
            'type': 'keyword'
        }

        expected = {
            'description': 'This is my field.',
            'type': 'object',
            'required': ['type'],
            'properties': {
                'type': {
                    '$ref': '#/definitions/types/keyword'
                }
            }
        }

        field_entry = es_mappings_schema.entry_for(field)
        self.assertEqual(field_entry, expected)


    def test_candidate_field_sets(self):
        nested = {
            'agent': {
                'reusable': {
                    'top_level': True
                }
            },
            'host': {
                'reusable': {
                    'top_level': False
                }
            }
        }

        expected = {
            'agent': {
                'reusable': {
                    'top_level': True
                }
            }
        }

        candidate_fields = es_mappings_schema.candidate_field_sets(nested)
        self.assertEqual(candidate_fields, expected)


    def test_used_data_types(self):
        flat = {
            'field1': {
                'type': 'keyword'
            },
            'field2': {
                'type': 'keyword'
            },
            'field3': {
                'type': 'object'
            }
        }

        expected = ['keyword', 'object']
        data_types = es_mappings_schema.used_data_types(flat)

        self.assertEqual(data_types, expected)


    def test_save_schema_file(self):
        fake_filename = './generated/json_schema/schema.json'
        field_mapping = {'ecs_version': '1.0.0'}
        expected = '{\n  "ecs_version": "1.0.0"\n}'

        with patch('builtins.open', mock_open()) as mocked_file:
            es_mappings_schema.save_schema_file(fake_filename, field_mapping)

            mocked_file.assert_called_once_with(fake_filename, 'w')

            mocked_file().write.assert_called_once_with(expected)


    def test_schema_definitions(self):
        data_types = ['keyword', 'object']

        expected = {
            'types': {
                'type': 'object',
                'keyword': {
                    'type': 'string',
                    'enum': ['keyword']
                },
                'object': {
                    'type': 'string',
                    'enum': ['object']
                }
            }
        }

        definitions = es_mappings_schema.schema_definitions(data_types)
        self.assertEqual(definitions, expected)
