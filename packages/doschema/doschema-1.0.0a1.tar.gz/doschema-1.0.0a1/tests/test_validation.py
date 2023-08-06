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

import jsonschema
import pytest

from doschema.errors import JSONSchemaCompatibilityError
from doschema.validation import JSONSchemaValidator


def test_no_conflicting_fields():
    """Test that having no conflict between fields inside schema passes."""
    v1 = {
        "type": "object",
        "properties": {
            "root_field": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "sub_field": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')


def test_conflicting_fields():
    """Test that having a conflict between fields inside schema fails."""
    v1 = {
        "type": "object",
        "properties": {
            "properties": {
                "type": "string"
            },
            "type": {
                "type": "string"
            },
            "items": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "dependencies": {
                "properties": {
                    "dependencies": {
                        "type": "integer"
                    }
                },
                "dependencies": {
                    "dependencies": {
                        "type": "object",
                        "properties": {
                            "dependencies": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v1, 'first')


def test_no_conflict_between_schemas_pass():
    """Test that having two correct schemas and no conflict between them
    passes."""
    v1 = {
        "type": "object",
        "properties": {
            "field_A": {"type": "string"}
        }
    }
    v2 = {
        "type": "object",
        "properties": {
            "field_B": {"type": "string"}
        }
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')
    obj.validate(v2, 'second')


def test_conflict_between_schemas():
    """Test that having correct schemas and conflict between them fails."""
    v1 = {
        "type": "object",
        "properties": {
            "field_A": {"type": "string"}
        }
    }
    v2 = {
        "type": "object",
        "properties": {
            "field_A": {"type": "number"}
        }
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v2, 'second')


def test_root_object_explicit_pass():
    """Test that having explicit type 'object' of the root passes."""
    v1 = {
        "type": "object",
        "properties": {
            "type": "string"
        }
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')


def test_root_object_implicit_pass():
    """Test that having implicit type 'object' of the root passes."""
    v1 = {
        "properties": {
            "type": "string"
        }
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')


def test_root_not_object():
    """Test that not having type 'object' of the root fails."""
    v1 = {
        "type": "string"
    }
    obj = JSONSchemaValidator()
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v1, 'first')


def test_type_conflict_with_properties_implied():
    """Test that having type given in schema and type 'object' implied by
    properties fails."""
    v1 = {
        "type": "string",
        "properties": {
            "field_a": {"type": "string"}
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v1, 'first')


def test_type_conflict_with_dependencies_implied():
    """Test that having type given in schema and type 'object' implied by
    dependencies fails."""
    v1 = {
        "type": "string",
        "dependencies": {
            "field_a": {"type": "string"}
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v1, 'first')


def test_new_field_in_dependencies_passes():
    """Test that having a new field in dependencies fails."""
    v1 = {
        "type": "object",

        "properties": {
            "billing_address": {"type": "number"}
        },

        "dependencies": {
            "credit_card": {
                "properties": {
                    "billing_address": {"type": "number"}
                }
            }
        }
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')


def test_dependencies_not_dict():
    """Test the exception raised when dependencies are neither of type list
    nor a dict."""
    v1 = {
        "type": "object",

        "properties": {
            "name": {"type": "string"},
            "credit_card": {"type": "number"},
        },

        "dependencies": {
            "name": "credit_card"
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(ValueError):
        obj.validate(v1, 'first')


def test_conflict_in_dependencies():
    """Test that having conflict between elements in dependencies fails."""
    v1 = {
        "type": "object",

        "properties": {
            "credit_card": {"type": "number"},
            "billing_address": {"type": "number"}
        },

        "dependencies": {
            "credit_card": {
                "properties": {
                    "billing_address": {"type": "string"}
                }
            }
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v1, 'first')


def test_array_no_items_pass():
    """Test that having an array without items passes."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "$schema": {"type": "string"},
            "_files": {
                "type": "array"
            }
        }
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')


def test_different_types_inside_enum():
    """Test that having different types inside enum fails."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "resource_type": {
                "type": "array",
                "items": {
                    "enum": [
                        "Text",
                        42
                    ]
                }
            }
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v1, 'first')


def test_enum_in_array_items_pass():
    """Test that having enum in array's items passes."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "$schema": {"type": "string"},
            "resource_type": {
                "title": "Resource Type",
                "description": "The type of the resource.",
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "Text",
                        "Image",
                        "Video",
                        "Audio",
                        "Time-Series",
                        "Other"
                    ]
                },
                "uniqueItems": True
            }
        },
        "required": ["community", "title", "open_access"]
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')


def test_different_types_given_and_guessed_enum():
    """Tets that having type given in schema and different type guessed from
    enum fails."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "resource_type": {
                "type": "integer",
                "enum": [
                    "Text",
                    "Image"
                ]
            }
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v1, 'first')


def test_dict_type_inside_enum():
    "Test that having a dict inside enum fails."
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "resource_type": {
                "type": "array",
                "items": {
                    "enum": [{
                        "field_A": {"type": "string"}
                    }]
                }
            }
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(NotImplementedError):
        obj.validate(v1, 'first')


def test_list_type_inside_enum():
    "Test that having a list inside enum fails."
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "resource_type": {
                "type": "array",
                "items": {
                    "enum": [['abc'], ['bdc']]
                }
            }
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(NotImplementedError):
        obj.validate(v1, 'first')


def test_no_conflict_in_collection_pass():
    """Test that having no conflict between elements of a collection passes."""
    v1 = {
        "type": "object",
        "oneOf": [
            {
                "type": "object",
                "properties": {
                    "field_A": {"type": "string"}
                }
            }, {
                "type": "object",
                "properties": {
                    "field_B": {"type": "integer"}
                }
            }
        ]
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')


def test_conflict_in_collection():
    """Test that having a conflict between properties of a oneOf
    collection fails."""
    v1 = {
        "type": "object",
        "oneOf": [
            {
                "type": "object",
                "properties": {
                    "field_A": {"type": "string"}
                }
            }, {
                "type": "object",
                "properties": {
                    "field_A": {"type": "integer"}
                }
            }
        ]
    }
    obj = JSONSchemaValidator()
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v1, 'first')


def test_conflict_in_collection2():
    """Test that having a conflict between properties of an allOf
    collection fails."""
    v1 = {
        "type": "object",
        "allOf": [
            {
                "type": "object",
                "properties": {
                    "my_field": {
                        "type": "string"
                    }
                }
            },
            {
                "type": "object",
                "dependencies": {
                    "my_field": {
                        "type": "object",
                        "properties": {
                            "my_field": {
                                "type": "integer"
                            }
                        }
                    }
                }
            }
        ]
    }
    obj = JSONSchemaValidator()
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v1, 'first')


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
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')


def test_ref_conflict_inside_schema():
    """Test that having an invalid reference in the schema raises
    RefResolutionError."""
    v1 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "type": "object",

        "properties": {
            "billing_address": {"$ref": "#/definitions/differentaddress"},
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
    obj = JSONSchemaValidator()
    with pytest.raises(jsonschema.exceptions.RefResolutionError):
        obj.validate(v1, 'first')


def test_ref_conflict_between_schemas():
    """Test that having a conflict between schemas with references passes."""
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
    v2 = {
        "$schema": "http://json-schema.org/draft-04/schema#",

        "definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street_address": {"type": "differenttype"}
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
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v2, 'second')


def test_none_types_pass():
    """Test that having a field with no type passes.

    FIXME: Later we will want to add an optional failure for unknown types.
    """
    v1 = {
        "type": "object",

        "properties": {
            "credit_card": {"type": "number"}
        },

        "dependencies": {
            # 'billing_address' is only referenced here without defining type
            # thus we save it as 'None'
            "credit_card": ["billing_address"]
        }
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')


def test_null_type_not_implemented():
    """Test that having a field with null type fails."""
    v1 = {
        "type": "object",
        "properties": {
            "abc": {
                "type": "null"
            }
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(NotImplementedError):
        obj.validate(v1, 'first')


def test_null_type_repeated_fields():
    """Test that having already used field using it with type null fails."""
    v1 = {
        "type": "object",
        "properties": {
            "abc": {
                "type": "string"
            }
        }
    }
    v2 = {
        "type": "object",
        "properties": {
            "abc": {
                "type": "null"
            }
        }
    }
    obj = JSONSchemaValidator()
    obj.validate(v1, 'first')
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v2, 'second')


def test_not_ignoring_indices_pass():
    """Test that with option 'ignore index' set to False and different types
    in array passes."""
    v1 = {
        "type": "object",
        "properties": {
            "experiment_info": {
                "type": "array",
                "items": [
                    {
                        "type": "object",
                        "properties": {
                            "field_A": {"type": "string"}
                        }
                    },
                    {
                        "type": "object",
                        "properties": {
                            "field_A": {"type": "number"}
                        }
                    }
                ]
            }
        }
    }
    obj = JSONSchemaValidator(False)
    obj.validate(v1, 'first')


def test_ignoring_indices():
    """Test that with option 'ignore index' set to True and different types
    in array fails."""
    v1 = {
        "type": "object",
        "properties": {
            "experiment_info": {
                "type": "array",
                "items": [
                    {
                        "type": "object",
                        "properties": {
                            "field_A": {"type": "string"}
                        }
                    },
                    {
                        "type": "object",
                        "properties": {
                            "field_A": {"type": "number"}
                        }
                    }
                ]
            }
        }
    }
    obj = JSONSchemaValidator()
    with pytest.raises(JSONSchemaCompatibilityError):
        obj.validate(v1, 'first')
