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
import pprint
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from schema import finalizer


class TestSchemaFinalizer(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def schema_base(self):
        return {
            'base': {
                'schema_details': {
                    'title': 'Base',
                    'root': True,
                },
                'field_details': {
                    'name': 'base',
                    'node_name': 'base',
                    'short': 'short desc',
                },
                'fields': {
                    '@timestamp': {
                        'field_details': {
                            'name': '@timestamp',
                            'node_name': '@timestamp',
                        }
                    },
                }
            }
        }

    def schema_process(self):
        return {
            'process': {
                'schema_details': {
                    'title': 'Process',
                    'root': False,
                    'reusable': {
                        'top_level': True,
                        'order': 2,
                        'expected': [
                            {'full': 'process.parent', 'at': 'process', 'as': 'parent',
                                'short_override': 'short override desc'},
                            {'full': 'process.previous', 'at': 'process', 'as': 'previous', 'normalize': ['array']},
                            {'full': 'reuse.process', 'at': 'reuse', 'as': 'process'},
                            {'full': 'reuse.process.parent', 'at': 'reuse.process', 'as': 'parent'},
                            {'full': 'reuse.process.target', 'at': 'reuse.process', 'as': 'target'},
                            {'full': 'reuse.process.target.parent', 'at': 'reuse.process.target', 'as': 'parent'}
                        ]
                    }
                },
                'field_details': {
                    'name': 'process',
                    'node_name': 'process',
                    'short': 'short desc',
                },
                'fields': {
                    'pid': {
                        'field_details': {
                            'name': 'pid',
                            'node_name': 'pid',
                        }
                    },
                    'thread': {
                        'field_details': {
                            'name': 'thread',
                            'node_name': 'thread',
                        },
                        'fields': {
                            'id': {
                                'field_details': {
                                    'name': 'thread.id',
                                    'node_name': 'id',
                                }
                            }
                        }
                    }
                }
            }
        }

    def schema_user(self):
        return {
            'user': {
                'schema_details': {
                    'root': False,
                    'reusable': {
                        'top_level': True,
                        'order': 2,
                        'expected': [
                            {'full': 'server.user', 'at': 'server', 'as': 'user'},
                            {'full': 'user.target', 'at': 'user', 'as': 'target', 'beta': 'Some beta notice'},
                            {'full': 'user.effective', 'at': 'user', 'as': 'effective'},
                        ]
                    }
                },
                'field_details': {
                    'name': 'user',
                    'node_name': 'user',
                    'type': 'group',
                    'short': 'short desc',
                },
                'fields': {
                    'name': {
                        'field_details': {
                            'name': 'name',
                            'node_name': 'name',
                        }
                    },
                    'full_name': {
                        'field_details': {
                            'name': 'full_name',
                            'node_name': 'full_name',
                            'multi_fields': [
                                {'name': 'text', 'type': 'text'}
                            ]
                        }
                    },
                }
            }
        }

    def schema_server(self):
        return {
            'server': {
                'schema_details': {'root': False},
                'field_details': {
                    'name': 'server',
                    'node_name': 'server',
                    'type': 'group',
                    'short': 'short desc',
                },
                'fields': {
                    'ip': {
                        'field_details': {
                            'name': 'ip',
                            'node_name': 'ip',
                            'type': 'ip'
                        }
                    }
                }
            }
        }

    def schema_process_reuse(self):
        return {
            'reuse': {
                'schema_details': {
                    'title': 'Reuse',
                    'root': False
                },
                'field_details': {
                    'name': 'Reuse',
                    'node_name': 'Reuse',
                    'short': 'reuse example',
                },
                'fields': {
                    'pid': {
                        'field_details': {
                            'name': 'pid',
                            'node_name': 'pid',
                        }
                    }
                }
            }
        }

    # perform_reuse

    def test_perform_reuse_with_foreign_reuse_and_self_reuse(self):
        fields = {**self.schema_user(), **self.schema_server(), **self.schema_process(), **self.schema_process_reuse()}
        # If the test had multiple foreign destinations for user fields, we could compare them together instead
        finalizer.perform_reuse(fields)
        process_fields = fields['process']['fields']
        server_fields = fields['server']['fields']
        user_fields = fields['user']['fields']
        process_reuse_fields = fields['reuse']['fields']['process']['fields']
        process_target_reuse_fields = fields['reuse']['fields']['process']['fields']['target']['fields']
        # Expected reuse
        self.assertIn('parent', process_fields)
        self.assertIn('previous', process_fields)
        self.assertIn('user', server_fields)
        self.assertIn('target', user_fields)
        self.assertIn('effective', user_fields)
        self.assertIn('parent', process_reuse_fields)
        self.assertIn('parent', process_target_reuse_fields)
        # Sanity check for presence of leaf fields, after performing reuse
        self.assertIn('name', user_fields['target']['fields'])
        self.assertIn('name', user_fields['effective']['fields'])
        self.assertIn('name', server_fields['user']['fields'])
        self.assertIn('pid', process_fields['parent']['fields'])
        self.assertIn('pid', process_reuse_fields['parent']['fields'])
        self.assertIn('pid', process_target_reuse_fields['parent']['fields'])
        # Ensure the parent field of reused fields is marked as intermediate
        self.assertTrue(server_fields['user']['field_details']['intermediate'])
        self.assertTrue(process_fields['parent']['field_details']['intermediate'])
        self.assertTrue(user_fields['target']['field_details']['intermediate'])
        self.assertTrue(user_fields['effective']['field_details']['intermediate'])
        self.assertTrue(process_reuse_fields['parent']['field_details']['intermediate'])
        self.assertTrue(process_target_reuse_fields['parent']['field_details']['intermediate'])
        # No unexpected cross-nesting
        self.assertNotIn('target', user_fields['target']['fields'])
        self.assertNotIn('target', user_fields['effective']['fields'])
        self.assertNotIn('target', server_fields['user']['fields'])
        # Legacy list of nestings, added to destination schema
        self.assertIn('process.parent', fields['process']['schema_details']['nestings'])
        self.assertIn('process.previous', fields['process']['schema_details']['nestings'])
        self.assertIn('user.effective', fields['user']['schema_details']['nestings'])
        self.assertIn('user.target', fields['user']['schema_details']['nestings'])
        self.assertIn('server.user', fields['server']['schema_details']['nestings'])
        self.assertIn('reuse.process.parent', fields['reuse']['schema_details']['nestings'])
        self.assertIn('reuse.process.target.parent', fields['reuse']['schema_details']['nestings'])
        # Attribute 'reused_here' lists nestings inside a destination schema
        self.assertIn({'full': 'process.parent', 'schema_name': 'process', 'short': 'short override desc'},
                      fields['process']['schema_details']['reused_here'])
        self.assertIn({'full': 'process.previous', 'schema_name': 'process', 'short': 'short desc', 'normalize': ['array']},
                      fields['process']['schema_details']['reused_here'])
        self.assertIn({'full': 'user.effective', 'schema_name': 'user', 'short': 'short desc'},
                      fields['user']['schema_details']['reused_here'])
        self.assertIn({'full': 'user.target', 'schema_name': 'user', 'short': 'short desc', 'beta': 'Some beta notice'},
                      fields['user']['schema_details']['reused_here'])
        self.assertIn({'full': 'server.user', 'schema_name': 'user', 'short': 'short desc'},
                      fields['server']['schema_details']['reused_here'])
        self.assertIn({'full': 'reuse.process.parent', 'schema_name': 'process', 'short': 'short desc'},
                      fields['reuse']['schema_details']['reused_here'])
        self.assertIn({'full': 'reuse.process.target.parent', 'schema_name': 'process', 'short': 'short desc'},
                      fields['reuse']['schema_details']['reused_here'])
        # Reused fields have an indication they're reused
        self.assertEqual(process_fields['parent']['field_details']['original_fieldset'], 'process',
                         "The parent field of reused fields should have 'original_fieldset' populated")
        self.assertEqual(process_fields['parent']['fields']['pid']['field_details']['original_fieldset'], 'process',
                         "Leaf fields of reused fields for self-nested fields should have 'original_fieldset'")
        self.assertEqual(server_fields['user']['field_details']['original_fieldset'], 'user',
                         "The parent field of foreign reused fields should have 'original_fieldset' populated")
        self.assertEqual(server_fields['user']['fields']['name']['field_details']['original_fieldset'], 'user')
        self.assertEqual(process_reuse_fields['parent']['field_details']['original_fieldset'], 'process',
                         "The parent field of reused fields should have 'original_fieldset' populated")
        self.assertEqual(process_target_reuse_fields['parent']['field_details']['original_fieldset'], 'process',
                         "The parent field of reused fields should have 'original_fieldset' populated")
        # Original fieldset's fields must not be marked with 'original_fieldset='
        self.assertNotIn('original_fieldset', user_fields['name']['field_details'])
        self.assertNotIn('original_fieldset', process_fields['pid']['field_details'])

    def test_root_schema_cannot_be_reused_nor_have_field_set_reused_in_it(self):
        reused_schema = {
            'schema_details': {'reusable': {'expected': ['foo']}},
            'field_details': {'name': 'reused_schema'}
        }
        destination_schema = {
            'schema_details': {'reusable': {'expected': ['foo']}},
            'field_details': {'name': 'destination_schema'}
        }
        # test root=true on reused
        reused_schema['schema_details']['root'] = True
        # foreign reuse
        with self.assertRaisesRegex(ValueError, 'reused_schema.*root.*cannot be reused'):
            finalizer.ensure_valid_reuse(reused_schema, destination_schema)
        # self-nesting
        with self.assertRaisesRegex(ValueError, 'reused_schema.*root.*cannot be reused'):
            finalizer.ensure_valid_reuse(reused_schema)
        # test root=true on destination
        reused_schema['schema_details']['root'] = False
        destination_schema['schema_details']['root'] = True
        with self.assertRaisesRegex(ValueError, 'destination_schema.*root.*cannot'):
            finalizer.ensure_valid_reuse(reused_schema, destination_schema)

    # calculate_final_values

    def test_calculate_final_values(self):
        fields = {**self.schema_base(), **self.schema_user(), **self.schema_server()}
        finalizer.perform_reuse(fields)
        finalizer.calculate_final_values(fields)
        base_fields = fields['base']['fields']
        server_fields = fields['server']['fields']
        user_fields = fields['user']['fields']
        # Pre-calculated path-based values
        # root=true
        timestamp_details = base_fields['@timestamp']['field_details']
        self.assertEqual(timestamp_details['flat_name'], '@timestamp',
                         "Field sets with root=true must not namespace field names with the field set's name")
        self.assertEqual(timestamp_details['dashed_name'], 'timestamp')
        # root=false
        self.assertEqual(server_fields['ip']['field_details']['flat_name'], 'server.ip',
                         "Field sets with root=false must namespace field names with the field set's name")
        self.assertEqual(server_fields['ip']['field_details']['dashed_name'], 'server-ip')
        # reused
        server_user_name_details = server_fields['user']['fields']['name']['field_details']
        self.assertEqual(server_user_name_details['flat_name'], 'server.user.name')
        self.assertEqual(server_user_name_details['dashed_name'], 'server-user-name')
        # self-nestings
        user_target_name_details = user_fields['target']['fields']['name']['field_details']
        self.assertEqual(user_target_name_details['flat_name'], 'user.target.name')
        self.assertEqual(user_target_name_details['dashed_name'], 'user-target-name')
        # multi-fields flat_name
        user_full_name_details = user_fields['full_name']['field_details']
        self.assertEqual(user_full_name_details['multi_fields'][0]['flat_name'], 'user.full_name.text')

    def test_dashed_name_cleanup(self):
        details = {'field_details': {'node_name': '@time.stamp_'}}
        finalizer.field_finalizer(details, [])
        self.assertEqual(details['field_details']['dashed_name'], 'time-stamp-')

    # field_group_at_path

    def test_field_group_at_path_root_destination(self):
        all_fields = self.schema_server()
        fields = finalizer.field_group_at_path('server', all_fields)
        self.assertIn('ip', fields.keys(),
                      "should return the dictionary of server fields")

    def test_field_group_at_path_find_nested_destination(self):
        all_fields = self.schema_process()
        fields = finalizer.field_group_at_path('process.thread', all_fields)
        self.assertIn('id', fields.keys(),
                      "should return the dictionary of process.thread fields")
        self.assertEqual('thread.id', fields['id']['field_details']['name'])

    def test_field_group_at_path_missing_nested_path(self):
        all_fields = self.schema_server()
        with self.assertRaisesRegex(ValueError, "Field server.nonexistent not found"):
            finalizer.field_group_at_path('server.nonexistent', all_fields)

    def test_field_group_at_path_leaf_field_not_field_group(self):
        all_fields = self.schema_server()
        with self.assertRaisesRegex(ValueError, "Field server\.ip \(type ip\) already exists"):
            finalizer.field_group_at_path('server.ip', all_fields)

    def test_field_group_at_path_for_leaf_object_field_creates_the_section(self):
        all_fields = {
            'network': {
                'field_details': {
                    'name': 'network',
                },
                'fields': {
                    'ingress': {
                        'field_details': {
                            'name': 'network.ingress',
                            'type': 'object'
                        }
                    }
                }
            }
        }
        ingress_subfields = finalizer.field_group_at_path('network.ingress', all_fields)
        self.assertEqual(ingress_subfields, {})
        self.assertEqual(all_fields['network']['fields']['ingress']['fields'], {})
