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

from scripts.generators import ecs_helpers


class TestECSHelpers(unittest.TestCase):

    def test_is_intermediate_field(self):
        pseudo_field = {'field_details': {}}
        self.assertEqual(ecs_helpers.is_intermediate(pseudo_field), False)
        pseudo_field['field_details']['intermediate'] = False
        self.assertEqual(ecs_helpers.is_intermediate(pseudo_field), False)
        pseudo_field['field_details']['intermediate'] = True
        self.assertEqual(ecs_helpers.is_intermediate(pseudo_field), True)

    # dict_copy_existing_keys

    def test_dict_copy_existing_keys(self):
        source = {'key1': 'value1'}
        destination = {}
        ecs_helpers.dict_copy_existing_keys(source, destination, ['key1', 'missingkey'])
        self.assertEqual(destination, {'key1': 'value1'})

    def test_dict_copy_existing_keys_overwrites(self):
        source = {'key1': 'new_value'}
        destination = {'key1': 'overwritten', 'untouched': 'untouched'}
        ecs_helpers.dict_copy_existing_keys(source, destination, ['key1', 'untouched'])
        self.assertEqual(destination, {'key1': 'new_value', 'untouched': 'untouched'})

    # dict_sorted_by_keys

    def test_sorted_by_one_key(self):
        dict = {
            'message': {'name': 'message'},
            'labels': {'name': 'labels'},
            '@timestamp': {'name': '@timestamp'},
            'tags': {'name': 'tags'}
        }
        expected = [
            {'name': '@timestamp'},
            {'name': 'labels'},
            {'name': 'message'},
            {'name': 'tags'}
        ]
        result = ecs_helpers.dict_sorted_by_keys(dict, 'name')
        self.assertEqual(result, expected)
        result = ecs_helpers.dict_sorted_by_keys(dict, ['name'])
        self.assertEqual(result, expected)

    def test_sorted_by_multiple_keys(self):
        dict = {
            'cloud': {'group': 2, 'name': 'cloud'},
            'agent': {'group': 2, 'name': 'agent'},
            'base': {'group': 1, 'name': 'base'},
        }
        expected = [
            {'group': 1, 'name': 'base'},
            {'group': 2, 'name': 'agent'},
            {'group': 2, 'name': 'cloud'}
        ]
        result = ecs_helpers.dict_sorted_by_keys(dict, ['group', 'name'])
        self.assertEqual(result, expected)

    def test_merge_dicts(self):
        a = {
            'cloud': {'group': 2, 'name': 'cloud'},
            'agent': {'group': 2, 'name': 'agent'},
        }
        b = {'base': {'group': 1, 'name': 'base'}}

        result = ecs_helpers.safe_merge_dicts(a, b)

        self.assertEqual(result,
                         {
                             'cloud': {'group': 2, 'name': 'cloud'},
                             'agent': {'group': 2, 'name': 'agent'},
                             'base': {'group': 1, 'name': 'base'}
                         })

    def test_merge_dicts_raises_if_duplicate_key_added(self):
        a = {'cloud': {'group': 2, 'name': 'cloud'}}
        b = {'cloud': {'group': 9, 'name': 'bazbar'}}

        with self.assertRaises(ValueError):
            ecs_helpers.safe_merge_dicts(a, b)

    def test_clean_string_values(self):
        dict = {'dirty': ' space, the final frontier  ', 'clean': 'val', 'int': 1}
        ecs_helpers.dict_clean_string_values(dict)
        self.assertEqual(dict, {'dirty': 'space, the final frontier', 'clean': 'val', 'int': 1})

    # List helper tests

    def test_list_subtract(self):
        self.assertEqual(ecs_helpers.list_subtract(['a', 'b'], ['a']), ['b'])
        self.assertEqual(ecs_helpers.list_subtract(['a', 'b'], ['a', 'c']), ['b'])

    # git helper tests

    def test_get_tree_by_ref(self):
        ref = 'v1.5.0'
        tree = ecs_helpers.get_tree_by_ref(ref)
        self.assertEqual(tree.hexsha, '4449df245f6930d59bcd537a5958891261a9476b')

    def test_path_exists_in_git_tree(self):
        ref = 'v1.6.0'
        tree = ecs_helpers.get_tree_by_ref(ref)
        self.assertFalse(ecs_helpers.path_exists_in_git_tree(tree, 'nonexistant'))
        self.assertTrue(ecs_helpers.path_exists_in_git_tree(tree, 'schemas'))

    # file helpers

    def test_is_yaml(self):
        self.assertTrue(ecs_helpers.is_yaml('./schemas/base.yml'))
        self.assertTrue(ecs_helpers.is_yaml('./build/docs/conf.yaml'))
        self.assertFalse(ecs_helpers.is_yaml('./README.md'))
        self.assertFalse(ecs_helpers.is_yaml('./schemas/'))
        self.assertFalse(ecs_helpers.is_yaml('./build'))

    def test_glob_yaml_files(self):
        self.assertEqual(ecs_helpers.glob_yaml_files('non_existent_file'), [])
        self.assertEqual(ecs_helpers.glob_yaml_files('non_existent_directory/'), [])
        self.assertEqual(ecs_helpers.glob_yaml_files('non_existent_wildcard.*'), [])
        self.assertEqual(ecs_helpers.glob_yaml_files('schemas/base.yml'), ['schemas/base.yml'])
        self.assertEqual(ecs_helpers.glob_yaml_files(['schemas/base.yml']), ['schemas/base.yml'])
        # convert to set as element order is not being tested
        self.assertEqual(set(ecs_helpers.glob_yaml_files(
            ['schemas/base.yml', 'schemas/log.yml'])), {'schemas/base.yml', 'schemas/log.yml'})
        self.assertTrue(set(ecs_helpers.glob_yaml_files('schemas/b*.yml')).intersection({'schemas/base.yml'}) != set())
        self.assertTrue(set(ecs_helpers.glob_yaml_files(
            'schemas/[bl]*.yml')).intersection({'schemas/base.yml', 'schemas/log.yml'}) != set())
        min_schema_count = 46
        self.assertTrue(len(ecs_helpers.glob_yaml_files(ecs_helpers.glob_yaml_files('schemas'))) >= min_schema_count)
        self.assertTrue(len(ecs_helpers.glob_yaml_files(ecs_helpers.glob_yaml_files('schemas/'))) >= min_schema_count)
        self.assertTrue(len(ecs_helpers.glob_yaml_files(
            ecs_helpers.glob_yaml_files('schemas/*.yml'))) >= min_schema_count)
        self.assertEqual(len(ecs_helpers.glob_yaml_files(ecs_helpers.glob_yaml_files('schemas/*.yaml'))), 0)

    # Remove top_level:false field sets helper

    def test_remove_top_level_false_field_sets(self):
        nested_schema_original = {
            'as': {'group': 2, 'name': 'as', 'reusable': {'top_level': False}},
            'agent': {'group': 2, 'name': 'agent'},
        }
        nested_schema_expected = {
            'agent': {'group': 2, 'name': 'agent'}
        }
        self.assertEqual(ecs_helpers.remove_top_level_reusable_false(nested_schema_original), nested_schema_expected)


if __name__ == '__main__':
    unittest.main()
