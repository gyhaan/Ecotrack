import unittest
import sys
import os

# Add the project directory to the sys.path to locate the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_jwt_extended import create_access_token
from app import create_app 
from db import db
from models import CollectorModel

class CollectorTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables and initialize the app."""
        # Create a Flask application configured for testing
        self.app = create_app("sqlite:///:memory:")  # Use in-memory database for testing
        self.client = self.app.test_client()  # Create a test client

        # Set up the application context for database operations
        with self.app.app_context():
            db.create_all()  # Create all database tables

            # Create a test collector user in the database
            collector_user = CollectorModel(user_id=1, allocated_area="Test Area")
            db.session.add(collector_user)  # Add the collector to the session
            db.session.commit()  # Commit the session to save the collector

            # Generate access tokens with roles for authorization testing
            self.admin_token = create_access_token(identity=1, additional_claims={"role": "admin"})
            self.collector_token = create_access_token(identity=1, additional_claims={"role": "collector"})

    def tearDown(self):
        """Clean up resources after each test."""
        with self.app.app_context():
            db.session.remove()  # Remove the session
            db.drop_all()  # Drop all database tables

    def test_get_all_collectors(self):
        """Test retrieving all collectors."""
        # Send a GET request to retrieve all collectors
        response = self.client.get(
            "/collectors",
            headers={"Authorization": f"Bearer {self.admin_token}"}  # Use admin token for authorization
        )
        self.assertEqual(response.status_code, 200)  # Check that the status code is 200 (OK)
        self.assertEqual(len(response.json), 1)  # Verify that one collector is returned

    def test_add_collector(self):
        """Test adding a new collector."""
        collector_data = {"allocated_area": "New Area"}  # Data for the new collector
        # Send a POST request to add a new collector
        response = self.client.post(
            "/collectors",
            json=collector_data,
            headers={"Authorization": f"Bearer {self.admin_token}"}  # Use admin token for authorization
        )
        self.assertEqual(response.status_code, 201)  # Check that the status code is 201 (Created)
        self.assertIn("user_id", response.json)  # Verify that 'user_id' is in the response JSON
        self.assertEqual(response.json["allocated_area"], "New Area")  # Verify that the allocated area is correct

    def test_get_collector_by_id(self):
        """Test retrieving a collector by ID."""
        # Send a GET request to retrieve a collector by ID
        response = self.client.get(
            "/collectors/1",
            headers={"Authorization": f"Bearer {self.admin_token}"}  # Use admin token for authorization
        )
        self.assertEqual(response.status_code, 200)  # Check that the status code is 200 (OK)
        self.assertIn("user_id", response.json)  # Verify that 'user_id' is in the response JSON
        self.assertEqual(response.json["user_id"], 1)  # Verify that the 'user_id' is correct

    def test_delete_collector(self):
        """Test deleting a collector by ID."""
        # Send a DELETE request to delete a collector by ID
        response = self.client.delete(
            "/collectors/1",
            headers={"Authorization": f"Bearer {self.admin_token}"}  # Use admin token for authorization
        )
        self.assertEqual(response.status_code, 200)  # Check that the status code is 200 (OK)
        self.assertEqual(response.json, {"message": "Collector deleted"})  # Verify the deletion message


if __name__ == "__main__":
    unittest.main()
