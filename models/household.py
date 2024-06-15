"""
This module contains the model for the household table in the database.
"""

from database import db


class HouseholdModel(db.Model):
    """
    Class representing the household table in the database.

    Attributes:
        id (int): The primary key of the household.
        house_number (str): The house number of the household.
        area (str): The area where the household is located.
        collection_requests (Relationship): The collection requests
        associated with the household.
    """

    __tablename__ = "households"

    id = db.Column(
        db.Integer,
        primary_key=True
        )
    house_number = db.Column(
        db.String(80),
        nullable=False)
    area = db.Column(
        db.String(80),
        nullable=False
        )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
        )
    user = db.relationship(
        "UserModel",
        back_populates="household",
        uselist=False
        )
    collection_requests = db.relationship(
        "CollectionRequestModel",
        back_populates="household",
        lazy="dynamic"
        )
