import unittest
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

        # user
        self.assertIn('client.user.id', all_keys)
        self.assertIn('destination.user.id', all_keys)
        self.assertIn('server.user.id', all_keys)
        self.assertIn('source.user.id', all_keys)

        # os
        self.assertIn('host.os.name', all_keys)
        self.assertIn('observer.os.name', all_keys)
        self.assertIn('user_agent.os.name', all_keys)

if __name__ == '__main__':
    unittest.main()
