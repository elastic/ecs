import mock
import os
import pprint
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from schema import exclude_filter


class TestSchemaExcludeFilter(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @mock.patch('schema.loader.warn')
    def test_load_exclude_definitions_raises_when_no_exclude_found(self, mock_warn):
        with self.assertRaisesRegex(ValueError,
                                    "--exclude specified, but no exclusions found in \['foo\*.yml'\]"):
            exclude_filter.load_exclude_definitions(['foo*.yml'])

    def test_exclude_field(self):
        fields = {'my_field_set': {'fields': {
            'my_field_exclude': {'field_details': {'flat_name': 'my_field_set.my_field_exclude'}},
            'my_field_persist': {'field_details': {'flat_name': 'my_field_set.my_field_persist'}}}}}
        excludes = [[{'name': 'my_field_set', 'fields': [{'name': 'my_field_exclude'}]}]]
        fields = exclude_filter.exclude_fields(fields, excludes)
        expect_persisted = {'my_field_set': {'fields': {
            'my_field_persist': {'field_details': {'flat_name': 'my_field_set.my_field_persist'}}}}}
        self.assertEqual(fields, expect_persisted)

    def test_exclude_fields(self):
        fields = {'my_field_set': {'fields': {
            'my_field_exclude_1': {'field_details': {'flat_name': 'my_field_set.my_field_exclude_1'}},
            'my_field_exclude_2': {'field_details': {'flat_name': 'my_field_set.my_field_exclude_2'}}}}}
        excludes = [[{'name': 'my_field_set', 'fields': [
            {'name': 'my_field_exclude_1'}, {'name': 'my_field_exclude_2'}]}]]
        fields = exclude_filter.exclude_fields(fields, excludes)
        expect_persisted = {'my_field_set': {'fields': {}}}
        self.assertEqual(fields, expect_persisted)

    def test_exclude_non_existing_field_set(self):
        fields = {'my_field_set': {'fields': {
            'my_field_exclude': {'field_details': {'flat_name': 'my_field_set.my_field_exclude'}}}}}
        excludes = [[{'name': 'my_non_existing_field_set', 'fields': [
            {'name': 'my_field_exclude_1'}]}]]
        with self.assertRaisesRegex(ValueError,
                                    "--exclude specified, but no field my_non_existing_field_set.my_field_exclude_1 found"):
            exclude_filter.exclude_fields(fields, excludes)


'''
    def test_merging_superset(self):
        # 'log' is used to test superset with the explicit '{'fields': '*'}' notation
        supersets = {'log': {'fields': '*'}, 'process': {'fields': '*'}}
        supserseded = {
            'log': {'fields': {'syslog': {'fields': '*'}}},
            'process': {'fields': {'parent': {'fields': '*'}}},
        }
        excludes = {}
        exclude_filter.merge_excludes(excludes, supersets)
        exclude_filter.merge_excludes(excludes, supserseded)
        self.assertEqual(excludes, supersets)
        # reverse order
        excludes = {}
        exclude_filter.merge_excludes(excludes, supserseded)
        exclude_filter.merge_excludes(excludes, supersets)
        self.assertEqual(excludes, supersets)

    def test_exclude_option_merging(self):
        exclude1 = {
            'log': {'enabled': False},
            'network': {'enabled': False, 'fields': '*'},
            'base': {'fields': {'message': {'index': False}}},
        }
        exclude2 = {
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
        exclude_filter.merge_excludes(merged, exclude1)
        exclude_filter.merge_excludes(merged, exclude2)
        self.assertEqual(merged, expected)

    def test_strip_non_ecs_options(self):
        exclude = {
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
        exclude_filter.strip_non_ecs_options(exclude)
        self.assertEqual(exclude, expected)

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
                        'field_details': {
                            'name': 'origin',
                            'intermediate': True,
                            'type': 'object'
                        },
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
        exclude = {'log': {'fields': '*'}}
        filtered_fields = exclude_filter.extract_matching_fields(self.schema_log(), exclude)
        self.assertEqual(filtered_fields, self.schema_log())

    def test_extract_matching_fields_subfields_only_notation(self):
        exclude = {'log': {'fields': {'origin': {'fields': '*'}}}}
        filtered_fields = exclude_filter.extract_matching_fields(self.schema_log(), exclude)
        expected_fields = {
            'log': {
                'schema_details': {'root': False},
                'field_details': {
                    'name': 'log',
                    'type': 'group'
                },
                'fields': {
                    'origin': {
                        'field_details': {
                            'name': 'origin',
                            'intermediate': True,
                            'type': 'object'
                        },
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
        exclude = {'log': {'fields': {'origin': {'fields': {'function': {}}}}}}
        filtered_fields = exclude_filter.extract_matching_fields(self.schema_log(), exclude)
        expected_fields = {
            'log': {
                'schema_details': {'root': False},
                'field_details': {
                    'name': 'log',
                    'type': 'group'
                },
                'fields': {
                    'origin': {
                        'field_details': {
                            'name': 'origin',
                            'intermediate': True,
                            'type': 'object'
                        },
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
        exclude = {
            'log': {
                'enabled': False,
                'fields': {
                    'level': {
                        'custom_option': True
                    },
                    'origin': {
                        'custom_option': False,
                        'fields': {
                            'function': {}
                        }
                    }
                }
            }
        }
        filtered_fields = exclude_filter.extract_matching_fields(self.schema_log(), exclude)
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
                    },
                    'origin': {
                        'field_details': {
                            # This field is changed by the exclude_filter from an intermediate field to non-intermediate by adding
                            # a custom option, so the exclude_filter is responsible for filling in more field_detail attributes
                            'name': 'origin',
                            'intermediate': False,
                            'custom_option': False,
                            'description': 'Intermediate field included by adding option with exclude',
                            'level': 'custom',
                            'type': 'object',
                            'short': 'Intermediate field included by adding option with exclude',
                            'normalize': []
                        },
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

'''
