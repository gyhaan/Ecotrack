"""
Entry point of the application
"""

from flask import Flask
from flask_smorest import Api

from resources.household import blp as HouseholdBlp
from resources.collector import blp as CollectorBlp
from resources.collection_dates import blp as CollectionDatesBlp
from resources.collection_requests import blp as CollectionRequestsBlp


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


api = Api(app)

# Register the blueprints
api.register_blueprint(HouseholdBlp)
api.register_blueprint(CollectorBlp)
api.register_blueprint(CollectionDatesBlp)
api.register_blueprint(CollectionRequestsBlp)
