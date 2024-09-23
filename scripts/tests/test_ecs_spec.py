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
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.schema import loader
from scripts.schema import cleaner
from scripts.schema import finalizer
from scripts.generators import intermediate_files


class TestEcsSpec(unittest.TestCase):
    """Sanity check for things that should be true in the ECS spec."""

    @classmethod
    def setUpClass(cls):
        fields = loader.load_schemas()
        cleaner.clean(fields)
        finalizer.finalize(fields)
        cls.ecs_nested = intermediate_files.generate_nested_fields(fields)
        cls.ecs_fields = intermediate_files.generate_flat_fields(fields)

    def setUp(self):
        self.ecs_nested = TestEcsSpec.ecs_nested
        self.ecs_fields = TestEcsSpec.ecs_fields

    def test_base_flat_name(self):
        self.assertIn('@timestamp', self.ecs_fields)
        self.assertIn('@timestamp', self.ecs_nested['base']['fields'])
        self.assertEqual(
            self.ecs_nested['base']['fields']['@timestamp']['flat_name'],
            '@timestamp')

    def test_root_fieldsets_can_have_nested_keys(self):
        self.assertIn('trace.id', self.ecs_fields)
        self.assertIn('transaction.id', self.ecs_fields)
        self.assertIn('trace.id', self.ecs_nested['tracing']['fields'])
        self.assertIn('transaction.id', self.ecs_nested['tracing']['fields'])

    def test_flat_includes_reusable_fields(self):
        all_keys = sorted(self.ecs_fields.keys())

        # geo
        self.assertIn('client.geo.name', all_keys)
        self.assertIn('destination.geo.name', all_keys)
        self.assertIn('host.geo.name', all_keys)
        self.assertIn('observer.geo.name', all_keys)
        self.assertIn('server.geo.name', all_keys)
        self.assertIn('source.geo.name', all_keys)

        # group
        self.assertIn('user.group.name', all_keys)
        self.assertIn('client.user.group.id', all_keys)
        self.assertIn('destination.user.group.id', all_keys)
        self.assertIn('server.user.group.id', all_keys)
        self.assertIn('source.user.group.id', all_keys)

        # user
        self.assertIn('client.user.id', all_keys)
        self.assertIn('destination.user.id', all_keys)
        self.assertIn('server.user.id', all_keys)
        self.assertIn('source.user.id', all_keys)

        # os
        self.assertIn('host.os.name', all_keys)
        self.assertIn('observer.os.name', all_keys)
        self.assertIn('user_agent.os.name', all_keys)

    def test_nested_includes_reusable_fields(self):
        client_keys = sorted(self.ecs_nested['client']['fields'].keys())
        destination_keys = sorted(self.ecs_nested['destination']['fields'].keys())
        host_keys = sorted(self.ecs_nested['host']['fields'].keys())
        observer_keys = sorted(self.ecs_nested['observer']['fields'].keys())
        server_keys = sorted(self.ecs_nested['server']['fields'].keys())
        source_keys = sorted(self.ecs_nested['source']['fields'].keys())
        user_agent_keys = sorted(self.ecs_nested['user_agent']['fields'].keys())
        user_keys = sorted(self.ecs_nested['user']['fields'].keys())

        # geo
        self.assertIn('client.geo.name', client_keys)
        self.assertIn('destination.geo.name', destination_keys)
        self.assertIn('host.geo.name', host_keys)
        self.assertIn('observer.geo.name', observer_keys)
        self.assertIn('server.geo.name', server_keys)
        self.assertIn('source.geo.name', source_keys)

        # group (chained reuses)
        self.assertIn('user.group.name', user_keys)
        self.assertIn('client.user.group.id', client_keys)
        self.assertIn('destination.user.group.id', destination_keys)
        self.assertIn('server.user.group.id', server_keys)
        self.assertIn('source.user.group.id', source_keys)

        # user
        self.assertIn('client.user.id', client_keys)
        self.assertIn('destination.user.id', destination_keys)
        self.assertIn('server.user.id', server_keys)
        self.assertIn('source.user.id', source_keys)

        # os
        self.assertIn('host.os.name', host_keys)
        self.assertIn('observer.os.name', observer_keys)
        self.assertIn('user_agent.os.name', user_agent_keys)

    def test_related_fields_always_arrays(self):
        for (field_name, field) in self.ecs_nested['related']['fields'].items():
            self.assertIn('normalize', field.keys())
            self.assertIn('array', field['normalize'],
                          "All fields under `related.*` should be arrays")

    def test_normalize_always_array(self):
        for (field_name, field) in self.ecs_fields.items():
            self.assertIsInstance(field.get('normalize'), list, field_name)

    def test_valid_type(self):
        valid_types = ['binary',
                       'boolean',
                       'keyword',
                       'constant_keyword',
                       'wildcard',
                       'long',
                       'integer',
                       'short',
                       'byte',
                       'double',
                       'float',
                       'half_float',
                       'scaled_float',
                       'unsigned_long',
                       'date',
                       'date_nanos',
                       'alias',
                       'object',
                       'flattened',
                       'nested',
                       'join',
                       'long_range',
                       'double_range',
                       'date_range',
                       'ip',
                       'text',
                       'match_only_text',
                       'geo_point',
                       'geo_shape',
                       'point',
                       'shape']
        for (field_name, field) in self.ecs_fields.items():
            self.assertIn(field.get('type'), valid_types, field_name)


if __name__ == '__main__':
    unittest.main()
