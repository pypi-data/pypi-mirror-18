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


"""In this example, there is no option set, so by default
"--ignore_index" option is enabled.
Thus array indexes are ignored and for each array field, all items have to be
of the same type.

Run this example:
.. code-block:: console
    $ cd examples
    $ python app.py
The same result could be created with the cli:
.. code-block:: console
    $ doschema file1.json file2.json
"""

import json
from io import open

import doschema.validation
from doschema.utils import detect_encoding

schemas = [
    './examples/jsonschema_ignore_index_option.json'
]

schema_validator = doschema.validation.JSONSchemaValidator()
for schema in schemas:
    with open(schema, 'rb') as infile:
        byte_file = infile.read()
        encoding = detect_encoding(byte_file)
        string_file = byte_file.decode(encoding)
        json_schema = json.loads(string_file)
        schema_validator.validate(json_schema, schema)
