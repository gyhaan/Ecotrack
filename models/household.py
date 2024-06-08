"""
This model represents a household.
"""

from db import db


class HouseholdModel(db.Model):
    """
    This model represents a household table in the database.
    """

    __tablename__ = 'households'

    id = db.Column(db.Integer, primary_key=True)
    house_number = db.Column(db.String(80), nullable=False)
    area = db.Column(db.String(80), nullable=False)
