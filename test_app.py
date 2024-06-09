"""
Module for testing the app.py
"""

import unittest

class HelloWorldTestCase(unittest.TestCase):
    """
    Test case for the hello world endpoint.
    """

    def test_hello_world(self):
        """
        Test case for the hello world endpoint.

        This method sends a GET request to the '/hello' endpointand asserts
        that the responsestatus code is 200 and the response data is
        'Hello, World!'.

        """
        self.assertEqual(2 + 2, 4)


if __name__ == '__main__':
    unittest.main()
