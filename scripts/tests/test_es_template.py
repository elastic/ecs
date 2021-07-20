import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.generators import es_template


class TestGeneratorsEsTemplate(unittest.TestCase):
    # dict_add_nested

    def test_add_not_nested(self):
        dict = {}
        es_template.dict_add_nested(dict, ['field1'], {'field': 'details'})
        self.assertEqual(dict, {'field1': {'field': 'details'}})

    def test_dict_add_nested(self):
        dict = {}
        es_template.dict_add_nested(dict, ['parent_field', 'leaf_field'], {'field': 'details'})
        self.assertEqual(dict, {'parent_field': {'properties': {'leaf_field': {'field': 'details'}}}})

    def test_add_siblings(self):
        dict = {'field1': {'field': 'details 1'},
                'field2': {'properties': {'leaf1': {'field': 'details 2-1'}}}}
        es_template.dict_add_nested(dict, ['field3'], {'field': 'details 3'})
        es_template.dict_add_nested(dict, ['field2', 'leaf2'], {'field': 'details 2-2'})
        self.assertEqual(dict, {
            'field1': {'field': 'details 1'},
            'field2': {'properties': {
                'leaf1': {'field': 'details 2-1'},
                'leaf2': {'field': 'details 2-2'}
            }},
            'field3': {'field': 'details 3'}
        })

    def test_dict_add_nested_to_explicit_object(self):
        dict = {'answers': {'type': 'object'}}
        es_template.dict_add_nested(dict, ['answers', 'ttl'], {'type': 'long'})
        self.assertEqual(dict, {'answers': {'type': 'object', 'properties': {'ttl': {'type': 'long'}}}})

    def test_dict_add_nested_shouldnt_clobber_with_objects(self):
        dict = {'answers': {'properties': {'ttl': {'type': 'long'}}}}
        es_template.dict_add_nested(dict, ['answers'], {'type': 'object'})
        self.assertEqual(dict, {'answers': {'properties': {'ttl': {'type': 'long'}}}})

    def test_entry_for_adds_enabled_field(self):
        test_map = {
            'other': 'some data',
            'type': 'object',
            'enabled': False,
        }

        exp = {
            'type': 'object',
            'enabled': False,
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_enabled_true_ignored(self):
        test_map = {
            'other': 'some data',
            'type': 'object',
            'enabled': True,
        }

        exp = {
            'type': 'object',
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_enabled_with_index(self):
        test_map = {
            'other': 'some data',
            'type': 'object',
            'enabled': False,
            'index': False
        }

        exp = {
            'type': 'object',
            'enabled': False,
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_enabled_nested(self):
        test_map = {
            'other': 'some data',
            'type': 'nested',
            'enabled': False,
        }

        exp = {
            'type': 'nested',
            'enabled': False,
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_index(self):
        test_map = {
            'other': 'some data',
            'type': 'keyword',
            'index': False,
        }

        exp = {
            'type': 'keyword',
            'index': False,
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_alias(self):
        test_map = {
            'name': 'test.alias',
            'type': 'alias',
            'path': 'alias.target'
        }

        exp = {
            'type': 'alias',
            'path': 'alias.target'
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_entry_for_scaled_float(self):
        test_map = {
            'name': 'test.scaled_float',
            'type': 'scaled_float',
            'scaling_factor': 1000
        }

        exp = {
            'type': 'scaled_float',
            'scaling_factor': 1000
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_constant_keyword_with_value(self):
        test_map = {
            'name': 'field_with_value',
            'type': 'constant_keyword',
            'value': 'foo'
        }

        exp = {
            'type': 'constant_keyword',
            'value': 'foo'
        }
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_constant_keyword_no_value(self):
        test_map = {
            'name': 'field_without_value',
            'type': 'constant_keyword'
        }

        exp = {'type': 'constant_keyword'}
        self.assertEqual(es_template.entry_for(test_map), exp)

    def test_es6_fallback_base_case_wildcard(self):
        test_map = {
            "field": {
                "name": "field",
                "type": "wildcard"
            }
        }

        exp = {
            "field": {
                "name": "field",
                "type": "keyword",
                "ignore_above": 1024
            }
        }

        es_template.es6_type_fallback(test_map)
        self.assertEqual(test_map, exp)

    def test_es6_fallback_recursive_case_wildcard(self):
        test_map = {
            "top_field": {
                "properties": {
                    "field": {
                        "name": "field",
                        "type": "wildcard"
                    }
                }
            }
        }

        exp = {
            "top_field": {
                "properties": {
                    "field": {
                        "name": "field",
                        "type": "keyword",
                        "ignore_above": 1024
                    }
                }
            }
        }

        es_template.es6_type_fallback(test_map)
        self.assertEqual(test_map, exp)

    def test_es6_fallback_base_case_constant_keyword(self):
        test_map = {
            "field": {
                "name": "field",
                "type": "constant_keyword"
            }
        }

        exp = {
            "field": {
                "name": "field",
                "type": "keyword",
                "ignore_above": 1024
            }
        }

        es_template.es6_type_fallback(test_map)
        self.assertEqual(test_map, exp)

    def test_es6_fallback_base_case_match_only_text(self):
        test_map = {
            "field": {
                "name": "field",
                "type": "match_only_text"
            }
        }

        exp = {
            "field": {
                "name": "field",
                "type": "text",
                "norms": False
            }
        }

        es_template.es6_type_fallback(test_map)
        self.assertEqual(test_map, exp)

    def test_es6_fallback_recursive_case_match_only_text(self):
        test_map = {
            "top_field": {
                "properties": {
                    "field": {
                        "name": "field",
                        "type": "match_only_text"
                    }
                }
            }
        }

        exp = {
            "top_field": {
                "properties": {
                    "field": {
                        "name": "field",
                        "type": "text",
                        "norms": False
                    }
                }
            }
        }

        es_template.es6_type_fallback(test_map)
        self.assertEqual(test_map, exp)

    def test_es6_fallback_multifield_base_match_only_text(self):
        test_map = {
            "field": {
                "name": "field",
                "fields": {
                    "text": {
                        "type": "match_only_text"
                    }
                }
            }
        }

        exp = {
            "field": {
                "name": "field",
                "fields": {
                    "text": {
                        "type": "text",
                        "norms": False
                    }
                }
            }
        }

        es_template.es6_type_fallback(test_map)
        self.assertEqual(test_map, exp)

    def test_es6_fallback_multifield_recursive_match_only_text(self):
        test_map = {
            "top_field": {
                "properties": {
                    "field": {
                        "fields": {
                            "text": {
                                "type": "match_only_text"
                            }
                        }
                    }
                }
            }
        }

        exp = {
            "top_field": {
                "properties": {
                    "field": {
                        "fields": {
                            "text": {
                                "type": "text",
                                "norms": False
                            }
                        }
                    }
                }
            }
        }

        es_template.es6_type_fallback(test_map)
        self.assertEqual(test_map, exp)

    def test_component_composable_template_name(self):
        version = "1.8"
        test_map = {
            "Acme": {
                "name": "Acme",
            }
        }

        exp = ["ecs_{}_acme".format(version)]
        self.assertEqual(es_template.component_name_convention(version, test_map), exp)


if __name__ == '__main__':
    unittest.main()
