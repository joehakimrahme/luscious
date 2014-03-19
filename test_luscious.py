# Copyright (c) 2014 Joe H. Rahme <joe@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import jsonschema
import voluptuous

import luscious


class Example1Test(unittest.TestCase):

    def setUp(self):
        schema = voluptuous.Schema({
            voluptuous.Required("id"): int,
            voluptuous.Required("name"): str,
            voluptuous.Required("price"): voluptuous.Range(min=0,
                                                           min_included=False),
            "tags": [str]
        })

        self.jsonschema = luscious.get_jsonschema(schema)

    def test_valid_instance(self):

        instance = {
            "id": 1,
            "name": "A green door",
            "price": 10,
            "tags": ["home", "green"]
        }

        self.assertIsNone(jsonschema.validate(instance, self.jsonschema))

    def test_non_int_id(self):

        instance = {
            "id": "1",
            "name": "A green door",
            "price": 10,
            "tags": ["home", "green"]
        }

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          jsonschema.validate, instance, self.jsonschema)

    def test_non_str_name(self):

        instance = {
            "id": 1,
            "name": 0,
            "price": 10,
            "tags": ["home", "green"]
        }

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          jsonschema.validate, instance, self.jsonschema)

    def test_zero_price(self):

        instance = {
            "id": 1,
            "name": "A green door",
            "price": 0,
            "tags": ["home", "green"]
        }

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          jsonschema.validate, instance, self.jsonschema)

    def test_negative_price(self):

        instance = {
            "id": 1,
            "name": "A green door",
            "price": -5,
            "tags": ["home", "green"]
        }

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          jsonschema.validate, instance, self.jsonschema)

    def test_non_int_price(self):

        instance = {
            "id": 1,
            "name": "A green door",
            "price": "10",
            "tags": ["home", "green"]
        }

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          jsonschema.validate, instance, self.jsonschema)

    def test_non_list_tags(self):

        instance = {
            "id": 1,
            "name": "A green door",
            "price": 10,
            "tags": "home",
        }

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          jsonschema.validate, instance, self.jsonschema)

    def test_non_stringlist_tags(self):

        instance = {
            "id": 1,
            "name": "A green door",
            "price": 10,
            "tags": ["home", 5],
        }

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          jsonschema.validate, instance, self.jsonschema)

    def test_non_unique_tags(self):

        instance = {
            "id": 1,
            "name": "A green door",
            "price": 10,
            "tags": ["home", "home"],
        }

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          jsonschema.validate, instance, self.jsonschema)

    def test_empty_tags(self):

        instance = {
            "id": 1,
            "name": "A green door",
            "price": 10,
            "tags": [],
        }

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          jsonschema.validate, instance, self.jsonschema)
