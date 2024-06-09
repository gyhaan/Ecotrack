"""
Blueprint for handling requests to the /collectors endpoint
"""

import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import collectors


blp = Blueprint(
    "collectors",
    __name__,
    description="Operations on collectors"
    )


@blp.route("/collectors")
class Collectors(MethodView):
    """
    Class for handling requests to the /collectors endpoint
    """
    def get(self):
        """
        Get all collectors in the database

        Returns:
            dict: A dictionary containing all collectors in the database
        """
        return {"collectors": list(collectors.values())}

    def post(self):
        """
        Add a new collector to the database

        Returns:
            tuple: A tuple containing the newly added collector and the
            HTTP status code 201
        """
        collector_data = request.get_json()
        collector_id = uuid.uuid4().hex
        new_collector = {**collector_data, "id": collector_id}
        collectors[collector_id] = new_collector
        return new_collector, 201


@blp.route("/collectors/<collector_id>")
class Collector(MethodView):
    """
    Class for handling requests to the /collectors/<collector_id> endpoint
    """
    def get(self, collector_id):
        """
        Get a collector by ID

        Args:
            collector_id (str): The ID of the collector to retrieve

        Returns:
            tuple: A tuple containing the requested collector and the
            HTTP status code 200

        Raises:
            404: If the collector with the given ID is not found
        """
        try:
            return collectors[collector_id], 200
        except KeyError:
            abort(404, message="Collector not found.")

    def delete(self, collector_id):
        """
        Delete a collector by ID

        Args:
            collector_id (str): The ID of the collector to delete

        Returns:
            dict: A dictionary containing a message indicating the collector
            was deleted

        Raises:
            404: If the collector with the given ID is not found
        """
        try:
            del collectors[collector_id]
            return {"message": "Collector deleted"}, 200
        except KeyError:
            abort(404, message="Collector not found.")
