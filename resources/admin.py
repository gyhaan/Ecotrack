"""
This module contains a bluepring for the admin resources
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models.admin import AdminModel
from schemas.admin import AdminSchema