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

import os

from click.testing import CliRunner

from doschema.cli import validate


def path_helper(filename):
    """Make the path for test files."""
    return os.path.join('.', 'examples', filename)


def test_repetition():
    """Test that adding field with the same type passes."""
    runner = CliRunner()
    schemas = [
        'jsonschema_for_repetition.json',
        'jsonschema_repetition.json'
    ]

    files = [path_helper(filename) for filename in schemas]
    result = runner.invoke(validate, files)

    assert result.exit_code == 0


def test_difference():
    """Test that adding field with different type fails."""
    runner = CliRunner()
    schemas = [
        'jsonschema_for_repetition.json',
        'jsonschema_no_repetition.json'
    ]

    files = [path_helper(filename) for filename in schemas]
    result = runner.invoke(validate, files)

    assert result.exit_code == 1


def test_ref():
    """Test that references works."""
    runner = CliRunner()
    schemas = ['jsonschema_ref.json', 'jsonschema_other_ref.json']

    files = [path_helper(filename) for filename in schemas]
    result = runner.invoke(validate, files)

    assert result.exit_code == 1


def test_ignore_option():
    """Test that with no option "--ignore_index" option  is set."""
    runner = CliRunner()
    schemas = ['jsonschema_ignore_index_option.json']

    files = [path_helper(filename) for filename in schemas]
    result = runner.invoke(validate, files)

    assert result.exit_code == 0


def test_with_option():
    """Test that "--with_index" option references works."""
    runner = CliRunner()
    schemas = ['jsonschema_with_index_option.json']

    files = [path_helper(filename) for filename in schemas]
    files.append('--with_index')
    result = runner.invoke(validate, files)
    assert result.exit_code == 0
