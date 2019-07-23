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


if __name__ == '__main__':
    unittest.main()
