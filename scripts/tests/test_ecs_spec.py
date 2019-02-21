import unittest
from scripts import schema_reader


class TestEcsSpec(unittest.TestCase):
    """Sanity check for things that should be true in the ECS spec."""

    def setUp(self):
        (nested, flat) = schema_reader.load_ecs()
        self.ecs_nested = nested
        self.ecs_fields = flat

    def test_base_flat_name(self):
        self.assertIsInstance(self.ecs_fields['@timestamp'], dict)
        self.assertEqual(
            self.ecs_nested['base']['fields']['@timestamp']['flat_name'],
            '@timestamp')


if __name__ == '__main__':
    unittest.main()
