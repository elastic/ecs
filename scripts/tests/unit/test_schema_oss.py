import os
import pprint
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from schema import oss
from schema import visitor


class TestSchemaOss(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    # Fallbacks

    def test_wildcard_fallback(self):
        field = {'field_details': {'name': 'myfield', 'type': 'wildcard'}}
        oss.perform_fallback(field)
        self.assertEqual('keyword', field['field_details']['type'])

    def test_version_fallback(self):
        field = {'field_details': {'name': 'myfield', 'type': 'version'}}
        oss.perform_fallback(field)
        self.assertEqual('keyword', field['field_details']['type'])

    def test_constant_keyword_fallback(self):
        field = {'field_details': {'name': 'myfield', 'type': 'constant_keyword'}}
        oss.perform_fallback(field)
        self.assertEqual('keyword', field['field_details']['type'])

    # Not falling back

    def test_basic_without_fallback(self):
        field = {'field_details': {'name': 'myfield', 'type': 'histogram'}}
        oss.perform_fallback(field)
        self.assertEqual('histogram', field['field_details']['type'])

    def test_oss_no_fallback_needed(self):
        field = {'field_details': {'name': 'myfield', 'type': 'keyword'}}
        oss.perform_fallback(field)
        self.assertEqual('keyword', field['field_details']['type'])
