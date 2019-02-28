import unittest
from scripts.generators import asciidoc_fields


class TestGeneratorsAsciidocFields(unittest.TestCase):
    # dict_add_nested

    def test_sorted_by_group(self):
        dict = {
                'agent': { 'group': 2 },
                'base': { 'group': 1 },
                'cloud': { 'group': 2 }
        }
        triples = asciidoc_fields.sorted_by_group(dict)
        expected_triples = [
                (1, 'base', { 'group': 1 }),
                (2, 'agent', { 'group': 2 }),
                (2, 'cloud', { 'group': 2 })
        ]
        self.assertEqual(triples, expected_triples)


if __name__ == '__main__':
    unittest.main()
