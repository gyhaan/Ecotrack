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


@app.get("/collectors")
def get_collectors():
    """
    Get all collectors in the database
    """
    return {"collectors": list(collectors.values())}


@app.post("/collectors")
def create_new_collector():
    """
    Add a new collector to the database
    """
    collector_data = request.get_json()
    collector_id = uuid.uuid4().hex
    new_collector = {**collector_data, "id": collector_id}
    collectors[collector_id] = new_collector
    return new_collector, 201


@app.get("/collectors/<collector_id>")
def get_collector(collector_id):
    """
    Get a collector by ID
    """
    try:
        return collectors[collector_id], 200
    except KeyError:
        return {"error": "Collector not found"}, 404


@app.delete("/collectors/<collector_id>")
def delete_collector(collector_id):
    """
    Delete a collector by ID
    """
    try:
        del collectors[collector_id]
        return {"message": "Collector deleted"}, 200
    except KeyError:
        return {"error": "Collector not found"}, 404