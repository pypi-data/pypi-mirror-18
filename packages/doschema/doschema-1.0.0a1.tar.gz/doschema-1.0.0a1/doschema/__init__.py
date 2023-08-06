# -*- coding: utf-8 -*-
#
# This file is part of DoSchema.
# Copyright (C) 2016 CERN.
#
# DoSchema is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# DoSchema is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DoSchema; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

r"""JSON Schema utility functions and commands.

Compatibility Validation
-------------------------

It validates compatibility between different JSON schemas versions.

A schema is backward compatible if the fields' type remain the same in all
JSON schemas declaring it and JSON schemas are type consistent within
themselves too.

>>> import json
>>> from io import open
>>>
>>> import doschema.validation
>>> from doschema.utils import detect_encoding
>>>
>>> schemas = [
...     './examples/jsonschema_for_repetition.json',
...     './examples/jsonschema_repetition.json'
... ]
>>>
>>> schema_validator = doschema.validation.JSONSchemaValidator()
>>> for schema in schemas:
...     with open(schema, 'rb') as infile:
...         byte_file = infile.read()
...         encoding = detect_encoding(byte_file)
...         string_file = byte_file.decode(encoding)
...         json_schema = json.loads(string_file)
...         schema_validator.validate(json_schema, schema)

By default the index of "array" "items" are ignored. Thus all the values of
an array should have the same type in order to be compatible.
This behavior can be disabled by setting "ignore_index = False" in the
validator's constructor.

>>> import json
>>> from io import open
>>>
>>> import doschema.validation
>>> from doschema.utils import detect_encoding
>>>
>>> schemas = [
...     './examples/jsonschema_with_index_option.json'
... ]
>>>
>>> schema_validator = doschema.validation.JSONSchemaValidator(
...     ignore_index = False
... )
>>> for schema in schemas:
...     with open(schema, 'rb') as infile:
...         byte_file = infile.read()
...         encoding = detect_encoding(byte_file)
...         string_file = byte_file.decode(encoding)
...         json_schema = json.loads(string_file)
...         schema_validator.validate(json_schema, schema)

CLI usage
--------------
.. code-block:: console

    $ doschema validate jsonschema_for_repetition.json \
    jsonschema_repetition.json
    $ doschema validate jsonschema_with_index_option.json --with_index

"""

from __future__ import absolute_import, print_function

from .version import __version__

__all__ = ('__version__')
