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

"""CLI commands."""

import json
from io import open

import click

import doschema.validation
from doschema.errors import JSONSchemaCompatibilityError
from doschema.utils import detect_encoding


@click.group()
def cli():
    """CLI group."""
    pass  # pragma: no cover


@cli.command()
@click.argument(
    'schemas',
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True
    ),
    nargs=-1
)
@click.option(
    '--ignore_index/--with_index',
    default=True,
    help="Enable/Disable conflict detection between different indices of "
    "array fields in JSON-Schemas. Enabled by default."
)
def validate(schemas, ignore_index):
    """Main function for cli."""
    try:
        schema_validator = doschema.validation.JSONSchemaValidator(
            ignore_index)
        for schema in schemas:
            with open(schema, 'rb') as infile:
                byte_file = infile.read()
                encoding = detect_encoding(byte_file)
                string_file = byte_file.decode(encoding)
                json_schema = json.loads(string_file)
                schema_validator.validate(json_schema, schema)
    except JSONSchemaCompatibilityError as e:
        raise click.ClickException(str(e))
