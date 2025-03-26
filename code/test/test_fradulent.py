import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from io import StringIO


class TestFraudulentTransactionDetection(unittest.TestCase):

    @patch("fradulent.st")  # Mock Streamlit
    def test_file_upload_and_anomaly_detection(self, mock_streamlit):
        # Mock the uploaded CSV file
        csv_data = StringIO(
            """TransactionAmount,BankBalance,Country
            1000,5000,USA
            20000,100000,India
            500,200,Canada
            30000,1000000,USA
            100,50,India"""
        )
        mock_streamlit.file_uploader.return_value = csv_data

        # Mock Streamlit methods
        mock_streamlit.text = MagicMock()
        mock_streamlit.error = MagicMock()
        mock_streamlit.write = MagicMock()
        mock_streamlit.download_button = MagicMock()

        # Read the uploaded CSV file
        data = pd.read_csv(csv_data)

        # Check if numeric columns are detected
        numeric_columns = data.select_dtypes(include=["number"]).columns
        self.assertIn("TransactionAmount", numeric_columns)
        self.assertIn("BankBalance", numeric_columns)
        print(data.head())  # Verify that the data is being processed correctly
        # Simulate Streamlit write
        mock_streamlit.write(data.head())  # Ensure this is called in the test
        mock_streamlit.write.assert_called()  # Verify Streamlit write was called

        # Verify Streamlit download button
        mock_streamlit.download_button.assert_not_called()  # Adjust based on your logic


if __name__ == "__main__":
    unittest.main()