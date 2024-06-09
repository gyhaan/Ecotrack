"""
Entry point of the application
"""

import os

from flask import Flask
from flask_smorest import Api

from db import db
import models
from resources.household import blp as HouseholdBlp
from resources.collector import blp as CollectorBlp
from resources.collection_dates import blp as CollectionDatesBlp
from resources.collection_requests import blp as CollectionRequestsBlp


def create_app(db_url=None):
    app = Flask(__name__)

    # Configuration
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "EcoTrack API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui/api/docs"
    swagger_ui_url = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = swagger_ui_url
    database_uri = os.getenv("DATABASE_URL", "sqlite:///ecotrack.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    # Register the blueprints
    api.register_blueprint(HouseholdBlp)
    api.register_blueprint(CollectorBlp)
    api.register_blueprint(CollectionDatesBlp)
    api.register_blueprint(CollectionRequestsBlp)

    return app
