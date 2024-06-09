"""
Blueprint for handling collection requests
"""

import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import CollectionRequestSchema


blp = Blueprint(
    "collection_requests",
    __name__,
    description="Operations on collection requests"
    )


@blp.route("/collection_requests")
class CollectionRequests(MethodView):
    """
    Class for handling requests to the /collection_requests endpoint
    """
    @blp.response(200, CollectionRequestSchema(many=True))
    def get(self):
        """
        Get all collection requests in the database

        Returns:
            dict: A dictionary containing all collection requests in
            the database
        """
        return collection_requests.values()

    @blp.arguments(CollectionRequestSchema)
    @blp.response(201, CollectionRequestSchema)
    def post(self):
        """
        Add a new collection request to the database

        Returns:
            tuple: A tuple containing the newly added collection request
            and the
            HTTP status code 201
        """
        collection_request_data = request.get_json()
        collection_request_id = uuid.uuid4().hex
        new_collection_request = {
            **collection_request_data,
            "id": collection_request_id
            }
        collection_requests[collection_request_id] = new_collection_request
        return new_collection_request


@blp.route("/collection_requests/<collection_request_id>")
class CollectionRequest(MethodView):
    """
    Class for handling requests to the
    /collection_requests/<collection_request_id> endpoint
    """
    @blp.response(200, CollectionRequestSchema)
    def get(self, collection_request_id):
        """
        Get a collection request by ID

        Args:
            collection_request_id (str): The ID of the collection request
            to retrieve

        Returns:
            tuple: A tuple containing the collection request and the
            HTTP status code 200
        """
        try:
            return collection_requests[collection_request_id]
        except KeyError:
            abort(404, message="Collection request not found.")

    def delete(self, collection_request_id):
        """
        Delete a collection request by ID

        Args:
            collection_request_id (str): The ID of the collection
            request to delete

        Returns:
            tuple: A tuple containing a message and the HTTP status code 200
        """
        try:
            del collection_requests[collection_request_id]
            return {"message": "Collection request deleted"}, 200
        except KeyError:
            abort(404, message="Collection request not found.")
