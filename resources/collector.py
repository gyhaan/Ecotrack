"""
Blueprint for handling requests to the /collectors endpoint
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from database import db
from models import CollectorModel
from schemas import CollectorSchema


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
    @jwt_required()
    @blp.response(200, CollectorSchema(many=True))
    def get(self):
        """
        Get all collectors in the database

        Returns:
            dict: A dictionary containing all collectors in the database
        """
        jwt = get_jwt()

        if jwt.get("role") != "admin":
            abort(
                403,
                message="Admin privileges required to access resources"
                )
        return CollectorModel.query.all()

    @jwt_required()
    @blp.arguments(CollectorSchema)
    @blp.response(201, CollectorSchema)
    def post(self, collector_data):
        """
        Add a new collector to the database.

        Args:
            collector_data (dict): A dictionary containing the data
            for the new collector.

        Returns:
            tuple: A tuple containing the newly added collector and the
            HTTP status code 201.

        Raises:
            abort: If there is an error adding the collector to the database.

        """
        jwt = get_jwt()
        user_id = jwt.get("sub")

        collector = CollectorModel(**collector_data, user_id=user_id)

        try:
            db.session.add(collector)
            db.session.commit()
        except SQLAlchemyError as error:
            db.session.rollback()
            abort(400, message=str(error))

        return collector


@blp.route("/collectors/<collector_id>")
class Collector(MethodView):
    """
    Class for handling requests to the /collectors/<collector_id> endpoint
    """
    @jwt_required()
    @blp.response(200, CollectorSchema)
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
        jwt = get_jwt()
        user_role = jwt.get("role")
        if user_role == "admin":
            return CollectorModel.query.get_or_404(collector_id)
        abort(
            403,
            message="Admin/collector privileges required"
            )

    @jwt_required()
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
        jwt = get_jwt()

        if jwt.get("role") != "admin":
            abort(
                403,
                message="Admin privileges required to delete a collector"
                )

        collector = CollectorModel.query.get_or_404(collector_id)
        db.session.delete(collector)
        db.session.commit()
        return {"message": "Collector deleted"}
