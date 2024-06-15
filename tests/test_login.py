import sys
import os
import unittest
from unittest.mock import patch
from passlib.hash import pbkdf2_sha256

# Add the project root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models import UserModel

class UserLoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.app.app_context().push()  # Push application context once for setup
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('models.UserModel.query')
    def test_user_login_success(self, mock_query):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        hashed_password = pbkdf2_sha256.hash(user_data['password'])

        mock_user = UserModel(
            username=user_data['username'],
            password=hashed_password
        )
        mock_query.filter_by.return_value.first.return_value = mock_user

        response = self.client.post('/login', json=user_data)
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['message'], 'Logged in successfully')
        self.assertIn('access_token', response_json)
        self.assertIn('role', response_json)

    @patch('models.UserModel.query')
    def test_user_login_incorrect_password(self, mock_query):
        user_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        correct_password = pbkdf2_sha256.hash('correctpassword')

        mock_user = UserModel(
            username=user_data['username'],
            password=correct_password
        )
        mock_query.filter_by.return_value.first.return_value = mock_user

        response = self.client.post('/login', json=user_data)
        response_json = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['message'], 'Incorrect username or password')

    @patch('models.UserModel.query')
    def test_user_login_nonexistent_user(self, mock_query):
        user_data = {
            'username': 'nonexistentuser',
            'password': 'any_password'
        }

        mock_query.filter_by.return_value.first.return_value = None

        response = self.client.post('/login', json=user_data)
        response_json = response.get_json()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json['message'], 'Incorrect username or password')

if __name__ == '__main__':
    unittest.main()
