import os
import sys
from typing import OrderedDict
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from scripts.generators import beats


class TestGeneratorsBeatsFields(unittest.TestCase):
    def setUp(self):
        self.df_allowlist = {"@timestamp"}

    def test_fieldset_field_array_expected_structure(self):
        fields = {
            'id': {
                'dashed_name': 'agent-id',
                'description': 'description',
                'flat_name': 'agent.id',
                'ignore_above': 1024,
                'level': 'extended',
                'name': 'agent.id',
                'normalize': [],
                'short': 'short',
                'type': 'keyword'
            }
        }
        beats_fields = beats.fieldset_field_array(fields, 'prefix')
        self.assertIsInstance(beats_fields, list)
        self.assertIsInstance(beats_fields[0], OrderedDict)

    def test_fieldset_field_array_expected_values_keyword(self):
        fields = {
            'id': {
                'dashed_name': 'agent-id',
                'description': 'description',
                'flat_name': 'agent.id',
                'ignore_above': 1024,
                'level': 'extended',
                'name': 'agent.id',
                'normalize': [],
                'short': 'short',
                'type': 'keyword'
            }
        }

        beats_fields = beats.fieldset_field_array(fields, '')
        field_entry = beats_fields[0]
        self.assertEqual(field_entry['type'], 'keyword')
        self.assertEqual(field_entry['ignore_above'], 1024)
        self.assertEqual(field_entry['name'], 'id')

    def test_fieldset_field_array_expected_values_keyword_index_false(self):
        fields = {
            'id': {
                'dashed_name': 'agent-id',
                'description': 'description',
                'flat_name': 'agent.id',
                'level': 'extended',
                'name': 'agent.id',
                'normalize': [],
                'short': 'short',
                'type': 'keyword',
                'index': False,
                'doc_values': False
            }
        }

        beats_fields = beats.fieldset_field_array(fields, '')
        field_entry = beats_fields[0]
        self.assertEqual(field_entry['type'], 'keyword')
        self.assertFalse(field_entry['index'])
        self.assertFalse(field_entry['doc_values'])


if __name__ == '__main__':
    unittest.main()
