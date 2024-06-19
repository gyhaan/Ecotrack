import unittest
import sys
import os
from flask_jwt_extended import create_access_token
from app import create_app
from db import db
from models import CollectorModel
# Add the project directory to the sys.path to locate the app module
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


class CollectorTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables and initialize the app."""
        # Create a Flask application configured for testing
        self.app = create_app("sqlite:///:memory:")
        self.client = self.app.test_client()

        # Set up the application context for database operations
        with self.app.app_context():
            db.create_all()
            # Create a test collector user in the database
            collector_user = CollectorModel(
                user_id=1, allocated_area="Test Area")
            db.session.add(collector_user)
            db.session.commit()

            # Generate access tokens with roles for authorization testing
            self.admin_token = create_access_token(
                identity=1, additional_claims={"role": "admin"})
            self.collector_token = create_access_token(
                identity=1, additional_claims={"role": "collector"})

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
            headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_add_collector(self):
        """Test adding a new collector."""
        collector_data = {"allocated_area": "New Area"}
        # Send a POST request to add a new collector
        response = self.client.post(
            "/collectors",
            json=collector_data,
            headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("user_id", response.json)
        self.assertEqual(response.json["allocated_area"], "New Area")

    def test_get_collector_by_id(self):
        """Test retrieving a collector by ID."""
        # Send a GET request to retrieve a collector by ID
        response = self.client.get(
            "/collectors/1",
            headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", response.json)
        self.assertEqual(response.json["user_id"], 1)

    def test_delete_collector(self):
        """Test deleting a collector by ID."""
        # Send a DELETE request to delete a collector by ID
        response = self.client.delete(
            "/collectors/1",
            headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Collector deleted"})


if __name__ == "__main__":
    unittest.main()
