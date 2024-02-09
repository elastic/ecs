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
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generators import es_template


class TestGeneratorsEsTemplate(unittest.TestCase):
    # dict_add_nested

    def test_add_not_nested(self):
        dict = {}
        es_template.dict_add_nested(dict, ['field1'], {'field': 'details'})
        self.assertEqual(dict, {'field1': {'field': 'details'}})

    def test_dict_add_nested(self):
        dict = {}
        es_template.dict_add_nested(dict, ['parent_field', 'leaf_field'], {'field': 'details'})
        self.assertEqual(dict, {'parent_field': {'properties': {'leaf_field': {'field': 'details'}}}})

    def test_add_siblings(self):
        dict = {'field1': {'field': 'details 1'},
                'field2': {'properties': {'leaf1': {'field': 'details 2-1'}}}}
        es_template.dict_add_nested(dict, ['field3'], {'field': 'details 3'})
        es_template.dict_add_nested(dict, ['field2', 'leaf2'], {'field': 'details 2-2'})
        self.assertEqual(dict, {
            'field1': {'field': 'details 1'},
            'field2': {'properties': {
                'leaf1': {'field': 'details 2-1'},
                'leaf2': {'field': 'details 2-2'}
            }},
            'field3': {'field': 'details 3'}
        })

    def test_dict_add_nested_to_explicit_object(self):
        dict = {'answers': {'type': 'object'}}
        es_template.dict_add_nested(dict, ['answers', 'ttl'], {'type': 'long'})
        self.assertEqual(dict, {'answers': {'type': 'object', 'properties': {'ttl': {'type': 'long'}}}})

    def test_dict_add_nested_shouldnt_clobber_with_objects(self):
        dict = {'answers': {'properties': {'ttl': {'type': 'long'}}}}
        es_template.dict_add_nested(dict, ['answers'], {'type': 'object'})
        self.assertEqual(dict, {'answers': {'properties': {'ttl': {'type': 'long'}}}})

    def test_entry_for_adds_enabled_field(self):
        test_map = {
            'other': 'some data',
            'type': 'object',
            'enabled': False,
        }

        exp = {
            'type': 'object',
            'enabled': False,
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_enabled_true_ignored(self):
        test_map = {
            'other': 'some data',
            'type': 'object',
            'enabled': True,
        }

        exp = {
            'type': 'object',
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_enabled_with_index(self):
        test_map = {
            'other': 'some data',
            'type': 'object',
            'enabled': False,
            'index': False
        }

        exp = {
            'type': 'object',
            'enabled': False,
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_enabled_nested(self):
        test_map = {
            'other': 'some data',
            'type': 'nested',
            'enabled': False,
        }

        exp = {
            'type': 'nested',
            'enabled': False,
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_index(self):
        test_map = {
            'other': 'some data',
            'type': 'keyword',
            'index': False,
        }

        exp = {
            'type': 'keyword',
            'index': False,
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_alias(self):
        test_map = {
            'name': 'test.alias',
            'type': 'alias',
            'path': 'alias.target'
        }

        exp = {
            'type': 'alias',
            'path': 'alias.target'
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_scaled_float(self):
        test_map = {
            'name': 'test.scaled_float',
            'type': 'scaled_float',
            'scaling_factor': 1000
        }

        exp = {
            'type': 'scaled_float',
            'scaling_factor': 1000
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_constant_keyword_with_value(self):
        test_map = {
            'name': 'field_with_value',
            'type': 'constant_keyword',
            'value': 'foo'
        }

        exp = {
            'type': 'constant_keyword',
            'value': 'foo'
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_constant_keyword_no_value(self):
        test_map = {
            'name': 'field_without_value',
            'type': 'constant_keyword'
        }

        exp = {'type': 'constant_keyword'}
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_keyword_pass_ignore_above(self):
        test_map = {
            'name': 'field_with_ignore_above_set',
            'type': 'keyword',
            'ignore_above': 1024
        }

        exp = {
            'type': 'keyword',
            'ignore_above': 1024
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_flattened_pass_ignore_above(self):
        test_map = {
            'name': 'field_with_ignore_above_set',
            'type': 'flattened',
            'ignore_above': 1024
        }

        exp = {
            'type': 'flattened',
            'ignore_above': 1024
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_other_types_not_pass_ignore_above(self):
        test_map = {
            'name': 'field_should_not_have_ignore_above_set',
            'type': 'text',
            'ignore_above': 1024
        }

        exp = {
            'type': 'text'
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_parameters(self):
        test_map = {
            'name': 'field_with_parameters',
            'type': 'date',
            'parameters': {
                'format': 'strict_date_optional_time||epoch_seconds',
            }
        }

        exp = {
            'type': 'date',
            'format': 'strict_date_optional_time||epoch_seconds'
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_multi_fields(self):
        test_map = {
            'name': 'field_with_multi_fields',
            'type': 'keyword',
            'multi_fields': [
                {
                    'name': 'text',
                    'type': 'match_only_text'
                }
            ]
        }

        exp = {
            'type': 'keyword',
            'fields': {
                'text': {
                    'type': 'match_only_text'
                }
            }
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_multi_fields_parameters(self):
        test_map = {
            'name': 'field_with_multi_fields_with_parameters',
            'type': 'keyword',
            'multi_fields': [
                {
                    'name': 'text',
                    'type': 'match_only_text',
                    'parameters': {
                        'analyzer': 'english'
                    }
                }
            ]
        }

        exp = {
            'type': 'keyword',
            'fields': {
                'text': {
                    'type': 'match_only_text',
                    'analyzer': 'english'
                }
            }
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_component_composable_template_name(self):
        version = "1.8"
        test_map = {
            "Acme": {
                "name": "Acme",
            }
        }

        exp = ["ecs_{}_acme".format(version)]
        self.assertEqual(es_template.component_name_convention(version, test_map), exp)

    def test_legacy_template_settings_override(self):
        ecs_version = 100
        default = es_template.default_legacy_template_settings(ecs_version)

        generated_template = es_template.template_settings(ecs_version, None, None, is_legacy=True)
        self.assertEqual(generated_template, default)

        generated_template = es_template.template_settings(
            ecs_version, None, './usage-example/fields/template-settings-legacy.json', is_legacy=True)
        self.assertNotEqual(generated_template, default)

    def test_default_composable_template_settings(self):
        ecs_version = 100
        default = es_template.default_template_settings(ecs_version)
        # Setting these to empty since we aren't testing this piece
        default['template']['mappings'] = None
        default['composed_of'] = None

        generated_template = es_template.template_settings(ecs_version, None, None)
        self.assertEqual(generated_template, default)

        generated_template = es_template.template_settings(
            ecs_version, None, './usage-example/fields/template-settings.json', is_legacy=True)
        self.assertNotEqual(generated_template, default)


if __name__ == '__main__':
    unittest.main()
