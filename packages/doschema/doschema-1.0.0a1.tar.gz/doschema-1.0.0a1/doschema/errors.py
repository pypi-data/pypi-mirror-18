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

"""Define all DoSchema exceptions."""


class DoSchemaError(Exception):
    """Parent for all DoSchema exceptions.

    .. versionadded:: 1.0.0
    """

    pass


class JSONSchemaCompatibilityError(DoSchemaError):
    """Exception raised when a JSON schema is not backward compatible."""

    def __init__(self, err_msg, schema, prev_schema=None):
        """Constructor."""
        self.prev_schema = prev_schema
        """Index of schema in which field has occured before."""
        self.schema = schema
        """Index of schema in which field occurs now."""
        super(JSONSchemaCompatibilityError, self).__init__(err_msg)
        """Error message."""


class EncodingError(DoSchemaError):
    """Exception raised when file encoding is not compatible."""

    pass
