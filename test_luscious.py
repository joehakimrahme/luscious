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
            "tags": list
        })

        self.jsonschema = luscious.get_jsonschema(schema)

    def test_valid_instance(self):

        instance = {
            "id": 1,
            "name": "A green door",
            "price": 10,
            "tags": ["home", "green"]
        }

        self.assertIsNone(jsonschema.validate(self.jsonschema, instance))

    def test_non_int_id(self):

        instance = {
            "id": 1,
            "name": "A green door",
            "price": 10,
            "tags": ["home", "green"]
        }

        self.assertRaises(jsonschema.exceptions.ValidationError,
                          jsonschema.validate, self.jsonschema, instance)
