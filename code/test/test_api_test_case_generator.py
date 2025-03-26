import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the parent directory to the path so we can import swagger.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from swagger import generate_bdd_swagger

class TestAPITestCaseGenerator(unittest.TestCase):

    @patch("swagger.Groq")  # Correctly mock Groq from swagger.py
    @patch("swagger.requests.get")  # Mock requests.get
    def test_generate_bdd_swagger_success(self, mock_requests_get, MockGroq):
        # Mock the HTTP response from requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = {"paths": {}}  # Mock Swagger data
        mock_requests_get.return_value = mock_response

        # Mock Groq client and its method
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Generated BDD Test Case"))]
        mock_client.chat.completions.create.return_value = mock_response
        MockGroq.return_value = mock_client

        # Call the function with a mock URL
        with patch.dict(os.environ, {"GROQ_API_KEY": "dummy_key"}):
            result = generate_bdd_swagger("http://example.com/swagger.json")

        self.assertIn("Generated BDD Test Case", result)

    @patch("swagger.requests.get")  # Mock requests.get
    def test_generate_bdd_swagger_missing_api_key(self, mock_requests_get):
        # Mock the HTTP response from requests.get
        mock_response = MagicMock()
        mock_response.json.return_value = {"paths": {}}  # Mock Swagger data
        mock_requests_get.return_value = mock_response

        # Clear environment to simulate missing API key
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                generate_bdd_swagger("http://example.com/swagger.json")
            self.assertEqual(str(context.exception), "GROQ_API_KEY is not set")


if __name__ == '__main__':
    unittest.main()