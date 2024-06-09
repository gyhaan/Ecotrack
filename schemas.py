"""
This file contains the schema for the various models.
"""

from marshmallow import Schema, fields


class HouseholdSchema(Schema):
    """
    This schema represents a household.
    """
    id = fields.Str(dump_only=True)
    house_number = fields.Str(required=True)
    area = fields.Str(required=True)


class CollectorSchema(Schema):
    """
    This schema represents a collector.
    """
    id = fields.Str(dump_only=True)
    allocated_area = fields.Str(required=True)


class CollectionDateSchema(Schema):
    """
    This schema represents a collection date.
    """
    id = fields.Str(dump_only=True)
    date = fields.Date(required=True)


class CollectionRequestSchema(Schema):
    """
    This schema represents a collection request.
    """
    id = fields.Str(dump_only=True)
    status = fields.Str(missing="pending")
    household_id = fields.Int(required=True)
    collection_date_id = fields.Int(required=True)
