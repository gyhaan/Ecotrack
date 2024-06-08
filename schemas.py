"""
This file contains the schema for the various models.
"""

from marshmallow import Schema, fields


class HouseholdSchema(Schema):
    """
    This schema represents a household.
    """
    id = fields.Int(dump_only=True)
    house_number = fields.Str(required=True)
    area = fields.Str(required=True)
