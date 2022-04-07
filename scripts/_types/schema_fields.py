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

from typing import (
    Any,
    Dict,
    List,
    TypedDict,
    Union
)


class MultiField(TypedDict, total=False):
    doc_values: bool
    index: bool
    ignore_above: int
    name: str
    norms: bool
    type: str


class AllowedValues(TypedDict, total=False):
    name: str
    description: str


class Field(TypedDict, total=False):
    allowed_values: List[AllowedValues]
    dashed_name: str
    description: str
    doc_values: bool
    example: str
    flat_name: str
    footnote: str
    ignore_above: int
    index: bool
    intermediate: bool
    level: str
    multi_fields: List[MultiField]
    name: str
    node_name: str
    normalize: List[str]
    norms: bool
    required: bool
    short: str
    type: str


class FieldDetails(TypedDict, total=False):
    field_details: Field
    fields: Dict[str, Field]


class Reuseable(TypedDict, total=False):
    expected: List[Any]
    top_level: bool
    order: int


class SchemaDetails(TypedDict, total=False):
    group: int
    prefix: str
    reusable: Reuseable
    root: bool
    title: str


class FieldEntry(TypedDict, total=False):
    field_details: Field
    fields: Dict[str, Field]
    schema_details: SchemaDetails


class FieldNestedEntry(TypedDict, total=False):
    description: str
    fields: List[Field]
    footnote: str
    group: int
    name: str
    node_name: str
    prefix: str
    short: str
    title: str
    type: str
