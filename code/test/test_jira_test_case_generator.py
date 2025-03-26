import unittest
from unittest.mock import patch, MagicMock
import os
from jira_test_case_generator import generate_bdd_swagger, generate_bdd_from_text


class TestJiraTestCaseGenerator(unittest.TestCase):

    @patch("jira_test_case_generator.Groq")  # Mock the Groq class
    def test_generate_bdd_swagger_success(self, MockGroq):
        # Mock the Groq client and its method
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Generated BDD Test Case"))]
        mock_client.chat.completions.create.return_value = mock_response
        MockGroq.return_value = mock_client

        swagger_data = {
            "paths": {
                "/login": {
                    "post": {
                        "summary": "User login",
                        "responses": {
                            "200": {
                                "description": "Successful login"
                            }
                        }
                    }
                }
            }
        }

        with patch.dict(os.environ, {"GROQ_API_KEY": "dummy_key"}):
            result = generate_bdd_swagger(swagger_data)
            self.assertEqual(result, "Generated BDD Test Case")

    def test_generate_bdd_swagger_missing_api_key(self):
        # Clear environment to simulate missing API key
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                generate_bdd_swagger({"paths": {}})
            self.assertEqual(str(context.exception), "GROQ_API_KEY is not set")

    @patch("jira_test_case_generator.Groq")  # Mock the Groq class
    def test_generate_bdd_from_text_success(self, MockGroq):
        # Mock the Groq client and its method
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Generated BDD Test Case from Text"))]
        mock_client.chat.completions.create.return_value = mock_response
        MockGroq.return_value = mock_client

        requirements = "As a user, I want to log in so that I can access my account."

        with patch.dict(os.environ, {"GROQ_API_KEY": "dummy_key"}):
            result = generate_bdd_from_text(requirements)
            self.assertEqual(result, "Generated BDD Test Case from Text")

    def test_generate_bdd_from_text_missing_api_key(self):
        # Clear environment to simulate missing API key
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                generate_bdd_from_text("Some requirements")
            self.assertEqual(str(context.exception), "GROQ_API_KEY is not set")


if __name__ == "__main__":
    unittest.main()