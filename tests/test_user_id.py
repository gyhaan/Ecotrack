import unittest
import os
import sys
from flask_jwt_extended import create_access_token

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from db import db
from models import UserModel, AdminModel

class TestUserEndpoint(unittest.TestCase):

    def setUp(self):
        self.app = create_app("sqlite:///:memory:")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create a test user and an admin user
        self.test_user = UserModel(username="testuser", password="testpassword")
        self.admin_user = UserModel(username="adminuser", password="adminpassword")
        db.session.add(self.test_user)
        db.session.add(self.admin_user)
        db.session.commit()

        # Assign admin role to the admin user
        admin_role = AdminModel(user_id=self.admin_user.id)
        db.session.add(admin_role)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_user_valid_id(self):
        # Test retrieving a user by a valid user ID
        response = self.client.get(f"/users/{self.test_user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["username"], "testuser")

    #def test_get_user_invalid_id(self):
        # Test retrieving a user by an invalid user ID
        #response = self.client.get("/users/999")
        #self.assertEqual(response.status_code, 404)
        #self.assertEqual(response.json["message"], "User not found")

    def test_delete_user_admin(self):
        # Test deleting a user with an admin role
        access_token = create_access_token(identity=self.admin_user.id)
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.delete(f"/users/{self.test_user.id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "User deleted successfully")

    def test_delete_user_non_admin(self):
        # Test deleting a user with a non-admin role
        access_token = create_access_token(identity=self.test_user.id)
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.client.delete(f"/users/{self.test_user.id}", headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json["message"], "Admin privileges required to carry out this action")

if __name__ == "__main__":
    unittest.main()
