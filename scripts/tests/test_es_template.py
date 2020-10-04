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

    def test_entry_for_alias_missing_path(self):
        test_map = {
            'name': 'test.alias',
            'type': 'alias'
        }

        with self.assertRaisesRegex(ValueError,
                                    "The \[path\] property must be specified for field \[{}\]".format(test_map['name'])):
            es_template.entry_for(test_map)

if __name__ == '__main__':
    unittest.main()
