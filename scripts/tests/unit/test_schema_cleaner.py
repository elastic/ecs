# Licensed to Elasticsearch B.V. under one or more contributor
# license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright
# ownership. Elasticsearch B.V. licenses this file to you under
# the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
import pprint
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from schema import cleaner


class TestSchemaCleaner(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def schema_process(self):
        return {
            'process': {
                'schema_details': {'title': 'Process'},
                'field_details': {
                    'name': 'process',
                    'description': 'Process details',
                    'type': 'group',
                },
                'fields': {
                    'pid': {
                        'field_details': {
                            'name': 'pid',
                            'type': 'keyword',
                            'description': 'The process ID',
                            'level': 'core',
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
                                    'level': 'core',
                                    'description': 'The process ID',
                                    'type': 'keyword',
                                }
                            }
                        }
                    }
                }
            }
        }

    # schemas

    def test_schema_raises_on_missing_required_attributes(self):
        schema = self.schema_process()['process']
        schema['schema_details'].pop('title')
        with self.assertRaisesRegex(ValueError, 'mandatory attributes: title'):
            cleaner.schema_cleanup(schema)

        schema = self.schema_process()['process']
        schema['field_details'].pop('description')
        with self.assertRaisesRegex(ValueError, 'mandatory attributes: description'):
            cleaner.schema_cleanup(schema)

    def test_reusable_schema_raises_on_missing_reuse_attributes(self):
        schema = self.schema_process()['process']
        schema['schema_details']['reusable'] = {}
        with self.assertRaisesRegex(ValueError, 'reuse attributes: expected, top_level'):
            cleaner.schema_mandatory_attributes(schema)

        schema['schema_details']['reusable']['expected'] = ['somewhere']
        with self.assertRaisesRegex(ValueError, 'reuse attributes: top_level'):
            cleaner.schema_mandatory_attributes(schema)

        schema['schema_details']['reusable'].pop('expected')
        schema['schema_details']['reusable']['top_level'] = True
        with self.assertRaisesRegex(ValueError, 'reuse attributes: expected'):
            cleaner.schema_mandatory_attributes(schema)

    def test_normalize_reuse_notation(self):
        reuse_locations = ['source', 'destination']
        pseudo_schema = {
            'field_details': {'name': 'user'},
            'schema_details': {'reusable': {'expected': reuse_locations}},
        }
        expected_reuse = [
            {'at': 'source', 'as': 'user', 'full': 'source.user'},
            {'at': 'destination', 'as': 'user', 'full': 'destination.user'},
        ]
        cleaner.normalize_reuse_notation(pseudo_schema)
        self.assertEqual(pseudo_schema['schema_details']['reusable']['expected'], expected_reuse)

    def test_already_normalized_reuse_notation(self):
        reuse_locations = [{'at': 'process', 'as': 'parent'}]
        pseudo_schema = {
            'field_details': {'name': 'process'},
            'schema_details': {'reusable': {'expected': reuse_locations}},
        }
        expected_reuse = [
            {'at': 'process', 'as': 'parent', 'full': 'process.parent'},
        ]
        cleaner.normalize_reuse_notation(pseudo_schema)
        self.assertEqual(pseudo_schema['schema_details']['reusable']['expected'], expected_reuse)

    def test_schema_simple_cleanup(self):
        my_schema = {
            'schema_details': {
                'title': "My Schema\n",
                'type': "group\n ",
                'group': 2,
                'root': False
            },
            'field_details': {
                'name': 'my_schema',
                'short': " a really short description\n\n",
                'description': "\ta long\n\nmultiline description   ",
            }
        }
        cleaner.schema_cleanup(my_schema)
        self.assertEqual(my_schema['schema_details']['title'], 'My Schema')
        self.assertEqual(my_schema['field_details']['type'], 'group')
        self.assertEqual(my_schema['field_details']['short'], 'a really short description')
        self.assertEqual(my_schema['field_details']['description'], "a long\n\nmultiline description")

    def test_schema_cleanup_setting_defaults(self):
        my_schema = {
            'schema_details': {
                'title': 'My Schema',
                'reusable': {
                    'top_level': True,
                    'expected': ['foo']
                }
            },
            'field_details': {
                'name': 'my_schema',
                'description': "a nice description   ",
            }
        }
        cleaner.schema_cleanup(my_schema)
        self.assertEqual(my_schema['schema_details']['root'], False)
        self.assertEqual(my_schema['schema_details']['group'], 2)
        self.assertEqual(my_schema['schema_details']['prefix'], 'my_schema.')
        self.assertEqual(my_schema['schema_details']['reusable']['order'], 2)
        self.assertEqual(my_schema['field_details']['type'], 'group')
        self.assertEqual(my_schema['field_details']['short'], 'a nice description')

    # fields

    def test_field_raises_on_missing_required_attributes(self):
        for missing_attribute in ['name', 'description', 'type', 'level']:
            field = self.schema_process()['process']['fields']['pid']
            field['field_details'].pop(missing_attribute)
            with self.assertRaisesRegex(ValueError,
                                        "mandatory attributes: {}".format(missing_attribute)):
                cleaner.field_mandatory_attributes(field)

    def test_field_raises_on_alias_missing_path_attribute(self):
        field = self.schema_process()['process']['fields']['pid']
        field['field_details']['type'] = "alias"
        with self.assertRaisesRegex(ValueError,
                                    "mandatory attributes: {}".format("path")):
            cleaner.field_mandatory_attributes(field)

    def test_raises_on_missing_scaling_factor(self):
        field = self.schema_process()['process']['fields']['pid']
        field['field_details']['type'] = "scaled_float"
        with self.assertRaisesRegex(ValueError,
                                    "mandatory attributes: {}".format("scaling_factor")):
            cleaner.field_mandatory_attributes(field)

    def test_field_simple_cleanup(self):
        my_field = {
            'field_details': {
                'name': "my_field\t",
                'type': 'keyword',
                'level': 'core',
                'short': " a really short description\n\n",
                'description': "\ta long\n\nmultiline description   ",
                'allowed_values': [
                    {
                        'name': "authentication\t",
                        'description': "when can auth be used?\n\n",
                    }
                ]
            }
        }
        cleaner.field_cleanup(my_field)
        self.assertEqual(my_field['field_details']['name'], 'my_field')
        self.assertEqual(my_field['field_details']['short'], 'a really short description')
        self.assertEqual(my_field['field_details']['description'], "a long\n\nmultiline description")
        self.assertEqual(my_field['field_details']['allowed_values'][0]['name'], 'authentication')
        self.assertEqual(my_field['field_details']['allowed_values'][0]['description'], 'when can auth be used?')

    def test_field_defaults(self):
        field_min_details = {
            'description': 'description',
            'level': 'extended',
            'name': 'my_field',
            'type': 'unknown',
        }
        # Note: unknown datatypes simply don't have defaults (for future proofing)
        field_details = field_min_details.copy()
        cleaner.field_defaults({'field_details': field_details})
        self.assertEqual(field_details['short'], field_details['description'])
        self.assertEqual(field_details['normalize'], [])

        field_details = {**field_min_details, **{'type': 'keyword'}}
        cleaner.field_defaults({'field_details': field_details})
        self.assertEqual(field_details['ignore_above'], 1024)

        field_details = {**field_min_details, **{'type': 'text'}}
        cleaner.field_defaults({'field_details': field_details})
        self.assertEqual(field_details['norms'], False)

        field_details = {**field_min_details, **{'index': True}}
        cleaner.field_defaults({'field_details': field_details})
        self.assertNotIn('doc_values', field_details)

        field_details = {**field_min_details, **{'index': False}}
        cleaner.field_defaults({'field_details': field_details})
        self.assertEqual(field_details['doc_values'], False)

        field_details = {**field_min_details, **{'type': 'wildcard', 'index': True}}
        cleaner.field_defaults({'field_details': field_details})
        self.assertNotIn('index', field_details)

    def test_field_defaults_dont_override(self):
        field_details = {
            'description': 'description',
            'level': 'extended',
            'name': 'my_long_field',
            'type': 'keyword',
            'ignore_above': 8000,
        }
        cleaner.field_defaults({'field_details': field_details})
        self.assertEqual(field_details['ignore_above'], 8000)

    def test_field_defaults_index_false_doc_values_false(self):
        field_details = {
            'description': 'description',
            'level': 'extended',
            'name': 'my_non_indexed_field',
            'type': 'keyword',
            'index': False,
            'doc_values': False
        }
        cleaner.field_defaults({'field_details': field_details})
        self.assertNotIn("ignore_above", field_details)

    def test_multi_field_defaults_and_precalc(self):
        field_details = {
            'description': 'description',
            'level': 'extended',
            'name': 'my_field',
            'type': 'unimportant',
            'multi_fields': [
                {
                    'type': 'text'
                },
                {
                    'type': 'keyword',
                    'name': 'special_name'
                },
            ]
        }
        cleaner.field_defaults({'field_details': field_details})

        mf = field_details['multi_fields'][0]
        self.assertEqual(mf['name'], 'text')
        self.assertEqual(mf['norms'], False)

        mf = field_details['multi_fields'][1]
        self.assertEqual(mf['name'], 'special_name')
        self.assertEqual(mf['ignore_above'], 1024)

    # common to schemas and fields

    def test_very_long_short_description_raises(self):
        schema = {'field_details': {
            'name': 'fake_schema',
            'short': "Single line but really long. " * 10}}
        with self.assertRaisesRegex(ValueError, 'under 120 characters \(current length: 290\)'):
            cleaner.single_line_short_description(schema)

    def test_multiline_short_description_raises(self):
        schema = {'field_details': {
            'name': 'fake_schema',
            'short': "multiple\nlines"}}
        with self.assertRaisesRegex(ValueError, 'single line'):
            cleaner.single_line_short_description(schema)

    def test_very_long_short_description_warns_strict_disabled(self):
        schema = {'field_details': {
            'name': 'fake_schema',
            'short': "Single line but really long. " * 10}}
        try:
            with self.assertWarnsRegex(UserWarning, 'under 120 characters \(current length: 290\)'):
                cleaner.single_line_short_description(schema, strict=False)
        except Exception:
            self.fail("cleaner.single_line_short_description() raised Exception unexpectedly.")

    def test_multiline_short_description_warns_strict_disabled(self):
        schema = {'field_details': {
            'name': 'fake_schema',
            'short': "multiple\nlines"}}
        try:
            with self.assertWarnsRegex(UserWarning, 'single line'):
                cleaner.single_line_short_description(schema, strict=False)
        except Exception:
            self.fail("cleaner.single_line_short_description() raised Exception unexpectedly.")

    def test_field_pattern_regex_raises_if_invalid(self):
        field = {
            'name': 'test',
            'pattern': '[.*'
        }
        with self.assertRaisesRegex(ValueError, 'Pattern value must be a valid regular expression'):
            cleaner.validate_pattern_regex(field, strict=True)

    def test_field_pattern_regex_warns_strict_disabled(self):
        field = {
            'name': 'test',
            'pattern': '[.*'
        }
        try:
            with self.assertWarnsRegex(UserWarning, 'valid regular expression'):
                cleaner.validate_pattern_regex(field, strict=False)
        except Exception:
            self.fail("cleaner.validate_pattern_regex() raised Exception unexpectedly.")

    def test_field_pattern_regex_success(self):
        field = {
            'name': 'test',
            'pattern': '[.*]'
        }
        self.assertIsNone(cleaner.validate_pattern_regex(field))

    def test_field_example_value_is_object_raises(self):
        field = {
            'field_details': {
                'name': 'test',
                'example': {
                    'a': 'bob',
                    'b': 'alice'
                }
            }
        }
        with self.assertRaisesRegex(ValueError, 'contains an object or array'):
            cleaner.check_example_value(field)

    def test_field_example_value_is_array_raises(self):
        field = {
            'field_details': {
                'name': 'test',
                'example': [
                    'bob',
                    'alice'
                ]
            }
        }
        with self.assertRaisesRegex(ValueError, 'contains an object or array'):
            cleaner.check_example_value(field)

    def test_example_field_value_is_object_warns_strict_disabled(self):
        field = {
            'field_details': {
                'name': 'test',
                'example': {
                    'a': 'bob',
                    'b': 'alice'
                }
            }
        }
        try:
            with self.assertWarnsRegex(UserWarning, 'contains an object or array'):
                cleaner.check_example_value(field, strict=False)
        except Exception:
            self.fail("cleaner.check_example_value() raised Exception unexpectedly.")

    def test_example_field_value_is_array_warns_strict_disabled(self):
        field = {
            'field_details': {
                'name': 'test',
                'example': [
                    'bob',
                    'alice'
                ]
            }
        }
        try:
            with self.assertWarnsRegex(UserWarning, 'contains an object or array'):
                cleaner.check_example_value(field, strict=False)
        except Exception:
            self.fail("cleaner.check_example_value() raised Exception unexpectedly.")

    def test_very_long_short_override_description_raises(self):
        schema = {
            'schema_details': {
                'reusable': {
                    'expected':
                        [{'at': 'process',
                          'as': 'parent',
                          'full': 'process.parent',
                          'short_override': "Single line but really long. " * 10}]
                }
            }
        }
        with self.assertRaisesRegex(ValueError, 'under 120 characters \(current length: 290\)'):
            cleaner.single_line_short_override_description(schema)

    def test_multiline_short_override_description_raises(self):
        schema = {
            'schema_details': {
                'reusable': {
                    'expected':
                        [{'at': 'process',
                          'as': 'parent',
                          'full': 'process.parent',
                          'short_override': "multiple\nlines"}]
                }
            }
        }
        with self.assertRaisesRegex(ValueError, 'single line'):
            cleaner.single_line_short_override_description(schema)

    def test_very_long_short_override_description_warns_strict_disabled(self):
        schema = {
            'schema_details': {
                'reusable': {
                    'expected':
                        [{'at': 'process',
                          'as': 'parent',
                          'full': 'process.parent',
                          'short_override': "Single line but really long. " * 10}]
                }
            }
        }
        try:
            with self.assertWarnsRegex(UserWarning, 'under 120 characters \(current length: 290\)'):
                cleaner.single_line_short_override_description(schema, strict=False)
        except Exception:
            self.fail("cleaner.single_line_short_override_description() raised Exception unexpectedly.")

    def test_multiline_short_override_description_warns_strict_disabled(self):
        schema = {
            'schema_details': {
                'reusable': {
                    'expected':
                        [{'at': 'process',
                          'as': 'parent',
                          'full': 'process.parent',
                          'short_override': "multiple\nlines"}]
                }
            }
        }
        try:
            with self.assertWarnsRegex(UserWarning, 'single line'):
                cleaner.single_line_short_override_description(schema, strict=False)
        except Exception:
            self.fail("cleaner.single_line_short_override_description() raised Exception unexpectedly.")

    def test_clean(self):
        """A high level sanity test"""
        fields = self.schema_process()
        cleaner.clean(fields)
        # schemas are processed
        self.assertEqual(fields['process']['schema_details']['prefix'], 'process.')
        self.assertEqual(fields['process']['schema_details']['group'], 2)
        # fields are processed
        parent_pid = fields['process']['fields']['parent']['fields']['pid']
        self.assertEqual(parent_pid['field_details']['name'], 'parent.pid')
        self.assertEqual(parent_pid['field_details']['ignore_above'], 1024)
        self.assertEqual(parent_pid['field_details']['short'],
                         parent_pid['field_details']['description'])
