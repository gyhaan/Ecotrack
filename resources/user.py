"""
This module contains the User blueprint.
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint(
    "users",
    __name__,
    description="Operations on users"
)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        Register a new user

        Parameters:
        - user_data (dict): The data of the user to be registered. It should contain the following keys:
            - username (str): The username of the user.
            - password (str): The password of the user.

        Returns:
        - dict: A dictionary containing the message "User created successfully".

        Raises:
        - 409 Conflict: If a user with the same username already exists.
        """
        if UserModel.query.filter_by(username=user_data["username"]).first():
            abort(409, message="User already exists")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}, 201


@blp.route("/users/<int:user_id>")
class User(MethodView):
    @blp.response(UserSchema)
    def get(self, user_id):
        """
        Get a user by ID

        Parameters:
        - user_id (int): The ID of the user to retrieve.

        Returns:
        - UserModel: The user object corresponding to the given ID.

        Raises:
        - 404 Not Found: If no user with the given ID exists.
        """
        return UserModel.query.get_or_404(user_id)

    def delete(self, user_id):
        """
        Delete a user by ID

        Parameters:
        - user_id (int): The ID of the user to delete.

        Returns:
        - dict: A dictionary containing the message "User deleted successfully".

        Raises:
        - 404 Not Found: If no user with the given ID exists.
        """
        user = UserModel.query.get(user_id)
        if user is None:
            abort(404, message="User not found")

        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted successfully"}
