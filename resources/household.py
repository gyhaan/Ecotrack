"""
Blueprint for household resources
"""

import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import households
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
    @blp.response(200, HouseholdSchema(many=True))
    def get(self):
        """
        Get all households in the database

        Returns:
            dict: A dictionary containing all households in the database
        """
        return {"households": list(households.values())}

    @blp.arguments(HouseholdSchema)
    def post(self, household_data):
        """
        Add a new household to the database

        Returns:
            tuple: A tuple containing the newly added household and the
            HTTP status code 201
        """
        household_id = uuid.uuid4().hex
        new_household = {**household_data, "id": household_id}
        households[household_id] = new_household
        return new_household, 201


@blp.route("/households/<household_id>")
class Household(MethodView):
    """
    Class for handling requests to the /households/<household_id> endpoint
    """
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
        try:
            return households[household_id], 200
        except KeyError:
            abort(404, message="Household not found.")

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
        try:
            del households[household_id]
            return {"message": "Household deleted"}, 200
        except KeyError:
            abort(404, message="Household not found.")
