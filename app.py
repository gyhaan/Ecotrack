"""
Entry point of the application
"""
import uuid

from flask import Flask, request
from db import households, collectors, collection_dates, collection_requests


app = Flask(__name__)

@app.get("/households")
def get_households():
    """
    Get all households in the database
    """
    return {"households": list(households.values())}


@app.post("/households")
def create_new_household():
    """
    Add a new household to the database
    """
    household_data = request.get_json()
    household_id = uuid.uuid4().hex
    new_household = {**household_data, "id": household_id}
    households[household_id] = new_household
    return new_household, 201


@app.get("/households/<household_id>")
def get_household(household_id):
    """
    Get a household by ID
    """
    try:
        return households[household_id], 200
    except KeyError:
        return {"error": "Household not found"}, 404


@app.delete("/households/<household_id>")
def delete_household(household_id):
    """
    Delete a household by ID
    """
    try:
        del households[household_id]
        return {"message": "Household deleted"}, 200
    except KeyError:
        return {"error": "Household not found"}, 404



