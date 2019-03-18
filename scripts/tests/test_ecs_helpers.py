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


if __name__ == '__main__':
    unittest.main()
