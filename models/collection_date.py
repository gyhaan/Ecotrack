"""
This module contains the model for the collection_date table
in the database.
"""

from db import db


class CollectionDateModel(db.Model):
    """
    Class representing the collection_date table in the database.

    Attributes:
        id (int): The primary key of the collection date.
        collection_date (str): The date of the collection.
        collector_id (int): The foreign key referencing the collector.
        collector (CollectorModel): The relationship to the collector model.
    """

    __tablename__ = "collection_dates"

    id = db.Column(
        db.Integer,
        primary_key=True
        )
    collection_date = db.Column(
        db.String(80),
        nullable=False
        )
    collector_id = db.Column(
        db.Integer,
        db.ForeignKey("collectors.id"),
        nullable=False
        )
    collector = db.relationship(
        "CollectorModel",
        back_populates="collection_dates"
        )
