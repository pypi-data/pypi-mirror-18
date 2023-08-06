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

"""Transformation module."""

import copy

import jsonschema
import six


def resolve_references(schema, uri='', ref_resolver=None, in_place=False):
    """Resolve references in schema.

    It is assumed that schemas have already been validated for backward
    compatibility before transforming.

    :param schema: Schema that is currently processed.
    :param uri: URI of the currently processed schema.
                If not provided it will use default.
    :param ref_resolver: Resolver used to retrieve referenced schemas.
                         If not provided it will use default.
    :param in_place: If set to False it will not modify given schema.
                          Modified copy of the schema will be returned.
    """
    if not in_place:
        schema = copy.deepcopy(schema)

    if ref_resolver is None:
        ref_resolver = jsonschema.RefResolver(base_uri=uri, referrer=schema)
    return _resolve_references_sub(schema, ref_resolver)


def _resolve_references_sub(schema, ref_resolver):
    """Go through the schema and resolve references.

    :param schema: Schema that is currently processed.
    :param ref_resolver: Resolver used to retrieve referenced schemas.
    """
    if isinstance(schema, dict):
        for key, json_value in six.iteritems(schema):
            if isinstance(json_value, dict):
                if '$ref' in json_value:
                    ref = json_value.pop('$ref', None)
                    schema[key] = ref_resolver.resolve(ref)[1]
            _resolve_references_sub(schema[key], ref_resolver)

    elif isinstance(schema, list):
        for index, schema_part in enumerate(schema):
            if '$ref' in schema_part:
                ref = schema_part.pop('$ref', None)
                schema[index] = ref_resolver.resolve(ref)[1]
            _resolve_references_sub(schema_part, ref_resolver)

    return schema
