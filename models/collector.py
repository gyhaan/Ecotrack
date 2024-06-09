"""
This module contains the model for the collector table in the database.
"""

from db import db


class CollectorModel(db.Model):
    """
    Class representing the collector table in the database.

    Attributes:
        id (int): The primary key of the collector.
        allocated_area (str): The area allocated to the collector.
        collection_dates (Relationship): The collection dates
        associated with the collector.
    """

    __tablename__ = "collectors"

    id = db.Column(
        db.Integer,
        primary_key=True
        )
    allocated_area = db.Column(
        db.String(80),
        nullable=False
        )
    collection_dates = db.relationship(
        "CollectionDateModel",
        back_populates="collector",
        lazy="dynamic"
        )
