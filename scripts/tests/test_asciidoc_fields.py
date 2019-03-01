import unittest
from scripts.generators import asciidoc_fields


class TestGeneratorsAsciidocFields(unittest.TestCase):

    def test_sorted_by_one_key(self):
        dict = {
                '@timestamp': { 'order': 0, 'name': '@timestamp' },
                'message': { 'order': 3, 'name': 'message' },
                'labels': { 'order': 1, 'name': 'labels' },
                'tags': { 'order': 2, 'name': 'tags' }
        }
        expected = [
                { 'order': 0, 'name': '@timestamp' },
                { 'order': 1, 'name': 'labels' },
                { 'order': 2, 'name': 'tags' },
                { 'order': 3, 'name': 'message' }
        ]
        result = asciidoc_fields.sorted_by_keys(dict, 'order')
        self.assertEqual(result, expected)
        result = asciidoc_fields.sorted_by_keys(dict, ['order'])
        self.assertEqual(result, expected)


    def test_sorted_by_multiple_keys(self):
        dict = {
                'cloud': { 'group': 2, 'name': 'cloud' },
                'agent': { 'group': 2, 'name': 'agent' },
                'base': { 'group': 1, 'name': 'base' },
        }
        expected = [
                { 'group': 1, 'name': 'base' },
                { 'group': 2, 'name': 'agent' },
                { 'group': 2, 'name': 'cloud' }
        ]
        result = asciidoc_fields.sorted_by_keys(dict, ['group', 'name'])
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
