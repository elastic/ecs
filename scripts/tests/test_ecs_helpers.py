import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generators import ecs_helpers


class TestECSHelpers(unittest.TestCase):
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
            '@timestamp': {'order': 0, 'name': '@timestamp'},
            'message': {'order': 3, 'name': 'message'},
            'labels': {'order': 1, 'name': 'labels'},
            'tags': {'order': 2, 'name': 'tags'}
        }
        expected = [
            {'order': 0, 'name': '@timestamp'},
            {'order': 1, 'name': 'labels'},
            {'order': 2, 'name': 'tags'},
            {'order': 3, 'name': 'message'}
        ]
        result = ecs_helpers.dict_sorted_by_keys(dict, 'order')
        self.assertEqual(result, expected)
        result = ecs_helpers.dict_sorted_by_keys(dict, ['order'])
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


if __name__ == '__main__':
    unittest.main()
