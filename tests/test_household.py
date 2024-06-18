import unittest
import sys
import os

# Add the project directory to the sys.path to locate the app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_jwt_extended import create_access_token
from app import create_app  # Ensure this matches the actual application module
from db import db
from models import HouseholdModel, AdminModel

class HouseholdTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables and initialize the app."""
        # Create a Flask application configured for testing
        self.app = create_app("sqlite:///:memory:")  # Use in-memory database for testing
        self.client = self.app.test_client()  # Create a test client

        # Set up the application context for database operations
        with self.app.app_context():
            db.create_all()  # Create all database tables

            # Create a test admin user in the database
            admin_user = AdminModel(user_id=1)
            db.session.add(admin_user)  # Add the admin to the session
            db.session.commit()  # Commit the session to save the admin

            # Generate access tokens with roles for authorization testing
            self.admin_token = create_access_token(identity=1, additional_claims={"role": "admin"})

    def tearDown(self):
        """Clean up resources after each test."""
        with self.app.app_context():
            db.session.remove()  # Remove the session
            db.drop_all()  # Drop all database tables

    def test_get_all_households(self):
        """Test retrieving all households."""
        # Send a GET request to retrieve all households
        response = self.client.get(
            "/households",
            headers={"Authorization": f"Bearer {self.admin_token}"}  # Use admin token for authorization
        )
        self.assertEqual(response.status_code, 200)  # Check that the status code is 200 (OK)
        self.assertEqual(len(response.json), 0)  # Verify that no households are returned initially

    def test_add_household(self):
        """Test adding a new household."""
        household_data = {"house_number": "123", "area": "Main Street"}  # Data for the new household
        # Send a POST request to add a new household
        response = self.client.post(
            "/households",
            json=household_data,
            headers={"Authorization": f"Bearer {self.admin_token}"}  # Use admin token for authorization
        )
        self.assertEqual(response.status_code, 201)  # Check that the status code is 201 (Created)
        self.assertIn("house_number", response.json)  # Verify that 'house_number' is in the response JSON
        self.assertEqual(response.json["house_number"], "123")  # Verify that the house number is correct

    def test_get_household_by_id(self):
        """Test retrieving a household by ID."""
        # First, add a household
        new_household = HouseholdModel(house_number='124', area='First Street', user_id=1)
        with self.app.app_context():
            db.session.add(new_household)
            db.session.commit()
            household_id = new_household.id

        # Send a GET request to retrieve the household by ID
        response = self.client.get(
            f"/households/{household_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"}  # Use admin token for authorization
        )
        self.assertEqual(response.status_code, 200)  # Check that the status code is 200 (OK)
        self.assertIn("house_number", response.json)  # Verify that 'house_number' is in the response JSON
        self.assertEqual(response.json["house_number"], '124')  # Verify that the house number is correct

    def test_delete_household(self):
        """Test deleting a household by ID."""
        # First, add a household to delete
        new_household = HouseholdModel(house_number='125', area='Second Street', user_id=1)
        with self.app.app_context():
            db.session.add(new_household)
            db.session.commit()
            household_id = new_household.id

        # Send a DELETE request to delete the household by ID
        response = self.client.delete(
            f"/households/{household_id}",
            headers={"Authorization": f"Bearer {self.admin_token}"}  # Use admin token for authorization
        )
        self.assertEqual(response.status_code, 200)  # Check that the status code is 200 (OK)
        self.assertEqual(response.json, {"message": "Household deleted"})  # Verify the deletion message

        # Verify household is removed from the database
        with self.app.app_context():
            household = db.session.get(HouseholdModel, household_id)
            self.assertIsNone(household)

    def test_delete_household_unauthorized(self):
        """Test unauthorized deletion of a household by ID."""
        # Add a household to delete
        new_household = HouseholdModel(house_number='126', area='Third Street', user_id=1)
        with self.app.app_context():
            db.session.add(new_household)
            db.session.commit()
            household_id = new_household.id

        # Test unauthorized deletion (no token provided)
        response = self.client.delete(f"/households/{household_id}")
        self.assertEqual(response.status_code, 401)  # Check that the status code is 401 (Unauthorized)


if __name__ == "__main__":
    unittest.main()
