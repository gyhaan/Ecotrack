"""
This module contains the User model.
"""

from db import db


class UserModel(db.Model):
    """
    Represents a user in the system.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)