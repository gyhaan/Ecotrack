"""
This file contains the schema for the various models.
"""

from marshmallow import Schema, fields


class PlainHouseholdSchema(Schema):
    """
    This schema represents a household.
    """
    id = fields.Int(dump_only=True)
    house_number = fields.Str(required=True)
    area = fields.Str(required=True)


class PlainCollectorSchema(Schema):
    """
    This schema represents a collector.
    """
    id = fields.Int(dump_only=True)
    allocated_area = fields.Str(required=True)


class PlainCollectionDateSchema(Schema):
    """
    This schema represents a collection date.
    """
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)


class PlainCollectionRequestSchema(Schema):
    """
    This schema represents a collection request.
    """
    id = fields.Int(dump_only=True)
    status = fields.Str(missing="pending")
    household_id = fields.Str(required=True)
    collection_date_id = fields.Int(required=True)


class CollectionRequestSchema(PlainCollectionRequestSchema):
    """
    This schema represents a collection request with relationships.
    """
    household_id = fields.Int(required=True, load_only=True)
    collection_date_id = fields.Int(required=True, load_only=True)
    household = fields.Nested(PlainHouseholdSchema(), dump_only=True)
    collection_date = fields.Nested(
        PlainCollectionDateSchema(), dump_only=True)


class CollectionDateSchema(PlainCollectionDateSchema):
    """
    This schema represents a collection date with relationships.
    """
    collection_requests = fields.List(fields.Nested(
        PlainCollectionRequestSchema()), dump_only=True)


class HouseholdSchema(PlainHouseholdSchema):
    """
    This schema represents a household with relationships.
    """
    collection_requests = fields.List(fields.Nested(
        PlainCollectionRequestSchema()), dump_only=True)


class CollectorSchema(PlainCollectorSchema):
    """
    This schema represents a collector with relationships.
    """
    collection_dates = fields.List(fields.Nested(
        PlainCollectionDateSchema()), dump_only=True)
