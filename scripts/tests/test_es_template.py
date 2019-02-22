import unittest
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

    # dict_copy_existing_keys

    def test_dict_copy_existing_keys(self):
        source = {'key1': 'value1'}
        destination = {}
        es_template.dict_copy_existing_keys(source, destination, ['key1', 'missingkey'])
        self.assertEqual(destination, {'key1': 'value1'})

    def test_dict_copy_existing_keys_overwrites(self):
        source = {'key1': 'new_value'}
        destination = {'key1': 'overwritten', 'untouched': 'untouched'}
        es_template.dict_copy_existing_keys(source, destination, ['key1', 'untouched'])
        self.assertEqual(destination, {'key1': 'new_value', 'untouched': 'untouched'})


if __name__ == '__main__':
    unittest.main()
