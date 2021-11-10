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
        beats_fields = beats.fieldset_field_array(fields, self.df_allowlist, 'prefix')
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

        beats_fields = beats.fieldset_field_array(fields, self.df_allowlist, '')
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

        beats_fields = beats.fieldset_field_array(fields, self.df_allowlist, '')
        field_entry = beats_fields[0]
        self.assertEqual(field_entry['type'], 'keyword')
        self.assertFalse(field_entry['index'])
        self.assertFalse(field_entry['doc_values'])


if __name__ == '__main__':
    unittest.main()
