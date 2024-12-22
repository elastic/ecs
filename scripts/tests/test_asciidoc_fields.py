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

from scripts.generators import asciidoc_fields


class TestGeneratorsAsciiFields(unittest.TestCase):

    def setUp(self):
        self.foo_fieldset = self.dummy_fieldset()
        self.event_dummy_nested_fields = self.dummy_nested_event_fieldset()

    def dummy_fieldset(self):
        return {
            'description': 'foo',
            'fields': {
                'foo.type': {
                    'dashed_name': 'foo-type',
                    'description': 'describes the foo',
                    'example': '2016-05-23T08:05:34.853Z',
                    'flat_name': 'foo.type',
                    'level': 'core',
                    'name': 'type',
                    'normalize': ['array'],
                    'short': 'describes the foo',
                    'ignore_above': 1024,
                    'type': 'keyword',
                    'allowed_values': [{
                        'description': 'fluffy foo',
                        'name': 'fluffy',
                    },
                        {
                        'description': 'coarse foo',
                        'name': 'coarse',
                    }
                    ]
                },
                'foo.id': {
                    'beta': 'this is a beta field',
                    'dashed_name': 'foo-id',
                    'description': 'Unique ID of the foo.',
                    'example': 'foo123',
                    'flat_name': 'foo.id',
                    'ignore_above': 1024,
                    'level': 'core',
                    'name': 'id',
                    'normalize': [],
                    'short': 'Unique ID of the foo.',
                    'type': 'keyword'
                }
            },
            'reusable': {
                'expected': [
                    {
                        'as': 'foo',
                        'at': 'server',
                        'full': 'server.foo'
                    },
                    {
                        'as': 'foo',
                        'at': 'source',
                        'full': 'source.foo'
                    },
                    {
                        'as': 'foo',
                        'at': 'client',
                        'full': 'client.foo',
                    },
                    {
                        'as': 'foo',
                        'at': 'destination',
                        'full': 'destination.foo'
                    }
                ],
                'top_level': False,
            },
            'reused_here': [
                {
                    'full': 'foo.as',
                    'schema_name': 'as',
                    'short': 'Fields describing an AS'
                },
                {
                    'full': 'foo.file',
                    'schema_name': 'file',
                    'short': 'Fields describing files',
                    'normalize': ['array']
                },
            ],
            'group': 2,
            'name': 'foo',
            'prefix': 'foo.',
            'short': 'Foo fields',
            'title': 'Foo',
            'type': 'group'
        }

    def dummy_nested_event_fieldset(self):
        return {
            'event': {
                'name': 'event',
                'description': 'description',
                'type': 'group',
                'title': 'Event',
                'prefix': 'event.',
                'fields': {
                    'event.kind': {
                        'dashed_name': 'event-kind',
                        'name': 'kind',
                        'allowed_values': [{
                            'description': 'fluffy foo',
                            'name': 'fluffy',
                        },
                            {
                            'description': 'coarse foo',
                            'name': 'coarse',
                            'beta': 'beta',
                        }
                        ]
                    },
                    'event.category': {
                        'dashed_name': 'event-category',
                        'name': 'category',
                        'allowed_values': [{
                            'description': 'fluffy foo',
                            'name': 'fluffy',
                        },
                            {
                            'description': 'coarse foo',
                            'name': 'coarse',
                            'beta': 'beta',
                        }
                        ]
                    },
                    'event.type': {
                        'dashed_name': 'event-type',
                        'name': 'type',
                        'allowed_values': [{
                            'description': 'fluffy foo',
                            'name': 'fluffy',
                        },
                            {
                            'description': 'coarse foo',
                            'name': 'coarse',
                            'beta': 'beta',
                        }
                        ]
                    },
                    'event.outcome': {
                        'dashed_name': 'event-outcome',
                        'name': 'outcome',
                        'allowed_values': [{
                            'description': 'fluffy foo',
                            'name': 'fluffy',
                        },
                            {
                            'description': 'coarse foo',
                            'name': 'coarse',
                            'beta': 'beta',
                        }
                        ]
                    }
                }
            }
        }

    def test_validate_sort_fieldset(self):
        sorted_foo_fields = asciidoc_fields.sort_fields(self.foo_fieldset)
        # import pdb;pdb.set_trace()
        self.assertIsInstance(sorted_foo_fields, list)

        # `allowed_value_names` always present
        for field in sorted_foo_fields:
            self.assertIsInstance(field.get('allowed_value_names'), list)

        self.assertFalse(sorted_foo_fields[0]['allowed_value_names'])
        self.assertEqual('id', sorted_foo_fields[0]['name'])
        self.assertEqual('type', sorted_foo_fields[1]['name'])
        self.assertIn('fluffy', sorted_foo_fields[1]['allowed_value_names'])
        self.assertIn('coarse', sorted_foo_fields[1]['allowed_value_names'])

    def test_rendering_fieldset_reuse(self):
        foo_reuse_fields = asciidoc_fields.render_fieldset_reuse_text(self.foo_fieldset)
        expected_sorted_reuse_fields = (
            'client.foo',
            'destination.foo',
            'server.foo',
            'source.foo'
        )

        self.assertEqual(expected_sorted_reuse_fields, tuple(foo_reuse_fields))

    def test_rendering_fieldset_nesting(self):
        foo_nesting_fields = asciidoc_fields.render_nestings_reuse_section(self.foo_fieldset)
        self.assertIsInstance(foo_nesting_fields, list)
        self.assertEqual('foo.as.*', foo_nesting_fields[0]['flat_nesting'])
        self.assertEqual('as', foo_nesting_fields[0]['name'])
        self.assertEqual('Fields describing an AS', foo_nesting_fields[0]['short'])

        self.assertEqual('foo.file.*', foo_nesting_fields[1]['flat_nesting'])
        self.assertEqual('file', foo_nesting_fields[1]['name'])
        self.assertEqual('Fields describing files', foo_nesting_fields[1]['short'])
        self.assertEqual(['array'], foo_nesting_fields[1]['normalize'])

    def test_check_for_usage_doc_true(self):
        usage_files = ["foo.asciidoc"]
        foo_name = self.foo_fieldset.get('name')
        self.assertTrue(asciidoc_fields.check_for_usage_doc(foo_name, usage_file_list=usage_files))

    def test_check_for_usage_doc_false(self):
        usage_files = ["notfoo.asciidoc"]
        foo_name = self.foo_fieldset.get('name')
        self.assertFalse(asciidoc_fields.check_for_usage_doc(foo_name, usage_file_list=usage_files))

    def test_check_for_page_field_value_rendering(self):
        rendered_field_values = asciidoc_fields.page_field_values(self.event_dummy_nested_fields)
        self.assertIn('beta', rendered_field_values)


if __name__ == '__main__':
    unittest.main()
