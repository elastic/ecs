import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts import schema_reader
from generators import ecs_helpers


class TestEcsSpec(unittest.TestCase):
    """Sanity check for things that should be true in the ECS spec."""

    def setUp(self):
        versions = ['master', 'v1.5.0']
        self.ecs_nested_schemas = []
        self.ecs_flat_schemas = []
        for version in versions:
            tree = ecs_helpers.get_git_tree(version)
            schemas = schema_reader.load_schemas_from_git(tree)
            intermediate_schemas = schema_reader.create_schema_dicts(schemas)
            schema_reader.assemble_reusables(intermediate_schemas)
            (nested, flat) = schema_reader.generate_nested_flat(intermediate_schemas)
            self.ecs_nested_schemas.append(nested)
            self.ecs_flat_schemas.append(flat)

    def test_base_flat_name(self):
        for flat_schema in self.ecs_flat_schemas:
            self.assertIsInstance(flat_schema['@timestamp'], dict)
        for nested_schema in self.ecs_nested_schemas:
            self.assertEqual(
                nested_schema['base']['fields']['@timestamp']['flat_name'],
                '@timestamp')

    def test_flat_includes_reusable_fields(self):
        for flat_schema in self.ecs_flat_schemas:
            all_keys = sorted(flat_schema.keys())

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
        for nested_schema in self.ecs_nested_schemas:
            client_keys = sorted(nested_schema['client']['fields'].keys())
            destination_keys = sorted(nested_schema['destination']['fields'].keys())
            host_keys = sorted(nested_schema['host']['fields'].keys())
            observer_keys = sorted(nested_schema['observer']['fields'].keys())
            server_keys = sorted(nested_schema['server']['fields'].keys())
            source_keys = sorted(nested_schema['source']['fields'].keys())
            user_agent_keys = sorted(nested_schema['user_agent']['fields'].keys())
            user_keys = sorted(nested_schema['user']['fields'].keys())

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

    def test_related_fields_always_arrays(self):
        for nested_schema in self.ecs_nested_schemas:
            for (field_name, field) in nested_schema['related']['fields'].items():
                self.assertIn('normalize', field.keys())
                self.assertIn('array', field['normalize'],
                              "All fields under `related.*` should be arrays")


if __name__ == '__main__':
    unittest.main()
