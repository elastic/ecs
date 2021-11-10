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

from schema import exclude_filter
import mock
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))


class TestSchemaExcludeFilter(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @mock.patch('schema.loader.warn')
    def test_load_exclude_definitions_raises_when_no_exclude_found(self, mock_warn):
        with self.assertRaisesRegex(ValueError,
                                    "--exclude specified, but no exclusions found in \['foo\*.yml'\]"):
            exclude_filter.load_exclude_definitions(['foo*.yml'])

    def test_exclude_field(self):
        fields = {'my_field_set': {'fields': {
            'my_field_exclude': {'field_details': {'flat_name': 'my_field_set.my_field_exclude'}},
            'my_field_persist': {'field_details': {'flat_name': 'my_field_set.my_field_persist'}}}}}
        excludes = [
            [{'name': 'my_field_set', 'fields': [{'name': 'my_field_exclude'}]}]]
        fields = exclude_filter.exclude_fields(fields, excludes)
        expect_persisted = {'my_field_set': {'fields': {
            'my_field_persist': {'field_details': {'flat_name': 'my_field_set.my_field_persist'}}}}}
        self.assertEqual(fields, expect_persisted)

    def test_exclude_field_deep_path(self):
        fields = {'d0': {'fields': {
            'd1': {'field_details': {'flat_name': 'd0.d1'}, 'fields': {
                'd2': {'field_details': {'flat_name': 'd0.d1.d2'}, 'fields': {
                    'd3': {'field_details': {'flat_name': 'd0.d1.d2.d3'}, 'fields': {
                        'd4': {'field_details': {'flat_name': 'd0.d1.d2.d3.d4'}, 'fields': {
                            'd5': {'field_details': {'flat_name': 'd0.d1.d2.d3.d4.d5'}}}}}}}}}}}}}
        excludes = [[{'name': 'd0', 'fields': [{
            'name': 'd1.d2.d3.d4.d5'}]}]]
        fields = exclude_filter.exclude_fields(fields, excludes)
        expect_persisted = {}
        self.assertEqual(fields, expect_persisted)

    def test_exclude_field_dot_path(self):
        fields = {'d0': {'fields': {
            'd1': {'field_details': {'flat_name': 'd0.d1'}, 'fields': {
                'd2': {'field_details': {'flat_name': 'd0.d1.d2'}, 'fields': {
                    'd3': {'field_details': {'flat_name': 'd0.d1.d2.d3'}, 'fields': {
                        'd4': {'field_details': {'flat_name': 'd0.d1.d2.d3.d4'}, 'fields': {
                            'd5': {'field_details': {'flat_name': 'd0.d1.d2.d3.d4.d5'}}}}}}}}}}}}}
        excludes = [[{'name': 'd0', 'fields': [{
            'name': 'd1.d2.d3.d4.d5'}]}]]
        fields = exclude_filter.exclude_fields(fields, excludes)
        expect_persisted = {}
        self.assertEqual(fields, expect_persisted)

    def test_exclude_field_base_always_persists(self):
        fields = {'base': {'fields': {
            'd1': {'field_details': {'flat_name': 'base.d1'}, 'fields': {
                'd2': {'field_details': {'flat_name': 'base.d1.d2'}, 'fields': {
                    'd3': {'field_details': {'flat_name': 'base.d1.d2.d3'}, 'fields': {
                        'd4': {'field_details': {'flat_name': 'base.d1.d2.d3.d4'}, 'fields': {
                            'd5': {'field_details': {'flat_name': 'base.d1.d2.d3.d4.d5'}}}}}}}}}}}}}
        excludes = [[{'name': 'base', 'fields': [{
            'name': 'd1.d2.d3.d4.d5'}]}]]
        fields = exclude_filter.exclude_fields(fields, excludes)
        expect_persisted = {'base': {'fields': {}}}
        self.assertEqual(fields, expect_persisted)

    def test_exclude_fields(self):
        fields = {'my_field_set': {'fields': {
            'my_field_exclude_1': {'field_details': {'flat_name': 'my_field_set.my_field_exclude_1'}},
            'my_field_exclude_2': {'field_details': {'flat_name': 'my_field_set.my_field_exclude_2'}}}}}
        excludes = [[{'name': 'my_field_set', 'fields': [
            {'name': 'my_field_exclude_1'}, {'name': 'my_field_exclude_2'}]}]]
        fields = exclude_filter.exclude_fields(fields, excludes)
        expect_persisted = {}
        self.assertEqual(fields, expect_persisted)

    def test_exclude_non_existing_field_set(self):
        fields = {'my_field_set': {'fields': {
            'my_field': {'field_details': {'flat_name': 'my_field_set.my_field'}}}}}
        excludes = [[{'name': 'my_non_existing_field_set', 'fields': [
            {'name': 'my_field_exclude'}]}]]
        with self.assertRaisesRegex(ValueError,
                                    "--exclude specified, but no field my_non_existing_field_set.my_field_exclude found"):
            exclude_filter.exclude_fields(fields, excludes)

    def test_exclude_non_existing_field(self):
        fields = {'my_field_set': {'fields': {
            'my_field': {'field_details': {'flat_name': 'my_field_set.my_field'}}}}}
        excludes = [[{'name': 'my_field_set', 'fields': [
            {'name': 'my_non_existing_field'}]}]]
        with self.assertRaisesRegex(ValueError,
                                    "--exclude specified, but no field my_field_set.my_non_existing_field found"):
            exclude_filter.exclude_fields(fields, excludes)

    def test_exclude_non_existing_field_deep_path(self):
        fields = {'d0': {'fields': {
            'd1': {'field_details': {'flat_name': 'd0.d1'}}, 'fields': {
                'd2': {'field_details': {'flat_name': 'd0.d1.d2'}}, 'fields': {
                    'd3': {'field_details': {'flat_name': 'd0.d1.d2.d3'}}}}}}}
        excludes = [[{'name': 'd0', 'fields': [{
            'name': 'd1.d2.d3.d4.d5'}]}]]
        with self.assertRaisesRegex(ValueError,
                                    "--exclude specified, but no path to field d0.d1.d2.d3.d4.d5 found"):
            exclude_filter.exclude_fields(fields, excludes)
