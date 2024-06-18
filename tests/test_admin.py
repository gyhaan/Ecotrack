import sys
import os
import unittest
from flask_jwt_extended import create_access_token
from app import create_app
from db import db
from models.admin import AdminModel


# Add the directory containing app.py to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class AdminTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables and initialize the app."""
        # Use in-memory database for testing
        self.app = create_app("sqlite:///:memory:")  
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            # Create a test admin user
            admin_user = AdminModel(user_id=1)
            db.session.add(admin_user)
            db.session.commit()

            # Generate access tokens
            self.admin_token = create_access_token(
                identity=1, additional_claims={"role": "admin"})
            self.new_admin_token = create_access_token(
                identity=2, additional_claims={"role": "admin"})

    def tearDown(self):
        """Clean up resources after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_admins(self):
        """Test retrieving all admins."""
        response = self.client.get(
            "/admins",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_add_admin(self):
        """Test adding a new admin."""
        with self.app.app_context():
            response = self.client.post(
                "/admins",
                headers={"Authorization": f"Bearer {self.new_admin_token}"}
            )
            self.assertEqual(response.status_code, 201)
            self.assertIn("user_id", response.json)
            self.assertEqual(response.json["user_id"], 2)

    def test_get_admin_by_id(self):
        """Test retrieving an admin by ID."""
        response = self.client.get(
            "/admins/1",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", response.json)
        self.assertEqual(response.json["user_id"], 1)

    def test_delete_admin(self):
        """Test deleting an admin by ID."""
        response = self.client.delete(
            "/admins/1",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")


if __name__ == "__main__":
    unittest.main()
