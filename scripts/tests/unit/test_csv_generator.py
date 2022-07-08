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

import mock
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from generators import csv_generator


class TestGeneratorsCsvFields(unittest.TestCase):
    def test_base_first(self):
        fields = {
            '@timestamp': {
                'dashed_name': 'timestamp'
            },
            'host.name': {
                'dashed_name': 'host-name'
            }
        }
        sorted_base_first = csv_generator.base_first(fields)
        self.assertIsInstance(sorted_base_first, list)
        self.assertIsInstance(sorted_base_first[0], dict)
        self.assertEqual(sorted_base_first[0].get('dashed_name'), 'timestamp')

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch('generators.csv_generator.csv')
    def test_csv_writing(self, mock_csv, _):
        mock_csv.writer = mock.Mock(writerow=mock.Mock())
        fields = [{
            'example': '2016-05-23T08:05:34.853Z',
            'flat_name': '@timestamp',
            'level': 'core',
            'name': '@timestamp',
            'normalize': [],
            'required': True,
            'short': 'Date/time when the event originated.',
            'type': 'date'
        }]

        csv_generator.save_csv('ecs.csv', fields, '0.0.1')

        self.assertEqual(mock_csv.writer.call_count, 1)
        self.assertEqual(mock_csv.writer().writerow.call_count, 2)
        mock_csv.writer().writerow.assert_has_calls([
            mock.call(['ECS_Version', 'Indexed', 'Field_Set', 'Field', 'Type',
                      'Level', 'Normalization', 'Example', 'Description']),
            mock.call(['0.0.1', 'true', 'base', '@timestamp', 'date', 'core', '',
                      '2016-05-23T08:05:34.853Z', 'Date/time when the event originated.'])
        ])
