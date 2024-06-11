"""
Blueprint for household resources
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import db
from models import HouseholdModel
from schemas import HouseholdSchema


blp = Blueprint(
    "households",
    __name__,
    description="Operations on households"
)


@blp.route("/households")
class Households(MethodView):
    """
    Class for handling requests to the /households endpoint
    """
    @jwt_required()
    @blp.response(200, HouseholdSchema(many=True))
    def get(self):
        """
        Get all households in the database

        Returns:
            dict: A dictionary containing all households in the database
        """
        jwt = get_jwt()
        if jwt.get("role") == "admin":
            return HouseholdModel.query.all()
        abort(403, message="Admin privileges required to access resources")


    @jwt_required()
    @blp.arguments(HouseholdSchema)
    @blp.response(201, HouseholdSchema)
    def post(self, household_data):
        """
        Add a new household to the database

        Args:
            household_data (dict): A dictionary containing the data for the
            new household

        Returns:
            tuple: A tuple containing the newly added household and the
            HTTP status code 201

        Raises:
            abort: If there is an error adding the household to the database

        """
        household = HouseholdModel(**household_data)

        try:
            db.session.add(household)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(400, message=str(error))

        return household


@blp.route("/households/<household_id>")
class Household(MethodView):
    """
    Class for handling requests to the /households/<household_id> endpoint
    """
    @jwt_required()
    @blp.response(200, HouseholdSchema)
    def get(self, household_id):
        """
        Get a household by ID

        Args:
            household_id (str): The ID of the household to retrieve

        Returns:
            tuple: A tuple containing the requested household and the
            HTTP status code 200

        Raises:
            404: If the household with the given ID is not found
        """
        jwt = get_jwt()
        user_role = jwt.get("role")

        if user_role in ("admin", "household"):
            return HouseholdModel.query.get_or_404(household_id)
        abort(403, message="Household or admin privileges required to access resources")

    @jwt_required()
    def delete(self, household_id):
        """
        Delete a household by ID

        Args:
            household_id (str): The ID of the household to delete

        Returns:
            tuple: A tuple containing a message indicating the deletion and
            the HTTP status code 200

        Raises:
            404: If the household with the given ID is not found
        """

        jwt = get_jwt()
        if jwt.get("role") != "admin":
            abort(403, message="Admin privileges required to delete a household")

        household = HouseholdModel.query.get_or_404(household_id)

        db.session.delete(household)
        db.session.commit()

        return {"message": "Household deleted"}, 200
