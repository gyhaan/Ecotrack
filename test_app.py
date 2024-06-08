"""
Module for testing the app.py
"""

import unittest
from app import app


class HelloWorldTestCase(unittest.TestCase):
    """
    Test case for the HelloWorld endpoint in the Flask app.
    """

    def setUp(self):
        """
        Set up the test environment before each test case.

        This method is called before each test case is executed.
        It initializes the Flask test client and sets the testing flag
        to True.

        """
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_world(self):
        """
        Test case for the hello world endpoint.

        This method sends a GET request to the '/hello' endpointand asserts
        that the responsestatus code is 200 and the response data is
        'Hello, World!'.

        """
        response = self.app.get('/hello')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Hello, World!')

    def tearDown(self):
        """
        Clean up the test environment after each test case.

        This method is called automatically after each test case is
        executed.

        """
        del self.app


if __name__ == '__main__':
    unittest.main()
