import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generators import es_template


class TestGeneratorsEsTemplate(unittest.TestCase):
    # dict_add_nested

    def test_add_not_nested(self):
        dict = {}
        es_template.dict_add_nested(dict, ['level1'], 'value')
        self.assertEqual(dict, {'level1': 'value'})

    def test_dict_add_nested(self):
        dict = {}
        es_template.dict_add_nested(dict, ['level1', 'level2'], 'value')
        self.assertEqual(dict, {'level1': {'properties': {'level2': 'value'}}})

    def test_add_siblings(self):
        dict = {'key1': 'value1', 'key2': {'properties': {'nested1': 'value12'}}}
        es_template.dict_add_nested(dict, ['key3'], 'value3')
        es_template.dict_add_nested(dict, ['key2', 'nested2'], 'value22')
        self.assertEqual(dict, {
            'key1': 'value1',
            'key2': {'properties': {'nested1': 'value12', 'nested2': 'value22'}},
            'key3': 'value3'
        })


if __name__ == '__main__':
    unittest.main()
