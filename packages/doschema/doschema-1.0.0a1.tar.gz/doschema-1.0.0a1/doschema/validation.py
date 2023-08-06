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

"""Merger module."""


import collections
import logging

import jsonschema
import six

from doschema.errors import JSONSchemaCompatibilityError


class JSONSchemaValidator(object):
    """Class for checking compatibility between schemas."""

    COLLECTION_KEYS = frozenset(['allOf', 'anyOf', 'oneOf'])

    python_to_json_types_map = {
        "list": "array",
        "bool": "boolean",
        "int": "integer",
        "float": "number",
        "complex": "number",
        "NoneType": "null",
        "dict": "object",
        "str": "string",
        "unicode": "string",
    }

    def __init__(self, ignore_index=True, resolver_factory=False):
        """Constructor.

        :param ignore_index: If set to True, which is default, it will ignore
                             array indexes.
        :param resolver_factory: Resolver used to retrieve referenced schemas.
                                 If not provided it will use default.
        """
        self.ignore_index = ignore_index
        self.fields_types_dict = {}
        self.uri = None
        self.resolver_factory = resolver_factory or jsonschema.RefResolver

    def validate(self, schema, uri):
        """Check that the given schema is compatible with previously validated schemas.

        :param schema: Schema that is currently processed.
        :param uri: URI of the currently processed schema.
        """
        self.uri = uri
        self.resolver = self.resolver_factory(base_uri=uri, referrer=schema)

        self._validate_root(schema, ())

        root = self.fields_types_dict.get(())

        if not root or root.field_type != 'object':
            err_msg = "Root field / type is not 'object' in {0}"
            raise JSONSchemaCompatibilityError(
                err_msg.format(self.uri),
                self.uri
            )

        for path, field in six.iteritems(self.fields_types_dict):
            if field is None:
                logging.warning(
                    'No type in field ' + self.make_json_pointer(path)
                )

        self.uri = None
        self.resolver = None

    def _validate_root(self, curr_schema, curr_field):
        """Go through the schema and retrieve schema's particular fields.

        :param curr_schema: Schema or subschema that is currently processed.
        :param curr_field: Tuple with path to currently processed field.
        """
        while '$ref' in curr_schema:
            path = curr_schema.get('$ref')
            curr_schema = self.resolver.resolve(path)[1]

        self._validate_collection(curr_schema, curr_field)

        field = self.fields_types_dict.get(curr_field)

        field_type = curr_schema.get('type')
        if "type" in curr_schema:
            if field is not None and field.field_type == 'null':
                raise NotImplementedError(
                        'JSON schema null type is not supported.'
                    )
            elif field and curr_schema['type'] != field.field_type:
                err_msg = "{0} type mismatch in schemas {1} and {2}."
                raise JSONSchemaCompatibilityError(
                    err_msg.format(
                        self.make_json_pointer(curr_field),
                        field.schema_index,
                        self.uri
                    ),
                    self.uri,
                    field.schema_index
                )

            if field_type == 'null':
                raise NotImplementedError(
                    'JSON schema null type is not supported.'
                )

            if field is None or field.field_type is None:
                self.fields_types_dict[curr_field] = field = FieldToAdd(
                    schema_index=self.uri,
                    field_tuple=curr_field,
                    field_type=field_type
                )

            if curr_schema['type'] == 'array':
                if curr_schema.get('items') is not None:
                    self._validate_array(
                        curr_schema['items'],
                        curr_field + ('items',)
                    )
        if "enum" in curr_schema:
            guessed_enum_type = self._validate_enum(
                curr_schema['enum'],
                curr_field
            )
            if field_type and field_type != guessed_enum_type:
                err_msg = "Predicted enum type {0} conflicting with " \
                            "properties type {1} in schema {2}"
                raise JSONSchemaCompatibilityError(
                    err_msg.format(
                        guessed_enum_type,
                        field_type,
                        self.uri
                    ),
                    self.uri,
                    self.uri
                )

        if 'properties' in curr_schema:
            if field and field.field_type != "object":
                err_msg = "Conflicting type for field {0} previously found " \
                            "in schema {1} with type {2}, found next in {3} " \
                            "where 'properties' imply type 'object'."
                raise JSONSchemaCompatibilityError(
                    err_msg.format(
                        self.make_json_pointer(curr_field),
                        field.schema_index,
                        field.field_type,
                        self.make_json_pointer(field.field_tuple)
                    ),
                    self.uri,
                    field.schema_index
                )
            self.fields_types_dict[curr_field] = field = FieldToAdd(
                schema_index=self.uri,
                field_tuple=curr_field,
                field_type='object'
            )
            for prop in curr_schema['properties']:
                if isinstance(curr_schema['properties'][prop], dict):
                    self._validate_root(
                        curr_schema['properties'][prop],
                        curr_field + (prop,)
                    )

        if "dependencies" in curr_schema:
            if field and field.field_type != "object":
                err_msg = "Conflicting type for field {0} previously found " \
                            "in schema {1} with type {2}, found next in {3} " \
                            "where 'dependencies' imply type 'object'."
                raise JSONSchemaCompatibilityError(
                    err_msg.format(
                        self.make_json_pointer(curr_field),
                        field.schema_index,
                        field.field_type,
                        self.make_json_pointer(field.field_tuple)
                    ),
                    self.uri,
                    field.schema_index
                )
            self.fields_types_dict[curr_field] = field = FieldToAdd(
                schema_index=self.uri,
                field_tuple=curr_field,
                field_type='object'
            )
            self._validate_dependencies(curr_schema, curr_field)

    def _validate_array(self, field_value, curr_field):
        """Process each JSON object in the array according to ignore_index.

        :param field_value: Type of the field.
        :param curr_field: Tuple with path to currently processed field.
        """
        field_path = curr_field
        if isinstance(field_value, list):
            for elem in field_value:
                if self.ignore_index:
                    new_field_path = field_path
                else:
                    new_field_path = field_path + (field_value.index(elem), )

                self._validate_root(elem, new_field_path)

        elif isinstance(field_value, dict):
            self._validate_root(field_value, curr_field)

    def _validate_collection(self, curr_schema, curr_field):
        """Check schema for allOf, anyOf and oneOf.

        :param curr_schema: Schema or subschema that is currently processed.
        :param curr_field: Tuple with path to currently processed field.
        """
        keys = self.COLLECTION_KEYS.intersection(curr_schema)
        for key in keys:
            subschema = curr_schema[key]

            for elem in subschema:
                self._validate_root(elem, curr_field)

    def _validate_dependencies(self, curr_schema, curr_field):
        """validate_root and check dependencies in schema.

        :param curr_schema: Schema or subschema that is currently processed.
        :param curr_field: Tuple with path to currently processed field.
        """
        dependencies = curr_schema['dependencies']

        while '$ref' in dependencies:
            path = dependencies.get('$ref')
            dependencies = self.resolver.resolve(path)[1]

        for field_name, field_value in six.iteritems(dependencies):
            if curr_field + (field_name, ) not in self.fields_types_dict:
                self.fields_types_dict[
                    curr_field + (field_name, )
                ] = FieldToAdd(
                        schema_index=self.uri,
                        field_tuple=curr_field + (field_name, ),
                        field_type=None
                    )

            if isinstance(field_value, dict):
                self._validate_root(field_value, curr_field)

            elif type(field_value) is list:
                for field in field_value:
                    path = curr_field + (field, )
                    if path not in self.fields_types_dict:
                        self.fields_types_dict[
                            curr_field + (field_name, )
                        ] = FieldToAdd(
                                schema_index=self.uri,
                                field_tuple=curr_field + (field_name, ),
                                field_type=None
                            )
            else:
                raise ValueError(
                    'Dependencies value is not a dict nor a list.'
                )

    def _validate_enum(self, field_value, path):
        """Process each element in enum field values.

        :param field_value: Type of the field.
        :param path: Tuple with path to currently processed field.
        """
        types = map(lambda x: type(x), field_value)
        types_inside_enum = list(set(types))
        if len(types_inside_enum) > 1:
            err_msg = "Conflicting types {0} found for enum {1} in schema {2}."
            raise JSONSchemaCompatibilityError(
                err_msg.format(
                    types_inside_enum,
                    self.make_json_pointer(path),
                    self.uri
                ),
                self.uri
            )
        if isinstance(field_value[0], dict) \
                or isinstance(field_value[0], list):
            raise NotImplementedError(
                'JSON schema {0} type inside enum is not supported.'.format(
                    field_value[0].__class__.__name__
                )
            )
        return self.python_to_json_types_map[field_value[0].__class__.__name__]

    @staticmethod
    def make_json_pointer(path):
        """Make json pointer path from tuple.

        :param path: tuple with current path
        """
        return '/' + '/'.join(path)

FieldToAdd = collections.namedtuple(
    'FieldToAdd',
    'schema_index field_tuple field_type'
)
