# Copyright (c) 2014 Joe H. Rahme <joe@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json


class SchemaNode(dict):

    def __init__(self, description=None, *args, **kwargs):
        self["type"] = self.typename
        if description:
            self["description"] = description

    def __repr__(self):
        return json.dumps(self, sort_keys=True)


class ObjectNode(SchemaNode):
    typename = "object"

    def __init__(self, properties, *args, **kwargs):
        super(ObjectNode, self).__init__(*args, **kwargs)
        self["properties"] = properties


class ArrayNode(SchemaNode):
    typename = "array"

    def __init__(self, items, *args, **kwargs):
        super(ArrayNode, self).__init__(*args, **kwargs)
        self["items"] = items


class StringNode(SchemaNode):
    typename = "string"


class NumberNode(SchemaNode):
    typename = "number"


class RangeNode(SchemaNode):
    typename = "number"

    def __init__(self, maximum, max_included=False, minimum=None,
                 min_included=False, msg=None, *args, **kwargs):
        super(RangeNode, self).__init__(*args, **kwargs)
        if maximum is not None:
            self["maximum"] = maximum
        if minimum is not None:
            self["minimum"] = minimum

        self["exclusive_minimum"] = min_included
        self["exclusive_maximum"] = max_included


def get_jsonschema(schema, title=None, description=None):

    jsonschema = jsonify(schema.schema)
    jsonschema["$schema"] = "http=//json-schema.org/draft-04/schema#"

    if title:
        jsonschema["title"] = title

    if description:
        jsonschema["description"] = description

    return jsonschema


def jsonify(schema):

    if isinstance(schema, dict):
        p = {}

        for key, value in schema.iteritems():
            if hasattr(key, "schema"):
                key = key.schema

            p[key] = jsonify(value)

        return ObjectNode(properties=p)

    elif isinstance(schema, list):
        i = {}

        key = schema[0]
        i["items"] = jsonify(key)
        return ArrayNode(items=i)

    elif schema is str:
        return StringNode()

    elif schema is int:
        return NumberNode()

    elif hasattr(schema, "func_name") and schema.func_name == "Range":
        range_vars = dict(zip(schema.func_code.co_freevars,
                              (i.cell_contents for i in schema.func_closure)))

        maximum = range_vars['max']
        max_included = range_vars['max_included']
        minimum = range_vars['min']
        min_included = range_vars['min_included']
        msg = range_vars['msg']

        return RangeNode(maximum, max_included, minimum, min_included, msg)
