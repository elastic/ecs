import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts import schema_reader


class TestSchemaReader(unittest.TestCase):

    # File loading stuff

    # Validation

    # Generic helpers

    def test_clean_string_values(self):
        dict = {'dirty': ' space, the final frontier  ', 'clean': 'val', 'int': 1}
        schema_reader.dict_clean_string_values(dict)
        self.assertEqual(dict, {'dirty': 'space, the final frontier', 'clean': 'val', 'int': 1})

    # In memory representation

    # schemas

    def test_schema_set_fieldset_prefix_at_root(self):
        schema = {'root': True, 'name': 'myfieldset'}
        schema_reader.schema_set_fieldset_prefix(schema)
        self.assertEqual(schema,
                         {'prefix': '', 'root': True, 'name': 'myfieldset'})

    def test_schema_set_fieldset_prefix_root_unspecified(self):
        schema = {'name': 'myfieldset'}
        schema_reader.schema_set_fieldset_prefix(schema)
        self.assertEqual(schema,
                         {'prefix': 'myfieldset.', 'name': 'myfieldset'})

    def test_schema_set_fieldset_prefix_not_at_root(self):
        schema = {'root': False, 'name': 'myfieldset'}
        schema_reader.schema_set_fieldset_prefix(schema)
        self.assertEqual(schema,
                         {'prefix': 'myfieldset.', 'root': False, 'name': 'myfieldset'})

    def test_set_default_values_defaults(self):
        schema = {'description': '...'}
        schema_reader.schema_set_default_values(schema)
        self.assertEqual(schema, {'group': 2, 'type': 'group', 'description': '...', 'short': '...'})

    def test_set_default_values_no_overwrite(self):
        schema = {'group': 1, 'description': '...'}
        schema_reader.schema_set_default_values(schema)
        self.assertEqual(schema, {'group': 1, 'type': 'group', 'description': '...', 'short': '...'})

    # field definitions

    def test_field_set_defaults_no_short(self):
        field = {'description': 'a field', 'type': 'faketype'}
        schema_reader.field_set_defaults(field)
        self.assertEqual(field, {'description': 'a field', 'short': 'a field', 'type': 'faketype'})

    def test_field_set_flat_name_nested(self):
        nested = {'name': 'nested'}
        schema_reader.field_set_flat_name(nested, 'parent.')
        self.assertEqual(nested, {'name': 'nested', 'flat_name': 'parent.nested'})

    def test_field_set_flat_name_root(self):
        nested = {'name': 'root_field'}
        schema_reader.field_set_flat_name(nested, '')
        self.assertEqual(nested, {'name': 'root_field', 'flat_name': 'root_field'})

    def test_field_cleanup_values(self):
        field = {'name': 'myfield', 'type': 'faketype', 'description': 'a field   '}
        schema_reader.field_cleanup_values(field, 'event.')
        expected = {
            'name': 'myfield',
            'type': 'faketype',
            'flat_name': 'event.myfield',
            'description': 'a field',
            'short': 'a field'
        }
        self.assertEqual(field, expected)

    def test_field_set_multi_field_defaults_missing_name(self):
        field = {
            'name': 'myfield',
            'flat_name': 'myfieldset.myfield',
            'multi_fields': [
                    {'type': 'text'}
            ]
        }
        schema_reader.field_set_multi_field_defaults(field)
        expected = {
            'name': 'myfield',
            'flat_name': 'myfieldset.myfield',
            'multi_fields': [{
                    'name': 'text',
                    'type': 'text',
                    'flat_name': 'myfieldset.myfield.text',
            }]
        }
        self.assertEqual(field, expected)


if __name__ == '__main__':
    unittest.main()
