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

import jsonschema
import pytest

from doschema.transform import resolve_references


def test_ref_no_array_pass():
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/address"},
            "shipping_address": {"$ref": "#/definitions/address"}
        }
    }
    expected = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            },
            "shipping_address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        }
    }
    result = resolve_references(v1)
    assert expected == result


def test_ref_no_conflict_inside_schema_pass():
    """Test that having no conflict in schema with references passes."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/address"},
            "shipping_address": {
                "allOf": [
                    {"$ref": "#/definitions/address"},
                    {
                        "properties":   {
                            "type": {"enum": ["residential", "business"]}
                        }
                    }
                ]
            }
        }
    }
    expected = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            },
            "shipping_address": {
                "allOf": [
                    {
                        "type": "object",
                        "properties": {
                            "street_address": {"type": "string"}
                        }
                    },
                    {
                        "properties": {
                            "type": {"enum": ["residential", "business"]}
                        }
                    }
                ]
            }
        }
    }
    result = resolve_references(v1)
    assert expected == result


def test_ref_conflict_inside_schema():
    """Test that having an invalid reference in the schema raises
    RefResolutionError."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/differentaddress"},
        }
    }
    with pytest.raises(jsonschema.exceptions.RefResolutionError):
        resolve_references(v1)


def test_ref_outside_schema():
    """Test that having a reference to schema in different file passes."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {
                "$ref": "test_outside.json#/definitions/address"

            },
            "shipping_address": {
                "allOf": [
                    {"$ref": "#/definitions/address"},
                    {
                        "properties":   {
                            "type": {"enum": ["residential", "business"]}
                        }
                    }
                ]
            }
        }
    }
    expected = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "differenttype"}
                }
            },
            "shipping_address": {
                "allOf": [
                    {
                        "type": "object",
                        "properties": {
                            "street_address": {"type": "string"}
                        }
                    },
                    {
                        "properties":   {
                            "type": {"enum": ["residential", "business"]}
                        }
                    }
                ]
            }
        }
    }
    result = resolve_references(
        v1,
        'file://' + os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_outside',
            'test_outside'
        )
    )
    assert expected == result


def test_internal_resolving():
    """Test internal resolving passes."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "^[a-zA-Z0-9]+$": {"type": "string"}
        },

        "type": "object",

        "properties": {
            "^[a-zA-Z]+$": {"$ref": "#/definitions"}
        }
    }
    expected = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "^[a-zA-Z0-9]+$": {"type": "string"}
        },

        "type": "object",

        "properties": {
            "^[a-zA-Z]+$": {
                "^[a-zA-Z0-9]+$": {"type": "string"}
            }
        }
    }
    result = resolve_references(v1)
    assert expected == result


def test_in_place_false_option():
    """Test if in_place option set to False not modifies schema."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/address"},
        }
    }
    result = resolve_references(v1, in_place=False)
    assert result is not v1
    assert result != v1


def test_in_place_true_option():
    """Test if in_place option set to True modifies schema."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "string"}
                }
            }
        },

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/address"},
        }
    }
    result = resolve_references(v1, in_place=True)
    assert result is v1
    assert result == v1
