"""
This module contains a bluepring for the admin resources
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models.admin import AdminModel
from schemas import AdminSchema


blp = Blueprint(
    "admins",
    __name__,
    description="Operations on admins"
)


@blp.route("/admins")
class Admins(MethodView):
    """
    class for handling requests to the /admins endpoint
    """

    @jwt_required()
    @blp.response(200, AdminSchema(many=True))
    def get(self):
        """
        Get all admins in the database

        Returns:
            dict: A dictionary containing all admins in the database
        """
        jwt = get_jwt()

        if jwt.get("role") != "admin":
            abort(403, message="Admin privileges required to view all admins")
        return AdminModel.query.all()

    @jwt_required()
    @blp.response(201, AdminSchema())
    def post(self):
        """
        Add a new admin to the database.

        Args:
            admin_data (dict): A dictionary containing the data
            for the new admin.

        Returns:
            tuple: A tuple containing the newly added admin and the
            HTTP status code 201.

        Raises:
            abort: If there is an error adding the admin to the database.

        """
        jwt = get_jwt()
        user_id = jwt.get("sub")
        admin = AdminModel(user_id=user_id)

        try:
            db.session.add(admin)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(400, message=str(error))
        return admin, 201


@blp.route("/admins/<int:admin_id>")
class Admin(MethodView):
    """
    Class for handling requests to the /admins/<admin_id> endpoint
    """

    @jwt_required()
    @blp.response(200, AdminSchema)
    def get(self, admin_id):
        """
        Get an admin by ID

        Args:
            admin_id (int): The ID of the admin to retrieve

        Returns:
            dict: A dictionary containing the admin with the specified ID

        Raises:
            abort: If there is no admin with the specified ID

        """

        jwt = get_jwt()

        if jwt.get("role") != "admin":
            abort(403, message="Admin privileges required to view an admin")

        admin = AdminModel.query.get(admin_id)

        if not admin:
            abort(404, message="Admin not found")

        return admin

    @jwt_required()
    @blp.response(204)
    def delete(self, admin_id):
        """
        Delete an admin by ID

        Args:
            admin_id (int): The ID of the admin to delete

        Returns:
            tuple: An empty tuple and the HTTP status code 204

        Raises:
            abort: If there is no admin with the specified ID

        """
        jwt = get_jwt()
        if jwt.get("role") != "admin":
            abort(403, message="Admin privileges required to delete an admin")

        admin = AdminModel.query.get(admin_id)

        if not admin:
            abort(404, message="Admin not found")

        db.session.delete(admin)
        db.session.commit()

        return {}, 204
