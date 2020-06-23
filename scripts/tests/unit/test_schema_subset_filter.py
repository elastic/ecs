import mock
import os
import pprint
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from schema import subset_filter


class TestSchemaSubsetFilter(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @mock.patch('schema.subset_filter.warn')
    def test_eval_globs(self, mock_warn):
        files = subset_filter.eval_globs(['schemas/*.yml', 'missing*'])
        self.assertTrue(mock_warn.called, "a warning should have been printed for missing*")
        self.assertIn('schemas/base.yml', files)
        self.assertEqual(list(filter(lambda f: f.startswith('missing'), files)), [],
                         "The 'missing*' pattern should not show up in the resulting files")

    @mock.patch('schema.subset_filter.warn')
    def test_load_subset_definitions_raises_when_no_subset_found(self, mock_warn):
        with self.assertRaisesRegex(ValueError,
                                    "--subset specified, but no subsets found in \['foo\*.yml'\]"):
            subset_filter.load_subset_definitions(['foo*.yml'])

    def test_basic_merging(self):
        basics = {'base': {'fields': '*'}, 'event': {}}
        network = {'network': {'fields': '*'}}
        subsets = {}
        subset_filter.merge_subsets(subsets, basics)
        subset_filter.merge_subsets(subsets, network)
        expected_subsets = {**basics, **network}
        self.assertEqual(subsets, expected_subsets)

    def test_merging_superset(self):
        # 'log' is used to test superset with the explicit '{'fields': '*'}' notation
        supersets = {'log': {'fields': '*'}, 'process': {'fields': '*'}}
        supserseded = {
            'log': {'fields': {'syslog': {'fields': '*'}}},
            'process': {'fields': {'parent': {'fields': '*'}}},
        }
        subsets = {}
        subset_filter.merge_subsets(subsets, supersets)
        subset_filter.merge_subsets(subsets, supserseded)
        self.assertEqual(subsets, supersets)
        # reverse order
        subsets = {}
        subset_filter.merge_subsets(subsets, supserseded)
        subset_filter.merge_subsets(subsets, supersets)
        self.assertEqual(subsets, supersets)

    def test_subset_option_merging(self):
        subset1 = {
            'log': {'enabled': False},
            'network': {'enabled': False, 'fields': '*'},
            'base': {'fields': {'message': {'index': False}}},
        }
        subset2 = {
            'log': {'enabled': False},
            'network': {'fields': '*'},
            'base': {'fields': {'message': {}}},
        }
        expected = {
            'log': {'enabled': False},
            'network': {'fields': '*'},
            'base': {'fields': {'message': {}}},
        }
        merged = {}
        subset_filter.merge_subsets(merged, subset1)
        subset_filter.merge_subsets(merged, subset2)
        self.assertEqual(merged, expected)

    def test_strip_non_ecs_options(self):
        subset = {
            'log': {
                'custom_option': True,
                'enabled': False,
                'fields': {
                    'syslog': {
                        'custom_option': True
                    }
                }
            }
        }
        expected = {
            'log': {
                'enabled': False,
                'fields': {
                    'syslog': {}
                }
            }
        }
        subset_filter.strip_non_ecs_options(subset)
        self.assertEqual(subset, expected)

    def schema_log(self):
        return {
            'log': {
                'schema_details': {'root': False},
                'field_details': {
                    'name': 'log',
                    'type': 'group'
                },
                'fields': {
                    'level': {
                        'field_details': {
                            'name': 'level',
                            'type': 'keyword'
                        }
                    },

                    'origin': {
                        'fields': {
                            'function': {
                                'field_details': {
                                    'name': 'function',
                                    'type': 'keyword'
                                }
                            },
                            'foo': {
                                'field_details': {
                                    'name': 'foo',
                                    'type': 'keyword'
                                }
                            },
                        }
                    }
                }
            }
        }

    def test_extract_matching_fields_explicit_all_fields_notation(self):
        subset = {'log': {'fields': '*'}}
        filtered_fields = subset_filter.extract_matching_fields(self.schema_log(), subset)
        self.assertEqual(filtered_fields, self.schema_log())

    def test_extract_matching_fields_subfields_only_notation(self):
        subset = {'log': {'fields': {'origin': {'fields': '*'}}}}
        filtered_fields = subset_filter.extract_matching_fields(self.schema_log(), subset)
        expected_fields = {
            'log': {
                'schema_details': {'root': False},
                'field_details': {
                    'name': 'log',
                    'type': 'group'
                },
                'fields': {
                    'origin': {
                        'fields': {
                            'function': {
                                'field_details': {
                                    'name': 'function',
                                    'type': 'keyword'
                                }
                            },
                            'foo': {
                                'field_details': {
                                    'name': 'foo',
                                    'type': 'keyword'
                                }
                            },
                        }
                    }
                }
            }
        }
        self.assertEqual(filtered_fields, expected_fields)

    def test_extract_matching_individual_field(self):
        subset = {'log': {'fields': {'origin': {'fields': {'function': {}}}}}}
        filtered_fields = subset_filter.extract_matching_fields(self.schema_log(), subset)
        expected_fields = {
            'log': {
                'schema_details': {'root': False},
                'field_details': {
                    'name': 'log',
                    'type': 'group'
                },
                'fields': {
                    'origin': {
                        'fields': {
                            'function': {
                                'field_details': {
                                    'name': 'function',
                                    'type': 'keyword'
                                }
                            },
                        }
                    }
                }
            }
        }
        self.assertEqual(filtered_fields, expected_fields)

    def test_extract_field_with_options(self):
        subset = {'log': {'enabled': False, 'fields': {'level': {'custom_option': True}}}}
        filtered_fields = subset_filter.extract_matching_fields(self.schema_log(), subset)
        expected_fields = {
            'log': {
                'schema_details': {'root': False},
                'field_details': {
                    'name': 'log',
                    'type': 'group',
                    'enabled': False
                },
                'fields': {
                    'level': {
                        'field_details': {
                            'name': 'level',
                            'type': 'keyword',
                            'custom_option': True
                        }
                    }
                }
            }
        }
        self.assertEqual(filtered_fields, expected_fields)
