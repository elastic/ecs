import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts import schema_reader


(nested, flat) = schema_reader.load_ecs()


class TestEcsSpec(unittest.TestCase):
    """Sanity check for things that should be true in the ECS spec."""

    def setUp(self):
        global nested
        global flat
        self.ecs_nested = nested
        self.ecs_fields = flat

    def test_base_flat_name(self):
        self.assertIsInstance(self.ecs_fields['@timestamp'], dict)
        self.assertEqual(
            self.ecs_nested['base']['fields']['@timestamp']['flat_name'],
            '@timestamp')

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
        self.assertIn('geo.name', client_keys)
        self.assertIn('geo.name', destination_keys)
        self.assertIn('geo.name', host_keys)
        self.assertIn('geo.name', observer_keys)
        self.assertIn('geo.name', server_keys)
        self.assertIn('geo.name', source_keys)

        # group
        self.assertIn('group.name', user_keys)
        self.assertIn('user.group.id', client_keys)
        self.assertIn('user.group.id', destination_keys)
        self.assertIn('user.group.id', server_keys)
        self.assertIn('user.group.id', source_keys)

        # user
        self.assertIn('user.id', client_keys)
        self.assertIn('user.id', destination_keys)
        self.assertIn('user.id', server_keys)
        self.assertIn('user.id', source_keys)

        # os
        self.assertIn('os.name', host_keys)
        self.assertIn('os.name', observer_keys)
        self.assertIn('os.name', user_agent_keys)


if __name__ == '__main__':
    unittest.main()
