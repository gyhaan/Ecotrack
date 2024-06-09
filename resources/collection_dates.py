"""
Blueprint for handling collection dates
"""

import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import collection_dates


blp = Blueprint(
    "collection_dates",
    __name__,
    description="Operations on collection dates"
    )


@blp.route("/collection_dates")
class CollectionDates(MethodView):
    """
    Class for handling requests to the /collection_dates endpoint
    """
    def get(self):
        """
        Get all collection dates in the database

        Returns:
            dict: A dictionary containing all collection dates
            in the database
        """
        return {"collection_dates": list(collection_dates.values())}

    def post(self):
        """
        Add a new collection date to the database

        Returns:
            tuple: A tuple containing the newly added collection date and the
            HTTP status code 201
        """
        collection_date_data = request.get_json()
        collection_date_id = uuid.uuid4().hex
        new_collection_date = {
            **collection_date_data,
            "id": collection_date_id
            }
        collection_dates[collection_date_id] = new_collection_date
        return new_collection_date, 201


@blp.route("/collection_dates/<collection_date_id>")
class CollectionDate(MethodView):
    """
    Class for handling requests to the /collection_dates/<collection_date_id>
    endpoint
    """
    def get(self, collection_date_id):
        """
        Get a collection date by ID

        Args:
            collection_date_id (str): The ID of the collection date to
            retrieve

        Returns:
            tuple: A tuple containing the collection date and the
            HTTP status code 200
        """
        try:
            return collection_dates[collection_date_id], 200
        except KeyError:
            abort(404, message="Collection date not found.")

    def delete(self, collection_date_id):
        """
        Delete a collection date by ID

        Args:
            collection_date_id (str): The ID of the collection date to delete

        Returns:
            tuple: A tuple containing a message and the HTTP status code 200
        """
        try:
            del collection_dates[collection_date_id]
            return {"message": "Collection date deleted"}, 200
        except KeyError:
            abort(404, message="Collection date not found.")
