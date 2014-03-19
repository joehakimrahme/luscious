==============================================
Luscious, generate json-schema from Voluptuous
==============================================

:Homepage:  https://github.com/joehakimrahme/luscious.git
:Credits:   Joe H. Rahme <joe@enovance.com>
:Licence:   Apache

DESCRIPTION
===========

Luscious provides a simple way to generate json-schema (json-schema.org) from a Voluptuous schema.


REQUIREMENT
===========

- Voluptuous
- jsonschema

Operating Systems
=================

This has been tested and developed on MacOSX and Linux system, but there's no reason why it shouldn't work on other systems.

USAGE
======

Here's how to generate a valid schema::
  >>> import voluptuous
  >>> schema = voluptuous.Schema({
  ... voluptuous.Required("id"): int,
  ... voluptuous.Required("name"): str,
  ... voluptuous.Required("price"): voluptuous.Range(min=0, min_included=False),
  ... "tags": [str]
  ... })
  >>> from luscious import get_jsonschema
  >>> print json.dumps(get_jsonschema(schema), indent=4)
  {
      "$schema": "http=//json-schema.org/draft-04/schema#",
      "required": [
          "name",
          "id",
          "price"
      ],
      "type": "object",
      "properties": {
          "id": {
              "type": "number"
          },
          "price": {
              "exclusiveMinimum": true,
              "minimum": 0,
              "type": "number"
          },
          "name": {
              "type": "string"
          },
          "tags": {
              "items": {
                  "items": {
                      "type": "string"
                  }
              },
              "type": "array"
          }
      }
  }

Author
======

Joe H. Rahme <joe@enovance.com>
